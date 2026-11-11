"""Tests for skills/monitor/scripts/monitor-pr, run against fixture PR snapshots.

Run with: python3 -m unittest discover tests
"""

from __future__ import annotations

import contextlib
import importlib.machinery
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "monitor" / "scripts" / "monitor-pr"
loader = importlib.machinery.SourceFileLoader("monitor_pr", str(SCRIPT))
spec = importlib.util.spec_from_loader("monitor_pr", loader)
assert spec
monitor = importlib.util.module_from_spec(spec)
sys.modules["monitor_pr"] = monitor
loader.exec_module(monitor)

REPO = "owner/repo"
OLD = "a" * 40
HEAD = "b" * 40
OLD_AT = "2026-11-10T10:00:00Z"
HEAD_AT = "2026-11-10T12:00:00Z"
LATER = "2026-11-10T12:05:00Z"
VIEWER = "adelrodriguez"
MARKER = "> [!NOTE]\n> 🤖 **Claude (on behalf of adelrodriguez)**"

CLEAN = "Bugbot Review\n**Final Result:** Bugbot completed review - no issues found! ✅"
FOUND = "Bugbot Review\n**Final Result:** Bugbot completed review and found 1 potential issue."
CANCELLED = "Bugbot Review\n✅ ❌ Run was cancelled (2m 1s)\n**Result:** Bugbot run cancelled because the review request was cancelled"


def bot(login):
    return {"login": f"{login}[bot]", "kind": "Bot"}


def user(login=VIEWER):
    return {"login": login, "kind": "User"}


def check(name, conclusion, text, app=""):
    title, _, summary = text.partition("\n")
    return {
        "kind": "CheckRun", "name": name, "status": "COMPLETED", "conclusion": conclusion,
        "title": title, "summary": summary, "startedAt": HEAD_AT, "completedAt": LATER,
        "detailsUrl": f"https://example.com/{name}", "checkSuite": {"app": {"slug": app} if app else None},
    }


def ci_check():
    return check("test", "SUCCESS", "ok\nall good", "github-actions")


def review(login, state, commit, body, at=LATER):
    return {
        "databaseId": abs(hash((login, commit, body))) % 10**8, "url": f"https://example.com/r/{login}",
        "state": state, "body": body, "submittedAt": at, "commit": {"oid": commit}, "author": bot(login),
    }


def comment(body, at=LATER, author=None):
    return {
        "databaseId": abs(hash((body, at))) % 10**8, "url": "https://example.com/c", "body": body,
        "createdAt": at, "lastEditedAt": None, "author": author or user(),
    }


def snapshot(checks=(), reviews=(), comments=(), earlier=(), merge_state="CLEAN"):
    return {
        "url": "https://github.com/owner/repo/pull/1", "state": "OPEN", "headRefOid": HEAD,
        "baseRefName": "main", "mergeStateStatus": merge_state, "baseRef": {"target": {"oid": "c" * 40}},
        "commits": {"nodes": [{"commit": {"committedDate": HEAD_AT, "statusCheckRollup": {"contexts": {"nodes": [ci_check(), *checks]}}}}]},
        "reviews": {"nodes": list(reviews)},
        "comments": {"nodes": list(comments)},
        "reactions": {"nodes": []},
        "reviewThreads": {"nodes": []},
        # Check names on the PR's recent commits, as the query's `earlier` field returns them.
        "earlier": {"nodes": [
            {"commit": {"statusCheckRollup": {"contexts": {"nodes": [
                {"kind": "CheckRun", "name": name, "checkSuite": {"app": {"slug": app}}} for name, app in earlier
            ]}}}},
        ]},
    }


# Bugbot reviewed the first push and found nothing.
BUGBOT_REVIEWED_OLD = review("cursor", "COMMENTED", OLD, "<!-- BUGBOT_REVIEW --> Cursor Bugbot has reviewed your changes and found no issues.", OLD_AT)
PULLFROG_APPROVED = review("pullfrog", "APPROVED", HEAD, "✅ No new issues found.")
PULLFROG_FINDINGS = review("pullfrog", "COMMENTED", HEAD, "> [!IMPORTANT]\n> Folder ownership checks miss aliases.")


def states(pr, require):
    status = monitor.analyze(pr, VIEWER, {"test"}, require, set())
    return {a.agent.name: a.state for a in status.agents}


class AgentStates(unittest.TestCase):
    def test_first_push_agent_waits_for_its_first_review(self):
        self.assertEqual(states(snapshot(), ["bugbot"]), {"bugbot": "waiting"})

    def test_first_push_agent_that_reviewed_an_earlier_push_is_unrequested(self):
        self.assertEqual(states(snapshot(reviews=[BUGBOT_REVIEWED_OLD]), ["bugbot"]), {"bugbot": "unrequested"})

    def test_check_run_on_an_earlier_push_counts_as_its_first_review(self):
        # A clean Bugbot run leaves only a check run, with no review or comment.
        pr = snapshot(earlier=[("Cursor Bugbot", "cursor")])
        self.assertEqual(states(pr, ["bugbot"]), {"bugbot": "unrequested"})

    def test_request_that_starts_with_the_command_counts(self):
        for request in ("@cursor review", "bugbot run"):
            pr = snapshot(reviews=[BUGBOT_REVIEWED_OLD], comments=[comment(f"{request}\n\n{MARKER}")])
            self.assertEqual(states(pr, ["bugbot"]), {"bugbot": "waiting"}, request)

    def test_longer_word_is_not_a_request(self):
        pr = snapshot(reviews=[BUGBOT_REVIEWED_OLD], comments=[comment("@cursor reviewer, see above")])
        self.assertEqual(states(pr, ["bugbot"]), {"bugbot": "unrequested"})

    def test_request_after_the_marker_does_not_count(self):
        # Bugbot ignored these on sanely #159 and #161.
        pr = snapshot(reviews=[BUGBOT_REVIEWED_OLD], comments=[comment(f"{MARKER}\n\n@cursor review")])
        self.assertEqual(states(pr, ["bugbot"]), {"bugbot": "unrequested"})

    def test_request_before_the_head_does_not_count(self):
        pr = snapshot(reviews=[BUGBOT_REVIEWED_OLD], comments=[comment("@cursor review", at=OLD_AT)])
        self.assertEqual(states(pr, ["bugbot"]), {"bugbot": "unrequested"})

    def test_on_request_agent_is_unrequested_before_it_ever_reviews(self):
        self.assertEqual(states(snapshot(), ["codex"]), {"codex": "unrequested"})

    def test_every_push_agent_waits_on_a_new_head(self):
        old = review("pullfrog", "APPROVED", OLD, "✅ No new issues found.", OLD_AT)
        self.assertEqual(states(snapshot(reviews=[old]), ["pullfrog"]), {"pullfrog": "waiting"})

    def test_cancelled_run_on_the_head_failed(self):
        pr = snapshot(checks=[check("Cursor Bugbot", "NEUTRAL", CANCELLED, "cursor")], reviews=[BUGBOT_REVIEWED_OLD])
        self.assertEqual(states(pr, ["bugbot"]), {"bugbot": "failed"})

    def test_bugbot_check_results(self):
        clean = snapshot(checks=[check("Cursor Bugbot", "SUCCESS", CLEAN, "cursor")])
        found = snapshot(checks=[check("Cursor Bugbot", "NEUTRAL", FOUND, "cursor")])
        self.assertEqual(states(clean, ["bugbot"]), {"bugbot": "approved"})
        self.assertEqual(states(found, ["bugbot"]), {"bugbot": "findings"})


class FakeGitHub:
    """Answers the REST calls that poll() makes, from per-commit Bugbot check runs."""

    def __init__(self, runs):
        self.runs = runs  # sha -> list of check runs, oldest commit first

    def __call__(self, *args, ok=(0,)):
        path = args[1]
        if path.startswith(f"repos/{REPO}/pulls/1/commits"):
            return json.dumps([{"sha": sha} for sha in self.runs])
        if path.startswith(f"repos/{REPO}/commits/"):
            sha = path.split("/")[4]
            return json.dumps({"check_runs": self.runs.get(sha, [])})
        if path.startswith(f"repos/{REPO}/compare/"):
            return "0\n"
        raise AssertionError(f"unexpected gh call: {args}")


def rest_run(conclusion, text):
    title, _, summary = text.partition("\n")
    return {"name": "Cursor Bugbot", "conclusion": conclusion, "app": {"slug": "cursor"}, "output": {"title": title, "summary": summary}}


class Poll(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.patches = {
            "STATE_DIR": Path(self.tmp.name),
            "required_check_names": lambda repo, base: {"test"},
            "expected_agents": lambda repo: set(),
            "gh": FakeGitHub({OLD: [rest_run("success", CLEAN)], HEAD: []}),
        }
        self.saved = {name: getattr(monitor, name) for name in self.patches}
        for name, value in self.patches.items():
            setattr(monitor, name, value)

    def tearDown(self):
        for name, value in self.saved.items():
            setattr(monitor, name, value)
        self.tmp.cleanup()

    def poll(self, pr, require):
        monitor.fetch = lambda repo, number: (pr, VIEWER)
        args = monitor.Args()
        args.require = require
        args.stall = float("inf")  # the fixtures are older than any stall limit
        watcher = monitor.Watcher(REPO, 1, args)
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            watcher.poll()  # the first poll records the checks
            try:
                watcher.poll()
            except SystemExit as exit:
                return exit.code, out.getvalue()
        return None, out.getvalue()

    def test_push_agent_findings_come_before_any_request(self):
        code, out = self.poll(snapshot(reviews=[BUGBOT_REVIEWED_OLD, PULLFROG_FINDINGS]), ["pullfrog", "bugbot"])
        self.assertEqual(code, 1)
        self.assertIn("pullfrog left findings", out)
        self.assertNotIn("@cursor review", out)

    def test_request_waits_for_push_agents(self):
        pending = review("pullfrog", "COMMENTED", OLD, "✅ No new issues found.", OLD_AT)
        code, _ = self.poll(snapshot(reviews=[BUGBOT_REVIEWED_OLD, pending]), ["pullfrog", "bugbot"])
        self.assertIsNone(code)

    def test_request_once_everything_else_is_ready(self):
        code, out = self.poll(snapshot(reviews=[BUGBOT_REVIEWED_OLD, PULLFROG_APPROVED]), ["pullfrog", "bugbot"])
        self.assertEqual(code, 1)
        self.assertIn("ready for an on-request review", out)
        self.assertIn('post "@cursor review" as the first line', out)
        self.assertIn(f"bugbot approved {OLD[:7]}; compare: git diff {OLD[:7]}..{HEAD[:7]}", out)

    def test_no_earlier_approval_when_the_last_review_had_findings(self):
        monitor.gh = FakeGitHub({OLD: [rest_run("success", CLEAN)], "d" * 40: [rest_run("neutral", FOUND)], HEAD: []})
        code, out = self.poll(snapshot(reviews=[BUGBOT_REVIEWED_OLD, PULLFROG_APPROVED]), ["pullfrog", "bugbot"])
        self.assertEqual(code, 1)
        self.assertIn("ready for an on-request review", out)
        self.assertNotIn("bugbot approved", out)

    def test_ready_after_a_requested_review_approves(self):
        pr = snapshot(
            checks=[check("Cursor Bugbot", "SUCCESS", CLEAN, "cursor")],
            reviews=[BUGBOT_REVIEWED_OLD, PULLFROG_APPROVED],
            comments=[comment("@cursor review")],
        )
        code, out = self.poll(pr, ["pullfrog", "bugbot"])
        self.assertEqual(code, 0, out)
        self.assertIn("ready on", out)


if __name__ == "__main__":
    unittest.main()

---
name: takeover
description: Use when the user asks to take over a pull request, branch, or agent thread.
metadata:
  reference:
    - "https://github.com/t3dotgg/tstack/blob/main/skills/takeover/SKILL.md"
---

# Take over existing work

Finish the goal of a pull request, branch, or thread that someone else started, and keep the credit with the people who did the work. The earlier implementation is context, not a plan you must defend.

A takeover request authorizes you to continue on the original branch: rebase it, push to it with `--force-with-lease`, and update the original PR's description. It does not authorize merging or closing the original PR.

## Read the source

Read the source the user names:

- **PR.** Read the description, every review finding, every comment, and the diff with `gh pr view <pr> --comments` and `gh pr diff <pr>`.
- **Branch.** Read `git log origin/<base>..<branch>` and the diff against its base. Find its PR with `gh pr list --head <branch>`.
- **T3 thread.** Read it with `t3_thread_read`, including the user's later corrections. Find the worktree it worked in, its branch, and that branch's PR. Check the worktree for uncommitted changes with `git status --porcelain`.

The step is done when you have recorded the original goal in one sentence, the head SHA as `<original-head>`, the branch on GitHub as `<head-branch>`, the base branch as `<base>`, the PR if one exists, any uncommitted work, and every open finding and correction.

## Choose the mode

Use the first mode that applies:

| Mode | When | Branch you push | PR |
|---|---|---|---|
| Stacked | The user asks to stack on the original | A new branch, with `<head-branch>` as `<base>` | A new PR |
| Replacement | The user asks for a new PR, or you cannot push to `<head-branch>` | A new branch | A new PR |
| In place | Every other case | `<head-branch>` | The original PR, or a new one when none exists |

You cannot push to `<head-branch>` when your permission on the repository is below `WRITE`:

```bash
gh repo view --json viewerPermission
```

When the source has a PR, you also cannot push when the PR comes from a fork:

```bash
gh pr view <pr> --json isCrossRepository
```

The step is done when you have recorded the mode and, for a fallback to Replacement, the reason.

## Start the continuation branch

Create a local branch from the original head, so the original commits and their authors carry over unchanged:

```bash
git switch -c <local-branch> <original-head>
```

In place, push this branch to `<head-branch>` in later steps. In a T3 worktree, the local branch name often differs from `<head-branch>`.

Commit uncommitted work from the source on this branch with its author's identity, and say in the message where it came from.

The step is done when `git log` on the local branch shows every original commit with its original author.

## Update it to the base

Record `<original-head>` as `<old-head>`, and `git merge-base origin/<base> <original-head>` as `<old-base>`. Then follow these sections of the `refresh` skill on the local branch: "List what merged since", "Check for overlap", "Rebase the branch", and "Verify the refreshed PR".

Check the source again before you continue, because its author may have pushed since you read it. Fetch, then add only their new commits, so the commits you dropped while refreshing stay dropped:

```bash
git cherry-pick <old-head>..origin/<head-branch>
```

Then record `origin/<head-branch>` as `<old-head>`, so the next push leases the head you just took in. When `<head-branch>` does not exist on `origin`, use the local `<head-branch>` in both places. When the PR comes from a fork, run `git fetch origin pull/<pr>/head` and use `FETCH_HEAD` in both places.

The step is done when the branch is rebased onto `origin/<base>` and includes the source's latest commits.

## Finish the goal

Fix each open finding and correction you recorded, in commits of your own. Keep every behavior and surface the original meant to ship.

The step is done when every recorded finding and correction is fixed or has a written reason for declining it.

## Keep the credit

- Keep each original commit's author and every existing `Co-authored-by` trailer.
- Take each contributor's name and email from `git log --format='%an <%ae>'` on the original commits, or from their GitHub profile. Never guess an email.
- When the repository squash-merges, add a `Co-authored-by` trailer for each human contributor to the PR description, so the squash commit keeps them.
- For a new PR, name the original contributors in its description and link the original PR. The `pr` skill's model attribution line does not replace this credit.

The step is done when every human who committed to the original work appears as an author or a verified co-author.

## Push and watch the PR

In place, push with the command in the `refresh` skill's "Push and update the PR" section, using `<old-head>` as the lease. When `<head-branch>` does not exist on `origin`, such as a thread's branch that was never pushed, push it with `git push -u origin HEAD:<head-branch>` instead.

When the lease fails, the author pushed again. Repeat the source check from "Update it to the base", run the repository's checks again, and push again. Update the original PR's description to match what the branch now does, following the `pr` skill. When the branch has no PR, file one with the `pr` skill.

For a Replacement or Stacked continuation, push the new branch and file its PR with the `pr` skill.

Then watch the PR with the `monitor` skill.

The step is done when the `monitor` skill reports the PR ready, or reports a blocker.

## Check the takeover

- In place, the PR's head on GitHub equals the local `HEAD`, and the original PR is still open.
- For a Replacement or Stacked continuation, the original branch and PR are unchanged.
- Every original commit is on the pushed branch with its original author.
- The branch is rebased onto `origin/<base>` and includes the source's latest commits.
- Every recorded finding and correction is fixed or declined with a reason.
- Every human contributor is credited with a verified identity.

## Return the result

When you fell back to a Replacement PR, say why on the report's first line. Return the PR URL, the mode, and the head SHA. Then report what you took over, what you changed, how you kept the credit, and any decision left for the user, such as closing the original PR after a Replacement.

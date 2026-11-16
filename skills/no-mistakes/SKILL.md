---
name: no-mistakes
description: Take a task to a ready pull request with a council-approved design, a clean rebuild, and evidence for every claim.
disable-model-invocation: true
---

# No mistakes

Take the task to a pull request that is ready to merge, with no mistake left for a reviewer to find. Apply the extra care to proof and review, not to scope. The change stays as small as the goal allows.

## Use these permissions

A no-mistakes request grants the testing and branch permissions of the `full-stop` skill and keeps the pull request unmerged as `full-stop` describes. When the user also says "full send", follow `full-send` to the merge instead.

The council approves the design and the final diff in place of the user. Do not wait for the user's agreement on a design, a dry run, or a structural change, even where another skill or the user's instructions ask for it. The request also approves `prune`'s proven removals, and counts as the fix request for `footguns` and `harden-ui`. Make the decisions of `footguns` and `harden-ui` yourself, record them in the ledger, and skip their closing questions. List `prune`'s Ask candidates as follow-ups.

Ask the user only under `full-send`'s "Ask when blocked" conditions, when an ambiguity changes a claim, when a finding stays disputed after two replies, as `code-review` describes, or when a council reaches its round limit without approval. Ask through the harness's question tool, as `full-send` describes, and do not start the next step until the user answers. Record each answer in the ledger. For a disputed finding or a round limit, the user's decision on each open finding resolves it, and a request for another pass starts a new council pass. When such an answer does neither, stop the run and report.

## Choose the council

Use the `council-review` skill with three reviewers on at least two providers. When the user names models, use those instead. When the reviewers end up on one provider, record the shortfall for the report. When no subagent tool is available, stop the run and report, because the council cannot run.

Each council pass gets three rounds for a design and five for code. Revisions inside a pass count toward its limit. A design sent back from the spike or the rebuild, and a re-review after the pull request opens, each start a new pass.

Every round reviews the whole proposal and ledger, or the whole diff from the base. In the reviewer brief, this replaces the instructions in `council-review` and `code-review` to check only revised sections, open findings, or changed code.

The council approves when every member approves the same version, when a round returns only nits, or when the user decided each finding that stayed open.

The step is done when the reviewers are named, three or the set the user named, and they cover at least two providers or the shortfall is recorded.

## Write the claims

Read the task, the code it touches, and the repository's `AGENTS.md`, `CODING_STANDARDS.md`, and `GLOSSARY.md` when they exist. Run `git fetch origin`, then choose the base, which is `origin/<default-branch>` unless the task names another, and a name for the delivery branch that no existing branch uses.

Write the claims ledger at `$(git rev-parse --git-common-dir)/no-mistakes/<delivery-branch>.md`, outside the working tree. Each claim is one behavior the finished change must have, with the check that will prove it. For example:

```
| Claim | Proof | Evidence |
| --- | --- | --- |
| Expired invites return 410 | Test through the invite API with a past expiry | |
| The settings page shows the invite list | Screenshot of the running app | |
| Out of scope: resending invites | | |
```

The step is done when the base and delivery branch are named, every claim has a proof that observes behavior, the out-of-scope rows are listed, and every ambiguity that changes a claim is resolved.

## Design the change

Follow the `codebase-design` skill through its proposal. Send the proposal and the claims ledger to the council as a proposal review.

The step is done when the council approves the design.

## Spike the change

When work for the task already exists, that work is the spike. When it has uncommitted changes, create `<delivery-branch>-spike` from its head and commit them there. Leave the original branch as it was, and disable auto-merge on its pull request if it has one.

Otherwise, create the spike from the base with `git switch --no-track -c <delivery-branch>-spike <base>`, so it does not track the default branch. Build the approved design quickly to find the constraints the design missed, and commit it.

Never push the spike.

Record in the ledger which claims the spike passes and fails, each constraint it revealed, and each workaround it needed. When a constraint changes the design, revise the design and send it back to the council.

The step is done when the ledger records the spike's results and constraints, the council approves a revision for every constraint that changes the design, and the working tree is clean.

## Rebuild the change

Create the delivery branch from the base with `git switch --no-track -c <delivery-branch> <base>`, and rebuild the change from the approved design and the ledger. Read the spike as a reference, but do not copy a workaround that the design now makes unnecessary. When the rebuild cannot follow the approved design, revise the design, and continue once the council approves it.

Order the commits so the history makes the case. Removals come before reshaping, scaffolding before the failing test, and a failing test before its fix. Every commit passes the repository's checks, except that a failing-test commit fails only on its new test.

The step is done when `git diff <base>` holds only the change the design describes, and every commit meets the check rule.

## Prove every claim

Prove each claim with the check the ledger names, and write the evidence next to it. Follow `full-send`'s "Prove the change" for what counts as evidence. Then add these checks:

- Export the base with `git archive <base> | tar -x -C <directory>` into a new directory from `mktemp -d`, so the copy has no `.git` and no branch with the implementation. The request covers that directory. Start a subagent on a different model, with fresh context and that directory as its working directory, and tell it to read only that directory. Give it the Claim column, the public interface's signatures, and the repository's test setup, but not the ledger's spike notes. Ask it for tests that try to break each claim. Copy its tests onto the delivery branch and run them. Each failure is a code bug, a claim to correct, or a test that asserts what no claim states. Narrow a test of the last kind to what its claim states, or delete it when no claim covers it, and record why in the ledger. When no other model is available, use a fresh subagent on the same model and record the shortfall. Keep only the tests that cover behavior no existing test covers.
- Run the spike's tests on the delivery branch. Delete a spike test that fails only because it relies on a workaround the design dropped. Keep only the spike tests that cover behavior no other test covers.
- Run the `footguns` skill on the changed paths, and fix each Confirmed footgun that the change introduced.
- For UI, run the `harden-ui` skill on the changed screens, and fix each break that the change introduced. Leave its switch and worst-case fixtures out of the diff, and keep a regression test for each fixed break when the test runner can render the component. Otherwise, record a screenshot of the fix in the ledger.

List the defects that existed before the change, and Plausible footguns, as follow-ups instead of fixing them.

Add each fix after the rebuild's commits, with its test in the same commit as `footguns` does, and a message that names the claim or finding it answers. Apart from the spike tests and the blind tests narrowed or deleted above, do not weaken, skip, or delete a test to make it pass.

The step is done when all of these hold:

- Every claim has evidence from this session.
- The blind tests ran on the delivery branch, and each one passes, was corrected along with its claim, was narrowed to its claim, or was deleted because no claim covers it. When the tester found no behavior it could test from outside, its reason is in the ledger. When no other model was available, the shortfall is recorded.
- Each spike test passes, or was deleted because it relied on a dropped workaround.
- `footguns` ran on the changed paths, and each Confirmed footgun the change introduced is fixed with its test.
- For UI, `harden-ui` ran on the changed screens, and each break the change introduced is fixed.

## Cut what the change does not need

Review the diff by subtraction, as the `restraint` skill describes. Run the `prune` skill on what the change added or left unused, and list other candidates as follow-ups. Fold each cut into the commit that added the code. When the change introduces a pattern that the rest of the repository does not follow, use the existing pattern instead, or list the sweep as a follow-up.

The step is done when every line of the diff serves a claim or a fixed finding, every claim's proof passes again on the cut head, and every commit still meets the rebuild's check rule.

## Review the diff

Run the council on the full diff from the base. After each fix, run the claims' proofs again.

The step is done when the council approves the diff.

## Hand off the pull request

Delete the `<delivery-branch>-spike` branch if you built the spike yourself. Keep a spike branch that you created to commit existing work, because it holds the only copy of that work. Follow `full-send` from "File the PR", with `full-stop`'s overrides unless the user said "full send". Put the ledger's claims table, with its evidence, in the pull request description, and link the pull request of any existing work that served as the spike.

When a CI failure, review comment, or conflict fix leads to a behavior change after the pull request opens, run the claims' proofs again and send the full diff back to the council before the pull request counts as ready or merges.

The step is done when the council approves the latest behavior change, and the pull request either meets `full-stop`'s readiness check or `full-send` merged it.

## Return the result

When the run had less than it needed, such as a single provider or no browser, say so on the first line and name what you used instead.

Report the pull request URL, the claims ledger with its evidence, the council's verdicts for each design round, its score table for the code, the constraints the spike revealed, and the follow-ups. When you created a spike branch to commit existing work, name it. If any existing work that served as the spike has a pull request, name it and ask whether to close it. List the mistake types the council found more than once as candidates for the `coding-standards` skill. When the report ends with a question for the user, put the question last.

## Check the run

- Every claim in the ledger has a proof that observes behavior and evidence from this session.
- The council approved the design and the latest behavior change.
- The change was rebuilt on the delivery branch from the base. A spike you built yourself was deleted, and any spike branch you created to commit existing work remains.
- `footguns`, the spike tests, and for UI `harden-ui` ran, and each problem the change introduced is fixed.
- The blind tests ran from an export of the base with no access to the implementation, or the tester's reason for finding nothing to test is in the ledger.
- Every line of the diff serves a claim or a fixed finding.
- The pull request is open and unmerged, unless the user said "full send".

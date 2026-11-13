---
name: no-mistakes
description: Take a task to a ready pull request with a council-approved design, a clean rebuild, and evidence for every claim.
disable-model-invocation: true
---

# No mistakes

Take the task to a pull request that is ready to merge, with no mistake left for a reviewer to find. Apply the extra care to proof and review, not to scope. The change stays as small as the goal allows.

## Use these permissions

A no-mistakes request grants the testing and branch permissions of the `full-stop` skill and keeps the pull request unmerged as `full-stop` describes. When the user also says "full send", follow `full-send` to the merge instead.

The council approves the design and the final diff in place of the user. Do not wait for the user's agreement on a design, a dry run, or a structural change, even where another skill or the user's instructions ask for it. The request also counts as the fix request for `footguns` and `harden-ui`. Make their decisions yourself, record them in the ledger, and skip their closing questions.

Ask the user only under `full-send`'s "Ask when blocked" conditions, when an ambiguity changes a claim, or when a finding stays disputed after the council's round limit. Ask through the harness's question tool, as `full-send` describes.

## Choose the council

Use the `council-review` skill with three reviewers. Spread them across every provider the agent tools offer, so at least two providers review each round. When the user names models, use those. When only one provider is available, use it and name the shortfall in the report.

Allow three rounds for the design and five for the code. Approval needs every member to approve the current version, with no blocker or should finding open.

## Write the claims

Read the task, the code it touches, and the repository's `AGENTS.md`, `CODING_STANDARDS.md`, and `GLOSSARY.md` when they exist. Write the claims ledger at `$(git rev-parse --git-dir)/no-mistakes.md`, outside the working tree. Each claim is one behavior the finished change must have, with the check that will prove it. For example:

```
| Claim | Proof | Evidence |
| --- | --- | --- |
| Expired invites return 410 | Test through the invite API with a past expiry | |
| The settings page shows the invite list | Screenshot of the running app | |
| Out of scope: resending invites | | |
```

The step is done when every claim has a proof that observes behavior, the out-of-scope rows are listed, and every ambiguity that changes a claim is resolved.

## Design the change

Follow the `codebase-design` skill through its proposal. Send the proposal and the claims ledger to the council as a proposal review. Revise until the council approves.

The step is done when every council member approves the same version of the design.

## Spike the change

Build the approved design quickly on a local branch named `<branch>-spike`, to find the constraints the design missed. Never push the spike. When work for the task already exists, that work is the spike. Leave its branch and any pull request for it untouched, and rebuild on a new branch.

Record in the ledger each constraint the spike revealed, each claim that turned out wrong, and each workaround it needed. When a constraint changes the design, revise it and send it back to the council.

The step is done when the spike passes the claims' proofs, and every constraint it revealed is in the ledger or the council has approved a revised design.

## Rebuild the change

Create a fresh branch from the base, and rebuild the change from the approved design and the ledger. Read the spike as a reference, but do not copy a workaround that the design now makes unnecessary.

Order the commits so the history makes the case. Removals come before reshaping, scaffolding before the feature, and a failing test before its fix, as the `testing` skill describes. Every commit passes the repository's checks, except that a failing-test commit fails only on its new test.

The step is done when `git diff <base>` holds only the change the design describes, and every commit meets the check rule.

## Prove every claim

Prove each claim with the check the ledger names, and write the evidence next to it. Follow `full-send`'s "Prove the change" for what counts as evidence. Then add these checks:

- Give a subagent on a different model only the claims ledger, the public interface, and the repository's test setup, without the implementation. Ask it for tests that try to break each claim. Run them and the spike's tests against the rebuild. Each failure is a code bug or a claim to correct. Keep only the tests that cover behavior no existing test covers.
- Run the `footguns` skill on the changed paths, and fix each confirmed footgun that the change introduced.
- For UI, run the `harden-ui` skill on the changed screens, and fix each break.

Add each fix after the rebuild's commits, as its own commit that names the claim or finding it answers. Do not weaken, skip, or delete a test to make it pass.

The step is done when every claim has evidence from this session, and every blind test passes or was corrected along with its claim.

## Cut what the change does not need

Review the diff by subtraction, as the `restraint` skill describes. Run the `prune` skill on the changed paths. When the change introduces a pattern that the rest of the repository does not follow, use the existing pattern instead, or list the sweep as a follow-up issue.

The step is done when every line of the diff serves a claim or a check the skills above require, and the checks still pass.

## Review the diff

Run the council on the full diff from the base. Every round reviews the whole diff, not only what changed since the last round. After each fix, run the claims' proofs again. This review replaces `full-send`'s "Review the change" step.

The step is done when every council member approves the same head.

## Hand off the pull request

Delete the `<branch>-spike` branch if you created it. Follow `full-send` from "File the PR", with `full-stop`'s overrides unless the user said "full send". Put the claims ledger, with its evidence, in the pull request description.

When a CI failure or review comment leads to a behavior change after the pull request opens, run the claims' proofs again and send the full diff back to the council before the pull request counts as ready.

The step is done when the council approved the latest head and the pull request meets `full-stop`'s readiness check, or `full-send` reports it merged.

## Return the result

When the run had less than it needed, such as a single provider, no subagents, or no browser, say so on the first line and name what you used instead.

Report the pull request URL, the claims ledger with its evidence, the council's verdicts for each design round, its score table for the code, the constraints the spike revealed, and the follow-ups. List the mistake types the council found more than once as candidates for the `coding-standards` skill. When the report ends with a question for the user, put the question last.

## Check the run

- Every claim in the ledger has a proof that observes behavior and evidence from this session.
- Every council member approved the design and the latest head, or the report names the shortfall.
- The change was rebuilt on a fresh branch from the base, and no spike branch you created remains.
- The blind tests ran without access to the implementation.
- Every line of the diff serves a claim or a required check.
- The pull request is open and unmerged, unless the user said "full send".

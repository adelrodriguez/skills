---
name: takeover
description: Use when the user asks to take over a pull request, branch, or agent thread.
metadata:
  reference:
    - "https://github.com/t3dotgg/tstack/blob/main/skills/takeover/SKILL.md"
---

# Take over existing work

Finish the goal of a pull request, branch, or thread that someone else started, and keep the credit with the people who did the work. The earlier implementation is context, not a plan you must defend.

A takeover request authorizes a new branch and a replacement PR. It does not authorize pushing to the original branch or editing or closing the original PR. Continue in place or stack on the original only when the user asks for that.

## Read the source

Read the source the user names:

- **PR.** Read the description, every review finding, every comment, and the diff with `gh pr view <pr> --comments` and `gh pr diff <pr>`.
- **Branch.** Read `git log origin/<base>..<branch>` and the diff against its base.
- **T3 thread.** Read it with `t3_thread_read`, including the user's later corrections. Find the worktree it worked in, and check it for uncommitted changes with `git status --porcelain`.

The step is done when you have recorded the original goal in one sentence, the head SHA as `<original-head>`, the base branch as `<base>`, any uncommitted work, and every open finding and correction.

## Start the continuation branch

Create a new branch from the original head, so the original commits and their authors carry over unchanged:

```bash
git switch -c <new-branch> <original-head>
```

Commit uncommitted work from the source on the new branch with its author's identity, and say in the message where it came from.

For an in-place continuation, work on the original branch instead. For a stacked continuation, use the original branch as `<base>`.

The step is done when `git log` on the new branch shows every original commit with its original author.

## Update it to the base

Record `<original-head>` as `<old-head>`, and `git merge-base origin/<base> <original-head>` as `<old-base>`. Then follow these sections of the `refresh` skill on the new branch: "List what merged since", "Check for overlap", "Rebase the branch", and "Verify the refreshed PR".

Check the source again before you continue, because its author may have pushed since you read it. Add any new commits to the new branch.

The step is done when the branch is rebased onto `origin/<base>` and includes the source's latest commits.

## Finish the goal

Fix each open finding and correction you recorded, in commits of your own. Keep every behavior and surface the original meant to ship.

The step is done when every recorded finding and correction is fixed or has a written reason for declining it.

## Keep the credit

- Keep each original commit's author and every existing `Co-authored-by` trailer.
- Take each contributor's name and email from `git log --format='%an <%ae>'` on the original commits, or from their GitHub profile. Never guess an email.
- When the repository squash-merges, add a `Co-authored-by` trailer for each human contributor to the PR description, so the squash commit keeps them.
- Name the original contributors in the PR description and link the original PR. The `pr` skill's model attribution line does not replace this credit.

The step is done when every human who committed to the original work appears as an author or a verified co-author.

## File and watch the PR

File the replacement PR with the `pr` skill, then watch it with the `monitor` skill.

The step is done when the `monitor` skill reports the PR ready, or reports a blocker.

## Check the takeover

- The original branch and PR are unchanged, unless the user asked for an in-place continuation.
- Every original commit is on the new branch with its original author.
- The branch is rebased onto `origin/<base>` and includes the source's latest commits.
- Every recorded finding and correction is fixed or declined with a reason.
- Every human contributor is credited with a verified identity.

## Return the result

Return the replacement PR URL and head SHA. Then report what you took over, what you changed, how you kept the credit, and any decision left for the user, such as closing the original PR.

---
name: hillclimb
description: Use when the user says "hill climb" or "hillclimb", asks to keep improving something until a score or target is reached, or asks how to measure a goal or optimization.
metadata:
  reference:
    - "https://youtu.be/xq0eB8vxeqk"
---

# Hillclimb

Raise a score until it reaches the target, one measured round at a time. Keep each round that improves the score without breaking a guardrail, and revert every other round.

## Get the hill

Read the spec at `.hillclimb/<slug>/hill.md`. If no spec exists, or the goal, score, target, or budget is unclear, follow [`references/find-the-hill.md`](references/find-the-hill.md) to write one. When the user only asked how to measure a goal, stop after the spec.

The step is done when the user has agreed to a spec with a measure, a baseline, a target, guardrails, and a budget.

## Set up the climb

Create the branch `hillclimb/<slug>`. When you climb past a target that an earlier climb already reached, stack the new branch on the earlier one, so the result that already met its target stays mergeable. When the harness is worth keeping after the climb, such as an eval built from real failures, move it out of `.hillclimb/` and commit it first.

Create `.hillclimb/<slug>/log.md` with the start time and one table. Record the baseline as round 0.

```
Started: 2026-11-04 14:10

| Round | Change | Score | Guardrails | Outcome | Time |
| --- | --- | --- | --- | --- | --- |
| 0 | baseline | 1104 ms | pass | kept | 0 |
| 1 | sieve instead of trial division | 0.78 ms | pass | kept | 4 min |
| 2 | skip even numbers | 0.80 ms | pass | reverted: within noise | 3 min |
```

## Run each round

1. Pick the next change most likely to raise the score. Use the findings from the last judged round, the failing eval cases, or a profile of the slow path. Make one idea per round, so a regression traces back to one idea.
2. Make the change.
3. Measure with the spec's command. For a judged hill, follow [`references/judged-scores.md`](references/judged-scores.md).
4. Keep the round when the score beats the last kept score by more than the spec's noise and every guardrail passes. Commit it with the score in the message. Otherwise, run `git reset --hard <last kept commit>` and `git clean -fd`. Leave out `-x`, so `.hillclimb/` survives.
5. Add the round to the log. For a reverted round, write the reason in the outcome.

The round is done when the log has its row and the working tree matches the last kept commit.

## Climb two goals in order

When the user wants two things, such as a perfect eval score and smaller tool descriptions, climb them in order. Reach the target on the first score and commit. Then move the first score into the guardrails at its reached value, and climb the second. For example, get every eval case to pass, then cut the descriptions to a third of their size while every case still passes.

## Keep the score honest

A change must raise the score by improving the goal. Revert any change that raises the score another way, and log it:

- Deleting, skipping, or weakening tests or eval cases.
- Special-casing the benchmark inputs or eval cases, or caching results across samples.
- Editing the harness, its fixtures, the rubric, or the references. Only the user changes the hill.
- Telling judges the target, the previous scores, or which artifact is the candidate.

## Stop the climb

Stop when the first of these happens:

- The score meets the target in two measurements in a row. For a judged hill, every judge meets it in one round, and a second round agrees.
- The climb reaches the budget.
- Three rounds in a row are reverted. Report the plateau and the ideas you tried.

Do not lower the target to finish. When the user adds a direction during the climb, such as "too grayscale, bring back color", add it to the spec as a guardrail or rubric note and continue.

## Hand back the result

Report the score at round 0 and at the last round, the log's table, the reverted attempts and why, the stop reason, and the total time. Add the token spend when the tool reports it. For a visual change, show before and after artifacts with a callout on each change, so the user can see what moved.

The user decides whether the top is high enough. If the user raises the target, start a new climb on a stacked branch.

Open a pull request only when the user asks, using the `pr` skill.

## Check the climb

- Every round has a log row with its score, guardrails, and outcome.
- Every kept round beat the last kept score by more than the noise, and every guardrail passed.
- The harness, rubric, and references match the spec the user agreed to.
- The report gives the start and end scores, the stop reason, and the time.

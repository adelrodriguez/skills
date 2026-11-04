# Judged scores

Use this file when the hill's kind is judged. It covers the panel, the artifacts, the judge brief, and how to read the scores. Everything else is in [`../SKILL.md`](../SKILL.md).

A judged score is relative. One model can score the same screenshot differently on three runs, and a design that scores 9 alone can score 7.4 next to strong references. References in every round keep the scores tied to something real.

## Choose the panel

Choose the judges and models with the `council-review` skill's rules for choosing reviewers. Order them from the fastest and cheapest to the slowest and most expensive, and record the order in the spec.

Add judges in stages. Run only the first judge until it scores the target in every category. Then add the next judge, and continue. A slow judge must not delay the rounds before its stage. The climb finishes only when every judge meets the target in one round.

## Capture the artifacts

Capture the candidate with the spec's capture steps every round, in the same states, sizes, and themes. Keep the round 0 artifacts as the baseline. Capture the references once, unless they come from software that changes.

## Brief each judge

Start each judge in a fresh context every round, and keep it read-only. Give every judge the same brief with the candidate, the baseline, and the references. Label each artifact with a neutral letter and shuffle the order each round, so the judge cannot tell which artifact is the candidate.

```
Review only. Do not edit files or start subagents.

You are comparing <N> versions of <kind of work>, labeled A to <letter>.
<artifact paths, one per label>

Score every version from 1 to 10 in each category:
<rubric from the spec, one line per category>

Then list the five changes that would most improve each version,
each with its location and the fix.

Reply:
| Version | <category> | <category> | ... |
Findings:
<label>-1 <location>: <problem>. Fix: <fix>
```

Do not tell a judge the target, the previous scores, or which version is the candidate.

## Read the scores

Map the labels back to the candidate, the baseline, and the references. Save every judge's full reply as `.hillclimb/<slug>/scores/<round>-<judge>.md`. In the log's score column, write each judge's lowest category score for the candidate and the candidate's gap to the best reference.

- References can score differently between rounds even when their artifacts do not change, so track the gap with the score.
- Treat a change of less than half a point from one judge as noise. Score again before you keep or revert on it.
- Verify each finding against the artifact before you act on it. Count evidence, not votes.

## Check the judged round

- Every judge saw the same artifacts under neutral labels in a fresh context.
- No brief mentioned the target, earlier scores, or which version is the candidate.
- Every judge's full reply is saved, and the log has each judge's lowest score and gap.

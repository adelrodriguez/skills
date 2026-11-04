# Judged scores

Use this file when the hill's kind is judged. It covers the panel, the artifacts, the judge brief, and how to read the scores. Everything else is in [`../SKILL.md`](../SKILL.md).

A judged score is relative and noisy. One model can score byte-identical screenshots a full point apart on two runs, and a design that scores 9 alone can score 7.4 next to strong references. References in every round keep the scores tied to something real, and two runs per judge keep one run's noise from deciding a round.

## Choose the panel

Choose the judges and models with the `council-review` skill's rules for choosing reviewers. Order them from the fastest and cheapest to the slowest and most expensive, and record the order in the spec.

Add judges in stages. Run only the first judge until it scores the target in every category. Then add the next judge, and continue. A slow judge must not delay the rounds before its stage. The climb finishes only when every judge meets the target in one round.

Run the full panel at round 0 and at least every third round, even before the first judge meets the target. One judge's gains do not always carry over to another, and a later judge can raise problems the first never mentions. When the user names the judges for every round, run all of them every round.

## Capture the artifacts

Capture the candidate with the spec's capture steps every round, in the same states, sizes, and themes, and save the capture in `.hillclimb/<slug>/artifacts/<round>/`. Show the last kept round's folder as the baseline, so the keep decision compares two versions scored in the same runs. A judge can score the same unchanged artifacts lower in one round than in the round before, so a comparison across rounds can hide a real gain. Capture the references once, unless they come from software that changes.

## Brief each judge

Run each judge twice every round, each run in a fresh context with its own shuffle, and keep every run read-only. Give every run the same brief with the candidate, the baseline, and the references. Label each artifact with a neutral letter and shuffle the order each run, so the judge cannot tell which artifact is the candidate. Before each run, empty `.hillclimb/<slug>/blind/`, copy the artifacts into it under names made only of the label and the state, such as `B-dark.png`, and give the judge only those paths. A path such as `artifacts/3/` or `references/linear/` names the version.

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

Map the labels back to the candidate, the baseline, and the references. Save every run's full reply as `.hillclimb/<slug>/scores/<round>-<judge>-<run>.md`. Average each judge's two runs per category. In the log's score column, write each judge's lowest averaged category score for the candidate and the candidate's gap to the best reference.

- References and the baseline can score differently between rounds even when their artifacts do not change, so decide keep or revert from the candidate against the baseline in the same runs, and track the gap to the best reference with the score.
- Each judge's averaged score in each category is one part of the score. A part moves when both of the judge's runs differ from the baseline by at least the spec's noise in the same direction. When three or more judges move the same category the same way by at least the noise in their averages, count the move for each of them. Treat any other change as noise.
- Act on a finding only when it repeats across runs, judges, or rounds, or when you can see the problem in the artifact. Judges contradict each other, such as asking for a control beside a label in one round and below it in the next. When findings conflict, keep the current design and log the conflict.
- Decline a finding that would make the artifact misrepresent the product, and log why.

## Check the judged round

- Every judge ran twice on the same artifacts, under neutral labels and file names, each run in a fresh context.
- No brief mentioned the target, earlier scores, or which version is the candidate.
- Every run's full reply is saved, and the log has each judge's lowest averaged score and gap.

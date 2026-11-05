# Find the hill

Use this file when no spec exists, or when the goal, score, target, or budget is unclear. It turns a goal into a hill: a score that one command or one council round produces, a target that ends the climb, and guardrails that must not get worse. Everything else is in [`../SKILL.md`](../SKILL.md).

An agent raises whatever score it gets, so the score must reward the goal and nothing else.

Keep every file for the hill in `.hillclimb/<slug>/` at the repository root, where `<slug>` is the goal in a few kebab-case words.

## Name the goal

Write the goal in one sentence that names what gets better. List what must not get worse, such as behavior, tests, other metrics, or the look of screens the goal does not cover. List what is out of scope.

The step is done when the goal is one sentence and every guardrail is something a check can pass or fail.

## Choose the kind of score

Pick the first kind that can measure the goal:

1. **Programmatic.** A program prints a number, such as wall time, bytes sent, bundle size, tokens in a prompt, or passing tests.
2. **Eval.** No program exists yet, but you can collect cases where the current behavior fails. Collect real failures from history, issues, logs, or agent threads. Group them by category, and turn each into a case with an expected outcome. The score is the number of passing cases.
3. **Judged.** The goal is a matter of taste, such as visual design, writing, or API ergonomics. A council of models scores artifacts against a rubric, as described in [`judged-scores.md`](judged-scores.md).

A judged score is noisy and costs the most, so use it only when the first two kinds cannot measure the goal. A judged goal can still have programmatic guardrails.

| Goal | Score | Guardrail |
| --- | --- | --- |
| Make a function faster | Median wall time of a benchmark | Output matches the baseline's output |
| Agents call the right tool | Passing cases in an eval built from past wrong calls | None |
| Shrink tool descriptions | Tokens in the descriptions | The eval above stays at its full score |
| Send less data to the client | Bytes sent for a recorded session | Screenshots of real threads show no visual change |
| Make the UI look better | Rubric scores from a council that compares screenshots with references | Existing tests pass |

The step is done when the score has a kind and a direction, higher or lower is better.

## Build the harness

Write one command, or one documented set of steps for a judged score, that measures the current checkout and prints the score and a pass or fail for every guardrail.

- **Programmatic and eval.** Run each sample in a fresh process, so a cache cannot raise the score, and keep build output and caches out of the working tree. Make the command take the median of at least five samples and print it with the spread, which is the highest sample minus the lowest. Record the noise as the spread's share of the median, such as 3%, so it still applies after the score moves. When the median is zero, as in an eval where every case fails at the start, record the spread itself as the noise, in the score's unit, such as zero cases for an eval that gives the same result every run.
- **Judged.** Write the rubric: four to eight categories, such as hierarchy, typography, color and contrast, spacing, iconography, and consistency, each with one line on what a 10 means. Pick references, which are the best comparable products, so judges score by comparison and not in isolation. Open each reference capture and drop any that renders differently from what its users see, such as a fallback font or an unrelated site at the expected address. Write the steps that capture the same states as artifacts every round, such as screenshots in light and dark mode, without development overlays such as a framework toolbar. Score the baseline twice with the first judge, and set the noise to the largest category difference between the two runs, and at least one point.

Check that the guardrails cover the behavior a change could break. When the existing tests are weak, add a check that compares the output with the baseline's output.

The step is done when the harness runs end to end on the baseline and prints a score, and every guardrail passes.

## Set the target and budget

Propose a target from the baseline. For a programmatic or eval score, estimate the best reachable value, such as a theoretical bound, the best known implementation, or a full eval pass, and set the target near it. Do not pick a target you already know the first change will beat. For a judged score, propose a target such as "every judge scores every category 9 or higher, and higher than every reference".

Propose a budget: a maximum number of rounds, hours, or spend.

The step is done when the target and budget are written down.

## Write the spec

Save the spec as `.hillclimb/<slug>/hill.md`. Leave out the judged section for other kinds. Use this template:

```
# Hill: <name>

Goal: <one sentence>
Kind: programmatic | eval | judged
Score: <name>, <higher|lower> is better
Measure: <command and the directory to run it from, or the steps for a judged round>
Harness: <paths of the harness and its fixtures>
Baseline: <value>
Noise: <share of the score, or points for judged>
Target: <condition that ends the climb>
Guardrails:
- <name>: <check>
Budget: <rounds, hours, or spend>
Out of scope: <list>

Judged only:
Rubric:
- <category>: <what a 10 means>
References:
- <name>: <artifact path>
Judges: <models, in the order to add them>
```

The user decides where the top is, because the climb spends their tokens. Show the spec and wait for the user to agree to the target and budget before the climb starts.

## Check the hill

- The goal is one sentence, and every guardrail is a check that passes or fails.
- The score kind is the first of programmatic, eval, and judged that can measure the goal.
- The harness ran on the baseline, and the spec records the baseline and its noise.
- A judged hill has a rubric, references, and capture steps.
- The user agreed to the target and budget.

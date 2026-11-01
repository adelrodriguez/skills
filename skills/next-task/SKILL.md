---
name: next-task
description: Use when the user asks what's next, or after a PR merges.
---

# Pick the next task

Read the repository's tracker and recommend the one unblocked item to work on next. A task is unblocked when nothing it depends on is still open and nobody is already working on it.

## Find the tracker

Check the repository's `AGENTS.md` and its issue-tracker documentation for where work is tracked: GitHub issues, a GitHub project, or Linear. When neither names a tracker, use the repository's GitHub issues.

When the user names a tracker issue, a milestone, or a label, limit the candidates to it.

The step is done when you know which tracker to read and what limits the candidates.

## Read the current state

Read the open items in the tracker, the open PRs, and the last 20 merged PRs. Read each PR's `closingIssuesReferences` to see which items it closes.

For each candidate, read its blocked-by dependencies:

```bash
gh api repos/<owner>/<repo>/issues/<number>/dependencies/blocked_by --jq '.[] | {number, state}'
```

The step is done when you have the open items, the open PRs, and the recent merges.

## Rule out what is not ready

Drop an item when any of these is true:

- An open PR already closes it, or its branch name refers to it.
- It has an open blocked-by dependency, or its tracker orders it after an open sibling.
- Someone other than the user is assigned to it.
- It is labeled as needing triage, a decision, or more information.
- A recent merge already did the work. Check the current source before you treat it as open.

The step is done when every candidate is kept or dropped with a reason.

## Rank the candidates

Rank what remains, in this order:

1. The item the last merged PR unblocked, or the next sibling in the same tracker.
2. Higher priority, from the tracker's priority field or labels.
3. Items that unblock the most other items.
4. Smaller items, when the above tie.

The step is done when the candidates are in one ranked list.

## Recommend one

Recommend the top item, with one sentence on why it is next and what it unblocks. List the next two as alternatives, one line each.

When the user asked you to pick and start, start the recommended item. Otherwise stop after the recommendation.

The step is done when one item is recommended, or the work on it has started.

## Check the pick

- The recommended item has no open PR and no open blocked-by dependency.
- The current source shows the work is not already done.
- The reason names what the item unblocks or why it outranks the alternatives.

## Return the result

Return the recommended item as a link with its one-sentence reason, then the two alternatives. When nothing is unblocked, say so, and name the item that blocks the most others.

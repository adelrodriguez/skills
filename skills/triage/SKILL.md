---
name: triage
description: Use when triaging issues, auditing open issues for stale reports or missing metadata, or ranking bugs by priority and effort.
---

# Triage issues

Check what work is still needed, classify each issue, and update the tracker. Finish with the actionable bugs and the decisions that need the user. Start implementation only when the user asks.

## Find the scope and conventions

Read the repository's `AGENTS.md`, issue-tracker documentation, and triage-label mapping. Identify the tracker, issue types, readiness labels, effort values, and priority field. Use native types and fields where the repository does. Do not invent labels or copy field IDs from another repository.

Keep the user's filters, such as a tracker, label, milestone, or exclusion of feature trackers. For a bare triage request, check issues needing triage, issues with missing or conflicting readiness, and `needs-info` issues with new information. For "all open issues," assess every open issue, including previously classified ones. A repeat request such as "again" keeps the scope and refreshes the live state.

Fetch every page in scope. Do not treat a CLI's default result limit or a capped search as the complete queue. Record the issue IDs so the final check can account for every issue.

The step is done when the scope has a complete inventory and the metadata conventions are known.

## Check each issue against current work

Read the issue's body, comments, and current metadata. Check the affected code on the current default branch. A fix in a local branch does not establish that the default branch is fixed.

For each issue, check these sources:

- Related open PRs and recent merges, including their closing references. Search issue mentions and branches too, since a PR may lack a native link.
- The actual changes in a matching PR. Distinguish a complete fix from a partial fix or a related change.
- Parent issues, sub-issues, and blocked-by dependencies. Read the current state of each blocker.
- Existing owners and active work. Use the `sessions` skill when an agent thread may already own the work.

Decide whether the report describes a current bug, unfinished work, an already fixed problem, a duplicate, or an obsolete request. Check the reported behavior, not just whether a named symbol still exists. Recent green CI alone does not prove that an intermittent bug was fixed.

If the evidence is insufficient, name the missing reproduction, access, or decision. An investigation can be ready for an agent when its question and completion criteria are clear. Do not present a suspected cause as confirmed.

The step is done when each issue has a supported disposition, known blockers, and verified PR coverage or an explicit gap in the search.

## Classify the work

Keep readiness, effort, priority, blockers, and PR coverage separate. An issue can be specified well enough for an agent while a dependency or an existing PR prevents new work.

Use the repository's mapping for these readiness roles:

| Role | Apply when |
|---|---|
| `needs-triage` | The assessment is unfinished. |
| `needs-info` | A specific missing fact or decision prevents a useful next action. |
| `ready-for-agent` | An agent can carry out the specified implementation or investigation and verify its result. |
| `ready-for-human` | The work requires human access or judgment that cannot be reduced to an agent task yet. |
| `wontfix` | The project has decided not to pursue the work. |

Set one readiness role. If a role has no tracker equivalent, report the gap instead of creating a label. Use the repository's issue types to distinguish bugs from tasks and features. A test or tooling failure can be a bug even when it does not affect production.

Estimate the remaining work, including verification. Use the repository's effort scale. Without a documented scale, distinguish a small, understood change from work spanning several areas or requiring substantial investigation. Do not call an issue low effort because its title sounds simple or its likely patch is short.

Set priority by impact and urgency. Consider who is affected, how often the problem occurs, whether it blocks progress, whether a workaround exists, and whether delay increases harm. Use the tracker's values. When the repository has no rubric, apply these distinctions:

- Treat confirmed active incidents, such as data loss or a widespread broken core flow, as urgent.
- Give high priority to confirmed failures in core behavior and serious security or cost exposure.
- Schedule bounded defects with limited reach or a usable workaround below those failures.
- Give minor polish and cleanup lower priority unless they block other work.

Keep uncertainty explicit. Missing impact evidence is not proof of low priority. A quick fix is not automatically a high-priority fix.

The step is done when every issue has a disposition, and each remaining open issue has a type, readiness, effort, and priority, or a named metadata gap.

## Update and verify the tracker

Apply the requested triage changes without asking for approval on each classification. Re-read an issue before writing if another actor may have changed it. Update only the fields that need changing, and preserve assignees, relationships, and work already in progress.

Add a concise rationale when the decision needs evidence or leaves an action for someone. State the missing information for `needs-info` and the human task for `ready-for-human`. Link a covering PR if the issue does not already reference it. Use the `comment` skill for comments. On repeated passes, leave unchanged classifications and existing notes alone unless new evidence changes the decision.

Close verified fixes when the user requests closure or the repository's triage rules include it. Use the completed outcome and link the fix. An open or partially covering PR leaves the issue open. Reserve `wontfix` for a decision not to do the work. If a report no longer applies but obsolete code remains, assess the remaining cleanup before recommending closure.

For stale issue bodies, update the facts when requested and preserve useful history. Use the `issue` skill if the requested triage requires a new tracker or child issue.

Read back each changed issue's fields, labels, state, and relationships. Re-enumerate the queue after the updates. Account for issues added, closed, or changed during the pass. Continue through the requested inventory rather than stopping after a sample.

The step is done when every requested issue has been assessed and every saved change is verified, or the remaining issues have explicit blockers.

## Return the actionable work

If a required source was unavailable, start by naming it and the part of the assessment it limits. Report how many issues you assessed and changed, what remains, and which requested fields could not be applied. Distinguish metadata verification from runtime verification.

Surface confirmed bugs affecting users before hypothetical failures and enhancements. Show the low-effort, high-priority bugs that are ready and unblocked. List issues with active PRs separately so they do not look like unclaimed work. Include links, effort, priority, and the reason for any blocker or human decision.

Follow the user's requested sort. Otherwise, order actionable bugs by priority, then smaller remaining effort, then age. When the user wants one next task, use the `next-task` skill.

Treat schedules and provider choices from other sessions as examples, not defaults. Preserve authorization given in the current task, including earlier turns.

The step is done when the user can identify the next work without rechecking whether the listed issues are open, blocked, or already covered.

## Check the triage

- Every issue in scope is accounted for. An incomplete assessment is not reported as a complete pass.
- Each changed field was read back, and the final counts describe the refreshed queue.
- Readiness, effort, priority, dependencies, and PR coverage remain separate.
- Issues listed as actionable are still open and unblocked, and no other worker or covering PR already handles them.
- Closure reasons distinguish completed work from a decision not to pursue it.
- The report identifies missing evidence and states which behavior checks actually ran.

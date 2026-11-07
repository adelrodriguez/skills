---
name: triage
description: Use when triaging issues, finding duplicates, proposing project trackers, or ranking bugs by priority and effort.
---

# Triage issues

Check what work is still needed, classify each issue, and update the tracker. Find duplicates and propose related work as projects. A tracker is an issue that groups distinct child issues toward a shared outcome. Start implementation only when the user asks.

## Find the scope and conventions

Read the repository's `AGENTS.md` and issue-tracker documentation. Identify the tracker, existing project trackers, and supported issue type, effort, and priority fields. Use the repository's existing fields. If a field is unavailable, put the assessment in the report.

Keep the user's filters, such as a tracker, milestone, or exclusion of feature trackers. For a bare triage request, use the repository's triage queue, including unassessed issues and reports with new information. For "all open issues," assess every open issue, including previously classified ones. A repeat request such as "again" keeps the scope and refreshes the live state.

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

## Find duplicates

Search open and closed issues for reports of the same problem. Compare the affected behavior, reproduction, and requested outcome. Treat reports as duplicates only when they describe the same problem and one resolution covers both. Sharing a component or topic is not enough.

For each duplicate set, recommend one canonical issue to keep. Prefer the issue with the clearest evidence and useful discussion, accounting for active ownership and PR coverage. Identify any unique details that should move to the canonical issue before the others close. If a closed issue's bug has returned, treat the new report as a recurrence and link the earlier issue.

Recommend duplicate closures unless the user has authorized them. Preserve distinct work as separate issues for the project proposals.

The step is done when each suspected duplicate has a linked canonical issue and supporting reason, or remains separate because the overlap is unconfirmed.

## Classify the work

Keep readiness, effort, priority, blockers, and PR coverage separate. An issue can be specified well enough for an agent while a dependency or an existing PR prevents new work.

Describe readiness as the next action: an agent can implement or investigate, a specific fact or decision is missing, or a human must act. Name that action and who can take it. Use the repository's issue types to distinguish bugs from tasks and features. A test or tooling failure can be a bug even when it does not affect production.

Estimate the remaining work, including verification. Use the repository's effort scale. Without a documented scale, distinguish a small, understood change from work spanning several areas or requiring substantial investigation. Do not call an issue low effort because its title sounds simple or its likely patch is short.

Set priority by impact and urgency. Consider who is affected, how often the problem occurs, whether it blocks progress, whether a workaround exists, and whether delay increases harm. Use the tracker's values. When the repository has no rubric, apply these distinctions:

- Treat confirmed active incidents, such as data loss or a widespread broken core flow, as urgent.
- Give high priority to confirmed failures in core behavior and serious security or cost exposure.
- Schedule bounded defects with limited reach or a usable workaround below those failures.
- Give minor polish and cleanup lower priority unless they block other work.

Keep uncertainty explicit. Missing impact evidence is not proof of low priority. A quick fix is not automatically a high-priority fix.

The step is done when every issue has a disposition and each remaining open issue has a next action, effort, and priority assessment, with unsupported fields kept in the report.

## Update and verify the tracker

Apply the requested triage changes without asking for approval on each classification. Limit classification updates to supported issue type, effort, and priority fields. Re-read an issue before writing if another actor may have changed it. Preserve assignees, relationships, and work already in progress.

Add a concise rationale when the decision needs evidence or leaves an action for someone. State the missing information or human task. Link a covering PR if the issue does not already reference it. Use the `comment` skill for comments. On repeated passes, leave unchanged classifications and existing notes alone unless new evidence changes the decision.

Close verified fixes when the user requests closure or the repository's triage rules include it. Use the completed outcome and link the fix. An open or partially covering PR leaves the issue open. Distinguish completed work from a decision not to pursue it. If a report no longer applies but obsolete code remains, assess the remaining cleanup before recommending closure.

For stale issue bodies, update the facts when requested and preserve useful history.

Read back each changed issue's fields, state, and relationships. Re-enumerate the queue after the updates. Account for issues added, closed, or changed during the pass. Continue through the requested inventory rather than stopping after a sample.

The step is done when every requested issue has been assessed and every saved change is verified, or the remaining issues have explicit blockers.

## Propose projects

Group distinct issues when their combined work achieves one useful outcome. For example, separate failures in a checkout flow can belong under a tracker to make checkout reliable. Unrelated bugs in the same package can remain standalone.

Check existing trackers before proposing a new one. Recommend an existing tracker when its scope and completion criteria cover the group. Preserve current parents and ownership, and call out any proposed move. Count duplicate work once, through its canonical issue.

For each proposed group, show the tracker title or existing tracker link, the shared outcome, observable completion criteria, and the member issue links. Explain why those issues belong together and note dependencies that affect where work can start. Keep unrelated or uncertain issues standalone.

Wait for the caller's approval of the proposed grouping before creating a tracker or changing membership. Continue ordinary triage while proposals await approval.

After approval, use the `issue` skill to create the approved trackers and connect their existing child issues. Pass the approved content and relationships, and limit metadata changes to what the caller explicitly requested. Recheck for an existing tracker before creation so a repeated run does not create a duplicate. Apply only missing parent-child links. Read back the tracker and links.

The step is done when each group is a concrete proposal awaiting approval or an approved grouping with verified links.

## Return the actionable work

If a required source was unavailable, start by naming it and the part of the assessment it limits. Report how many issues you assessed and changed, what remains, and which requested fields could not be applied. Distinguish metadata verification from runtime verification.

Surface confirmed bugs affecting users before hypothetical failures and enhancements. Show the low-effort, high-priority bugs that are ready and unblocked. List issues with active PRs separately so they do not look like unclaimed work. Include links, effort, priority, and the reason for any blocker or human decision.

Include duplicate recommendations and project proposals with their member issues. Distinguish proposed groups from trackers actually created or updated. If approval is pending, put the request to approve the specific proposals last.

Follow the user's requested sort. Otherwise, order actionable bugs by priority, then smaller remaining effort, then age. When the user wants one next task, use the `next-task` skill.

Treat schedules and provider choices from other sessions as examples, not defaults. Preserve authorization given in the current task, including earlier turns.

The step is done when the user can choose the next issue or project and approve a grouping without reconstructing its scope.

## Check the triage

- Every issue in scope is accounted for. An incomplete assessment is not reported as a complete pass.
- Each changed field was read back, and the final counts describe the refreshed queue.
- Readiness, effort, priority, dependencies, and PR coverage remain separate.
- Duplicate recommendations explain why the same work resolves both reports and preserve unique evidence.
- Each project proposal has a shared outcome, completion criteria, and member issue links.
- Every created tracker or membership change belongs to an approved proposal, and its links were read back.
- Issues listed as actionable are still open and unblocked, and no other worker or covering PR already handles them.
- Closure reasons distinguish completed work from a decision not to pursue it.
- The report identifies missing evidence and states which behavior checks actually ran.

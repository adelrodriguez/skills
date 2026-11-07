---
name: retro
description: Review agent sessions and the project's history, and propose changes to the agent's environment.
disable-model-invocation: true
metadata:
  reference:
    - "https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md"
---

# Run a retrospective

Find what made agent sessions slow, wrong, or wasteful, and propose changes to the agent's environment so that the next session gets it right the first time. The environment is everything the agent reads or runs besides the task itself: global instructions, skills, the repository's agent documents, checks, and tools. Propose changes only. Each accepted change ships later as its own pull request in the repository that owns the file. Apply an accepted change to `CODING_STANDARDS.md` or to a check with the `coding-standards` skill.

Read the `writing-for-agents` skill before you write any proposed change to an agent document.

## Find the harness

Read [`references/harnesses.md`](references/harnesses.md), and detect every harness that the current session runs in, by the markers listed for each one. A session can run in more than one, such as Claude Code inside T3 Code. For each detected harness, record how to list and read sessions, which machines it reaches, and where its global instructions live.

When a harness reaches other machines, such as T3 Code's linked environments, list them and record which ones answer.

When the session runs in a harness that the reference does not list, find its session store and add a section for it to `references/harnesses.md` in the same format, as one of the findings.

The step is done when every detected harness has a recorded session source, and every reachable machine is listed with its status.

## Pick the sessions

Use the sessions the user names, such as a thread link, a session ID, a branch, a pull request, or "this week". When the user names none, use the current session.

Then add the sessions about the same work, from every detected harness and every reachable machine: sessions on the same branch, pull request, or worktree, and subagent or delegated sessions that a picked session started. Prefer the outermost harness as the source, such as T3 Code over Claude Code, because it holds sessions from every provider and machine.

Read each session in full, including the user's corrections, failed commands, tool errors, retries, and review findings. Note the position or timestamp of every event you will cite.

The step is done when every picked session is read to its last message, and every related session found is either read or listed with the reason it was left out.

## Read the project history

Skip this step when the sessions did not work in a repository.

For each repository the sessions changed, read the history of the work from its base:

- The commits from `git log --stat <base>..<head>`.
- Each pull request's description, review summaries, and comments from `gh pr view <pr> --comments`, and its inline review comments and replies, including resolved and outdated ones, from `gh api --paginate repos/<owner>/<repo>/pulls/<pr>/comments`. `gh pr view` leaves out inline comments, where most review findings live.
- Earlier work on the same files from `git log --follow --stat -- <path>`, back to the change that introduced their current shape.

Look for rework, which is work that a later commit undid or reshaped:

- A file or symbol that was renamed or moved after it was created, from `git log --follow --name-status` and `git log -M --diff-filter=R`.
- Code that a later commit deleted or rewrote, from `git log -S '<symbol>'`.
- A revert, a follow-up "fix" commit, or a review finding that changed the design.
- A module or folder layout that a later pull request reorganized.

For each rework, write down what the agent would have needed to know to write the final version first, such as a convention, a glossary term, a design step, or a check.

The step is done when every rework in the history has a recorded cause, or a note that the history does not show one.

## List the steering files

Read [`references/targets.md`](references/targets.md). For each target it lists, record whether it exists, where its source of truth lives, and its size. Record a missing target too, because a finding can propose creating it.

The step is done when every target in the reference is recorded as present or missing.

## Find the candidates

Go through each category in "Candidate categories" in [`references/targets.md`](references/targets.md), and look for its signal in the sessions and the history. For each candidate, record:

- The evidence: a session event with its position, or a commit SHA, and what went wrong.
- The category and the target file, including a target that does not exist yet.
- The proposed change, written as the exact text, check, or script it adds or removes.
- What the change would have saved: the turns, tool calls, review rounds, or commits it would have prevented.

For each candidate whose target is `CODING_STANDARDS.md` or a check, apply the criteria in the "Collect the evidence" and "Sort each candidate" steps of the `coding-standards` skill, and record whether it becomes a check or a rule. Propose the check instead of adding it, because the retro changes no files.

When a rule already exists but the agent did not follow it, the finding is about its trigger or its location, not a new rule. When the same fix applies to other repositories that use the same convention, name them.

The step is done when every category is checked, every candidate has evidence and a target, and every coding candidate is sorted as a check or a rule.

## Rank the candidates

Order the candidates by what they would have saved, most first. Put a mistake that reached a merged pull request above one that a check or review caught. Merge candidates that share a cause into one.

Drop a candidate when the model already behaves that way without the change, or when it would add a rule for a case that happened once and cannot recur.

The step is done when each remaining candidate has a rank and no two share a cause.

## Check the retro

- Every detected harness and reachable machine was searched, or the report says why not.
- Every candidate cites a session event or a commit.
- Every rework in the history has a cause or a note.
- Every target is in the repository that owns its source of truth, not an installed copy.
- Every coding candidate was sorted with the `coding-standards` skill.
- No candidate repeats a rule that another skill already owns.

## Return the report

When a harness, a machine, a session, or `gh` could not be read, say so on the first line, and name what the retro covered instead.

List the sessions and repositories the retro covered. Then list the candidates in rank order. For each one, give its category, the evidence, the target file and its repository, the proposed change, and what it would have saved. Mark each target that does not exist yet as "new".

End with a numbered list that asks the user which candidates to apply.

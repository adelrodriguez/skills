---
name: janitor
description: Use when the user says "janitor", or before handing back a finished task.
---

# Clean up after the task

Stop and remove everything this task started or created that should not outlive it. Clean up only what this task created. Leave everything else alone, even when it looks abandoned, and report it instead. Machine-wide cleanup belongs to the `housekeeping` skill.

## List what the task left behind

Read back through the thread and list each of these that the task started or created:

- **Processes:** dev servers, watchers, test runners in watch mode, tunnels, and background commands.
- **Browser sessions:** preview tabs, `agent-browser` sessions, and Chrome tabs the task opened.
- **Watchers:** PR watchers and monitors that are still running after the work they watch is done.
- **Temp files:** files and folders in `/tmp` and `$TMPDIR`, including those from `mktemp`, and scratch scripts, logs, and screenshots outside the repository.
- **Repository leftovers:** untracked files the task created, and debug logging, commented-out code, images, and `TODO`s that the task added to its own diff.
- **Git state:** stashes, temporary branches, and worktrees the task created.

The step is done when every item is listed with its PID, tab, path, or name.

## Confirm each item is yours

Confirm each process by PID with `ps -o pid,ppid,etime,command -p <pid>`, and check that its command and start time match what the task ran. Confirm each file by its path and the command that created it.

Move any item you cannot tie to this task to the report.

The step is done when every listed item is confirmed as the task's own or moved to the report.

## Keep what the user needs

Keep an item when the user asked for it, still uses it, or needs it to review the work. This covers a dev server the user is testing against, a tab the user has open, and a worktree with unpushed commits.

The step is done when every item is marked keep or remove.

## Clean up

Remove the items marked remove:

- Stop each process by its PID with `kill <pid>`. Never use `pkill -f` or a pattern match. When a process is still running after a few seconds, report it instead of using `kill -9`.
- Close each browser tab and session the task opened.
- Stop each watcher, using the tool or process that started it.
- Delete temp files by their literal paths. Never delete a path built from an unset or empty variable.
- In the repository, delete the untracked files the task created, and remove the leftovers from the task's diff. Leave every other change alone.
- Drop a stash or delete a branch only when its changes are committed and pushed elsewhere.

The step is done when every item marked remove is gone.

## Check the cleanup

- Every removed item was confirmed as this task's own.
- No process was stopped by a pattern match.
- No file outside the task's own list was deleted.
- Kept items each have a reason.
- `git status` and the task's diff show only the changes the task meant to leave.

## Return the result

Return one short list of what you stopped, closed, and deleted. Then list what you kept, with the reason, and what you found but could not tie to this task.

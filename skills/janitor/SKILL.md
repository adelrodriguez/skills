---
name: janitor
description: Use when the user says "janitor" or asks to clean up running browsers, simulators, or processes, and before handing back a finished task.
---

# Clean up after agents

Stop and remove what an agent started or created that should not outlive its work. Clean up only what falls in the scope, and report everything else instead, even when it looks abandoned. Old worktrees and temp files across the machine belong to the `housekeeping` skill.

## Set the scope

Pick the scope from how the skill was called:

- **Task.** You call the skill yourself before handing back a finished task. The scope is what this task started or created.
- **Session.** The user says "janitor this session", or "janitor" with no scope. The scope is what the current session started or created, across all of its tasks. A session is the current agent thread.
- **All sessions.** The user says "janitor all sessions". The scope is what any agent session on this machine started or created.
- **Kind.** The user names a kind of item, such as "running browsers" or "simulators". The scope is every item of that kind that any agent session started.

Task and session are your own scopes. All sessions and kind are other agents' scopes.

The step is done when the scope is one of the four, and for kind scope, the kinds are listed.

## List what was left behind

These are the kinds of items:

- **Processes:** dev servers, watchers, test runners in watch mode, tunnels, and background commands.
- **Browsers:** preview tabs, `agent-browser` sessions, Chrome tabs, and headless or automated Chrome instances.
- **Simulators and emulators:** iOS simulators and Android emulators.
- **Watchers:** PR watchers and monitors that are still running after the work they watch is done.
- **Temp files:** files and folders in `/tmp` and `$TMPDIR`, including those from `mktemp`, and scratch scripts, logs, and screenshots outside the repository.
- **Repository leftovers:** untracked files the task created, and debug logging, commented-out code, images, and `TODO`s that the task added to its own diff.
- **Git state:** stashes, temporary branches, and worktrees the task created.

In your own scopes, read back through the thread and list each item of every kind that it started or created.

In other agents' scopes, survey the machine for running items only, because you cannot see the other sessions' tabs, temp files, repository leftovers, git state, or watchers:

- Processes from `ps -axo pid,ppid,etime,command`, with the working directory of each from `lsof -a -d cwd -p <pid>`.
- Browsers from that process list, by `--headless`, `--remote-debugging-port`, or a `--user-data-dir` under `/tmp` or `$TMPDIR`.
- Booted simulators from `xcrun simctl list devices booted`, and emulators from `adb devices`.

In kind scope, keep only the items of the named kinds.

The step is done when every item is listed with its PID, tab, device ID, path, or name.

## Confirm who owns each item

In your own scopes, confirm each process by PID with `ps -o pid,ppid,etime,command -p <pid>`, and check that its command and start time match what the task ran. Confirm each file by its path and the command that created it.

In other agents' scopes, tie each item to the session that started it:

- A process whose parent chain leads to an agent process, such as `claude` or `codex`, belongs to that agent's session.
- A process whose working directory is under `~/.t3/worktrees/` belongs to the thread whose `worktreePath` is that worktree. Find it with `t3_thread_list` in each project from `t3_project_list`.
- A process whose parent PID is 1 and whose working directory is an agent worktree is an orphan. The agent that started it has exited.

Record for each item its session and that session's status.

Move any item you cannot tie to an agent to the report in your own scopes, or to the ask group in other agents' scopes. It may be the user's own.

The step is done when every item has an owner or is in the report or the ask group.

## Decide what to keep

In task scope, keep an item when the user asked for it, still uses it, or needs it to review the work. This covers a dev server the user is testing against, a tab the user has open, and a worktree with unpushed commits.

In session scope, keep an item only when the user asked to keep it, or when it is a worktree with unpushed commits.

In other agents' scopes, put each item in the first group that matches:

1. **Keep.** Its session's status is `running`.
2. **Remove.** It is an orphan, or its thread is settled.
3. **Ask.** Every other item, including the items you could not tie to an agent.

The step is done when every item is marked keep, remove, or ask.

## Show the dry run

Skip this step in your own scopes.

In other agents' scopes, show the remove group as a table with the item, its PID or device ID, its session, and the reason. Show the ask group with what each item is. Give only the count of the keep group.

Wait for the user's agreement, because these items belong to other sessions. Remove an item from the ask group only when the user names it.

The step is done when the user agrees.

## Clean up

Remove the items marked remove:

- Stop each process by its PID with `kill <pid>`. Never use `pkill -f` or a pattern match. When a process is still running after a few seconds, report it instead of using `kill -9`.
- Close each browser tab and session with the tool that opened it. Stop a browser that no tool can close by the PID of its main process.
- Shut down each simulator with `xcrun simctl shutdown <udid>`, and each emulator with `adb -s <serial> emu kill`.
- Stop each watcher, using the tool or process that started it.
- Delete temp files by their literal paths. Never delete a path built from an unset or empty variable.
- In the repository, delete the untracked files the task created, and remove the leftovers from the task's diff. Leave every other change alone.
- Drop a stash or delete a branch only when its changes are committed and pushed elsewhere.

The step is done when every item marked remove is gone.

## Check the cleanup

- Every removed item was confirmed as the scope's own.
- In other agents' scopes, nothing was removed before the user agreed, and no item from the ask group was removed unless the user named it.
- No process was stopped by a pattern match.
- No file outside the scope's own list was deleted.
- Kept items each have a reason.
- `git status` and the task's diff show only the changes the task meant to leave.

## Return the result

Return one short list of what you stopped, closed, and deleted. Then list what you kept, with the reason, and what you found but could not tie to the scope. In all sessions scope, suggest the `housekeeping` skill for old worktrees and temp files.

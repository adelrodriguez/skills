---
name: housekeeping
description: Clean up what agents left across the machine, starting with old worktrees.
disable-model-invocation: true
---

# Clean up the machine

Remove what agents have left across the machine, across every repository and thread. Running processes, browsers, and simulators, and cleanup for one task or session, belong to the `janitor` skill.

## Set the scope

Use the machine and the areas the user names. When they name none, use this machine and every area below.

The areas:

- **Worktrees.** T3 worktrees under `~/.t3/worktrees/`, and other worktrees of the repositories they belong to.
- **Temp files.** Entries directly under `/tmp` and `$TMPDIR`.

The step is done when the scope is a list of areas.

## Survey the worktrees

Find each repository with worktrees under `~/.t3/worktrees/<repo>/`, and list all of its worktrees with `git -C <repo> worktree list --porcelain`. The T3 worktree tools cover only the current thread, so they cannot list the machine's worktrees.

For each worktree, record:

- Its path, branch, and last commit date.
- Whether it has uncommitted or untracked changes, from `git -C <worktree> status --porcelain`.
- Whether its commits are pushed, from `git -C <worktree> log --oneline @{upstream}..HEAD`.
- The state of its branch's PR, from `gh pr list --head <branch> --state all --json number,state,url`.
- Whether a T3 thread still uses it: a thread from `t3_thread_list` whose `worktreePath` is the worktree, and that is neither `archived` nor `settled`.

The step is done when every worktree has all five values.

## Classify each worktree

Put each worktree in the first of these groups that matches:

1. **Keep.** An active thread uses it, its PR is open, or its last commit is from the last 7 days.
2. **Remove.** It has no uncommitted changes and no unpushed commits, and its PR is merged or closed, or its branch is gone from the remote.
3. **Ask.** Every other worktree.

The step is done when every worktree is in exactly one group.

## Survey the temp files

List the entries directly under `/tmp` and `$TMPDIR` that the current user owns:

```bash
find /tmp "$TMPDIR" -mindepth 1 -maxdepth 1 -user "$USER"
```

For each entry, record its size, the date of the newest file inside it, and whether a process has it open, from `lsof +D <entry>` for a folder or `lsof -- <entry>` for a file.

Put each entry in one of these groups:

- **Remove.** Nothing inside it changed in the last 7 days, and no process has it open.
- **Keep.** Something inside it changed in the last 7 days, a process has it open, or it is a socket or a folder that the system or a running service owns, such as `com.apple.*`, `tmux-*`, or `launchd-*`.

The step is done when every entry is in exactly one group.

## Show the dry run

Show the remove group of worktrees as a table with the path, the branch, the PR, and the reason. Show the ask group with what each worktree would lose. Give only the count of the keep group.

Show the remove group of temp files as their count and total size, with the 20 largest entries listed. Give only the count of the keep group.

Wait for the user's agreement, because removals cannot be undone. Remove the ask group's worktrees only when the user names them.

The step is done when the user agrees.

## Remove the worktrees

Remove each worktree from its repository, never with `rm -rf`:

```bash
git -C <repo> worktree remove <worktree>
```

When `git worktree remove` refuses, report the worktree instead of forcing it. Then prune each repository's records of worktrees that no longer exist:

```bash
git -C <repo> worktree prune
```

Delete a removed worktree's local branch only when its PR is merged:

```bash
git -C <repo> branch -d <branch>
```

The step is done when every agreed worktree is removed and every repository is pruned.

## Remove the temp files

Delete each temp entry in the remove group by its literal path, from the list in the dry run:

```bash
rm -r -- <entry>
```

Never build the path from a variable or a glob. When `rm` fails on an entry, report it instead of using `sudo`.

The step is done when every temp entry in the remove group is gone or reported.

## Check the cleanup

- Nothing was deleted before the user agreed to the dry run.
- No removed worktree had uncommitted changes, unpushed commits, or an active thread, unless the user named it.
- Every removal went through `git worktree remove`, and no branch was deleted with `-D`.
- No deleted temp entry was open, changed in the last 7 days, or owned by the system.
- `git worktree list` in each repository shows no missing paths.

## Return the result

Return the number of worktrees and temp entries removed and the disk space freed, then the worktrees kept from the ask group and the ones git refused to remove, with the reason.

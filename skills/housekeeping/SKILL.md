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
- **Build caches.** Folders inside worktrees that a build tool regenerates, such as `apps/*/.next`.

Record the free space with `df -k /` before you start.

The step is done when the scope is a list of areas.

## Survey the worktrees

Find each repository with worktrees under `~/.t3/worktrees/<repo>/`, and list all of its worktrees with `git -C <repo> worktree list --porcelain`. The T3 worktree tools cover only the current thread, so they cannot list the machine's worktrees.

For each worktree, record:

- Its path, branch, and last commit date.
- Whether it has uncommitted or untracked changes, from `git -C <worktree> status --porcelain`.
- Whether its commits are pushed, from `git -C <worktree> log --oneline @{upstream}..HEAD`. When the upstream branch is gone, count a commit as pushed when it is the PR's `headRefOid` or an ancestor of it, because a squash merge leaves the branch's commits on no remote branch.
- The state of its branch's PR. Run `gh pr list --state all --limit 2000 --json number,state,url,headRefName,headRefOid` once per repository, and match each worktree's branch to `headRefName`.
- Whether a T3 thread still uses it: a thread whose `worktreePath` is the worktree, and that is neither archived nor settled. `t3_thread_list` does not return `worktreePath`, so read it from T3's state database without changing it:

  ```bash
  sqlite3 -readonly "file:$HOME/.t3/userdata/statev2.sqlite?mode=ro" \
    "select payload_json from orchestration_v2_projection_threads where archived_at is null and deleted_at is null" |
    jq -r 'select(.worktreePath != null and .settledAt == null and .settledOverride == null) | .worktreePath'
  ```

- Its size, from `du -sk`. Run one `du` per worktree in parallel, such as with `xargs -P 12 -n 1`, because one `du` over all worktrees can take longer than 10 minutes.

Also list each folder under `~/.t3/worktrees/<repo>/` that no repository's `git worktree list` includes, such as a folder whose `.git` file points to a repository that no longer exists, or a folder with no `.git`. Record its size and whether a thread uses it.

The step is done when every worktree has all six values and every unlisted folder is recorded.

## Classify each worktree

Put each worktree in the first of these groups that matches:

1. **Keep.** An active thread uses it, its PR is open, or its last commit is from the last 7 days.
2. **Remove.** It has no uncommitted changes and no unpushed commits, and its PR is merged or closed, or its branch is gone from the remote.
3. **Ask.** Every other worktree.

For each ask worktree with unpushed commits, check whether its work is already in the default branch, such as `origin/main`. Merge `HEAD` into it without touching the worktree, and compare the result with the default branch's tree:

```bash
git -C <worktree> merge-tree --write-tree origin/main HEAD | head -1
git -C <worktree> rev-parse 'origin/main^{tree}'
```

When the two hashes match, mark the worktree as "already in main", because removing it loses no work. A squash-merged branch can still fail this check when later commits on main touched the same lines.

When the user is short on disk space, also mark each keep worktree that is kept only for its recent commit and would otherwise be in the remove group.

The step is done when every worktree is in exactly one group, every unlisted folder is in the ask group, and every ask worktree with unpushed commits is checked against main.

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

## Survey the build caches

In each worktree that stays, find the folders that a build tool regenerates, such as `apps/*/.next`, `.output`, and `ios/build`. For each folder, record its size and whether a process has it open, from `lsof +D <folder>`.

Put each folder in the remove group when no process has it open, and in the keep group otherwise. Leave `node_modules` out. pnpm on macOS can clone its files from the store, so deleting `node_modules` may free much less than `du` shows, and `pnpm install` has to restore it.

The step is done when every build cache folder is in exactly one group.

## Show the dry run

Show the remove group of worktrees as a table with the path, the branch, the PR, and the reason. Show the ask group with what each worktree would lose, the "already in main" worktrees first, and each unlisted folder with its size. Give only the count of the keep group, and, when the user is short on disk space, the count and size of the keep worktrees kept only for their recent commit.

Show the remove group of temp files as their count and total size, with the 20 largest entries listed. Give only the count of the keep group.

Show the remove group of build caches as their count and total size, split by whether an active thread uses the worktree.

`du` adds up blocks that worktrees share, so call every size from `du` an estimate.

Wait for the user's agreement, because removals cannot be undone. Remove the ask group's worktrees, the unlisted folders, and the recent keep worktrees only when the user names them.

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

`branch -d` refuses a squash-merged branch as "not fully merged". Report each branch it refuses, and delete it with `branch -D` only when the user names it and its PR is still merged.

When the user names an unlisted folder, delete it by its literal path with `rm -r -- <folder>`, because git does not list the folder and cannot remove it.

The step is done when every agreed worktree is removed, every named unlisted folder is gone, and every repository is pruned.

## Remove the temp files

Delete each temp entry in the remove group by its literal path, from the list in the dry run:

```bash
rm -r -- <entry>
```

Never build the path from a variable or a glob. When `rm` fails on an entry, report it instead of using `sudo`.

The step is done when every temp entry in the remove group is gone or reported.

## Remove the build caches

Remove the worktrees first, because removing a worktree also deletes its build caches. Then check each remaining build cache with `lsof +D <folder>` again, and delete it by its literal path from the dry run:

```bash
rm -r -- <folder>
```

The step is done when every build cache in the remove group is gone or reported.

## Check the cleanup

- Nothing was deleted before the user agreed to the dry run.
- No removed worktree had uncommitted changes, unpushed commits, or an active thread, unless the user named it.
- Every worktree removal went through `git worktree remove`, and every `branch -D` was for a branch the user named.
- No deleted temp entry was open, changed in the last 7 days, or owned by the system.
- No deleted build cache was open.
- `git worktree list` in each repository shows no missing paths.

## Return the result

Return the number of worktrees, unlisted folders, temp entries, and build caches removed. Give the disk space freed as the change in `df -k /`, because `du` counts shared blocks. Then list the worktrees kept from the ask group, the ones git refused to remove, and the branches `branch -d` refused, with the reason.

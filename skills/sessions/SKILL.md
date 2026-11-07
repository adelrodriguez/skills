---
name: sessions
description: Use when finding, listing, or reading agent sessions or threads, or matching a worktree or process to its session.
---

# Agent sessions

A harness is the program that runs an agent and stores its sessions, such as T3 Code, Claude Code, Codex, or OpenCode. Each harness section below has the same fields:

- **Present when:** the check that shows the harness is on this machine or in this session.
- **Current session:** how to identify the session you run in.
- **List sessions:** how to find sessions by project, branch, or date.
- **Read a session:** how to read one session in full.
- **Other machines:** how to reach sessions on other machines, when the harness can.
- **Global instructions:** where the harness loads the user's global instructions from.

Search every harness that is present, not only the one running the current session, because the same work often spans several. One harness's search can miss a session that another harness's logs hold, so search the other harnesses' logs for the branch or PR too, such as with `grep -l <branch> ~/.claude/projects/*/*.jsonl`.

To add a harness, copy a section, fill in every field, and verify each command against a real session before you write it down.

## Match a worktree or process to its session

- **T3 Code worktree.** A worktree under `~/.t3/worktrees/` belongs to the thread whose `worktreePath` is that worktree. `t3_thread_list` does not return `worktreePath`, so read it from T3 Code's state database without changing it. This query prints the ID and worktree of each thread that is neither archived, deleted, nor settled:

  ```bash
  sqlite3 -readonly "file:$HOME/.t3/userdata/statev2.sqlite?mode=ro" \
    "select payload_json from orchestration_v2_projection_threads where archived_at is null and deleted_at is null" |
    jq -r 'select(.worktreePath != null and (.settledOverride == "active" or (.settledOverride == null and .settledAt == null))) | "\(.id) \(.worktreePath)"'
  ```

  A `settledOverride` of `"active"` means the user pinned the thread open, so it counts as unsettled even when `settledAt` is set. Subagent threads share their parent's worktree, and their IDs start with `thread:`. Read a thread's status with `t3_thread_read`.

- **Process.** A process whose parent chain, from `ps -o ppid= -p <pid>`, leads to an agent process, such as `claude`, `codex`, or `opencode`, belongs to that agent's session. A process whose working directory, from `lsof -a -d cwd -p <pid>`, is a T3 Code worktree belongs to that worktree's thread. A process whose parent PID is 1 and whose working directory is an agent worktree is an orphan, because the agent that started it has exited.
- **Other worktrees.** Find the sessions whose working directory is the worktree, from each harness's "List sessions" field.

## T3 Code

T3 Code runs other harnesses, such as Claude Code, Codex, and OpenCode, as threads. It holds every thread from every provider, so use it first when it is present.

- **Present when:** the `t3_*` tools are available, such as `t3_thread_read`, or `T3CODE_THREAD_ID` is set.
- **Current session:** the thread ID from `echo $T3CODE_THREAD_ID`. Read it in the shell first, because tool arguments do not expand environment variables.
- **List sessions:** `t3_thread_search` with a title, branch, PR, or project, and `t3_thread_list` with `allProjects: true` or a `projectId` from `t3_project_list`. `t3_thread_search` skips subagent threads and is not exhaustive, so use `t3_thread_list` with `includeSubagents: true` to find a thread's children by `parentThreadId`. The thread record holds `branch`, `worktreePath`, `pullRequests`, `providerInstanceId`, and `model`.
- **Read a session:** `t3_thread_read` with a low `limit` and `maxCharsPerItem`, paging with `afterPosition`. Use `view: "activity"` to see tool calls and errors, and `view: "messages"` for the conversation only.
- **Other machines:** `t3_environment_links` lists the linked machines and whether each is `reachable`. Pass a machine's `environmentId` to `t3_project_list`, `t3_thread_list`, `t3_thread_search`, and `t3_thread_read` to act there. Thread and project IDs belong to their machine.
- **Global instructions:** none of its own. Each thread uses the global instructions of the harness that runs it.

## Claude Code

- **Present when:** `~/.claude/projects/` exists. The current session runs in Claude Code when `CLAUDECODE` is set.
- **Current session:** the session ID in `CLAUDE_CODE_SESSION_ID`.
- **List sessions:** one folder per working directory under `~/.claude/projects/`, named after the path with each `/` and `.` replaced by `-`. Each session is one `<session-id>.jsonl` file in that folder, so a worktree's sessions sit in the worktree path's folder.
- **Read a session:** read the `.jsonl` file with `jq`, one event per line. Filter by `type` to skip bookkeeping events, and keep `user` and `assistant` events with their tool calls and results.
- **Other machines:** none.
- **Global instructions:** `~/.claude/CLAUDE.md` and `~/.claude/rules/*.md`, and the installed skills in `~/.claude/skills/`.

## Codex

- **Present when:** `~/.codex/sessions/` exists.
- **Current session:** the newest session file whose `session_meta` `cwd` is the current working directory.
- **List sessions:** one `rollout-<timestamp>-<session-id>.jsonl` file per session under `~/.codex/sessions/<year>/<month>/<day>/`. The first line is a `session_meta` event with the session's `cwd`, so filter by `cwd` to find a project's sessions.
- **Read a session:** read the `.jsonl` file with `jq`, one event per line. The conversation and tool calls are `response_item` events, and the turn boundaries are `event_msg` events.
- **Other machines:** none.
- **Global instructions:** `~/.codex/AGENTS.md`, and the installed skills in `~/.codex/skills/`, which link to `~/.agents/skills/`.

## OpenCode

- **Present when:** `~/.local/share/opencode/opencode.db` exists.
- **Current session:** the newest session in `opencode session list --format json` whose `directory` is the current working directory.
- **List sessions:** run `opencode session list --format json -n <count>` from a directory inside the project. It returns each top-level session's `id`, `title`, and `directory`, including sessions in the project's worktrees. The command skips child sessions, such as subagents, so find them in the database without changing it:

  ```bash
  sqlite3 -readonly "file:$HOME/.local/share/opencode/opencode.db?mode=ro" \
    "select id, title from session where parent_id = '<session-id>'"
  ```

- **Read a session:** `opencode session export <session-id>` prints one JSON object with `info` and `messages`. Each message has a `type`, such as `user`, `assistant`, or `compaction`, and an assistant message lists its reasoning and `tool` calls in `content`, with any `error`. A long session can export tens of megabytes, so write the export to a file and filter it with `jq`.
- **Other machines:** none.
- **Global instructions:** `~/.config/opencode/AGENTS.md`, and the installed skills in `~/.config/opencode/skills/`.

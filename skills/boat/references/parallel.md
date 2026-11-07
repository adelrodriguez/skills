# Run independent work in parallel

Use this reference for several agents, independent application instances, comparison runs, and parallel evaluations.

## Decide what needs a machine

Several reviewers reading the same source may need only the harness's ordinary subagents. Choose separate Boat sandboxes when tasks need independent filesystems, databases, browser sessions, machine configuration, or compute capacity.

Keep agent creation, provider selection, and background-task handling within the current harness's orchestration rules. This reference provides machines, not an alternative delegation policy.

Record the task assigned to each worker, the concurrency requested, and the result each worker must return. For evaluations, preserve the tested revision, persona inputs, and seed so results can be compared. Use `hillclimb` when the user requests optimization against those results.

The step is done when each worker has a reason for isolation and a distinct assignment.

## Prepare a reproducible source

Use [sandboxes](sandboxes.md) for lifecycle and credential handling, and [agents](agents.md) if workers run coding agents. Prepare dependencies and reusable files once when every worker needs the same starting state.

A fork copies the latest disk snapshot. Stop a task-owned source and wait for `stopped` when its final writes must be included. Do not stop a shared active source without authorization. Forks inherit disk data, which can include credentials and browser sessions. A sanitized fresh source is preferable for untrusted workers.

The step is done when the source snapshot represents the intended inputs and sharing boundary.

## Start bounded workers

Run `boat limits` and choose concurrency within the account's available starts and running-sandbox limits. Do not copy the pack's fixed fleet size or concurrency cap.

For a fork whose ID is needed after readiness, use `--wait`:

```sh
set -o pipefail
fork_id=$(boat fork "$source_id" --wait --ttl 3600 --json |
  jq -er 'select(.event == "ready") | .id')
boat info "$fork_id"
```

Record each returned ID before starting its task. A fork does not inherit the source's auto-stop setting. Start workload processes explicitly or verify restored enabled services. For GUI tasks, give each worker its own sandbox.

If a create or fork loses its response, inspect existing task resources before retrying. Use a consistent idempotency key when implementing retries with the API. Pace starts from live limits and respect rate-limit responses.

The step is done when every started sandbox is recorded with its task and deadline, including failed starts or partial batches.

## Collect and compare

Gather each worker's result before cleanup. Verify agent reports against the actual artifacts. Keep failed runs visible. For measured comparisons, record the number of runs, spread, and any skipped or cached work.

Stop or delete only the IDs created for this batch, following their planned final states. Do not clean up by selecting every sandbox in `boat list`.

## Check the batch

- Workers had independent state where the task required it.
- Starts and concurrent work stayed within the intended bounds.
- Every started worker has an outcome and recoverable results.
- No task-owned machine remains without an intentional owner and deadline.

See [parallel agents](https://docs.boat.dev/recipes/parallel-agents) and [resume and fork](https://docs.boat.dev/snapshots/resume-and-fork) for the current API and CLI behavior.

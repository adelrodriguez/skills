# Use a sandbox

Use this reference for a Linux workspace, SSH, file transfer, code execution, credential isolation, and disk snapshots.

## Select the environment

Run `boat status --check`, `boat list --all`, and `boat limits`. Reuse a suitable sandbox in the task's scope. If sign-in is missing, follow the [quickstart](https://docs.boat.dev/quickstart). Let the user complete browser sign-in or checkout. A sandbox task does not require creating a new API key.

Choose the size and auto-stop from the workload and current account limits. Read [machine sizes](https://docs.boat.dev/machines) when disk or memory matters. Do not copy the old pack's fixed capacity, price comparisons, or disk specification.

The step is done when the account can start the workload and the selected sandbox or creation settings are known.

## Choose what enters the sandbox

For untrusted code, start a fresh sandbox with `--no-env`. It withholds account environment secrets and credentials. Pass only the inputs the workload needs. A private repository may need a separately prepared source copy.

A fork of a credentialed sandbox is not a clean security boundary. `--no-env` scrubs Boat-managed credentials, but credentials you wrote yourself, application data, and browser profiles may remain. Use a fresh sandbox when that state must not be inherited. See [access and credentials](https://docs.boat.dev/environments/access).

The step is done when the source files, data, and credentials entering the sandbox are appropriate for the workload.

## Create or resume

Run shell pipelines with `pipefail` so a failed Boat command does not become a successful parse. For example, in Bash or Zsh:

```sh
set -o pipefail
id=$(boat new --type small --ttl 3600 --no-env --json |
  jq -er 'select(.event == "ready") | .id')
boat info "$id"
```

Use the size, environment, and lifetime selected above. Always pass the ID in automation. The `current` alias depends on shell state.

Resume a stopped sandbox with `boat resume "$id" --ttl 3600`. The usable states are `ready`, `idle`, and `running`. A working command proves readiness more directly than matching only the word `ready`. Services may become available later. See [readiness](https://docs.boat.dev/readiness).

The step is done when a command runs in the intended sandbox.

## Move files and run work

```sh
boat push "$id" ./my-app
boat exec --cwd my-app --timeout 600 "$id" -- npm test
boat ssh "$id"
boat scp "$id:/home/user/my-app/result.json" ./result.json
```

`boat push` copies to `/home/user/<directory-name>` unless `--to` is given. In a Git repository, it includes tracked files and unignored files. Review the inputs before copying them. Use SCP for explicitly chosen files, including ignored files that the workload needs.

Pass arguments after `--`. For shell operators or expansion, run an explicit shell, such as `boat exec "$id" -- bash -lc 'cd my-app && npm test'`.

The ordinary command timeout is 30 seconds. Give finite jobs a suitable timeout. For a process that must outlive the request, use [services](services.md).

The step is done when the command's exit code and output have been inspected and required artifacts have been copied back.

## Stop or retain the workspace

For a workspace to keep, run `boat stop "$id"`, then inspect `boat info "$id"` until it is stopped. A stop request returns before the snapshot finishes. If saving fails, inspect the reported error. Do not use `--force` to make a failed save disappear.

Snapshots retain disk state, not running programs or memory. `/tmp` and `~/.cache` are excluded. Keep reusable files under `/home/user`, and read [what snapshots save](https://docs.boat.dev/snapshots/whats-saved) for other paths. Machine addresses change after resume and fork.

A normal stopped snapshot is retained for at least 14 days. For longer retention, use a named saved snapshot after checking its current terms. `--no-snapshots` and zero-data-retention settings change what survives a stop. See [stopping a sandbox](https://docs.boat.dev/snapshots/stop).

For a disposable sandbox whose outputs are safe outside it, use `boat delete "$id" --yes`. Limit cleanup to the recorded task-owned IDs.

## Check the sandbox

- Inputs and credentials match the workload's trust level.
- Commands ran against the recorded ID and working directory.
- Required results exist outside any sandbox being deleted.
- The final state and retention match the task's scope.

For other flags, consult the [CLI reference](https://docs.boat.dev/cli-reference).

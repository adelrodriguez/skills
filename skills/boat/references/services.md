# Run background work and services

Use this reference for dev servers, long commands, bots, queue workers, and scheduled work.

## Choose the lifetime

A command that only needs more execution time can use an explicit timeout. A command that must continue after the calling request ends needs detached execution. A service that must restart after a reboot or restore needs an enabled systemd unit.

Use [sandboxes](sandboxes.md) for the machine and [hosting](hosting.md) for external access. Decide whether the workload is temporary or intentionally persistent before changing its lifetime.

The step is done when the command's lifetime, restart requirement, and sandbox deadline are known.

## Start and track a detached command

```sh
set -o pipefail
pid=$(boat exec --cwd my-app --detach --json "$id" -- npm run dev |
  jq -er .processId)
boat exec --status "$pid" "$id"
```

Record both the sandbox ID and process ID. Inspect status and logs, then test the service's actual behavior. Use `boat exec --attach "$pid" "$id"` to stream a finite job's output and obtain its exit status. Use `boat exec --kill "$pid" "$id"` to stop that job and its children.

A detached process does not restart after stop/resume or fork. Its old process record can become `lost`. Start it again and record its new process ID. Read [background commands](https://docs.boat.dev/long-running-tasks/background-commands) for status and attach behavior.

The step is done when the command is tracked and its expected output or service response is observed.

## Make a service restart

For a worker or server that must survive restores, write an enabled systemd service in the sandbox. Resolve its executable path there, set its working directory and required environment explicitly, and choose a restart policy appropriate for the process. Shell startup files are not a reliable source of service configuration.

Use `systemctl status` and `journalctl -u` to diagnose startup, then verify the real application operation. A healthy unit alone does not prove a queue consumer processed a job.

Do not use `nohup` as a substitute for restart management. Follow [always-on services](https://docs.boat.dev/long-running-tasks/always-on-services) for the unit definition and resume behavior.

The step is done when the service starts under its intended runtime environment and performs its requested operation.

## Set auto-stop explicitly

Keep a finite deadline for experiments. `boat extend "$id" --hours 2` sets the remaining time from now, rather than adding two hours to the existing deadline. Check the account's current limits before requesting a longer lifetime or `--no-auto-stop`.

Turning off auto-stop does not make a process restart. Enabling systemd does not prevent Boat from stopping the sandbox. An intentionally always-on service needs both settings. Do not make a preview always-on just because the old pack's recipe does so.

Inspect `boat info "$id"` for the resulting deadline. For timers and schedulers, also consider whether a fork would duplicate scheduled work before enabling it in multiple machines.

## Check the service

- The process or unit is recorded and its real behavior works.
- Runtime environment and logs are available for diagnosis.
- Restart behavior was tested if the result claims it survives resume.
- The auto-stop setting matches the requested operating period.

See [auto-stop](https://docs.boat.dev/long-running-tasks/auto-stop) for deadline behavior and account restrictions.

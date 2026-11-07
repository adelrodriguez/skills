# Run containers

Use this reference for Docker builds, Compose applications, databases, and service-backed tests.

## Prepare the stack

Use [sandboxes](sandboxes.md) to select or create the machine and copy the project. Inspect the repository's Dockerfiles, Compose files, environment examples, volumes, and health checks. Give independent tasks their own service state instead of pointing them at a shared development database.

The step is done when the stack's commands, inputs, persistent data, and readiness checks are known.

## Start and verify services

Boat includes Docker and Compose. After restoring a snapshot, Docker can become available after ordinary commands work. Wait for the daemon with a bounded command:

```sh
boat exec --timeout 120 "$id" -- bash -lc \
  'until docker info >/dev/null 2>&1; do sleep 1; done'
boat exec --cwd my-app --timeout 600 "$id" -- docker compose up -d --build --wait
boat exec --cwd my-app "$id" -- docker compose ps
```

Use `--wait` when the installed Compose version supports it and the project defines suitable health checks. Otherwise wait for each service's real readiness signal. Inspect failing service logs before retrying.

Exercise the application or database operation the task needs. A running container is not proof that migrations succeeded or requests work. Use [hosting](hosting.md) when a browser or external caller needs access.

The step is done when the application responds correctly with its required services available.

## Preserve or discard data deliberately

Current Boat snapshots save named volumes, container configuration, and images used by containers or Compose projects. Containers that were running are restored and started again. Docker's build cache and unused images are not retained by default.

After resume or fork, wait for Docker and application health again. Do not rely on process memory, previous IP addresses, or a warm build cache. Consult [what snapshots save](https://docs.boat.dev/snapshots/whats-saved) and [readiness](https://docs.boat.dev/readiness) before designing persistent Docker state.

Stop task-specific containers when a reused sandbox should no longer run them. Remove volumes only when their data is disposable within the task. Use the sandbox's planned final state from [sandboxes](sandboxes.md).

## Check the containers

- The stack used its intended configuration and independent data.
- Service health and the affected application behavior passed.
- Persistent results were retained or exported before cleanup.
- Resume behavior, when claimed, was tested through the application.

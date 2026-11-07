# Run checks in a clean environment

Use this reference for builds, tests, CI reproductions, dependency migrations, and installer or project-generator checks.

## Define what the run must prove

Record the source revision, runtime versions, command, required services, and expected result. Distinguish a clean install from a check in a prepared development environment. A successful cached task does not prove a fresh installation works.

Use the repository's package manager and documented commands. Use the `testing` skill when writing or changing tests, and `hillclimb` when the user asks for measured optimization. Boat provides the environment for those workflows.

The step is done when the command and its success condition are explicit.

## Choose one-shot or inspectable execution

Follow [sandboxes](sandboxes.md) for account setup, input selection, and credential isolation.

For a run whose console output is sufficient, `boat run` creates a sandbox, copies the project, runs the command, and deletes the sandbox:

```sh
boat run --type small --no-env --push . --timeout 600 -- npm test
```

Adapt the command to install the locked dependencies when the check needs them. Use a shell explicitly for a sequence, such as `-- bash -lc 'npm ci && npm test'`.

When the result includes reports, screenshots, a branch, or files to inspect after failure, use a regular sandbox or `boat run --keep`. Copy artifacts out before disposal. `--keep` leaves the sandbox subject to its auto-stop.

The step is done when the selected execution mode preserves all evidence the check needs.

## Run without hidden prerequisites

For installer checks, start fresh rather than from a snapshot that already contains the installed product. Inventory the relevant preinstalled tools. A fresh Boat image still includes developer tools, so it does not represent a minimal Ubuntu installation.

Run the documented installation path. Verify generated files and the installed command from a fresh shell. Check services with their actual runtime environment. A temporary home alone does not isolate inherited `PATH` or services.

For an application with databases or queues, use [containers](containers.md). For a browser check, also use [desktop](desktop.md). Test the application through its normal boundary after setup succeeds.

The step is done when the requested behavior has run and its expected output has been inspected.

## Check the run

- The source revision, toolchain, commands, and exit status are recorded.
- Required tasks executed rather than being cached or skipped.
- The report distinguishes setup failures from workload failures.
- Required artifacts are readable outside the disposable sandbox.

See [CI with Boat](https://docs.boat.dev/ci) for automation and [setup scripts](https://docs.boat.dev/setup) for startup provisioning.

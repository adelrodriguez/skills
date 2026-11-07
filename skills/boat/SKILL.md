---
name: boat
description: Use when the user asks for Boat, many parallel agents, untrusted code execution, or work isolated from this machine.
metadata:
  reference:
    - "https://docs.boat.dev/ai-tools"
    - "https://github.com/ariana-dot-dev/cloud-sandbox-vm-skills/tree/95ab83b306c9313139409ad16aec7e1ccb0d57f5"
---

# Use Boat

Use Boat for the parts of the requested work that need a remote execution environment. Read only the references needed for that work. A task can use more than one reference.

## Set the scope

Identify the workload, an existing sandbox to reuse if appropriate, the result to keep, and whether the sandbox should remain running, stop, or be deleted afterward. Record which sandboxes belong to this task before creating more.

For many parallel agents, read the parallel-work reference before choosing machines. Model-only reviews may need no remote execution. Work that depends on macOS, an iOS Simulator, or a particular physical machine still needs that environment.

The step is done when the target, result, and final state are known.

## Choose the references

| When the task needs... | Read |
| --- | --- |
| A sandbox, SSH, file transfer, code execution, credential isolation, or snapshots | [Sandboxes](references/sandboxes.md) |
| A clean build, test run, installer check, or bug reproduction | [Checks](references/checks.md) |
| Docker images, containers, or a Compose stack | [Containers](references/containers.md) |
| An agent working inside a sandbox | [Agents](references/agents.md) |
| Independent machines for parallel tasks or evaluations | [Parallel work](references/parallel.md) |
| An HTTPS preview, webhook receiver, or forwarded service | [Hosting](references/hosting.md) |
| A background command, persistent worker, or service | [Services](references/services.md) |
| A browser, Linux desktop, screenshot, or recording | [Desktop](references/desktop.md) |

Follow the selected procedures. Add another reference when the task needs it, rather than loading every reference in advance.

## Check the result

- The selected references' checks passed, or the report names what failed or could not run.
- Results needed after deletion have been copied out.
- Each sandbox's final state matches the task's scope.
- Retained servers and workers have a recorded auto-stop setting.

## Return the result

If a required capability was unavailable, name it and the fallback first. Return the sandbox ID, the outcome, the evidence or artifact, and the final state. Include the access URL when the task needs one.

# Use the Linux desktop

Use this reference for browser checks, GUI-only tasks, screenshots, and recordings inside Boat.

## Select the desktop task

Use [sandboxes](sandboxes.md) for the machine and [agents](agents.md) when an integrated agent will drive it. Follow the current harness's browser and device routing rules. A Linux desktop is not a replacement for a macOS app or iOS Simulator.

Each sandbox has one shared desktop. Give simultaneous GUI tasks separate sandboxes, or run them sequentially. Use [parallel work](parallel.md) for isolated browser sessions and evaluations.

The step is done when the target application, browser state, evidence, and execution path are known.

## Drive the task

Boat's current harnesses have the preinstalled `computer` MCP tools. They act on the same screen that `boat desktop "$id"` streams. Use the current tools and [computer-use documentation](https://docs.boat.dev/integrated-agents/computer-use), rather than installing the old pack's Lux automation.

An authorized, authenticated integrated agent can receive a scoped browser task through `boat prompt`. It needs model credentials separately from the working desktop. Use shell-based browser automation when that is the task's selected execution path and the required tools are available.

The sandbox has its own browser profile. It does not inherit the local machine's signed-in browser. Account for login before choosing an unattended task. Profiles can persist through snapshots and forks, so a fresh isolated session must not be made by blindly copying a signed-in profile.

If the computer tools are unavailable, inspect their documented service health. If only headless checks can run, report that fallback rather than claiming desktop verification.

The step is done when the requested interaction has run and its visible result has been inspected.

## Record evidence when requested

The desktop recorder retains its documented internal name:

```sh
boat exec "$id" -- ascii-record-desktop start /home/user/demo.mp4
# Perform the scoped desktop task.
boat exec "$id" -- ascii-record-desktop stop
boat scp "$id:/home/user/demo.mp4" ./demo.mp4
```

Stop the recording before downloading it so the MP4 is complete. Open the resulting artifact and verify it captures the claimed behavior. See [drive and record the desktop](https://docs.boat.dev/desktop-streaming/drive-and-record) for the current recording interface.

Keep reusable browser downloads outside excluded cache paths when preparing a template. Read [what snapshots save](https://docs.boat.dev/snapshots/whats-saved) before relying on installed Playwright browsers across restores.

## Check the desktop task

- The intended interaction and application state were observed.
- Parallel workers did not share the same desktop unexpectedly.
- Evidence files are complete and readable outside the sandbox.
- The report identifies login, tool, or platform limitations that prevented a check.

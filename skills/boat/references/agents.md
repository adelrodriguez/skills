# Run an agent inside a sandbox

Use this reference when an agent needs a repository, tools, and an execution environment inside Boat.

## Choose how the agent runs

Follow the current harness's delegation rules. A remote machine does not authorize extra agents or a different provider or model. Use an existing T3 or harness delegation path when it owns the task. Use Boat's integrated agent when that execution mode is within the user's request.

Select the repository, branch, result, and allowed side effects. Follow [sandboxes](sandboxes.md) to prepare the machine. For separate machines per task, also read [parallel work](parallel.md).

The step is done when the execution mode and agent's scope are known.

## Prepare credentials and project context

The installed harness is separate from model access. `boat prompt` requires configured AI credentials. If Boat returns `provider_not_configured`, follow [keys and subscriptions](https://docs.boat.dev/integrated-agents/keys). Do not enable account-wide credential injection or collect a pasted subscription token to bypass missing configuration.

Use an authenticated environment appropriate for the agent's trust level. For sandboxes used by other people, follow [access and credentials](https://docs.boat.dev/environments/access) and the documented credential-proxy flow. A credential-free sandbox can still run shell commands without a configured model.

Put the repository's instructions, required skills, and tool configuration where the chosen harness reads them. Boat's built-in skill describes operating from inside a sandbox. The local `boat` skill does not need to overwrite it. See [harness customization](https://docs.boat.dev/integrated-agents/customize).

The step is done when the chosen harness has its required context and an approved model-authentication path.

## Run a scoped conversation

Give the agent the branch, working directory, task, acceptance checks, and output location. Set `provider` to the selected harness and preserve any requested model settings. For example, once that choice and authentication are established:

```sh
boat prompt --provider "$provider" "$id" "In /home/user/my-app, run the requested checks and save the results in /home/user/results."
boat conversations "$id"
```

Record the conversation ID. Subsequent prompts use `--resume`; events, steering, and interruption use `--convo`. Pass the ID so another conversation is not affected. Confirm the flags with the installed command's `--help`. See the [conversation reference](https://docs.boat.dev/integrated-agents/conversations) and [steering](https://docs.boat.dev/integrated-agents/steering) for their behavior.

Conversations in one sandbox share its files, configuration, and desktop. They are not isolated workspaces. Agent activity can extend the auto-stop deadline, so inspect the final deadline instead of assuming the initial TTL still applies.

The step is done when the intended conversation has completed or has a recorded handoff and result location.

## Check the agent's work

- Inspect the actual diff, files, or application behavior against the task's acceptance checks.
- Copy out results and preserve the branch before disposing of its only workspace.
- Report missing credentials or tools separately from an unsuccessful task.
- Leave conversations and the sandbox in the planned final state.

See [integrated agents](https://docs.boat.dev/integrated-agents) for the supported harnesses and model discovery.

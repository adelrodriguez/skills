<div align="center">
  <h1 align="center">🧰 <code>skills</code></h1>

  <p align="center">
    <strong>Agent skills I use every day</strong>
  </p>
</div>

I took and adapted these skills from several sources, listed in [Credits](#credits). Each skill is a folder in `skills/<name>/` with a `SKILL.md`, so any agent that supports [Agent Skills](https://agentskills.io) can load it.

My global instructions, which name some of these skills, live in [adelrodriguez/instructions](https://github.com/adelrodriguez/instructions).

## Contents

- [Install the skills](#install-the-skills)
  - [With the skills CLI](#with-the-skills-cli)
  - [With APM](#with-apm)
- [Requirements](#requirements)
- [Skills](#skills)
- [Credits](#credits)
- [License](#license)

## Install the skills

Many skills call other skills from this repo. When you install only some of them, also install the skills in their **Needs** column under [Skills](#skills).

### With the skills CLI

To pick skills interactively and install them for your agents:

```sh
npx skills add adelrodriguez/skills --global
```

To install some skills without prompts, name them:

```sh
npx skills add adelrodriguez/skills --global --skill pr --skill unslop --skill upload
```

### With APM

To install every skill at user scope with [APM](https://github.com/microsoft/apm):

```sh
apm install --global adelrodriguez/skills
```

To install some of them, list them in your `apm.yml`:

```yaml
dependencies:
  apm:
    - git: adelrodriguez/skills
      skills:
        - pr
        - unslop
        - upload
```

## Requirements

Every skill needs an agent that loads Agent Skills, such as Claude Code, Codex, Cursor, or OpenCode. Some skills need more:

- **GitHub CLI.** The skills that work with pull requests and issues run [`gh`](https://cli.github.com), and it must be logged in.
- **Boat.** `boat` needs the [Boat CLI](https://docs.boat.dev/quickstart), a signed-in account with sandbox access, and `jq` for its shell examples. Integrated agents also need configured model access.
- **Subagents.** `code-review`, `council-review`, `codebase-design`, and `design-review` start other agents, so the agent must be able to run subagents. `hillclimb` needs them only for a judged hill, where a council scores the work. `how`, `why`, and `test-pruning` use subagents when they can, and do the work themselves when they can't.
- **A browser tool.** `interface-design`, `design-review`, and `harden-ui` take screenshots of the rendered page. Without one, they check the code instead and say which checks did not run.
- **Python.** `monitor` runs `scripts/monitor-pr`, which needs Python 3.
- **A public file bucket.** `upload` stores files in a Cloudflare R2 bucket with a public URL, using curl 7.75 or later. It reads the bucket settings from `FILE_UPLOAD_*` environment variables, which the machine must load. See [`upload/SKILL.md`](skills/upload/SKILL.md) for the list.
- **T3 Code.** `housekeeping` cleans up T3 Code worktrees and threads. `sessions` reads T3 Code threads, including those on linked machines, when T3 Code is present.
- **Adamantite.** In a repository that uses [Adamantite](https://github.com/adelrodriguez/adamantite), `modernize` hands the dependencies Adamantite manages to the `adamantite` skill, which ships in that repository's `skills/adamantite` folder.
- **My instructions.** `unslop` applies the "Write clearly" rules from [adelrodriguez/instructions](https://github.com/adelrodriguez/instructions).

## Skills

The **Invoked by** column says who can start each skill. "You" means it starts only when you type its name, such as `/retro`. "You or the agent" means the agent also starts it on its own when a task calls for it.

| Skill | Invoked by | What it does | Needs |
|---|---|---|---|
| `boat` | You or the agent | Selects focused procedures for isolated execution, parallel agents, hosted services, containers, and Linux desktop work | Boat CLI, `jq` |
| `code-review` | You or the agent | Has an independent reviewer find issues, then checks and fixes them, for up to three rounds | Subagents, `gh` |
| `codebase-design` | You or the agent | Designs module interfaces, APIs, and folder layout from the callers outward, and compares at least two designs | Subagents, `testing` |
| `coding-standards` | You or the agent | Records the coding rules that no check can enforce in `CODING_STANDARDS.md`, each backed by a real mistake, and prunes stale ones | `writing-for-agents`, `unslop` |
| `comment` | You or the agent | Posts a pull request or issue comment that says an agent wrote it | `gh`, `unslop`, `upload`, `monitor` |
| `consistency` | You or the agent | Applies one pattern to every matching place in a scope, after a dry run | `codebase-design` |
| `council-review` | You or the agent | Runs `code-review` with several reviewers, which can be different models, and compares their scores | Subagents, `code-review` |
| `design-context` | You or the agent | Records the product in `PRODUCT.md` and the visual system in `DESIGN.md`, and asks only what the code can't answer | None |
| `design-review` | You or the agent | Reviews a design through two independent lenses, screenshots and code, and ranks the verified findings | Subagents, a browser tool, `interface-design` |
| `full-send` | You or the agent | Takes a task all the way to a merged pull request without stopping to ask | `pr`, `code-review`, `monitor`, `upload` |
| `full-stop` | You or the agent | Runs `full-send` until the pull request is ready, then hands it back unmerged | `full-send` |
| `harden-ui` | You or the agent | Breaks UI with worst-case data, failed requests, and missing permissions behind a dev-only switch, then reports a fix for each break | A browser tool, `testing` |
| `hillclimb` | You or the agent | Turns a goal into a score and target, then raises the score one measured round at a time and keeps only the rounds that improve it | `pr`, `council-review` for judged hills |
| `housekeeping` | You | Cleans up old agent worktrees, temp files, and build caches across the machine, after a dry run | T3 Code, `gh`, `sessions` |
| `how` | You | Explains how a subsystem works, or where code belongs, from the source | None |
| `interface-design` | You or the agent | Designs pages, screens, and components from the subject instead of the category default, and checks the render | A browser tool, `design-context`, `writing-for-humans`, `restraint` |
| `issue` | You or the agent | Files a GitHub issue after checking for duplicates, with evidence, labels, and links | `gh`, `unslop`, `upload` |
| `janitor` | You or the agent | Cleans up what a task, a session, or every agent session left behind, such as processes, browsers, simulators, and temp files | `housekeeping`, `sessions` |
| `maintenance` | You | Upgrades dependencies, replaces old patterns, and prunes tests across a repository, one pull request per part | `modernize`, `consistency`, `test-pruning`, `pr` |
| `modernize` | You | Upgrades dependencies, reads their release notes, and adopts the changes | `consistency`, `pr` |
| `monitor` | You or the agent | Watches a pull request until its checks pass and its reviewers approve, and fixes what they find | Python 3, `gh`, `comment`, `upload` |
| `next-task` | You or the agent | Recommends the one unblocked issue to do next | `gh` |
| `pr` | You or the agent | Opens a pull request with a problem-first description and evidence | `gh`, `unslop`, `upload`, `monitor`, `comment` |
| `refresh` | You or the agent | Rebases a pull request onto its base, adapts it to what merged since, and pushes it | `gh`, `pr`, `monitor` |
| `restraint` | You or the agent | Cuts additions down to what improves the user's outcome | None |
| `retro` | You | Reviews agent sessions and the project's history, then proposes changes to instructions, skills, and checks | `gh`, `writing-for-agents`, `coding-standards`, `sessions` |
| `sessions` | You or the agent | Finds and reads agent sessions in T3 Code, Claude Code, Codex, and OpenCode, including T3 Code threads on linked machines, and matches worktrees and processes to them | None |
| `takeover` | You or the agent | Finishes someone else's pull request, branch, or thread on its own branch, and keeps their credit | `gh`, `refresh`, `pr`, `monitor`, T3 Code for threads |
| `test-pruning` | You | Sorts every test into delete, strengthen, rewrite, or keep, and applies the changes | `testing` |
| `testing` | You or the agent | Writes tests that prove behavior through the public interface, with bug fixes test-first | `codebase-design` |
| `unslop` | You or the agent | Rewrites text to remove filler, jargon, and patterns that sound generated | My instructions |
| `upload` | You or the agent | Uploads a file to a public bucket and returns its URL | R2 bucket, curl, `FILE_UPLOAD_*` environment variables |
| `what` | You | Restates the last message in plain language | `unslop` |
| `why` | You | Investigates why code is shaped the way it is, from history, issues, and docs, and rates its confidence | `gh` |
| `writing-changesets` | You or the agent | Writes changesets for the parts of a diff that users notice | `writing-documentation`, `unslop` |
| `writing-documentation` | You or the agent | Writes and reorganizes documentation by the four [Diátaxis](https://diataxis.fr) types | `unslop` |
| `writing-for-agents` | You or the agent | Writes skills and `AGENTS.md` files that agents follow the same way every run | `writing-documentation`, `restraint`, `unslop` |
| `writing-for-humans` | You or the agent | Writes product and marketing copy without filler or sales language | `restraint`, `unslop`, `harden-ui` |

## Credits

Many of these skills started as someone else's. Each `SKILL.md` links its sources under `metadata.reference`:

- [t3dotgg/tstack](https://github.com/t3dotgg/tstack)
- [Boat documentation](https://docs.boat.dev/ai-tools) and [cloud-sandbox-vm-skills](https://github.com/ariana-dot-dev/cloud-sandbox-vm-skills)
- [cursor/plugins](https://github.com/cursor/plugins)
- [mattpocock/skills](https://github.com/mattpocock/skills)
- [blader/humanizer](https://github.com/blader/humanizer)
- [Diátaxis](https://diataxis.fr)
- [Agents sucked at UI (until today)](https://youtu.be/xq0eB8vxeqk) by Theo Browne
- [Less is more](https://jakub.kr/writing/less-is-more) by Jakub Krehel
- [pbakaus/impeccable](https://github.com/pbakaus/impeccable)
- [anthropics/skills](https://github.com/anthropics/skills)
- [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)
- [emilkowalski/skills](https://github.com/emilkowalski/skills)

## License

[MIT](LICENSE)

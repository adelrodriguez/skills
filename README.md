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
- **Subagents.** `code-review`, `council-review`, `codebase-design`, and `design-review` start other agents, so the agent must be able to run subagents. `hillclimb` needs them only for a judged hill, where a council scores the work. `footguns`, `how`, `why`, and `prune` use subagents when they can, and do the work themselves when they can't.
- **A browser tool.** `design-ui`, `design-review`, and `harden-ui` take screenshots of the rendered page. Without one, they check the code instead and say which checks did not run.
- **Python.** `monitor` runs `scripts/monitor-pr`, which needs Python 3.
- **A public file bucket.** `upload` stores files in a Cloudflare R2 bucket with a public URL, using curl 7.75 or later. It reads the bucket settings from `FILE_UPLOAD_*` environment variables, which the machine must load. See [`upload/SKILL.md`](skills/upload/SKILL.md) for the list.
- **T3 Code.** `housekeeping` cleans up T3 Code worktrees and threads. `sessions` reads T3 Code threads, including those on linked machines, when T3 Code is present.
- **Adamantite.** In a repository that uses [Adamantite](https://github.com/adelrodriguez/adamantite), `modernize` hands the dependencies Adamantite manages to the `adamantite` skill, which ships in that repository's `skills/adamantite` folder.
- **My instructions.** `unslop` applies the "Write clearly" rules from [adelrodriguez/instructions](https://github.com/adelrodriguez/instructions).

## Skills

A ✓ under **Agent invocation** means the agent also starts the skill on its own when a task calls for it. You can start every skill by typing its name, such as `/retro`, and a skill without a ✓ starts only that way.

| Skill | Agent invocation | What it does | Needs |
|---|---|---|---|
| `boat` | ✓ | Selects focused procedures for isolated execution, parallel agents, hosted services, containers, and Linux desktop work | Boat CLI, `jq` |
| `code-review` | ✓ | Has an independent reviewer find issues, then checks and fixes them, for up to three rounds | Subagents, `gh` |
| `codebase-design` | ✓ | Designs module interfaces, APIs, and folder layout from the callers outward, and compares at least two designs | Subagents, `testing` |
| `coding-standards` | ✓ | Records the coding rules that no check can enforce in `CODING_STANDARDS.md`, each backed by a real mistake, and prunes stale ones | `writing-for-agents`, `unslop` |
| `comment` | ✓ | Posts a pull request or issue comment that says an agent wrote it | `gh`, `unslop`, `upload`, `monitor` |
| `consistency` | ✓ | Applies one pattern to every matching place in a scope, after a dry run | `codebase-design` |
| `council-review` | ✓ | Runs `code-review` with several reviewers, which can be different models, and compares their scores | Subagents, `code-review` |
| `design-context` | ✓ | Records the product in `PRODUCT.md` and the visual system in `DESIGN.md`, and asks only what the code can't answer | None |
| `design-review` | ✓ | Reviews a design through two independent lenses, screenshots and code, and ranks the verified findings | Subagents, a browser tool, `design-ui` |
| `design-ui` | ✓ | Designs pages, screens, and components from the subject instead of the category default, and checks the render | A browser tool, `design-context`, `writing-for-humans`, `restraint` |
| `footguns` | ✓ | Finds code that lets mistakes pass the type checker, such as implicit state machines and unenforced invariants, and reports each with a failure scenario and a fix | `codebase-design`, `issue` |
| `full-send` | ✓ | Takes a task all the way to a merged pull request without stopping to ask | `pr`, `code-review`, `monitor`, `upload` |
| `full-stop` | ✓ | Runs `full-send` until the pull request is ready, then hands it back unmerged | `full-send` |
| `harden-ui` | ✓ | Breaks UI with worst-case data, failed requests, and missing permissions behind a dev-only switch, then reports a fix for each break | A browser tool, `testing` |
| `hillclimb` | ✓ | Turns a goal into a score and target, then raises the score one measured round at a time and keeps only the rounds that improve it | `pr`, `council-review` for judged hills |
| `housekeeping` |  | Cleans up old agent worktrees, temp files, and build caches across the machine, after a dry run | T3 Code, `gh`, `sessions` |
| `how` |  | Explains how a subsystem works, or where code belongs, from the source | None |
| `issue` | ✓ | Files a GitHub issue after checking for duplicates, with evidence, labels, and links | `gh`, `unslop`, `upload` |
| `janitor` | ✓ | Cleans up what a task, a session, or every agent session left behind, such as processes, browsers, simulators, and temp files | `housekeeping`, `sessions` |
| `maintenance` | ✓ | Prunes unused material, upgrades dependencies, replaces old patterns, and prunes tests across a repository, one pull request per part | `prune`, `modernize`, `consistency`, `pr` |
| `modernize` | ✓ | Upgrades dependencies, reads their release notes, and adopts the changes | `consistency`, `pr` |
| `monitor` | ✓ | Watches a pull request until its checks pass and its reviewers approve, and fixes what they find | Python 3, `gh`, `comment`, `upload` |
| `next-task` | ✓ | Recommends the one unblocked issue to do next | `gh` |
| `pr` | ✓ | Opens a pull request with a problem-first description and evidence | `gh`, `unslop`, `upload`, `monitor`, `comment` |
| `prune` | ✓ | Removes unused tests, dependencies, dead code, suppressions, workarounds, feature flags, assets, and config, and strengthens weak tests | `testing`, `modernize` for upgrades |
| `refresh` | ✓ | Rebases a pull request onto its base, adapts it to what merged since, and pushes it | `gh`, `pr`, `monitor` |
| `restraint` | ✓ | Cuts additions down to what improves the user's outcome | None |
| `retro` |  | Reviews agent sessions and the project's history, then proposes changes to instructions, skills, and checks | `gh`, `writing-for-agents`, `coding-standards`, `sessions` |
| `sessions` | ✓ | Finds and reads agent sessions in T3 Code, Claude Code, Codex, and OpenCode, including T3 Code threads on linked machines, and matches worktrees and processes to them | None |
| `takeover` | ✓ | Finishes someone else's pull request, branch, or thread on its own branch, and keeps their credit | `gh`, `refresh`, `pr`, `monitor`, T3 Code for threads |
| `testing` | ✓ | Writes tests that prove behavior through the public interface, with bug fixes test-first | `codebase-design` |
| `triage` | ✓ | Assesses issues, finds duplicates, proposes project trackers for approval, and recommends actionable work | `gh`, `sessions`, `comment`, `issue`, `next-task` |
| `unslop` | ✓ | Rewrites text to remove filler, jargon, and patterns that sound generated | My instructions |
| `upload` | ✓ | Uploads a file to a public bucket and returns its URL | R2 bucket, curl, `FILE_UPLOAD_*` environment variables |
| `what` |  | Restates the last message in plain language | `unslop` |
| `why` |  | Investigates why code is shaped the way it is, from history, issues, and docs, and rates its confidence | `gh` |
| `writing-changesets` | ✓ | Writes changesets for the parts of a diff that users notice | `writing-documentation`, `unslop` |
| `writing-documentation` | ✓ | Writes and reorganizes documentation by the four [Diátaxis](https://diataxis.fr) types | `unslop` |
| `writing-for-agents` | ✓ | Writes skills and `AGENTS.md` files that agents follow the same way every run | `writing-documentation`, `restraint`, `unslop` |
| `writing-for-humans` | ✓ | Writes product and marketing copy without filler or sales language | `restraint`, `unslop`, `harden-ui` |

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

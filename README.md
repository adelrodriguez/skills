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
- **Subagents.** `code-review`, `council-review`, `codebase-design`, and `design-review` start other agents, so the agent must be able to run subagents. `hillclimb` needs them only for a judged hill, where a council scores the work. `how`, `why`, and `test-pruning` use subagents when they can, and do the work themselves when they can't.
- **A browser tool.** `interface-design`, `design-review`, and `harden-ui` take screenshots of the rendered page. Without one, they check the code instead and say which checks did not run.
- **Python.** `monitor` runs `scripts/monitor-pr`, which needs Python 3.
- **A public file bucket.** `upload` stores files in a Cloudflare R2 bucket with a public URL, using curl 7.75 or later. It reads the bucket settings from `FILE_UPLOAD_*` environment variables, which the machine must load. See [`upload/SKILL.md`](skills/upload/SKILL.md) for the list.
- **T3 Code.** `housekeeping` cleans up T3 Code worktrees and threads.
- **My instructions.** `unslop` applies the "Write clearly" rules from [adelrodriguez/instructions](https://github.com/adelrodriguez/instructions).

## Skills

| Skill | What it does | Needs |
|---|---|---|
| `code-review` | Has an independent reviewer find issues, then checks and fixes them, for up to three rounds | Subagents, `gh` |
| `codebase-design` | Designs module interfaces, APIs, and folder layout from the callers outward, and compares at least two designs | Subagents, `testing` |
| `comment` | Posts a pull request or issue comment that says an agent wrote it | `gh`, `unslop`, `upload`, `monitor` |
| `consistency` | Applies one pattern to every matching place in a scope, after a dry run | `codebase-design` |
| `council-review` | Runs `code-review` with several reviewers, which can be different models, and compares their scores | Subagents, `code-review` |
| `design-context` | Records the product in `PRODUCT.md` and the visual system in `DESIGN.md`, and asks only what the code can't answer | None |
| `design-review` | Reviews a design through two independent lenses, screenshots and code, and ranks the verified findings | Subagents, a browser tool, `interface-design` |
| `full-send` | Takes a task all the way to a merged pull request without stopping to ask | `pr`, `code-review`, `monitor`, `upload` |
| `full-stop` | Runs `full-send` until the pull request is ready, then hands it back unmerged | `full-send` |
| `harden-ui` | Breaks UI with worst-case data, failed requests, and missing permissions behind a dev-only switch, then reports a fix for each break | A browser tool, `testing` |
| `hillclimb` | Turns a goal into a score and target, then raises the score one measured round at a time and keeps only the rounds that improve it | `pr`, `council-review` for judged hills |
| `housekeeping` | Cleans up old agent worktrees, temp files, and build caches across the machine, after a dry run | T3 Code, `gh` |
| `how` | Explains how a subsystem works, or where code belongs, from the source | None |
| `interface-design` | Designs pages, screens, and components from the subject instead of the category default, and checks the render | A browser tool, `design-context`, `writing-for-humans`, `restraint` |
| `issue` | Files a GitHub issue after checking for duplicates, with evidence, labels, and links | `gh`, `unslop`, `upload` |
| `janitor` | Cleans up what a task, a session, or every agent session left behind, such as processes, browsers, simulators, and temp files | `housekeeping`, T3 Code for other sessions |
| `maintenance` | Upgrades dependencies, replaces old patterns, and prunes tests across a repository, one pull request per part | `modernize`, `consistency`, `test-pruning`, `pr` |
| `modernize` | Upgrades dependencies, reads their release notes, and adopts the changes | `consistency`, `pr` |
| `monitor` | Watches a pull request until its checks pass and its reviewers approve, and fixes what they find | Python 3, `gh`, `comment`, `upload` |
| `next-task` | Recommends the one unblocked issue to do next | `gh` |
| `pr` | Opens a pull request with a problem-first description and evidence | `gh`, `unslop`, `upload`, `monitor`, `comment` |
| `refresh` | Rebases a pull request onto its base, adapts it to what merged since, and pushes it | `gh`, `pr`, `monitor` |
| `restraint` | Cuts additions down to what improves the user's outcome | None |
| `takeover` | Finishes someone else's pull request, branch, or thread on its own branch, and keeps their credit | `gh`, `refresh`, `pr`, `monitor`, T3 Code for threads |
| `test-pruning` | Sorts every test into delete, strengthen, rewrite, or keep, and applies the changes | `testing` |
| `testing` | Writes tests that prove behavior through the public interface, with bug fixes test-first | `codebase-design` |
| `unslop` | Rewrites text to remove filler, jargon, and patterns that sound generated | My instructions |
| `upload` | Uploads a file to a public bucket and returns its URL | R2 bucket, curl, `FILE_UPLOAD_*` environment variables |
| `what` | Restates the last message in plain language | `unslop` |
| `why` | Investigates why code is shaped the way it is, from history, issues, and docs, and rates its confidence | `gh` |
| `writing-changesets` | Writes changesets for the parts of a diff that users notice | `writing-documentation`, `unslop` |
| `writing-documentation` | Writes and reorganizes documentation by the four [Diátaxis](https://diataxis.fr) types | `unslop` |
| `writing-for-agents` | Writes skills and `AGENTS.md` files that agents follow the same way every run | `writing-documentation`, `restraint`, `unslop` |
| `writing-for-humans` | Writes product and marketing copy without filler or sales language | `restraint`, `unslop`, `harden-ui` |

## Credits

Many of these skills started as someone else's. Each `SKILL.md` links its sources under `metadata.reference`:

- [t3dotgg/tstack](https://github.com/t3dotgg/tstack)
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

# Targets and candidate categories

## Targets

A target is a file or check that a finding changes. Edit a target in the repository that owns its source of truth, never in an installed copy, because the next install overwrites the copy. A missing target is still a valid target. Propose creating it with the skill named in its row.

| Target | What belongs there | Source of truth | Create it with |
|---|---|---|---|
| Global rules | Rules that apply in every project, such as the files in `~/.claude/rules/` and `~/.codex/AGENTS.md` | The `adelrodriguez/instructions` repository | `writing-for-agents` |
| Skills | A workflow the agent follows for one kind of task | The repository the skill was installed from: `adelrodriguez/skills` for a skill in its README, otherwise the skill's `metadata.reference` or its APM dependency | `writing-for-agents` |
| `AGENTS.md` or `CLAUDE.md` in the repository | Navigation pointers to other files, and facts every task in the repository needs. Every line loads on every turn | The repository | `writing-for-agents` |
| `CODING_STANDARDS.md` | Judgement calls that a reviewer checks against the diff, such as consistency across files | The repository | `coding-standards` |
| `GLOSSARY.md` and ADRs | Domain terms, and decisions with their reasons | The repository | `writing-documentation` |
| `PRODUCT.md` and `DESIGN.md` | The product's users and goals, and its visual system | The repository | `design-context` |
| Docs | Reference that an agent document points to | The repository's docs folder | `writing-documentation` |
| Checks | Lint rules, type checks, tests, pre-commit hooks, and CI jobs | The repository's check config and CI workflows | `coding-standards`, which adds the check to the tools the repository already runs |
| Tools | Scripts and CLIs that replace expensive tool calls | The skill's `scripts/` folder, or the repository's scripts | A script in the skill or repository |
| Harness reference | How agents find and read sessions in each harness | The `sessions` skill | `writing-for-agents` |

## Candidate categories

Each category lists its signal, which is what to look for in the sessions and history, and the target it usually changes.

| Category | Signal | Usual target |
|---|---|---|
| Rework | The history shows a rename, move, rewrite, revert, or reorganization of work that a session or an earlier pull request created | The rule, glossary term, ADR, or design step that would have produced the final version first |
| Corrections | The user corrected the agent, or repeated a correction from an earlier session | A global rule when the correction applies to every project, otherwise the repository's `AGENTS.md` or `CODING_STANDARDS.md` |
| Missed trigger | A rule or skill existed, but the agent did not load or follow it | The skill's `description` or the pointer that should have loaded the rule, following "Write the trigger" in `writing-for-agents` |
| Navigation | The agent spent many tool calls finding a file, or missed a dependency between files | A navigation pointer in `AGENTS.md` or in the file the agent read first |
| Automated checks | The agent made a mistake that a check could catch, or the repository has no pre-commit hook and no CI job running its lint, type check, and tests | A check. Read the repository's check command and CI workflow first, because an existing check that is not wired up or is broken is the finding |
| Coding standards | The reviewer missed a mistake, or flagged one that no rule covers | A check or a rule in `CODING_STANDARDS.md`, as the `coding-standards` skill sorts it |
| Steering bloat | An always-loaded file is long, holds coding rules, or holds lines that do not change what the agent does. A rule in `CODING_STANDARDS.md` meets a condition in the "Prune the file" step of the `coding-standards` skill | Move a coding rule to `CODING_STANDARDS.md` or a check, or delete the line or rule |
| Tool economy | A tool call returned far more output than the agent used, or the agent repeated the same sequence of calls | A script, a narrower command in the skill, or a fix to the tool |
| Information access | The agent lacked information it needed, such as dev server logs, a third-party service, or another machine's sessions | Read-only access, such as logs written to a file or a tool for the service |
| Harness coverage | The retro could not read a harness, machine, or session store | The `sessions` skill |

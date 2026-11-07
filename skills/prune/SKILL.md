---
name: prune
description: Use when the user says "prune" or asks to remove unused tests, dependencies, dead code, suppressions, workarounds, feature flags, assets, or config.
---

# Prune a repository

Remove what a repository no longer uses. Prove each removal with the evidence its target requires. For tests, also strengthen weak tests and rewrite tests that reach past the interface.

## Set the scope

Use the targets and paths the user names. When they name no targets, use every target below. When they name no paths, use the whole repository.

For example:

```text
/prune
/prune tests
/prune dependencies dead-code src/api
```

Use this order, and read only the reference files for the selected targets:

| Target | Covers | Reference |
|---|---|---|
| `feature-flags` | Settled flags and their inactive branches | [Feature flags](references/feature-flags.md) |
| `workarounds` | Workarounds whose removal condition is met | [Workarounds](references/workarounds.md) |
| `dead-code` | Unused files, exports, members, and obsolete code comments | [Dead code](references/dead-code.md) |
| `suppressions` | Lint and type suppressions that suppress nothing | [Suppressions](references/suppressions.md) |
| `config` | Unused environment declarations, scripts, jobs, and settings | [Config](references/config.md) |
| `assets` | Unused images, fonts, icons, styles, and translation keys | [Assets](references/assets.md) |
| `dependencies` | Unused packages, patches, overrides, and resolutions | [Dependencies](references/dependencies.md) |
| `tests` | Redundant, weak, and obsolete tests | [Tests](references/tests.md) |

Search the whole repository for consumers even when edits are scoped to a path. Include necessary companion changes, such as a lockfile update, in the dry run. Report unrelated candidates outside the scope instead of removing them.

The step is done when the targets and paths are listed, the selected references are read, and every test file in the tests scope is listed.

## Record the baseline

Run the repository's checks, build, and tests relevant to the scope, using its scripts. When it has a coverage command, run it too.

Record the commands, their results, and the counts described in each selected reference. Include the test count, run time, and coverage when available. Record existing failures without fixing them as part of the baseline.

The step is done when every selected target has a baseline, and every unavailable check or existing failure is recorded.

## Find and classify the candidates

Follow each selected reference's detection and proof rules in the target order. Read each candidate and its consumers. A detector finding or a passing build alone does not prove that something is unused.

Put each candidate in exactly one group:

- **Remove.** The target's proof is complete. Record the evidence.
- **Keep.** It still has a consumer or a required purpose. Record that use.
- **Ask.** The evidence is incomplete, or removal needs a product or compatibility decision. Record what is missing.

The tests reference adds **Strengthen** and **Rewrite**. Classify every test in scope, including tests that failed at the baseline.

Keep public APIs with external consumers, database schema, remote branches, and changes to supported runtimes outside this pass. Leave Ask candidates untouched until the missing evidence is available or the user explicitly decides their removal.

The step is done when every candidate has one group and its evidence or missing decision, and every test in scope has one group.

## Show the dry run

Show one short list per target and group, with each item's file, name, reason, and evidence. Give only the Keep count. For Ask, show the missing evidence or decision.

Count every file that will change, including companion changes. When fewer than five files will change, or the user already approved these changes, continue without waiting. Otherwise, wait for the user's agreement.

The step is done when the concrete changes are listed and either fewer than five files will change or the user has approved them.

## Prune

Apply the selected targets in the table's order, so later targets can remove material left unused by earlier ones. Follow each reference's removal rules. Keep each target and group in its own commit, with the companion changes needed to keep that commit working.

Run the affected checks after each group. Restore changes that introduce failures you cannot fix within the group, and move those candidates to Ask.

Rerun the selected detectors after the removals. Classify newly exposed candidates and update the dry run before removing them. Report candidates in unselected targets instead of starting another target.

The step is done when every planned change is committed or moved to Ask, and no proven removal remains in the selected scope.

## Compare with the baseline

Run the same commands and recount with the same definitions. Explain every new failure and every drop in coverage.

A coverage drop is acceptable only when it comes from code that no longer exists, or from a test of the framework or a library. Otherwise, restore the test or add a test at the interface that covers the lost behavior, following the `testing` skill.

The step is done when the checks pass or fail only as they did at the baseline, and every drop in coverage has a reason.

## Return the result

If a tool, source, or check was unavailable, say so on the first line and name what you used instead.

Return a before-and-after table with the selected targets' counts, the test count, run time, and coverage when available. List the removed, strengthened, and rewritten items with their reasons and evidence. Include the Keep count, the Ask candidates, and any candidates outside the scope. State whether each baseline failure still occurs.

## Check the pruning

- Every selected target followed its reference's proof and removal rules.
- Every candidate, and every test in scope, has exactly one group.
- Every removal has evidence, and every Ask candidate remains untouched unless the user explicitly decided its removal.
- Each target and group has its own commit, including its necessary companion changes.
- The selected detectors were rerun, and no proven removal remains in scope.
- Checks pass or match the baseline failures, and every drop in coverage has a reason.

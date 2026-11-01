---
name: maintenance
description: Upgrade dependencies, replace old patterns, make code consistent, and prune tests across a repository.
disable-model-invocation: true
---

# Maintain a repository

Run a full maintenance pass on a repository that has drifted: upgrade its dependencies, replace old patterns, make the code consistent, and prune its tests. This skill orders the work and chooses what to do. The `modernize`, `consistency`, and `test-pruning` skills do each part.

## Set the scope

Use the repository and the parts of the pass the user names. When they name none, run every part below on the whole repository.

The step is done when the scope is a repository and a list of parts.

## Survey the repository

Read the repository's `AGENTS.md`, `CODING_STANDARDS.md`, and the last few months of merged PRs. Then collect the candidates for each part:

- **Dependencies.** The outdated packages.
- **Old patterns.** Code that predates the repository's current standards, or that the repository wrote for itself where a library it uses now ships the primitive. Search for patterns the standards forbid, code that recent PRs replaced in some places but not others, and deprecated APIs.
- **Consistency.** Places where the repository solves the same problem in more than one way, and places where it differs from my other repositories without a reason.
- **Tests.** The size and run time of the suite, and folders that look duplicated or weak.

The step is done when every part in the scope has a list of candidates, or a note that it has none.

## Plan the pass

Order the parts:

1. **Dependencies,** because new versions ship primitives that change which old patterns to replace.
2. **Old patterns,** one pattern at a time.
3. **Consistency,** one pattern at a time.
4. **Tests,** last, so pruning does not remove coverage the refactors relied on.

Within old patterns and consistency, rank each pattern by the number of sites and how often it causes bugs or review comments. Drop a pattern that touches only one or two sites, and list it in the result instead.

Show the plan as a dry run: one bullet per part, with its patterns and site counts. Wait for the user's agreement.

The step is done when the user agrees.

## Run each part

Run each part on its own branch, and file its PR with the `pr` skill before you start the next part:

- **Dependencies:** follow the `modernize` skill.
- **Old patterns** and **Consistency:** follow the `consistency` skill once per pattern. Several patterns may share a PR when each is in its own commit.
- **Tests:** follow the `test-pruning` skill.

Base each part on the previous part's branch when it depends on it, and stack the PRs. Otherwise base it on the default branch.

The step is done when every part has a PR, or a reason it was skipped.

## Check the pass

- Each part ran in the planned order, and on its own branch.
- Each part followed its skill's own checks.
- Every PR's checks pass.

## Return the result

Return one line per part with its PR link and a one-line summary. Then list the patterns dropped for having too few sites, and the design sites the `consistency` runs proposed.

---
name: modernize
description: Use when upgrading a repository's dependencies and adopting the changes in the new versions.
---

# Upgrade the dependencies

Bring a repository's dependencies up to date, read what changed in each one, and adopt the changes the new versions ask for. An upgrade is done when the code uses the new version the way its authors intend, not only when it installs.

## Set the scope

Use the packages or workspaces the user names. When they name none, use every dependency in the repository, including dev dependencies, workspace catalogs, engines, and the package manager itself.

When the repository uses Adamantite, update the dependencies it manages with the `adamantite` skill, and leave them out of this scope.

The step is done when the scope is a list of packages.

## Record the baseline

Run the repository's checks, build, and tests. When one already fails, record it, and do not fix it as part of the upgrade.

The step is done when you have recorded the result of each check.

## List what is outdated

For each outdated package, record the current version, the latest version, and whether the jump is a patch, a minor, or a major.

The step is done when every package in the scope has a current and a latest version.

## Read what changed

For each minor and major jump, read the release notes from the package's primary sources: its GitHub releases, its `CHANGELOG.md`, and its migration guide. Use `packref` to read the source of the new version when the notes are thin.

Record, for each package:

- Breaking changes that touch code in this repository.
- Deprecations of APIs this repository uses.
- New APIs that replace code this repository wrote for itself.
- Changes to the minimum Node, TypeScript, or peer-dependency versions.

The step is done when every minor and major jump has its notes recorded, or a note that none exist.

## Plan the upgrade

Group the upgrades:

- **Batch.** Patches and minors with no recorded breaking change. These go in one commit.
- **Alone.** Each major, and each minor with a breaking change. Each goes in its own commit, together with the code changes it needs.
- **Together.** Packages that must move in lockstep, such as a framework and its plugins. Each set goes in one commit.
- **Hold.** Upgrades blocked by a peer dependency or a runtime version. Give the blocker.

Show the groups as a dry run, with the recorded breaking changes and new APIs for each alone and together group. Wait for the user's agreement.

The step is done when the user agrees.

## Upgrade

Apply the groups in this order: batch, then together, then alone.

For each group:

1. Upgrade with the package manager, so the lockfile updates with it.
2. Apply the breaking changes, and replace deprecated APIs.
3. Replace code this repository wrote for itself when the new version ships it. Follow the `consistency` skill when the replacement spans many sites.
4. Run the checks, build, and tests, and fix what failed because of the upgrade.
5. Commit the group.

When a group cannot pass without a change outside the upgrade, revert the group and move it to hold.

The step is done when every group is committed or on hold.

## Check the upgrade

- Every minor and major jump had its release notes read.
- Every recorded breaking change and deprecation was applied or explained.
- Each group is in its own commit, with its code changes.
- The checks, build, and tests pass, or fail only as they did at the baseline.

## Return the result

Return a table of the upgraded packages with the old and new versions. Then list the code changes each upgrade required, the packages on hold with their blockers, and the checks that failed at the baseline. File the PR with the `pr` skill.

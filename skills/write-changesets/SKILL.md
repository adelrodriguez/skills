---
name: write-changesets
description: Use when writing a changeset, or before filing a PR in a repository that uses changesets.
---

# Write changesets

Write the changesets for a diff, so the release notes tell the developers who use the package what changed for them. A changeset is one entry file in `.changeset/`. A change is one feature, fix, or breaking change, not one file.

## Find the change

Read the staged changes with `git diff --staged`. When nothing is staged, read the branch's changes against its base with `git diff origin/<base>...HEAD`.

Read `.changeset/config.json` for packages it ignores and packages it versions together. Only packages that are published, which means not `private` in their `package.json`, get a changeset.

The step is done when you have the diff and the list of published packages it touches.

## Sort the changes

Put each change in the diff in one of these groups:

- **Write.** A developer using the package can notice it: a new feature, a fixed bug, a breaking change, a performance gain, or a dependency update that changes behavior.
- **Skip.** Internal refactoring, reorganized code, test-only changes, and cosmetic cleanups. When internal cleanup carries a small user-facing fix, put only the fix in the write group.

When the write group is empty, write no changeset, and say so.

The step is done when every change is in exactly one group.

## Match the pending changesets

Read every changeset in `.changeset/`, ignoring `README.md`. These are pending: their changes are not released yet.

For each change in the write group, decide:

- **Expand.** A pending changeset covers the same feature, fix, or API in the same package. When the change fixes or adjusts something that changeset added, fold it in without a separate mention, because users never saw the earlier version.
- **New.** No pending changeset covers it. Give it its own changeset, even when another change in the same package also gets one.

The step is done when every change in the write group is marked expand, with the changeset's path, or new.

## Pick the version bump

Use semantic versioning, with these choices:

- Bump a performance gain or a dependency update as a patch.
- Below 1.0.0, bump a breaking change as a minor. Use major only when the user asks for it.
- When you expand a changeset, keep the higher of its bump and the change's bump.

The step is done when every changeset you will write has a bump for each package it names.

## Write each changeset

Rewrite each expanded changeset in place, so it describes the combined result. Create each new changeset with the repository's package runner, such as `bunx changeset --empty`, and fill in the file it creates.

A changeset is reference: it describes what changed, in the product's terms. Follow `references/reference.md` and `references/style.md` in the `writing-documentation` skill. For a breaking change, add the steps to migrate as a short how-to, following `references/how-to-guide.md` in the same skill.

Start with one line that names the change from the user's side:

- Avoid: `This changeset updates the internal implementation to improve code organization`
- Avoid: `The system has been enhanced to provide improved functionality`
- Prefer: `Fix race condition in file watcher when multiple saves occur rapidly`
- Prefer: `Add --dry-run flag to preview changes without writing files`

Add a paragraph only when a user needs more than that line to use the change, such as how a new option behaves or how to migrate:

```markdown
---
"package-name": minor
---

Add `--watch` mode for continuous file monitoring

Runs the command once, then re-runs whenever source files change. Uses filesystem events when available, and falls back to polling on unsupported platforms.
```

Use the `unslop` skill on the prose.

The step is done when every change in the write group is in a changeset.

## Check the changesets

- Every change in the write group is in exactly one changeset, and no changeset mentions a change in the skip group.
- Every change that a pending changeset covers expanded it instead of adding a new one.
- Every changeset names only published packages that its changes touch.
- Every breaking change has a major bump, or a minor bump below 1.0.0, and steps to migrate.
- Every changeset's first line names the change from the user's side.

## Return the result

Return the path of each changeset you created or expanded, marked as new or expanded, with its packages, bumps, and first line. List the changes you skipped, one line each.

# Dependencies

## Candidates

Unused direct dependencies in any workspace, and patches, overrides, or resolutions whose original requirement no longer applies. Count direct dependency declarations and patch or override entries separately; installed transitive packages are not the baseline unit.

## Detect

Use the repository's dependency analysis tooling. For JavaScript and TypeScript, [Knip](https://knip.dev/overview/getting-started) reports unused dependencies. Check its workspace, entry-point, and plugin coverage before treating the report as evidence.

Search manifests, source, build config, scripts, CI, and documentation for package names and their binaries. For other languages, combine native analysis with package metadata, imports, and entry points. A package can provide a command or plugin without any source import.

For each patch, override, or resolution, record its reason, affected package, and currently resolved version.

## Prove unused

- A package has no consumer in source, scripts, tooling, plugins, or supported builds. Side-effect imports and runtime registration count as consumers.
- A patch's fix is present in the installed version, or its original condition no longer applies. The affected behavior passes without the patch.
- An override or resolution no longer enforces a needed compatibility or security constraint. The resolved versions without it satisfy the original requirement, and the affected checks pass.

A closed upstream issue alone does not prove a patch or override obsolete. A test-only dependency remains used while any test needs it.

## Send to Ask

- Peer or optional dependencies that form part of a published package's contract.
- Packages loaded by name, external scripts, or deployment tooling whose consumers cannot be inspected.
- Patches with no recorded reason or no way to verify the original failure.
- Constraints whose removal requires an upgrade. Upgrades belong to the `modernize` skill.

## Remove

Remove packages with the repository's package manager and regenerate its lockfile. Remove obsolete patch files and their manifest entries together. Keep patches that another workspace or version still needs.

Verify installation from the updated lockfile in a clean dependency environment, without cached patched copies. Run the affected build, tests, and package scripts. Keep unrelated versions unchanged.

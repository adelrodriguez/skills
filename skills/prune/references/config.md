# Config

## Candidates

Unused environment variable declarations, package scripts, CI jobs, path aliases, lint overrides, and settings for removed files or tools. Count entries by kind so a removed CI job is not mixed with a removed alias.

## Detect

Trace each setting from its declaration to its consumers in source, scripts, CI workflows, build tools, deployment config, and documentation. Include framework conventions, package lifecycle scripts, scheduled jobs, and reusable workflows.

A CI job triggered by an event needs no caller. A package script can be a documented command or a lifecycle hook even when no other script names it.

## Prove unused

The entry has no consumer, convention, trigger, or published command contract. Path and lint patterns match no supported source, including generated files. An environment name is read by neither application code nor its framework or deployment tooling.

For CI jobs, removal also leaves required checks and downstream workflows satisfiable. Repository search alone cannot establish branch protection or external workflow usage.

## Send to Ask

- Environment variables read only in unavailable deployments or by external tooling.
- Commands documented for users outside the repository.
- CI jobs whose required-check status or external consumers cannot be inspected.
- Patterns for files generated only in CI or on another supported platform.

## Remove

Remove obsolete repository declarations, schema entries, examples, and documentation together. Remove dependent CI references only when their behavior is also obsolete. Live secrets and hosted settings are separate external changes; report them without changing them.

Run the affected scripts, build, config validation, and workflow checks available in the repository. Verify that surviving jobs still have valid dependencies and that no required environment validation or path resolution breaks.

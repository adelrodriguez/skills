# Dead code

## Candidates

Unreachable branches, unused files, exports, members, and local bindings; commented-out implementation; and TODOs whose obligation is complete. Count files and symbols separately from comment blocks.

## Detect

Use the compiler's unused-code diagnostics and the repository's analyzer. [Knip](https://knip.dev/overview/getting-started) reports unused JavaScript and TypeScript files and exports. [Vulture](https://github.com/jendrikseipp/vulture) finds Python candidates, including findings that need manual confirmation.

Trace consumers from application, test, CLI, worker, and framework entry points. Include dynamic imports, registries, reflection, generated consumers, and builds for other supported platforms.

## Prove unused

- A file or symbol is unreachable from every supported entry point and is not a published contract or a side-effect module.
- A branch cannot run under any supported configuration. A branch absent from test coverage is not enough.
- A commented-out block is abandoned implementation, rather than an example or a record of a still-needed constraint.
- A TODO's requested change is complete in the current code. An issue closed as rejected or superseded does not establish completion.

An unused binding can still run an initializer with required side effects. Its removal must preserve those effects.

## Send to Ask

- Public exports with possible consumers outside the repository.
- Framework hooks, plugin registration, reflection, and generated code whose reachability cannot be established.
- Branches controlled by unavailable runtime settings, or TODOs whose obligation is unresolved.

## Remove

Remove the code and its internal re-exports, imports, and registrations. Remove tests only when the behavior they cover no longer exists; retain coverage for surviving behavior.

Change the source template for generated code, then regenerate. Run the affected compiler, build, and tests, and verify that no dangling reference remains.

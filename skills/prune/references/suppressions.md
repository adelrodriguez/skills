# Suppressions

## Candidates

Lint and type directives that suppress no current diagnostic, such as `eslint-disable`, `biome-ignore`, `@ts-ignore`, `@ts-expect-error`, and `# noqa`. Count directives, including individual rule names in a multi-rule directive.

## Detect

Use the installed checker's unused-suppression diagnostic with the repository's normal rules. Examples include [ESLint's `--report-unused-disable-directives`](https://eslint.org/docs/latest/use/command-line-interface#--report-unused-disable-directives) and [Ruff's `RUF100`](https://docs.astral.sh/ruff/rules/unused-noqa/).

[TypeScript reports unused `@ts-expect-error` directives](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-9.html#-ts-expect-error-comments). It does not report unused `@ts-ignore` directives; remove those temporarily and rerun the actual type check.

For other tools, remove a candidate temporarily and compare diagnostics. A file excluded from the check provides no proof.

## Prove unused

Without the directive, the same checker, rules, and supported configuration matrix report no diagnostic it previously suppressed. A clean result from a cache or a syntax-only build is insufficient.

An unused `@ts-expect-error` in a negative type test can signal a contract regression. The `testing` skill's public-type rules apply before treating that directive as obsolete.

## Send to Ask

- Directives needed by another supported checker version or build configuration.
- Suppressions in generated files whose source is unavailable.
- Directives whose checker does not run, or whose removal exposes a real issue requiring a separate fix.
- Negative type tests whose expected error disappeared without an intended contract change.

## Remove

Remove only the unused rule names when a directive also suppresses live diagnostics. Keep the explanation for any remaining suppression. Change the source template for generated files.

Rerun the affected linter or type checker without cached results. Do not disable a rule or broaden an exclusion to make the removal pass.

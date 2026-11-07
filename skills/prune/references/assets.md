# Assets

## Candidates

Unused images, fonts, icons, stylesheets, CSS classes, and translation keys. Count asset files, CSS classes, and translation keys separately.

## Detect

Use the repository's asset, stylesheet, or translation analysis tooling, then search source, templates, CSS URLs, manifests, public paths, and generated output for each candidate.

Include constructed paths and names, such as `icons/${name}.svg`, CSS classes built from variants, and translation keys assembled from prefixes. An analyzer that sees only literal references misses these consumers.

## Prove unused

No source, generated output, supported theme, locale, or runtime convention consumes the asset or key. Public URLs and files copied by convention need a consumer check beyond source imports.

For example, an icon absent from imports remains used when a template constructs its public URL. A CSS class absent from one page can still be used by another route or by user content.

## Send to Ask

- Assets served to external consumers or referenced by stored user content.
- Dynamic names whose possible values cannot be enumerated.
- Translation fallback, platform, locale, or theme behavior that cannot be verified.
- Generated assets whose source or generator is unavailable.

## Remove

Remove the unused asset and its obsolete declarations, manifests, or generated entries. Change the generator's source when it owns the output. For translation keys, remove the corresponding entries across locales only after checking fallback behavior.

Run the affected build and asset checks, then inspect the affected pages or flows for missing content. Report any render or locale check that could not run.

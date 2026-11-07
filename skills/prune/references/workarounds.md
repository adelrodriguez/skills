# Workarounds

## Candidates

Local fallbacks, compatibility branches, wrappers, and temporary config linked to an upstream defect or an explicit removal condition. Count workaround sites and record each condition separately.

## Detect

Search for workaround comments, upstream issue links, and instructions such as "remove when". Read the code and the original failure before checking the issue or release.

Use the upstream issue, merged fix, release notes, and the repository's resolved dependency and runtime versions to identify whether the removal condition is met.

## Prove unused

The fix has shipped in the version this repository actually uses, or the recorded removal condition is otherwise met. Every supported runtime and platform is covered.

The original failure no longer occurs without the workaround. A merged fix on an unreleased branch, an issue closed without a fix, or an unverified version range is insufficient.

## Send to Ask

- Workarounds with no known original failure or removal condition.
- Fixes unavailable in a supported version or platform.
- Upstream sources or reproduction environments that cannot be accessed.
- Code that now implements an independent requirement in addition to the workaround.

## Remove

Remove the workaround and its obsolete comment or setting together. Keep regression tests that still protect required behavior. When a test asserts only the workaround's implementation, adapt it through the interface using the `testing` skill.

Run the reproduction without the workaround and the affected integration checks. Report a needed version upgrade for the `modernize` skill instead of upgrading within this target.

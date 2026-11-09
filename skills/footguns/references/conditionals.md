# Conditionals

## Candidates

An `if`/`else` chain or `switch` that gains one branch per feature, plan, provider, or type, especially when the same set of cases appears in several places. Adding a case then means finding every chain, and the type checker does not say when one is missed.

## Detect

- Search for chains of three or more branches that compare one value, such as `plan === "pro"` or `provider === "stripe"`.
- Search for the same case values compared in several files.
- Search for `switch` statements with a `default` branch over a closed set of values.

## Confirm

Adding a case, or a case added in the past, misses a chain and takes the wrong branch without an error. For example, the `enterprise` plan was added to the pricing chain but not to the limits chain, so enterprise users get free-tier limits. A missed case in the current code is Confirmed. A chain that a future case could miss is Plausible.

## Reject

- The chain covers an open set, such as user input, where a default branch is the right behavior.
- The chain is exhaustive over a union, the type checker fails when a case is missing, and the cases appear in one place.

## Encode

Move the cases into one lookup table keyed by the union, typed so every key is required:

```ts
const limits: Record<Plan, Limits> = {
  free: { seats: 1 },
  pro: { seats: 10 },
  enterprise: { seats: 500 },
}
```

When the cases carry behavior, use a discriminated union with an exhaustive match, using the repository's match helper when it has one.

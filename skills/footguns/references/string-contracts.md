# String contracts

## Candidates

A string that two or more places must spell the same way, with no shared definition. Examples are event names, cache keys, storage keys, queue and topic names, route paths, feature flag names, analytics events, and translation keys.

## Detect

- Search for string literals passed to `emit`, `on`, `subscribe`, `publish`, `get`, `set`, `invalidate`, `localStorage`, and router helpers.
- Group the literals by value, and list each value that appears in more than one file.
- Search for cache and storage keys built with template strings, and compare the templates across readers and writers.

## Confirm

A reader and a writer use different strings for the same thing, or a rename can change one without the other, and the result is silent. For example, the writer invalidates `user:${id}` but the reader caches `users:${id}`, so profiles stay stale. A mismatch in the current code is Confirmed. A rename that could cause one is Plausible.

## Reject

- Both places import the string from one constant, enum, or generated module.
- The string is an external contract that a typed client or schema already checks.

## Encode

Define each string once and import it in every reader and writer. Build keys with one function, such as `cacheKey.user(id)`. For events, define a typed map from each name to its payload, so a wrong name or payload fails the type check.

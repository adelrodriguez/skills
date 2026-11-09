# Errors

## Candidates

Failures signaled in a way the caller can ignore or confuse with success. Examples are returning `null`, `-1`, `false`, or an empty array on failure, results shaped like `{ ok: false }` or `{ success: boolean, error?: string }`, thrown strings, a generic `Error` with only a message, and `catch` blocks that log and continue.

## Detect

- Search for `return null`, `return -1`, and `return false` in functions that can fail, and for `throw "` and `throw new Error(`.
- Search for result types with a `success`, `ok`, or `error` field.
- Search for `catch` blocks that do not rethrow, return a typed error, or handle a specific error.
- Search for callers that match an error by its message text.

## Confirm

A caller treats the failure as a valid value or cannot tell two failures apart, and the result is wrong. For example, `findUser` returns `null` for both "not found" and "database down", so the login page shows "wrong password" during an outage. Or a `catch` swallows a failed payment, and the order ships.

## Reject

- `null` means a normal absence, such as an optional lookup, and every caller handles it.
- The repository already uses tagged errors or a typed result, and the candidate uses them.

## Encode

Represent each failure as a tagged error that names what failed, using the repository's error primitive, such as Effect's `Data.TaggedError` or a discriminated union of error types. Make the failure part of the function's return or error type, so the caller must handle each tag. Replace message matching with a match on the tag.

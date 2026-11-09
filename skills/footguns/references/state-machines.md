# State machines

## Candidates

Two or more booleans, optional fields, or a status string whose combinations are not all valid. For example, `isLoading`, `error`, and `data` on one object, where `isLoading: true` with `data` set should never happen. Also a `status` field whose allowed transitions live in scattered `if` blocks.

## Detect

- Search for objects and component state with several `is*`, `has*`, or `*ed` booleans, and for fields that are set and cleared together.
- Search for `status`, `state`, `phase`, `step`, and `stage` fields, and list every place that writes them.
- Read each writer. List which combinations or transitions it can produce.

## Confirm

A writer, or a sequence of writers, can produce an invalid combination or an invalid transition. For example, a retry sets `isLoading` without clearing `error`, so the screen shows a spinner and an error at once. Or a cancel handler moves an order from `shipped` back to `pending`.

## Reject

- Every combination of the fields is valid.
- One function owns all writes and already enforces the transitions, and nothing else writes the fields.
- The repository already models the state with a union or a state machine library, and the candidate uses it.

## Encode

Replace the fields with one discriminated union, so each state carries only its own data:

```ts
type Request<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "failure"; error: RequestError }
```

When transitions matter, move them into one function or state machine that accepts an event and returns the next state, and make it reject invalid transitions. Use the repository's state machine library when it has one.

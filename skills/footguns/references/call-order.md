# Call order

## Candidates

An API or module that works only when the caller follows an order that nothing enforces. Examples are `init()` before `send()`, `connect()` before `query()`, setting config before importing a module, registering a plugin before the first render, and `close()` exactly once.

## Detect

- Search for classes and modules with `init`, `setup`, `configure`, `connect`, `start`, `open`, or `register` methods, and for mutable module-level variables that one of them sets.
- Search for comments such as "must be called before", "call first", and "after X".
- Search for imports placed for their side effects, and for import order that a comment says matters.

## Confirm

A caller can use the API in the wrong order, and the API returns a wrong result or fails late with an unclear error. For example, a test imports the mailer before the config module, so `send()` uses an `undefined` API key and fails on the first email.

## Reject

- The API checks the order and fails at once with a clear error, and every caller sits on a path that runs the setup first.
- The language or framework enforces the order, such as a constructor or a dependency injection container.

## Encode

Make the wrong order impossible to write. Have the setup step return the object that the later steps need, such as `const client = await connect(config)` instead of `connect()` then `client.query()`. Inject dependencies instead of reading module state, using the repository's layers or container when it has them. Use the language's scoped resource primitive for open and close, such as `using`, `try`/`finally`, or Effect's `acquireRelease`.

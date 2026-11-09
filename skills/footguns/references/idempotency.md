# Idempotency

## Candidates

A command that changes the result when it runs twice, in a place where it can run twice. Retries, webhooks, queue consumers, cron jobs, migrations, setup scripts, and form submissions can all run twice.

## Detect

- List the webhook handlers, queue consumers, scheduled jobs, migrations, and setup scripts.
- Search those handlers and the mutations they call for blind `INSERT`, `+= 1`, `increment`, `push`, charge and email calls, and file appends.
- Check whether the retry policy, queue, or provider documents at-least-once delivery.

## Confirm

A second run, or a run after a crash halfway through, ends in a different state than one run. For example, the payment provider retries a webhook after a timeout, and the handler credits the account twice. Or a migration that adds a column fails on its second run because the column exists.

## Reject

- An idempotency key, unique constraint, or upsert already makes the second run a no-op.
- Nothing can run the command twice. A user action with no retry and no double-submit path qualifies.

## Encode

Make the command read the current state, compare it to the goal, and apply only the difference. Use an upsert or unique constraint for inserts. Record processed event IDs or idempotency keys for webhooks and messages. Write a migration or setup step so it checks before it changes, such as `CREATE ... IF NOT EXISTS`.

# Races

## Candidates

A check followed by an action, or a read followed by a write, where another request, job, or tab can change the state in between. Examples are "check the username is free, then insert it", "read the balance, then write the new balance", and "check the coupon is unused, then mark it used".

## Detect

- Search for a query followed by an insert or update on the same row or key, outside a transaction.
- Search for counters, balances, stock levels, and quotas updated by reading the value, changing it in code, and writing it back.
- Search for in-memory locks and flags, such as `let isRunning = false`, in code that runs on more than one process or server.
- Check which handlers can run at the same time: concurrent requests, several queue workers, cron overlap, and several browser tabs.

## Confirm

Two concurrent runs can interleave between the check and the action, and both succeed when only one should. For example, two requests redeem the same coupon, both read `used = false`, and both apply the discount. Name the two concurrent runs and the step where they interleave.

## Reject

- A unique constraint, row lock, conditional update, or serializable transaction already makes the second run fail or wait.
- Only one run can happen at a time, such as a single worker with a concurrency limit of one.

## Encode

Move the check into the write. Use a unique constraint and handle the conflict, a conditional update such as `UPDATE ... SET used = true WHERE id = ? AND used = false` that checks the affected row count, or an atomic increment. When the logic cannot fit in one statement, use a transaction with a row lock, or a distributed lock that the repository already has.

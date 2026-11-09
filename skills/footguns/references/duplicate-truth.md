# Duplicate truth

## Candidates

A value or type that has a source and a copy, where the copy can drift from the source. Examples are a stored `commentCount` next to the comments table, an order `total` next to its line items, a hand-written type next to the schema it describes, a constant list copied into two packages, and client state that mirrors server state.

## Detect

- Search for stored counts, totals, flags such as `hasChildren`, and denormalized columns. List every path that changes the source.
- Search for types that repeat a schema, a database table, or an API response field by field.
- Search for literal lists, such as roles, plans, and statuses, defined in more than one place.

## Confirm

A path changes the source without updating the copy, or changes the copy alone, and a reader then trusts the stale copy. For example, the bulk delete job removes comments without touching `commentCount`, so the badge shows comments that do not exist. Or someone adds a field to the schema, and the hand-written type omits it.

## Reject

- The copy is derived on read, or a trigger, a generated file, or one function updates it on every write path.
- The copy is a deliberate snapshot, such as the price on a past invoice, and nothing expects it to follow the source.

## Encode

Derive the copy from its source. Compute it on read, infer the type from the schema, or import the one definition. When the copy must be stored for speed, update it in the same transaction as the source, or with a database trigger, and add a check that compares the two.

# Invariants

## Candidates

A rule that must always hold for the code to work, but that nothing checks. For example, an order has one or more items, `endDate` comes after `startDate`, a user belongs to exactly one organization, or a percentage stays between 0 and 100.

## Detect

- Search for non-null assertions, `[0]` on arrays, unchecked `.find()` results, and casts. Each one assumes something.
- Search for comments such as "always", "never", "should not happen", "must", and "assumes".
- Read the code that divides, indexes, or looks up by a value, and ask what that value must satisfy.
- Compare the database schema with how the code uses each column. A nullable column that the code treats as required is a candidate.

## Confirm

A reachable writer can store or pass a value that breaks the rule, and a reader then fails or returns a wrong result. Name the writer and the reader. For example, the admin form allows an empty item list, and the invoice code then reads `items[0].price` and throws.

## Reject

- A type, schema, database constraint, or check at the boundary already enforces the rule on every write path.
- No write path can break the rule, such as a value that only the code itself computes.

## Encode

Enforce the rule at the strongest layer that can hold it, and name that layer:

- **Type.** Make the invalid value unrepresentable, such as a non-empty array type or a union.
- **Schema.** Reject the value where it enters, using the repository's schema library.
- **Database.** Add a `NOT NULL`, `CHECK`, `UNIQUE`, or foreign key constraint when other writers share the table.
- **Constructor.** Make one function the only way to create the value, and have it check the rule.

Add a test only when no layer above can hold the rule.

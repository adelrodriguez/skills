# Primitives

## Candidates

Strings and numbers that mean different things but share one type, so the type checker accepts one where the other belongs. For example, `userId` and `orgId` as `string`, cents and dollars as `number`, seconds and milliseconds, or a raw string and its HTML-escaped form.

## Detect

- List the ID fields in the domain types and database schema, and check whether they share a type.
- Search for functions that take two or more parameters of the same primitive type, such as `transfer(fromId: string, toId: string, amount: number)`.
- Search for unit words in names, such as `Ms`, `Seconds`, `Cents`, `Amount`, and `Price`, and check whether different units mix.

## Confirm

A call site passes one meaning where the other belongs, or could do so with an ordinary edit, and the result is wrong without an error. For example, a caller swaps the two IDs in `addMember(orgId, userId)` and inserts a row that points at the wrong records. A real swap in the code is Confirmed. A swap that only an edit could cause is Plausible.

## Reject

- The values already have branded or distinct types.
- Only one meaning of the primitive exists in the scope.

## Encode

Brand each meaning, using the repository's schema library when it supports brands:

```ts
type UserId = string & { readonly __brand: "UserId" }
type OrgId = string & { readonly __brand: "OrgId" }
```

Create branded values only where the boundary parses them. For units, brand the unit or store one canonical unit, such as integer cents, and convert at the edge.

---
name: footguns
description: Use when the user says "footguns" or asks to find foot guns, implicit state machines, or invariants the code relies on but does not enforce.
---

# Find footguns

Find code that makes the wrong move easy. A footgun is a rule the code relies on but does not encode, so a mistake passes the type checker and review and fails at runtime. Report each footgun with a concrete failure and the encoding that would prevent it. Edit code only when the user asks you to fix footguns, either in the request or after the report.

## Set the scope

Use the lenses and paths the user names. When they name no lenses, use every lens below. When they name no paths, use the whole repository.

For example:

```text
/footguns
/footguns state-machines invariants
/footguns idempotency src/billing
/footguns fix races
```

Read only the reference files for the selected lenses:

| Lens | Covers | Reference |
|---|---|---|
| `state-machines` | Booleans and optional fields that must stay in sync | [State machines](references/state-machines.md) |
| `invariants` | Rules the code relies on but never checks | [Invariants](references/invariants.md) |
| `boundaries` | External input used without parsing, and validation repeated inside the system | [Boundaries](references/boundaries.md) |
| `primitives` | Strings and numbers that mean different things and can be swapped | [Primitives](references/primitives.md) |
| `errors` | Failures signaled by sentinels, flags, or thrown strings | [Errors](references/errors.md) |
| `idempotency` | Commands that change the result when they run twice | [Idempotency](references/idempotency.md) |
| `duplicate-truth` | Stored or hand-written copies that can drift from their source | [Duplicate truth](references/duplicate-truth.md) |
| `conditionals` | Branch chains that grow by one case per feature | [Conditionals](references/conditionals.md) |
| `call-order` | Calls that work only in an order nothing enforces | [Call order](references/call-order.md) |
| `string-contracts` | Keys and names that two places must spell the same way | [String contracts](references/string-contracts.md) |
| `races` | Check-then-act and read-modify-write without a transaction or lock | [Races](references/races.md) |

Read the repository's `AGENTS.md`, `CODING_STANDARDS.md`, and `GLOSSARY.md` when they exist. Note the libraries the code already uses for schemas, errors, state, and transactions, because each proposed encoding must use them.

The step is done when the lenses and paths are listed, the selected references are read, and the repository's primitives for each lens are known.

## Find the candidates

Run each selected lens's detection rules over the scope. When subagents are available, give each lens to its own subagent with the scope, the reference file, and the repository's primitives. Otherwise, run the lenses yourself in the table's order.

Trace each candidate to the code that reads and writes it. A search match alone is not a candidate. Search the whole repository for those readers and writers even when the scope is a path.

The step is done when every selected lens has run over every path in scope.

## Confirm each footgun

Keep a candidate only when you can write its failure scenario: the inputs or sequence of events, the code path they take, and the wrong result. Follow the reference's rules for what confirms and what rejects a candidate.

Mark each kept footgun with one confidence:

- **Confirmed.** You traced the full path from a reachable input to the wrong result.
- **Plausible.** The path exists, but a step depends on runtime state you could not check, such as production data or a deployment setting. Name that step.

Drop a candidate when the code already prevents the failure, such as with a database constraint, a schema, a type, a lock, or a test. Record why you dropped it.

When one piece of code fails under several lenses, merge the findings into one footgun under the lens whose encoding fixes the most. List the other lenses on it.

The step is done when every candidate is kept with a failure scenario or dropped with a reason.

## Rank the footguns

Rank by impact, then by how easy the mistake is to make. Put data loss, money, security, and corrupted state first. Put a footgun that ordinary use triggers above one that needs a rare sequence. Put Confirmed above Plausible at equal rank.

The step is done when every footgun has a rank.

## Return the report

If subagents or another capability were unavailable, say so on the first line and name what you did instead.

State the lenses and paths you checked, and the counts of kept and dropped candidates per lens. Then list the footguns in rank order. Give each one:

- The lens, and any merged lenses.
- The `file:line` of each place involved.
- The rule the code relies on, stated in one sentence.
- The failure scenario.
- The proposed encoding, using the repository's primitives.
- The confidence. For Plausible, the step you could not check.

List the dropped candidates in one short table with their reasons, so the user can disagree.

When a proposed encoding changes a module boundary or public API, say that it needs the `codebase-design` skill first. When the user has not asked for fixes, end with a question that asks which footguns to file with the `issue` skill or to fix, with nothing after it.

## Fix the footguns

Run this step only when the user asks for fixes. Fix the footguns they name, or every kept footgun when they say to fix all of them.

For each footgun, in rank order:

1. Write a test that fails because of the footgun, using the `testing` skill. When the encoding is a type, the failing check can be a type test or a compile error in a test file.
2. Apply the proposed encoding. When it changes a module boundary or public API, use the `codebase-design` skill and wait for the user's agreement first.
3. Run the new test and the affected checks, and commit the test and the fix together.

When a fix fails checks you cannot fix within that footgun, restore it and report the footgun as unfixed with the failure. Report each fixed footgun with its commit and the test that now passes.

The step is done when every footgun the user named is committed with a passing test or reported as unfixed with a reason.

## Check the report

- Every selected lens ran over every path in scope.
- Every kept footgun has a failure scenario, a `file:line`, a one-sentence rule, an encoding, and a confidence.
- Every dropped candidate has a reason.
- Every encoding uses a library or pattern the repository already has, or says that it adds one.
- No code was edited unless the user asked for fixes, and every fix has a test that failed before it.
- The report names any missing capability on its first line, and any closing question comes last.

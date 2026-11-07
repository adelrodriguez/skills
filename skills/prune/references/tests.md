# Tests

## Candidates

Every test in the selected files, including skipped tests, todo tests, and tests that fail at the baseline. The baseline counts tests and records their run time and coverage.

## Detect

The `testing` skill owns the criteria for low-value tests, weak assertions, and testing through the interface. Read each test and the code it tests against those criteria.

When the scope has more than a few dozen test files, split classification by folder among subagents when available. Give each one this reference, the classification step in `../SKILL.md`, and the `testing` skill. Without subagents, classify the folders yourself and name that fallback in the report.

## Prove unused

The groups have these meanings for tests:

- **Remove.** It matches "Delete low-value tests" in the `testing` skill.
- **Strengthen.** It matches "Strengthen weak tests" in that skill.
- **Rewrite.** It tests past the interface, and no test at the interface covers the same behavior.
- **Keep.** It fails when its behavior breaks, and no other test covers the same behavior.

Each duplicate in Remove must name the test that covers it. Temporarily break the behavior and confirm that the covering test fails for that reason. Restore the code and confirm that it passes. Among duplicates, keep the one that tests through the interface with the most exact assertion.

A test of removed code is removable only when the behavior no longer exists. Its name or an uncovered file alone is insufficient evidence.

## Send to Ask

- Tests whose behavior or replacement coverage cannot be confirmed.
- Tests whose failure cannot be checked safely, such as tests that require an unavailable external service.
- Existing failures whose cause is unknown. Failure alone is not a reason to delete a test.

## Remove

Apply the groups in this order:

1. Remove the tests in Remove.
2. Strengthen the tests in Strengthen. Confirm that each fails when its behavior breaks and passes after the code is restored.
3. Rewrite the tests in Rewrite through the interface. Confirm the same way.

Remove the helpers, fixtures, mocks, and snapshots left without any consumer. Every deleted duplicate must retain its named covering test. The final report includes the proof for each duplicate, strengthened test, and rewritten test.

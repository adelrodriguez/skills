---
name: test-pruning
description: Use when the user says "test pruning" or asks to prune or clean up tests.
disable-model-invocation: true
---

# Prune the tests

Clean up a test suite that many people and agents have added to. Delete the tests that do not earn their place, and strengthen the weak ones, without losing coverage of any behavior. The criteria for weak and low-value tests are in the `testing` skill. This skill applies them across a scope.

## Set the scope

Use the folders, files, or modules the user names. When they name none, use the whole test suite.

The step is done when the scope is a list of test files.

## Record the baseline

Run the repository's test command on the scope. When the repository has a coverage command, run it too.

Record the number of tests, the run time, and the coverage. When a test already fails, record it and classify it like the others. Do not fix it as part of the baseline.

The step is done when you have recorded the test count, the run time, the coverage when available, and every failing test.

## Classify each test

Read each test in the scope, and the code it tests. Put each test in one of these groups:

- **Delete.** It matches a case in "Delete low-value tests" in the `testing` skill.
- **Strengthen.** It matches a sign in "Strengthen weak tests" in the `testing` skill.
- **Rewrite.** It tests past the interface, as "Test through the interface" in the `testing` skill describes, and no test at the interface covers the same behavior.
- **Keep.** It fails when the behavior it covers breaks, and no other test covers the same behavior.

For each test in the delete group that another test duplicates, name the test that covers it. Confirm the coverage by breaking the behavior temporarily and checking that the covering test fails. Restore the code afterward.

When several tests duplicate each other, keep the one that tests through the interface with the most exact assertion.

When the scope has more than a few dozen test files, split it by folder. Classify each folder in a separate subagent, and give each one this step and the `testing` skill.

The step is done when every test is in exactly one group, and every duplicate in the delete group names the test that covers it.

## Show the dry run

Show one short bullet list per group, with the test's file and name and a reason of a few words. Leave out the keep group, and give only its count.

When fewer than five files will change, continue without waiting. Otherwise, wait for the user's agreement.

The step is done when fewer than five files will change, or when the user agrees.

## Prune the suite

Apply the groups in this order, and keep each group in its own commit, so the user can review or revert each one alone:

1. Delete the tests in the delete group.
2. Strengthen the tests in the strengthen group. Confirm that each one fails when you break the behavior, as the `testing` skill describes.
3. Rewrite the tests in the rewrite group through the interface. Confirm the same way.

After the deletions, delete the helpers, fixtures, mocks, and snapshot files that no remaining test uses.

The step is done when every group is applied, and no helper, fixture, mock, or snapshot file in the scope is unused.

## Compare with the baseline

Run the test command and the coverage command again.

Explain every drop in coverage. A drop is acceptable only when it comes from a test whose code no longer exists, or from a test of the framework or a library. Otherwise, restore the test, or add a test at the interface that covers the lost lines.

The step is done when the suite passes and every drop in coverage has a reason.

## Check the pruning

- Every test in the scope was classified into exactly one group.
- Every deleted duplicate names the test that covers it, and that test failed when the behavior broke.
- Every strengthened and rewritten test failed when the behavior broke, and passed after the code was restored.
- No unused helper, fixture, mock, or snapshot file remains in the scope.
- Each group is in its own commit.
- The suite passes, and every drop in coverage has a reason.

## Return the result

Return a table with the test count, the run time, and the coverage, before and after. Then list the deleted, strengthened, and rewritten tests, one bullet each, with the reason. End with the tests that failed at the baseline, and whether each one still fails.

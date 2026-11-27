---
name: test-slop
description: Finds tests that prove nothing - no assertions, assertions that cannot fail, tests of a mock instead of the code, swallowed failures, duplicates - and proves each case by breaking the code and showing the test still passes. Reports by default; strengthens or removes them on request. Use when the user asks to review, audit or clean up tests, asks whether tests are any good, mentions fake, weak or useless tests, or types /test-slop or /anti-slopware tests.
license: MIT
metadata:
  version: "0.1.0"
---

# test-slop

A test is worth keeping only if some real bug would make it fail. A suite full of tests that always pass is worse than no suite, because people trust it.

## 1. Read the request

| Argument | Meaning | Default |
|---|---|---|
| `report` | List weak tests with proof. Change nothing. | on |
| `fix` | Strengthen or remove them, after showing the list | off |
| a path | Test file or folder | test files in the current changes |

Never change the code under test. This skill edits test files only.

## 2. Record a baseline

Run the suite. Note the command, the number of tests, and any that already fail or are skipped.

## 3. Find suspects

For each test, ask: **which bug in the code would make this fail?** If you cannot name one, it is a suspect.

- **No assertion**: the test calls the code and checks nothing.
- **Cannot fail**: `assertTrue(True)`, comparing a value with itself, asserting a literal, `is not None` on something that is never `None`, `len(x) >= 0`.
- **Tests the mock**: the function under test is itself patched, or the only assertions are on values the test told a mock to return.
- **Swallows failure**: assertions or the call inside `try`/`except` that passes either way; expecting any `Exception` where a specific one is meant.
- **Never runs**: assertions behind a condition that is not met, or inside a loop over nothing.
- **Duplicate**: same inputs and same checks as another test.
- **Name promises more than it checks**: `test_rejects_invalid_input` that only passes valid input.
- **Disabled**: skipped or expected-to-fail with no reason; assertions commented out.

## 4. Prove it

Do not rely on reading alone. For each suspect:

1. Break the code in the one way the test's name says it guards against: flip a comparison, change a constant, delete a check, return early.
2. Run that one test.
3. Restore the code at once.

Still passes: the test proves nothing, and you have the evidence. Fails: it is a real test; drop it from the list.

Duplicates are the exception. A duplicate fails when its twin does, so identify it by comparing the two tests, not by breaking the code.

Work on a temporary copy of the code where you can. Whichever way you do it, confirm at the end that the code under test is byte-for-byte what it was at the start.

## 5. Not slop

- A test that asserts by expecting a specific exception.
- An assertion on a mock at a real boundary (email, payment, network, clock). Calling the outside world correctly is the behaviour.
- Tests that look alike but use different inputs, such as each side of a boundary.
- Table-driven and parametrised tests, property tests, snapshot tests.
- Tests that assert through a helper function.
- A smoke test of code whose result cannot be checked directly (a whole program starting, a page rendering), where a comment or docstring says it only checks that nothing raises. Keep it and label it weak. This does not cover a test that calls a function with a checkable return value and asserts nothing, whatever its name: that is "No assertion". Strengthen it, or remove it if another test already checks the same call.

Leave these exactly as they are.

## 6. Fix (only with `fix`, after showing the list)

In this order:

1. **Strengthen**: replace the empty check with a real one. Take the expected value from the documentation, the docstring, the function's contract or the issue, not from copying the implementation's formula into the test.
2. **Remove**: only exact duplicates and tests that cannot be made meaningful.

Rules:

- Keep each test's intent. A test named for an error case must test that error case.
- If a strengthened test fails, the code may have a bug. Stop on that test and report it. Do not adjust the expected value to match the code, and do not change the code.
- If the intended behaviour is unclear, ask. Do not guess an expected value.
- Do not add tests for things the suite never covered. Say what is uncovered in the report.

## 7. Verify

- The suite passes, except tests reported as exposing a possible bug.
- Each strengthened test now fails under the break from step 4.
- The code under test is unchanged.

## 8. Report

```
test-slop: <tests examined> examined, <n> prove nothing

Proves nothing: <n>
  - <test>: <kind>. Still passed with <the break>. <strengthened | removed | reported>
Possible bugs exposed: <n>
  - <test>: expected <x> from <source>, code gives <y>
Left alone: <n valid tests>
Not covered by any test: <behaviour>
Checks: <command> <before> -> <after>
```

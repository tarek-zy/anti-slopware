---
name: test-slop
description: Finds tests that prove nothing (no assertions, assertions that cannot fail, tests of a mock or of a copy instead of the code, tests the runner never runs, swallowed failures, duplicates) and tests that a change weakened, skipped, deleted or rewrote so a failure would go away. Proves each case by running it - breaks the code and shows the test still passes, runs the old test against the new code, runs a fix's test against the code before the fix. Reports by default; strengthens, restores or removes tests on request. Use when the user asks to review, audit or clean up tests, asks whether tests are any good or whether a fix is really tested, suspects tests were changed to make them pass, mentions fake, weak or useless tests, or types /test-slop or /anti-slopware tests.
license: MIT
metadata:
  version: "0.2.0"
---

# test-slop

A test is worth keeping only if some real bug would make it fail. A suite full of tests that always pass is worse than no suite, because people trust it.

A green suite is evidence only if the tests run, reach the code, and were not bent to fit it. This skill checks all three by running things, not by reading alone.

## 1. Read the request

| Argument | Meaning | Default |
|---|---|---|
| `report` | List weak and bent tests with proof. Change nothing. | on |
| `fix` | Restore, strengthen or remove them, after showing the list | off |
| a path | Test file or folder | test files in the current changes |

Never change the code under test. This skill edits test files only. It reports changes to the test runner's and CI's configuration and leaves them to the user.

## 2. Record a baseline

Run the suite. Note the command, the number of tests, and any that already fail or are skipped.

Check that the runner runs what the files contain: compare the tests it collected with the test functions written in the files. A test in a file that the runner does not list is a suspect.

Find the base: the commit the current change started from. That is the merge base with the default branch, or the last commit when the change is uncommitted. With no version control there is no base: skip step 5 and say so under "Not checked".

## 3. Find suspects

For each test, ask: **which bug in the code would make this fail?** If you cannot name one, it is a suspect.

- **No assertion**: the test calls the code and checks nothing.
- **Cannot fail**: `assertTrue(True)`, comparing a value with itself, asserting a literal, `is not None` on something that is never `None`, `len(x) >= 0`.
- **Tests the mock**: the function under test is itself patched, or the only assertions are on values the test told a mock to return.
- **Never reaches the code**: the test checks a copy of the logic written in the test file, a helper or a stand-in module, and never calls the real function.
- **Swallows failure**: assertions or the call inside `try`/`except` that passes either way; expecting any `Exception` where a specific one is meant.
- **Never runs**: assertions behind a condition that is not met, or inside a loop over nothing.
- **Not collected**: the runner never runs it. A name without the runner's prefix, a second test with the same name replacing the first, a file outside the configured paths, a test deselected or ignored in configuration.
- **Duplicate**: same inputs and same checks as another test.
- **Name promises more than it checks**: `test_rejects_invalid_input` that only passes valid input.
- **Agrees with the bug**: the expected value repeats the implementation's formula, or contradicts the documentation, the docstring or the issue the test names.
- **Disabled**: skipped or expected-to-fail with no reason; assertions commented out.

## 4. Prove it

Do not rely on reading alone. For each suspect:

1. Break the code in the one way the test's name says it guards against: flip a comparison, change a constant, delete a check, return early.
2. Run that one test.
3. Restore the code at once.

Still passes: the test proves nothing, and you have the evidence. Fails: it is a real test; drop it from the list.

Duplicates are the exception. A duplicate fails when its twin does, so identify it by comparing the two tests, not by breaking the code.

Work on a temporary copy of the code where you can. Whichever way you do it, confirm at the end that the code under test is byte-for-byte what it was at the start.

## 5. Check what the change did to its tests

Tests are the evidence that a change works. When the same change edits the evidence, check the edit. Compare every test file, test configuration file and CI file the change touches with the base, and list:

- **Weakened**: an assertion deleted or loosened (exact to approximate, equal to greater-than or truthy, a wider tolerance, a specific exception to a general one), an expected value changed, a failing case dropped from a table.
- **Disabled**: a test deleted, skipped, marked expected-to-fail, commented out, renamed so the runner no longer finds it, replaced by a later test of the same name, or excluded in the runner's or CI's configuration.
- **Detached**: a mock, patch or fixture added that replaces the code the test used to run.
- **Regenerated**: a snapshot or golden file rewritten.

Prove each one: run the test as it was at the base against the code as it is now. Use a temporary copy of the project with that test swapped for its base version, and bypass any new exclusion.

- **The old test passes**: the edit hid nothing. It is a refactor. Drop it from the list.
- **The old test fails**: the edit hid a failure. Decide which side is wrong. Look for a statement that the behaviour was meant to change: the user's request, the issue, the commit message, the pull request description, the changelog, the documentation. If the change says so, the test edit is right; leave it. If nothing says so, or the documentation still describes the old behaviour, the test was **changed to pass**: the code broke and the test was bent to fit.
- **Cannot tell**: ask. In an unattended run, report it as a question and change nothing.

**A fix needs a test that fails without it.** When the change says it fixes a bug and adds or edits a test for it, run that test against the code at the base. It must fail there, for the reason the bug report gives. If it passes on the unfixed code, it does not test the fix. If the change adds no test that fails at the base, say the fix is untested.

## 6. Not slop

- A test that asserts by expecting a specific exception.
- An assertion on a mock at a real boundary (email, payment, network, clock). Calling the outside world correctly is the behaviour.
- Tests that look alike but use different inputs, such as each side of a boundary.
- Table-driven and parametrised tests, property tests, snapshot tests.
- Tests that assert through a helper function.
- A smoke test of code whose result cannot be checked directly (a whole program starting, a page rendering), where a comment or docstring says it only checks that nothing raises. Keep it and label it weak. This does not cover a test that calls a function with a checkable return value and asserts nothing, whatever its name: that is "No assertion". Strengthen it, or remove it if another test already checks the same call.
- A test edited to follow a behaviour change that the request, the issue, the commit message, the changelog or the documentation states.
- A test renamed, moved, merged into a table or rewritten, whose base version still passes against the new code.
- A test deleted together with the code it tested, when the removal is stated.
- A skip or expected failure with a reason that can be checked: a platform, an optional dependency, a named open issue.
- An approximate comparison on a floating-point result that was never exact.

Leave these exactly as they are.

## 7. Fix (only with `fix`, after showing the list)

In this order:

1. **Restore** tests that were changed to pass: bring back the base version of the assertion, the case, the test or its name, and keep unrelated edits to the same file. The restored test will fail. That is the point: list it under "Possible bugs exposed".
2. **Strengthen**: replace the empty check with a real one. Take the expected value from the documentation, the docstring, the function's contract or the issue, not from copying the implementation's formula into the test. For a test that does not test its fix, take the failing case from the bug report.
3. **Remove**: only exact duplicates and tests that cannot be made meaningful.

Rules:

- Keep each test's intent. A test named for an error case must test that error case.
- If a restored or strengthened test fails, the code may have a bug. Stop on that test and report it. Do not adjust the expected value to match the code, and do not change the code.
- If the intended behaviour is unclear, ask. Do not guess an expected value.
- Do not add tests for things the suite never covered. Say what is uncovered in the report.
- Do not edit the runner's or CI's configuration. Report each exclusion and what it hides.

## 8. Verify

- The suite passes, except tests reported as exposing a possible bug.
- Each strengthened test now fails under the break from step 4.
- Each restored test is collected and runs.
- The code under test is unchanged, and no temporary copy is left behind.

## 9. Report

```
test-slop: <tests examined> examined, <n> prove nothing, <n> changed to pass

Proves nothing: <n>
  - <test>: <kind>. Still passed with <the break>. <strengthened | removed | reported>
Changed to pass: <n>
  - <test>: <weakened | disabled | detached | regenerated>. Was <old check>, now <new check>. The old test fails on the current code: <message>. <restored | reported | asked>
Does not test its fix: <n>
  - <test>: passes on the code before the fix. <strengthened | reported>
Possible bugs exposed: <n>
  - <test>: expected <x> from <source>, code gives <y>
Left alone: <n valid tests>, <n test edits that follow a stated change>
Not covered by any test: <behaviour>
Not checked: <what could not be run, and why>
Checks: <command> <before> -> <after>
```

Leave out sections with nothing in them.

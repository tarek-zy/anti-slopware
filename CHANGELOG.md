# Changelog

## 0.6.0

- `test-slop` skill: finds tests that prove nothing and proves each case by breaking the code. Reports by default; `fix` strengthens or removes them. Never edits the code under test.

## 0.5.0

- `slim-pr` skill: writes or trims a pull request description to what, why, how to test and risks; drops unsupported claims; keeps breaking changes; flags noise in the diff.

## 0.4.1

From the first independent test run:

- Test files are no longer edited in the same run as the code they test.
- Code with no tests is compared before and after instead of blocking the whole run.
- The report counts lines in changed files only.
- README section on how the plugin keeps changes reviewable by humans.

## 0.4.0

- Language checks for Python, JavaScript and TypeScript, Java, C#, C++, Go, Rust, PHP, and Dart and Flutter, alongside C.
- Shared method for every language: build first, run installed tools, read for known bugs, report findings separately.
- Checks for mistakes AI-written code makes in any language.
- Each language lists what is not slop there, so cleanup leaves it alone.

## 0.3.0

- Two named modes: `guard` (prevents slop while code is written, stays on for the session, self-checks before finishing) and `fix` (cleans existing code).
- `all` runs fix mode across a whole project in reviewable batches.
- `write` still works as an older name for `guard`.

## 0.2.0

- `hard` now also covers unclear and disorganised code: misleading private names, unnamed constants, functions that do several jobs, scattered related code, mixed patterns.
- The skill states its goal as readable, editable, organised code. Fewer lines is a side effect.

## 0.1.0

- `anti-slopware` skill: levels `easy`, `medium`, `hard`; refine, `write` and `report` modes.
- C checks.
- Python example with tests run against every level; C example for AddressSanitizer.

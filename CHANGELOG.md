# Changelog

## 0.11.0

- `split-pr` skill: plans how to break one oversized branch into small pull requests, one purpose each, with dependencies, merge order and a drop list. Plan only; it does not change the branch.
- The JavaScript and Go language checks were tested on projects with planted bugs and traps. Both passed with no change needed.

## 0.10.1

From a harder guard mode test (a vague request in a messier project):

- Guard mode now says to leave existing shared code alone and report weaknesses as findings.
- It says how to read vague words such as "robust" without adding machinery.
- It cleans up caches and scratch files its own checks create.

## 0.10.0

- `review-map` skill: a reading guide for the human reviewing a change. Orders the files, gives each careful file one question, marks what can be skimmed and what does not belong. 250 words at most, no verdict.

## 0.9.0

- `junk-sweep` skill: finds session leftovers and regenerable caches, lists them with sizes, and removes them only after approval. Tracked files, referenced files, secrets, user data and editor settings are never candidates.
- All six v1 skills are now shipped.

## 0.8.0

- `error-slop` skill: finds handlers that hide failures and separates them from deliberate handling such as bounded retries, boundary handlers and documented fallbacks. Reports by default; `fix` applies the smallest change.

## 0.7.0

- `dep-check` skill: finds unused and undeclared dependencies and names that may not exist. Adds a package only when a lock file, the installed environment or the registry proves it exists. Edits manifests only.

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

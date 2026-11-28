# Changelog

## 0.15.0

- `test-slop` now checks what a change did to its own tests. It lists tests that were weakened, skipped, deleted, renamed out of the run, shadowed, detached with a mock or excluded in configuration, and runs each old test against the new code. A test edit that follows a stated behaviour change is left alone. A test changed to pass is restored with `fix`, and the failure it hid is reported as a possible bug.
- A fix must come with a test that fails without it: the fix's test is run against the code before the fix.
- New suspects: tests that never reach the code, tests the runner does not collect, expected values that agree with the bug.
- It reports exclusions in the runner's and CI's configuration and does not edit them.
- Tested by a fresh agent on a Python project where a branch broke the code and bent the tests to fit. It passed with no change to the draft.

## 0.14.0

- Shell language check for `sh`, Bash and zsh scripts: unquoted expansions, deletes and moves through an empty variable, hidden failures, Bash syntax under `sh`, variables lost in a subshell, `read` pitfalls, injection and temporary files. It lists what is not slop in shell, and says to run a script only inside a throwaway directory.
- Tested by a fresh agent on a shell project with planted bugs and traps. It passed with no change to the draft.

## 0.13.3

- Wording only. The stated goal is now code quality that keeps a project easy to maintain and to improve, for people and for agents. Readable code and small, checkable changes are how it gets there, not the goal. Changed in the README, the plugin and marketplace descriptions, and the description and opening of the `anti-slopware` skill. No rule changed.
- The C language check was tested on a project with planted bugs and traps, before and after this change. It passed both times with no change needed.

## 0.13.2

- `junk-sweep` asks the user about every item it was unsure of, one clear question each, with keep as the default. It deletes one only on a clear yes for that item. In an unattended run it deletes none of them and puts the questions in the report.

## 0.13.1

- `junk-sweep` now tells logs and copies apart by evidence, not by name. Throwaway logs (debug output, package-manager dumps, captured test runs, empty files) are candidates. Application, audit, transaction, deploy, crash and rotated logs never are, and are listed as kept with a flag on any that contain errors.
- Backups are never candidates. A merge or editor leftover is a candidate only when its content is identical to the real file or a committed version.
- A tool cache inside a dependency folder is a candidate; the folder around it is not.
- Log contents are never copied into the report.

## 0.13.0

- `code-docs` skill: documents a codebase in layers (file map, how it fits together, logic, reference, comments). Learns the project's own documentation system first and extends it. Moves long comment blocks into doc pages and leaves a pointer. Changes no code.
- Cleanup no longer deletes comments at any level. Comment work belongs to `code-docs`. Commented-out code is still removed.
- Guard mode documents new code in the project's style.
- The example's `medium` and `hard` versions keep their comments (61 and 55 lines).

## 0.12.0

- `organize` skill: improves project structure without changing behaviour. Plans first; then one pure move at a time, with old import paths kept working and tests left unchanged.

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

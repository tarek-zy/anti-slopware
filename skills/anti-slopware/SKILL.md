---
name: anti-slopware
description: Improves code quality without changing behaviour. Removes duplicated and useless code, simplifies verbose code, makes code easier to read, edit and navigate, and keeps every change small and explained so humans can review it. Three levels - easy (duplication only), medium (plus dead and useless code), hard (plus simplifying, clear naming and organisation). Includes bug checks for Python, JavaScript, TypeScript, Java, C#, C, C++, Go, Rust, PHP and Dart. Use when the user asks to clean up, deslop, dedupe, simplify, tidy or reorganise code, to make code more readable or maintainable, to remove dead code or AI slop, or types /anti-slopware. Two modes - guard (prevents slop in code as it is written; use when the user asks for guard mode, slop-free code, or to keep new code clean) and fix (cleans existing code, from the current change to a whole project).
license: MIT
metadata:
  version: "0.10.0"
---

# anti-slopware

Make code easier to read, easier to change and easier to find your way around, without changing what it does.

Fewer lines is a side effect, not the goal. A change that makes code shorter but harder to follow is not made. A change that adds a line to make code clearer (a named constant, a well-named helper) is.

Every change must be provably safe or it is not made.

## 1. Read the request

If the first argument names another skill in this plugin, use that skill instead and pass the rest of the arguments to it:

| Argument | Skill |
|---|---|
| `pr` | `slim-pr` |
| `map` | `review-map` |
| `tests` | `test-slop` |
| `deps` | `dep-check` |
| `errors` | `error-slop` |
| `junk` | `junk-sweep` |

Otherwise continue here.

Two modes. **Guard** stops slop from being written. **Fix** removes it from code that exists. They are independent: fix can run while guard is on.

Arguments, in any order, all optional:

| Argument | Meaning | Default |
|---|---|---|
| `easy`, `medium`, `hard` | Level (see below) | `medium` |
| `fix` | Fix mode: clean code that already exists | on |
| `guard` | Guard mode: prevent slop in every piece of code you write this session | off |
| `all` | Fix mode across the whole project | off |
| `report` | Find and list, change nothing | off |
| a path | File or folder for fix mode to work on | current uncommitted and branch changes |

Levels are cumulative:

- **easy**: duplicated code only.
- **medium**: easy + useless code.
- **hard**: medium + verbose, unclear and disorganised code.

Exact definitions, with what counts and what does not, are in [references/levels.md](references/levels.md). Read it before finding anything.

If `guard` is given (or `write`, its older name), follow [references/guard-mode.md](references/guard-mode.md) and skip steps 2 to 7.

Steps 2 to 7 are fix mode.

## 2. Set the scope

- No path given: the files changed on this branch (`git diff` against the base branch, plus uncommitted changes). Only touch lines in, or directly entangled with, those changes.
- Path given: that file or folder.
- `all` given: the whole project, one folder or module at a time. Finish steps 3 to 7 for one before starting the next, so each batch is small enough to review. At `medium` and `hard`, get approval per batch. Stop and ask if a batch would change more than about 300 lines.
- Never edit test files in the same run as the code they test. They are the safety net, and a net that changes with the code proves nothing. Clean tests only when the path given is a test file or folder.
- Never edit: generated files, vendored or third-party code, lock files, migrations, snapshots, anything matched by `.gitignore`.

## 3. Record a baseline

Find the project's own checks (test command, linter, type-checker, compiler warnings) from its config files and docs. Run them and record the result before changing anything.

- Checks already failing: note which. A change may not add new failures.
- Some code in scope has no test: before changing it, record its outputs for a spread of inputs (normal, edge and invalid) with a throwaway script kept outside the project. Compare after the change, then delete the script. List that code under "Not verified" as checked by comparison only.
- Code that cannot be exercised that way (it needs a network, a database or a device): `report` only for that code. Say why, and offer to write tests that pin current behaviour first.

## 4. Find

Read the code in scope and every caller of anything you might change. List candidates by category from `references/levels.md`, each with file, lines and a one-line reason.

Before listing something as unused, search the whole repository for it, including strings, config, templates and build files. Code reached by reflection, registration, plugin entry points, serialisation or public export is not unused.

Then run the language checks: read [references/languages.md](references/languages.md) and the file it names for each language in scope. They report bugs as findings, and list what is not slop in that language.

## 5. Apply

| Level | Behaviour |
|---|---|
| `easy` | Apply directly. |
| `medium`, `hard` | Show the candidate list first. Apply after the user approves. |
| `report` | Never apply. |

Make one kind of change at a time, smallest first, so a reviewer can accept one kind and reject another. Match the project's existing style and naming.

A cleanup a human cannot review is not finished. If the result is too large to read in one sitting, split it and say how.

## 6. Verify

After each group of changes, rerun the baseline checks.

- Anything newly failing: revert that change, keep the rest, and list it under "Skipped".
- Never edit a test's assertions to make it pass.

## 7. Report

End with only this:

```
anti-slopware <level>: <files changed> files, <lines before> -> <lines after> lines (changed files only)

Removed duplication: <n>
  - <file>:<lines> <what, in a few words>
Removed useless code: <n>
Simplified: <n>
Clarified and organised: <n>
Skipped: <n>
  - <file>:<lines> <why>
Checks: <command> <result before> -> <result after>
Not verified: <anything no check covered>
```

Leave out sections with nothing in them.

## Hard limits

Never, at any level:

- Change behaviour: outputs, side effects, error types and messages, ordering, numeric results, performance class.
- Change or remove a public API: exported names, signatures, CLI flags, config keys, wire formats.
- Rewrite working code to suit your taste. The project's style wins.
- Trade clarity for fewer lines: no nested ternaries, no dense one-liners, no clever tricks.
- Touch code outside the scope, even if it is worse.
- Claim the code is correct, bug-free or memory safe. Say what was checked and what was not.

A real bug found along the way is a finding, not a cleanup. Report it separately and fix it only if the user asks, because fixing it changes behaviour.

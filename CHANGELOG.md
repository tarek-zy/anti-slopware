# Changelog

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

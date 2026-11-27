# Roadmap

## v1 (in progress)

Shipped one skill at a time, each with examples and tests.

- [x] `anti-slopware`: guard and fix modes; duplicated, useless, verbose, unclear and disorganised code
- [x] Language checks: Python, JavaScript and TypeScript, Java, C#, C, C++, Go, Rust, PHP, Dart and Flutter
- [ ] `slim-pr`: PR descriptions as what / why / how to test / risks; flags noise in the diff
- [ ] `test-slop`: assertions that cannot fail, over-mocking, copy-pasted cases
- [ ] `dep-check`: unused dependencies, imports of packages that do not exist
- [ ] `error-slop`: swallowed exceptions, catch-everything blocks
- [ ] `junk-sweep`: leftover screenshots, temp files and regenerable build caches; lists first, deletes after approval

## v1.1

- Hook that checks each edit as code is written
- Language checks: Kotlin, Swift, Ruby, SQL, shell scripts
- A test set for each language, with planted bugs and traps, scored automatically

## v1.2

- `split-pr`: break one large change into small reviewable PRs
- `review-map`: a reading guide for the reviewer

## v1.3

- `clean-commits`: tidy commit messages and group fix-up commits
- `slop-report`: audit only
- `mem-safe`: the C checks as their own skill

## Later

- Plugin formats for other agents
- A GitHub Action that runs the checks on pull requests

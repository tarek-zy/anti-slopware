# Roadmap

## v1 (in progress)

Shipped one skill at a time, each with examples and tests.

- [x] `anti-slopware`: duplicated, useless, verbose, unclear and disorganised code; C checks
- [ ] `slim-pr`: PR descriptions as what / why / how to test / risks; flags noise in the diff
- [ ] `test-slop`: assertions that cannot fail, over-mocking, copy-pasted cases
- [ ] `dep-check`: unused dependencies, imports of packages that do not exist
- [ ] `error-slop`: swallowed exceptions, catch-everything blocks
- [ ] `junk-sweep`: leftover screenshots, temp files and regenerable build caches; lists first, deletes after approval

## v1.1

- Hook that checks each edit as code is written
- Language checks: Python, JavaScript/TypeScript, Dart/Flutter

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

# Roadmap

## v1 (shipped)

Shipped one skill at a time, each with examples and tests.

- [x] `anti-slopware`: guard and fix modes; duplicated, useless, verbose, unclear and disorganised code
- [x] Language checks: Python, JavaScript and TypeScript, Java, C#, C, C++, Go, Rust, PHP, Dart and Flutter, shell scripts, SQL, Ruby
- [x] `organize`: project structure; splits do-everything files, breaks up dumping grounds, removes circular dependencies, one pure move at a time
- [x] `code-docs`: layered documentation that adapts to the project's own system; organises comments instead of deleting them
- [x] `slim-pr`: PR descriptions as what / why / how to test / risks; flags noise in the diff
- [x] `test-slop`: assertions that cannot fail, over-mocking, copy-pasted cases, tests weakened, skipped or deleted to hide a failure, fixes with no test that fails without them
- [x] `dep-check`: unused dependencies, imports of packages that do not exist
- [x] `error-slop`: swallowed exceptions, catch-everything blocks
- [x] `review-map`: a reading guide for the reviewer
- [x] `split-pr`: plans how to break one large change into small pull requests
- [x] `junk-sweep`: leftover screenshots, temp files and regenerable build caches; lists first, deletes after approval

## v1.1

- Hook that checks each edit as code is written
- Language checks: Kotlin, Swift
- A test set for each language, with planted bugs and traps, scored automatically


## v1.2

- `clean-commits`: tidy commit messages and group fix-up commits
- `slop-report`: audit only
- `mem-safe`: the C checks as their own skill

## Later

- Plugin formats for other agents
- A GitHub Action that runs the checks on pull requests

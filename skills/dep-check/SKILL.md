---
name: dep-check
description: Checks a project's dependencies against what the code really uses - finds declared packages nothing uses, imports of packages that are not declared, and names that may not exist at all (AI-invented packages), and never adds a package without evidence that it exists. Reports by default; edits the manifest on request. Use when the user asks to check, audit, prune or clean up dependencies, requirements or packages, asks about unused or missing dependencies or hallucinated packages, or types /dep-check or /anti-slopware deps.
license: MIT
metadata:
  version: "0.1.0"
---

# dep-check

Every dependency is code you did not write, running with your permissions. Keep the list equal to what the project uses: nothing extra, nothing missing, nothing invented.

## 1. Read the request

| Argument | Meaning | Default |
|---|---|---|
| `report` | List findings. Change nothing. | on |
| `fix` | Edit the manifest, after showing the list | off |
| a path | Project or package folder | the repository root |

This skill edits dependency manifests only. It never edits source code, never installs, upgrades or removes installed packages, and never rewrites a lock file.

## 2. Gather

- **Declared**: every manifest (`requirements*.txt`, `pyproject.toml`, `setup.cfg`, `package.json`, `go.mod`, `Cargo.toml`, `pubspec.yaml`, `composer.json`, `Gemfile`, `pom.xml`, `build.gradle`) and its lock file.
- **Imported**: every import in source and tests.
- **Used without an import**: commands in scripts, `Makefile`, `Procfile`, `Dockerfile` and CI files; plugins and presets named in tool configuration; entry points; connection strings that select a driver.

Standard-library modules are not dependencies.

## 3. Use tools first

Run what is installed and confirm each hit by reading, because these tools misjudge the cases in step 6.

| Ecosystem | Tools |
|---|---|
| Python | `deptry .`, `pip-check-reqs` |
| JavaScript, TypeScript | `knip`, `depcheck` |
| Go | `go mod tidy -diff` (Go 1.23+), `go mod why <module>` |
| Rust | `cargo machete`, `cargo udeps` |
| PHP | `composer-unused` |
| Dart, Flutter | `dart pub deps`, the analyzer's `depend_on_referenced_packages` lint |

## 4. Classify

- **Unused**: declared, never imported, and not used by any command, configuration or connection string.
- **Missing**: imported but not declared. It works today only because another package happens to pull it in, or it is installed on this machine.
- **Misplaced**: a test or build tool among runtime dependencies, or the reverse.
- **Overlapping**: two packages doing one job. Report it as a question, not a fault.

## 5. Does the package exist?

AI-written code sometimes imports packages that were never published, and attackers register those names. So before a name is added to a manifest, there must be evidence that it exists.

Check every **missing** package, and every declared package that is new in the current change. Long-standing declared packages are not checked.

Evidence, in this order:

1. An entry in the lock file.
2. It is installed in the project's environment.
3. A lookup of the exact name in the ecosystem's registry, when the network is available. If it exists, check it is the package the code means and not a look-alike of a well-known one.

None of these: the answer is "could not verify". Your own memory of a package name is not evidence; that is how invented names get in. Never install a package to find out whether it exists.

## 6. Not unused

- The import name differs from the package name: `PyYAML` is `yaml`, `python-dateutil` is `dateutil`, `Pillow` is `PIL`, `beautifulsoup4` is `bs4`, `scikit-learn` is `sklearn`.
- Plugins and presets a tool loads by name: pytest plugins, linter plugins, Babel presets, webpack loaders.
- Command-line tools called from scripts, `Procfile`, `Dockerfile` or CI: servers, migration tools, formatters.
- Drivers selected by a connection string or configuration, such as a database driver named in a URL.
- Optional imports inside `try`/`except ImportError`.
- Type stubs and `@types/*` packages.
- Peer dependencies, and packages loaded through entry points or dynamic imports.

## 7. Fix (only with `fix`, after showing the list)

- **Unused**: remove the line from the manifest.
- **Missing, and it exists**: add it, with the version from the lock file or the installed version.
- **Missing, could not verify**: do not add it. Report it and tell the user to check the registry.
- **Missing, not in the registry**: do not add it. The import is a bug in the code. Report the file and line; do not edit the code.
- **Misplaced** and **overlapping**: report only, unless the user asks.

Do not run an install. Tell the user the command that refreshes the environment and the lock file.

## 8. Verify

- The manifest still parses.
- Every import in the code is either declared, standard library, or listed in the report.
- Run the project's checks if its dependencies are installed. If they are not, say the checks did not run.

## 9. Report

```
dep-check: <declared> declared, <imported> imported

Unused: <n>
  - <package>: no import, command or configuration uses it. <removed | reported>
Missing: <n>
  - <package>: imported in <file>:<line>. Exists: <yes, lock file | yes, installed | yes, registry | no, not in the registry | could not verify>. <added <version> | not added>
Misplaced: <n>
Overlapping: <n>
Kept (looks unused, is not): <package>: <why>
Checks: <what ran, or why it did not>
Next: <command to refresh the environment and lock file>
```

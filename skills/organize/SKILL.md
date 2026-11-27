---
name: organize
description: Improves how a codebase is organised without changing what it does - splits files that do several unrelated jobs, moves code to where a reader would look for it, breaks up utils dumping grounds, removes circular dependencies and stale duplicate modules, and makes the layout consistent. Plans first, then makes one pure move at a time, keeping every existing import path working. Use when the user asks to organise, restructure, reorganise or tidy a project's structure, files, folders or modules, says a file is too big or code is hard to find, or types /organize or /anti-slopware organize.
license: MIT
metadata:
  version: "0.1.0"
---

# organize

Good structure means a reader can guess where something lives, and a change to one feature touches one place. AI-written code drifts away from that: each new piece lands in whichever file was open, and `utils` collects everything else.

Moving code is risky and makes large diffs, so this skill plans first, moves in small pure steps, and keeps old paths working.

## 1. Read the request

| Argument | Meaning | Default |
|---|---|---|
| `report` | Write the plan. Change nothing. | on |
| `apply` | Carry out the plan, after showing it | off |
| a path | Folder or package to organise | the project |

## 2. Understand the project first

Before judging anything, learn its conventions: how the existing folders are divided (by feature, by layer, by type), where tests live, what the framework requires, what is public. Read the README and any architecture notes. **The project's own structure is the standard.** Extend the pattern it already has. Do not bring in a different one.

Record a baseline: run the build, tests, linter and type-checker.

## 3. Find

- **A file doing several unrelated jobs**: data model, parsing, formatting and a command-line entry point in one file. The test is unrelated reasons to change, not length.
- **A dumping ground**: `utils`, `helpers`, `common`, `misc` holding unrelated things. Each belongs with its topic or its only user.
- **Code in the wrong place**: a helper used by one module but living in another; presentation code in the data layer; a constant defined far from its only use.
- **Circular dependencies**, and the tricks that hide them: imports inside functions, late imports at the bottom of a file. Usually something shared needs a home both sides can depend on.
- **Dependencies pointing the wrong way**: low-level code importing high-level code.
- **Stale duplicates**: `thing_old`, `thing2`, `thing_new`, `thing_backup`, kept beside the real one and referenced by nothing. Remove one only when the project is under version control, so it can be recovered. Otherwise list it and leave it.
- **Inconsistent layout**: the same kind of thing in two places or under two naming schemes.
- **Names that mislead**: a file whose name no longer describes what it holds.

## 4. Not a problem

Leave these alone.

- A long file with one job. Length alone is never a reason to split.
- Layout a framework or tool requires: routing folders, migrations and their order, entry points, plugin folders, generated code.
- Anything loaded by name: modules named in configuration, plugin lists, entry points, strings passed to an importer. Search for the dotted path as text before moving anything.
- A structure that is consistent but not the one you would choose.
- Small projects. Three files do not need folders.

Never create layers, interfaces or abstractions. Organising moves existing code; it does not design new architecture.

## 5. Plan

List the moves in the order they will be made. Each move is one line: what moves, from where, to where, and why. Put dependency fixes before the moves that rely on them. Flag any move that changes a public path.

```
organize: <n> moves planned

1. <what>: <from> -> <to>. <why>
2. ...
Left alone: <file>: <why it looks like a candidate and is not>
Not sure: <file>: <what made it unclear>
```

With `report`, stop here.

## 6. Apply (only with `apply`, after the plan is shown)

One move at a time:

1. **Move, do not edit.** The moved code stays character for character the same. The only other things that change are imports and the way a moved name is referred to (`utils.money(x)` becomes `money(x)`). Any improvement to the code itself is a separate change, for another day or another skill.
2. **Keep every old path working.** Where code is imported from its old location by tests, documentation, other packages or anything public, leave a re-export at the old location. Remove a re-export only if the user asks.
   A re-export covers reading a name, not changing it. If any code assigns to or patches a module-level value through the old path (a setting, a constant patched in a test, a registry), leave that value where it is. Search for such assignments before moving it.
3. **Update references that are text**: configuration, entry points, documentation, scripts. An entry point must still resolve.
4. **Do not edit tests.** They must pass unchanged, through the old paths. That is the proof the move was safe.
5. **Use the version-control move** (`git mv`) when the whole file moves, so history follows.
6. **Run the checks after every move.** If they fail, undo that move and list it under "Skipped".

## 7. Report

```
organize: <n> moves made, <files before> -> <files after> files

Moved:
  - <what>: <from> -> <to>
Removed: <stale duplicate>: <how you confirmed nothing references it>
Old paths kept working: <path> re-exports from <new path>
Skipped: <move>: <why>
Left alone: <file>: <why>
Checks: <command> <before> -> <after>
```

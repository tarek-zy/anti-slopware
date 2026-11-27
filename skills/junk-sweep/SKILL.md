---
name: junk-sweep
description: Finds files a coding session left behind and caches that only waste disk space - review screenshots, scratch scripts, logs, backup files, build output - shows them with sizes, and removes them only after approval. Never touches tracked files, referenced files, secrets or user data. Use when the user asks to clean up a workspace or project folder, free disk space, remove leftover screenshots, temporary files or build caches, or types /junk-sweep or /anti-slopware junk.
license: MIT
metadata:
  version: "0.1.0"
---

# junk-sweep

Coding agents leave things behind: screenshots taken to check a screen, scratch scripts, logs, backups of files they edited, build output nobody cleared. This skill finds them. Deleting cannot be undone, so the default is to list, and every rule below leans toward leaving a file in place.

## 1. Read the request

| Argument | Meaning | Default |
|---|---|---|
| `report` | List candidates with sizes. Delete nothing. | on |
| `clean` | Remove them, after showing the list | off |
| a path | Folder to sweep | the project root |

Stay inside the given folder. Never follow a link out of it.

## 2. Find candidates

A file is a candidate only if it is in one of these two groups **and** passes every check in step 3.

**Regenerable**: output that a command recreates.

- Build output and tool caches: `build/`, `dist/`, `out/`, `target/`, `.dart_tool/`, `.gradle/`, `.next/`, `coverage/`, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `*.pyc`.
- System files: `.DS_Store`, `Thumbs.db`.

Confirm each is really generated: it is ignored by git or untracked, and the project has the tool that produces it. A folder named `build` that holds hand-written files is not a candidate.

**Session leftovers**: files made while working that are not part of the project.

- Screenshots and screen recordings: `Screenshot*`, `Screen Recording*`, review captures.
- Scratch files: `tmp_*`, `scratch*`, `debug*`, `output.txt`, `nohup.out`, one-off scripts in the project root.
- Logs: `*.log`.
- Backups and merge leftovers: `*.bak`, `*.orig`, `*.rej`, `*~`, `*.swp`.

## 3. Checks every candidate must pass

1. **Not tracked by git.** A tracked file is part of the project, whatever it is called. If a tracked file looks like junk, list it under "Tracked, looks like junk" and leave it.
2. **Not referenced.** Search the whole project for the file's name and path: source, tests, documentation, manifests, asset lists, build scripts, configuration. Any reference means it stays. An untracked image named in a manifest is a new asset someone has not committed yet.
3. **Not a secret or local setting.** `.env*`, keys, certificates, credentials, tokens. Never delete them and never print their contents.
4. **Not user data.** Databases (`*.db`, `*.sqlite`), uploads, downloads, documents, notes, exports the user asked for.
5. **Not editor or tool settings.** `.vscode/`, `.idea/`, lock files.
6. **You can say what it is.** If you cannot classify a file with confidence, list it under "Not sure" and leave it.

Dependency folders (`node_modules/`, virtual environments, `Pods/`) are regenerable but slow to rebuild. List them separately with their size. Remove one only if the user names it.

Global caches outside the project (`~/.pub-cache`, `~/.gradle`, `~/.npm`, `~/.cache`) are out of scope. Report their size if asked, and give the tool's own clean command.

## 4. Show the list

```
junk-sweep: <n> items, <total size>

Regenerable (<size>):
  - <path> <size> <what recreates it>
Session leftovers (<size>):
  - <path> <size> <why it is a leftover> <cannot be recovered | recoverable from <where>>
Dependency folders (not removed unless you name them):
  - <path> <size>
Tracked, looks like junk (left alone):
  - <path>: remove with `git rm` if you agree
Not sure (left alone):
  - <path>: <what made it unclear>
```

Session leftovers are untracked, so most cannot be recovered once deleted. Say so on each line, so the approval is an informed one. Hand-written files such as scratch scripts deserve the most care.

With `report`, stop here.

## 5. Clean (only with `clean`, after the list is approved)

- Prefer the project's own clean command for regenerable output: `flutter clean`, `cargo clean`, `gradle clean`, `dotnet clean`, `make clean`, `npm run clean`.
- Otherwise delete exactly the paths on the approved list, one by one. No wildcards, and no deleting a folder that is not itself on the list.
- If deleting is not permitted, move the items into a `_to_delete/` folder in the project and tell the user to remove it.
- Do not edit `.gitignore`, do not run git commands that change the repository, and do not touch anything not on the list.

## 6. Verify and report

Confirm each listed path is gone, that `git status` shows no tracked file changed or deleted, and that the project's checks still pass.

```
Removed: <n> items, <size freed>
Could not remove: <path>: <why>
Checks: <command> <result>
To stop these coming back: <.gitignore lines to consider>
```

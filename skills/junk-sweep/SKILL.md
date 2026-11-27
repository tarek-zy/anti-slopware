---
name: junk-sweep
description: Finds files a coding session left behind and caches that only waste disk space - review screenshots, scratch scripts, throwaway logs, build output - shows them with sizes, and removes them only after approval. Tells a useless cache from a backup, and a throwaway debug log from a log that matters. Never touches backups, application or audit logs, tracked files, referenced files, secrets or user data. Use when the user asks to clean up a workspace or project folder, free disk space, remove leftover screenshots, temporary files or build caches, or types /junk-sweep or /anti-slopware junk.
license: MIT
metadata:
  version: "0.2.0"
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
- Tool caches kept inside a dependency folder, such as `node_modules/.cache/`. The cache is a candidate; the dependency folder around it is not.
- System files: `.DS_Store`, `Thumbs.db`.

Confirm each is really generated: it is ignored by git or untracked, and the project has the tool that produces it. A folder named `build` that holds hand-written files is not a candidate.

**Session leftovers**: files made while working that are not part of the project.

- Screenshots and screen recordings: `Screenshot*`, `Screen Recording*`, review captures.
- Scratch files: `tmp_*`, `scratch*`, `output.txt`, one-off scripts in the project root.
- Throwaway logs: see "Logs" below. A `.log` ending alone decides nothing.
- Editor and merge leftovers: `*.orig`, `*.rej`, `*~`, `*.swp`, but only when "Copies and backups" below says the content exists elsewhere.

## Logs

A log can be noise from a test run or the only record of what happened in production. Work out which before listing it. Decide from evidence, in this order:

1. **Who writes it.** Search the code and configuration for the path. A file the application's logging is configured to write is an application log.
2. **What kind of record it is.** Names and folders such as `audit`, `access`, `security`, `transactions`, `payments`, `deploy`, `migration` mark records people rely on later.
3. **What is in it.** Read the first and last lines to classify it. A crash, a stack trace or error-level entries are evidence someone may still need. A file of debug lines from one local run is not. Never copy log lines into your output: logs often hold personal data and secrets.
4. **How it is managed.** Rotated files (`app.log.1`, `app.log.2.gz`) belong to a rotation policy. Leave them to it.

| Throwaway (candidate) | Matters (never a candidate) |
|---|---|
| Debug output from a local or agent session | Application and server logs |
| Package-manager and build-tool error dumps (`npm-debug.log`, `yarn-error.log`) | Audit, access, security and transaction logs |
| Captured output of a test run or a one-off command (`nohup.out`, `test-run.log`) | Deploy and migration records |
| Empty log files | Crash reports and logs containing errors or stack traces |
| | Rotated logs, and any log tracked by git |

List the logs that matter under "Logs kept", with a one-line reason and a flag on any that contain errors. If one is very large, suggest rotation or compression. Do not do it.

Unsure which kind it is: "Not sure", and leave it.

## Copies and backups

A backup exists so that something can be recovered. It is never junk because of its name.

- **Never a candidate**: `*.bak`, `*.backup`, `*.old`, `backup/` and `backups/` folders, database dumps (`*.sql`, `*.dump`), archives.
- **Editor and merge leftovers** (`*.orig`, `*.rej`, `*~`, `*.swp`) are candidates only when you have compared them and the content exists elsewhere: the file is identical to the file it was copied from, or to a version committed in git. If it differs, it may hold work that exists nowhere else: keep it.

List what you kept under "Backups kept". If backups take a lot of space, say so and let the user decide.

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
Logs kept:
  - <path> <size> <why it matters> <contains errors, if so>
Backups kept:
  - <path> <size> <what it appears to back up>
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

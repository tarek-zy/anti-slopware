---
name: split-pr
description: Plans how to break one oversized branch or pull request into small ones a human can review - groups the changes by purpose, orders them, says what depends on what, and lists what should be dropped. Produces a plan; it does not rewrite the branch. Use when the user says a PR or branch is too big, asks how to split, break up or stack a change, or types /split-pr or /anti-slopware split.
license: MIT
metadata:
  version: "0.1.0"
---

# split-pr

A pull request with five purposes gets one tired approval. Five pull requests with one purpose each get five real reviews. AI agents produce the first kind easily, because doing everything in one go costs them nothing.

This skill writes the plan for the split. It does not create branches, move commits or push. Carrying out the plan is a separate step the user asks for.

## 1. Gather

The diff against the base branch, the list of changed files with line counts, and the commit messages. Read the whole diff.

## 2. Find the purposes

Give every change exactly one purpose. Typical ones:

- **Mechanical**: a rename, a move, formatting. Large but quick to review when it is alone, and impossible to review when mixed with logic.
- **Groundwork**: settings, schema, a helper that later work needs.
- **Feature**: new behaviour.
- **Fix**: a bug fix.
- **Dependencies**: version bumps and their lock file.
- **Does not belong**: debug output, stray files, secrets.

A test belongs with the code it tests, never in a pull request of its own.

## 3. Build the plan

- One purpose per pull request.
- Every pull request must build and pass the tests by itself, once the ones it depends on are merged.
- Order: mechanical changes first, then groundwork, then the work that depends on it. Independent pieces can be reviewed in parallel: say so.
- State each dependency: "needs 1".
- Aim for under about 300 changed lines each, mechanical ones excepted.
- A file changed for two purposes is split by hunk. Name the file and say which hunks go where. If the hunks cannot be separated, say so under "Cannot be split cleanly" and put the file in the later pull request.
- If the branch already has one purpose and a reasonable size, say it does not need splitting, and stop.

## 4. Rules

- Every changed file appears in exactly one pull request, in the drop list, or under "Cannot be split cleanly". None is left out.
- Say only what the diff shows.
- If a file looks like a secret, say where it is. Never print its value. Dropping it from the branch does not remove it from history: say that it must be rotated.
- 300 words at most.
- Do not change the branch.

## 5. Output

```
Split plan: <n> files, <lines> lines -> <k> pull requests

1. <title> (<purpose>, about <lines> lines, needs: nothing)
   Files: <files>
   Review note: <one line on how to review it>
2. <title> (<purpose>, about <lines> lines, needs: 1)
   ...
Drop from the branch:
  - <file>: <why>
Cannot be split cleanly:
  - <file>: <which hunks belong where, or why they cannot be separated>
Merge order: <1, then 2 and 3 in either order, then 4>
```

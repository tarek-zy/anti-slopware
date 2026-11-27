---
name: review-map
description: Writes a short reading guide for the human reviewing a change - which files to read first and in what order, which need careful eyes and what question to ask of each, which are mechanical and can be skimmed, and what does not belong. Use when the user asks how to review a change, where to start in a large diff or pull request, wants a review guide, reviewer notes or a walkthrough of a branch, or types /review-map or /anti-slopware map.
license: MIT
metadata:
  version: "0.1.0"
---

# review-map

A reviewer's attention is the scarcest thing in a code review. A large diff gets skimmed evenly, so the risky ten lines get the same glance as the formatting change. This skill tells the reviewer where to spend their attention. It is a map, not a verdict: it never says the change is good.

## 1. Gather

The diff against the base branch, the list of changed files, and the commit messages. Read the whole diff before writing anything.

## 2. Sort every changed file into one group

- **Read carefully**: logic, money, security, permissions, data and schema changes, public interfaces, configuration and settings, concurrency, error handling.
- **Check the tests**: test files. Note what they prove and what they leave out.
- **Skim**: mechanical changes such as renames, formatting, moved code, generated files, lock files.
- **Does not belong**: stray files, debug output, unrelated edits, anything that looks like a secret.

Every changed file appears in exactly one group. None is left out.

## 3. Order the careful reading

Give the order that makes the change understandable, not alphabetical order:

1. The contract first: settings, schema, types, public signatures.
2. Then the core logic.
3. Then the callers of that logic.
4. Then the tests.

## 4. Give each careful file a question

For each file in "Read carefully", write one line: what changed, then the specific question the reviewer should answer, with line numbers where they help. A good question can be answered by reading the code: "Is an 8-character signature long enough?", not "Check security".

## 5. Rules

- 250 words at most, however large the diff. A longer map defeats its purpose.
- At most three risk hot spots, the three that matter most.
- Say only what the diff shows. No guesses about intent, no praise, no approval, no "looks good".
- If a file looks like a secret, say where it is. Never print its value.
- Do not review the code line by line. Point; do not judge.
- Do not change the branch.

## 6. Output

```
Review map: <n> files, <lines changed> lines. Careful reading: about <n> files.

Start here, in this order:
  1. <file>: <what changed>. Ask: <question>
  2. ...
Check the tests:
  - <test file>: covers <what>. Missing: <what>
Skim:
  - <file>: <why it is mechanical>
Does not belong:
  - <file>: <why>
Hot spots:
  - <file>:<line> <the risk in one line>
```

Leave out a group that is empty.

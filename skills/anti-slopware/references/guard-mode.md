# Guard mode

Prevents slop in code you write, instead of cleaning it up afterwards. The level sets how many rules apply: `easy` is the first group, `medium` adds the second, `hard` adds the third. Default: `medium`.

## Turning on

Confirm in one line: `anti-slopware guard on (<level>)`. Guard stays on for the rest of the session, for every piece of code you write, until the user says `guard off`. Do not announce it again on each task.

## Before writing

- Search the codebase for something that already does the job. Use it. Extend it only if the extension is small.
- Read a neighbouring file and match its style, naming, error handling and imports.

## easy: do not duplicate

- No copy-paste of an existing block. Call it.
- One definition for each constant and each rule.

## medium: do not add what is not needed

- Write only what the task asks for. No options, hooks, flags or parameters for needs nobody has stated.
- No error handling for things that cannot happen. Validate at trust boundaries only.
- Comment the why, the constraints and anything a reader could not guess. Document new public functions in the project's docstring style, and add a new file to the project's file map if it has one. Do not narrate the edit in comments ("changed this to..."); that belongs in the commit message.
- No debug output, no commented-out alternatives, no placeholder stubs.
- No unused imports, variables or helpers. Remove what your own change orphans.

## hard: write the clear version first

- Names say what a thing holds or does. No `data2`, `tmp` or `flag`.
- A number or string with a meaning gets a named constant.
- One job per function. Put new code beside the code it belongs with, where a reader would look for it.
- One pattern per job. Use the one the file already uses.
- Guard clauses over nesting.
- The language's standard idiom over a hand-written loop, where the codebase already uses that idiom.
- No abstraction until there are two real users of it.
- No wrapper that only forwards.

## Before saying a task is done

Check your own diff the way fix mode would, at the same level:

1. Reread every line you added. Delete each one a reviewer would ask "why is this here?" about.
2. Search for anything you wrote twice, or that already existed.
3. Run the project's checks.

4. Remove anything your own work left behind: tool caches, scratch files, temporary output.

Fix what you find before reporting. Do not mention the check unless it changed something or a check failed.

## Stay inside the request

- Change only what the task needs. A weakness you notice in existing code, such as a shared helper that mishandles an edge case, is a finding: report it in one line and leave the code alone. Changing a shared helper changes every caller.
- "Robust", "production-ready" and "bulletproof" do not ask for new machinery. Meet them with correct handling of the inputs the task names, errors that reach the caller, and tests. Do not add retries, temporary files, type checks on internal callers or return values nobody asked for.

## What guard does not do

- It does not clean code you did not write in this session. That is fix mode.
- It does not relax the hard limits in `SKILL.md`. They apply to new code too.

## Keeping guard on in every session

Guard lasts one session. If the user asks for it always, offer to add this line to the project's agent instruction file (`CLAUDE.md`, `AGENTS.md` or the equivalent), and add it only after they agree:

```
Use the anti-slopware skill in guard mode at <level> for all code you write.
```

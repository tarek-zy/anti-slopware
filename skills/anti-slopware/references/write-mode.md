# Write mode

Rules for code you are about to write. The level sets how many apply: `easy` is the first group, `medium` adds the second, `hard` adds the third.

## Before writing

- Search the codebase for something that already does the job. Use it. Extend it only if the extension is small.
- Read a neighbouring file and match its style, naming, error handling and imports.

## easy: do not duplicate

- No copy-paste of an existing block. Call it.
- One definition for each constant and each rule.

## medium: do not add what is not needed

- Write only what the task asks for. No options, hooks, flags or parameters for needs nobody has stated.
- No error handling for things that cannot happen. Validate at trust boundaries only.
- No comments that restate the code or describe the change. Comment only a non-obvious why.
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

## After writing

Reread your diff as a reviewer. Delete every line the reviewer would ask "why is this here?" about. Then run the project's checks.

---
name: error-slop
description: Finds error handling that hides failures - empty catch blocks, errors replaced by a default value, log-and-carry-on, catch-everything handlers, lost root causes, fake success - and tells them apart from deliberate handling. Reports by default; fixes on request. Use when the user asks to review or clean up error handling or exception handling, mentions swallowed, hidden or silent errors, try/except or try/catch overuse, or types /error-slop or /anti-slopware errors.
license: MIT
metadata:
  version: "0.1.0"
---

# error-slop

A failure that disappears is worse than a crash. The program carries on with wrong data, and nobody finds out until much later. AI-written code hides failures often, because a handler that swallows everything makes the code look robust and makes the tests pass.

## 1. Read the request

| Argument | Meaning | Default |
|---|---|---|
| `report` | List findings. Change nothing. | on |
| `fix` | Change the handlers, after showing the list | off |
| a path | File or folder | the current changes |

A fix here changes behaviour on purpose: an error that was hidden becomes visible. That is why nothing is changed without the list being shown first, and why each fix says what callers will now see.

## 2. Record a baseline

Run the project's checks and record the result.

## 3. Find

Read every handler: `try`/`except`, `try`/`catch`, `finally`, error return values, promise handlers, result types.

- **Swallowed**: a handler that does nothing, or only `pass`, `continue` or a comment.
- **Replaced by a default**: the handler returns `None`, `[]`, `{}`, `False`, `0` or `""`, so the caller cannot tell failure from a real empty result.
- **Log and carry on**: the handler prints or logs, then execution continues as if the step had worked.
- **Fake success**: the function reports success whatever happened.
- **Too broad**: a bare `except`, or catching `Exception`, `Throwable` or everything, around code that can also raise programming errors (wrong key, wrong type, missing attribute). In Python a bare `except` also catches `KeyboardInterrupt` and `SystemExit`.
- **Lost cause**: a new error raised from a handler without the original attached (`raise New(...)` with no `from e`; a message that drops the original detail; `throw ex;` in C#).
- **`finally` that hides**: `return`, `break` or `continue` inside `finally`, which discards any error in flight.
- **Ignored result**: an error return value, result type or rejected promise that nothing checks.
- **Unbounded retry**: retrying forever, or retrying errors that will never succeed.

## 4. Not slop

Leave these as they are.

- A **specific** exception with a deliberate fallback that the docstring, a comment, a test or the caller shows is intended: an unparsable field becomes `None` and callers skip it; a cache miss falls through to the real lookup.
- A **boundary handler** at the top of a program, request, job or worker loop that logs the error with its traceback and turns it into an exit code or error response.
- **Best-effort cleanup** that ignores one specific, expected error, such as deleting a file that may already be gone.
- A **bounded retry** on a specific transient error that re-raises when attempts run out.
- **Translation** to a domain error with the original attached.
- Optional-import fallbacks.

When a broad handler contains one legitimate case, the fix is to narrow it to that case, not to delete it.

## 5. Choose the smallest fix

For each finding, pick one:

1. **Remove the handler** when it adds nothing. The error then reaches a caller that can deal with it.
2. **Narrow it** to the specific exceptions this code can really handle, keeping the existing fallback for those.
3. **Stop hiding it**: keep the handler, log with the traceback at error level, and re-raise or return something the caller can tell apart from success.
4. **Attach the cause**: `raise New(...) from e`, or the language's equivalent.

Rules:

- Before changing a function, read every caller. If a caller relies on the silent default (`if result is None:`), prefer narrowing, and name that caller in the report.
- If a test pins the fallback for one case, that case is intended. Keep it and narrow the handler around it.
- Never invent a new fallback value or a new recovery path.
- Never replace one catch-everything with a different catch-everything.
- Do not edit tests. A test that asserted the silent behaviour and now fails is a decision for the user: report it.

## 6. Verify

Rerun the checks. Then, for each fix, trigger the failure and confirm it is now visible in the way the report says.

## 7. Report

```
error-slop: <handlers examined> examined, <n> hide failures

Hides failures: <n>
  - <file>:<line> <function>: <kind>. <what a failure looked like before> -> <what callers see now>. <fixed | reported>
Callers that relied on the old behaviour: <caller>: <what it must now handle>
Tests now failing because they asserted the silent behaviour: <test>
Left alone (deliberate handling): <n>
  - <function>: <why>
Checks: <command> <before> -> <after>
```

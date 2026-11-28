# Language checks

Run these for every language in scope. They look for bugs, which is a different job from cleanup, so the results are **findings**: reported separately, and fixed only when the user asks, because a fix changes behaviour.

| Files | Read |
|---|---|
| `.py` | [lang-python.md](lang-python.md) |
| `.js` `.jsx` `.ts` `.tsx` `.mjs` `.cjs` | [lang-javascript.md](lang-javascript.md) |
| `.java` | [lang-java.md](lang-java.md) |
| `.cs` | [lang-csharp.md](lang-csharp.md) |
| `.c` `.h` | [lang-c.md](lang-c.md) |
| `.cpp` `.cc` `.cxx` `.hpp` | [lang-cpp.md](lang-cpp.md), then [lang-c.md](lang-c.md) |
| `.go` | [lang-go.md](lang-go.md) |
| `.rs` | [lang-rust.md](lang-rust.md) |
| `.php` | [lang-php.md](lang-php.md) |
| `.dart` | [lang-dart.md](lang-dart.md) |
| `.sh` `.bash` `.zsh`, and any file whose first line is a shell shebang | [lang-shell.md](lang-shell.md) |
| `.sql`, and SQL statements inside other files | [lang-sql.md](lang-sql.md) |

No file for the language: apply the "Every language" list below and use the project's own compiler and linter.

## Method

1. **Does it build?** Run the build or syntax check listed for the language. A syntax or type error is the first finding; stop cleanup on that file until the user decides.
2. **Run the tools** that are installed. Prefer the project's own configuration and commands. Do not install anything without asking. Record which tools ran and which were missing.
3. **Read for the listed bugs**, in the code in scope and in what it calls.
4. **Respect "Not slop"** for the language during cleanup at every level.

Tools only see what they are built to see, and runtime tools only see paths the tests execute. Say what was not covered.

## Every language

Mistakes AI-written code makes everywhere:

- **Invented APIs**: a function, method, option or package that does not exist, or exists in a different version than the project uses. Check each unfamiliar call against the installed version, not memory.
- **Wrong signature**: arguments in the wrong order, a missing required argument, a return value used as the wrong type.
- **Unhandled absence**: null, nil, None, undefined or an empty collection on a path the code assumes is filled.
- **Swallowed errors**: an error caught and ignored, logged and dropped, or replaced with a default that hides the failure.
- **Off-by-one**: loop bounds, slices, ranges, pagination, inclusive against exclusive ends.
- **Leaked resources**: files, sockets, connections, locks, timers and subscriptions not released on every path, including the error path.
- **Missing await or join**: asynchronous work started and never awaited, so errors vanish and order is not guaranteed.
- **Shared state without protection**: data touched from several threads, tasks or requests.
- **Injection**: user input concatenated into SQL, shell commands, HTML, file paths or regular expressions.
- **Secrets in code**: keys, passwords and tokens written into source or logs.
- **Tests that mirror the code**: a new test that would pass whatever the code did.

## Report

```
<Language> findings: <n> (tools run: <list>; not available: <list>)
  - <file>:<line> <kind>: <one line>. Confirmed by <tool> | by reading only.
Not covered: <paths no test or tool exercised>
```

Never write "bug-free", "safe" or "secure". Write what ran and what it found.

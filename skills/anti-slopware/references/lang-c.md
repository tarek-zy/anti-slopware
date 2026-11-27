# C checks

Run these on C files in scope. They produce **findings**, reported separately from cleanup. Fix a finding only when the user asks: a fix changes behaviour.

## Use tools first

Reading code misses memory bugs. Use what is installed, and say which tools ran and which were missing.

| Tool | Command | Finds |
|---|---|---|
| Compiler warnings | `cc -Wall -Wextra -Wpedantic` | Uninitialised use, format mismatches, implicit conversions |
| AddressSanitizer | `cc -g -fsanitize=address,undefined` then run the tests | Use-after-free, double free, overflows, leaks, undefined behaviour |
| Valgrind | `valgrind --leak-check=full --error-exitcode=1 <test binary>` | Leaks, invalid reads and writes, uninitialised reads |
| clang-tidy | `clang-tidy <files> --` | Static bug patterns |
| cppcheck | `cppcheck --enable=warning,portability <files>` | Static bug patterns |

Sanitizers and Valgrind only see paths the tests execute. Name the paths that were not executed.

## Then read for these

For each allocation, trace every path to its release.

- **Use-after-free**: pointer read, written or returned after `free`; pointer into a buffer that `realloc` may have moved; pointer to a local returned or stored.
- **Double free**: two release paths for one allocation, common in error cleanup with `goto`.
- **Leak**: early `return` between allocation and release; overwritten pointer; `realloc` result assigned straight to the original pointer.
- **Unchecked allocation**: `malloc`, `calloc`, `realloc`, `strdup` result used without a null check.
- **Buffer overflow**: `strcpy`, `strcat`, `sprintf`, `gets`; `strncpy` without termination; index from input with no bound check; off-by-one on the terminator.
- **Size arithmetic**: `malloc(n * size)` with no overflow check; `sizeof` of a pointer where the pointee was meant; signed/unsigned mix in a length.
- **Format string**: non-literal passed as the format to `printf`-family functions.
- **Uninitialised read**: struct or buffer read before every field is set.
- **Unchecked return**: `read`, `write`, `fread`, `fopen`, `snprintf` results ignored where failure matters.

## Cleanup interactions

- Do not merge two cleanup blocks if ownership differs between the paths.
- Do not remove a null check before `free`-like project functions unless the function is documented to accept null.
- Do not remove `ptr = NULL` after `free`. It is not useless.
- Removing an "unused" variable can remove a side effect in its initialiser. Check.

## Report

```
C findings: <n> (tools run: <list>; not available: <list>)
  - <file>:<line> <kind>: <one line>. Confirmed by <tool> | by reading only.
Paths not executed by any test: <list>
```

Never write "memory safe". Write what ran and what it found.

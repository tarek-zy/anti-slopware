# C checks

Use with [languages.md](languages.md).

## Build and tools

| Tool | Command | Finds |
|---|---|---|
| Compiler | `cc -Wall -Wextra -Wpedantic -fsyntax-only <files>` | Syntax errors, uninitialised use, format mismatches, implicit conversions |
| AddressSanitizer | `cc -g -fsanitize=address,undefined`, then run the tests | Use-after-free, double free, overflows, leaks, undefined behaviour |
| Valgrind | `valgrind --leak-check=full --error-exitcode=1 <test binary>` | Leaks, invalid reads and writes, uninitialised reads |
| clang-tidy | `clang-tidy <files> --` | Static bug patterns |
| cppcheck | `cppcheck --enable=warning,portability <files>` | Static bug patterns |

## Frequent bugs

For each allocation, trace every path to its release.

- **Use-after-free**: pointer read, written or returned after `free`; pointer into a buffer that `realloc` may have moved; pointer to a local returned or stored.
- **Double free**: two release paths for one allocation, common in error cleanup with `goto`.
- **Leak**: early `return` between allocation and release; overwritten pointer; `realloc` result assigned straight to the original pointer.
- **Unchecked allocation**: `malloc`, `calloc`, `realloc`, `strdup` result used without a null check.
- **Buffer overflow**: `strcpy`, `strcat`, `sprintf`, `gets`; `strncpy` without termination; index from input with no bound check; off-by-one on the terminator.
- **Size arithmetic**: `malloc(n * size)` with no overflow check; `sizeof` of a pointer where the pointee was meant; signed and unsigned mixed in a length.
- **Format string**: non-literal passed as the format to `printf`-family functions.
- **Uninitialised read**: struct or buffer read before every field is set.
- **Unchecked return**: `read`, `write`, `fread`, `fopen`, `snprintf` results ignored where failure matters.
- **Integer overflow**: signed overflow is undefined behaviour; check before arithmetic on sizes and indexes.
- **Macro pitfalls**: arguments evaluated twice, missing parentheses, multi-statement macros without `do { } while (0)`.

## Not slop in C

- `ptr = NULL` after `free`.
- A null check before a project `free`-like function, unless it is documented to accept null.
- Two cleanup blocks whose ownership differs between paths. Do not merge them.
- An "unused" variable whose initialiser has a side effect.
- `(void)x;` and header guards.
- Functions that look unused but are exported in a header or referenced from a linker script or function-pointer table.

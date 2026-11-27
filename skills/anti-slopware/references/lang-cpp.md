# C++ checks

Use with [languages.md](languages.md). The C list in [lang-c.md](lang-c.md) applies too.

## Build and tools

| Tool | Command | Finds |
|---|---|---|
| Compiler | `c++ -std=<project standard> -Wall -Wextra -Wpedantic -fsyntax-only <files>` | Syntax and type errors, narrowing, unused results |
| Sanitizers | `-g -fsanitize=address,undefined` (and `-fsanitize=thread` in a separate build), then run the tests | Lifetime errors, undefined behaviour, data races |
| clang-tidy | `clang-tidy <files>` with `bugprone-*`, `cppcoreguidelines-*`, `performance-*` | Use-after-move, dangling handles, slicing, needless copies |
| cppcheck | `cppcheck --enable=warning,performance,portability <files>` | Static bug patterns |

## Frequent bugs

- **Dangling reference or view**: reference, pointer, iterator, `std::string_view` or `std::span` that outlives what it points to; reference to a local returned; lambda capturing a local by reference and stored.
- **Iterator invalidation**: inserting into or erasing from a container while iterating it; holding an iterator or pointer across `push_back`.
- **Use-after-move**: object read after `std::move`.
- **Manual ownership**: raw `new` and `delete`; `new[]` freed with `delete`; missing copy or move members when a destructor is written (rule of three and five).
- **Missing virtual destructor** on a base class deleted through a base pointer.
- **Object slicing**: derived object passed or stored by value as its base.
- **Uninitialised members**: built-in members left unset by a constructor.
- **Out-of-bounds**: `operator[]` on `vector`, `string` and `map` with unchecked indexes; `map[key]` inserting by accident.
- **Undefined behaviour**: signed overflow, shifting by too many bits, reading an inactive union member, strict-aliasing casts.
- **Accidental copies**: `for (auto x : container)` on large elements, pass by value where a const reference was meant.
- **Data races**: shared data without a mutex or atomic; mutex locked without a guard and left locked on an exception.
- **Exceptions**: throwing from a destructor; resources released by hand instead of RAII, so they leak when something throws.

## Not slop in C++

- Explicitly defaulted or deleted special members. They state intent.
- `override`, `noexcept`, `[[nodiscard]]`, `explicit` and `const`.
- Templates and inline functions in headers that look duplicated but must be visible in each translation unit.
- A static object whose constructor registers something.
- Include-what-you-use includes that another header happens to provide today.

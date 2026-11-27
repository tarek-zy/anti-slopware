# PHP checks

Use with [languages.md](languages.md).

## Build and tools

| Tool | Command | Finds |
|---|---|---|
| Syntax | `php -l <file>` | Syntax errors |
| PHPStan | `vendor/bin/phpstan analyse` | Undefined variables, methods and indexes, wrong types |
| Psalm | `vendor/bin/psalm` | Type errors, tainted input reaching a sink |
| Tests | `vendor/bin/phpunit` | Runtime behaviour |

## Frequent bugs

- **Loose comparison**: `==` and `!=` with type juggling; `in_array` and `array_search` without strict mode; `strpos(...) == false` where `=== false` is needed.
- **SQL injection**: queries built by concatenation instead of prepared statements.
- **Cross-site scripting**: output echoed without escaping.
- **Undefined variable, index or property** on a path that skips the assignment.
- **Missing `declare(strict_types=1)`** in a codebase that uses it elsewhere.
- **Unsafe input handling**: `unserialize`, `eval`, `include` or `require` with user input; `extract` on request data.
- **Weak password and token handling**: `md5` or `sha1` for passwords instead of `password_hash`; `rand` for tokens instead of `random_bytes`.
- **Suppressed errors**: `@` in front of a call.
- **Argument order**: needle and haystack swapped in string and array functions.
- **Null handling**: a method called on a value that can be `null`; nullable return types ignored.
- **Money in floats**.

## Not slop in PHP

- Magic methods (`__get`, `__call`, `__invoke`) and members reached through them.
- Classes and methods a framework finds by name or convention: controllers, routes named in strings, service providers, event listeners, console commands, template helpers.
- Callbacks registered by string, such as WordPress `add_action` and `add_filter`.
- Classes loaded through the autoloader that nothing references directly.
- Docblock types that static analysis reads.

# Python checks

Use with [languages.md](languages.md).

## Build and tools

| Tool | Command | Finds |
|---|---|---|
| Syntax | `python -m compileall -q <paths>` | Syntax and indentation errors |
| Ruff | `ruff check <paths>` | Undefined names, unused imports and variables, common bugs |
| Type checker | `mypy <paths>` or `pyright <paths>` | Wrong argument types, missing attributes, `None` misuse |
| Vulture | `vulture <paths>` | Unused code (confirm each hit; see "Not slop") |
| Bandit | `bandit -r <paths>` | Unsafe calls |

## Frequent bugs

- **Mutable default argument**: `def f(items=[])` or `={}` shared between calls.
- **Late-binding closure**: a lambda or inner function created in a loop that reads the loop variable later.
- **Unawaited coroutine**: `async` function called without `await`; blocking calls (`time.sleep`, `requests`) inside `async` code.
- **Broad except**: bare `except:` or `except Exception:` that hides the error, or catches `KeyboardInterrupt` and `SystemExit`.
- **Identity for equality**: `is` used to compare strings or numbers; `== None` instead of `is None`.
- **Changing a collection while iterating it**.
- **Shadowing**: a variable or file named after a builtin or a standard module (`list`, `id`, `json.py`).
- **Missing `f`** on a string with `{placeholders}`; `%` and `.format` argument mismatches.
- **Files and connections** opened without `with`.
- **Dates and numbers**: naive and aware `datetime` mixed; `datetime.utcnow()`; float equality; `/` where `//` was meant; money in floats.
- **`assert` for validation**: removed when Python runs with `-O`.
- **Unsafe input handling**: `eval`, `exec`, `pickle.loads`, `yaml.load` without a safe loader, `subprocess(..., shell=True)`, SQL built with string formatting.
- **Wrong scope**: a name assigned inside a function that was meant to change a global; a missing `return` on one branch, so the function returns `None`.
- **Truthiness**: `if x:` where `0`, `""` or an empty list is a valid value.

## Not slop in Python

- Names listed in `__all__`, and imports in `__init__.py` that re-export.
- Functions used through a decorator or a framework: routes, CLI commands, signal handlers, pytest fixtures and hooks, Django models, migrations and admin classes.
- Dunder methods, and attributes reached through `getattr` or by name from config.
- Imports under `if TYPE_CHECKING:`, imports kept for side effects, and lines marked `# noqa`.
- `conftest.py`, `setup.py`, entry points declared in `pyproject.toml`.

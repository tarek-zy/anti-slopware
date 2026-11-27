# Levels

Each level includes the ones above it.

## easy: duplication

**Counts**

- Two or more functions with the same body.
- The same block of statements repeated in several places.
- The same condition or expression chain repeated when it has one meaning.
- Constants and literals with one meaning defined in several places.

**Fix**

- Keep one copy; make the others call it.
- If a duplicate is a public name, keep the name and make it delegate. Never delete it.

**Does not count**

- Code that looks alike but changes for different reasons (two validators for unrelated forms). Merging these couples things that should move apart.
- Two or three similar lines. A helper that needs a paragraph of parameters is worse than the repetition.
- Tests that repeat setup for readability.
- Anything where merging needs a new flag or mode parameter to tell the callers apart.

## medium: useless code

**Counts**

- Unused imports, variables, parameters of private functions, private functions, private types.
- Unreachable code: after `return`/`throw`, branches on constants, conditions that cannot be true.
- Commented-out code.
- Leftover debugging: prints, logs added for a one-off investigation, flags that are always off.
- Comments that restate the code, narrate the edit ("added this to fix..."), or describe what was removed.
- Wrappers that only forward to another function with the same arguments, when private.
- Checks for states the surrounding code already rules out (null check right after construction, re-validating validated input inside the same module).
- `try`/`catch` that only rethrows the same error unchanged.
- Variables assigned once and returned on the next line, where the name adds nothing.
- Stubs, placeholder implementations and empty overrides nothing calls.

**Does not count**

- Comments explaining why: constraints, workarounds, links to issues.
- Validation at a trust boundary: user input, network, files, other processes.
- Anything public, exported, or referenced from config, templates, reflection or registration.
- Feature flags that can be turned on from outside the code.
- Defensive code with a test that exercises it.
- Logging that is part of the product's behaviour.

## hard: over-verbose code

**Counts**

- Nested conditionals that flatten with early returns or guard clauses.
- `if cond: return True else: return False` and its relatives.
- Hand-written loops that match a standard idiom of the language (sum, any/all, map/filter, comprehension) when the idiom is common in this codebase.
- Temporary variables that only rename a value once.
- Abstractions with one user: a class with one method, an interface with one implementation, a factory that builds one thing, a config option nobody sets. Inline them when private.
- Repeated string building that a format call expresses directly.
- Boolean expressions that simplify with no change in short-circuit behaviour.

**Test for every hard change**

A reader new to the code must understand the new version faster than the old one. If that is not clearly true, leave it.

**Does not count**

- Anything that changes evaluation order, short-circuiting, or the number of times something is called.
- Floating-point rewrites. `a + a * r` and `a * (1 + r)` can round differently. Leave arithmetic as written.
- Replacing a loop with an idiom that changes laziness, memory use or complexity.
- Collapsing code that is long because the problem is.
- Performance-sensitive code where the verbose form is deliberate.
- Renaming. Names are out of scope unless a name is false.

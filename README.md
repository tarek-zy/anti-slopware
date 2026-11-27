# anti-slopware

Skills for AI coding agents that remove duplicated, useless and over-verbose code without changing what the code does, and keep changes easy for humans to review.

Works in Claude Code as a plugin. The skills use the open [Agent Skills](https://agentskills.io) format, so other agents that read `SKILL.md` can use them too.

## Install

**Claude Code plugin**

```
/plugin marketplace add tarek-zy/anti-slopware
/plugin install anti-slopware@tarek-zy
```

Run it as `/anti-slopware:anti-slopware`.

**Standalone skill, any agent**

```
npx skills add tarek-zy/anti-slopware
```

Run it as `/anti-slopware`.

## Use

```
/anti-slopware                    clean the current changes at medium
/anti-slopware easy               duplication only
/anti-slopware hard src/parser.c  everything, one file
/anti-slopware report             list findings, change nothing
/anti-slopware write hard         apply the rules to code about to be written
```

Or ask in plain words: "clean up this branch", "remove the dead code in `utils/`".

## Levels

| Level | Removes | Applies |
|---|---|---|
| `easy` | Duplicated code | Directly |
| `medium` | + unused, unreachable and leftover code, comments that restate the code | After you approve the list |
| `hard` | + needless nesting, hand-written loops, single-use abstractions | After you approve the list |

Full definitions: [levels.md](skills/anti-slopware/references/levels.md).

## What it will not do

- Change behaviour: outputs, errors, ordering, numeric results.
- Remove or change anything public.
- Edit generated, vendored or ignored files, or anything outside the scope you gave.
- Make code shorter at the cost of clarity.
- Work without a safety net. With no tests covering the code, it reports and stops.
- Say your code is bug-free. It says what was checked and what was not.

It runs your tests, linter and type-checker before and after, and reverts any change that breaks them.

## Proof

[`examples/python`](examples/python) holds one sloppy file and the result at each level. One test file runs against all four:

```
$ python3 examples/verify.py
before   96 lines  tests: pass
easy     86 lines  tests: pass
medium   56 lines  tests: pass
hard     47 lines  tests: pass
```

Two rewrites `hard` refused in that file, because they change results:

- `sum()` instead of the running total. On Python 3.12+, `sum([0.1] * 10)` is `1.0`; the loop gives `0.9999999999999999`.
- A dictionary lookup for the discount tier. It raises on an unhashable tier where the original returned `0`.

## Language checks

C: use-after-free, double free, leaks, overflows, unchecked allocations, format strings. It runs AddressSanitizer, Valgrind, clang-tidy and cppcheck when installed, and reports which ones ran. See [lang-c.md](skills/anti-slopware/references/lang-c.md) and [`examples/c`](examples/c).

## Status

| Skill | Does | Status |
|---|---|---|
| `anti-slopware` | Duplicated, useless and verbose code | Shipped |
| `slim-pr` | Short, clear PR descriptions | Next |
| `test-slop` | Tests that prove nothing | Planned |
| `dep-check` | Unused and non-existent dependencies | Planned |
| `error-slop` | Swallowed and hidden errors | Planned |
| `junk-sweep` | Leftover screenshots, temp files, build caches | Planned |

More in [ROADMAP.md](ROADMAP.md).

## Related

For generic-looking UI and copy, see [antislop](https://github.com/miqdadbadjuber/anti-slop). This project covers code and review.

## License

[MIT](LICENSE)

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img src="assets/banner-light.svg" alt="anti-slopware: cleaner code, same behaviour" width="100%">
</picture>

<br>

**A plugin that helps your coding agent produce higher-quality code<br>and pull requests humans can review, then proves nothing broke.**

[What it improves](#what-it-improves) · [Two modes](#two-modes) · [Built for review](#built-for-human-review) · [Install](#install) · [Use](#use) · [Levels](#levels) · [Proof](#proof) · [Roadmap](ROADMAP.md)

[![verify](https://github.com/tarek-zy/anti-slopware/actions/workflows/verify.yml/badge.svg)](https://github.com/tarek-zy/anti-slopware/actions/workflows/verify.yml)
[![license](https://img.shields.io/github/license/tarek-zy/anti-slopware?style=flat-square&color=1a7f37)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-compatible-1f2328?style=flat-square)](https://agentskills.io)
[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-cf222e?style=flat-square)](#install)

</div>

---

AI agents write code fast, and a lot of it is filler: the same function twice, imports nobody uses, comments that repeat the line below them, five levels of nesting where one would do. A human still has to review all of it.

anti-slopware improves the quality of that code. It removes the filler, then makes what is left clearer and better organised. It runs your tests before and after, and reverts any change that breaks them.

## What it improves

| Goal | What changes |
|---|---|
| **Easier to read** | Flat control flow instead of deep nesting, names that say what a thing holds, named constants instead of bare numbers |
| **Easier to edit** | One copy of each rule, no dead code to step around, functions that do one job |
| **Better organised** | Related code kept together, one pattern per job, consistent with the rest of your project |

This is not a minifier. Fewer lines is a side effect, not the goal. When a named constant or a small helper makes code clearer, it adds one, and it never trades clarity for brevity.

## Two modes

| Mode | When | What it does |
|---|---|---|
| **Guard** | While the agent writes code | Stops slop before it is written. The agent reuses what exists, writes only what the task needs, and checks its own diff before saying it is done. Stays on for the whole session. |
| **Fix** | On code that already exists | Finds and removes slop, from your current change up to the whole project, in batches small enough to review. |

Use one or both. Guard keeps new code clean. Fix deals with what is already there.

## Built for human review

AI can write code faster than people can read it. When reviews turn into skimming, quality slips without anyone deciding it should. Every part of this plugin is meant to keep a human able to follow what changed.

- **Small scope.** By default it touches only your current change, not the whole repo.
- **One kind of change at a time.** Duplicate removal, dead code and renames arrive separately, so you can accept one and reject another.
- **Renames and moves on their own.** They never hide inside other edits.
- **A short report.** What changed and why, what was skipped, which checks ran, and what nothing verified.
- **Batches you can read.** A whole-project cleanup goes folder by folder and stops to ask when a batch gets large.
- **Tests left alone.** It does not edit tests in the same run as the code they protect.

The `slim-pr` skill then writes the pull request description: what changed, why, how to test it and the risks, in 200 words or fewer. It drops claims the diff does not support, never trims a breaking change, and lists stray files and unrelated edits that should not be in the branch.

## Before and after

One function from [`examples/python`](examples/python), cleaned with `/anti-slopware hard`:

<table>
<tr><th>Before</th><th>After</th></tr>
<tr>
<td>

```python
def get_discount(customer):
    if customer is not None:
        if "tier" in customer:
            if customer["tier"] == "gold":
                return 0.1
            else:
                if customer["tier"] == "silver":
                    return 0.05
                else:
                    return 0
        else:
            return 0
    else:
        return 0
```

</td>
<td>

```python
def get_discount(customer):
    if customer is None or "tier" not in customer:
        return 0
    if customer["tier"] == "gold":
        return 0.1
    if customer["tier"] == "silver":
        return 0.05
    return 0
```

Same result for every input. No nesting to keep in your head.

</td>
</tr>
</table>

## Install

### Claude Code

```
/plugin marketplace add tarek-zy/anti-slopware
/plugin install anti-slopware@tarek-zy
```

Run it as `/anti-slopware:anti-slopware`.

### Any agent that reads SKILL.md

```
npx skills add tarek-zy/anti-slopware
```

Run it as `/anti-slopware`.

## Use

| Command | What it does |
|---|---|
| `/anti-slopware` | Fix the current changes at `medium` |
| `/anti-slopware easy` | Duplication only |
| `/anti-slopware hard src/parser.c` | Everything, including naming and organisation, one file |
| `/anti-slopware all` | Fix the whole project, one folder at a time |
| `/anti-slopware report` | List findings, change nothing |
| `/anti-slopware pr` or `/slim-pr` | Write or trim the pull request description |
| `/anti-slopware junk` or `/junk-sweep` | List leftover files and caches with sizes; add `clean` to remove them after approval |
| `/anti-slopware errors` or `/error-slop` | Report error handling that hides failures; add `fix` to change it |
| `/anti-slopware deps` or `/dep-check` | Report unused, missing and unverifiable dependencies; add `fix` to edit the manifest |
| `/anti-slopware tests` or `/test-slop` | Report tests that prove nothing; add `fix` to strengthen or remove them |
| `/anti-slopware guard` | Turn guard mode on for this session |
| `/anti-slopware guard hard` | Guard mode with the strictest rules |

Or ask in plain words: "clean up this branch", "remove the dead code in `utils/`".

## Levels

| Level | Fixes | Applies |
|---|---|---|
| `easy` | Duplicated code | Directly |
| `medium` | + unused, unreachable and leftover code, comments that restate the code | After you approve the list |
| `hard` | + needless nesting and single-use abstractions, misleading names, unnamed constants, functions that do several jobs, scattered related code | After you approve the list |

Full definitions: [levels.md](skills/anti-slopware/references/levels.md).

## What it will not do

- Change behaviour: outputs, errors, ordering, numeric results.
- Remove or change anything public.
- Edit generated, vendored or ignored files, or anything outside the scope you gave.
- Make code shorter at the cost of clarity.
- Rename or reorganise to suit its own taste. Your project's style wins.
- Work without a safety net. Code with no tests is compared before and after, and listed as not verified by tests. Code it cannot exercise is reported, not changed.
- Edit your tests while it edits the code they protect.
- Say your code is bug-free. It says what was checked and what was not.

## Proof

[`examples/python`](examples/python) holds one sloppy file and the result at each level. One test file runs against all four:

```
$ python3 examples/verify.py
before   96 lines  tests: pass
easy     86 lines  tests: pass
medium   56 lines  tests: pass
hard     50 lines  tests: pass
```

`hard` is not the shortest possible version. It added a named constant, `BULK_ORDER_MIN_UNITS`, in place of a bare `10`, because that reads better.

Two rewrites `hard` refused in that file, because they change results:

| Tempting rewrite | Why it was refused |
|---|---|
| `sum()` instead of the running total | On Python 3.12+, `sum([0.1] * 10)` is `1.0`. The loop gives `0.9999999999999999`. |
| A dictionary lookup for the discount tier | It raises on an unhashable tier where the original returned `0`. |

## Language checks

Cleanup is one job. Finding bugs is another. For each language in your code, the skill first checks that the code builds, runs the standard tools that are installed, then reads for the bugs that language is known for. It reports them as findings and fixes them only if you ask, because a fix changes behaviour.

| Language | Tools it runs when installed | Examples of what it looks for |
|---|---|---|
| Python | compileall, Ruff, mypy or Pyright, Vulture, Bandit | Mutable default arguments, unawaited coroutines, broad `except`, unsafe `eval` and `pickle` |
| JavaScript, TypeScript | `node --check`, `tsc`, ESLint, Knip | Missing `await`, loose equality, stale closures in hooks, `any` and `!` hiding errors |
| Java | javac, SpotBugs, Error Prone, PMD | Null dereference, `==` on strings, unclosed resources, thread-unsafe shared state |
| C# | `dotnet build` analyzers, `dotnet format` | `async void`, blocking on `.Result`, undisposed objects, LINQ enumerated twice |
| C | compiler warnings, AddressSanitizer, Valgrind, clang-tidy, cppcheck | Use-after-free, double free, leaks, buffer overflows |
| C++ | sanitizers, clang-tidy, cppcheck | Dangling references, iterator invalidation, use-after-move, slicing |
| Go | `go vet`, race detector, Staticcheck, govulncheck | Ignored errors, shadowed `err`, goroutine leaks, data races |
| Rust | `cargo check`, Clippy, Miri, cargo audit | `unwrap` on recoverable errors, unjustified `unsafe`, locks held across `.await` |
| PHP | `php -l`, PHPStan, Psalm | Loose comparison, SQL injection, unescaped output |
| Dart, Flutter | `dart analyze`, `flutter test` | `BuildContext` after `await`, undisposed controllers, futures created in `build` |

Every language also gets the checks for mistakes AI-written code makes everywhere: invented APIs, wrong signatures, swallowed errors, off-by-one, leaked resources, injection and secrets in code.

Each language file also lists what is **not** slop there, such as functions a framework finds by name, so cleanup leaves them alone. Details: [languages.md](skills/anti-slopware/references/languages.md).

It reports which tools ran and which were missing, and it never claims your code is bug-free.

## Skills

| Skill | Does | Status |
|---|---|---|
| `anti-slopware` | Duplicated, useless, verbose, unclear and disorganised code | Shipped |
| `slim-pr` | PR descriptions a reviewer can read in a minute; flags noise in the diff and claims the diff does not support | Shipped |
| `test-slop` | Finds tests that prove nothing, and proves it by breaking the code and showing the test still passes | Shipped |
| `dep-check` | Unused and undeclared dependencies, and AI-invented package names. Never adds a package without evidence it exists | Shipped |
| `error-slop` | Error handling that hides failures: empty catches, silent defaults, fake success, lost causes. Leaves deliberate handling alone | Shipped |
| `junk-sweep` | Leftover screenshots, scratch files, logs and build caches. Lists with sizes, removes only after approval, never touches tracked or referenced files, secrets or user data | Shipped |

More in [ROADMAP.md](ROADMAP.md). Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).

## Related

For generic-looking UI and copy, see [antislop](https://github.com/miqdadbadjuber/anti-slop). This project covers code and review.

---

<div align="center">

*The best code review is the one with less to read.*

[MIT](LICENSE)

</div>

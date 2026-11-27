# JavaScript and TypeScript checks

Use with [languages.md](languages.md).

## Build and tools

| Tool | Command | Finds |
|---|---|---|
| Syntax | `node --check <file.js>` | Syntax errors |
| TypeScript | `tsc --noEmit` | Type errors, missing properties, wrong arguments |
| ESLint | `eslint <paths>` (with the project's config) | Unused code, floating promises, hook rules, common bugs |
| Knip | `knip` | Unused files, exports and dependencies (confirm each hit) |
| Tests | the project's test script | Runtime behaviour |

## Frequent bugs

- **Missing `await`**: a promise not awaited or returned, so errors are unhandled and order is not guaranteed; `await` inside `forEach`, which does not wait.
- **Loose equality**: `==` and `!=`; comparing objects or arrays by value with `===`; checks against `NaN`.
- **Falsy checks that drop valid values**: `if (x)` or `x || default` where `0`, `""` or `false` is valid. Use `??`.
- **Lost `this`**: a method passed as a callback without binding.
- **Mutation**: changing an argument, shared object or React state or props in place; `sort` and `reverse` mutating the original array.
- **Default sort**: `array.sort()` on numbers sorts them as strings.
- **Stale closure**: a callback or effect reading an old value; wrong or missing dependency array in React hooks; hooks called conditionally.
- **Missing cleanup**: event listeners, timers, subscriptions and effects not removed.
- **Unsafe parsing**: `JSON.parse` on outside input without a try; `parseInt` without checking for `NaN`.
- **Dates**: zero-based months, local time against UTC, date strings parsed without a time zone.
- **TypeScript escapes**: `any`, `as` casts, non-null `!`, `@ts-ignore` used to silence a real error.
- **Injection**: `innerHTML`, `dangerouslySetInnerHTML`, `eval`, `new Function`, user input in a query string or shell command.
- **Module mistakes**: mixing CommonJS and ES modules; importing a package that is not in `package.json`.

## Not slop in JavaScript and TypeScript

- Side-effect imports: `import "./styles.css"`, polyfills, instrumentation.
- Exports a framework finds by convention: pages, routes, layouts, loaders, config files, default exports, serverless handlers.
- Barrel files (`index.ts`) that re-export a public API.
- Anything named in `package.json`: `main`, `exports`, `bin`, `scripts`.
- Classes and members used through decorators or dependency injection.
- `// eslint-disable` and `@ts-expect-error` lines that carry a reason.
- Type-only exports and declaration files (`.d.ts`).

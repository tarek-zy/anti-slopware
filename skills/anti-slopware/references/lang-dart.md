# Dart and Flutter checks

Use with [languages.md](languages.md).

## Build and tools

| Tool | Command | Finds |
|---|---|---|
| Analyzer | `dart analyze` or `flutter analyze` | Syntax and type errors, null-safety problems, lint rules |
| Fixes | `dart fix --dry-run` | Mechanical fixes available |
| Tests | `dart test` or `flutter test` | Runtime behaviour |

## Frequent bugs

- **Null assertion**: `!` on a value that can be null; `late` fields read before they are set.
- **Unawaited future**: an async call without `await`, so errors are lost and order is not guaranteed.
- **`BuildContext` after `await`**: context used across an async gap without checking `mounted`.
- **`setState` after `dispose`**, or called from `build`.
- **Not disposed**: controllers, focus nodes, animation controllers, stream subscriptions and timers left open.
- **Future created in `build`**: a `FutureBuilder` or `StreamBuilder` given a new future on every rebuild, so the work repeats.
- **Heavy work in `build`**: network calls, parsing or sorting on every rebuild.
- **Missing keys** on list items that can reorder, so state attaches to the wrong item.
- **Rebuilding too much**: `setState` high in the tree; missing `const` constructors.
- **Swallowed errors**: `catch (e) {}`; catching everything where a specific exception was meant.
- **Parsing**: `int.parse` and `double.parse` on outside input instead of `tryParse`.
- **`dynamic`** used where a type is known, hiding errors until run time.
- **Layout errors**: unbounded height or width inside scrollables, `Expanded` outside a flex.

## Not slop in Dart and Flutter

- Generated files: `*.g.dart`, `*.freezed.dart`, `*.gr.dart`, localisation output. Never edit them.
- `build/` and `.dart_tool/`.
- Code marked `@pragma('vm:entry-point')`, and `main`.
- Widgets, routes and platform channels referenced by name in strings.
- `const` constructors and `Key` parameters.
- `initState` and `dispose` overrides that set up or tear down something.

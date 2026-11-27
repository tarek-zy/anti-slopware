# C# checks

Use with [languages.md](languages.md).

## Build and tools

| Tool | Command | Finds |
|---|---|---|
| Compiler and analyzers | `dotnet build` | Syntax and type errors, nullable warnings, analyzer rules |
| Format | `dotnet format --verify-no-changes` | Style and analyzer violations |
| Tests | `dotnet test` | Runtime behaviour |

## Frequent bugs

- **Null reference**: values used without a check; the null-forgiving `!` hiding a real warning; nullable reference types switched off.
- **Async misuse**: `async void` outside event handlers; `.Result`, `.Wait()` or `.GetAwaiter().GetResult()` blocking and deadlocking; a task not awaited.
- **Not disposed**: `IDisposable` and `IAsyncDisposable` objects without `using`; a new `HttpClient` per request.
- **LINQ deferred execution**: a query enumerated several times, or enumerated after its source changed or was disposed.
- **Closure capture**: a lambda in a loop capturing a variable that changes afterwards.
- **Equality**: `==` on reference types where `Equals` was meant; `Equals` overridden without `GetHashCode`.
- **Struct copies**: changing a struct held in a collection or property changes a copy.
- **Swallowed exceptions**: `catch (Exception)` with nothing done; `throw ex;` losing the stack trace instead of `throw;`.
- **Dates**: `DateTime.Now` where UTC was meant; `DateTime` kinds mixed.
- **Event handler leaks**: subscribing without unsubscribing.
- **Collections changed while enumerated**.
- **SQL built with string interpolation** instead of parameters.

## Not slop in C#

- Members used by reflection, dependency injection, serialisation or data binding: controllers, DTO properties, XAML-bound members, EF Core entities and migrations.
- Anything carrying an attribute a framework reads.
- `partial` classes and generated files (`*.g.cs`, `*.Designer.cs`).
- Public members of a library.
- `ConfigureAwait(false)` in library code.
- Empty constructors that serialisers or frameworks need.

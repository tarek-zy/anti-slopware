# Go checks

Use with [languages.md](languages.md).

## Build and tools

| Tool | Command | Finds |
|---|---|---|
| Compiler | `go build ./...` | Syntax and type errors, unused imports and variables |
| Vet | `go vet ./...` | Copied locks, bad format strings, unreachable code, lost cancels |
| Race detector | `go test -race ./...` | Data races on executed paths |
| Staticcheck | `staticcheck ./...` or `golangci-lint run` | Unused code, ignored errors, misuse of the standard library |
| Vulnerabilities | `govulncheck ./...` | Known vulnerable dependencies in use |

## Frequent bugs

- **Ignored error**: a returned `error` dropped or assigned to `_`; `rows.Err()` not checked; `defer f.Close()` hiding a write error.
- **Shadowed `err`**: `:=` inside a block creating a new `err`, so the outer one is never set.
- **Nil map write**: assigning into a map that was declared and never made.
- **Nil interface confusion**: an interface holding a nil pointer is not `nil`.
- **Goroutine leak**: a goroutine blocked forever on a channel nobody reads or closes; no way to stop it.
- **Data race**: shared variables or maps used from several goroutines without a mutex or channel.
- **Deadlock**: send on an unbuffered channel with no receiver; a lock taken twice; `WaitGroup.Add` called inside the goroutine.
- **Loop variable capture** in goroutines and closures, in modules on a Go version before 1.22.
- **Resource leak**: `resp.Body`, files and rows not closed; `defer` inside a loop; `context.WithCancel` or `WithTimeout` whose cancel is never called.
- **Slice aliasing**: `append` writing into an array another slice still shares.
- **Copied lock**: a struct holding a `sync.Mutex` passed by value.
- **Context**: not passed down, or stored in a struct.

## Not slop in Go

- Exported identifiers in a library, and methods that satisfy an interface.
- `init()` functions and blank imports that register something (`_ "github.com/lib/pq"`).
- Compile-time interface checks: `var _ Iface = (*T)(nil)`.
- Files behind build tags, `//go:generate` and `//go:embed` directives, and generated files.
- `if err != nil` blocks. They are the language's error handling, not repetition to merge.
- Struct tags.

# Rust checks

Use with [languages.md](languages.md).

## Build and tools

| Tool | Command | Finds |
|---|---|---|
| Compiler | `cargo check --all-targets` | Syntax, type, borrow and lifetime errors |
| Clippy | `cargo clippy --all-targets -- -D warnings` | Common mistakes, needless clones, suspicious casts |
| Tests | `cargo test` | Runtime behaviour, including panics and debug overflow checks |
| Miri | `cargo +nightly miri test` (when `unsafe` is in scope; needs the nightly toolchain) | Undefined behaviour in unsafe code |
| Audit | `cargo audit` | Known vulnerable dependencies |

## Frequent bugs

- **Panics on recoverable errors**: `unwrap()`, `expect()`, indexing with `[]`, slicing strings at byte offsets, and division, in code that should return a `Result`.
- **Dropped results**: `let _ = fallible();` or a `Result` ignored.
- **Clone to satisfy the borrow checker**: `.clone()` that copies large data or hides a design problem.
- **Unjustified `unsafe`**: an unsafe block with no comment stating why it is sound; raw pointers kept past the data's lifetime.
- **Integer behaviour**: arithmetic that overflows (it wraps in release builds); `as` casts that truncate or change sign.
- **Async**: blocking calls inside async code; a `std::sync::Mutex` guard held across `.await`; a future created and never awaited.
- **Deadlock**: taking the same mutex twice; inconsistent lock order.
- **Reference cycles**: `Rc` or `Arc` cycles that never free; a missing `Weak`.
- **Invented crate APIs**: methods and features that do not exist in the version in `Cargo.lock`.

## Not slop in Rust

- `pub` items of a library, trait implementations and derives.
- Code behind `#[cfg(...)]` and cargo features, including `#[cfg(test)]`.
- `#[allow(...)]` attributes that carry a reason.
- FFI items: `#[no_mangle]`, `extern "C"`.
- Explicit lifetimes and type annotations the compiler needs.
- `?` chains and `match` arms that look repetitive but handle different errors.

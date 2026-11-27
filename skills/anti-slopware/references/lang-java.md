# Java checks

Use with [languages.md](languages.md).

## Build and tools

| Tool | Command | Finds |
|---|---|---|
| Compiler | the project's build (`mvn -q compile`, `gradle compileJava`) or `javac -Xlint:all` | Syntax and type errors, unchecked and deprecated use |
| SpotBugs | the project's SpotBugs task | Null dereference, bad equality, leaks, concurrency bugs |
| Error Prone | compiler plugin, if configured | Common bug patterns at compile time |
| PMD | the project's PMD task | Unused code, empty catch blocks |
| Tests | `mvn test` or `gradle test` | Runtime behaviour |

## Frequent bugs

- **NullPointerException**: return values, map lookups and fields used without a null check; `Optional.get()` without checking; unboxing a null `Integer`.
- **`==` on objects**: strings, boxed numbers and enums-as-strings compared with `==` instead of `equals`.
- **Resource leak**: streams, readers, connections and statements not opened in try-with-resources.
- **`equals` without `hashCode`**, or either one using mutable fields.
- **ConcurrentModificationException**: removing from a collection inside a for-each over it.
- **Swallowed exceptions**: empty `catch`; catching `Exception` or `Throwable`; `InterruptedException` caught without restoring the interrupt flag.
- **Thread safety**: shared `HashMap`, `ArrayList` or `SimpleDateFormat`; check-then-act on shared state; mutable static fields.
- **Numbers**: `int` overflow, integer division, `new BigDecimal(double)`, `BigDecimal.equals` where `compareTo` was meant, money in `double`.
- **Exposed internals**: returning or storing a mutable collection or array without copying.
- **Streams**: reusing a consumed stream; side effects inside `map` or `filter`.
- **Unchecked casts and raw types**.
- **SQL built by concatenation** instead of a `PreparedStatement`.

## Not slop in Java

- Members used by reflection or a framework: Spring beans and injected fields, JPA entities, Jackson getters, setters and no-argument constructors, JUnit methods.
- Anything carrying an annotation that a framework or processor reads.
- `serialVersionUID`, `equals`, `hashCode`, `toString`.
- Public and protected members of a library.
- Generated sources, and `module-info.java`.
- Interfaces with one implementation that exist for testing or dependency injection the project uses.

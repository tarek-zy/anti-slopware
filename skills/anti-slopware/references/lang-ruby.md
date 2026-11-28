# Ruby checks

Use with [languages.md](languages.md).

## Build and tools

| Tool | Command | Finds |
|---|---|---|
| Syntax and warnings | `ruby -wc <file>` | Syntax errors, unused variables, unreachable statements, shadowed names |
| RuboCop | `bundle exec rubocop`, with the project's configuration | Useless assignments, shadowed exceptions, unsafe calls |
| Tests | `bundle exec rake test` or `bundle exec rspec` | Runtime behaviour |
| Brakeman | `brakeman`, in a Rails app | Injection, unsafe redirects, mass assignment |
| bundler-audit | `bundle audit` | Known vulnerable gems |

## Frequent bugs

- **Nil**: a method called on a result that can be `nil`: `find`, `first`, `[]`, `match`, a hash lookup. A `&.` chain that turns a real error into a silent `nil`.
- **Truthiness**: only `nil` and `false` are false. `0`, `""` and `[]` are true. `value || default` and `||=` where `false` is a valid value.
- **Rescue too wide**: `rescue Exception`; a bare `rescue` that swallows the error; `x = risky rescue nil`; `retry` with no limit; `return` inside `ensure`.
- **Shared default**: `Hash.new([])` and `Array.new(3, [])` hand out one object; a constant or default argument changed with `<<`.
- **Bang methods that return `nil`**: `uniq!`, `compact!`, `gsub!`, `chomp!`, `strip!` return `nil` when nothing changed. Chaining on them or using their result is a bug.
- **Changing a collection while iterating it**: `delete` or `<<` inside its own `each`.
- **Precedence**: `and`, `or` and `not` bind looser than `=`, so `ok = a and b` assigns `a`. `{ }` and `do ... end` attach to different calls.
- **String and Symbol keys**: `hash[:name]` on data parsed from JSON or YAML, where the keys are strings.
- **Unsafe input handling**: `eval`, `instance_eval`, `send`, `public_send` and `constantize` on input; `system`, backticks and `Kernel#open` with an interpolated string; `Marshal.load` and `YAML.unsafe_load` on data from outside; SQL built by interpolation.
- **Resources**: `File.open` without a block; a thread whose exception nobody reads; shared state changed from several threads without a `Mutex`.
- **Visibility**: `private` does not apply to `def self.` methods.
- **Numbers and time**: integer division (`5 / 2` is `2`), float equality, money in floats, `Time.now` where the application's time zone is meant.
- **Rails**: queries inside a loop; `update_all` and `delete_all` skipping validations and callbacks; request parameters passed to a model without strong parameters; `find_by` returning `nil` where `find` would raise.

## Not slop in Ruby

- Methods reached by name: `send`, `public_send`, `method_missing` with `respond_to_missing?`, `define_method`, callbacks given as symbols (`before_action :check`), Rake tasks, classes named in configuration and loaded with `const_get`.
- Classes and methods a framework finds by convention: Rails controllers, models, helpers, jobs, mailers, concerns, initialisers and migrations, methods called only from templates, and classes loaded by the autoloader that nothing requires.
- Methods Ruby calls itself: `initialize`, `to_s`, `inspect`, `<=>`, `==`, `hash`, `each` under `Enumerable`, `call`, `coerce`, `included`, `inherited`.
- Public methods and `attr_reader`, `attr_writer` and `attr_accessor` in a library, even with no caller in the repository.
- `self.` in front of a setter call. Without it, `name = value` creates a local variable.
- `dup` and `freeze` that protect a constant, a default or an argument from being changed.
- Magic comments such as `# frozen_string_literal: true`, and `# rubocop:disable` lines. They are instructions to tools, not comments to tidy.
- A `require` kept for what loading the file does: a monkey patch, a registration.

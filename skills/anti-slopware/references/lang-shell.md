# Shell checks

Use with [languages.md](languages.md).

The shebang decides the rules. `#!/bin/sh` means POSIX `sh`, which on many systems is `dash`, not Bash. A file with no shebang that other scripts source follows the shell of the scripts that source it.

## Build and tools

| Tool | Command | Finds |
|---|---|---|
| Syntax | `bash -n <file>`, or `sh -n`, `dash -n`, `zsh -n` to match the shebang | Syntax errors |
| ShellCheck | `shellcheck -x <files>` | Unquoted expansions, unused variables, Bash syntax under `sh`, tests that cannot work |
| checkbashisms | `checkbashisms <files>` | Bash-only syntax in `sh` scripts |
| Tests | The project's own: `bats`, `shunit2` or a test script | Runtime behaviour |

Run a script to check it only inside a throwaway directory, with every path argument pointing there. Never run one that deletes, moves, installs or deploys with real paths or with arguments left empty.

## Frequent bugs

- **Unquoted expansion**: `$var`, `$(cmd)` or `$@` without quotes where the value can hold spaces or glob characters, or be empty: `cp $src $dest`, `[ $x = y ]`, `for f in $(ls)`.
- **Delete or move through an empty variable**: `rm -rf "$dir/"*` or a glob built from a variable that can be unset or empty; no `${var:?}` and no check before it.
- **Unchecked `cd`**: `cd "$dir"` followed by a destructive command, with no `|| exit` and no `set -e`.
- **Hidden failure**: a command whose failure matters with no check and no `set -e`; a pipeline without `pipefail`, where only the last command counts; `local x=$(cmd)` and `export x=$(cmd)`, which return the status of `local` and `export`.
- **Lost exit status**: `$?` read after another command has run; `cmd || true` on a command that must succeed.
- **Bash syntax under `sh`**: `[[ ]]`, `==` inside `[ ]`, arrays, `function f`, `source`, `<<<`, `${var//a/b}`, `&>`, `echo -e` in a script whose shebang is `sh`.
- **Variable lost in a subshell**: a counter or flag set inside `cmd | while read ...` or `( ... )` and read after it.
- **Reading lines**: `read` without `-r`; `for line in $(cat file)`, which splits on spaces; a command inside a `while read` loop that swallows the loop's input, such as `ssh`.
- **Injection**: `eval`, `sh -c`, `bash -c` or a remote command string built from arguments, file names or file contents; a file name starting with `-` passed with no `--`.
- **Temporary files**: a fixed or guessable name such as `/tmp/out.$$` in place of `mktemp`; no `trap` that removes it on every exit.
- **Tests that do something else**: `[ $a > $b ]` writes a file named after `$b` and is always true; `=` on numbers, `-eq` on strings; `[ -n $x ]` unquoted is always true.
- **Secrets**: a password or token given as a command argument, where any user can list it, or printed by `set -x`.

## Not slop in shell

- A function or variable that looks unused in a file other scripts source, or that is called by a built name (`"cmd_$1"`), named in a config file or the docs, or used as a `trap` handler, completion function or hook.
- Variables the shell or a child process reads: `IFS`, `PATH`, `LC_ALL`, `PS4` and anything exported.
- `: "${VAR:=default}"` and `${VAR:-default}`. They are the script's settings.
- `|| true` and `|| :` after a command that may fail in normal use under `set -e`, such as `grep` finding nothing.
- An unquoted expansion that is split on purpose, usually marked with a `# shellcheck disable=` line. Quoting it changes behaviour.
- `# shellcheck` directives and the shebang line. They are instructions to tools, not comments to tidy.
- `( cd dir && cmd )`. The subshell keeps the directory change local.
- A helper repeated in a script that must run alone, such as an installer fetched with `curl` or a git hook. It cannot source a shared file.
- The text of a here-document. It is data, even when it looks like code.

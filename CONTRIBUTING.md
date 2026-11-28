# Contributing

Issues and pull requests are welcome. Pick an issue template when you open one, and comment on an issue before starting large work so nobody duplicates it.

Items in [ROADMAP.md](ROADMAP.md) are open for anyone to take.

## Good first contributions

- A language check: add `skills/anti-slopware/references/lang-<name>.md`, following an existing one such as `lang-go.md`, and add it to the table in `languages.md`. Wanted: Kotlin, Swift, SQL.
- A case the skill gets wrong: open an issue with the code before, what it did, and what it should have done.
- A new example under `examples/` with tests.

## Rules

- Every skill change comes with an example that shows it and tests that pass before and after.
- Keep `SKILL.md` files short. Detail goes in `references/`.
- Use only these frontmatter keys so skills stay portable: `name`, `description`, `license`, `metadata`, `allowed-tools`.
- Write the way the skills ask code to be written: no filler.

## Before you push

```
python3 examples/verify.py
scripts/check-sensitive.sh
```

`check-sensitive.sh` fails if tracked files or commit metadata contain an email address, a home-directory path, a hardware address or something shaped like a secret.

## Pull requests

Fork the repo, make your change on a branch, and open a pull request. Say what changed, why, and how you tested it. Keep one change per PR.

By contributing you agree that your work is released under the [MIT license](LICENSE) and that you follow the [code of conduct](CODE_OF_CONDUCT.md).

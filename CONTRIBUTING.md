# Contributing

## Good first contributions

- A language check: add `skills/anti-slopware/references/lang-<name>.md`, following `lang-c.md`.
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

Say what changed, why, and how you tested it. Keep one change per PR.

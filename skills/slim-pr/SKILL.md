---
name: slim-pr
description: Writes or trims a pull request description so a human can review the change quickly - what changed, why, how to test it, and the risks - with no filler and no claim the diff does not support. Also flags noise in the diff and pull requests too large to review. Use when the user asks to write, shorten, clean up or check a PR or merge request description, to prepare a branch for review, or types /slim-pr or /anti-slopware pr.
license: MIT
metadata:
  version: "0.1.0"
---

# slim-pr

A reviewer should learn in one minute what the change does, why, how to check it, and where it could hurt. Everything else in a description costs them time.

## 1. Gather

- The diff against the base branch (`git diff <base>...HEAD`), the list of changed files, and the commit messages.
- An existing description or draft, if the user gave one.
- The repository's PR template, if one exists (`.github/pull_request_template.md` and similar).

Read the diff itself. The description is derived from the diff. Commit messages and an existing draft are hints, and either can be wrong.

## 2. Check the diff for noise

Report these. Do not change the branch unless the user asks.

- **Unrelated changes**: formatting-only edits in files the change did not need, drive-by refactors, renames that serve another purpose.
- **Stray files**: debug output, logs, screenshots, editor and system files, local configuration.
- **Secrets**: a file or line that looks like a key, password or token. Say where it is. Never print its value, in the description or anywhere else.
- **Generated and lock files** changed with no dependency change to explain them.
- **Size**: more than about 400 changed lines of hand-written code, or several unrelated purposes in one branch. Propose a split and name the pieces.

## 3. Write

Use the repository's template if it has one. Otherwise use exactly these four parts:

```
**What**
<1 to 3 sentences: the change in behaviour, in terms a user or caller would notice. Not a list of files.>

**Why**
<The problem or request behind it, with the issue reference if there is one.>

**How to test**
<Exact commands or steps, and the result to expect.>

**Risks**
<Breaking changes, migrations, new or renamed settings, data changes, manual steps, anything not tested.>
```

Add **Notes for the reviewer** only when it saves them time: where to look first, which parts are mechanical.

Rules:

- **200 words at most**, unless the user asks for more.
- **Every statement is supported** by the diff or by something the user said. If you cannot support a claim from a draft, leave it out: performance numbers, coverage figures, "fully tested", "no breaking changes", "backward compatible". Check such claims against the diff. A draft that says "no breaking changes" above a renamed setting is wrong, and the description must say so under Risks.
- **Never trim these**, however short the description must be: breaking changes, migrations, new or renamed settings and environment variables, security-relevant changes, manual deployment steps, known gaps in testing, the issue reference.
- **Why is never invented.** If nothing states the reason, write `Why: not stated` and ask the user.
- **Risks is never left empty.** Write `None known` only after checking the diff for each item in the list above.
- **Leave out**: a file-by-file restatement of the diff, emoji, extra headings, "This PR" as an opener, a summary of the summary, checklists nobody will tick, thanks and sign-offs, generated-by lines, and filler words such as comprehensive, robust, seamless, enhance and leverage.
- Plain sentences. Put identifiers in backticks.

## 4. Deliver

Give the description in one block, ready to paste, or write it to the file the user names. Then, outside the description, list only what applies:

```
Noise in the diff:
  - <file or change>: <why it does not belong>
Claims left out:
  - "<claim>": <not supported by the diff | contradicted by <what>>
Split suggestion: <pieces, if the PR is too large>
```

Do not push, open, edit or comment on a pull request unless the user asks.

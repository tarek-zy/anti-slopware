---
name: code-docs
description: Documents a codebase so people and coding agents can find their way around it - a file map, how the parts fit together, the logic that is not obvious from the code, reference docstrings, and comments that are short, correct and useful. Learns the project's existing documentation system first and extends it; never imposes a template. Moves long comment blocks into doc files and leaves a pointer; never deletes information. Use when the user asks to document code, write or update docs, add a file map or architecture notes, fix or organise comments or docstrings, check whether docs are out of date, or types /code-docs or /anti-slopware docs.
license: MIT
metadata:
  version: "0.1.0"
---

# code-docs

Code says what happens. Documentation says where things are, how they fit together and why they are the way they are. Without it, every reader, human or agent, has to rebuild that understanding from scratch, and a reviewer cannot tell an intended change from an accident.

Two rules shape everything here:

1. **The project's own documentation system is the standard.** Learn it, extend it, improve it where it falls short. Never drop in a template.
2. **Never lose information.** A comment is removed only when what it said now lives somewhere a reader will find it.

## 1. Read the request

| Argument | Meaning | Default |
|---|---|---|
| `report` | Audit: what exists, what is missing, what is wrong. Change nothing. | on |
| `write` | Make the changes, after showing the plan | off |
| a path | Folder, file or doc to work on | the code in the current changes |
| `all` | The whole project, one area at a time | off |

This skill changes comments, docstrings and documentation files. It never changes what the code does.

## 2. Learn how this project documents itself

Do this before judging anything. Record what you find at the top of the plan.

- **Where docs live**: `README`, a `docs/` folder, a wiki, a docs site, files beside the code. Which tool builds them (MkDocs, Sphinx, Docusaurus, TypeDoc, rustdoc, dartdoc) and its navigation file.
- **What kinds exist**: overview, setup, file map or project layout, architecture, per-feature docs, decision records, how-to guides, reference, changelog, files written for coding agents (`AGENTS.md`, `CLAUDE.md` and similar).
- **Docstring and comment style**: the convention in use (Google, NumPy, reST, JSDoc, Javadoc, XML docs, doc comments), how much the project comments, which language it writes in, its tone.
- **Formats and names**: heading style, file naming, how docs link to code and to each other, any front matter.
- **How current it is**: which docs match the code and which have drifted.

Then decide, for each thing you want to add, where this project would put it. A new page goes in the existing docs folder and into its navigation. A file map goes where the project already keeps one. Use the existing docstring style even if you prefer another.

**No system at all**: propose the smallest one that fits the project's size, and get agreement before creating it. A ten-file project needs a good README, not a docs site.

**A system that falls short**: say what is missing and propose the improvement inside the existing system.

## 3. The layers

Good documentation answers different questions at different depths. Check each layer; add only what is missing and worth having for this project.

| Layer | Answers | Typical home |
|---|---|---|
| **File map** | What lives where? Where do I start? | A "project layout" section or page |
| **How it fits together** | What are the main parts and how does data move between them? | An architecture or overview page |
| **Logic** | How does this non-obvious piece work, and why this way? | A page per feature or module, a decision record, or a docstring when a few lines cover it |
| **Reference** | What does this function, class or endpoint take and return? | Docstrings in the project's style |
| **Comments** | What must I know right here, on this line? | Short comments in the code |
| **Running it** | How do I set up, run and test? | README or a setup page |

A file map lists folders and important files with one line each on what they are for, names the entry points, and says where to add new things. It is not a directory listing.

## 4. Comments

Comments are part of the documentation. Organise them; do not strip them.

- **Keep** every comment that carries something the code does not: why, a constraint, a unit, a warning, an example, a link to an issue.
- **Long explanation in the code** (more than about ten lines): move the full text to a doc file in the project's docs, and leave a short comment that states the key point and points to it: `# Proration uses actual days in the year. See docs/billing.md#proration.` Everything the long comment said must be in the doc.
- **Wrong or stale comment**: check it against the code. If the code is clearly the truth, correct the comment. If you cannot tell which is right, do not guess: report it as a question.
- **Comment that only repeats the code**: improve it to say why, or fold it into the function's docstring. Remove it only if nothing would be lost.
- **Scattered comments on one topic**: gather them into one comment or docstring where the reader meets the topic first.
- **Edit narration** ("changed this to use the new API", "removed the old check"): that is history, and history belongs in the commit message. Remove it once you have checked it says nothing about the code as it is now.

Never touch:

- Directives a tool reads: `noqa`, `type: ignore`, `eslint-disable`, `pragma`, `fmt: off`, `go:generate`, `go:embed`, build tags, shebang lines, encoding lines.
- Licence and copyright headers.
- `TODO`, `FIXME`, `HACK` and `XXX` notes. List them in the report.
- Commented-out code. That is dead code, not documentation; the `anti-slopware` skill handles it.

## 5. Rules for what you write

- **Verify every statement against the code.** Read the function before describing it. Documentation that is wrong is worse than none.
- **Never invent the why.** If nothing states the reason for a decision (code, comments, commit messages, issues, existing docs), write what the code does and list the missing reason as a question for the user.
- **Document what is not obvious.** Do not restate code in prose. A page that says nothing a reader could not see in ten seconds should not exist.
- **Point to code by path and name**, never by line number. Line numbers rot.
- **Every pointer must resolve.** A comment that names a doc file or section must name one that exists.
- **Historical records stay as written**: decision records, changelog entries, release notes. Add a new one; do not rewrite an old one.
- **Docstrings can be behaviour.** A docstring used as command-line help, shown by an API, or containing a doctest is read by the program. Change it only with care, and run the doctests and the help output afterwards.
- **Docs for agents**: if the project keeps a file for coding agents, keep it short and make it point to the file map and the key docs. Create one only if the user asks.

## 6. Plan

```
code-docs: <project's system in one or two lines>

Missing:
  - <layer>: <what>, to go in <where this project would put it>
Wrong or stale:
  - <file>: says <x>, code does <y>
Comments to organise:
  - <file>: <long block to move | scattered | repeats the code>
Questions (reasons nobody wrote down, or doc and code disagree and it is unclear which is right):
  - <question>
Left alone: <what looks odd but follows the project's convention>
```

With `report`, stop here.

## 7. Write (only with `write`, after the plan is shown)

Work one area at a time. After each:

- Run the project's tests and its docs build if it has one.
- Confirm no code changed: only comments, docstrings and documentation files differ.
- Check every new pointer and link resolves, and every new page is in the navigation.

## 8. Working with the other skills

- After `organize` moves files, update the file map and any doc that names the old path.
- `anti-slopware` leaves comments alone. Comment work happens here.
- In guard mode, new code is documented in the project's style as it is written, and a new file is added to the file map.
- `slim-pr` and `review-map` can point reviewers to the pages this skill keeps current.

## 9. Report

```
code-docs: <files changed> files, <docs added> pages added, <docs updated> updated

Added: <page or docstrings>: <what it covers>
Corrected: <file>: <what was wrong>
Moved to docs: <comment block> -> <doc file>, pointer left at <file>
Questions for you: <list>
TODO and FIXME notes found: <n> (<files>)
Checks: <tests, docs build, doctests> <before> -> <after>
Code unchanged: <how you confirmed it>
```

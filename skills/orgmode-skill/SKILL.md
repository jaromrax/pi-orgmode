---
name: orgmode-skill
description: Maintain and update .org documents in the conventions of org-mode of emacs. You know how to prepare texts with export preparation to latex, you know, how to operate with presentations using beamer in org-mode.
license: MIT
---

# Org-mode skill (joint)

This is the entry point. Pick a **branch** from the task, then follow that file. Do not mix article headers with beamer slide templates.

## Branches

| Task | Branch file | What it covers |
|------|-------------|----------------|
| Beamer slides / presentation | `SKILL_presentation.md` | Slide regimes, MARKER lines, page templates (C1T, C2TI, …), overlays, compile |
| General org document (not a presentation) | `main_battle_tested_org_SKILL.md` | Article/PDF export: isotopes, `\nbsp{}` / `\mu{}m`, entities, geometry, EXAMPLE blocks |
| Org-document **tables** (named, formula-driven, PDF) | `SKILL_org_doc_tables.md` | Startblock, F8, helper Babel, named tables, minipage, `remote()`, decimal align (`S` **or** longtable+`d{n,m}`), sidewaystable. Examples: `org_doc_tables.org`, `org_doc_longtable.org` |
| Org-document **literate / coding** | `SKILL_org_doc_literate.md` | Minted `bash`/`python`/`asc` colours, noweb `<<name>>` def→caller, PROPERTY header-args, tangle, `#+CALL`, sessions. Template: `template_literate.org` |

Document line is complete for now (general + tables + literate). Later split, not written: booklet.

Pygments (minted): `uv tool install Pygments` or `apt install python3-pygments`; PDF export needs `--shell-escape`. Details: literate branch + `tramp_and_install.md`.

## How to choose

- User wants slides, frames, beamer, one-slide mock-up, or a `.org` that exports to a presentation PDF → **presentation** branch. Also read `tramp_and_install.md` for font, TeX packages, and TRAMP.
- User wants a normal `.org` (article, notes, isotopes, `\nbsp{}` / `\mu{}m`, LaTeX/PDF that is **not** beamer) → **org-document** branch.
- User wants named tables, `TBLFM` / `remote()`, minipages, longtable/dcolumn decimals, sidewaystable, or F8 buffer recalc → **org-document** plus the **tables** sub-branch.
- User wants literate programming, noweb `<<name>>`, tangle, minted src (python/bash/asc), `#+CALL`, or a lab notebook that exports code → **org-document** plus the **literate** sub-branch. Start from `template_literate.org`.
- Unclear → ask which branch. Default is org-document unless they mention slides/beamer.

## Shared vs not shared

- Org syntax, Emacs, LaTeX export, isotope `\null^{…}` / `\nul^{}` can appear in both.
- Headers are **not** shared: presentation uses the beamer skeleton in `SKILL_presentation.md`; documents use the article header in `main_battle_tested_org_SKILL.md`; literate copies minted/noweb from `template_literate.org`.
- Do not put `geometry` article margins, table `<r>` cookies, minipage table pairs, `startblock` Babel autorun, or literate `\setminted` / noweb PROPERTY into a beamer file unless the user asks.

## When to use me

When working with org-mode: a presentation, a general document, a table-heavy document, or a literate/coding document. Load the matching branch skill before editing.

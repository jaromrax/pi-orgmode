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
| General org document (not a presentation) | `main_battle_tested_org_SKILL.md` | Article/PDF export: isotopes, entities, tables, geometry, EXAMPLE blocks |

Later sub-branches of the **document** line (not written yet): booklet, tables, programming languages.

## How to choose

- User wants slides, frames, beamer, one-slide mock-up, or a `.org` that exports to a presentation PDF → **presentation** branch. Also read `tramp_and_install.md` for font, TeX packages, and TRAMP.
- User wants a normal `.org` (article, notes, tables, isotopes, LaTeX/PDF that is **not** beamer) → **org-document** branch.
- Unclear → ask which branch. Default is org-document unless they mention slides/beamer.

## Shared vs not shared

- Org syntax, Emacs, LaTeX export, isotope `\null^{…}` / `\nul^{}` can appear in both.
- Headers are **not** shared: presentation uses the beamer skeleton in `SKILL_presentation.md`; documents use the article header in `main_battle_tested_org_SKILL.md`.
- Do not put `geometry` article margins or table `<r>` cookies into a beamer file unless the user asks.

## When to use me

When working with org-mode: either a presentation or a general document. Load the matching branch skill before editing.

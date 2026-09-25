---
name: orgmode-skill
description: Maintain and update .org documents in the conventions of org-mode of emacs. You know how to prepare texts with export preparation to latex, you know, how to operate with presentations using beamer in org-mode.
license: MIT
---

# AGENTS_org_mode.md — org-mode lessons learned (this project)

This is the **general org-document** branch of the org-mode skill (not presentations). Joint entry point: `SKILL.md`. Beamer slides: `SKILL_presentation.md`.

Practical rules established while writing `.org` with an option for LaTeX/PDF export.
User preferences here override generic org defaults.

Later this branch may split further (booklet, tables, programming languages).

## 1. Isotope superscripts (indices)

- Write isotopes as `\null^{241}Am`, `\null^{57}Co`, `\null^{60}Co`,
  `\null^{137}Cs`, `\null^{88}Y` — **no `$...$`** around them.
- `\null` supplies the (empty) base LaTeX needs for a leading `^{...}`;
  without it a table cell or line starting with `^{...}` breaks.
- Keep `_:nil` in `#+OPTIONS` (see header below) — it was added for the
  index handling; do not remove it.
- Applies **everywhere**: table cells AND running prose.

## 2. `$` usage

- `$\pm$` is fine and stays as-is (tables + prose).
- `$\approx$` is NOT wanted — use the bare org entity `\approx{}`
  (see next section).
- No `$^{...}$` isotope math anywhere (verified with grep for `$^{`).

## 3. `\approx` (and entities in general)

- Write `\approx{}` — no surrounding `$`.
- The `{}` terminates the entity name so a following digit parses correctly:
  `(\approx{}16.8 half-lives)`, not `(\approx16.8 ...)`.
- Same rule generalizes: any `\entity` directly before a letter/digit gets `{}`.

## 4. Page margin (top)

- Decrease via the geometry package in the header:
  `#+LATEX_HEADER: \usepackage[top=2cm]{geometry}`
- Placed right after `#+LATEX_CLASS_OPTIONS`, before other packages.
- Tighten further with `top=1.5cm` if asked; adjust other sides only on request.

## 5. Table alignment

- Right-align a column for **export** with an alignment-cookie row directly
  under the header hline, e.g. for column 1:
  `| <r> | | | |` (one `<r>`, remaining cells empty = defaults kept).
- The cookie row is not exported; it drives the LaTeX `tabular` alignment.
- Buffer display: run `C-c C-c` (`org-table-align`) on the table to
  re-justify cells in the source after edits.
- Only the isotope column is `<r>` here; numeric columns were left at defaults.

## 6. Current header (reference, 2026-09-10)

```org
#+OPTIONS: toc:nil _:nil  num:t H:2
#+LATEX_CLASS: article
#+LATEX_CLASS_OPTIONS: [a4paper,11pt]
#+LATEX_HEADER: \usepackage[top=2cm]{geometry}
#+LATEX_HEADER: \usepackage{booktabs}
#+LATEX_HEADER: \usepackage{siunitx}
#+LATEX_HEADER: \sisetup{separate-uncertainty=true, per-mode=symbol}
```

## 7. Verification checklist (before calling a file done)

- No `$^{` anywhere: search for `$^{`.
- No `$\approx$`: search for `$` around `\approx`.
- Every isotope cell/prose mention matches `\null^{...}Xy`.
- No bare `^` anywhere except `\null^{...}` isotope marks: search for `^`.
- `<r>` cookie row present under each table header.
- `_:nil` still in `#+OPTIONS`; geometry header still present.
- EXAMPLE blocks fit the page: with the default text width, tt fits ~60 cols at normalsize, ~73 at footnotesize, ~85 at scriptsize; check longest line (e.g. awk) and narrow art to <=80 when wrapped in scriptsize.

## 8. Emacs display + verbatim figures (added 2026-09-10)

- Inline-image width in Emacs is driven by `#+ATTR_ORG: :width <px>`
  (pixels), independent of `#+ATTR_LATEX`. Put both lines above
  `[[file:...]]` so the figure is sized in Emacs and in PDF export alike.
  `iimage-mode` ignores all of this — view with `C-c C-x C-v`
  (`org-toggle-inline-images`); window-following width (Olivetti-safe)
  lives in init.el via `org-image-actual-width`, not in the org file.
- ASCII schematics go in `#+BEGIN_EXAMPLE` / `#+END_EXAMPLE`: exported
  verbatim (monospace), immune to entity and subscript interpretation.
  Project convention: captioned figure first, ASCII fallback after it.
- `[[file:*.md]]` links to sibling notes (e.g. pre-experiment-findings.md)
  are fine inline.

## 9. Shrinking wide EXAMPLE blocks (added 2026-09-10)

- Verbatim ignores text width and overflows the PDF margin. Fix in two parts:
  wrap the block in a size group — `#+LATEX: {\scriptsize` before
  `#+BEGIN_EXAMPLE`, `#+LATEX: \par}` after `#+END_EXAMPLE` — and redraw
  the ASCII art narrow enough to fit (rule of thumb: <=80 columns under
  scriptsize on the default A4 text width).
- Keep the art buildable: fixed cell widths joined by `|` pipes, verified by
  script (assert on every line length), not by eye.

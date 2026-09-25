---
name: orgmode-skill-tables
description: Org-document variant for named, formula-driven tables that export to PDF. Use with the general org-document branch, not beamer.
license: MIT
---

# Org-document tables (sub-branch)

This is a **tables** variant of the general org-document line. Joint entry: `SKILL.md`. Article/PDF habits that are not table-specific (`\null^{…}`, `\nbsp{}`, `\mu{}m`, geometry): `main_battle_tested_org_SKILL.md`. Literate src/noweb: `SKILL_org_doc_literate.md`.

Worked examples:
- `org_doc_tables.org` — named tables, Babel, `remote()`, minipage, siunitx `S`
- `org_doc_longtable.org` — longtable + dcolumn `d{n,m}`, sidewaystable, prose entities

Use this branch when the `.org` is built around named tables, Babel helpers, `TBLFM` / `remote()`, longtable/dcolumn, or PDF export — expense sheets, rate conversions, gamma/energy tables, side-by-side numeric summaries.

Do not mix with beamer headers.

## 1. Startblock (no y/n on every eval)

Put a named emacs-lisp block near the top. It turns off Babel confirmation so F8 / table formulas that call source blocks do not stop for `y/n` on every iteration.

```org
#+NAME: startblock
#+BEGIN_SRC emacs-lisp :exports none
(setq org-confirm-babel-evaluate nil)  ;;; DANGEROUS AUTORUN
#+END_SRC
```

- `:exports none` — helper only, never in the PDF.
- Dangerous on untrusted files; fine for a personal buffer you recalculate often.
- Evaluate it once per session (or let the first F8 pass hit it) before iterating tables.

## 2. F8 — recalculate every table in the buffer

The user should have **F8** bound to recalculate (preferably **iterate**) all tables in the buffer. `remote()` chains need a stable pass, not a single recalc.

Typical binding (init.el / local):

```elisp
(define-key org-mode-map (kbd "<f8>") #'org-table-iterate-buffer-tables)
```

`org-table-recalculate-buffer-tables` is one pass; `org-table-iterate-buffer-tables` repeats until values stop changing. Prefer iterate when tables feed each other.

Workflow: startblock → F8 (seamless, no confirmations) → export PDF.

## 3. Helper source blocks do not export

Fetch rates, parse dates, or any other lookup lives in a **named** Babel block with `:exports none`. It is not part of the PDF; tables call it.

```org
#+NAME: calc-kurz
#+header: :eval yes
#+begin_src python :var date="<2026-07-21 Tue>" :results output :exports none
# ... fetch / compute ...
print(value)
#+end_src
```

From `TBLFM`, call it with `org-sbe`:

```org
#+TBLFM: @2$2..@3$2='(org-sbe calc-kurz (date $$1))
```

The example fetches a CNB EUR rate; the pattern is the same for any helper.

## 4. Every table has a `#+NAME`

Name is required for `remote()` and for captions you can point at.

```org
#+NAME: mytotam
#+ATTR_LATEX: :placement [H] :align S
#+CAPTION: Mytne tam EUR
|  4.8 |
...
#+TBLFM: @>$1=vsum(@1..@-1)
```

Use stable, short names (`mytotam`, `dieseleur`, `total`).

## 5. Minipage — tables side by side

Wrap each table in `minipage` at half text width. `ATTR_LATEX :options` belongs on the minipage, table `ATTR_LATEX` on the table.

```org
#+ATTR_LATEX: :options {0.5\textwidth}
#+begin_minipage
#+NAME: lefttab
#+ATTR_LATEX: :placement [H] :align S
#+CAPTION: Left
| ... |
#+end_minipage
#+ATTR_LATEX: :options {0.5\textwidth}
#+begin_minipage
#+NAME: righttab
#+ATTR_LATEX: :placement [H] :align S
#+CAPTION: Right
| ... |
#+end_minipage
```

Keep the two minipages adjacent (no blank line between `#+end_minipage` and the next `#+ATTR_LATEX`) so they sit on one row.

## 6. `remote()` — pull a cell from another table

Reference a named table instead of copying numbers. Last row, first column:

```org
remote(mytotam,@>$1)
```

Last row, last column (useful for a grand-total sheet):

```org
remote(mytocelkem,@>$>)
```

In `TBLFM` (example: fill a column from two source tables, then sum):

```org
#+TBLFM: @2$3=remote(mytotam,@>$1)::@3$3=remote(mytozpet,@>$1)::@>$4=vsum(@2..@-1);%.2f
```

`@>` = last row, `$1` / `$>` = first / last column, `@-1` = row above the hline for `vsum` ranges.

## 7. Decimal alignment — two working recipes

Do **not** invent a third stack. `colortbl`, `tabularray`, and “full” siunitx table kits are large and **not** a solved decimal-alignment habit here. Pick one of the two examples we already have.

### A. siunitx `S` — money / rates (`org_doc_tables.org`)

Load siunitx. Then:

- `l` — left-aligned text (labels, dates)
- `r` — right-aligned text
- `c` — centered
- `S` — siunitx column, decimal-point alignment (not org `<r>` cookies)

- one numeric column: `:align S`
- label + one number: `:align l S`
- label + three numbers: `:align l S S S`

```org
#+ATTR_LATEX: :placement [H] :align l S
#+CAPTION: Celkový součet v CZK
```

### B. longtable + dcolumn `d{n,m}` — scientific tables (`org_doc_longtable.org`)

**longtable works well for decimal alignment.** Header:

```org
#+LATEX_HEADER: \usepackage{booktabs,dcolumn}
#+LATEX_HEADER: \newcolumntype{d}[1]{D{.}{.}{#1}}%
```

`d{7,3}` = 7 digits before the point, 3 after. `d{5,3}` likewise. Mix with `r`, `l`, `c` and `|` rules:

```org
#+NAME: table1
#+CAPTION: Table of gamma energies, intensities and halflives
#+ATTR_LATEX: :environment longtable
#+ATTR_LATEX: :placement [H!]
#+ATTR_LATEX: :align r|l|d{7,3}|d{5,3}|c|c
```

Several `#+ATTR_LATEX:` lines on one table are fine (`:environment`, `:placement`, `:align`).

`:placement [H]` / `[H!]` keeps the float here (needs `float` if the class does not define `H`).

Org `<r>` cookies (general-document skill) remain for buffer display / simple right-align — they are not a substitute for `S` or `d{n,m}` when the PDF must line up on the decimal point.

## 7b. Sidewaystable

Wide tables: `sidewaystable` + smaller font. Needs `rotating` (org usually loads it for this float type).

```org
#+NAME: tblSideways
#+CAPTION: A sidewaystable
#+ATTR_LATEX: :font \footnotesize :float sidewaystable :placement [H]
```

## 8. Prepared for PDF export

Keep the file export-ready. Two header families (do not merge blindly):

**Formula / rate sheets** (`org_doc_tables.org`) — LuaLaTeX, siunitx `S`:

```org
#+TITLE: ...
#+OPTIONS: title:nil
#+OPTIONS: toc:nil
#+OPTIONS: ^:nil
#+OPTIONS: _:nil
#+LATEX_COMPILER: lualatex
#+LaTeX_HEADER: \usepackage{minted} \usepackage{bookmark} \usepackage{xcolor}
#+LATEX_HEADER: \makeatletter \@ifpackageloaded{geometry}{\geometry{margin=2cm}}{\usepackage[margin=2cm]{geometry}} \makeatother
#+LATEX_HEADER: \usepackage{siunitx}
```

**Scientific longtable** (`org_doc_longtable.org`) — parskip, dcolumn, optional `tex:dvipng`:

```org
#+OPTIONS: toc:nil
#+OPTIONS: num:nil
#+OPTIONS: tex:dvipng
#+LATEX_CLASS_OPTIONS: [a4paper,12pt]
#+LATEX_HEADER: \usepackage{parskip} \usepackage[margin=2cm]{geometry} \usepackage{booktabs,dcolumn}
#+LATEX_HEADER: \newcolumntype{d}[1]{D{.}{.}{#1}}%
```

Leave `# #+LATEX_HEADER: \usepackage{utf8}` and biblatex commented unless asked.

- Helper Babel: `:exports none`
- Tables: names, captions, `ATTR_LATEX`, `TBLFM` when formulas exist
- Recalc with F8 until `remote()` / `org-sbe` values settle, then export
- Table footnotes: `*\footnotemark[1]` in a cell is fine; define the mark in the surrounding text

## Checklist

- [ ] `startblock` present, `:exports none`, confirmations off (if Babel / F8 is used)
- [ ] F8 → `org-table-iterate-buffer-tables` (user Emacs)
- [ ] Helper src named, `:exports none`, not in the PDF
- [ ] Every table has `#+NAME:`
- [ ] Side-by-side pairs use adjacent `minipage`s
- [ ] Cross-table numbers go through `remote(name,@>…)` — no pasted totals
- [ ] Decimal align is **one** recipe: `S` (siunitx) **or** longtable + `d{n,m}` (dcolumn) — not tabularray/colortbl for decimals
- [ ] Header matches that recipe (siunitx **or** dcolumn `\newcolumntype`)
- [ ] Wide tables: `:float sidewaystable` + `:font \footnotesize` when needed
- [ ] Prose units: `\nbsp{}`, `\mu{}m`, `\null^{…}` (general-document skill)

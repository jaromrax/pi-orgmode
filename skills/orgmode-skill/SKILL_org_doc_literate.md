---
name: orgmode-skill-literate
description: Org-document variant for literate programming — named src blocks, noweb <<name>>, minted bash/python/asc, tangle, PDF. Not beamer.
license: MIT
---

# Org-document literate programming (sub-branch)

This is the **coding / literate** variant of the general org-document line. Joint entry: `SKILL.md`. Prose/PDF habits: `main_battle_tested_org_SKILL.md`. Tables (if the same file has longtable): `SKILL_org_doc_tables.md`.

**Source of truth:** `template_literate.org`. Copy its header; do not invent minted styles.

Use this branch when the `.org` is a lab notebook / literate program: Python (often ROOT), bash, terminal dumps (`asc`), noweb expansion, tangle, PDF with minted.

Do not mix with beamer headers.

## 1. Three src languages only (for PDF colour)

Minted styles live in the **document header** (the file’s “ini”), not in each block. Emacs/Pygments must be installed (`python3-pygments` or `uv tool install Pygments`; export with `--shell-escape`). Map these three:

| Lang | Role | Minted (from template) |
|------|------|-------------------------|
| `python` | code | `style=pastie`, `bgcolor=codecolor`, `frame=topline`, `breaklines` |
| `bash` | shell | `style=autumn`, `bgcolor=shellcolor`, `frame=topline`, `breaklines` |
| `asc` | terminal dump (not a real language) | `style=vim`, `bgcolor=ascicolor`, `frame=lines`, `breaklines` |

Colours (keep as in the template):

```latex
\definecolor{shadecolor}{rgb}{0.96, .96, .96}  % EXAMPLE / RESULTS verbatim
\definecolor{ascicolor}{rgb}{.97, 1., .9}
\definecolor{codecolor}{rgb}{.97, .97, .99}
\definecolor{shellcolor}{rgb}{.95, .97, .97}
```

```latex
\setminted[bash]{style=autumn,bgcolor=shellcolor,breaklines,frame=topline}
\setminted[python]{style=pastie,bgcolor=codecolor,frame=topline,framesep=2mm, breaklines}
\setminted[asc]{style=vim,bgcolor=ascicolor,breaklines,frame=lines,framesep=2mm}
```

`EXAMPLE` / Babel `RESULTS` use a **redefined `verbatim`** (framed + `shadecolor`). Do not start an `EXAMPLE` block with a blank line.

Optional on `asc`: `#+ATTR_LATEX: :options numbers=both`.

Do not add `colortbl` / random minted langs unless asked — colours will not match.

## 2. File-level `#+PROPERTY` (python vs bash)

From the template (keep these defaults):

```org
#+PROPERTY: header-args:python :session *python_session* :results replace output :exports none :tangle yes :comments both :noweb yes :eval never-export
#+PROPERTY: header-args:bash :session *bash_session* :results replace  output :exports results :eval never-export
```

Meaning:

- **`:eval never-export`** — PDF does not re-run code; you run in Emacs (`C-c C-c`).
- **python `:exports none`** — definition blocks stay out of the PDF; override **one** run block with `:exports both` or `code`.
- **`:noweb yes`** on python — later blocks may splice `<<name>>`.
- **`:session *python_session*`** — one interpreter; debug in that buffer; **kill the buffer to restart**.
- **`:tangle yes`** + **`:comments both`** — `C-c C-v t` writes a `.py` next to the org file.
- bash defaults to **`:exports results`**.

Global vars (activate with `C-c C-c` on the PROPERTY line, then verify with a small print block):

```org
#+PROPERTY: header-args :var runnum=141
```

Pass a named table into python:

```org
#+NAME: TAB
| a | b |
| 1 | 2 |

#+NAME: a2_functions
#+HEADER: :var tab=TAB
#+begin_src python
```

## 3. Noweb: definitions block → caller via `<<name>>`

Name **every** block. A later block **includes** an earlier one by noweb, it does not copy-paste.

```org
#+NAME: a1_definitions
#+begin_src python
import datetime as dt
print(f"*********** START_______{runnum}_________________________", dt.datetime.now())
# imports …
print(f"i... a1 ...  done ")
#+end_src

#+NAME: a2_functions
#+HEADER: :var tab=TAB
#+begin_src python
<<a1_definitions>>
def fu(r):
    print(f"RUN={r}")
print(f"i... a2 ...  done ")
#+end_src

#+NAME: a3_run
#+HEADER: :exports both
#+begin_src python
<<a2_functions>>
fu(runnum)
print(f"i... a3 ...  done ")
#+end_src
```

Rules:

- **`<<a1_definitions>>`** is the first line of the *next* block that needs those defs.
- Because noweb is on, expanding `a2` also expands `a1`. **`a3_run` is the only block you need to run** for the chain, and the only one to export (`:exports both`).
- Keep defs at **`:exports none`** (file default) so the PDF does not print the same imports three times. Use `:exports code` on a def block only if you *want* that snippet in the paper.
- RESULTS of the whole chain are noisy — do not export them by default; export by hand / `:exports both` on the run block only.
- Start/end prints (`i... a1 ... done`) make the session buffer readable.

## 4. Confirmations off (same idea as tables `startblock`)

```org
#+begin_src elisp :exports code
(setq org-confirm-babel-evaluate nil)  ;;; DANGEROUS AUTORUN
#+end_src
```

## 5. `#+CALL` and inline src

Named block with `:results none :exports code`, then in prose:

```org
#+CALL:hi() :exports results
```

`C-c C-c` on the CALL line. Exports the RESULTS, not a second copy of the code.

Inline (seamless in text / PDF):

```org
src_python[:exports results :results replace output]{print(dt.datetime.now())}
```

## 6. Organisation

- **One main file**; other files `#+INCLUDE:` headless (see template stub `Included texts`).
- Temp/Babel junk may stay in the working dir; **exported images → `./images/`**.
- Histograms: **jpg not png** (png save caused export problems).
- `#+NAME:` on every src, table, and CALL target.
- venv assumed: `cd ~/.venv; uv venv emacs; source emacs/bin/activate` (see `prepare_venv` in the template).
- Prerequisites block in the template: `python3-pygments`, `python3-jupyter-client`; PDF needs minted + shell-escape.

## 7. Keys

| Key | Action |
|-----|--------|
| `C-c C-c` | run this block / activate PROPERTY / CALL |
| `C-c '` | edit src in a language buffer; same to quit |
| `C-c C-v C-b` | run **all** src in the buffer |
| `C-c C-v t` | **tangle** full doc (`org-babel-tangle`) |

Open `*python_session*` / python output to debug; kill it to restart.

## 8. PDF header extras (already in the template)

Copy from `template_literate.org`, do not rebuild: `minted`+`bookmark`, `framed`/`xcolor`/`verbatim` rewrite, `enumitem` tight lists, `parindent=0`, `geometry` ~1.7–2 cm, `raggedbottom`, `placeins`, quote → `\itshape\bf`, `booktabs`/`dcolumn` if tables appear.

Longtable decimal recipe is the same as the tables branch (`d{n,m}`). Prefer that over tabularray/colortbl.

`#+OPTIONS:` in the template: `toc:nil num:nil`, title/date/author as there. `^:t` in this file (indices in titles); isotope-heavy articles still use `_:nil` / `^:nil` from the general-document skill — do not blindly copy `^:t` into those.

## Checklist

- [ ] Header copied from `template_literate.org` (minted bash / python / asc + colours)
- [ ] Src langs are `python`, `bash`, or `asc` — not ad-hoc names
- [ ] python PROPERTY: session, noweb yes, exports none, eval never-export, tangle yes
- [ ] Defs named; callers start with `<<that_name>>`; one run block `:exports both`
- [ ] No duplicate code in PDF (`:exports none` on noweb ingredients)
- [ ] Global `:var` PROPERTY activated with `C-c C-c`
- [ ] Images in `./images/`, jpg for plots
- [ ] EXAMPLE blocks have no leading blank line
- [ ] Babel confirmations off only on trusted files

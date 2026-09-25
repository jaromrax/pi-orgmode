---
name: org-presentation-slide
description: "Create or edit org-mode file with presentation slides."
license: MIT
compatibility: opencode
---

## What I do

This is the **presentation** branch of the org-mode skill. Joint entry point: `SKILL.md`. General (non-slide) org documents: `main_battle_tested_org_SKILL.md`.

 Org-mode is a mode in emacs. The presentations are done using latex and beamer.

### Creating the new org file with a presentation.

 The user will tell if we work on
  - one page mock-up or - ONE SLIDE regime - only one slide is between MARKER lines
  - full presentation - ALL SLIDES regime - all slides are included

- The template for full presentation is `template_presentation.org`
- The template for one slide /  mock-up slide  is `template_presentation_single_page.org`

To start with - copy one of these to the new file and we start the new presentation.

Host Emacs / VM install notes (TRAMP, TeX packages, Sora font) live in `tramp_and_install.md`.

### Document header skeleton

Every presentation org file should include this header block (templates already have it; keep it if you write a file by hand):

```
#+STARTUP: showeverything
#+OPTIONS: TeX:t LaTeX:t toc:nil skip:nil d:nil todo:t pri:nil tags:not-in-toc title:nil
#+LATEX_COMPILER: xelatex
#+LATEX_CLASS:
#+LATEX_HEADER:
#+BEAMER_HEADER:
```

`#+LATEX_COMPILER: xelatex` is mandatory because `fontspec` requires XeLaTeX, not pdflatex.

### Required image files

The first and last slides use background and logo images. When creating a new presentation from the template, copy these files from the skill directory to the presentation directory:

- `logosmall.png` — small logo for the footline (every slide)
- `logofull.png` — full logo for the first and last slides
- `bg_main.jpg` — background image for the first and last slides

```
cp .opencode/skills/org_presentation/logosmall.png .
cp .opencode/skills/org_presentation/logofull.png .
cp .opencode/skills/org_presentation/bg_main.jpg .
```

### .gitignore for LaTeX auxiliary files

After compiling, LaTeX generates auxiliary files that must not be committed. Ensure the project `.gitignore` includes:

```
# LaTeX auxiliary files
*.toc
*.snm
*.nav
*.log
*.aux
*.out
_minted-*
```

Content slides have no background image — only the first and last frames use `bg_main.jpg`.




### First and last slides

 They are given in the template `template_presentation.org` as
 - The very first frame
 - The very last frame

No first and last are given in  `template_presentation_single_page.org`


### Inserting a slide

 Both templates contain two MARKER lines

`# ================================ END OF THE INITIAL PART ===============`
and
`# ================================ START OF THE CLOSING PART =============`

The slides are blocks of text that can be inserted only between these two lines.

#### Two modes to include the text of pages/slides

1) FULL EDIT mode: full edit the text of slide(s) in the main file, text it always between the MARKER lines. Useful when working on one slide.

2) INCLUDE mode :generate a page into a standalone file (e.g. `s01_concept.org`) and include this file between the MARKER lines (e.g. `#+INCLUDE: "s01_concept.org"`). This method is useful for final display and fine tuning, where all slides one-by-one are included using the command `#+INCLUDE:`.

Typical workflow (optional, not mandatory):

- prepare slides one by one in ONE SLIDE regime, FULL EDIT mode
- save each finished slide to a separate file
- then switch to ALL SLIDES regime, INCLUDE mode

You may stay in either regime/mode for the whole job if that is simpler.

### Sections levels in org file:

 - Section level 1 '* ' name must be unique within the document, it groups number of slides together, trivial case is `* The very first slide` `* Normal slides` and `* The very last slide`. Not displayed in final pdf.
  - Section level 2 '** ' name is must be unique within the document and should characterize the slide. Not displayed in final pdf.
  - Section level 3 '*** ' name is displayed as the slide title.


###	Types of pages and page templates

 There are these page types/templates, the simple code says how many columns are and indicate Text and Image order:
  - C1T - text only
  - C2TI - two columns, text on the left, image on the right
  - C2TII - two columns, text on the left, two images on the right, one on top of the other
  - C2IT - two columns, image on the left, text on the right
  - C3 - three columns, each column with image and the text bellow

### \only overlays for slideshows

When a slide has two or more images that should cycle on click (to avoid overflow), use `\only<N>` overlays. **IMPORTANT: every image in the slideshow must be wrapped in `\only`, including the first one.** Forgetting `\only<1>` on the first image is a common bug — both images then appear simultaneously.

**Formatting rule**: each `#+LATEX:` directive must be on its own line. Do NOT compress `}\only<N>{%` onto a single `#+LATEX:` line — keep the closing and opening on separate lines for operability (easier editing, reordering, commenting out):

```
#+LATEX: \only<1>{%
#+ATTR_LATEX: :width 0.9\textwidth
  [[file:image_first.jpg]]
#+LATEX: }
#+LATEX: \only<2>{%
#+ATTR_LATEX: :width 0.9\textwidth
  [[file:image_second.jpg]]
#+LATEX: }
```

For more than two images:

```
#+LATEX: \only<1>{%
#+ATTR_LATEX: :width 0.9\textwidth
  [[file:image_a.jpg]]
#+LATEX: }
#+LATEX: \only<2>{%
#+ATTR_LATEX: :width 0.9\textwidth
  [[file:image_b.jpg]]
#+LATEX: }
#+LATEX: \only<3>{%
#+ATTR_LATEX: :width 0.9\textwidth
  [[file:image_c.jpg]]
#+LATEX: }
```

Checklist before committing:
- [ ] Every `\only` group starts with `#+LATEX: \only<N>{%` and ends with `#+LATEX: }`
- [ ] The first image starts with `#+LATEX: \only<1>{%` (not bare `#+ATTR_LATEX`)
- [ ] Closing `}` and opening `\only<N+1>{%` are on **separate** `#+LATEX:` lines (NOT `#+LATEX: }\only<2>{%`)
- [ ] The last group ends with just `#+LATEX: }`

**Template C1T:**

```

** Frame Unique Name C1T 1
***   Displayed Title                                    :B_fullframe:
  :PROPERTIES:
  :BEAMER_env: beamercolorbox
  :END:

  - Item 1
    - subItem 2
    - subItem 3
    - subItem 4

```

**Template C2TI:**

```
** Frame Unique Name C2TI 2
***   Displayed Title                                  :B_fullframe:
**** column-text
  :PROPERTIES:
  :BEAMER_env: column
  :BEAMER_col: 0.35
  :BEAMER_opt: [t]
  :END:
  # +LATEX:
Here is the text of the frame.
 - Item 1
 - Item 2
**** column-image
  :PROPERTIES:
  :BEAMER_env: column
  :BEAMER_col: 0.65
  :BEAMER_opt: [t]
  :END:

#+ATTR_LATEX: :width 0.8\textwidth
  [[file:image.png]]

```

**Template C2TII:**

```
** Frame Unique Name C2TII 2
***   Displayed Title                                           :B_fullframe:
**** column-text
  :PROPERTIES:
  :BEAMER_env: column
  :BEAMER_col: 0.6
  :BEAMER_opt: [t]
  :END:
  # +LATEX:
  Here is the text of the frame
  - Item 1
  - Item 2

**** column-image
  :PROPERTIES:
  :BEAMER_env: column
  :BEAMER_col: 0.4
  :BEAMER_opt: [t]
  :END:
\vspace{-12mm}
#+ATTR_LATEX: :width 0.8\textwidth
  [[file:image1.jpg]]
Text to image 1
#+ATTR_LATEX: :width 0.8\textwidth
  [[file:image2.jpg]]
Text to image 2
# a comment
```

**Template C2II:**


```
** Frame Unique Name C2II 4
***   Displayed Title                          :B_fullframe:
**** column-image1
  :PROPERTIES:
  :BEAMER_env: column
  :BEAMER_col: 0.45
  :BEAMER_opt: [t]
  :END:
#+ATTR_LATEX: :width 1.0\textwidth
  [[file:image1.png]]

**** column-image2
  :PROPERTIES:
  :BEAMER_env: column
  :BEAMER_col: 0.55
  :BEAMER_opt: [t]
  :END:

#+ATTR_LATEX: :width 1.0\textwidth
  [[file:image2.png]]

```

**Template C3:**

```
** Frame Unique Name C3 5
***   Displayed Title             :B_fullframe:
\vskip 0mm
**** column1
  :PROPERTIES:
  :BEAMER_env: column
  :BEAMER_col: 0.33
  :BEAMER_opt: [t]
  :END:

#+ATTR_LATEX: :width 1.\textwidth
  [[file:image1.png]]
#+LATEX: {\bf   {\color{myora} Orange} and normal text }\vspace{0.5em}

# \fontsize{4}{5}\selectfont
\footnotesize
Text to image 1

**** column2
  :PROPERTIES:
  :BEAMER_env: column
  :BEAMER_col: 0.33
  :BEAMER_opt: [t]
  :END:
#+ATTR_LATEX: :width 1.0\textwidth
  [[file:image2.png]]
#+LATEX: {\bf    {\color{myora} Orange} and normal text }\vspace{0.5em}

# \fontsize{4}{5}\selectfont
\footnotesize
Text to the image 2
**** column3
  :PROPERTIES:
  :BEAMER_env: column
  :BEAMER_col: 0.33
  :BEAMER_opt: [t]
  :END:
#+ATTR_LATEX: :width 1.\textwidth
  [[file:image3.png]]
#+LATEX: {\bf     {\color{myora} Orange} and normal color text }\vspace{0.5em}

# \fontsize{4}{5}\selectfont
\footnotesize
Text for the image 3

```


**Template onlyenv**
This uses `\begin{onlyenv}<range> ... \end{onlyenv}` and it generates a slide with some elements changing. Here is a complex example, where in the left column `\temporal<range>{before}{in range}{after}` is used for effect, and `onlyenv` is used in the right column:
```
*** Visible Title
**** column-left
  :PROPERTIES:
  :BEAMER_env: column
  :BEAMER_col: 0.55
  :BEAMER_opt: [t]
  :END:

/What may we do?/
\vskip 2mm

#+LATEX:\temporal<1>{ \ \usebeamertemplate{itemize item}\enspace C}{\ \usebeamertemplate{itemize item}\enspace  \LARGE C\normalsize}{ \ \usebeamertemplate{itemize item}\enspace C}\color{myblu}urate - see what TECH allows today \vskip 2mm

#+LATEX:\temporal<2>{ \ \usebeamertemplate{itemize item}\enspace I}{\ \usebeamertemplate{itemize item}\enspace  \LARGE I\normalsize}{ \ \usebeamertemplate{itemize item}\enspace I}\color{myblu}mplement - what can be done for us here  \vskip 2mm

#+LATEX:\temporal<3>{ \ \usebeamertemplate{itemize item}\enspace G}{\ \usebeamertemplate{itemize item}\enspace  \LARGE G\normalsize}{ \ \usebeamertemplate{itemize item}\enspace G}\color{myblu}o-to person - somebody to share/discuss with \vskip 2mm

#+LATEX:\temporal<4>{ \ \usebeamertemplate{itemize item}\enspace A}{\ \usebeamertemplate{itemize item}\enspace  \LARGE A\normalsize}{ \ \usebeamertemplate{itemize item}\enspace A}\color{myblu}wareness - see what is going to happen soon \vskip 2mm

#+LATEX:\temporal<5>{ \ \usebeamertemplate{itemize item}\enspace R}{\ \usebeamertemplate{itemize item}\enspace  \LARGE R\normalsize}{ \ \usebeamertemplate{itemize item}\enspace R}\color{myblu}isks - what not to do (OpenCLAW, unresticted local agents, automated chains) \vskip 2mm

**** column-right
  :PROPERTIES:
  :BEAMER_env: column
  :BEAMER_col: 0.45
  :BEAMER_opt: [t]
  :END:

#+LATEX: \begin{onlyenv}<1>
\Huge \textcolor{myora}{C:/>}
\normalsize
- check the progress in:
  - models
    - sizes + prices + capabilities
  - agents:
    - search engines (EXA)
    - new concepts (orchestration)
    - new tools (SKILLS)
  - web-services

#+LATEX: \end{onlyenv}
#+LATEX: \begin{onlyenv}<2>
\Huge \textcolor{myora}{I:}
\normalsize
- is there a moment to:
  - demand from people here?
  - deploy internal LLMs?
  - buy a big licence?

#+LATEX: \end{onlyenv}
#+LATEX: \begin{onlyenv}<3>
\Huge \textcolor{myora}{G:}
\normalsize
- somebody must sacrifice himself
  - remembers the status quo
  - is available to others

#+LATEX: \end{onlyenv}
#+LATEX: \begin{onlyenv}<4>
\Huge \textcolor{myora}{A:}
\normalsize
- We need to identify side-effects/impacts:
  - how do students write their theses?
  - how much do they understand to the processes they used?
  - how much do we suffocate each other by documents by LLMs?

#+LATEX: \end{onlyenv}
#+LATEX: \begin{onlyenv}<5>
\Huge \textcolor{myora}{R:}
\normalsize
- What is immediately dangerous:
  - OpenClaw
  - unrestricted agentic-coding run (CC maybe safer)
#+LATEX: \end{onlyenv}
```


### Missing Image

If the standard slide needs an image and it is missing, create a placeholder using script `generate_image.py`. It uses PEP 723 and dependencies are defined in the script - solve the dependencies using `uv add --script  generate_image.py 'click' 'huggingface_hub' 'Pillow'`.
Run with `uv run generate_image.py "Brief image description"`


### Checks
 - Check that each slide has max 10 lines of text. Resolve the cases by either creating new slide teplate C2TT (prefered) or split to 2 or more slides.
 - Check that each slide name (level 2 '** ') is as short as possible
 - Check that each slide title (to be displayed, level 3 '*** ') has max. 2 words or max. 2 words + ACRONYM


## Prerequisites

 Before compiling, ensure these are installed:

 1. **Pygments** (required by org-mode for code block export / minted):
     ```
     uv tool install Pygments
     ```

 2. **XeLaTeX** — the presentation uses `fontspec` which requires XeLaTeX (not pdflatex). Two things must be in place:
     - The org file **must** have `#+LATEX_COMPILER: xelatex` in the header. If missing, add it before `#+LATEX_CLASS:`.
     - The Emacs config (`init.el` or `init_beamer_only.el`) **must** set `org-latex-pdf-process` to use `xelatex`. **Beware**: if `org-latex-pdf-process` is set multiple times, only the last `setq` takes effect. A common mistake is setting it to `xelatex` first, then overriding it with a `latexmk ... lualatex` line — the last one wins and `xelatex` is ignored. Use only one `setq` for `org-latex-pdf-process`. Recommended:
       ```elisp
       (setq org-latex-pdf-process
             '("latexmk -xelatex -shell-escape -interaction nonstopmode -pdf -f %f"))
       ```
       Or without latexmk:
       ```elisp
       (setq org-latex-pdf-process
             '("xelatex -shell-escape -interaction nonstopmode -output-directory %o %f"
               "xelatex -shell-escape -interaction nonstopmode -output-directory %o %f"))
       ```

 3. **Sora font** — required by the theme. Install and verify with the steps in `tramp_and_install.md`.

 4. **Content slides have no background image.** Only the first and last frames use `bg_main.jpg`. Normal slides use the plain beamer background with the defined colors. Do not add background images to content slides unless explicitly requested.

## Compilation

### From Emacs

 Open the `.org` file and use `C-c C-e l P` to export to PDF. Emacs will use XeLaTeX because of the `#+LATEX_COMPILER: xelatex` header.

### From command line

 To compile via emacs batch mode:
 ```
 #!/bin/bash

 ORG_FILE="$1"
 if [ "$ORG_FILE" = "" ]; then
   echo "Usage: $0 <file.org> [--watch]"
   exit 1
 fi
 BASENAME=$(basename "$ORG_FILE" .org)

 # Check for watch flag
 if [ "$2" = "--watch" ]; then
     echo "Watching $ORG_FILE for changes..."
     while inotifywait -e close_write "$ORG_FILE"; do
         echo "Change detected, recompiling..."
         emacs --batch --load "~/.emacs.d/init_beamer_only.el" --eval "(progn
           (find-file \"$ORG_FILE\")
           (org-beamer-export-to-pdf)
           (kill-emacs 0))" && cp "$BASENAME.pdf" /tmp
         echo "Compilation complete."
     done
 else
     emacs --batch --load "~/.emacs.d/init_beamer_only.el" --eval "(progn
       (find-file \"$ORG_FILE\")
       (org-beamer-export-to-pdf)
       (kill-emacs 0))" && cp "$BASENAME.pdf" /tmp
 fi
 ```

### Quick test from command line (xelatex directly)

 If you need to debug LaTeX errors, compile the `.tex` file directly:
 ```
 xelatex --shell-escape spiral_introduction.tex
 ```
 Note: This requires the `.tex` file to already exist (e.g. from a prior org export that failed partway).


## Emacs tips

  - **org-tidy** — hides drawers (PROPERTIES, etc.) in org-mode for cleaner editing. Install and enable with:
    ```elisp
    (use-package org-tidy
      :ensure t
      :config
      (add-hook 'org-mode-hook #'org-tidy-mode))
    ```

  - **Handy keybindings for beamer presentations** (add to `init.el`):
    - `F5` — insert `\only<1>` overlay snippet
    - `Shift-F5` — insert `\visible<1>` overlay snippet
    - `F4` — switch to `ibuffer` (better buffer management with many slides open)
    - `F10` — export current org file to beamer PDF (`org-beamer-export-to-pdf`)

  - **Isotope notation in beamer/org** — use `\null^{A}Element` (e.g. `\null^{155}Gd`) for superscript isotope formatting. The shorter `\nul^{}` also works and does **not** disrupt `itemize` spacing, unlike `\null^{}` which can add unwanted vertical space inside bullet lists. Precedence: prefer `\nul^{}` inside `itemize` environments.

  - **Logo images must stay as `.png`** — logos (`logofull.png`, `logosmall.png`, `logo_s2cz.png`, etc.) often contain transparency (alpha channel) which `.jpg` does not support. Never convert logos to `.jpg`. Other (non-logo) images may be converted to `.jpg` for smaller file size.

## When to use me

When working with org-mode presentation (beamer). For a non-slide org document, use `main_battle_tested_org_SKILL.md` instead. Ask clarifying questions on feature name.

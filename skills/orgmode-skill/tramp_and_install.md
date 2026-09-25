# TRAMP and install notes

Environment setup for org-beamer presentations. Slide craft lives in `SKILL_presentation.md`. Joint skill entry: `SKILL.md`.

## Sora font

The theme uses Sora. Installing by copying `.ttf` files is not enough — refresh the font cache and verify.

From `Sora.zip` in the skill directory:

```bash
mkdir -p ~/.local/share/fonts/static
unzip Sora.zip -d ~/.local/share/fonts/static/
fc-cache -f -v
fc-list | grep -i sora   # must list Sora-*.ttf
```

If you already have loose `Sora-*.ttf` files:

```bash
mkdir -p ~/.local/share/fonts
cp Sora-*.ttf ~/.local/share/fonts/
fc-cache -fv
fc-list | grep -i sora
```

Expected location after the zip install: `~/.local/share/fonts/static/Sora-*.ttf`.

## VM LaTeX packages

On a fresh VM, PDF export needs XeLaTeX and friends:

```bash
sudo apt-get install -y latexmk texlive-xetex texlive-fonts-recommended texlive-fonts-extra
```

For full compatibility (avoids missing-package issues):

```bash
sudo apt-get install -y texlive-full
```

Pygments (org-mode minted / code-block export) is still installed with `uv tool install Pygments` — see `SKILL.md`.

## TRAMP: edit the VM repo from host Emacs

Use TRAMP to edit the VM repo from host Emacs via SSH:

- Ensure the VM allows SSH and you have a key set up
- In host Emacs: `M-x find-file RET /ssh:ubuntu@<vm-ip>:/home/ubuntu/44_lxc/organizer_physics`
- Open the repo there and run Magit as usual (Git runs on the VM)
- Use `magit-status` for git status
- Use `auto-revert-mode` to coordinate with an LLM editing files in the background

Auto-revert over TRAMP needs explicit enabling — file notifications (inotify) do not work remotely. Add this to host Emacs config:

```elisp
(setq auto-revert-remote-files t)
(setq auto-revert-interval 2)
(add-hook 'find-file-hook
          (lambda ()
            (when (file-remote-p (buffer-file-name))
              (auto-revert-mode 1))))
```

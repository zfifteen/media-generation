#!/usr/bin/env bash
set -e

echo "=== Manim reset script for macOS ==="
echo "This will uninstall old manim (3b1b/manimgl & community) from common locations"
echo "and install Manim Community Edition plus its Homebrew dependencies."
echo

read -p "Press Enter to continue, or Ctrl+C to cancel..."

########################################
# 1. Detect OS
########################################

if [[ "$(uname)" != "Darwin" ]]; then
  echo "This script is intended for macOS only."
  exit 1
fi

########################################
# 2. Uninstall Python packages (3b1b manim, manimgl, manim community) from common Pythons
########################################

echo
echo "=== Uninstalling Python manim packages (if present) ==="

PY_BIN_CANDIDATES=(
  "python3"
  "python"
  "python3.12"
  "python3.11"
  "python3.10"
)

for py in "${PY_BIN_CANDIDATES[@]}"; do
  if command -v "$py" >/dev/null 2>&1; then
    echo "-> Using $py to uninstall pip packages (if installed)..."
    "$py" -m pip uninstall -y manim manimgl manimce manimlib 2>/dev/null || true
  fi
done

########################################
# 3. Remove old manim source checkouts (optional cleanup)
########################################

echo
echo "=== Removing common local manim source directories (if they exist) ==="

SRC_DIRS=(
  "$HOME/manim"
  "$HOME/Manim"
  "$HOME/Projects/manim"
  "$HOME/IdeaProjects/manim"
)

for d in "${SRC_DIRS[@]}"; do
  if [[ -d "$d" ]]; then
    echo "-> Found directory $d"
    read -p "   Delete this directory? [y/N] " ans
    if [[ "$ans" == "y" || "$ans" == "Y" ]]; then
      rm -rf "$d"
      echo "   Deleted $d"
    else
      echo "   Skipped $d"
    fi
  fi
done

########################################
# 4. Ensure Homebrew is installed
########################################

echo
echo "=== Ensuring Homebrew is installed ==="

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found. Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

echo "Homebrew is installed at: $(command -v brew)"

########################################
# 5. Install system dependencies for Manim Community
########################################

echo
echo "=== Installing Manim system dependencies via Homebrew ==="

# Graphics & media
brew install pkg-config cairo pango ffmpeg sox || true

# LaTeX distribution (no GUI to save space, still includes dvisvgm)
brew install --cask mactex-no-gui || true

########################################
# 6. Ensure TeX binaries are on PATH
########################################

echo
echo "=== Configuring PATH for MacTeX binaries ==="

TEXBIN="/Library/TeX/texbin"

if [[ -d "$TEXBIN" ]]; then
  SHELL_RC="$HOME/.zshrc"
  if [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="$HOME/.bashrc"
  fi

  if ! grep -q '\/Library\/TeX\/texbin' "$SHELL_RC" 2>/dev/null; then
    echo "export PATH=\"$TEXBIN:\$PATH\"" >> "$SHELL_RC"
    echo "-> Added $TEXBIN to PATH in $SHELL_RC"
  else
    echo "-> $TEXBIN already in PATH config ($SHELL_RC)"
  fi

  # Update PATH for current shell session
  export PATH="$TEXBIN:$PATH"
else
  echo "WARNING: $TEXBIN not found. MacTeX install may not have completed correctly."
fi

echo
echo "Checking latex / dvisvgm availability..."
command -v latex  >/dev/null 2>&1 && echo "latex found:  $(command -v latex)" || echo "latex NOT found"
command -v dvisvgm >/dev/null 2>&1 && echo "dvisvgm found: $(command -v dvisvgm)" || echo "dvisvgm NOT found"

########################################
# 7. Install Manim Community Edition
########################################

echo
echo "=== Installing Manim Community Edition ==="

# Recommended in 2025+ to just use Brew if you are on macOS
# This avoids Python 3.13 / manimpango build issues.[web:65][web:41]
brew install manim || true

echo
echo "Manim version:"
manim --version || echo "Manim not found on PATH; check your Homebrew install."

########################################
# 8. Run manim checkhealth
########################################

echo
echo "=== Running 'manim checkhealth' ==="
manim checkhealth || true

echo
echo "=== Done ==="
echo "Open a NEW terminal so that PATH changes take effect, then run:"
echo "  manim -pql main2.py PythagoreanTheoremScene"
echo
echo "If 'latex' or 'dvisvgm' still show as missing in 'manim checkhealth',"
echo "paste that output and the result of 'which manim; which latex; which dvisvgm'."

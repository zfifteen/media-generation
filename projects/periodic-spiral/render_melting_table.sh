#!/usr/bin/env bash
# ===========================================================================
# render_melting_table.sh
# Renders all 5 scenes of "The Melting Table" and concatenates into one video.
#
# Usage:
#   chmod +x render_melting_table.sh
#   ./render_melting_table.sh
#
# Prerequisites:
#   - manim (manimce) installed and on PATH
#   - ffmpeg installed and on PATH
#
# Output:
#   media/videos/melting_table_final.mp4
# ===========================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIM_SCRIPT="${SCRIPT_DIR}/melting_table.py"
OUTPUT_DIR="${SCRIPT_DIR}/media/videos"

# Scene names in narrative order
SCENES=(
    "Scene1_FamiliarGrid"
    "Scene2_RollingSpiral"
    "Scene3_EngineUnderTheHood"
    "Scene4_Dissolution"
    "Scene5_WhatWeKnow"
)

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()  { echo -e "${GREEN}[OK]${NC}    $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC}  $1"; }
fail() { echo -e "${RED}[FAIL]${NC}  $1"; exit 1; }

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------
command -v manim  >/dev/null 2>&1 || fail "manim not found. Install with: pip install manim"
command -v ffmpeg >/dev/null 2>&1 || fail "ffmpeg not found. Install with: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
[[ -f "$MANIM_SCRIPT" ]]         || fail "melting_table.py not found in ${SCRIPT_DIR}"

mkdir -p "$OUTPUT_DIR"

# ---------------------------------------------------------------------------
# Render each scene
# ---------------------------------------------------------------------------
RENDERED_FILES=()

for scene in "${SCENES[@]}"; do
    echo ""
    echo "==========================================="
    echo " Rendering: ${scene}"
    echo "==========================================="

    if manim "$MANIM_SCRIPT" "$scene" 2>&1; then
        log "Rendered ${scene}"
    else
        fail "Failed to render ${scene}"
    fi

    # Locate the output file (manim puts it under media/videos/<script_name>/1440p60/)
    SCENE_VIDEO=$(find "${SCRIPT_DIR}/media/videos" -name "${scene}.mp4" -type f | head -n 1)

    if [[ -z "$SCENE_VIDEO" ]]; then
        # Fallback: search for any mp4 containing the scene name
        SCENE_VIDEO=$(find "${SCRIPT_DIR}/media" -name "*${scene}*" -name "*.mp4" -type f | head -n 1)
    fi

    if [[ -z "$SCENE_VIDEO" ]]; then
        fail "Could not locate rendered video for ${scene}"
    fi

    log "Found: ${SCENE_VIDEO}"
    RENDERED_FILES+=("$SCENE_VIDEO")
done

# ---------------------------------------------------------------------------
# Concatenate all scenes into one video
# ---------------------------------------------------------------------------
echo ""
echo "==========================================="
echo " Concatenating ${#RENDERED_FILES[@]} scenes"
echo "==========================================="

CONCAT_LIST="${OUTPUT_DIR}/concat_list.txt"
> "$CONCAT_LIST"

for f in "${RENDERED_FILES[@]}"; do
    echo "file '${f}'" >> "$CONCAT_LIST"
done

FINAL_OUTPUT="${OUTPUT_DIR}/melting_table_final.mp4"

ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" \
    -c copy \
    -movflags +faststart \
    "$FINAL_OUTPUT" 2>&1

rm -f "$CONCAT_LIST"

if [[ -f "$FINAL_OUTPUT" ]]; then
    FILESIZE=$(du -h "$FINAL_OUTPUT" | cut -f1)
    DURATION=$(ffprobe -v error -show_entries format=duration \
        -of default=noprint_wrappers=1:nokey=1 "$FINAL_OUTPUT" 2>/dev/null || echo "unknown")

    echo ""
    echo "==========================================="
    log "Final video: ${FINAL_OUTPUT}"
    log "Size: ${FILESIZE}"
    log "Duration: ${DURATION}s"
    echo "==========================================="
else
    fail "Concatenation failed. Check ffmpeg output above."
fi

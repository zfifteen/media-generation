#!/bin/bash
# ============================================================================
# render_euler_dimensions.sh
# Renders all scenes from euler_dimensions.py and concatenates into one video
# Usage: chmod +x render_euler_dimensions.sh && ./render_euler_dimensions.sh
# ============================================================================

set -e

SCRIPT="euler_dimensions.py"
SCENES=(
    "TitleScene"
    "Scene1_FourShadows"
    "Scene2_SeriesCompression"
    "Scene3_CFStaircase"
    "Scene4_SplitScreen"
    "Scene5_PhaseSeparation"
    "Scene6_HigherDimensional"
    "Scene7_FinalSynthesis"
)

FILELIST="filelist.txt"
FINAL_OUTPUT="euler_dimensions_full.mp4"

echo "============================================"
echo "  The Orthogonal Dimensions of e"
echo "  Manim Render Pipeline"
echo "============================================"
echo ""

# Verify dependencies
if ! command -v manim &> /dev/null; then
    echo "[ERROR] manim not found. Install: pip install manim"
    exit 1
fi
if ! command -v ffmpeg &> /dev/null; then
    echo "[ERROR] ffmpeg not found."
    exit 1
fi
if [ ! -f "$SCRIPT" ]; then
    echo "[ERROR] $SCRIPT not found."
    exit 1
fi

# Clean previous partial renders to avoid stale files
echo "[CLEANUP] Removing previous render artifacts..."
rm -rf media/videos/euler_dimensions/
echo ""

# Render each scene
echo "[STEP 1/3] Rendering ${#SCENES[@]} scenes..."
echo ""

for i in "${!SCENES[@]}"; do
    SCENE="${SCENES[$i]}"
    INDEX=$((i + 1))
    echo "  [$INDEX/${#SCENES[@]}] Rendering $SCENE..."
    # Capture full manim output so we can see errors
    manim "$SCRIPT" "$SCENE" 2>&1 | tee "/tmp/manim_${SCENE}.log" | grep -E "(File ready|\.mp4|ERROR|Error|error)" || true
    echo "  [$INDEX/${#SCENES[@]}] $SCENE done."
    echo ""
done

echo "[STEP 1/3] All renders attempted."
echo ""

# Discover videos
echo "[DEBUG] All .mp4 files produced:"
find media/ -name "*.mp4" -type f 2>/dev/null | sort
echo ""

echo "[STEP 2/3] Building file list..."
> "$FILELIST"
MISSING=0

for SCENE in "${SCENES[@]}"; do
    FOUND=""

    # Manim CE places the final combined scene video at:
    # media/videos/<script_stem>/<quality>/<SceneName>.mp4
    # Search broadly for <SceneName>.mp4 anywhere under media/
    CANDIDATE=$(find media/ -maxdepth 5 -name "${SCENE}.mp4" -type f 2>/dev/null | head -1)
    if [ -n "$CANDIDATE" ]; then
        FOUND="$CANDIDATE"
    fi

    if [ -z "$FOUND" ]; then
        echo "  [MISS] $SCENE -- no ${SCENE}.mp4 found"
        echo "         Check /tmp/manim_${SCENE}.log for errors"
        MISSING=$((MISSING + 1))
    else
        echo "file '${FOUND}'" >> "$FILELIST"
        echo "  [OK]   $SCENE -> $FOUND"
    fi
done

echo ""

if [ "$MISSING" -gt 0 ]; then
    echo "[WARNING] $MISSING scene(s) missing. Check logs in /tmp/manim_*.log"
    AVAILABLE=$(wc -l < "$FILELIST" | tr -d ' ')
    if [ "$AVAILABLE" -eq 0 ]; then
        echo "[ERROR] No videos to concatenate."
        exit 1
    fi
    echo "Proceeding with $AVAILABLE available scene(s)..."
    echo ""
fi

# Concatenate
echo "[STEP 3/3] Concatenating..."
echo ""
cat "$FILELIST"
echo ""

ffmpeg -y -f concat -safe 0 -i "$FILELIST" -c copy "$FINAL_OUTPUT" 2>&1 | tail -5

if [ -f "$FINAL_OUTPUT" ]; then
    FILESIZE=$(du -h "$FINAL_OUTPUT" | cut -f1)
    DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FINAL_OUTPUT" 2>/dev/null | cut -d'.' -f1)
    echo ""
    echo "============================================"
    echo "  BUILD COMPLETE"
    echo "  Output:   $FINAL_OUTPUT"
    echo "  Size:     $FILESIZE"
    echo "  Duration: ${DURATION}s (target: 120s)"
    echo "============================================"
else
    echo "[ERROR] Concatenation failed."
    exit 1
fi

rm -f "$FILELIST"
echo ""
echo "Play: open $FINAL_OUTPUT"

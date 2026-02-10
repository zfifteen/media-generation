#!/bin/bash
# =============================================================================
# stitch_scenes.sh
# Renders all 9 Manim scenes from a single file and stitches them into one video
# using ffmpeg.
# Usage: bash stitch_scenes.sh
# =============================================================================

set -e

echo "=== Rendering Manim Scenes (single file) ==="

PY_FILE="levitating_time_crystals_all_scenes.py"

# Ordered list of scene class names (must match the Python file)
declare -a CLASSES=(
  "Scene01_Title"
  "Scene02_AcousticLevitation"
  "Scene03_TwoBeads"
  "Scene04_NewtonThird"
  "Scene05_TimeCrystal"
  "Scene06_EnergyFlow"
  "Scene07_ExceptionalPoint"
  "Scene08_Implications"
  "Scene09_Credits"
)

# Render each scene
for class_name in "${CLASSES[@]}"; do
    echo "Rendering $PY_FILE ($class_name)..."
    manim "$PY_FILE" "$class_name"
done

echo ""
echo "=== Finding Rendered Videos ==="

CONCAT_FILE="concat_list.txt"
> "$CONCAT_FILE"

MEDIA_DIR="media/videos"
BASE_NAME="${PY_FILE%.py}"

for class_name in "${CLASSES[@]}"; do
    # Find the rendered mp4 (search in all quality subdirectories)
    video_path=$(find "$MEDIA_DIR/$BASE_NAME" -name "${class_name}.mp4" 2>/dev/null | head -1)

    if [ -z "$video_path" ]; then
        echo "ERROR: Could not find rendered video for $class_name"
        echo "  Searched in: $MEDIA_DIR/$BASE_NAME/"
        exit 1
    fi

    echo "  Found: $video_path"
    echo "file '$video_path'" >> "$CONCAT_FILE"
done

echo ""
echo "=== Stitching Videos ==="
OUTPUT="levitating_time_crystals_full.mp4"

ffmpeg -y -f concat -safe 0 -i "$CONCAT_FILE" -c copy "$OUTPUT"

echo ""
echo "=== Done ==="
echo "Output: $OUTPUT"
echo "Duration: ~90 seconds (9 scenes x 10 seconds)"

rm -f "$CONCAT_FILE"

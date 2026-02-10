#!/bin/bash
# render_gravity_zmapping.sh
# Renders the Z-mapping gravity anomaly visualization

set -e  # Exit on error

SCRIPT_NAME="gravity_zmapping.py"
MAIN_SCENE="GravityAnomalyZMapping"
DIAGNOSTIC_SCENE="WideFrameCheck"
OUTPUT_DIR="media/videos"

echo "=================================="
echo "Z-Mapping Gravity Visualization"
echo "Render Script"
echo "=================================="
echo ""

# Check if manim is installed
if ! command -v manim &> /dev/null
then
    echo "ERROR: manim could not be found"
    echo "Install with: pip install manim"
    exit 1
fi

# Check if script exists
if [ ! -f "$SCRIPT_NAME" ]; then
    echo "ERROR: $SCRIPT_NAME not found in current directory"
    exit 1
fi

echo "Found manim: $(which manim)"
echo "Script: $SCRIPT_NAME"
echo ""

# Render main scene
echo "Rendering main scene: $MAIN_SCENE"
echo "-----------------------------------"
manim "$SCRIPT_NAME" "$MAIN_SCENE"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Main scene rendered successfully"
    echo ""
else
    echo ""
    echo "✗ Main scene rendering failed"
    exit 1
fi

# Ask if user wants to render diagnostic frame check
read -p "Render diagnostic frame check? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Rendering diagnostic scene: $DIAGNOSTIC_SCENE"
    echo "-----------------------------------"
    manim "$SCRIPT_NAME" "$DIAGNOSTIC_SCENE"

    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ Diagnostic scene rendered successfully"
        echo ""
    else
        echo ""
        echo "✗ Diagnostic scene rendering failed"
    fi
fi

echo "=================================="
echo "Render Complete"
echo "=================================="
echo ""
echo "Output location:"
echo "$OUTPUT_DIR"
echo ""
echo "Main video:"
find "$OUTPUT_DIR" -name "*$MAIN_SCENE*.mp4" -type f -print -quit 2>/dev/null || echo "  (not found)"
echo ""

# Optional: Open the output directory
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    read -p "Open output folder? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "$OUTPUT_DIR"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    read -p "Open output folder? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        xdg-open "$OUTPUT_DIR" 2>/dev/null || nautilus "$OUTPUT_DIR" 2>/dev/null || echo "Could not open folder automatically"
    fi
fi

echo "Done!"

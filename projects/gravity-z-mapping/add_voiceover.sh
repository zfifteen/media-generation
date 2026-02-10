#!/bin/bash
# add_voiceover.sh
# Adds TTS voiceover to the rendered Manim video

set -e  # Exit on error

# File paths based on your project structure
VIDEO_SOURCE="media/videos/gravity_zmapping/1440p60/GravityAnomalyZMapping.mp4"
NARRATIVE_FILE="narrative.md"
VOICEOVER_AUDIO="voiceover.mp3"
OUTPUT_VIDEO="GravityAnomalyZMapping_with_voiceover.mp4"
VOICE="en-US-GuyNeural"  # Options: en-US-GuyNeural, en-GB-RyanNeural, en-US-AriaNeural

echo "=================================="
echo "Add Voiceover to Manim Video"
echo "=================================="
echo ""

# Check if video source exists
if [ ! -f "$VIDEO_SOURCE" ]; then
    echo "ERROR: Video file not found at $VIDEO_SOURCE"
    echo "Have you rendered the animation yet?"
    exit 1
fi

# Check if narrative exists
if [ ! -f "$NARRATIVE_FILE" ]; then
    echo "ERROR: Narrative file not found: $NARRATIVE_FILE"
    exit 1
fi

# Check if edge-tts is installed
if ! command -v edge-tts &> /dev/null
then
    echo "edge-tts not found. Installing..."
    pip install edge-tts
fi

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null
then
    echo "ERROR: ffmpeg not found. Please install it:"
    echo "  macOS: brew install ffmpeg"
    echo "  Linux: sudo apt install ffmpeg"
    exit 1
fi

echo "Source video: $VIDEO_SOURCE"
echo "Narrative: $NARRATIVE_FILE"
echo "Voice: $VOICE"
echo ""

# Generate TTS audio from narrative
echo "Generating voiceover audio..."
edge-tts \
    --text "$(cat $NARRATIVE_FILE)" \
    --write-media "$VOICEOVER_AUDIO" \
    --voice "$VOICE"

if [ $? -ne 0 ]; then
    echo "✗ Failed to generate voiceover audio"
    exit 1
fi

echo "✓ Voiceover audio generated: $VOICEOVER_AUDIO"
echo ""

# Get durations
echo "Checking durations..."
VIDEO_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO_SOURCE" 2>/dev/null)
AUDIO_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VOICEOVER_AUDIO" 2>/dev/null)

echo "  Video duration: ${VIDEO_DURATION}s"
echo "  Audio duration: ${AUDIO_DURATION}s"
echo ""

# Combine video and audio
echo "Combining video with voiceover..."
ffmpeg -y \
    -i "$VIDEO_SOURCE" \
    -i "$VOICEOVER_AUDIO" \
    -c:v copy \
    -c:a aac \
    -b:a 192k \
    -map 0:v:0 \
    -map 1:a:0 \
    -shortest \
    "$OUTPUT_VIDEO" \
    -loglevel error -stats

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Video with voiceover created successfully!"
    echo ""
    echo "Output: $OUTPUT_VIDEO"
    echo ""

    # Show output duration
    OUTPUT_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_VIDEO" 2>/dev/null)
    echo "Final duration: ${OUTPUT_DURATION}s"
    echo ""

    # Warn if audio is much longer than video
    if (( $(echo "$AUDIO_DURATION > $VIDEO_DURATION + 5" | bc -l) )); then
        echo "⚠️  WARNING: Audio is significantly longer than video"
        echo "   The voiceover will be cut off at the end"
        echo "   Consider adjusting the narrative or extending the animation"
    fi
else
    echo ""
    echo "✗ Failed to combine video and audio"
    exit 1
fi

# Optional: Open the output file
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    read -p "Play the video now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "$OUTPUT_VIDEO"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    read -p "Play the video now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        xdg-open "$OUTPUT_VIDEO" 2>/dev/null || echo "Please open $OUTPUT_VIDEO manually"
    fi
fi

echo ""
echo "=================================="
echo "Done!"
echo "=================================="
echo ""
echo "Cleanup temporary files:"
echo "  rm $VOICEOVER_AUDIO"

#!/bin/bash
# combine_audio_video.sh
# Combines the existing voiceover.mp3 with the rendered Manim video

set -e  # Exit on error

# File paths
VIDEO_SOURCE="media/videos/gravity_zmapping/1440p60/GravityAnomalyZMapping.mp4"
AUDIO_SOURCE="voiceover.mp3"
OUTPUT_VIDEO="GravityAnomalyZMapping_final.mp4"

echo "=================================="
echo "Combine Video with Voiceover"
echo "=================================="
echo ""

# Check if video source exists
if [ ! -f "$VIDEO_SOURCE" ]; then
    echo "ERROR: Video file not found at $VIDEO_SOURCE"
    echo "Please render the animation first with:"
    echo "  manim gravity_zmapping.py GravityAnomalyZMapping"
    exit 1
fi

# Check if audio source exists
if [ ! -f "$AUDIO_SOURCE" ]; then
    echo "ERROR: Audio file not found: $AUDIO_SOURCE"
    echo "Please ensure voiceover.mp3 is in the current directory"
    exit 1
fi

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null
then
    echo "ERROR: ffmpeg not found. Please install it:"
    echo "  macOS: brew install ffmpeg"
    echo "  Linux: sudo apt install ffmpeg"
    exit 1
fi

echo "Video source: $VIDEO_SOURCE"
echo "Audio source: $AUDIO_SOURCE"
echo "Output: $OUTPUT_VIDEO"
echo ""

# Get durations for info
echo "Checking durations..."
if command -v ffprobe &> /dev/null; then
    VIDEO_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO_SOURCE" 2>/dev/null)
    AUDIO_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$AUDIO_SOURCE" 2>/dev/null)

    echo "  Video duration: ${VIDEO_DURATION}s"
    echo "  Audio duration: ${AUDIO_DURATION}s"
    echo ""

    # Check if video is long enough
    if (( $(echo "$VIDEO_DURATION < $AUDIO_DURATION" | bc -l) )); then
        echo "⚠️  WARNING: Video (${VIDEO_DURATION}s) is shorter than audio (${AUDIO_DURATION}s)"
        echo "   Audio will be cut off at the end"
        echo "   Consider re-rendering with longer timing"
        echo ""
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Aborted."
            exit 1
        fi
    fi
fi

# Combine video and audio
echo "Combining video with voiceover..."
echo ""

ffmpeg -y \
    -i "$VIDEO_SOURCE" \
    -i "$AUDIO_SOURCE" \
    -c:v copy \
    -c:a aac \
    -b:a 192k \
    -map 0:v:0 \
    -map 1:a:0 \
    -shortest \
    "$OUTPUT_VIDEO" \
    -loglevel warning -stats

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Video with voiceover created successfully!"
    echo ""
    echo "Output: $OUTPUT_VIDEO"
    echo ""

    # Show output file size and duration
    if command -v ffprobe &> /dev/null; then
        OUTPUT_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_VIDEO" 2>/dev/null)
        OUTPUT_SIZE=$(du -h "$OUTPUT_VIDEO" | cut -f1)
        echo "Final duration: ${OUTPUT_DURATION}s"
        echo "File size: ${OUTPUT_SIZE}"
    fi
else
    echo ""
    echo "✗ Failed to combine video and audio"
    exit 1
fi

echo ""
echo "=================================="
echo "Success!"
echo "=================================="
echo ""

# Optional: Open/play the output file
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
echo "To share or upload, use: $OUTPUT_VIDEO"

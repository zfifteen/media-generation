#!/bin/bash
generate_voiceover.sh

set -e

NARRATIVE_FILE="narrative.md"
OUTPUT_AUDIO="voiceover.mp3"
VOICE="en-US-GuyNeural"  # Options: en-US-GuyNeural, en-GB-RyanNeural, en-US-AriaNeural

echo "=================================="
echo "Narrative Voice-Over Generator"
echo "=================================="
echo ""

# Check if edge-tts is installed
if ! command -v edge-tts &> /dev/null
then
    echo "edge-tts not found. Installing..."
    pip install edge-tts
fi

# Check if narrative file exists
if [ ! -f "$NARRATIVE_FILE" ]; then
    echo "✗ Narrative file not found: $NARRATIVE_FILE"
    exit 1
fi

# Extract text: Try headers first, fallback to whole file if headers not found
NARRATIVE_TEXT=$(sed -n '/## Scene Breakdown/,/## Key Narrative Insights/p' "$NARRATIVE_FILE" | \
    grep -v '```' | grep -v '^#' | grep -v '^\*\*' | grep -v '^---' | sed 's/^- //' | tr '\n' ' ')

if [ -z "$NARRATIVE_TEXT" ] || [ ${#NARRATIVE_TEXT} -lt 10 ]; then
    echo "Notice: Headers not found or empty. Using full content of $NARRATIVE_FILE"
    NARRATIVE_TEXT=$(cat "$NARRATIVE_FILE" | tr '\n' ' ')
fi

echo "Generating voice-over with voice: $VOICE"
echo "Text length: ${#NARRATIVE_TEXT} characters"
echo ""

# Default to current duration, but allow users to override speed if they want
# Usage: ./generate_voiceover.sh "+20%"
RATE=${1:-"+0%"}

edge-tts \
    --text "$NARRATIVE_TEXT" \
    --write-media "$OUTPUT_AUDIO" \
    --voice "$VOICE" \
    --rate="$RATE"

if [ $? -eq 0 ]; then
    echo "✓ Voice-over generated: $OUTPUT_AUDIO"
    echo ""

    # Show duration
    if command -v ffprobe &> /dev/null; then
        DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_AUDIO")
        echo "Duration: ${DURATION}s"
    fi
else
    echo "✗ Voice-over generation failed"
    exit 1
fi

echo ""
echo "To combine with video:"
echo "ffmpeg -i GravityAnomalyZMapping.mp4 -i $OUTPUT_AUDIO -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output_with_voiceover.mp4"

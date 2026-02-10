I need help synchronizing a Manim animation with a TTS voiceover that has incorrect duration.

SITUATION:
I'm creating an educational animation about gravity anomalies using Manim Community Edition. I have a Python script that generates the visualization and a separate voiceover audio file that should narrate over it. However, the audio duration doesn't match what I expected and I need to fix the synchronization.

CURRENT STATE:
- Video file: media/videos/gravity_zmapping/1440p60/GravityAnomalyZMapping.mp4
- Video duration: 54.03 seconds
- Audio file: voiceover.mp3
- Audio duration: 154.82 seconds (2 minutes 35 seconds)
- Expected audio duration: ~51-52 seconds based on word count

THE PROBLEM:
The audio file is almost 3 times longer than expected. The narrative.md file contains 343 words which should take approximately 51 seconds at normal speaking rate (140-180 words per minute). Instead, the TTS generated 154.8 seconds of audio.

FILES I HAVE:
1. gravity_zmapping.py - The Manim animation script with timing annotations
2. narrative.md - Plain text voiceover script (no markdown formatting)
3. voiceover.mp3 - The problematic audio file (154.8s)
4. The rendered video (54s)

WHAT I NEED TO KNOW:
1. How do I diagnose why the audio is so long? (Is it reading extra content? Is the TTS speed too slow? Are there long pauses?)
2. What's the best way to fix this:
    - Option A: Regenerate the audio with correct speed settings
    - Option B: Speed up the existing audio file to match expected duration
    - Option C: Extend the video timing to match the long audio
3. Once I have correctly-timed audio (~51-52s), how do I adjust the Manim script timing to synchronize properly?
4. What's the final command to combine the video and audio into one file?

TOOLS I HAVE AVAILABLE:
- Manim Community Edition 0.19.x
- ffmpeg and ffprobe
- edge-tts (Microsoft Edge TTS)
- bash scripts

CONSTRAINTS:
- The Manim script uses a custom config: frame_height=10, frame_width=17.78, 1440p resolution
- The video has 5 scenes: Title (2.85s), Parameters (16.07s), Calculation (5.10s), Cancellation (12.32s), Split (15.16s+)
- The narrative describes what appears on screen and must stay synchronized

Can you help me:
1. Analyze what went wrong with the audio generation
2. Provide the exact commands to fix the audio duration
3. Show me how to adjust the Manim script timing if needed
4. Give me the final ffmpeg command to combine them properly

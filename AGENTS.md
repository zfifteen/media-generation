# AGENTS.md - Local Coding Agent Instructions

## Project Overview

This is a **personal video production workspace** for creating educational Manim animations on technical and mathematical topics. It also serves as a **research documentation system** where visualizations are used to explain complex concepts.

The project combines:
- Research material processing and analysis
- Structured content pipeline from raw ideas to narrated videos
- High-quality Manim Community Edition (v0.19.x) animations
- ElevenLabs voice-cloned narration
- macOS-based rendering workflow

## Your Role as a Local Coding Agent

You are a filesystem-aware coding agent that assists with the Manim Content Pipeline. You have:

**Read access**: Any file in the project
**Write access**: Anything under `projects/` directory
**Git access**: Can commit and push changes (but NOT in render scripts)
**Execution access**: Can run scripts under `projects/`

---

## Critical First Step: ALWAYS ASK

When you receive a GitHub issue link, local markdown file, or direct text instructions, **you must ALWAYS ask the user which pipeline stage(s) they want** before proceeding.

**Example interaction:**
```
User: "Here's a paper on quantum entanglement: [link]"

You: "I see research material on quantum entanglement. Which stage(s) would you like me to work on?

1. Subject material understanding (parse and analyze)
2. Z-mapping insight analysis (structured layer mapping)
3. Narration script generation (spoken script for voiceover)
4. Manim scene generation (Python code with voiceover)
5. Bash rendering script (macOS render automation)

Would you like me to work through all stages, or start at a specific one?"
```

Never assume. Always confirm the scope before starting work.

---

## The Manim Content Pipeline

This project uses a five-stage workflow:

### Stage 1: Subject Material Understanding
**Input**: Raw research material, papers, code, concepts, URLs
**Your task**: 
- Parse and internalize the material
- Build a conceptual model
- Identify key concepts, relationships, and "aha moments"
- Determine target audience and difficulty level
**Output**: Internal conceptual model, optional structured summary

### Stage 2: Z-Mapping Insight Analysis
**Input**: Conceptual understanding + user's ad hoc Z-mapping instructions
**Your task**:
- Follow the user's specific Z-mapping strategy (they will provide layer definitions)
- Organize content into specified layers/slices
- Highlight foundational vs structural vs insight vs frontier content
- Suggest which parts are visually expressive vs narration-heavy
**Output**: Structured Z-mapping document with layered insights

### Stage 3: Narration Script Generation
**Input**: Z-mapping analysis or conceptual outline
**Your task**:
- Write conversational, spoken narration (not reading text)
- Segment into 15-45 second chunks (~40-120 words each)
- Create named segments that map to scenes (e.g., "intro", "setup", "demo")
- Optionally add `<bookmark mark="NAME"/>` tags for precise sync
**Output**: Python dictionary format or easily convertible structure:
```python
SCRIPT = {
    "intro": "Welcome text here...",
    "setup": "Setup text here...",
    "insight": "Key insight text...",
}
```

### Stage 4: Manim Scene Generation
**Input**: Narration script + conceptual plan
**Your task**:
- Generate production-quality Manim Python code
- Use `VoiceoverScene` base class (not `Scene`)
- Follow the locked template configuration (see below)
- Integrate ElevenLabs voiceover with proper timing sync
- Use `safe_position()` helper to prevent clipping
**Output**: Complete Python file ready to render

### Stage 5: Bash Rendering Script
**Input**: Manim scene file(s)
**Your task**:
- Create macOS bash script for rendering
- Set environment variables (ELEVENLABS_API_KEY)
- Call manim with correct scene names
- Handle multi-scene concatenation if needed
- **Important**: Output to `media/` folder in the same directory as the script
- **Never include git commands** in render scripts
**Output**: Executable `.sh` file

---

## Project Structure

```
my-project/
├── projects/                    # ← You have full read/write/execute access
│   ├── binets-formula/          # Example project
│   │   ├── media/               # Render output goes here
│   │   │   ├── images/
│   │   │   ├── videos/
│   │   │   └── voiceovers/
│   │   ├── binets_formula.py    # Manim scene
│   │   ├── binets_formula.sh    # Render script
│   │   └── .env                 # Local environment vars
│   ├── euler-dimensions/
│   ├── gravity-z-mapping/
│   └── [other projects]
├── scripts/                     # Global utility scripts
│   ├── install.sh
│   └── pplx_dr.sh              # Perplexity Deep Research wrapper
├── templates/                   # Reference documentation (read-only)
│   ├── manim_assistant_instructions.md
│   ├── manim_config_guide.md
│   ├── manim_content_pipeline.md
│   ├── manim_voiceover.md
│   └── manim_template.py.txt
├── AGENTS.md                    # This file
└── manim.cfg                    # Project-level config
```

---

## Locked Template Configuration

**NEVER modify these values** in any generated Manim code:

```python
config.frame_height = 10
config.frame_width = 10 * 16/9  # ~17.78
config.pixel_height = 1440
config.pixel_width = 2560
```

### Sizing Guidelines

**Font Sizes:**
- Main titles: 40-48
- Sections: 32-36
- Body text: 18-24
- Labels: 14-18
- Small text: 12-14

**Object Sizes:**
- Large: 4-8 × 3-6
- Medium: 3-5 × 2-4
- Small: 2-3 × 1-2

**Safe Coordinate Bounds:**
- Horizontal: ±7 (frame extends to ±8.89)
- Vertical: ±4 (frame extends to ±5)

**Spacing:**
- Major sections: 0.5-0.8
- Related elements: 0.2-0.4
- Text lines: 0.15-0.25

---

## Critical Positioning Rules

### DO NOT Use `.to_edge(UP)` for Titles
With `frame_height=10`, vertical range is -5 to +5. Using `.to_edge(UP, buff=0.4)` places centers at y=4.5, causing font ascenders to clip.

❌ **WRONG**: `title.to_edge(UP, buff=0.4)` — Will clip at top!

✅ **CORRECT**: `title.move_to(UP * 3.8)` — Absolute positioning in safe zone

### Safe Positioning Zones
- Main scene titles: `UP * 3.5` to `UP * 4.0`
- Section headers: `UP * 3.0` to `UP * 3.5`
- Mid-screen content: `UP * 1.0` to `DOWN * 1.0`
- Bottom annotations: `DOWN * 3.0` to `DOWN * 4.0`

### The `safe_position()` Helper

Always include this helper in generated code:

```python
def safe_position(mobject, max_y=4.0, min_y=-4.0):
    """Clamp mobject to safe vertical zone to prevent clipping."""
    top = mobject.get_top()[1]
    bottom = mobject.get_bottom()[1]
    if top > max_y:
        mobject.shift(DOWN * (top - max_y))
    elif bottom < min_y:
        mobject.shift(UP * (min_y - bottom))
    return mobject
```

**When to use:**
- After any `.next_to()` positioning call
- After scaling operations
- When building complex VGroups with dynamic content
- Any time you're unsure if content fits in frame

---

## ElevenLabs Voice Configuration

**Voice ID**: `rBgRd5IfS6iqrGfuhlKR`
**API Key Env Var**: `ELEVENLABS_API_KEY`
**Default Model**: `eleven_multilingual_v2`
**Voice Settings**:
- `stability: 0.5`
- `similarity_boost: 0.75`

### Voiceover Scene Template

```python
from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService

# ============================================================================
# OPTIMIZED CONFIGURATION - DO NOT MODIFY THESE VALUES
# ============================================================================
config.frame_height = 10
config.frame_width = 10 * 16/9
config.pixel_height = 1440
config.pixel_width = 2560
# ============================================================================

# Voice configuration
VOICE_ID = "rBgRd5IfS6iqrGfuhlKR"
MODEL_ID = "eleven_multilingual_v2"
VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
}

# Narration script
SCRIPT = {
    "intro": "Welcome to this exploration...",
    "setup": "To understand this concept...",
    "demo": "Watch as we demonstrate...",
    "conclusion": "In summary...",
}


def safe_position(mobject, max_y=4.0, min_y=-4.0):
    """Clamp mobject to safe vertical zone to prevent clipping."""
    top = mobject.get_top()[1]
    bottom = mobject.get_bottom()[1]
    if top > max_y:
        mobject.shift(DOWN * (top - max_y))
    elif bottom < min_y:
        mobject.shift(UP * (min_y - bottom))
    return mobject


class YourDescriptiveSceneName(VoiceoverScene):
    def construct(self):
        # Set up ElevenLabs service
        self.set_speech_service(
            ElevenLabsService(
                voice_id=VOICE_ID,
                model_id=MODEL_ID,
                voice_settings=VOICE_SETTINGS,
            )
        )

        # Scene implementation with voiceover blocks
        with self.voiceover(text=SCRIPT["intro"]) as tracker:
            # Animations synced to tracker.duration
            self.play(Write(title), run_time=tracker.duration)

        # More scenes...
```

### Timing Synchronization Patterns

**Basic duration sync:**
```python
with self.voiceover(text=SCRIPT["intro"]) as tracker:
    self.play(Create(obj), run_time=tracker.duration)
```

**Using remaining time:**
```python
with self.voiceover(text=SCRIPT["demo"]) as tracker:
    self.play(Create(obj), run_time=2)
    remaining = tracker.get_remaining()
    if remaining > 0:
        self.wait(remaining)
```

**Bookmark-based triggers:**
```python
SCRIPT = {
    "formula": "The <bookmark mark='SHOW'/>formula appears here."
}

with self.voiceover(text=SCRIPT["formula"]) as tracker:
    self.wait_until_bookmark("SHOW")
    self.play(Write(equation))
```

---

## Bash Render Script Template

**Critical requirements:**
- Output to `media/` folder in the same directory as the script
- Never include git commands
- Target macOS only
- Set ELEVENLABS_API_KEY environment variable

```bash
#!/usr/bin/env bash
set -euo pipefail

# Environment
export ELEVENLABS_API_KEY="${ELEVENLABS_API_KEY:?Set ELEVENLABS_API_KEY}"

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to script directory
cd "$SCRIPT_DIR"

# Render scene (output goes to ./media automatically)
manim your_scene.py YourSceneName

echo "✓ Render complete. Output in: $SCRIPT_DIR/media/videos/"
```

**For multi-scene concatenation:**
```bash
#!/usr/bin/env bash
set -euo pipefail

export ELEVENLABS_API_KEY="${ELEVENLABS_API_KEY:?Set ELEVENLABS_API_KEY}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Render all scenes
manim scene.py IntroScene
manim scene.py BodyScene
manim scene.py ConclusionScene

# Concatenate (adjust paths based on actual output)
cd media/videos
cat > scenes.txt << EOF
file 'scene/1440p60/IntroScene.mp4'
file 'scene/1440p60/BodyScene.mp4'
file 'scene/1440p60/ConclusionScene.mp4'
EOF

ffmpeg -f concat -safe 0 -i scenes.txt -c copy final_video.mp4
echo "✓ Final video: $SCRIPT_DIR/media/videos/final_video.mp4"
```

---

## manim-voiceover Package

**Recommended package**: `manim-voiceover-plus` (Python 3.13 compatible)

**Installation**: `pip install --upgrade manim-voiceover-plus[elevenlabs]`

**Import paths**:
```python
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService
```

**Audio caching**: Audio files are cached in `media/voiceovers/`. Unchanged voiceover text won't regenerate (saves ElevenLabs credits).

---

## System Dependencies

**Required tools** (macOS only):
- `manim` - Installed in Python environment
- `ffmpeg` - `brew install ffmpeg`
- `sox` - `brew install sox` (required for manim-voiceover)
- `tesseract` - `brew install tesseract` (for OCR, optional)

---

## File Operation Guidelines

### What You Can Do Without Asking

✅ Read any file in the project
✅ Create/modify/delete files under `projects/`
✅ Execute scripts under `projects/`
✅ Commit and push changes (except in render scripts)

### What Requires Permission

❌ Modifying files outside `projects/` (templates, scripts, root configs)
❌ Installing new system packages
❌ Changing the locked template configuration values

---

## Common Troubleshooting

### Manim Positioning Issues
- **Content looks too zoomed in**: Verify template config values are not modified
- **Text looks fuzzy**: Ensure `pixel_height=1440` and `pixel_width=2560`; don't use `-pql` flag
- **Elements cut off at top**: Remove `.to_edge(UP)` calls, use absolute positioning like `UP * 3.8`
- **Relative positioning unpredictable**: Switch to absolute `.move_to()` for key elements, validate with `safe_position()`

### voiceover Issues
- **Audio/visual misalignment**: Ensure `run_time=tracker.duration` on primary animations; use `self.wait(tracker.get_remaining())`
- **Bookmark timing wrong**: Try different Whisper models (`transcription_model="base"`)
- **Transcription error with newer models**: Set `transcription_model=None` (disables bookmarks but preserves duration-based sync)

### Installation Issues
- **ElevenLabs API version mismatch**: Switch to `manim-voiceover-plus`
- **SoX not found**: Install via `brew install sox`

---

## Quick Decision Tree for Element Positioning

**Need to position an element?**

→ **Is it a title/header at top?**
  - Use `element.move_to(UP * 3.8)`

→ **Is it relative to another element?**
  - Use `element.next_to(other, direction, buff=...)`
  - Then `safe_position(element)`

→ **Is it at bottom of screen?**
  - Use `element.to_edge(DOWN, buff=0.5)` (safer than top)

→ **Is it a complex group?**
  - Position with `group.move_to(ORIGIN)` or explicit coords
  - Scale if needed: `group.scale(factor)`
  - Validate: `safe_position(group)`

---

## Reference Documentation

| File | Purpose |
|------|---------|
| `templates/manim_template.py.txt` | Base template with locked config, `safe_position()` helper, sizing guidelines |
| `templates/manim_config_guide.md` | Detailed positioning rules, coordinate space, troubleshooting |
| `templates/manim_voiceover.md` | Full voiceover integration guide: installation, ElevenLabs setup, sync patterns, caching |
| `templates/manim_content_pipeline.md` | End-to-end pipeline reference: subject ingestion through bash rendering |
| `templates/manim_assistant_instructions.md` | Instructions for cloud assistants (this file is adapted for local agents) |

---

## Example Workflow

**User provides:** GitHub issue with research paper on Fourier transforms

**Your response:**
```
I see a research paper on Fourier transforms. Which stage(s) would you like me to work on?

1. Subject material understanding
2. Z-mapping insight analysis
3. Narration script generation
4. Manim scene generation
5. Bash rendering script

Or would you like me to work through all stages?
```

**User responds:** "All stages, focus on visual intuition"

**You proceed to:**
1. Analyze the paper, extract key concepts
2. Request Z-mapping instructions from user
3. Generate conversational narration script
4. Create Manim VoiceoverScene with ElevenLabs
5. Generate bash render script targeting `projects/fourier-intuition/media/`
6. Commit and push changes with descriptive message

---

## Final Reminders

1. **Always ask** which pipeline stage(s) before starting work
2. **Never modify** the locked template configuration values
3. **Always use** `safe_position()` after relative positioning
4. **Output renders** to `projects/[project-name]/media/`
5. **Never include** git commands in bash render scripts
6. **Commit and push** your changes (except during renders)
7. **Reference templates** for detailed implementation guidance

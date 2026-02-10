# manim-voiceover Integration Guide

## Overview

`manim-voiceover` is the official Manim Community plugin for adding voiceover narration
to Manim animations directly in Python. It eliminates the need for manual audio/video
synchronization via external editors or ffmpeg stitching.

**Key capabilities:**

- Define voiceover text inline with animation code using `with self.voiceover(...)` blocks
- Automatic audio generation via pluggable TTS backends (ElevenLabs, Azure, gTTS, OpenAI, etc.)
- Automatic duration-based sync: animations stretch or Manim waits to match audio length
- Per-word animation triggers via XML bookmark tags and OpenAI Whisper transcription
- Microphone recording mode for manual voiceover capture during render
- Built-in translation support via DeepL for multilingual output

**Repository:** https://github.com/ManimCommunity/manim-voiceover
**PyPI:** https://pypi.org/project/manim-voiceover/

---

## Installation

### Which Package to Install

There are three variants. The choice depends on your Python version and which ElevenLabs
model you need:

| Package | ElevenLabs Support | Python 3.13 | Notes |
|---|---|---|---|
| `manim-voiceover` (upstream) | `elevenlabs<1.0` API | Problematic | Official, but EL integration is outdated |
| `manim-voiceover-plus` | `elevenlabs>=2.1.0` | Supported | Fork with updated EL API |
| `manim-voiceover-enhanced` | `elevenlabs>=2.1.0` | Supported | Another fork, same fix approach |

**Recommended:** Use `manim-voiceover-plus` or `manim-voiceover-enhanced` if you are
using ElevenLabs with Python 3.10+.

### Install Commands

```bash
# Option A: manim-voiceover-plus (recommended for ElevenLabs)
pip install --upgrade "manim-voiceover-plus[elevenlabs]"

# Option B: manim-voiceover-enhanced (alternative fork)
pip install --upgrade "manim-voiceover-enhanced[elevenlabs]"

# Option C: upstream (if NOT using ElevenLabs, or using an older elevenlabs SDK)
pip install "manim-voiceover[elevenlabs]"
```

### Additional Extras

Install only what you need:

```bash
# For per-word timing via Whisper
pip install "manim-voiceover-plus[elevenlabs,transcribe]"

# For translation via DeepL
pip install "manim-voiceover-plus[elevenlabs,translate]"

# For microphone recording
pip install "manim-voiceover-plus[elevenlabs,recorder]"

# Everything
pip install "manim-voiceover-plus[all]"
```

### System Dependency: SoX

manim-voiceover requires SoX (Sound eXchange) for audio processing:

```bash
# macOS
brew install sox

# Ubuntu/Debian
sudo apt install sox

# Windows (via chocolatey)
choco install sox
```

### Environment Variable

Set your ElevenLabs API key as an environment variable:

```bash
export ELEVEN_API_KEY="your_api_key_here"
```

Or in a `.env` file (manim-voiceover reads from `python-dotenv`):

```
ELEVEN_API_KEY=your_api_key_here
```

---

## Core Concepts

### VoiceoverScene

Instead of inheriting from `Scene`, your class inherits from `VoiceoverScene`.
This adds the `self.voiceover()` and `self.set_speech_service()` methods.

```python
from manim_voiceover import VoiceoverScene
# OR for the plus fork:
# from manim_voiceover_plus import VoiceoverScene

class MyScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(...)  # configure TTS backend
        ...
```

**IMPORTANT:** If using `manim-voiceover-plus`, the import path changes:
- `from manim_voiceover_plus import VoiceoverScene`
- `from manim_voiceover_plus.services.elevenlabs import ElevenLabsService`

If using `manim-voiceover-enhanced`, the import path is:
- `from manim_voiceover_fixed import VoiceoverScene`
- `from manim_voiceover_fixed.services.elevenlabs import ElevenLabsService`

### The `with self.voiceover(...)` Block

This is the central mechanism. Wrap animations in a `with` block:

```python
with self.voiceover(text="This circle is drawn as I speak.") as tracker:
    self.play(Create(circle), run_time=tracker.duration)
```

**Behavior:**
- The TTS backend generates audio for the given text
- `tracker.duration` returns the total audio duration in seconds
- `tracker.get_remaining()` returns time left in the voiceover
- If animations finish before the voiceover, Manim waits automatically
- If no `run_time` is set, the animation plays at its default speed and Manim waits
  for the audio to finish

### The Tracker Object

The `tracker` provides timing information for precise sync:

```python
with self.voiceover(text="First we draw, then we transform.") as tracker:
    self.play(Create(circle), run_time=tracker.duration / 2)
    self.play(Transform(circle, square), run_time=tracker.duration / 2)
```

Or using remaining time:

```python
with self.voiceover(text="Draw and then wait for me to finish.") as tracker:
    self.play(Create(circle), run_time=2)
    self.wait(tracker.get_remaining())
```

### Bookmarks (Per-Word Animation Triggers)

Bookmarks let you trigger animations at specific words in the narration:

```python
with self.voiceover(
    text='You simply add an <bookmark mark="A"/>XML tag to trigger animations.'
) as tracker:
    self.wait_until_bookmark("A")
    self.play(Write(sentence))
```

**How it works:**
- Insert `<bookmark mark="NAME"/>` in the voiceover text at the trigger point
- Call `self.wait_until_bookmark("NAME")` to pause until that word is spoken
- Whisper transcription determines the exact timing of each word
- This requires the `transcribe` extra: `pip install "manim-voiceover-plus[transcribe]"`

---

## ElevenLabs Configuration

### Basic Setup

```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService

class MyScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            ElevenLabsService(
                voice_id="YOUR_VOICE_CLONE_ID",
                model_id="eleven_multilingual_v2",
                voice_settings={
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                },
            )
        )
        # ... animations with self.voiceover() blocks
```

### ElevenLabsService Parameters

| Parameter | Type | Description |
|---|---|---|
| `voice_id` | str | The voice ID from your ElevenLabs account (clone or preset) |
| `voice_name` | str | Alternative to voice_id; looks up by name |
| `model_id` | str | TTS model: `eleven_multilingual_v2`, `eleven_turbo_v2_5`, `eleven_v3`, etc. |
| `voice_settings` | dict | `stability` (0-1), `similarity_boost` (0-1), `style` (0-1), `use_speaker_boost` (bool) |
| `output_format` | str | Audio format: `mp3_44100_128` (default), `pcm_44100`, etc. |
| `transcription_model` | str/None | Whisper model for bookmarks. Set to `None` to disable if causing errors |

### Voice Settings Tuning

- **stability** (0.0 to 1.0): Higher = more consistent, lower = more expressive/variable
- **similarity_boost** (0.0 to 1.0): Higher = closer match to original voice, lower = more natural variation
- **style** (0.0 to 1.0): Higher = more expressive delivery (only supported by some models)
- **use_speaker_boost** (bool): Enhances speaker similarity at cost of some generality

**Recommended starting point for voice clones:**

```python
voice_settings={
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": True,
}
```

### Using eleven_v3 Model (Fork Required)

The upstream `manim-voiceover` does not support `eleven_v3`. Use one of the forks:

```python
# With manim-voiceover-enhanced (manim_voiceover_fixed)
from manim_voiceover_fixed import VoiceoverScene
from manim_voiceover_fixed.services.elevenlabs import ElevenLabsService

class MyScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            ElevenLabsService(
                voice_name="Liam",
                model="eleven_v3",
                transcription_model=None,  # workaround for issue #114
            )
        )
```

### Known Issue: Transcription Model Bug

When using newer ElevenLabs models, the Whisper transcription step can fail.
Workaround: set `transcription_model=None` to disable per-word timing.
This disables bookmark functionality but allows basic duration-based sync to work.

---

## Integration with Our Manim Template

### Combining VoiceoverScene with Custom Config

The standard template uses `Scene` as the base class. When adding voiceover,
change the inheritance to `VoiceoverScene`. All other config remains identical.

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


def safe_position(mobject, max_y=4.0, min_y=-4.0):
    top = mobject.get_top()[1]
    bottom = mobject.get_bottom()[1]
    if top > max_y:
        mobject.shift(DOWN * (top - max_y))
    elif bottom < min_y:
        mobject.shift(UP * (min_y - bottom))
    return mobject


# ---------------------------------------------------------------------------
# Voice configuration (edit these per project)
# ---------------------------------------------------------------------------
VOICE_ID = "YOUR_CLONE_ID"          # Swap in clone ID when ready
MODEL_ID = "eleven_multilingual_v2"  # or "eleven_v3" with fork
VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
}


class NarratedScene(VoiceoverScene):
    """Base class for all narrated scenes in this project."""

    def setup_voice(self):
        self.set_speech_service(
            ElevenLabsService(
                voice_id=VOICE_ID,
                model_id=MODEL_ID,
                voice_settings=VOICE_SETTINGS,
            )
        )

    def construct(self):
        self.setup_voice()
        # Override in subclass
```

### Full Example: Narrated Research Scene

```python
class GravityAnomalyExplainer(VoiceoverScene):
    def construct(self):
        # Voice setup
        self.set_speech_service(
            ElevenLabsService(
                voice_id=VOICE_ID,
                model_id=MODEL_ID,
                voice_settings=VOICE_SETTINGS,
            )
        )

        # Title
        title = Text("Gravity Anomalies", font_size=48, weight=BOLD)
        subtitle = Text("Bouguer Correction", font_size=32, color=BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        title_group = VGroup(title, subtitle).move_to(ORIGIN)

        with self.voiceover(
            text="Today we explore gravity anomalies and the Bouguer correction."
        ) as tracker:
            self.play(Write(title_group), run_time=tracker.duration)

        # Transition title to top
        title_group.generate_target()
        title_group.target.scale(0.6).move_to(UP * 3.8)

        with self.voiceover(
            text="The Bouguer correction accounts for the gravitational effect "
                 "of terrain between the observation point and sea level."
        ) as tracker:
            self.play(MoveToTarget(title_group), run_time=2)

            # Show formula
            formula = MathTex(
                r"\Delta g_B = 2 \pi G \rho h",
                font_size=48, color=GOLD
            )
            formula.move_to(ORIGIN)
            self.play(Write(formula), run_time=tracker.get_remaining() - 0.5)

        self.wait(1)
```

---

## Workflow Patterns

### Pattern 1: Develop Fast, Render Final

Use a free/fast TTS backend during development, then switch to ElevenLabs for
the final render. This saves API credits and iteration time.

```python
# During development:
from manim_voiceover.services.gtts import GTTSService

class MyScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        ...

# For final render, change one line:
# self.set_speech_service(ElevenLabsService(voice_id=VOICE_ID, ...))
```

**Tip:** Parameterize the backend selection with an environment variable:

```python
import os

class MyScene(VoiceoverScene):
    def construct(self):
        if os.getenv("MANIM_VOICE_PROD"):
            self.set_speech_service(ElevenLabsService(voice_id=VOICE_ID, ...))
        else:
            self.set_speech_service(GTTSService(lang="en", tld="com"))
```

Then render with:

```bash
# Dev (free, fast)
manim my_scene.py MyScene

# Production (ElevenLabs)
MANIM_VOICE_PROD=1 manim my_scene.py MyScene
```

### Pattern 2: Script-First Workflow

Write all narration text first as a standalone script, then build animations around it.
This mirrors a traditional video production workflow:

```python
SCRIPT = {
    "intro": "Welcome to this exploration of DNA breathing dynamics.",
    "setup": "DNA is not a rigid molecule. It undergoes thermal fluctuations called breathing.",
    "demo": "Watch as the base pairs open and close in response to temperature changes.",
    "conclusion": "These breathing dynamics have implications for gene regulation and drug binding.",
}

class DNABreathing(VoiceoverScene):
    def construct(self):
        self.set_speech_service(ElevenLabsService(voice_id=VOICE_ID, ...))

        with self.voiceover(text=SCRIPT["intro"]) as tracker:
            # title animation
            ...

        with self.voiceover(text=SCRIPT["setup"]) as tracker:
            # DNA structure animation
            ...
```

### Pattern 3: Multi-Scene Video with Consistent Voice

For videos with multiple scenes rendered separately and combined later:

```python
# voice_config.py (shared across scenes)
VOICE_ID = "YOUR_CLONE_ID"
MODEL_ID = "eleven_multilingual_v2"
VOICE_SETTINGS = {"stability": 0.5, "similarity_boost": 0.75}

# scene_01_intro.py
from voice_config import *

class Intro(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            ElevenLabsService(
                voice_id=VOICE_ID,
                model_id=MODEL_ID,
                voice_settings=VOICE_SETTINGS,
            )
        )
        ...

# scene_02_analysis.py
from voice_config import *

class Analysis(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            ElevenLabsService(
                voice_id=VOICE_ID,
                model_id=MODEL_ID,
                voice_settings=VOICE_SETTINGS,
            )
        )
        ...
```

Render each scene separately and concatenate with ffmpeg:

```bash
manim scene_01_intro.py Intro
manim scene_02_analysis.py Analysis
ffmpeg -f concat -i scenes.txt -c copy final_video.mp4
```

### Pattern 4: Bookmark-Driven Precision Sync

For educational content where specific visuals must appear at exact words:

```python
with self.voiceover(
    text='The <bookmark mark="formula"/>formula for gravitational potential is '
         '<bookmark mark="show_eq"/>shown here, where G is the '
         '<bookmark mark="highlight_G"/>gravitational constant.'
) as tracker:
    self.wait_until_bookmark("formula")
    self.play(Write(Text("Formula:", font_size=32).move_to(UP * 2)))

    self.wait_until_bookmark("show_eq")
    eq = MathTex(r"U = -\frac{GMm}{r}", font_size=48)
    self.play(Write(eq))

    self.wait_until_bookmark("highlight_G")
    self.play(eq[0][4].animate.set_color(YELLOW))
```

**Note:** Bookmarks require Whisper transcription. If using a fork with
`transcription_model=None`, bookmarks will not work. Use `tracker.duration`
based sync instead.

---

## Audio Caching

manim-voiceover caches generated audio files locally. This means:

- Re-rendering a scene does NOT re-generate audio if the text has not changed
- Audio files are stored in `media/voiceovers/` by default
- To force regeneration, delete the cache directory or change the text

This is especially important for ElevenLabs where each generation consumes credits.
Unchanged voiceover blocks are free on re-render.

---

## Translation Support

manim-voiceover integrates with DeepL for automatic translation:

```python
from manim_voiceover.translate import get_gettext

# Set up translation function
_ = get_gettext()

class TranslatedScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(ElevenLabsService(voice_id=VOICE_ID, ...))

        with self.voiceover(text=_("This circle is drawn as I speak.")) as tracker:
            self.play(Create(circle), run_time=tracker.duration)
```

Requires `DEEPL_API_KEY` environment variable and the `translate` extra.

---

## Troubleshooting

### Common Issues

| Issue | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: elevenlabs` | Wrong extras installed | `pip install "manim-voiceover-plus[elevenlabs]"` |
| `ElevenLabs API version mismatch` | Upstream package pins old SDK | Switch to `manim-voiceover-plus` or `manim-voiceover-enhanced` |
| `SoX not found` | Missing system dependency | `brew install sox` (macOS) |
| Bookmark timing is wrong | Whisper transcription inaccurate | Try `transcription_model="base"` or `"small"` for better accuracy |
| `transcription_model` error | Incompatible with newer EL models | Set `transcription_model=None` |
| Audio overlaps between scenes | Tracker duration not consumed | Ensure `run_time=tracker.duration` or call `self.wait()` |
| Python 3.13 compatibility | Upstream not updated | Use `manim-voiceover-plus` or `manim-voiceover-enhanced` |

### Debugging Audio Sync

If audio and visuals are misaligned:

1. Check that `run_time=tracker.duration` is set on the primary animation
2. Ensure `self.wait()` calls account for remaining voiceover time
3. Inspect generated audio files in `media/voiceovers/` for unexpected duration
4. Use `tracker.get_remaining()` to fill gaps:
   ```python
   with self.voiceover(text="Long narration here.") as tracker:
       self.play(Create(obj), run_time=3)
       remaining = tracker.get_remaining()
       if remaining > 0:
           self.wait(remaining)
   ```

### Render Command

No special flags needed. The template config handles quality:

```bash
# Standard render (quality baked into config)
manim my_scene.py MyScene

# With caching disabled (forces audio regeneration)
manim my_scene.py MyScene --disable_caching
```

---

## Supported TTS Backends

| Backend | Quality | Cost | Latency | Offline | Install Extra |
|---|---|---|---|---|---|
| ElevenLabs | Excellent | Paid (per char) | Medium | No | `elevenlabs` |
| Azure TTS | Very Good | Paid (per char) | Low | No | `azure` |
| OpenAI TTS | Very Good | Paid (per char) | Medium | No | `openai` |
| gTTS | Decent | Free | Low | No | `gtts` |
| Coqui TTS | Good | Free | High | Yes | `coqui` |
| pyttsx3 | Basic | Free | Instant | Yes | `pyttsx3` |
| Recorder | Your voice | Free | N/A | Yes | `recorder` |

---

## Quick Reference

### Minimal ElevenLabs Scene

```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService

config.frame_height = 10
config.frame_width = 10 * 16/9
config.pixel_height = 1440
config.pixel_width = 2560

class QuickDemo(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            ElevenLabsService(voice_id="YOUR_ID", model_id="eleven_multilingual_v2")
        )
        circle = Circle(color=BLUE)
        with self.voiceover(text="A circle appears.") as tracker:
            self.play(Create(circle), run_time=tracker.duration)
        self.wait(1)
```

### Import Paths by Package

```python
# Upstream (manim-voiceover)
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService

# manim-voiceover-plus
from manim_voiceover_plus import VoiceoverScene
from manim_voiceover_plus.services.elevenlabs import ElevenLabsService

# manim-voiceover-enhanced
from manim_voiceover_fixed import VoiceoverScene
from manim_voiceover_fixed.services.elevenlabs import ElevenLabsService
```

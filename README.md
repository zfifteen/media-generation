# media-generation

Personal video production workspace for creating narrated Manim animations on technical and mathematical research topics. Combines a structured content pipeline, Manim Community Edition rendering, and ElevenLabs voice-cloned narration into a macOS-based workflow.

## Requirements

### Platform

- **macOS only** — all scripts and rendering assume Darwin

### System Dependencies (Homebrew)

| Package | Purpose |
|---|---|
| `cairo` | Vector graphics rendering |
| `pango` | Text layout engine |
| `pkg-config` | Build configuration |
| `ffmpeg` | Video encoding and scene concatenation |
| `sox` | Audio processing (required by manim-voiceover) |
| `mactex-no-gui` | LaTeX distribution for math typesetting (`latex`, `dvisvgm`) |
| `manim` | Manim Community Edition (installed via Homebrew) |

### Python Packages

| Package | Purpose |
|---|---|
| `manim-voiceover-plus[elevenlabs]` | Voiceover integration with ElevenLabs TTS (Python 3.13 compatible fork) |
| `elevenlabs` | ElevenLabs Python SDK for `VoiceSettings` |
| `numpy` | Numerical computation |
| `scipy` | Scientific computing (used in some projects) |

### Environment Variables

| Variable | Required By |
|---|---|
| `ELEVENLABS_API_KEY` | All voiceover-enabled scenes and render scripts |
| `ELEVENLABS_VOICE_ID` | Optional override (defaults to `rBgRd5IfS6iqrGfuhlKR`) |
| `PERPLEXITY_API_KEY` | `scripts/pplx_dr.sh` Deep Research wrapper |

### Installation

Run `scripts/install.sh` to clean-install Manim CE and all Homebrew dependencies from scratch. The script uninstalls any existing 3b1b/manimgl packages first, installs all system deps, and configures the MacTeX PATH.

## Repository Structure

```
media-generation/
├── projects/           # Active project workspace (read/write/execute)
├── scripts/            # Global utility scripts (read-only)
├── templates/          # Reference documentation and base templates (read-only)
├── AGENTS.md           # Local coding agent instructions
├── manim.cfg           # Project-level Manim CLI defaults
└── .gitignore          # Excludes all generated media from version control
```

### `projects/`

Working directory for all video projects. Each subdirectory is a self-contained project that typically includes some combination of:

- Manim Python scene files (`.py`)
- Narration scripts or narrative documents (`.md`)
- Bash render scripts (`.sh`)
- Production instructions or research material

Render output goes to a `media/` folder within each project directory. All generated media (`.mp4`, `.wav`, `.mp3`, `.svg`, `.tex`, `.json`, etc.) is gitignored.

### `scripts/`

| Script | Purpose |
|---|---|
| `install.sh` | macOS Manim CE clean-install — uninstalls old versions, installs Homebrew deps, configures MacTeX PATH |
| `pplx_dr.sh` | Perplexity Deep Research API wrapper using `sonar-deep-research` model for research ingestion |

### `templates/`

Read-only reference documentation for AI assistants (local and cloud) working within this repo.

| File | Purpose |
|---|---|
| `manim_template.py.txt` | Base Manim scene template with locked config and `safe_position()` helper |
| `manim_config_guide.md` | Positioning rules, coordinate space reference, troubleshooting |
| `manim_voiceover.md` | ElevenLabs voiceover integration guide — installation, sync patterns, caching |
| `manim_content_pipeline.md` | End-to-end pipeline reference from subject ingestion through rendering |
| `manim_assistant_instructions.md` | Instructions for cloud-based AI assistants |

## Content Pipeline

The repo follows a five-stage workflow for turning raw research into narrated video:

1. **Subject material understanding** — parse and internalize research material
2. **Z-mapping insight analysis** — organize content into structured insight layers
3. **Narration script generation** — conversational spoken scripts segmented into timed chunks
4. **Manim scene generation** — production-quality Python code with ElevenLabs voiceover integration
5. **Bash rendering** — macOS render scripts that output to `projects/<name>/media/`

Stages are logically ordered but operationally flexible — any stage can be entered independently.

## Render Configuration

All scenes use a locked configuration that must not be modified:

```python
config.frame_height = 10
config.frame_width  = 10 * 16/9   # ~17.78
config.pixel_height = 1440
config.pixel_width  = 2560
```

This produces 1440p (2560×1440) output at 16:9 aspect ratio with a 25% larger-than-default frame for comfortable element spacing.

## Voice Configuration

- **Voice ID**: `rBgRd5IfS6iqrGfuhlKR`
- **Model**: `eleven_multilingual_v2`
- **Stability**: `0.5`
- **Similarity boost**: `0.75`
- **Audio caching**: Files cached in `media/voiceovers/` — unchanged text reuses cached audio

## Agent Instructions

`AGENTS.md` provides comprehensive instructions for local coding agents (GitHub Copilot, Claude Code, etc.) working in this repo. It covers the full pipeline, positioning rules, voiceover patterns, and file access permissions. `templates/manim_assistant_instructions.md` serves the same purpose for cloud-based assistants.

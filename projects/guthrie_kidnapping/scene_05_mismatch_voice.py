"""

Scene 05: Competence Mismatch (with ElevenLabs narration)

Render: manim scene_05_mismatch_voice.py CompetenceMismatchVoice

"""

from manim import *
import numpy as np

# ---------------------------------------------------------------------------
# Bypass manim-voiceover-plus v0.6.9 regression: set_transcription() runs
# its whisper import check BEFORE respecting transcription_model=None.
# ---------------------------------------------------------------------------
import manim_voiceover_plus.services.base as _base

_original_set_transcription = _base.SpeechService.set_transcription


def _patched_set_transcription(self, model=None, kwargs=None):
    if model is None:
        self.transcription_model = None
        self._whisper_model = None
        return
    _original_set_transcription(self, model=model, kwargs=kwargs)


_base.SpeechService.set_transcription = _patched_set_transcription

# ---------------------------------------------------------------------------
from manim_voiceover_plus import VoiceoverScene
from manim_voiceover_plus.services.elevenlabs import ElevenLabsService
from elevenlabs import VoiceSettings

# ============================================================================
# OPTIMIZED CONFIGURATION - DO NOT MODIFY THESE VALUES
# ============================================================================
config.frame_height = 10
config.frame_width = 10 * 16 / 9
config.pixel_height = 1440
config.pixel_width = 2560
# ============================================================================

# ---------------------------------------------------------------------------
# Voice configuration
# ---------------------------------------------------------------------------
VOICE_ID = "rBgRd5IfS6iqrGfuhlKR"
MODEL_ID = "eleven_multilingual_v2"
VOICE_SETTINGS = VoiceSettings(
    stability=0.5,
    similarity_boost=0.75,
)

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
BG_COLOR = "#0d1117"
ACCENT_RED = "#f85149"
ACCENT_GREEN = "#3fb950"
ACCENT_AMBER = "#d29922"
CARD_BG = "#161b22"
BORDER_COLOR = "#30363d"
TEXT_PRIMARY = "#e6edf3"
TEXT_SECONDARY = "#8b949e"

SCRIPT = {
    "title": (
        "This scene focuses on the competence gap in the Nancy Guthrie case: "
        "the difference between the offender's physical tradecraft and the structure "
        "of the so-called ransom operation."
    ),
    "columns": (
        "On the left is the physical operation at the house. "
        "On the right is the ransom architecture that followed. "
        "They do not look like the work of the same level of operator."
    ),
    "evidence": (
        "Physically, the intruder arrives masked, gloved, carrying a backpack and what appears "
        "to be a holstered firearm. They deliberately defeat the doorbell camera in stages and "
        "choose a narrow pre-dawn window. "
        "In contrast, the ransom side has no reply channel, no proof of life, "
        "an unfunded wallet, and deadlines that pass without consequence."
    ),
    "gauges": (
        "If you rate the physical tradecraft, it looks like a high sophistication operation. "
        "If you rate the ransom design on its ability to actually collect money, it is very low."
    ),
    "question": (
        "That gap raises the core analytical question: are we looking at one actor "
        "whose skills are uneven, or two different people splitting the work "
        "between on-scene action and off-scene communication?"
    ),
}


def safe_position(mobject, max_y=4.0, min_y=-4.0):
    top = mobject.get_top()[1]
    bottom = mobject.get_bottom()[1]
    if top > max_y:
        mobject.shift(DOWN * (top - max_y))
    elif bottom < min_y:
        mobject.shift(UP * (min_y - bottom))
    return mobject


class CompetenceMismatchVoice(VoiceoverScene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        self.set_speech_service(
            ElevenLabsService(
                voice_id=VOICE_ID,
                model_id=MODEL_ID,
                voice_settings=VOICE_SETTINGS,
                transcription_model=None,
            )
        )

        # ---------------------------------------------------------------
        # ACT 1: Title card
        # ---------------------------------------------------------------
        title = Text(
            "The Competence Gap",
            font_size=46,
            weight=BOLD,
            color=TEXT_PRIMARY,
        )
        subtitle = Text(
            "Physical Tradecraft vs. Ransom Architecture",
            font_size=22,
            color=TEXT_SECONDARY,
        )
        subtitle.next_to(title, DOWN, buff=0.35)
        title_group = VGroup(title, subtitle).move_to(ORIGIN)

        with self.voiceover(text=SCRIPT["title"]):
            self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)
            self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.6)

        # ---------------------------------------------------------------
        # ACT 2: Column headers
        # ---------------------------------------------------------------
        title_group.generate_target()
        title_group.target.scale(0.55).move_to(UP * 4.0)

        divider = Line(
            LEFT * 7, RIGHT * 7,
            stroke_width=1,
            color=BORDER_COLOR,
            ).move_to(UP * 3.45)

        # Column geometry
        col_left_x = -4.2
        col_right_x = 4.2
        col_top_y = 2.8

        with self.voiceover(text=SCRIPT["columns"]):
            self.play(MoveToTarget(title_group), run_time=0.8)
            self.play(Create(divider), run_time=0.4)

            phys_header = Text(
                "PHYSICAL TRADECRAFT",
                font_size=18,
                weight=BOLD,
                color=ACCENT_GREEN,
            ).move_to(np.array([col_left_x, col_top_y, 0]))

            ransom_header = Text(
                "RANSOM ARCHITECTURE",
                font_size=18,
                weight=BOLD,
                color=ACCENT_RED,
            ).move_to(np.array([col_right_x, col_top_y, 0]))

            self.play(
                FadeIn(phys_header, shift=DOWN * 0.2),
                FadeIn(ransom_header, shift=DOWN * 0.2),
                run_time=0.6,
            )

        # ---------------------------------------------------------------
        # ACT 3: Evidence rows
        # ---------------------------------------------------------------
        phys_items = [
            ("Ski mask, gloves, backpack", "Prepared kit, not improvised"),
            ("Holstered firearm visible", "Coercive control capability"),
            ("Sequential camera defeat", "Hand, then foliage, then damage"),
            ("Head-down anti-ID posture", "Counter-surveillance awareness"),
            ("Pre-dawn timing", "Operational window at about 1:47 a.m."),
        ]

        ransom_items = [
            ("No reply channel provided", "Cannot negotiate or collect"),
            ("Zero proof of life", "Ten days, nothing verifiable"),
            ("Bitcoin wallet at zero", "Never funded, never used"),
            ("Deadlines pass, no action", "No consequences enforced"),
            ("One-way media broadcast", "Not how ransoms normally work"),
        ]

        def make_evidence_card(label_text, detail_text, color, x_center, y_pos):
            label = Text(label_text, font_size=16, color=TEXT_PRIMARY)
            detail = Text(detail_text, font_size=12, color=TEXT_SECONDARY)
            detail.next_to(label, DOWN, buff=0.1, aligned_edge=LEFT)
            text_group = VGroup(label, detail)

            indicator = Dot(
                radius=0.08,
                fill_opacity=1.0,
                color=color,
            )

            row = VGroup(indicator, text_group).arrange(RIGHT, buff=0.25)
            row.move_to(np.array([x_center, y_pos, 0]))
            return row

        start_y = 1.9
        spacing = 0.85

        phys_mobjects = VGroup()
        ransom_mobjects = VGroup()

        for i, (label, detail) in enumerate(phys_items):
            y = start_y - i * spacing
            card = make_evidence_card(label, detail, ACCENT_GREEN, col_left_x, y)
            phys_mobjects.add(card)

        for i, (label, detail) in enumerate(ransom_items):
            y = start_y - i * spacing
            card = make_evidence_card(label, detail, ACCENT_RED, col_right_x, y)
            ransom_mobjects.add(card)

        with self.voiceover(text=SCRIPT["evidence"]):
            for i in range(5):
                self.play(
                    FadeIn(phys_mobjects[i], shift=RIGHT * 0.3),
                    FadeIn(ransom_mobjects[i], shift=LEFT * 0.3),
                    run_time=0.6,
                )

        # ---------------------------------------------------------------
        # ACT 4: Gauges
        # ---------------------------------------------------------------
        # CHANGED: moved gauges up from -3.8 to -3.0 so the question
        # text fits below them without overlapping
        gauge_y = -3.0
        gauge_w = 5.0

        # --- Left gauge (Physical Tradecraft) ---
        phys_gauge_bg = RoundedRectangle(
            width=gauge_w, height=0.45, corner_radius=0.22,
            fill_color=CARD_BG, fill_opacity=1.0,
            stroke_color=BORDER_COLOR, stroke_width=1.5,
        ).move_to(np.array([col_left_x, gauge_y, 0]))

        phys_gauge_fill = RoundedRectangle(
            width=0.01, height=0.35, corner_radius=0.17,
            fill_color=ACCENT_GREEN, fill_opacity=0.85,
            stroke_width=0,
        )
        phys_gauge_fill.move_to(phys_gauge_bg)
        phys_gauge_fill.align_to(phys_gauge_bg, LEFT).shift(RIGHT * 0.05)

        phys_gauge_label = Text(
            "HIGH", font_size=14, weight=BOLD, color=ACCENT_GREEN,
        ).next_to(phys_gauge_bg, RIGHT, buff=0.3)

        # --- Right gauge (Ransom Architecture) ---
        ransom_gauge_bg = RoundedRectangle(
            width=gauge_w, height=0.45, corner_radius=0.22,
            fill_color=CARD_BG, fill_opacity=1.0,
            stroke_color=BORDER_COLOR, stroke_width=1.5,
        ).move_to(np.array([col_right_x, gauge_y, 0]))

        ransom_gauge_fill = RoundedRectangle(
            width=0.01, height=0.35, corner_radius=0.17,
            fill_color=ACCENT_RED, fill_opacity=0.85,
            stroke_width=0,
        )
        ransom_gauge_fill.move_to(ransom_gauge_bg)
        ransom_gauge_fill.align_to(ransom_gauge_bg, LEFT).shift(RIGHT * 0.05)

        ransom_gauge_label = Text(
            "LOW", font_size=14, weight=BOLD, color=ACCENT_RED,
        ).next_to(ransom_gauge_bg, RIGHT, buff=0.3)

        phys_gauge_title = Text(
            "Operational Sophistication",
            font_size=14, color=TEXT_SECONDARY,
        ).next_to(phys_gauge_bg, UP, buff=0.2)

        ransom_gauge_title = Text(
            "Collection Viability",
            font_size=14, color=TEXT_SECONDARY,
        ).next_to(ransom_gauge_bg, UP, buff=0.2)

        with self.voiceover(text=SCRIPT["gauges"]):
            self.play(
                FadeIn(phys_gauge_bg),
                FadeIn(ransom_gauge_bg),
                FadeIn(phys_gauge_title),
                FadeIn(ransom_gauge_title),
                run_time=0.5,
            )

            phys_target = phys_gauge_fill.copy()
            phys_target.stretch_to_fit_width(gauge_w * 0.85)
            phys_target.move_to(phys_gauge_bg)
            phys_target.align_to(phys_gauge_bg, LEFT).shift(RIGHT * 0.05)

            ransom_target = ransom_gauge_fill.copy()
            ransom_target.stretch_to_fit_width(gauge_w * 0.15)
            ransom_target.move_to(ransom_gauge_bg)
            ransom_target.align_to(ransom_gauge_bg, LEFT).shift(RIGHT * 0.05)

            self.add(phys_gauge_fill, ransom_gauge_fill)
            self.play(
                Transform(phys_gauge_fill, phys_target),
                Transform(ransom_gauge_fill, ransom_target),
                run_time=2.0,
                rate_func=rate_functions.ease_out_cubic,
            )

            self.play(
                FadeIn(phys_gauge_label, shift=LEFT * 0.2),
                FadeIn(ransom_gauge_label, shift=LEFT * 0.2),
                run_time=0.4,
            )

        # ---------------------------------------------------------------
        # ACT 5: Core question
        # ---------------------------------------------------------------
        # CHANGED: position relative to the gauge bottoms instead of a
        # hardcoded y-value, with enough buff to sit cleanly below
        gauge_group_bottom = VGroup(phys_gauge_bg, ransom_gauge_bg)

        question = Text(
            "Same actor, or two different people?",
            font_size=24,
            weight=BOLD,
            color=ACCENT_AMBER,
        )
        question.next_to(gauge_group_bottom, DOWN, buff=0.6)
        # Use a more generous lower bound so it does not clamp back up
        safe_position(question, min_y=-4.6)

        with self.voiceover(text=SCRIPT["question"]):
            self.play(FadeIn(question, shift=UP * 0.3), run_time=0.8)

        # ---------------------------------------------------------------
        # Fade out
        # ---------------------------------------------------------------
        all_objects = VGroup(
            title_group, divider,
            phys_header, ransom_header,
            phys_mobjects, ransom_mobjects,
            phys_gauge_bg, phys_gauge_fill, phys_gauge_label, phys_gauge_title,
            ransom_gauge_bg, ransom_gauge_fill, ransom_gauge_label, ransom_gauge_title,
            question,
        )
        self.play(FadeOut(all_objects), run_time=1.2)
        self.wait(0.5)

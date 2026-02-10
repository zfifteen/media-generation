"""
Binet's Formula: The Self-Correcting Formula
A narrated Manim animation exploring the deep structure of Binet's Formula
and the golden ratio's unique self-correction property.

Render with:
    manim binets_formula.py BinetFormulaSelfCorrection
"""

from manim import *
import numpy as np
import os

# Attempt manim-voiceover-plus first, fall back to upstream
try:
    from manim_voiceover_plus import VoiceoverScene
    from manim_voiceover_plus.services.elevenlabs import ElevenLabsService
except ImportError:
    from manim_voiceover import VoiceoverScene
    from manim_voiceover.services.elevenlabs import ElevenLabsService

# Import VoiceSettings model from elevenlabs
from elevenlabs import VoiceSettings

# ============================================================================
# OPTIMIZED CONFIGURATION - DO NOT MODIFY THESE VALUES
# ============================================================================
config.frame_height = 10
config.frame_width = 10 * 16/9
config.pixel_height = 1440
config.pixel_width = 2560
# ============================================================================

# ---------------------------------------------------------------------------
# Voice configuration (reads from environment)
# ---------------------------------------------------------------------------
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "rBgRd5IfS6iqrGfuhlKR")
MODEL_ID = "eleven_multilingual_v2"
VOICE_SETTINGS = VoiceSettings(
    stability=0.5,
    similarity_boost=0.75,
)

# ---------------------------------------------------------------------------
# Narration script
# ---------------------------------------------------------------------------
SCRIPT = {
    "hook": (
        "How do irrational numbers produce perfect whole numbers? "
        "The Fibonacci sequence is simple. Each number is just the sum of the two before it. "
        "One, one, two, three, five, eight, thirteen, and so on. "
        "But there is a formula that skips all the adding and jumps straight to any position. "
        "The catch? It is built entirely from square roots and irrational constants. "
        "And yet, every single time, it lands on a whole number. Why?"
    ),

    "the_formula": (
        "This is Binet's Formula. "
        "It has two main pieces. "
        "The first uses phi, the golden ratio, "
        "roughly one point six one eight. "
        "The second uses psi, phi's algebraic conjugate, "
        "roughly negative zero point six one eight. "
        "Both contain the square root of five. "
        "Both are irrational. "
        "And both are divided by the square root of five again. "
        "So how does this mess of irrationals always produce an integer?"
    ),

    "the_standard_story": (
        "The textbook answer is that the irrational parts cancel. "
        "Let's test that. Plug in n equals five. "
        "Phi to the fifth gives us about eleven point oh nine. "
        "Psi to the fifth gives us about negative zero point oh nine. "
        "Subtract, divide by the square root of five, and you get exactly five. "
        "But calling this cancellation is misleading. "
        "The two terms are not equal and opposite. One is enormous. The other is tiny. "
        "Something deeper is going on."
    ),

    "split_the_signal": (
        "Let's split the formula into two roles. "
        "The phi term is the signal. "
        "It carries almost all the value. "
        "The psi term is the correction. "
        "It is a small nudge that lands the signal exactly on the nearest integer. "
        "Think of it this way. "
        "Phi to the n, divided by root five, overshoots or undershoots a whole number by a tiny amount. "
        "Psi to the n, divided by root five, is precisely the size of that overshoot. "
        "Subtract it, and you are exactly on the integer. Every time."
    ),

    "the_decay": (
        "Now here is what makes this remarkable. "
        "The correction term does not just shrink. "
        "It shrinks by a factor of exactly zero point six one eight at every single step. "
        "That number is one over phi. The reciprocal of the golden ratio. "
        "At n equals one, the correction is about twenty eight percent of the rounding tolerance. "
        "By n equals five, it is under one percent. "
        "By n equals ten, it is six thousandths of a percent. "
        "Watch the table build. "
        "The correction collapses toward zero, and the ratio between consecutive corrections is always the same constant."
    ),

    "the_golden_lock": (
        "This is the core insight. "
        "The golden ratio is not just the growth rate of the Fibonacci sequence. "
        "It is also, simultaneously, the rate at which the formula corrects its own irrational residue. "
        "Growth and self-correction are governed by the same constant, just inverted. "
        "Phi drives the signal up. One over phi pulls the error down. "
        "They are locked together by a simple algebraic fact: "
        "phi times psi equals negative one. "
        "This is called the norm of the golden ratio in the number ring Z of phi. "
        "It is not a coincidence. It is a conservation law."
    ),

    "why_only_fibonacci": (
        "Could another recurrence do the same thing? "
        "Let's check. "
        "Take the recurrence x squared equals x plus two. "
        "Its correction term does not decay at all. It oscillates between plus and minus one. Rounding fails immediately. "
        "Take x squared equals two x plus one. "
        "Its correction at step one is zero point seven oh seven, which exceeds the rounding tolerance of zero point five. "
        "The Fibonacci recurrence hits zero point two seven six at step one. "
        "Comfortably below the threshold, and shrinking from there. "
        "Among all unit-norm quadratic recurrences, this is the tightest safe margin that still works at every step."
    ),

    "practical_threshold": (
        "This is not just theory. It has a computational consequence. "
        "When you implement Binet's Formula in floating-point arithmetic, "
        "the correction term eventually shrinks below your machine's precision floor. "
        "For standard double precision, that crossover happens around n equals seventy. "
        "Past that point, the algebraic self-correction is smaller than the noise in your floating-point numbers. "
        "The formula still gives the right answer, but only by luck, not by structure. "
        "That is when you should switch to matrix exponentiation or arbitrary-precision arithmetic."
    ),

    "closing": (
        "So here is the real story of Binet's Formula. "
        "Fibonacci numbers are not integers despite the irrationals in the formula. "
        "They are integers because of a conservation law built into the golden ratio itself. "
        "The same constant that makes the sequence grow is the constant that makes the formula self-correct. "
        "And no other quadratic recurrence does this as tightly or as cleanly. "
        "The golden ratio is not just beautiful. It is uniquely necessary."
    ),
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def safe_position(mobject, max_y=4.0, min_y=-4.0):
    """Clamp mobject to safe vertical zone to prevent clipping."""
    top = mobject.get_top()[1]
    bottom = mobject.get_bottom()[1]
    if top > max_y:
        mobject.shift(DOWN * (top - max_y))
    elif bottom < min_y:
        mobject.shift(UP * (min_y - bottom))
    return mobject


# ============================================================================
# MAIN SCENE
# ============================================================================

class BinetFormulaSelfCorrection(VoiceoverScene):
    """
    Complete narrated animation of the Binet's Formula insight:
    The golden ratio simultaneously governs growth and self-correction.
    """

    def construct(self):
        # Voice setup
        self.set_speech_service(
            ElevenLabsService(
                voice_id=VOICE_ID,
                model_id=MODEL_ID,
                voice_settings=VOICE_SETTINGS,
                transcription_model=None,
            )
        )

        # Scene sequence
        self.scene_hook()
        self.scene_the_formula()
        self.scene_the_standard_story()
        self.scene_split_the_signal()
        self.scene_the_decay()
        self.scene_the_golden_lock()
        self.scene_why_only_fibonacci()
        self.scene_practical_threshold()
        self.scene_closing()

    # ------------------------------------------------------------------------
    # Scene 1: hook
    # ------------------------------------------------------------------------
    def scene_hook(self):
        with self.voiceover(text=SCRIPT["hook"]) as tracker:
            question = Text(
                "How do irrational numbers\nmake perfect integers?",
                font_size=40,
                color=YELLOW,
                line_spacing=1.2,
            )
            question.move_to(ORIGIN)
            self.play(FadeIn(question, shift=UP * 0.5), run_time=2)

            fib_seq = Text(
                "1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89...",
                font_size=32,
                color=WHITE,
            )
            fib_seq.next_to(question, DOWN, buff=1.0)
            safe_position(fib_seq)

            self.play(Write(fib_seq), run_time=2)

        self.play(FadeOut(question), FadeOut(fib_seq))

    # ------------------------------------------------------------------------
    # Scene 2: the_formula
    # ------------------------------------------------------------------------
    def scene_the_formula(self):
        title = Text("Binet's Formula", font_size=42, weight=BOLD, color=GOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=1)

        binet = MathTex(
            r"F_n = \frac{1}{\sqrt{5}} \left[ \left(\frac{1+\sqrt{5}}{2}\right)^n - \left(\frac{1-\sqrt{5}}{2}\right)^n \right]",
            font_size=36,
        )
        binet.move_to(ORIGIN)

        with self.voiceover(text=SCRIPT["the_formula"]) as tracker:
            self.play(Write(binet), run_time=3)

            phi_label = MathTex(r"\varphi \approx 1.618", font_size=28, color=GOLD)
            phi_label.next_to(binet, DOWN, buff=0.8).shift(LEFT * 2)

            psi_label = MathTex(r"\psi \approx -0.618", font_size=28, color=BLUE)
            psi_label.next_to(binet, DOWN, buff=0.8).shift(RIGHT * 2)

            safe_position(phi_label)
            safe_position(psi_label)

            self.play(FadeIn(phi_label, shift=UP * 0.3), run_time=1)
            self.play(FadeIn(psi_label, shift=UP * 0.3), run_time=1)

        self.clear()
        self.add(title)

    # ------------------------------------------------------------------------
    # Scene 3: the_standard_story
    # ------------------------------------------------------------------------
    def scene_the_standard_story(self):
        title = Text("Binet's Formula", font_size=42, weight=BOLD, color=GOLD)
        title.move_to(UP * 3.8)
        self.add(title)

        story_text = Text(
            '"The irrational parts cancel"',
            font_size=32,
            slant=ITALIC,
            color=GRAY,
        )
        story_text.move_to(UP * 2.5)

        with self.voiceover(text=SCRIPT["the_standard_story"]) as tracker:
            self.play(Write(story_text), run_time=1.5)

            demo = MathTex(
                r"n=5: \quad \varphi^5 \approx 11.09, \quad \psi^5 \approx -0.09",
                font_size=28,
            )
            demo.move_to(UP * 0.5)
            self.play(Write(demo), run_time=2)

            result = MathTex(r"F_5 = 5", font_size=36, color=GREEN)
            result.next_to(demo, DOWN, buff=0.5)
            self.play(Write(result), run_time=1)

            cross = Line(
                story_text.get_left() + LEFT * 0.2,
                story_text.get_right() + RIGHT * 0.2,
                color=RED,
                stroke_width=6,
            )
            self.play(Create(cross), run_time=0.8)

        self.play(FadeOut(story_text), FadeOut(cross), FadeOut(demo), FadeOut(result))

    # ------------------------------------------------------------------------
    # Scene 4: split_the_signal
    # ------------------------------------------------------------------------
    def scene_split_the_signal(self):
        title = Text("Binet's Formula", font_size=42, weight=BOLD, color=GOLD)
        title.move_to(UP * 3.8)
        self.add(title)

        signal_label = Text("Signal", font_size=28, color=GOLD)
        signal_label.move_to(UP * 2 + LEFT * 3)

        correction_label = Text("Correction", font_size=28, color=BLUE)
        correction_label.move_to(UP * 2 + RIGHT * 3)

        signal_formula = MathTex(
            r"\frac{\varphi^n}{\sqrt{5}}",
            font_size=32,
            color=GOLD,
        )
        signal_formula.next_to(signal_label, DOWN, buff=0.5)

        correction_formula = MathTex(
            r"\frac{\psi^n}{\sqrt{5}}",
            font_size=32,
            color=BLUE,
        )
        correction_formula.next_to(correction_label, DOWN, buff=0.5)

        with self.voiceover(text=SCRIPT["split_the_signal"]) as tracker:
            self.play(
                Write(signal_label),
                Write(signal_formula),
                run_time=1.5,
            )

            self.play(
                Write(correction_label),
                Write(correction_formula),
                run_time=1.5,
            )

            number_line = NumberLine(
                x_range=[0, 10, 1],
                length=10,
                include_numbers=True,
                font_size=20,
            )
            number_line.move_to(DOWN * 1.5)

            self.play(Create(number_line), run_time=2)

        self.clear()

    # ------------------------------------------------------------------------
    # Scene 5: the_decay
    # ------------------------------------------------------------------------
    def scene_the_decay(self):
        title = Text("Exponential Decay", font_size=42, weight=BOLD, color=GOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=1)

        decay_label = MathTex(
            r"\text{Decay rate: } |\psi| = \frac{1}{\varphi} \approx 0.618",
            font_size=28,
            color=BLUE,
        )
        decay_label.move_to(UP * 2.8)

        with self.voiceover(text=SCRIPT["the_decay"]) as tracker:
            self.play(Write(decay_label), run_time=2)

            table_data = [
                ["n", "Correction", "% of 0.5"],
                ["1", "0.276", "55.3%"],
                ["5", "0.040", "8.1%"],
                ["10", "0.0036", "0.7%"],
            ]

            table = Table(
                table_data,
                include_outer_lines=True,
                line_config={"stroke_width": 1, "color": WHITE},
            ).scale(0.5)
            table.move_to(DOWN * 0.5)

            self.play(Create(table), run_time=3)

        self.clear()

    # ------------------------------------------------------------------------
    # Scene 6: the_golden_lock
    # ------------------------------------------------------------------------
    def scene_the_golden_lock(self):
        title = Text("The Golden Lock", font_size=42, weight=BOLD, color=GOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=1)

        with self.voiceover(text=SCRIPT["the_golden_lock"]) as tracker:
            growth_text = Text("Growth = φ", font_size=28, color=GOLD)
            growth_text.move_to(UP * 1.5 + LEFT * 3)

            correction_text = Text("Correction = 1/φ", font_size=28, color=BLUE)
            correction_text.move_to(UP * 1.5 + RIGHT * 3)

            self.play(Write(growth_text), Write(correction_text), run_time=2)

            norm_eq = MathTex(
                r"\varphi \times \psi = -1",
                font_size=36,
                color=YELLOW,
            )
            norm_eq.move_to(ORIGIN)

            self.play(Write(norm_eq), run_time=2)

        self.clear()

    # ------------------------------------------------------------------------
    # Scene 7: why_only_fibonacci
    # ------------------------------------------------------------------------
    def scene_why_only_fibonacci(self):
        title = Text("Why Only Fibonacci?", font_size=42, weight=BOLD, color=GOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=1)

        with self.voiceover(text=SCRIPT["why_only_fibonacci"]) as tracker:
            comp_table = [
                ["Recurrence", "Correction at n=1", "Status"],
                ["x² = x+1 (Fib)", "0.276", "✓ Pass"],
                ["x² = x+2", "Oscillates", "✗ Fail"],
                ["x² = 2x+1", "0.707", "✗ Fail"],
            ]

            comparison = Table(
                comp_table,
                include_outer_lines=True,
                line_config={"stroke_width": 1, "color": WHITE},
            ).scale(0.45)
            comparison.move_to(ORIGIN)

            self.play(Create(comparison), run_time=4)

            gauge_label = Text(
                "Fibonacci: 0.276 < 0.5 ✓",
                font_size=28,
                color=GREEN,
            )
            gauge_label.move_to(DOWN * 3)
            self.play(Write(gauge_label), run_time=1.5)

        self.clear()

    # ------------------------------------------------------------------------
    # Scene 8: practical_threshold
    # ------------------------------------------------------------------------
    def scene_practical_threshold(self):
        title = Text("Computational Limit", font_size=42, weight=BOLD, color=GOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=1)

        with self.voiceover(text=SCRIPT["practical_threshold"]) as tracker:
            threshold_text = Text(
                "Double precision crossover: n ≈ 70",
                font_size=30,
                color=RED,
            )
            threshold_text.move_to(UP * 1.5)

            self.play(Write(threshold_text), run_time=2)

            advice = Text(
                "Beyond n=70: Use matrix exponentiation",
                font_size=26,
                color=YELLOW,
            )
            advice.move_to(DOWN * 0.5)
            self.play(FadeIn(advice, shift=UP * 0.3), run_time=2)

        self.clear()

    # ------------------------------------------------------------------------
    # Scene 9: closing
    # ------------------------------------------------------------------------
    def scene_closing(self):
        with self.voiceover(text=SCRIPT["closing"]) as tracker:
            final_statement = Text(
                "The golden ratio is uniquely necessary.",
                font_size=38,
                color=GOLD,
                weight=BOLD,
            )
            final_statement.move_to(ORIGIN)

            self.play(Write(final_statement), run_time=3)

        self.play(FadeOut(final_statement), run_time=1.5)

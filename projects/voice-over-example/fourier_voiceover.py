"""
fourier_voiceover.py
Five-minute narrated explainer: The Fourier Transform
Manim Community Edition + manim-voiceover (ElevenLabs)
"""

from manim import *
import numpy as np
import os

from manim_voiceover_plus import VoiceoverScene                            # NEW
from manim_voiceover_plus.services.elevenlabs import ElevenLabsService     # NEW


# If you are on Python 3.13+ or need the updated ElevenLabs SDK, swap imports:
# from manim_voiceover_plus import VoiceoverScene
# from manim_voiceover_plus.services.elevenlabs import ElevenLabsService

# ============================================================================
# OPTIMIZED CONFIGURATION -- DO NOT MODIFY THESE VALUES
# ============================================================================
config.frame_height = 10
config.frame_width  = 10 * 16 / 9   # ~17.78
config.pixel_height = 1440
config.pixel_width  = 2560
# ============================================================================

# ---------------------------------------------------------------------------
# Voice configuration (edit per project)
# ---------------------------------------------------------------------------
VOICE_ID       = "rBgRd5IfS6iqrGfuhlKR"
MODEL_ID       = "eleven_multilingual_v2"
VOICE_SETTINGS = {
    "stability":        0.5,
    "similarity_boost":  0.75,
}

# ---------------------------------------------------------------------------
# Narration script (~782 words, ~5.2 min at 150 wpm)
# ---------------------------------------------------------------------------
SCRIPT = {
    "intro_title": (
        "Welcome to this visual exploration of the Fourier Transform, "
        "one of the most powerful and beautiful ideas in all of mathematics. "
        "Over the next few minutes, we will build an intuition for what this "
        "transform does, why it works, and why it matters in the real world."
    ),
    "what_is_it": (
        "At its core, the Fourier Transform takes a complex signal and breaks "
        "it down into simple sine waves. Think of it like a prism splitting "
        "white light into a rainbow of individual colors. Each color represents "
        "a different frequency hidden inside the original signal. This idea, "
        "first proposed by Joseph Fourier in 1807, was so radical that even the "
        "great mathematician Lagrange doubted it. Fourier claimed that any "
        "periodic function, no matter how complex, could be represented as a "
        "sum of sines and cosines. He was right, and that insight changed "
        "mathematics forever."
    ),
    "sine_wave_intro": (
        "Let us start with the building blocks: sine waves. A single sine wave "
        "is defined by three properties. First, its frequency, which controls "
        "how fast it oscillates. Second, its amplitude, which controls how tall "
        "or strong the wave is. And third, its phase, which shifts the entire "
        "wave left or right along the time axis. Every sound you hear, every "
        "radio signal, every vibration in nature can be described using "
        "combinations of these simple waves."
    ),
    "show_frequency": (
        "Watch how changing the frequency affects the shape of a sine wave. "
        "A low frequency produces a slow, gentle oscillation, like a deep "
        "bass note. As we gradually increase the frequency, the wave oscillates "
        "faster and faster, producing higher and higher pitched tones. "
        "The frequency is measured in Hertz, which simply means cycles per second."
    ),
    "show_amplitude": (
        "Now let us examine amplitude. When the amplitude is small, the wave "
        "barely moves above and below the center line. As we increase the "
        "amplitude, the wave grows taller, carrying more energy with each "
        "oscillation. In sound, a larger amplitude means a louder signal. "
        "In light, it means a brighter beam."
    ),
    "combination": (
        "Here is where things get truly interesting. What happens when we add "
        "multiple sine waves together? Let us start by combining two waves "
        "with different frequencies. Notice how the result already looks more "
        "complex than either individual wave. Now let us add a third wave. "
        "The combined signal looks nothing like a simple sine wave anymore. "
        "It has bumps, dips, and intricate patterns. But remember, underneath "
        "all that complexity, it is just three simple sine waves added together."
    ),
    "decomposition_concept": (
        "The Fourier Transform performs the reverse operation. Given any "
        "complex signal, no matter how messy or irregular it appears, the "
        "transform tells us exactly which frequencies are present and how "
        "strong each one is. The output of this process is called the "
        "frequency spectrum. It is like an ingredients list for the signal, "
        "showing the recipe of sine waves that, when combined, reproduce "
        "the original."
    ),
    "formula": (
        "Mathematically, the continuous Fourier Transform is defined by this "
        "integral. For a time domain function f of t, we multiply it by a "
        "complex exponential, e to the negative two pi i f t, and integrate "
        "over all time from negative infinity to positive infinity. The result, "
        "capital F of f, is a complex number for each frequency. Its magnitude "
        "tells us the strength of that frequency, and its angle tells us "
        "the phase."
    ),
    "visual_wrapping": (
        "There is a beautiful geometric way to understand this. Imagine taking "
        "your signal and wrapping it around a circle, like winding a wire "
        "around a spool. You try different winding speeds. For most speeds, "
        "the wrapped signal distributes itself evenly around the circle, and "
        "the center of mass stays near the origin. But when the winding "
        "frequency matches a frequency actually present in the signal, "
        "something special happens. The wrapped curve bunches up on one side, "
        "and the center of mass shifts away from the origin. That shift is "
        "precisely what the Fourier Transform measures."
    ),
    "applications": (
        "The Fourier Transform is everywhere in modern technology. It compresses "
        "your MP3 music files by identifying which frequencies your ear notices "
        "most. It powers MRI machines in hospitals, reconstructing detailed "
        "images of your body from raw radio wave signals. It enables active "
        "noise cancellation in your headphones by analyzing and inverting "
        "unwanted frequencies in real time. It forms the backbone of all "
        "wireless communication, from Wi-Fi to cellular networks to satellite "
        "links. Even image compression formats like JPEG use a closely related "
        "variant called the Discrete Cosine Transform."
    ),
    "outro": (
        "The Fourier Transform reveals the hidden structure within complexity. "
        "No matter how tangled a signal looks when plotted against time, the "
        "frequency domain tells a cleaner, more illuminating story. It is a "
        "lens that lets us see the world in terms of its fundamental "
        "oscillations. Thank you for watching this visual journey through one "
        "of mathematics' greatest and most practical tools."
    ),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def safe_position(mobject, max_y=4.0, min_y=-4.0):
    top    = mobject.get_top()[1]
    bottom = mobject.get_bottom()[1]
    if top > max_y:
        mobject.shift(DOWN * (top - max_y))
    elif bottom < min_y:
        mobject.shift(UP * (min_y - bottom))
    return mobject


def make_sine_graph(axes, freq=1.0, amp=1.0, phase=0.0, color=BLUE):
    return axes.plot(
        lambda t: amp * np.sin(2 * np.pi * freq * t + phase),
        color=color,
    )


# ============================================================================
# SCENE
# ============================================================================

class FourierExplainer(VoiceoverScene):
    def construct(self):
        # --- Voice service (toggle with env var) ---
        if os.getenv("MANIM_VOICE_PROD"):
            self.set_speech_service(
                ElevenLabsService(
                    voice_id=VOICE_ID,
                    model_id=MODEL_ID,
                    voice_settings=VOICE_SETTINGS,
                )
            )
        else:
            from manim_voiceover.services.gtts import GTTSService
            self.set_speech_service(GTTSService(lang="en", tld="com"))

        self.camera.background_color = "#0e1117"

        # =================================================================
        # 1. TITLE (~19 s)
        # =================================================================
        title = Text(
            "The Fourier Transform", font_size=48, weight=BOLD, color=WHITE
        )
        subtitle = Text(
            "Seeing the Hidden Frequencies", font_size=32, color=BLUE
        )
        subtitle.next_to(title, DOWN, buff=0.3)
        title_group = VGroup(title, subtitle).move_to(ORIGIN)

        with self.voiceover(text=SCRIPT["intro_title"]) as tracker:
            self.play(Write(title), run_time=tracker.duration * 0.5)
            self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=tracker.duration * 0.3)
            self.wait(tracker.get_remaining())

        # Shrink title to top
        title_group.generate_target()
        title_group.target.scale(0.5).move_to(UP * 4.2)
        self.play(MoveToTarget(title_group), run_time=1)

        # =================================================================
        # 2. WHAT IS THE FOURIER TRANSFORM? (~37 s)
        # =================================================================
        prism = Triangle(color=WHITE, fill_opacity=0.15).scale(1.2)
        prism.move_to(LEFT * 1)

        white_arrow = Arrow(LEFT * 4, prism.get_left(), color=WHITE, buff=0.1)
        rainbow_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        rainbow_arrows = VGroup()
        for i, c in enumerate(rainbow_colors):
            angle = (i - 2.5) * 0.18
            end = prism.get_right() + RIGHT * 3 + UP * angle * 5
            arr = Arrow(prism.get_right(), end, color=c, buff=0.1, stroke_width=3)
            rainbow_arrows.add(arr)

        prism_group = VGroup(white_arrow, prism, rainbow_arrows).move_to(DOWN * 0.5)

        with self.voiceover(text=SCRIPT["what_is_it"]) as tracker:
            self.play(FadeIn(prism), GrowArrow(white_arrow), run_time=3)
            self.play(
                LaggedStart(
                    *[GrowArrow(a) for a in rainbow_arrows],
                    lag_ratio=0.15,
                ),
                run_time=4,
            )
            self.wait(tracker.get_remaining())

        self.play(FadeOut(prism_group), run_time=1)

        # =================================================================
        # 3. SINE WAVE BUILDING BLOCKS (~30 s)
        # =================================================================
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-2, 2, 1],
            x_length=12,
            y_length=5,
            axis_config={"include_tip": False, "color": GREY_B},
        ).move_to(DOWN * 0.3)
        x_label = axes.get_x_axis_label("t", direction=RIGHT)
        y_label = axes.get_y_axis_label("y", direction=UP)

        sine_graph = make_sine_graph(axes, freq=1.0, amp=1.5, color=BLUE)

        freq_label = Text("Frequency", font_size=20, color=YELLOW).next_to(axes, DOWN, buff=0.4).shift(LEFT * 3)
        amp_label  = Text("Amplitude", font_size=20, color=GREEN).next_to(freq_label, RIGHT, buff=1.5)
        phase_label = Text("Phase", font_size=20, color=RED).next_to(amp_label, RIGHT, buff=1.5)

        with self.voiceover(text=SCRIPT["sine_wave_intro"]) as tracker:
            self.play(Create(axes), Write(x_label), Write(y_label), run_time=2)
            self.play(Create(sine_graph), run_time=3)
            self.play(
                FadeIn(freq_label), FadeIn(amp_label), FadeIn(phase_label),
                run_time=2,
            )
            self.wait(tracker.get_remaining())

        self.play(
            FadeOut(freq_label), FadeOut(amp_label), FadeOut(phase_label),
            run_time=0.5,
        )

        # =================================================================
        # 4. FREQUENCY DEMO (~22 s)
        # =================================================================
        freq_tracker = ValueTracker(0.5)

        dynamic_sine = always_redraw(
            lambda: make_sine_graph(
                axes,
                freq=freq_tracker.get_value(),
                amp=1.5,
                color=BLUE,
            )
        )
        freq_text = always_redraw(
            lambda: Text(
                f"f = {freq_tracker.get_value():.1f} Hz",
                font_size=24,
                color=YELLOW,
            ).move_to(axes.c2p(3.5, 1.8))
        )

        self.remove(sine_graph)
        self.add(dynamic_sine, freq_text)

        with self.voiceover(text=SCRIPT["show_frequency"]) as tracker:
            self.play(
                freq_tracker.animate.set_value(4.0),
                run_time=tracker.duration - 1,
                rate_func=smooth,
            )
            self.wait(tracker.get_remaining())

        self.remove(dynamic_sine, freq_text)

        # =================================================================
        # 5. AMPLITUDE DEMO (~20 s)
        # =================================================================
        amp_tracker = ValueTracker(0.2)

        dynamic_amp = always_redraw(
            lambda: make_sine_graph(
                axes,
                freq=2.0,
                amp=amp_tracker.get_value(),
                color=GREEN,
            )
        )
        amp_text = always_redraw(
            lambda: Text(
                f"A = {amp_tracker.get_value():.1f}",
                font_size=24,
                color=GREEN,
            ).move_to(axes.c2p(3.5, 1.8))
        )

        self.add(dynamic_amp, amp_text)

        with self.voiceover(text=SCRIPT["show_amplitude"]) as tracker:
            self.play(
                amp_tracker.animate.set_value(1.8),
                run_time=tracker.duration - 1,
                rate_func=smooth,
            )
            self.wait(tracker.get_remaining())

        self.play(FadeOut(dynamic_amp), FadeOut(amp_text), run_time=0.5)

        # =================================================================
        # 6. COMBINING WAVES (~31 s)
        # =================================================================
        wave1 = make_sine_graph(axes, freq=1, amp=1.0, color=RED)
        wave2 = make_sine_graph(axes, freq=2.5, amp=0.6, color=YELLOW)
        wave3 = make_sine_graph(axes, freq=4, amp=0.4, color=TEAL)

        combined_2 = axes.plot(
            lambda t: 1.0 * np.sin(2 * np.pi * 1 * t) +
                      0.6 * np.sin(2 * np.pi * 2.5 * t),
            color=PURPLE,
        )
        combined_3 = axes.plot(
            lambda t: 1.0 * np.sin(2 * np.pi * 1 * t) +
                      0.6 * np.sin(2 * np.pi * 2.5 * t) +
                      0.4 * np.sin(2 * np.pi * 4 * t),
            color=WHITE,
        )

        l1 = Text("f=1 Hz", font_size=16, color=RED).move_to(axes.c2p(3.8, 1.6))
        l2 = Text("f=2.5 Hz", font_size=16, color=YELLOW).next_to(l1, DOWN, buff=0.15)
        l3 = Text("f=4 Hz", font_size=16, color=TEAL).next_to(l2, DOWN, buff=0.15)

        with self.voiceover(text=SCRIPT["combination"]) as tracker:
            self.play(Create(wave1), FadeIn(l1), run_time=3)
            self.play(Create(wave2), FadeIn(l2), run_time=3)
            self.play(
                ReplacementTransform(VGroup(wave1, wave2), combined_2),
                run_time=3,
            )
            self.wait(2)
            self.play(Create(wave3), FadeIn(l3), run_time=2)
            self.play(
                ReplacementTransform(VGroup(combined_2, wave3), combined_3),
                run_time=3,
            )
            self.wait(tracker.get_remaining())

        self.play(
            FadeOut(combined_3), FadeOut(l1), FadeOut(l2), FadeOut(l3),
            run_time=1,
        )

        # =================================================================
        # 7. DECOMPOSITION CONCEPT (~26 s)
        # =================================================================
        messy_signal = axes.plot(
            lambda t: (
                    1.0 * np.sin(2 * np.pi * 1 * t) +
                    0.6 * np.sin(2 * np.pi * 2.5 * t) +
                    0.4 * np.sin(2 * np.pi * 4 * t)
            ),
            color=GREY_A,
        )

        spectrum_axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 1.2, 0.5],
            x_length=12,
            y_length=4,
            axis_config={"include_tip": False, "color": GREY_B},
        ).move_to(DOWN * 0.5)
        spec_x = spectrum_axes.get_x_axis_label("f (Hz)", direction=RIGHT)
        spec_y = spectrum_axes.get_y_axis_label("Amplitude", direction=UP)

        bars = VGroup()
        bar_data = [(1, 1.0, RED), (2.5, 0.6, YELLOW), (4, 0.4, TEAL)]
        for freq, amp, color in bar_data:
            bar = Rectangle(
                width=0.5, height=amp * 3, color=color, fill_opacity=0.7,
            )
            bar.move_to(spectrum_axes.c2p(freq, amp / 2))
            bar.align_to(spectrum_axes.c2p(freq, 0), DOWN)
            bars.add(bar)

        with self.voiceover(text=SCRIPT["decomposition_concept"]) as tracker:
            self.play(Create(messy_signal), run_time=2)
            self.wait(2)
            self.play(
                FadeOut(messy_signal), FadeOut(axes),
                FadeOut(x_label), FadeOut(y_label),
                run_time=1,
            )
            self.play(Create(spectrum_axes), Write(spec_x), Write(spec_y), run_time=2)
            self.play(
                LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3),
                run_time=4,
            )
            self.wait(tracker.get_remaining())

        self.play(
            FadeOut(spectrum_axes), FadeOut(spec_x),
            FadeOut(spec_y), FadeOut(bars),
            run_time=1,
        )

        # =================================================================
        # 8. THE FORMULA (~30 s)
        # =================================================================
        formula = MathTex(
            r"\hat{f}(\xi) = \int_{-\infty}^{\infty} "
            r"f(t)\, e^{-2\pi i \xi t}\, dt",
            font_size=48,
            color=GOLD,
        ).move_to(ORIGIN)

        label_ft = Text("Time domain signal", font_size=18, color=BLUE)
        label_ft.next_to(formula, DOWN, buff=0.6).shift(LEFT * 2)

        label_exp = Text("Complex exponential", font_size=18, color=GREEN)
        label_exp.next_to(label_ft, RIGHT, buff=1.5)

        label_out = Text("Frequency domain output", font_size=18, color=GOLD)
        label_out.next_to(formula, UP, buff=0.6)

        with self.voiceover(text=SCRIPT["formula"]) as tracker:
            self.play(Write(formula), run_time=5)
            self.play(FadeIn(label_out), run_time=1.5)
            self.play(FadeIn(label_ft), run_time=1.5)
            self.play(FadeIn(label_exp), run_time=1.5)
            self.wait(tracker.get_remaining())

        self.play(
            FadeOut(formula), FadeOut(label_ft),
            FadeOut(label_exp), FadeOut(label_out),
            run_time=1,
        )

        # =================================================================
        # 9. WINDING / WRAPPING VISUALIZATION (~38 s)
        # =================================================================
        wrap_circle = Circle(radius=2, color=GREY_B, stroke_opacity=0.3)
        wrap_circle.move_to(ORIGIN)
        dot_center = Dot(ORIGIN, color=WHITE, radius=0.06)

        wind_freq = ValueTracker(0.1)
        signal_func = lambda t: 1.0 + (
                1.0 * np.sin(2 * np.pi * 2 * t) +
                0.5 * np.sin(2 * np.pi * 5 * t)
        )

        NUM_PTS = 400
        t_vals = np.linspace(0, 2, NUM_PTS)

        def get_wound_curve():
            wf = wind_freq.get_value()
            pts = []
            for t in t_vals:
                r = signal_func(t) * 0.8
                angle = 2 * np.pi * wf * t
                pts.append([r * np.cos(angle), r * np.sin(angle), 0])
            curve = VMobject(color=BLUE, stroke_width=2)
            curve.set_points_smoothly(pts)
            return curve

        wound_curve = always_redraw(get_wound_curve)

        def get_com_dot():
            wf = wind_freq.get_value()
            cx, cy = 0.0, 0.0
            for t in t_vals:
                r = signal_func(t) * 0.8
                angle = 2 * np.pi * wf * t
                cx += r * np.cos(angle)
                cy += r * np.sin(angle)
            cx /= NUM_PTS
            cy /= NUM_PTS
            return Dot([cx, cy, 0], color=YELLOW, radius=0.1)

        com_dot = always_redraw(get_com_dot)

        wind_label = always_redraw(
            lambda: Text(
                f"Winding freq = {wind_freq.get_value():.1f} Hz",
                font_size=22,
                color=YELLOW,
            ).move_to(DOWN * 3.8)
        )

        with self.voiceover(text=SCRIPT["visual_wrapping"]) as tracker:
            self.play(Create(wrap_circle), FadeIn(dot_center), run_time=2)
            self.add(wound_curve, com_dot, wind_label)
            self.play(
                wind_freq.animate.set_value(7.0),
                run_time=tracker.duration - 4,
                rate_func=linear,
            )
            self.wait(tracker.get_remaining())

        self.play(
            FadeOut(wrap_circle), FadeOut(dot_center),
            FadeOut(wound_curve), FadeOut(com_dot), FadeOut(wind_label),
            run_time=1,
        )

        # =================================================================
        # 10. APPLICATIONS (~35 s)
        # =================================================================
        app_data = [
            ("MP3 Compression",    "musical_note", BLUE),
            ("MRI Imaging",        "hospital",     GREEN),
            ("Noise Cancellation", "headphones",   RED),
            ("Wi-Fi / 5G",        "antenna",       YELLOW),
            ("JPEG Images",        "image",        PURPLE),
        ]

        app_icons = VGroup()
        for i, (label_text, _icon, color) in enumerate(app_data):
            box = RoundedRectangle(
                width=3, height=1.5, corner_radius=0.2,
                color=color, fill_opacity=0.15, stroke_width=2,
            )
            lbl = Text(label_text, font_size=20, color=color)
            lbl.move_to(box)
            group = VGroup(box, lbl)
            app_icons.add(group)

        app_icons.arrange_in_grid(rows=2, cols=3, buff=0.5)
        app_icons.move_to(DOWN * 0.2)
        safe_position(app_icons)

        apps_title = Text(
            "Applications of the Fourier Transform",
            font_size=36, color=WHITE,
        ).move_to(UP * 3.2)

        with self.voiceover(text=SCRIPT["applications"]) as tracker:
            self.play(Write(apps_title), run_time=2)
            self.play(
                LaggedStart(
                    *[FadeIn(icon, shift=UP * 0.3) for icon in app_icons],
                    lag_ratio=0.4,
                ),
                run_time=6,
            )
            self.wait(tracker.get_remaining())

        self.play(FadeOut(app_icons), FadeOut(apps_title), run_time=1)

        # =================================================================
        # 11. OUTRO (~24 s)
        # =================================================================
        self.play(FadeOut(title_group), run_time=0.5)

        outro_text = Text(
            "The Fourier Transform",
            font_size=48,
            weight=BOLD,
            color=GOLD,
        ).move_to(UP * 1)

        tagline = Text(
            "Revealing hidden structure in complexity",
            font_size=28,
            color=GREY_A,
        ).next_to(outro_text, DOWN, buff=0.4)

        thanks = Text(
            "Thank you for watching",
            font_size=24,
            color=BLUE,
        ).next_to(tagline, DOWN, buff=0.6)

        with self.voiceover(text=SCRIPT["outro"]) as tracker:
            self.play(Write(outro_text), run_time=3)
            self.play(FadeIn(tagline, shift=UP * 0.2), run_time=2)
            self.play(FadeIn(thanks, shift=UP * 0.2), run_time=2)
            self.wait(tracker.get_remaining())

        self.play(
            FadeOut(outro_text), FadeOut(tagline), FadeOut(thanks),
            run_time=2,
        )
        self.wait(1)

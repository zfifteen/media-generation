from manim import *
import numpy as np

config.frame_height = 10
config.frame_width = 10 * 16/9
config.pixel_height = 1440
config.pixel_width = 2560
config.background_color = "#0a0a0a"

def safe_position(mobject, max_y=4.0, min_y=-4.0):
    top = mobject.get_top()[1]
    bottom = mobject.get_bottom()[1]
    if top > max_y:
        mobject.shift(DOWN * (top - max_y))
    elif bottom < min_y:
        mobject.shift(UP * (min_y - bottom))
    return mobject

class Scene04_NewtonThird(Scene):
    def construct(self):
        header = Text("Breaking Newton's Third Law?", font_size=38, weight=BOLD, color=WHITE)
        header.move_to(UP * 3.8)

        # Newton's third law text
        law_text = Text("Every action has an equal and opposite reaction.", font_size=22, color=GREY_B)
        law_text.move_to(UP * 2.5)

        # Strike-through effect
        strike = Line(
            law_text.get_left() + LEFT * 0.1,
            law_text.get_right() + RIGHT * 0.1,
            color="#ff4444", stroke_width=3
        )

        # Ferry metaphor
        ferry_big = VGroup(
            RoundedRectangle(width=2.5, height=0.8, corner_radius=0.15,
                             color="#ff6f61", fill_opacity=0.6, stroke_width=2),
            Text("Large Ferry", font_size=14, color=WHITE)
        ).arrange(DOWN, buff=0.05).move_to(LEFT * 3 + DOWN * 0.5)

        ferry_small = VGroup(
            RoundedRectangle(width=1.4, height=0.5, corner_radius=0.1,
                             color="#ffd700", fill_opacity=0.6, stroke_width=2),
            Text("Small Ferry", font_size=14, color=WHITE)
        ).arrange(DOWN, buff=0.05).move_to(RIGHT * 3 + DOWN * 0.5)

        # Water waves
        waves = VGroup()
        for i in range(3):
            wave_arc = Arc(radius=0.8 + i * 0.4, angle=PI/2, start_angle=-PI/4,
                           color="#00bfff", stroke_width=1.5, stroke_opacity=0.5 - i * 0.12)
            wave_arc.move_to(LEFT * 1 + DOWN * 0.5)
            waves.add(wave_arc)

        # Explanation
        expl = Text(
            "The 'missing' momentum is carried away\nby the scattered sound waves.",
            font_size=20, color="#00bfff", line_spacing=1.3
        )
        expl.move_to(DOWN * 2.5)

        momentum_note = Text(
            "Total momentum is conserved.",
            font_size=18, color="#44ff44"
        )
        momentum_note.move_to(DOWN * 3.5)

        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.5)
        self.play(Write(law_text), run_time=1.0)
        self.play(Create(strike), run_time=0.5)
        self.play(
            FadeIn(ferry_big), FadeIn(ferry_small), FadeIn(waves),
            run_time=1.0
        )

        # Animate ferries: small one rocks more
        self.play(
            ferry_small.animate.shift(RIGHT * 0.4),
            ferry_big.animate.shift(LEFT * 0.1),
            rate_func=there_and_back, run_time=1.0
        )
        self.play(
            ferry_small.animate.shift(LEFT * 0.3),
            ferry_big.animate.shift(RIGHT * 0.08),
            rate_func=there_and_back, run_time=1.0
        )

        self.play(FadeIn(expl), run_time=0.7)
        self.play(FadeIn(momentum_note), run_time=0.7)
        self.wait(1.6)

        all_objs = VGroup(header, law_text, strike, ferry_big, ferry_small, waves, expl, momentum_note)
        self.play(FadeOut(all_objs), run_time=1.0)

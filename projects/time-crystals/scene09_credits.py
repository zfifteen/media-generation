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

class Scene09_Credits(Scene):
    def construct(self):
        # Recap line
        recap = Text(
            "A desktop experiment revealed time crystals\nhiding in a cushion of sound.",
            font_size=26, color=GREY_B, line_spacing=1.4
        )
        recap.move_to(UP * 1.5)

        # Decorative line
        line = Line(LEFT * 4, RIGHT * 4, color="#00bfff", stroke_width=2)
        line.move_to(UP * 0.2)

        # Attribution
        attribution = Text("Big D'", font_size=36, weight=BOLD, color=WHITE)
        attribution.move_to(DOWN * 0.8)

        handle = Text("@alltheputs", font_size=20, color="#00bfff")
        handle.next_to(attribution, DOWN, buff=0.3)

        # Source
        source = Text(
            "Source: Morrell, Elliott & Grier\nPhys. Rev. Lett. (2025)",
            font_size=16, color=GREY_C, line_spacing=1.3
        )
        source.move_to(DOWN * 2.5)

        # Decorative beads (callback to opening)
        bead_large = Circle(radius=0.3, color="#ff6f61", fill_opacity=0.4, stroke_width=2)
        bead_large.move_to(LEFT * 5.5 + DOWN * 3.0)
        bead_small = Circle(radius=0.18, color="#ffd700", fill_opacity=0.4, stroke_width=2)
        bead_small.move_to(RIGHT * 5.5 + DOWN * 2.8)

        self.play(FadeIn(recap), run_time=1.0)
        self.play(Create(line), run_time=0.5)
        self.play(FadeIn(attribution), FadeIn(handle), run_time=0.8)
        self.play(FadeIn(source), run_time=0.6)
        self.play(FadeIn(bead_large), FadeIn(bead_small), run_time=0.5)

        # Hold -- no fade out at end
        self.wait(6.6)

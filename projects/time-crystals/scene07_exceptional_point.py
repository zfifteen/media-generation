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

class Scene07_ExceptionalPoint(Scene):
    def construct(self):
        header = Text("The Tipping Point", font_size=40, weight=BOLD, color=WHITE)
        header.move_to(UP * 3.8)

        # Horizontal line representing parameter space
        param_line = Line(LEFT * 6, RIGHT * 6, color=GREY_C, stroke_width=2)
        param_line.move_to(UP * 0.5)

        param_label = Text("Size Asymmetry", font_size=16, color=GREY_C)
        param_label.next_to(param_line, DOWN, buff=0.3)

        # Two mode dots starting apart
        mode1 = Dot(color="#00bfff", radius=0.15).move_to(LEFT * 3 + UP * 0.5)
        mode2 = Dot(color="#ff6f61", radius=0.15).move_to(RIGHT * 3 + UP * 0.5)

        mode1_label = Text("Symmetric Mode", font_size=15, color="#00bfff")
        mode1_label.next_to(mode1, UP, buff=0.3)
        mode2_label = Text("Breathing Mode", font_size=15, color="#ff6f61")
        mode2_label.next_to(mode2, UP, buff=0.3)

        # Exceptional point marker (rotated square as diamond)
        ep_marker = Square(color="#ffd700", fill_opacity=0.8, stroke_width=2).scale(0.2).rotate(PI/4)
        ep_marker.move_to(UP * 0.5)
        ep_label = Text("Exceptional\nPoint", font_size=16, color="#ffd700", line_spacing=1.2)
        ep_label.next_to(ep_marker, DOWN, buff=0.5)

        # Before EP (left region)
        left_region = Text("Stationary\n(Overdamped)", font_size=16, color=GREY_B, line_spacing=1.2)
        left_region.move_to(LEFT * 4.5 + DOWN * 2.0)

        # After EP (right region)
        right_region = Text("Time Crystal!\n(Self-Oscillating)", font_size=16, color="#44ff44", line_spacing=1.2)
        right_region.move_to(RIGHT * 4.5 + DOWN * 2.0)

        # Divider
        divider = DashedLine(UP * 0.5, DOWN * 3.0, color="#ffd700", stroke_width=1.5, dash_length=0.15)

        explanation = Text(
            "When modes merge, the system tips into spontaneous oscillation.",
            font_size=20, color=GREY_B
        )
        explanation.move_to(DOWN * 3.5)
        safe_position(explanation)

        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.5)
        self.play(Create(param_line), FadeIn(param_label), run_time=0.6)
        self.play(
            FadeIn(mode1), FadeIn(mode1_label),
            FadeIn(mode2), FadeIn(mode2_label),
            run_time=0.7
        )
        self.play(FadeIn(left_region), run_time=0.5)

        # Modes approach each other
        self.play(
            mode1.animate.move_to(LEFT * 0.3 + UP * 0.5),
            mode1_label.animate.move_to(LEFT * 0.3 + UP * 1.2),
            mode2.animate.move_to(RIGHT * 0.3 + UP * 0.5),
            mode2_label.animate.move_to(RIGHT * 0.3 + UP * 1.2),
            run_time=2.0
        )

        # Merge at EP
        self.play(
            mode1.animate.move_to(UP * 0.5),
            mode2.animate.move_to(UP * 0.5),
            FadeOut(mode1_label), FadeOut(mode2_label),
            run_time=1.0
        )
        self.play(
            FadeIn(ep_marker, scale=2), FadeIn(ep_label),
            Create(divider),
            run_time=0.8
        )
        self.play(FadeIn(right_region), run_time=0.5)
        self.play(FadeIn(explanation), run_time=0.5)

        self.wait(1.9)

        all_objs = VGroup(header, param_line, param_label, mode1, mode2,
                          ep_marker, ep_label, left_region, right_region,
                          divider, explanation)
        self.play(FadeOut(all_objs), run_time=1.0)

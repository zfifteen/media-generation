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

class Scene05_TimeCrystal(Scene):
    def construct(self):
        header = Text("From Imbalance to Time Crystal", font_size=38, weight=BOLD, color=WHITE)
        header.move_to(UP * 3.8)

        # Phase space axes
        axes = Axes(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=5, y_length=5,
            axis_config={"color": GREY_C, "stroke_width": 1.5, "include_ticks": False},
        ).move_to(LEFT * 0.5 + DOWN * 0.3)

        x_label = Text("Position", font_size=16, color=GREY_B)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Velocity", font_size=16, color=GREY_B)
        y_label.next_to(axes.y_axis, LEFT, buff=0.2)

        # Limit cycle (ellipse)
        limit_cycle = Ellipse(width=3.5, height=3.0, color="#00bfff", stroke_width=3)
        limit_cycle.move_to(axes.get_center())

        # Dot tracing the limit cycle
        trace_dot = Dot(color="#ffd700", radius=0.1)
        trace_dot.move_to(limit_cycle.point_from_proportion(0))

        # Label
        lc_label = Text("Limit Cycle", font_size=18, color="#00bfff")
        lc_label.next_to(limit_cycle, RIGHT, buff=0.5).shift(UP * 0.5)

        # Right side explanation - FIXED SPACING
        expl_lines = VGroup(
            Text("The beads spontaneously", font_size=18, color=GREY_B),
            Text("enter a stable orbit.", font_size=18, color=GREY_B),
            Text("", font_size=6),  # Spacer
            Text("No external clock.", font_size=18, color="#ffd700"),
            Text("No periodic driving.", font_size=18, color="#ffd700"),
            Text("", font_size=6),  # Spacer
            Text("~61 cycles/second.", font_size=18, color="#00bfff"),
            Text("Runs for hours.", font_size=18, color="#00bfff"),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 5.2 + DOWN * 0.3)
        safe_position(expl_lines)

        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.5)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.0)
        self.play(Create(limit_cycle), FadeIn(lc_label), run_time=1.0)
        self.play(FadeIn(trace_dot), run_time=0.3)

        # Trace around the limit cycle
        self.play(
            MoveAlongPath(trace_dot, limit_cycle),
            run_time=3.0, rate_func=linear
        )

        self.play(FadeIn(expl_lines), run_time=0.8)
        self.wait(2.4)

        all_objs = VGroup(header, axes, x_label, y_label, limit_cycle, trace_dot, lc_label, expl_lines)
        self.play(FadeOut(all_objs), run_time=1.0)

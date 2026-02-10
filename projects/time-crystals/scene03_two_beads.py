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

class Scene03_TwoBeads(Scene):
    def construct(self):
        header = Text("Two Beads, One Strange Dance", font_size=38, weight=BOLD, color=WHITE)
        header.move_to(UP * 3.8)

        # Large bead
        large_bead = Circle(radius=0.5, color="#ff6f61", fill_opacity=0.7, stroke_width=3)
        large_bead.move_to(LEFT * 2)
        large_label = Text("Large", font_size=18, color="#ff6f61")
        large_label.next_to(large_bead, DOWN, buff=0.3)

        # Small bead
        small_bead = Circle(radius=0.28, color="#ffd700", fill_opacity=0.7, stroke_width=3)
        small_bead.move_to(RIGHT * 2)
        small_label = Text("Small", font_size=18, color="#ffd700")
        small_label.next_to(small_bead, DOWN, buff=0.3)

        # Force arrows (nonreciprocal)
        arrow_big = Arrow(
            start=large_bead.get_right() + RIGHT * 0.15,
            end=small_bead.get_left() + LEFT * 0.15,
            color="#ff6f61", stroke_width=5, max_tip_length_to_length_ratio=0.12
        ).shift(UP * 0.3)
        arrow_big_label = Text("Strong push", font_size=14, color="#ff6f61")
        arrow_big_label.next_to(arrow_big, UP, buff=0.15)

        arrow_small = Arrow(
            start=small_bead.get_left() + LEFT * 0.15,
            end=large_bead.get_right() + RIGHT * 0.15,
            color="#ffd700", stroke_width=2, max_tip_length_to_length_ratio=0.12
        ).shift(DOWN * 0.3)
        arrow_small_label = Text("Weak push back", font_size=14, color="#ffd700")
        arrow_small_label.next_to(arrow_small, DOWN, buff=0.15)

        # Explanation
        explanation = Text(
            "Different sizes scatter sound differently,\ncreating an imbalanced push.",
            font_size=20, color=GREY_B, line_spacing=1.3
        )
        explanation.move_to(DOWN * 2.5)

        bead_group = VGroup(large_bead, large_label, small_bead, small_label)

        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.5)
        self.play(FadeIn(bead_group), run_time=0.8)
        self.play(
            GrowArrow(arrow_big), FadeIn(arrow_big_label),
            run_time=0.8
        )
        self.play(
            GrowArrow(arrow_small), FadeIn(arrow_small_label),
            run_time=0.8
        )
        self.play(FadeIn(explanation), run_time=0.6)

        # Animate the imbalance: small bead moves more
        for _ in range(3):
            self.play(
                small_bead.animate.shift(RIGHT * 0.25),
                large_bead.animate.shift(LEFT * 0.08),
                rate_func=there_and_back, run_time=0.8
            )

        self.wait(1.5)

        all_objs = VGroup(header, bead_group, arrow_big, arrow_big_label,
                          arrow_small, arrow_small_label, explanation)
        self.play(FadeOut(all_objs), run_time=1.0)

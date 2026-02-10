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

class Scene06_EnergyFlow(Scene):
    def construct(self):
        header = Text("Energy Flow", font_size=40, weight=BOLD, color=WHITE)
        header.move_to(UP * 3.8)

        # Three boxes
        box_sound = RoundedRectangle(width=3.5, height=1.8, corner_radius=0.2,
                                      color="#00bfff", fill_opacity=0.15, stroke_width=2)
        label_sound = VGroup(
            Text("Sound Field", font_size=22, weight=BOLD, color="#00bfff"),
            Text("(Static, 40 kHz)", font_size=15, color=GREY_C)
        ).arrange(DOWN, buff=0.1)
        sound_group = VGroup(box_sound, label_sound).move_to(LEFT * 5 + DOWN * 0.2)

        box_beads = RoundedRectangle(width=3.5, height=1.8, corner_radius=0.2,
                                      color="#ffd700", fill_opacity=0.15, stroke_width=2)
        label_beads = VGroup(
            Text("Bead Pair", font_size=22, weight=BOLD, color="#ffd700"),
            Text("(Oscillating)", font_size=15, color=GREY_C)
        ).arrange(DOWN, buff=0.1)
        beads_group = VGroup(box_beads, label_beads).move_to(DOWN * 0.2)

        box_air = RoundedRectangle(width=3.5, height=1.8, corner_radius=0.2,
                                    color="#ff6f61", fill_opacity=0.15, stroke_width=2)
        label_air = VGroup(
            Text("Air (Drag)", font_size=22, weight=BOLD, color="#ff6f61"),
            Text("(Dissipation)", font_size=15, color=GREY_C)
        ).arrange(DOWN, buff=0.1)
        air_group = VGroup(box_air, label_air).move_to(RIGHT * 5 + DOWN * 0.2)

        # Arrows
        arrow_in = Arrow(
            sound_group.get_right(), beads_group.get_left(),
            color="#00bfff", stroke_width=4, buff=0.15,
            max_tip_length_to_length_ratio=0.12
        )
        label_in = Text("Energy In", font_size=16, color="#00bfff")
        label_in.next_to(arrow_in, UP, buff=0.15)

        arrow_out = Arrow(
            beads_group.get_right(), air_group.get_left(),
            color="#ff6f61", stroke_width=4, buff=0.15,
            max_tip_length_to_length_ratio=0.12
        )
        label_out = Text("Energy Out", font_size=16, color="#ff6f61")
        label_out.next_to(arrow_out, UP, buff=0.15)

        # Balance annotation
        balance = Text("Energy In = Energy Out  >>  Stable Oscillation", font_size=20, color="#44ff44")
        balance.move_to(DOWN * 2.8)

        mechanism = Text(
            "Nonreciprocal scattering extracts energy\nfrom the standing wave each cycle.",
            font_size=18, color=GREY_B, line_spacing=1.3
        )
        mechanism.move_to(DOWN * 3.7)
        safe_position(mechanism)

        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.5)
        self.play(FadeIn(sound_group), run_time=0.6)
        self.play(GrowArrow(arrow_in), FadeIn(label_in), run_time=0.6)
        self.play(FadeIn(beads_group), run_time=0.6)
        self.play(GrowArrow(arrow_out), FadeIn(label_out), run_time=0.6)
        self.play(FadeIn(air_group), run_time=0.6)
        self.play(FadeIn(balance), run_time=0.6)
        self.play(FadeIn(mechanism), run_time=0.5)

        # Pulse the beads box to show active oscillation
        self.play(
            box_beads.animate.set_fill(opacity=0.35),
            rate_func=there_and_back, run_time=1.0
        )
        self.play(
            box_beads.animate.set_fill(opacity=0.35),
            rate_func=there_and_back, run_time=1.0
        )

        self.wait(1.3)

        all_objs = VGroup(header, sound_group, beads_group, air_group,
                          arrow_in, label_in, arrow_out, label_out, balance, mechanism)
        self.play(FadeOut(all_objs), run_time=1.0)

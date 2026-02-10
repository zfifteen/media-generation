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

class Scene02_AcousticLevitation(Scene):
    def construct(self):
        header = Text("Acoustic Levitation", font_size=40, weight=BOLD, color=WHITE)
        header.move_to(UP * 3.8)

        # Speaker (top)
        speaker_top = VGroup(
            Rectangle(width=3, height=0.5, color="#888888", fill_opacity=0.8),
            Text("Speaker Array", font_size=14, color=WHITE)
        ).arrange(DOWN, buff=0.15).move_to(UP * 2.5)

        # Speaker (bottom)
        speaker_bot = VGroup(
            Rectangle(width=3, height=0.5, color="#888888", fill_opacity=0.8),
            Text("Reflector", font_size=14, color=WHITE)
        ).arrange(UP, buff=0.15).move_to(DOWN * 3.0)

        # Standing wave
        wave_left = VGroup()
        wave_right = VGroup()
        y_range = np.linspace(-2.3, 1.8, 200)
        amp = 0.8
        points_l = [np.array([-amp * np.sin(2 * np.pi * y / 1.7), y, 0]) for y in y_range]
        points_r = [np.array([amp * np.sin(2 * np.pi * y / 1.7), y, 0]) for y in y_range]

        wave_curve_l = VMobject(color="#00bfff", stroke_width=2, stroke_opacity=0.5)
        wave_curve_l.set_points_smoothly(points_l)
        wave_curve_r = VMobject(color="#00bfff", stroke_width=2, stroke_opacity=0.5)
        wave_curve_r.set_points_smoothly(points_r)

        # Pressure nodes (where beads sit)
        nodes = VGroup()
        node_labels = VGroup()
        node_positions = [-2.3 + 1.7/2 + i * 1.7/2 for i in range(5)]
        # Only show nodes that are within vertical range
        node_positions = [p for p in node_positions if -2.3 < p < 1.8]

        for yp in node_positions:
            dot = Dot(point=np.array([0, yp, 0]), radius=0.06, color="#ffd700")
            nodes.add(dot)

        # Beads at two nodes
        bead1 = Circle(radius=0.18, color="#ff6f61", fill_opacity=0.7, stroke_width=2)
        bead2 = Circle(radius=0.12, color="#ffd700", fill_opacity=0.7, stroke_width=2)
        if len(node_positions) >= 3:
            bead1.move_to(np.array([0, node_positions[1], 0]))
            bead2.move_to(np.array([0, node_positions[2], 0]))

        label_40k = Text("40 kHz ultrasound", font_size=16, color="#00bfff")
        label_40k.move_to(RIGHT * 3 + DOWN * 0.3)

        arrow_wave = Arrow(
            start=label_40k.get_left() + LEFT * 0.1,
            end=np.array([amp * 0.7, 0, 0]),
            color="#00bfff", stroke_width=2, max_tip_length_to_length_ratio=0.15
        )

        node_label = Text("Pressure nodes\n(trapping points)", font_size=15, color="#ffd700")
        node_label.move_to(LEFT * 3.5 + DOWN * 0.3)

        # Fade in
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.6)
        self.play(
            FadeIn(speaker_top), FadeIn(speaker_bot),
            Create(wave_curve_l), Create(wave_curve_r),
            run_time=1.5
        )
        self.play(FadeIn(nodes), FadeIn(bead1), FadeIn(bead2), run_time=1.0)
        self.play(FadeIn(label_40k), FadeIn(arrow_wave), FadeIn(node_label), run_time=1.0)

        # Gentle oscillation of beads
        self.play(
            bead1.animate.shift(UP * 0.08), bead2.animate.shift(DOWN * 0.06),
            rate_func=there_and_back, run_time=1.5
        )
        self.play(
            bead1.animate.shift(DOWN * 0.06), bead2.animate.shift(UP * 0.08),
            rate_func=there_and_back, run_time=1.5
        )

        self.wait(1.4)

        # Fade out
        all_objs = VGroup(header, speaker_top, speaker_bot, wave_curve_l, wave_curve_r,
                          nodes, bead1, bead2, label_40k, arrow_wave, node_label)
        self.play(FadeOut(all_objs), run_time=1.0)

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

class Scene08_Implications(Scene):
    def construct(self):
        header = Text("Implications", font_size=40, weight=BOLD, color=WHITE)
        header.move_to(UP * 3.8)

        # Left column: Technology
        tech_header = Text("Technology", font_size=26, weight=BOLD, color="#00bfff")
        tech_header.move_to(LEFT * 4 + UP * 2.3)

        tech_items = VGroup(
            self.make_item("Compact oscillators", "#00bfff"),
            self.make_item("Resonant sensors", "#00bfff"),
            self.make_item("Quantum-inspired computing", "#00bfff"),
            self.make_item("Precision time bases", "#00bfff"),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(LEFT * 4 + DOWN * 0.3)

        # Right column: Biology
        bio_header = Text("Biology", font_size=26, weight=BOLD, color="#ff6f61")
        bio_header.move_to(RIGHT * 4 + UP * 2.3)

        bio_items = VGroup(
            self.make_item("Circadian rhythms", "#ff6f61"),
            self.make_item("Metabolic oscillations", "#ff6f61"),
            self.make_item("Heartbeat regulation", "#ff6f61"),
            self.make_item("Biochemical clocks", "#ff6f61"),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 4 + DOWN * 0.3)

        # Divider
        divider = DashedLine(UP * 2.0, DOWN * 2.5, color=GREY_C, stroke_width=1, dash_length=0.15)

        # Bottom insight
        insight = Text(
            "Time crystal behavior may be hiding in plain sight\nwherever waves interact with objects of different sizes.",
            font_size=19, color="#ffd700", line_spacing=1.3
        )
        insight.move_to(DOWN * 3.3)
        safe_position(insight)

        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.5)
        self.play(FadeIn(tech_header), FadeIn(bio_header), Create(divider), run_time=0.6)

        for t_item, b_item in zip(tech_items, bio_items):
            self.play(FadeIn(t_item, shift=RIGHT * 0.2), FadeIn(b_item, shift=LEFT * 0.2), run_time=0.5)

        self.play(FadeIn(insight), run_time=0.7)
        self.wait(4.2)

        all_objs = VGroup(header, tech_header, tech_items, bio_header, bio_items, divider, insight)
        self.play(FadeOut(all_objs), run_time=1.0)

    def make_item(self, text, color):
        bullet = Dot(radius=0.06, color=color)
        label = Text(text, font_size=19, color=GREY_B)
        return VGroup(bullet, label).arrange(RIGHT, buff=0.2)

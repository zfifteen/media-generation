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

class Scene01_Title(Scene):
    def construct(self):
        # Main title - no fade, instant display for thumbnail
        title = Text("Levitating Time Crystals", font_size=52, weight=BOLD, color=WHITE)
        title.move_to(UP * 1.2)

        subtitle = Text(
            "Sound Waves, Nonreciprocal Forces,\nand Broken Time Symmetry",
            font_size=28, color="#00bfff", line_spacing=1.3
        )
        subtitle.next_to(title, DOWN, buff=0.6)

        # Decorative line
        line = Line(LEFT * 5, RIGHT * 5, color="#00bfff", stroke_width=2)
        line.next_to(subtitle, DOWN, buff=0.5)

        # Attribution
        credit = Text("Based on Morrell, Elliott & Grier (2025)", font_size=18, color=GREY_B)
        credit.next_to(line, DOWN, buff=0.4)

        journal = Text("Physical Review Letters", font_size=16, color=GREY_C, slant=ITALIC)
        journal.next_to(credit, DOWN, buff=0.2)

        # Decorative floating circles (bead hint)
        bead_large = Circle(radius=0.35, color="#ff6f61", fill_opacity=0.6, stroke_width=2)
        bead_large.move_to(LEFT * 5 + UP * 3.2)
        bead_small = Circle(radius=0.2, color="#ffd700", fill_opacity=0.6, stroke_width=2)
        bead_small.move_to(RIGHT * 5.5 + UP * 3.0)

        # Sound wave hints
        wave_lines = VGroup()
        for i in range(5):
            arc = Arc(radius=0.6 + i * 0.25, angle=PI/3, start_angle=PI/2 + PI/6,
                      color="#00bfff", stroke_opacity=0.3 - i*0.05, stroke_width=1.5)
            arc.move_to(LEFT * 5 + UP * 3.2)
            wave_lines.add(arc)

        # Add everything instantly (no animation for thumbnail)
        self.add(title, subtitle, line, credit, journal, bead_large, bead_small, wave_lines)
        self.wait(10)

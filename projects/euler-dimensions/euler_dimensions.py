from manim import *
import numpy as np

# ============================================================================
# OPTIMIZED CONFIGURATION - DO NOT MODIFY THESE VALUES
# ============================================================================
config.frame_height = 10
config.frame_width = 10 * 16/9
config.pixel_height = 1440
config.pixel_width = 2560
# ============================================================================


def safe_position(mobject, max_y=4.0, min_y=-4.0):
    top = mobject.get_top()[1]
    bottom = mobject.get_bottom()[1]
    if top > max_y:
        mobject.shift(DOWN * (top - max_y))
    elif bottom < min_y:
        mobject.shift(UP * (min_y - bottom))
    return mobject


# ============================================================================
# SCENE 0: TITLE CARD
# ============================================================================
class TitleScene(Scene):
    def construct(self):
        title = Text(
            "The Orthogonal Dimensions of e",
            font_size=48,
            weight=BOLD,
            color=WHITE,
        ).move_to(UP * 1.0)

        subtitle = Text(
            "Positional Precision  |  Relational Structure  |  Permanent Phase Separation",
            font_size=20,
            color=GREY_B,
        ).next_to(title, DOWN, buff=0.6)

        divider = Line(LEFT * 5, RIGHT * 5, color=BLUE_C, stroke_width=2).next_to(
            subtitle, DOWN, buff=0.5
        )

        e_value = Text(
            "e = 2.71828182845904523536028747135266249775...",
            font_size=24,
            color=GOLD_B,
        ).next_to(divider, DOWN, buff=0.5)

        credit = Text("Big D", font_size=18, color=GREY_C).move_to(DOWN * 3.5)

        safe_position(title)
        safe_position(subtitle)
        safe_position(e_value)
        safe_position(credit)

        self.play(FadeIn(title, run_time=0.05))
        self.play(FadeIn(subtitle, run_time=0.05))
        self.play(FadeIn(divider, run_time=0.05))
        self.play(FadeIn(e_value, run_time=0.05))
        self.play(FadeIn(credit, run_time=0.05))
        self.wait(14.5)


# ============================================================================
# SCENE 1: THE FOUR SHADOWS OF A SINGLE CONSTANT
# ============================================================================
class Scene1_FourShadows(Scene):
    def construct(self):
        header = Text(
            "The Four Shadows of a Single Constant",
            font_size=36,
            weight=BOLD,
            color=WHITE,
        ).move_to(UP * 3.8)
        safe_position(header)

        # Central glowing e
        e_dot = Dot(ORIGIN, radius=0.15, color=YELLOW)
        e_label = Text("e", font_size=48, weight=BOLD, color=YELLOW).next_to(
            e_dot, UR, buff=0.15
        )
        e_glow = Circle(radius=0.4, color=YELLOW, fill_opacity=0.15, stroke_width=0)
        center_group = VGroup(e_dot, e_label, e_glow).move_to(ORIGIN)

        # Four projection planes
        plane_colors = [BLUE_C, GREEN_C, TEAL_C, MAROON_C]
        plane_labels_text = [
            "Infinite Series",
            "Continued Fraction",
            "Limit Definition",
            "Infinite Product",
        ]
        plane_formulas_text = [
            "1/0! + 1/1! + 1/2! + 1/3! + ...",
            "[2; 1, 2, 1, 1, 4, 1, 1, 6, ...]",
            "lim (1 + 1/n)^n  as n -> inf",
            "Product: ((n+1)/n)^((-1)^(n+1))",
        ]
        directions = [LEFT * 5.0, RIGHT * 5.0, UP * 2.6, DOWN * 2.6]

        planes = []
        beams = []
        for i in range(4):
            rect = RoundedRectangle(
                width=4.2,
                height=1.6,
                corner_radius=0.15,
                color=plane_colors[i],
                fill_opacity=0.12,
                stroke_width=1.5,
            )
            label = Text(
                plane_labels_text[i], font_size=16, weight=BOLD, color=plane_colors[i]
            ).move_to(rect.get_top() + DOWN * 0.35)
            formula = Text(
                plane_formulas_text[i], font_size=18, color=WHITE
            ).move_to(rect.get_center() + DOWN * 0.15)
            plane_group = VGroup(rect, label, formula).move_to(directions[i])
            safe_position(plane_group)
            planes.append(plane_group)

            beam = Line(
                ORIGIN,
                directions[i] * 0.5,
                color=plane_colors[i],
                stroke_width=2,
                stroke_opacity=0.6,
            )
            beams.append(beam)

        caption = Text(
            "A number is not its formula. A number is the intersection of its projections.",
            font_size=18,
            color=GREY_B,
            slant=ITALIC,
        ).move_to(DOWN * 4.2)
        safe_position(caption)

        self.play(Write(header), run_time=1.0)
        self.play(FadeIn(center_group, scale=1.5), run_time=1.0)
        self.wait(0.3)

        for i in range(4):
            self.play(
                Create(beams[i]),
                FadeIn(planes[i], shift=directions[i] * 0.05),
                run_time=0.8,
            )

        self.wait(0.5)
        self.play(
            e_glow.animate.set_opacity(0.4).scale(1.5),
            rate_func=there_and_back,
            run_time=1.5,
        )
        self.play(FadeIn(caption), run_time=1.0)
        self.wait(4.6)


# ============================================================================
# SCENE 2: THE SERIES AS POSITIONAL COMPRESSION
# ============================================================================
class Scene2_SeriesCompression(Scene):
    def construct(self):
        header = Text(
            "The Series as Positional Compression",
            font_size=36,
            weight=BOLD,
            color=BLUE_C,
        ).move_to(UP * 3.8)
        safe_position(header)
        self.play(Write(header), run_time=1.0)

        import math as mth

        terms_display = [
            "1/0! = 1",
            "1/1! = 1",
            "1/2! = 0.5",
            "1/3! = 0.1667",
            "1/4! = 0.0417",
            "1/5! = 0.0083",
            "1/6! = 0.0014",
        ]
        terms_values = [1.0, 1.0, 0.5, 1/6, 1/24, 1/120, 1/720]
        partial_sums = []
        s = 0
        for v in terms_values:
            s += v
            partial_sums.append(s)

        left_label = Text("Terms:", font_size=20, color=BLUE_B).move_to(LEFT * 5.0 + UP * 2.8)
        self.play(FadeIn(left_label), run_time=0.4)

        # Precision bar
        bar_x = 5.5
        bar_bg = Rectangle(
            width=0.8, height=5.5, color=GREY_D, fill_opacity=0.15, stroke_width=1
        ).move_to(RIGHT * bar_x + DOWN * 0.1)
        bar_title = Text("Decimal\nPrecision", font_size=14, color=GOLD_B).move_to(
            RIGHT * bar_x + UP * 3.0
        )
        safe_position(bar_title)
        self.play(FadeIn(bar_bg), FadeIn(bar_title), run_time=0.5)

        sum_label = Text("Partial sum:", font_size=20, color=GREY_B).move_to(RIGHT * 1.5 + UP * 2.8)
        sum_display = Text("0.000000", font_size=28, color=GOLD_B).next_to(sum_label, DOWN, buff=0.2)
        self.play(FadeIn(sum_label), FadeIn(sum_display), run_time=0.5)

        fill = Rectangle(
            width=0.7, height=0.01, color=BLUE_C, fill_opacity=0.6, stroke_width=0
        )
        fill.align_to(bar_bg, DOWN).shift(UP * 0.05)
        self.add(fill)

        annotation = Text(
            "Factorial decay: positional information grows explosively.",
            font_size=18,
            color=BLUE_B,
            slant=ITALIC,
        ).move_to(DOWN * 4.2)
        safe_position(annotation)

        fill_heights = [0.1, 0.3, 1.0, 1.5, 2.5, 3.5, 4.5]

        for i in range(len(terms_display)):
            term = Text(terms_display[i], font_size=20, color=WHITE)
            term.move_to(LEFT * 4.5 + UP * (2.2 - i * 0.65))
            safe_position(term)

            new_sum = Text(
                f"{partial_sums[i]:.6f}", font_size=28, color=GOLD_B
            ).next_to(sum_label, DOWN, buff=0.2)

            new_fill = Rectangle(
                width=0.7,
                height=fill_heights[i],
                color=BLUE_C,
                fill_opacity=0.6,
                stroke_width=0,
            )
            new_fill.align_to(bar_bg, DOWN).shift(UP * 0.05)

            self.play(
                FadeIn(term, shift=DOWN * 0.2),
                Transform(sum_display, new_sum),
                Transform(fill, new_fill),
                run_time=0.8 if i < 4 else 0.6,
            )
            if i < 3:
                self.wait(0.2)

        self.play(FadeIn(annotation), run_time=0.8)
        self.wait(3.0)


# ============================================================================
# SCENE 3: THE CONTINUED FRACTION AS DIOPHANTINE STAIRCASE
# ============================================================================
class Scene3_CFStaircase(Scene):
    def construct(self):
        header = Text(
            "The Continued Fraction as Diophantine Staircase",
            font_size=32,
            weight=BOLD,
            color=GREEN_C,
        ).move_to(UP * 3.8)
        safe_position(header)
        self.play(Write(header), run_time=1.0)

        cf_coeffs = [2, 1, 2, 1, 1, 4, 1, 1, 6]
        convergents = [
            ("2/1", 2.0),
            ("3/1", 3.0),
            ("8/3", 2.6667),
            ("11/4", 2.75),
            ("19/7", 2.7143),
            ("87/32", 2.7188),
            ("106/39", 2.7179),
            ("193/71", 2.7183),
            ("1264/465", 2.71828),
        ]

        # Staircase on left
        stairs = VGroup()
        x_pos = -7.0
        y_pos = 2.5
        step_h = 0.4

        for i, coeff in enumerate(cf_coeffs):
            step_w = 0.4 + coeff * 0.25
            step = Rectangle(
                width=step_w,
                height=step_h,
                color=GREEN_C,
                fill_opacity=0.2 + 0.04 * i,
                stroke_width=1.5,
            )
            step.move_to(RIGHT * (x_pos + step_w / 2) + UP * (y_pos - i * step_h))
            lbl = Text(str(coeff), font_size=12, color=WHITE).move_to(step.get_center())
            stairs.add(VGroup(step, lbl))
            x_pos += step_w

        stairs.move_to(LEFT * 4.0 + DOWN * 0.3)
        safe_position(stairs)

        # Number line on right
        nline = NumberLine(
            x_range=[2.0, 3.2, 0.2],
            length=5.5,
            color=GREY_B,
            include_numbers=True,
            numbers_to_include=[2.0, 2.4, 2.8, 3.2],
            font_size=14,
            decimal_number_config={"num_decimal_places": 1},
        ).move_to(RIGHT * 3.0 + UP * 2.5)

        e_pos = nline.number_to_point(2.71828)
        e_dash = DashedLine(
            e_pos + UP * 0.3, e_pos + DOWN * 0.3, color=YELLOW, stroke_width=2
        )
        e_lbl = Text("e", font_size=20, weight=BOLD, color=YELLOW).next_to(e_dash, UP, buff=0.08)

        self.play(Create(nline), FadeIn(e_dash), FadeIn(e_lbl), run_time=1.2)
        self.wait(0.3)

        dot_colors = [RED_C, BLUE_C, RED_C, BLUE_C, RED_C, BLUE_C, RED_C, BLUE_C, RED_C]

        for i in range(min(len(cf_coeffs), 7)):
            frac_str, val = convergents[i]
            clamped = min(max(val, 2.0), 3.2)
            pos = nline.number_to_point(clamped)
            dot = Dot(pos, radius=0.06, color=dot_colors[i])

            combined_str = f"{frac_str} = {val:.4f}"
            lbl = Text(combined_str, font_size=11, color=dot_colors[i])

            if i % 2 == 0:
                lbl.next_to(dot, DOWN, buff=0.1 + (i % 3) * 0.15)
            else:
                lbl.next_to(dot, UP, buff=0.1 + (i % 3) * 0.15)
            safe_position(lbl)

            anims = [FadeIn(dot, scale=2)]
            if i < len(stairs):
                anims.append(FadeIn(stairs[i], shift=RIGHT * 0.15))
            anims.append(FadeIn(lbl))
            self.play(*anims, run_time=0.7)

        for i in range(7, len(stairs)):
            self.play(FadeIn(stairs[i], shift=RIGHT * 0.15), run_time=0.4)

        caption = Text(
            "Linear growth: relational information accumulates slowly but structurally.",
            font_size=18,
            color=GREEN_B,
            slant=ITALIC,
        ).move_to(DOWN * 4.2)
        safe_position(caption)
        self.play(FadeIn(caption), run_time=0.8)
        self.wait(3.0)


# ============================================================================
# SCENE 4: EQUAL COMPUTATIONAL COST, UNEQUAL INFORMATION
# ============================================================================
class Scene4_SplitScreen(Scene):
    def construct(self):
        header = Text(
            "Equal Cost, Unequal Information",
            font_size=36,
            weight=BOLD,
            color=WHITE,
        ).move_to(UP * 3.8)
        safe_position(header)

        div_line = DashedLine(UP * 3.2, DOWN * 3.2, color=GREY_C, stroke_width=1.5)

        left_title = Text("Infinite Series", font_size=22, color=BLUE_C).move_to(
            LEFT * 4.5 + UP * 3.0
        )
        right_title = Text("Continued Fraction", font_size=22, color=GREEN_C).move_to(
            RIGHT * 4.5 + UP * 3.0
        )

        self.play(Write(header), Create(div_line), run_time=1.0)
        self.play(FadeIn(left_title), FadeIn(right_title), run_time=0.5)

        ratio_label = Text("Information Ratio:", font_size=20, color=GREY_B).move_to(UP * 0.6)
        ratio_value = Text("--", font_size=48, weight=BOLD, color=GOLD_B).move_to(DOWN * 0.2)
        self.play(FadeIn(ratio_label), FadeIn(ratio_value), run_time=0.5)

        series_terms = ["1/1!", "1/2!", "1/3!", "1/4!", "1/5!"]
        cf_steps = ["[2]", "[2; 1]", "[2; 1, 2]", "[2; 1, 2, 1]", "[2; 1, 2, 1, 1]"]
        ratios = ["~8x", "~300x", "~120,000x", "~80 million x", "~300 billion x"]
        ratio_colors = [GOLD_B, GOLD_B, ORANGE, RED_B, RED]

        for i in range(5):
            s_term = Text(series_terms[i], font_size=22, color=BLUE_B).move_to(
                LEFT * 4.0 + UP * (1.8 - i * 0.9)
            )
            c_term = Text(cf_steps[i], font_size=18, color=GREEN_B).move_to(
                RIGHT * 4.0 + UP * (1.8 - i * 0.9)
            )
            safe_position(s_term)
            safe_position(c_term)

            new_ratio = Text(
                ratios[i], font_size=48, weight=BOLD, color=ratio_colors[i]
            ).move_to(DOWN * 0.2)

            self.play(
                FadeIn(s_term, shift=DOWN * 0.15),
                FadeIn(c_term, shift=DOWN * 0.15),
                Transform(ratio_value, new_ratio),
                run_time=1.0,
            )
            if i < 2:
                self.wait(0.4)
            else:
                self.wait(0.2)

        self.play(
            Flash(ratio_value.get_center(), color=GOLD, flash_radius=1.5),
            run_time=0.8,
        )

        caption = Text(
            "Not speed. Not efficiency. Orthogonal information channels.",
            font_size=18,
            color=GREY_B,
            slant=ITALIC,
        ).move_to(DOWN * 4.2)
        safe_position(caption)
        self.play(FadeIn(caption), run_time=0.8)
        self.wait(2.5)


# ============================================================================
# SCENE 5: PHASE SEPARATION
# ============================================================================
class Scene5_PhaseSeparation(Scene):
    def construct(self):
        header = Text(
            "Phase Separation",
            font_size=36,
            weight=BOLD,
            color=WHITE,
        ).move_to(UP * 3.8)
        safe_position(header)
        self.play(Write(header), run_time=1.0)

        series_plane = Rectangle(
            width=5, height=3, color=BLUE_C, fill_opacity=0.15, stroke_width=2
        ).move_to(LEFT * 3 + DOWN * 0.3)

        cf_plane = Rectangle(
            width=5, height=3, color=GREEN_C, fill_opacity=0.15, stroke_width=2
        ).move_to(RIGHT * 3 + DOWN * 0.3)

        series_label = Text(
            "Infinite Series", font_size=22, weight=BOLD, color=BLUE_C
        ).move_to(series_plane.get_top() + DOWN * 0.4)

        cf_label = Text(
            "Continued Fraction", font_size=22, weight=BOLD, color=GREEN_C
        ).move_to(cf_plane.get_top() + DOWN * 0.4)

        series_desc = Text(
            "Positional Information\n(Where is e on the number line?)",
            font_size=16,
            color=BLUE_B,
            line_spacing=1.2,
        ).move_to(series_plane.get_center() + DOWN * 0.3)

        cf_desc = Text(
            "Relational Information\n(How does e relate to every fraction?)",
            font_size=16,
            color=GREEN_B,
            line_spacing=1.2,
        ).move_to(cf_plane.get_center() + DOWN * 0.3)

        self.play(
            FadeIn(series_plane), FadeIn(cf_plane),
            FadeIn(series_label), FadeIn(cf_label),
            run_time=1.5,
        )
        self.play(FadeIn(series_desc), FadeIn(cf_desc), run_time=1.0)
        self.wait(0.5)

        # Arrows
        arrow_origin_s = series_plane.get_center() + UP * 0.5
        arrow_series = Arrow(
            arrow_origin_s,
            arrow_origin_s + UP * 2.2,
            color=BLUE_C,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15,
        )

        arrow_origin_c = cf_plane.get_center() + RIGHT * 0.3
        arrow_cf = Arrow(
            arrow_origin_c,
            arrow_origin_c + RIGHT * 2.5,
            color=GREEN_C,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15,
        )

        arrow_s_label = Text(
            "Positional", font_size=16, color=BLUE_B
        ).next_to(arrow_series, LEFT, buff=0.15)
        arrow_c_label = Text(
            "Relational", font_size=16, color=GREEN_B
        ).next_to(arrow_cf, UP, buff=0.1)

        self.play(GrowArrow(arrow_series), GrowArrow(arrow_cf), run_time=1.2)
        self.play(FadeIn(arrow_s_label), FadeIn(arrow_c_label), run_time=0.8)
        self.wait(0.5)

        # Perpendicularity indicator (manually drawn right angle)
        perp_size = 0.25
        perp_corner = VGroup(
            Line(DOWN * perp_size, ORIGIN, color=GOLD_B, stroke_width=2),
            Line(ORIGIN, RIGHT * perp_size, color=GOLD_B, stroke_width=2),
            Line(
                DOWN * perp_size + RIGHT * 0,
                DOWN * perp_size + RIGHT * perp_size,
                color=GOLD_B, stroke_width=1.5,
            ),
            Line(
                DOWN * perp_size + RIGHT * perp_size,
                RIGHT * perp_size,
                color=GOLD_B, stroke_width=1.5,
            ),
        ).move_to(ORIGIN + DOWN * 0.3)

        perp_text = Text(
            "Orthogonal", font_size=18, weight=BOLD, color=GOLD_B
        ).next_to(perp_corner, DOWN, buff=0.25)

        self.play(Create(perp_corner), FadeIn(perp_text), run_time=1.0)
        self.wait(0.5)

        # Drift apart
        left_group = VGroup(series_plane, series_label, series_desc, arrow_series, arrow_s_label)
        right_group = VGroup(cf_plane, cf_label, cf_desc, arrow_cf, arrow_c_label)

        self.play(
            left_group.animate.shift(LEFT * 0.8),
            right_group.animate.shift(RIGHT * 0.8),
            run_time=2.0,
        )

        caption = Text(
            "These representations do not converge. They span different dimensions.",
            font_size=18,
            color=GREY_B,
            slant=ITALIC,
        ).move_to(DOWN * 4.2)
        safe_position(caption)
        self.play(FadeIn(caption), run_time=1.0)
        self.wait(2.5)


# ============================================================================
# SCENE 6: THE HIGHER-DIMENSIONAL IDENTITY OF e
# ============================================================================
class Scene6_HigherDimensional(Scene):
    def construct(self):
        header = Text(
            "The Higher-Dimensional Identity of e",
            font_size=36,
            weight=BOLD,
            color=WHITE,
        ).move_to(UP * 3.8)
        safe_position(header)

        e_dot = Dot(ORIGIN, radius=0.18, color=YELLOW)
        e_label = Text("e", font_size=44, weight=BOLD, color=YELLOW).next_to(
            e_dot, UR, buff=0.15
        )

        plane_colors = [BLUE_C, GREEN_C, TEAL_C, MAROON_C]
        plane_names = ["Series", "CF", "Limit", "Product"]

        planes = VGroup()
        plane_labels = VGroup()
        beams = VGroup()

        for i in range(4):
            angle = i * PI / 2
            direction = np.array([np.cos(angle), np.sin(angle), 0])

            rect = Rectangle(
                width=3.0,
                height=0.8,
                color=plane_colors[i],
                fill_opacity=0.15,
                stroke_width=1.5,
            )
            rect.move_to(direction * 3.2)
            rect.rotate(angle)

            label = Text(
                plane_names[i], font_size=16, weight=BOLD, color=plane_colors[i]
            ).move_to(direction * 3.2)

            beam = Line(
                direction * 0.4,
                direction * 2.6,
                color=plane_colors[i],
                stroke_width=3,
                stroke_opacity=0.6,
            )

            planes.add(rect)
            plane_labels.add(label)
            beams.add(beam)

        self.play(Write(header), run_time=1.0)
        self.play(FadeIn(e_dot), FadeIn(e_label), run_time=0.8)
        self.play(
            *[Create(beams[i]) for i in range(4)],
            *[FadeIn(planes[i]) for i in range(4)],
            *[FadeIn(plane_labels[i]) for i in range(4)],
            run_time=1.5,
        )
        self.wait(0.5)

        # Rotate assembly
        assembly = VGroup(planes, plane_labels, beams)
        self.play(Rotate(assembly, angle=PI / 3, about_point=ORIGIN), run_time=3.0)
        self.wait(0.3)

        # Pulse beams
        for i in range(4):
            self.play(
                beams[i].animate.set_stroke(opacity=1.0).set_color(WHITE),
                rate_func=there_and_back,
                run_time=0.4,
            )

        # Transform center into polytope
        polytope = RegularPolygon(
            n=8, radius=0.6, color=GOLD_B, fill_opacity=0.3, stroke_width=2,
        ).move_to(ORIGIN)

        self.play(
            ReplacementTransform(e_dot, polytope),
            FadeOut(e_label),
            run_time=1.5,
        )

        caption = Text(
            "No single projection contains the whole identity.",
            font_size=18,
            color=GREY_B,
            slant=ITALIC,
        ).move_to(DOWN * 4.2)
        safe_position(caption)
        self.play(FadeIn(caption), run_time=1.0)
        self.wait(2.5)


# ============================================================================
# SCENE 7: THE FINAL SYNTHESIS (no fade to black)
# ============================================================================
class Scene7_FinalSynthesis(Scene):
    def construct(self):
        polytope = RegularPolygon(
            n=8, radius=0.8, color=GOLD_B, fill_opacity=0.25, stroke_width=2.5,
        ).move_to(ORIGIN)

        e_label = Text("e", font_size=56, weight=BOLD, color=YELLOW).move_to(ORIGIN)

        axis_colors = [BLUE_C, GREEN_C, TEAL_C, MAROON_C]
        axis_labels_text = ["Series", "CF", "Limit", "Product"]
        axes_group = VGroup()
        labels_group = VGroup()

        for i in range(4):
            angle = i * PI / 2
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            line = Line(
                direction * 1.0,
                direction * 3.5,
                color=axis_colors[i],
                stroke_width=2.5,
            )
            label = Text(
                axis_labels_text[i], font_size=16, weight=BOLD, color=axis_colors[i]
            ).move_to(direction * 3.9)
            safe_position(label)
            axes_group.add(line)
            labels_group.add(label)

        line1 = Text(
            "A transcendental number is not a value.",
            font_size=28,
            color=WHITE,
            weight=BOLD,
        )
        line2 = Text(
            "It is a constellation of independent invariants.",
            font_size=28,
            color=GOLD_B,
            weight=BOLD,
        )
        final_text = VGroup(line1, line2).arrange(DOWN, buff=0.3).move_to(DOWN * 3.2)
        safe_position(final_text)

        self.play(FadeIn(polytope, scale=0.5), run_time=1.5)
        self.play(FadeIn(e_label), run_time=0.8)
        self.wait(0.3)

        self.play(
            *[Create(axes_group[i]) for i in range(4)],
            *[FadeIn(labels_group[i]) for i in range(4)],
            run_time=2.0,
        )
        self.wait(0.5)

        frame_group = VGroup(polytope, axes_group, labels_group, e_label)
        self.play(
            Rotate(frame_group, angle=PI / 12, about_point=ORIGIN),
            run_time=1.5,
        )
        self.play(
            Rotate(frame_group, angle=-PI / 12, about_point=ORIGIN),
            run_time=1.5,
        )

        self.play(Write(line1), run_time=1.5)
        self.play(Write(line2), run_time=1.5)

        # Hold -- NO fade to black
        self.wait(3.5)

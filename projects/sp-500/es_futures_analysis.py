"""
E-Mini S&P 500 Z-Mapping Visualization - COMPLETE REWRITE
Phased scene design: each phase clears before the next to prevent overlap.
"""

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


class ESFuturesZMapping(Scene):

    def construct(self):
        # Market data
        es_close = 6952.75
        es_prev_close = 6820.75
        daily_move = 132.00
        year_high = 7043.00
        year_low = 4832.00
        remaining_gap = year_high - es_close

        # ===============================================================
        # PHASE 1: Title card (standalone, then fully removed)
        # ===============================================================
        title = Text(
            "E-Mini S&P 500: The Compression Regime",
            font_size=42, weight=BOLD, color=YELLOW
        ).move_to(UP * 0.5)
        subtitle = Text(
            "February 6, 2026",
            font_size=28, color=BLUE_B
        ).next_to(title, DOWN, buff=0.3)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.8)

        # ===============================================================
        # PHASE 2: Price scale with only the axis and labels
        # ===============================================================

        # Persistent header (small, top-left, out of the way)
        header = Text(
            "ES Futures | Feb 6, 2026",
            font_size=18, color=GRAY
        ).move_to(UP * 3.5 + LEFT * 5.5)
        self.play(FadeIn(header), run_time=0.5)

        # Axis setup -- LEFT half of screen only
        axis_x = LEFT * 5  # x-position of axis
        axis_height = 6.0
        axis = Line(
            axis_x + UP * (axis_height / 2),
            axis_x + DOWN * (axis_height / 2),
            color=WHITE, stroke_width=3
        )

        year_range = year_high - year_low

        def price_to_y(price):
            normalized = (price - year_low) / year_range
            return (normalized - 0.5) * axis_height

        high_y = price_to_y(year_high)
        close_y = price_to_y(es_close)
        prev_y = price_to_y(es_prev_close)

        # Price labels on the LEFT of the axis
        def make_label(text, y_offset, color):
            lbl = Text(text, font_size=14, color=color)
            tick = Line(LEFT * 0.15, RIGHT * 0.15, color=color)
            tick.move_to(axis.get_center() + UP * y_offset)
            lbl.next_to(tick, LEFT, buff=0.15)
            return VGroup(tick, lbl)

        high_grp = make_label(f"${year_high:,.0f}", high_y, RED)
        close_grp = make_label(f"${es_close:,.0f}", close_y, GREEN)
        prev_grp = make_label(f"${es_prev_close:,.0f}", prev_y, GRAY)
        low_grp = make_label(f"${year_low:,.0f}", price_to_y(year_low), BLUE)

        self.play(Create(axis), run_time=1)
        self.play(
            FadeIn(high_grp), FadeIn(close_grp),
            FadeIn(prev_grp), FadeIn(low_grp),
            run_time=1
        )
        self.wait(1)

        # Ceiling line -- short, only near the axis
        ceiling_line = DashedLine(
            axis.get_center() + UP * high_y + LEFT * 0.5,
            axis.get_center() + UP * high_y + RIGHT * 2,
            color=RED, stroke_width=3, dash_length=0.12
        )
        ceiling_label = Text("CEILING", font_size=14, color=RED, weight=BOLD)
        ceiling_label.next_to(ceiling_line, UP, buff=0.15)

        self.play(Create(ceiling_line), Write(ceiling_label), run_time=1)
        self.wait(1)

        # ===============================================================
        # PHASE 3: Show the daily move arrow (RIGHT side of axis)
        # ===============================================================
        arrow_x = axis_x + RIGHT * 1.5

        move_arrow = Arrow(
            [arrow_x[0], axis.get_center()[1] + prev_y, 0],
            [arrow_x[0], axis.get_center()[1] + close_y, 0],
            color=YELLOW, stroke_width=5, buff=0,
            max_tip_length_to_length_ratio=0.2
        )
        move_label = VGroup(
            Text(f"+{daily_move:.0f} pts", font_size=18, color=YELLOW, weight=BOLD),
            Text(f"(+1.9%)", font_size=14, color=YELLOW),
        ).arrange(DOWN, buff=0.08)
        move_label.next_to(move_arrow, RIGHT, buff=0.3)

        self.play(GrowArrow(move_arrow), run_time=1)
        self.play(FadeIn(move_label), run_time=0.8)
        self.wait(1.5)

        # ===============================================================
        # PHASE 4: Show the gap brace (separate from daily move)
        # Clear the daily move labels first to avoid collision
        # ===============================================================
        self.play(FadeOut(move_label), run_time=0.5)

        gap_brace = Brace(
            Line(
                [arrow_x[0], axis.get_center()[1] + close_y, 0],
                [arrow_x[0], axis.get_center()[1] + high_y, 0],
            ),
            direction=RIGHT, color=ORANGE, buff=0.15
        )
        gap_label = Text(
            f"Gap: {remaining_gap:.1f} pts", font_size=16, color=ORANGE, weight=BOLD
        )
        gap_label.next_to(gap_brace, RIGHT, buff=0.2)

        self.play(Create(gap_brace), Write(gap_label), run_time=1.2)
        self.wait(1.5)

        # ===============================================================
        # PHASE 5: Key ratio insight (RIGHT panel, clear of axis)
        # ===============================================================
        insight_panel = VGroup()

        box = Rectangle(
            width=5.5, height=3.5, color=PURPLE,
            stroke_width=3, fill_opacity=0.08, fill_color=PURPLE
        )
        box.move_to(RIGHT * 3.5)

        panel_title = Text(
            "The Compression", font_size=24, color=PURPLE, weight=BOLD
        ).move_to(box.get_top() + DOWN * 0.5)

        line1 = Text(
            f"Daily thrust:  +{daily_move:.0f} pts",
            font_size=20, color=YELLOW
        ).next_to(panel_title, DOWN, buff=0.5)
        line2 = Text(
            f"Gap to ATH:     {remaining_gap:.1f} pts",
            font_size=20, color=ORANGE
        ).next_to(line1, DOWN, buff=0.25)

        divider = Line(LEFT * 2, RIGHT * 2, color=WHITE).next_to(line2, DOWN, buff=0.3)

        ratio_line = Text(
            f"Ratio: {(daily_move / remaining_gap) * 100:.0f}%",
            font_size=32, color=YELLOW, weight=BOLD
        ).next_to(divider, DOWN, buff=0.3)

        insight_panel.add(box, panel_title, line1, line2, divider, ratio_line)

        self.play(Create(box), Write(panel_title), run_time=1)
        self.play(Write(line1), run_time=0.8)
        self.play(Write(line2), run_time=0.8)
        self.play(Create(divider), run_time=0.4)
        self.play(Write(ratio_line), run_time=1)
        self.wait(2.5)

        # ===============================================================
        # PHASE 6: Breakthrough concept (clear insight panel first)
        # ===============================================================
        self.play(FadeOut(insight_panel), FadeOut(gap_brace), FadeOut(gap_label), run_time=0.8)

        # Bring move_label back
        self.play(FadeIn(move_label), run_time=0.5)

        # Ghost arrow showing overshoot past ceiling
        ghost_start_y = axis.get_center()[1] + close_y
        ghost_end_y = axis.get_center()[1] + high_y + 0.4  # past ceiling
        ghost_arrow = Arrow(
            [arrow_x[0] + 2, ghost_start_y, 0],
            [arrow_x[0] + 2, ghost_end_y, 0],
            color=YELLOW, stroke_width=5, stroke_opacity=0.35,
            buff=0, max_tip_length_to_length_ratio=0.2
        )
        ghost_label = Text(
            "Same energy\nwould break through",
            font_size=16, color=YELLOW, line_spacing=1.0
        ).next_to(ghost_arrow, RIGHT, buff=0.3)

        self.play(GrowArrow(ghost_arrow), Write(ghost_label), run_time=1.5)
        self.wait(2)

        # ===============================================================
        # PHASE 7: Conclusion (clear everything, full screen statement)
        # ===============================================================
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1
        )

        conclusion_box = Rectangle(
            width=10, height=3.5, color=GREEN,
            stroke_width=3, fill_opacity=0.1, fill_color=GREEN
        ).move_to(ORIGIN)

        conclusion = VGroup(
            Text("The ceiling is psychological, not structural",
                 font_size=28, color=GREEN, weight=BOLD),
            Text("The market demonstrated 146% of the energy",
                 font_size=20, color=WHITE),
            Text("needed to reach ATH, but stopped short.",
                 font_size=20, color=WHITE),
            Text("February 6, 2026",
                 font_size=18, color=GRAY),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)

        self.play(Create(conclusion_box), run_time=0.8)
        self.play(Write(conclusion), run_time=2.5)
        self.wait(3)
        self.play(FadeOut(conclusion_box), FadeOut(conclusion), run_time=1.5)


class ZMappingFormula(Scene):

    def construct(self):
        title = Text("Z-Mapping Analysis", font_size=46, weight=BOLD, color=BLUE)
        title.move_to(UP * 3.5)

        self.play(Write(title), run_time=1)
        self.wait(0.5)

        formula_parts = VGroup(
            Text("Z", font_size=68, color=YELLOW, weight=BOLD),
            Text("=", font_size=68, color=WHITE),
            Text("a", font_size=68, color=GREEN),
            Text("x", font_size=68, color=WHITE),
            Text("(b / c)", font_size=68, color=WHITE),
        ).arrange(RIGHT, buff=0.25).move_to(UP * 2.2)

        self.play(Write(formula_parts), run_time=1.5)
        self.wait(1)

        param_a = Text("a = Current price = 6,952.75", font_size=26, color=GREEN)
        param_b = Text("b = Daily move = 132.00", font_size=26, color=YELLOW)
        param_c = Text("c = 52-week high = 7,043.00", font_size=26, color=RED)

        params = VGroup(param_a, param_b, param_c)
        params.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.6)

        for param in params:
            self.play(Write(param), run_time=1)
            self.wait(0.3)

        self.wait(1)

        calc_line = Line(LEFT * 3.5, RIGHT * 3.5, color=WHITE).move_to(DOWN * 0.9)
        self.play(Create(calc_line), run_time=0.5)

        calc_1 = Text("Z = 6,952.75 x (132.00 / 7,043.00)", font_size=28)
        calc_2 = Text("Z = 6,952.75 x 0.01874", font_size=28)
        calc_3 = Text("Z = 130.31", font_size=38, color=YELLOW, weight=BOLD)

        calculation = VGroup(calc_1, calc_2, calc_3)
        calculation.arrange(DOWN, buff=0.3).move_to(DOWN * 1.8)

        for calc in calculation:
            self.play(Write(calc), run_time=1)
            self.wait(0.5)

        self.wait(2)

        insight_box = Rectangle(
            width=8.5, height=0.9, color=PURPLE,
            stroke_width=3, fill_opacity=0.2, fill_color=PURPLE
        ).move_to(DOWN * 3.4)

        insight = Text(
            "Z-value (~130) ~ Daily move (132) = Tight coupling regime",
            font_size=21, color=PURPLE, weight=BOLD
        ).move_to(insight_box.get_center())

        self.play(Create(insight_box), Write(insight), run_time=2)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)

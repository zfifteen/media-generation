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

# Color palette
BG_COLOR = "#0d1117"
ACCENT_BLUE = "#58a6ff"
ACCENT_GREEN = "#3fb950"
ACCENT_ORANGE = "#d29922"
ACCENT_RED = "#f85149"
ACCENT_PURPLE = "#bc8cff"
SUBTLE_GRAY = "#8b949e"
GRID_COLOR = "#21262d"
HIGHLIGHT_YELLOW = "#e3b341"


class PolarMotionDrift(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ====================================================================
        # ACT 1: TITLE CARD (0:00 - 0:08)
        # ====================================================================
        title = Text(
            "Polar Motion Drift Analysis",
            font_size=46, weight=BOLD, color=WHITE
        )
        subtitle = Text(
            "From Chandler Wobble to Linear Drift",
            font_size=28, color=ACCENT_BLUE
        )
        subtitle.next_to(title, DOWN, buff=0.35)

        date_line = Text(
            "Observation Window: Jan 23 - Feb 5, 2026",
            font_size=18, color=SUBTLE_GRAY
        )
        date_line.next_to(subtitle, DOWN, buff=0.5)

        title_group = VGroup(title, subtitle, date_line).move_to(ORIGIN)

        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.0)
        self.play(FadeIn(subtitle, shift=DOWN*0.2), run_time=0.8)
        self.play(FadeIn(date_line), run_time=0.6)
        self.wait(1.5)
        self.play(
            title_group.animate.scale(0.55).to_edge(UP, buff=0.3),
            run_time=1.0
        )
        self.wait(0.5)

        # ====================================================================
        # ACT 2: CHANDLER WOBBLE VISUALIZATION (0:08 - 0:30)
        # ====================================================================
        section_label = Text(
            "Historical: Chandler Wobble",
            font_size=30, color=ACCENT_ORANGE, weight=BOLD
        )
        section_label.next_to(title_group, DOWN, buff=0.4)
        self.play(Write(section_label), run_time=0.8)

        wobble_center = LEFT * 3.5 + DOWN * 1.0
        wobble_radius = 2.0

        ref_circle = Circle(
            radius=wobble_radius, color=SUBTLE_GRAY,
            stroke_width=1.5, stroke_opacity=0.5
        ).move_to(wobble_center)

        ref_label = Text(
            "200 mas boundary", font_size=14, color=SUBTLE_GRAY
        )
        ref_label.next_to(ref_circle, UP, buff=0.15)

        x_axis = Line(
            wobble_center + LEFT * 2.5, wobble_center + RIGHT * 2.5,
            color=GRID_COLOR, stroke_width=1.5
        )
        y_axis = Line(
            wobble_center + DOWN * 2.5, wobble_center + UP * 2.5,
            color=GRID_COLOR, stroke_width=1.5
        )
        x_label = Text("x_p (mas)", font_size=12, color=SUBTLE_GRAY)
        x_label.next_to(x_axis, RIGHT, buff=0.1).shift(DOWN*0.2)
        y_label = Text("y_p (mas)", font_size=12, color=SUBTLE_GRAY)
        y_label.next_to(y_axis, UP, buff=0.1).shift(LEFT*0.2)

        center_dot = Dot(wobble_center, radius=0.05, color=WHITE)
        center_label = Text("CIP", font_size=12, color=WHITE)
        center_label.next_to(center_dot, DOWN+RIGHT, buff=0.1)

        wobble_axes = VGroup(x_axis, y_axis, x_label, y_label, center_dot, center_label)
        self.play(
            Create(wobble_axes),
            Create(ref_circle),
            FadeIn(ref_label),
            run_time=1.2
        )

        chandler_period = 433.0 / 365.25
        annual_period = 1.0

        def wobble_path(t):
            cx = 0.8 * np.cos(2 * PI * t / chandler_period)
            cy = 0.8 * np.sin(2 * PI * t / chandler_period)
            ax = 0.4 * np.cos(2 * PI * t / annual_period)
            ay = 0.4 * np.sin(2 * PI * t / annual_period)
            return wobble_center + np.array([
                (cx + ax) * wobble_radius / 1.4,
                (cy + ay) * wobble_radius / 1.4,
                0
            ])

        wobble_trace = ParametricFunction(
            lambda t: wobble_path(t),
            t_range=[0, 6.0, 0.01],
            color=ACCENT_BLUE, stroke_width=2.0, stroke_opacity=0.8
        )

        wobble_dot = Dot(wobble_path(0), radius=0.08, color=ACCENT_BLUE)

        info_box = RoundedRectangle(
            width=6.5, height=4.5, corner_radius=0.2,
            color=GRID_COLOR, fill_color=GRID_COLOR, fill_opacity=0.3,
            stroke_width=1
        ).move_to(RIGHT * 3.8 + DOWN * 1.0)

        info_title = Text(
            "Chandler Wobble", font_size=24, color=ACCENT_BLUE, weight=BOLD
        )
        info_title.move_to(info_box.get_top() + DOWN * 0.4)

        info_lines = VGroup(
            Text("Period: ~433 days (14.2 months)", font_size=16, color=WHITE),
            Text("Amplitude: ~200 mas (historical)", font_size=16, color=WHITE),
            Text("Pattern: Quasi-circular oscillation", font_size=16, color=WHITE),
            Text("Cause: Free nutation of a deformable Earth", font_size=16, color=WHITE),
            Text("Beat period with annual: ~6.4 years", font_size=16, color=WHITE),
        )
        info_lines.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        info_lines.next_to(info_title, DOWN, buff=0.4)

        self.play(FadeIn(info_box), Write(info_title), run_time=0.8)

        self.play(
            Create(wobble_trace, run_time=4.0, rate_func=linear),
            FadeIn(wobble_dot),
        )

        for line in info_lines:
            self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.5)

        self.wait(1.0)

        amp_arrow = DoubleArrow(
            wobble_center, wobble_center + RIGHT * wobble_radius,
            color=ACCENT_ORANGE, stroke_width=2.5, buff=0,
            tip_length=0.15
        )
        amp_text = Text("~200 mas", font_size=16, color=ACCENT_ORANGE, weight=BOLD)
        amp_text.next_to(amp_arrow, DOWN, buff=0.15)

        self.play(GrowFromCenter(amp_arrow), FadeIn(amp_text), run_time=0.8)
        self.wait(1.5)

        # ====================================================================
        # ACT 3: WOBBLE EXTINCTION + LINEAR DRIFT (0:30 - 0:55)
        # ====================================================================
        old_elements = VGroup(
            section_label, wobble_trace, wobble_dot, wobble_axes,
            ref_circle, ref_label, amp_arrow, amp_text,
            info_box, info_title, info_lines
        )
        self.play(FadeOut(old_elements), run_time=0.8)

        section2_label = Text(
            "Transition: Wobble Collapse to Linear Drift",
            font_size=30, color=ACCENT_RED, weight=BOLD
        )
        section2_label.next_to(title_group, DOWN, buff=0.4)
        self.play(Write(section2_label), run_time=0.8)

        plot_center = DOWN * 1.2

        time_axis = Arrow(
            LEFT * 7 + plot_center + DOWN * 2.2,
            RIGHT * 7 + plot_center + DOWN * 2.2,
            color=WHITE, stroke_width=2, tip_length=0.15
        )
        time_label = Text("Time", font_size=16, color=SUBTLE_GRAY)
        time_label.next_to(time_axis, RIGHT, buff=0.1).shift(DOWN*0.15)

        amp_axis = Arrow(
            LEFT * 7 + plot_center + DOWN * 2.2,
            LEFT * 7 + plot_center + UP * 2.8,
            color=WHITE, stroke_width=2, tip_length=0.15
        )
        amp_label = Text("Displacement (mas)", font_size=14, color=SUBTLE_GRAY)
        amp_label.next_to(amp_axis, UP, buff=0.1)

        self.play(Create(time_axis), Create(amp_axis), FadeIn(time_label), FadeIn(amp_label), run_time=0.8)

        phase1_label = Text("Stable Wobble", font_size=14, color=ACCENT_BLUE)
        phase1_label.move_to(LEFT * 3.5 + plot_center + DOWN * 2.7)
        phase2_label = Text("Extinction", font_size=14, color=ACCENT_ORANGE)
        phase2_label.move_to(LEFT * 0.0 + plot_center + DOWN * 2.7)
        phase3_label = Text("Linear Drift", font_size=14, color=ACCENT_RED)
        phase3_label.move_to(RIGHT * 3.5 + plot_center + DOWN * 2.7)

        div1 = DashedLine(
            LEFT * 1.5 + plot_center + DOWN * 2.2,
            LEFT * 1.5 + plot_center + UP * 2.5,
            color=SUBTLE_GRAY, stroke_width=1, dash_length=0.1
        )
        div2 = DashedLine(
            RIGHT * 1.5 + plot_center + DOWN * 2.2,
            RIGHT * 1.5 + plot_center + UP * 2.5,
            color=SUBTLE_GRAY, stroke_width=1, dash_length=0.1
        )

        self.play(
            Create(div1), Create(div2),
            FadeIn(phase1_label), FadeIn(phase2_label), FadeIn(phase3_label),
            run_time=0.8
        )

        def signal_func(x):
            if x < -1.5:
                t_norm = (x + 7) / 5.5
                amplitude = 1.8
                return amplitude * np.sin(8 * PI * t_norm)
            elif x < 1.5:
                t_norm = (x + 1.5) / 3.0
                amplitude = 1.8 * (1 - t_norm)
                freq_shift = 8 * PI * ((x + 7) / 5.5)
                return amplitude * np.sin(freq_shift)
            else:
                t_norm = (x - 1.5) / 5.5
                return 0.15 + t_norm * 1.2

        signal_points_x = np.linspace(-7, 6.5, 1000)
        signal_points = [
            plot_center + np.array([x, signal_func(x), 0])
            for x in signal_points_x
        ]

        phase1_pts = [p for p, x in zip(signal_points, signal_points_x) if x < -1.5]
        phase1_curve = VMobject(color=ACCENT_BLUE, stroke_width=2.5)
        phase1_curve.set_points_smoothly(phase1_pts)

        self.play(Create(phase1_curve), run_time=2.0, rate_func=linear)

        phase2_pts = [p for p, x in zip(signal_points, signal_points_x) if -1.5 <= x < 1.5]
        phase2_curve = VMobject(color=ACCENT_ORANGE, stroke_width=2.5)
        phase2_curve.set_points_smoothly(phase2_pts)

        self.play(Create(phase2_curve), run_time=2.0, rate_func=linear)

        phase3_pts = [p for p, x in zip(signal_points, signal_points_x) if x >= 1.5]
        phase3_curve = VMobject(color=ACCENT_RED, stroke_width=2.5)
        phase3_curve.set_points_smoothly(phase3_pts)

        now_arrow = Arrow(
            RIGHT * 5.5 + plot_center + UP * 2.5,
            RIGHT * 5.5 + plot_center + UP * 0.8,
            color=HIGHLIGHT_YELLOW, stroke_width=2.5, tip_length=0.15
        )
        now_label = Text("NOW", font_size=18, color=HIGHLIGHT_YELLOW, weight=BOLD)
        now_label.next_to(now_arrow, UP, buff=0.1)

        self.play(
            Create(phase3_curve, run_time=2.5, rate_func=linear),
        )
        self.play(
            GrowArrow(now_arrow), FadeIn(now_label),
            run_time=0.6
        )

        callout_box = RoundedRectangle(
            width=5.5, height=1.2, corner_radius=0.15,
            color=ACCENT_RED, fill_color=ACCENT_RED, fill_opacity=0.1,
            stroke_width=1.5
        ).move_to(RIGHT * 3.5 + plot_center + UP * 2.5)

        callout_text = Text(
            "Circular wobble replaced by\nstraight-line movement",
            font_size=16, color=WHITE, line_spacing=1.3
        ).move_to(callout_box)

        self.play(FadeIn(callout_box), Write(callout_text), run_time=1.0)
        self.wait(2.0)

        # ====================================================================
        # ACT 4: PARAMETER TABLE (0:55 - 1:15)
        # ====================================================================
        all_act3 = VGroup(
            section2_label, time_axis, time_label, amp_axis, amp_label,
            div1, div2, phase1_label, phase2_label, phase3_label,
            phase1_curve, phase2_curve, phase3_curve,
            now_arrow, now_label, callout_box, callout_text
        )
        self.play(FadeOut(all_act3), run_time=0.8)

        section3_label = Text(
            "Quantifying the Drift",
            font_size=30, color=ACCENT_GREEN, weight=BOLD
        )
        section3_label.next_to(title_group, DOWN, buff=0.4)
        self.play(Write(section3_label), run_time=0.8)

        # ---- FIXED TABLE: Use Manim's built-in Table for clean columns ----
        # Build each row as a VGroup of Text objects with explicit column positions
        col_widths = [2.0, 2.2, 2.8, 5.5]
        col_centers = []
        total_width = sum(col_widths) + 0.6  # padding
        running_x = -total_width / 2
        for w in col_widths:
            col_centers.append(running_x + w / 2)
            running_x += w

        table_top_y = 1.2
        row_spacing = 0.6

        header_data = ["Parameter", "Role", "Value", "Rationale"]
        row_data = [
            ["a", "Duration", "14 days", "Linear phase: Jan 23 to Feb 5"],
            ["b", "Drift Rate", "0.93 mas/day", "~26.9 mas over 29 days"],
            ["c", "Upper Limit", "200 mas", "Historical Chandler amplitude"],
        ]
        row_colors = [ACCENT_GREEN, ACCENT_BLUE, ACCENT_ORANGE]

        all_table_elements = VGroup()

        # Header row
        header_group = VGroup()
        for col_idx, htext in enumerate(header_data):
            t = Text(htext, font_size=17, color=ACCENT_PURPLE, weight=BOLD)
            t.move_to(np.array([col_centers[col_idx], table_top_y, 0]))
            header_group.add(t)
        all_table_elements.add(header_group)

        # Header underline
        header_line = Line(
            np.array([-total_width / 2, table_top_y - 0.28, 0]),
            np.array([total_width / 2, table_top_y - 0.28, 0]),
            color=ACCENT_PURPLE, stroke_width=1.5
        )
        all_table_elements.add(header_line)

        # Data rows
        data_row_groups = []
        for row_idx, (rdata, rcolor) in enumerate(zip(row_data, row_colors)):
            row_y = table_top_y - (row_idx + 1) * row_spacing
            rg = VGroup()
            for col_idx, cell_text in enumerate(rdata):
                if col_idx == 0:
                    color = rcolor
                    weight = BOLD
                elif col_idx == 2:
                    color = HIGHLIGHT_YELLOW
                    weight = BOLD
                else:
                    color = WHITE
                    weight = NORMAL
                t = Text(cell_text, font_size=16, color=color, weight=weight)
                t.move_to(np.array([col_centers[col_idx], row_y, 0]))
                rg.add(t)
            data_row_groups.append(rg)
            all_table_elements.add(rg)

        # Table background
        table_bg = RoundedRectangle(
            width=total_width + 0.8,
            height=row_spacing * 4 + 0.4,
            corner_radius=0.15,
            color=GRID_COLOR,
            fill_color=GRID_COLOR,
            fill_opacity=0.25,
            stroke_width=1
        ).move_to(np.array([0, table_top_y - row_spacing * 1.5, 0]))

        self.play(FadeIn(table_bg), run_time=0.5)
        self.play(FadeIn(header_group), FadeIn(header_line), run_time=0.6)
        self.wait(0.3)
        for rg in data_row_groups:
            self.play(FadeIn(rg, shift=RIGHT * 0.15), run_time=0.6)
            self.wait(0.3)

        self.wait(1.0)

        # ====================================================================
        # ACT 5: COMPUTATION (1:15 - 1:35)
        # ====================================================================
        formula_label = Text("Computing the Drift Ratio:", font_size=22, color=WHITE, weight=BOLD)
        formula_label.move_to(DOWN * 1.5)

        step1 = MathTex(
            r"\text{Ratio} = \frac{a \times b}{c}",
            font_size=36, color=WHITE
        ).next_to(formula_label, DOWN, buff=0.4)

        self.play(Write(formula_label), run_time=0.6)
        self.play(Write(step1), run_time=1.0)
        self.wait(0.8)

        step2 = MathTex(
            r"= \frac{14 \times 0.93}{200}",
            font_size=36, color=ACCENT_BLUE
        ).next_to(step1, DOWN, buff=0.3)

        self.play(Write(step2), run_time=1.0)
        self.wait(0.6)

        step3 = MathTex(
            r"= \frac{13.02}{200}",
            font_size=36, color=ACCENT_GREEN
        ).next_to(step2, DOWN, buff=0.3)

        self.play(Write(step3), run_time=0.8)
        self.wait(0.5)

        result = MathTex(
            r"= 0.0651",
            font_size=42, color=HIGHLIGHT_YELLOW
        ).next_to(step3, DOWN, buff=0.3)

        result_box = SurroundingRectangle(
            result, color=HIGHLIGHT_YELLOW, buff=0.15,
            corner_radius=0.1, stroke_width=2
        )

        self.play(Write(result), Create(result_box), run_time=1.0)
        self.wait(1.0)

        pct_text = Text(
            "~ 6.5% of the historical stable range",
            font_size=20, color=HIGHLIGHT_YELLOW
        ).next_to(result_box, DOWN, buff=0.3)

        self.play(FadeIn(pct_text, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)

        # ====================================================================
        # ACT 6: PROGRESS BAR VISUALIZATION (1:35 - 1:48)
        # ====================================================================
        all_act4_5 = VGroup(
            section3_label, table_bg, all_table_elements,
            formula_label, step1, step2, step3,
            result, result_box, pct_text
        )
        self.play(FadeOut(all_act4_5), run_time=0.8)

        section4_label = Text(
            "Fractional Progress Through Stable Range",
            font_size=30, color=HIGHLIGHT_YELLOW, weight=BOLD
        )
        section4_label.next_to(title_group, DOWN, buff=0.4)
        self.play(Write(section4_label), run_time=0.8)

        bar_width = 12.0
        bar_height = 1.2
        bar_bg = RoundedRectangle(
            width=bar_width, height=bar_height,
            corner_radius=0.15, color=SUBTLE_GRAY,
            fill_color=GRID_COLOR, fill_opacity=0.4,
            stroke_width=2
        ).move_to(UP * 0.3)

        bar_label_0 = Text("0 mas", font_size=14, color=SUBTLE_GRAY)
        bar_label_0.next_to(bar_bg, LEFT, buff=0.15)
        bar_label_200 = Text("200 mas", font_size=14, color=SUBTLE_GRAY)
        bar_label_200.next_to(bar_bg, RIGHT, buff=0.15)
        bar_top_label = Text(
            "Historical Chandler Wobble Amplitude",
            font_size=16, color=SUBTLE_GRAY
        ).next_to(bar_bg, UP, buff=0.2)

        self.play(
            FadeIn(bar_bg), FadeIn(bar_label_0),
            FadeIn(bar_label_200), FadeIn(bar_top_label),
            run_time=0.8
        )

        fill_tracker = ValueTracker(0)

        def get_fill():
            w = fill_tracker.get_value() * bar_width
            if w < 0.01:
                w = 0.01
            fill = RoundedRectangle(
                width=w, height=bar_height - 0.1,
                corner_radius=0.1, color=ACCENT_RED,
                fill_color=ACCENT_RED, fill_opacity=0.7,
                stroke_width=0
            )
            fill.align_to(bar_bg, LEFT).shift(RIGHT * 0.05)
            return fill

        fill_bar = always_redraw(get_fill)
        self.add(fill_bar)

        pct_counter = always_redraw(
            lambda: Text(
                f"{fill_tracker.get_value() * 100:.1f}%",
                font_size=36, color=HIGHLIGHT_YELLOW, weight=BOLD
            ).next_to(bar_bg, DOWN, buff=0.5)
        )
        self.add(pct_counter)

        self.play(fill_tracker.animate.set_value(0.065), run_time=2.5, rate_func=smooth)
        self.wait(0.5)

        fill_width = bar_width * 0.065
        marker_x = bar_bg.get_left()[0] + 0.05 + fill_width
        marker_line = DashedLine(
            np.array([marker_x, bar_bg.get_top()[1] + 0.3, 0]),
            np.array([marker_x, bar_bg.get_bottom()[1] - 0.3, 0]),
            color=HIGHLIGHT_YELLOW, stroke_width=2, dash_length=0.08
        )
        marker_label = Text(
            "13 mas traversed", font_size=14, color=HIGHLIGHT_YELLOW
        ).next_to(marker_line, UP, buff=0.1)

        self.play(Create(marker_line), FadeIn(marker_label), run_time=0.6)
        self.wait(0.5)

        remaining_brace = BraceBetweenPoints(
            np.array([marker_x + 0.1, bar_bg.get_bottom()[1] - 0.35, 0]),
            np.array([bar_bg.get_right()[0] - 0.05, bar_bg.get_bottom()[1] - 0.35, 0]),
            direction=DOWN, color=SUBTLE_GRAY
        )
        remaining_text = Text(
            "~187 mas remaining (93.5%)",
            font_size=14, color=SUBTLE_GRAY
        ).next_to(remaining_brace, DOWN, buff=0.15)

        self.play(FadeIn(remaining_brace), FadeIn(remaining_text), run_time=0.8)
        self.wait(1.5)

        # ====================================================================
        # ACT 7: INTERPRETATION + HOLD ON SCREEN (1:48 - 1:55)
        # ====================================================================
        # Snapshot the dynamic updaters before removing them
        fill_bar_snapshot = get_fill()
        pct_final = Text(
            f"{fill_tracker.get_value() * 100:.1f}%",
            font_size=36, color=HIGHLIGHT_YELLOW, weight=BOLD
        ).next_to(bar_bg, DOWN, buff=0.5)
        self.remove(fill_bar, pct_counter)
        self.add(fill_bar_snapshot, pct_final)

        all_act6 = VGroup(
            section4_label, bar_bg, bar_label_0, bar_label_200,
            bar_top_label, marker_line, marker_label,
            remaining_brace, remaining_text,
            fill_bar_snapshot, pct_final
        )
        self.play(FadeOut(all_act6), run_time=0.7)
        self.play(FadeOut(title_group), run_time=0.5)

        # Final interpretation card
        final_title = Text(
            "Interpretation", font_size=40, color=WHITE, weight=BOLD
        ).move_to(UP * 3.2)

        bullets = VGroup(
            Text(
                "Only 6.5% of the historical stable amplitude traversed",
                font_size=20, color=ACCENT_GREEN
            ),
            Text(
                "Indicates an incipient transition, not a completed shift",
                font_size=20, color=ACCENT_BLUE
            ),
            Text(
                "Potential for escalation during reduced external resistance",
                font_size=20, color=ACCENT_ORANGE
            ),
            Text(
                "GPS, navigation, and climate models warrant close monitoring",
                font_size=20, color=ACCENT_RED
            ),
        )
        bullets.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        bullets.next_to(final_title, DOWN, buff=0.6)

        for b in bullets:
            dot = Dot(radius=0.06, color=b.color)
            dot.next_to(b, LEFT, buff=0.2)
            b.add(dot)

        final_group = VGroup(final_title, bullets).move_to(ORIGIN + UP * 0.5)

        self.play(Write(final_title), run_time=0.6)
        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.5)
            self.wait(0.3)

        ratio_display = MathTex(
            r"\frac{a \times b}{c} = \frac{14 \times 0.93}{200} = 0.0651",
            font_size=36, color=HIGHLIGHT_YELLOW
        ).next_to(bullets, DOWN, buff=0.7)

        ratio_box = SurroundingRectangle(
            ratio_display, color=HIGHLIGHT_YELLOW, buff=0.2,
            corner_radius=0.1, stroke_width=2
        )

        self.play(Write(ratio_display), Create(ratio_box), run_time=1.0)

        # ---- FIX: Hold the final frame, do NOT fade to black ----
        self.wait(3.0)

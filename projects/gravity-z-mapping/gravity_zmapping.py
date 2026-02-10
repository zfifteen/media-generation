"""
Z-Mapping Analysis: Gravity Anomaly Coupling
Visualizes the hidden algebraic structure linking wide binary observations
to the QI/MOND theoretical gap.

SYNCHRONIZED TO 51.5s VOICEOVER
"""

from manim import *
import numpy as np

# ============================================================================
# OPTIMIZED CONFIGURATION - DO NOT MODIFY THESE VALUES
# ============================================================================
config.frame_height = 10        # Moderate zoom out (25% larger than default 8)
config.frame_width = 10 * 16/9  # Maintains 16:9 aspect ratio (~17.78)
config.pixel_height = 1440      # High quality 1440p resolution
config.pixel_width = 2560       # Crisp text and graphics
# ============================================================================


class GravityAnomalyZMapping(Scene):
    """
    Main scene synchronized to 154.8 second voiceover.

    CORRECTED TIMING:
    0.00s - 5.88s: Title & Intro (Lag fixed)
    5.88s - 21.59s: Parameter A
    21.59s - 41.63s: Parameter B
    41.63s - 53.81s: Parameter C
    53.81s - 64.79s: Formula Calculation
    64.79s - 76.87s: Cancellation Steps
    76.87s - 93.93s: Result & Coupling Revealed
    93.93s - 154.82s: Split & Interpretation
    """

    def construct(self):
        # Scene 1: Title (0.00s - 5.88s)
        self.show_title()

        # Scene 2: Parameters (5.88s - 53.81s)
        self.show_parameters()

        # Scene 3: Calculation (53.81s - 64.79s)
        self.show_calculation()

        # Scene 4: Cancellation (64.79s - 93.93s)
        self.show_cancellation()

        # Scene 5: Split (93.93s - 154.82s)
        self.show_split()

    def show_title(self):
        """
        Opening title sequence
        TIMING: 0.00s - 5.88s
        """
        title = Text("Gravity's Hidden Structure", font_size=48, weight=BOLD, color=BLUE)
        subtitle = Text("Z-Mapping the Low-Acceleration Regime", font_size=28, color=WHITE)

        title.move_to(UP * 3.8)
        subtitle.next_to(title, DOWN, buff=0.4)

        # 0.00s - 1.59s: Title appears
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP*0.2), run_time=0.25)
        self.wait(0.54) # Gap to silence_start 1.59

        # 1.59s - 5.88s: Intro VO + Transition
        # Fade title to corner while second sentence plays
        self.play(
            VGroup(title, subtitle).animate.scale(0.5).move_to(UP * 4.2 + LEFT * 5),
            run_time=2.0
        )
        self.wait(2.29) # Until 5.88s

        # Store for reference
        self.title_group = VGroup(title, subtitle)

    def show_parameters(self):
        """
        Display the three parameters
        TIMING: 5.88s - 53.81s
        """
        # PARAMETER A
        # 5.88s - 21.59s
        param_a = self.create_param_box(
            "a",
            "Observed Gravity Boost",
            "γ = 3/2 = 1.5",
            YELLOW,
            UP * 2
        )
        self.play(FadeIn(param_a, shift=RIGHT*0.5), run_time=0.5)
        self.wait(15.21) # Wait until silence_end 21.59

        # PARAMETER B
        # 21.59s - 41.63s
        param_b = self.create_param_box(
            "b",
            "Theory Ratio",
            "a_min(QI) / a_0(MOND) = 5/3",
            GREEN,
            ORIGIN
        )
        self.play(FadeIn(param_b, shift=RIGHT*0.5), run_time=0.5)
        self.wait(19.54) # Wait until silence_end 41.63

        # PARAMETER C
        # 41.63s - 53.81s
        param_c = self.create_param_box(
            "c",
            "Newtonian Ceiling",
            "γ_Newton = 1",
            RED,
            DOWN * 2
        )
        self.play(FadeIn(param_c, shift=RIGHT*0.5), run_time=0.5)
        self.wait(11.68) # Wait until silence_end 53.81

        self.params_group = VGroup(param_a, param_b, param_c)

    def create_param_box(self, label, description, value, color, position):
        """Helper to create parameter display boxes"""
        box = Rectangle(width=6, height=1.2, color=color, stroke_width=3)

        label_text = Text(label, font_size=32, weight=BOLD, color=color)
        label_text.move_to(box.get_left() + RIGHT * 0.5)

        desc_text = Text(description, font_size=18, color=WHITE)
        desc_text.next_to(label_text, RIGHT, buff=0.3)

        value_text = MathTex(value.replace("γ", r"\gamma").replace("_", r"\_"),
                             font_size=20, color=color)
        value_text.next_to(box, DOWN, buff=0.15)

        group = VGroup(box, label_text, desc_text, value_text)
        group.move_to(position)

        return group

    def show_calculation(self):
        """
        Show the calculation steps
        TIMING: 53.81s - 64.79s
        """
        # 53.81s - 54.81s: Transition
        self.play(
            self.params_group.animate.scale(0.7).move_to(LEFT * 4.5),
            run_time=1.0
        )

        formula_title = Text("Z-Mapping Formula", font_size=32, color=BLUE)
        formula_title.move_to(UP * 3.5 + RIGHT * 3)
        formula_line1 = MathTex(r"Z = a \times \frac{b}{c}", font_size=40).move_to(UP * 2.5 + RIGHT * 3)

        self.play(Write(formula_title), run_time=0.8)
        self.play(Write(formula_line1), run_time=1.0)
        self.wait(1.76) # Until 58.37s

        formula_line2 = MathTex(r"Z = \frac{3}{2} \times \frac{5/3}{1}", font_size=40).move_to(UP * 1.5 + RIGHT * 3)
        self.play(TransformFromCopy(formula_line1, formula_line2), run_time=1.0)
        self.wait(2.06) # Until 61.43s

        formula_line3 = MathTex(r"Z = \frac{3}{2} \times \frac{5}{3}", font_size=40).move_to(UP * 0.5 + RIGHT * 3)
        self.play(TransformFromCopy(formula_line2, formula_line3), run_time=1.0)
        self.wait(2.36) # Until 64.79s

        self.calc_group = VGroup(formula_title, formula_line1, formula_line2, formula_line3)

    def show_cancellation(self):
        """
        Cancellation reveal
        TIMING: 64.79s - 93.93s
        """
        self.wait(9.08) # Until 73.87s

        highlight_box1 = SurroundingRectangle(self.calc_group[-1][0][2], color=ORANGE, buff=0.1)
        highlight_box2 = SurroundingRectangle(self.calc_group[-1][0][6], color=ORANGE, buff=0.1)
        self.play(Create(highlight_box1), Create(highlight_box2), run_time=0.8)

        cancel_line1 = Line(self.calc_group[-1][0][2].get_corner(DL), self.calc_group[-1][0][2].get_corner(UR), color=RED)
        cancel_line2 = Line(self.calc_group[-1][0][6].get_corner(DL), self.calc_group[-1][0][6].get_corner(UR), color=RED)
        self.play(Create(cancel_line1), Create(cancel_line2), run_time=0.8)
        self.wait(1.4) # Until 76.87s

        result = MathTex(r"Z = \frac{5}{2} = 2.5", font_size=56, color=YELLOW).move_to(DOWN * 1 + RIGHT * 3)
        self.play(Write(result), FadeOut(highlight_box1), FadeOut(highlight_box2), run_time=1.2)
        self.wait(5.85) # Until 83.92s

        insight = Text("The 3s cancel!\nCoupling revealed.", font_size=22, color=GREEN).move_to(DOWN * 2.5 + RIGHT * 3)
        self.play(FadeIn(insight, shift=UP*0.3), run_time=0.8)
        self.wait(9.21) # Until 93.93s

        self.play(FadeOut(self.params_group), FadeOut(self.calc_group), FadeOut(cancel_line1), 
                  FadeOut(cancel_line2), FadeOut(result), FadeOut(insight), run_time=1.0)

    def show_split(self):
        """
        Pie chart and interpretation
        TIMING: 93.93s - 154.82s
        """
        split_title = Text("The Gravitational Budget", font_size=40, weight=BOLD, color=BLUE).move_to(UP * 3.8)
        self.play(Write(split_title), run_time=1.2)
        self.wait(2.77) # Until 97.90s

        circle_radius = 2.5
        newtonian_sector = Sector(radius=circle_radius, start_angle=0, angle=144 * DEGREES, color=RED, fill_opacity=0.4)
        anomalous_sector = Sector(radius=circle_radius, start_angle=144 * DEGREES, angle=216 * DEGREES, color=YELLOW, fill_opacity=0.4)
        self.play(Create(newtonian_sector), run_time=1.5)
        self.play(Create(anomalous_sector), run_time=1.5)

        newton_label = VGroup(Text("Newtonian", font_size=24, color=RED), Text("40%", font_size=32, color=RED)).arrange(DOWN).move_to(LEFT * 1.5 + DOWN * 0.8)
        anomaly_label = VGroup(Text("Anomalous", font_size=24, color=YELLOW), Text("60%", font_size=32, color=YELLOW)).arrange(DOWN).move_to(RIGHT * 1.5 + UP * 0.8)
        self.play(FadeIn(newton_label), FadeIn(anomaly_label), run_time=1.2)
        self.wait(7.66) # Until 109.76s

        z_ratio = MathTex(r"Z = 2.5 \quad \Rightarrow \quad \frac{1}{Z} = 0.4", font_size=32).move_to(DOWN * 3.5)
        self.play(Write(z_ratio), run_time=1.2)
        self.wait(21.35) # Until 132.31s

        interpretation = Text("Classical physics owns less than half the story", font_size=20, color=GRAY, slant=ITALIC).next_to(z_ratio, DOWN)
        self.play(FadeIn(interpretation, shift=UP*0.2), run_time=1.0)
        self.wait(21.51) # Final buffer
        """Helper to create parameter display boxes"""
        box = Rectangle(width=6, height=1.2, color=color, stroke_width=3)

        label_text = Text(label, font_size=32, weight=BOLD, color=color)
        label_text.move_to(box.get_left() + RIGHT * 0.5)

        desc_text = Text(description, font_size=18, color=WHITE)
        desc_text.next_to(label_text, RIGHT, buff=0.3)

        value_text = MathTex(value.replace("γ", r"\gamma").replace("_", r"\_"),
                             font_size=20, color=color)
        value_text.next_to(box, DOWN, buff=0.15)

        group = VGroup(box, label_text, desc_text, value_text)
        group.move_to(position)

        return group

    def show_calculation(self):
        """
        Show the Z = a × (b/c) calculation
        TIMING: 53.81s - 64.79s
        """
        # 53.81s - 54.81s: Move parameters to left (1.0s)
        self.play(
            self.params_group.animate.scale(0.7).move_to(LEFT * 4.5),
            run_time=1.0
        )

        # 54.81s - 58.37s: Formula title and first line
        formula_title = Text("Z-Mapping Formula", font_size=32, color=BLUE)
        formula_title.move_to(UP * 3.5 + RIGHT * 3)

        formula_line1 = MathTex(
            r"Z = a \times \frac{b}{c}",
            font_size=40
        )
        formula_line1.move_to(UP * 2.5 + RIGHT * 3)

        self.play(Write(formula_title), run_time=0.8)
        self.play(Write(formula_line1), run_time=1.0)
        self.wait(1.76) # Until 58.37s

        # 58.37s - 61.43s: Substitution step
        formula_line2 = MathTex(
            r"Z = \frac{3}{2} \times \frac{5/3}{1}",
            font_size=40
        )
        formula_line2.move_to(UP * 1.5 + RIGHT * 3)

        self.play(TransformFromCopy(formula_line1, formula_line2), run_time=1.0)
        self.wait(2.06) # Until 61.43s

        # 61.43s - 64.79s: Simplified form
        formula_line3 = MathTex(
            r"Z = \frac{3}{2} \times \frac{5}{3}",
            font_size=40
        )
        formula_line3.move_to(UP * 0.5 + RIGHT * 3)

        self.play(TransformFromCopy(formula_line2, formula_line3), run_time=1.0)
        self.wait(2.36) # Until 64.79s

        # Store for next scene
        self.calc_group = VGroup(formula_title, formula_line1, formula_line2, formula_line3)

    def show_cancellation(self):
        """
        Reveal the factor-of-3 cancellation
        TIMING: 64.79s - 93.93s
        """
        # 64.79s - 73.87s: Fraction structure narration (9.08s)
        self.wait(9.08)

        # 73.87s - 76.87s: Highlight and cancel
        highlight_box1 = SurroundingRectangle(
            self.calc_group[-1][0][2],
            color=ORANGE,
            buff=0.1
        )
        highlight_box2 = SurroundingRectangle(
            self.calc_group[-1][0][6],
            color=ORANGE,
            buff=0.1
        )

        self.play(
            Create(highlight_box1),
            Create(highlight_box2),
            run_time=0.8
        )

        cancel_line1 = Line(
            self.calc_group[-1][0][2].get_corner(DL),
            self.calc_group[-1][0][2].get_corner(UR),
            color=RED,
            stroke_width=4
        )
        cancel_line2 = Line(
            self.calc_group[-1][0][6].get_corner(DL),
            self.calc_group[-1][0][6].get_corner(UR),
            color=RED,
            stroke_width=4
        )

        self.play(
            Create(cancel_line1),
            Create(cancel_line2),
            run_time=0.8
        )
        self.wait(1.4) # Until 76.87s

        # 76.87s - 83.92s: Show result
        result = MathTex(
            r"Z = \frac{5}{2} = 2.5",
            font_size=56,
            color=YELLOW
        )
        result.move_to(DOWN * 1 + RIGHT * 3)

        self.play(
            Write(result),
            FadeOut(highlight_box1),
            FadeOut(highlight_box2),
            run_time=1.2
        )
        self.wait(5.85) # Until 83.92s

        # 83.92s - 93.93s: Insight text
        insight = Text(
            "The 3s cancel!\nCoupling revealed.",
            font_size=22,
            color=GREEN,
            line_spacing=1.2
        )
        insight.move_to(DOWN * 2.5 + RIGHT * 3)

        self.play(FadeIn(insight, shift=UP*0.3), run_time=0.8)
        self.wait(9.21) # Until 93.93s

        # Clear for next scene
        self.play(
            FadeOut(self.params_group),
            FadeOut(self.calc_group),
            FadeOut(cancel_line1),
            FadeOut(cancel_line2),
            FadeOut(result),
            FadeOut(insight),
            run_time=1.0
        )

    def show_split(self):
        """
        Show the 60/40 Newtonian vs Anomalous split
        TIMING: 93.93s - 154.82s
        """
        # 93.93s - 97.90s: Title transition
        split_title = Text("The Gravitational Budget", font_size=40, weight=BOLD, color=BLUE)
        split_title.move_to(UP * 3.8)

        self.play(Write(split_title), run_time=1.2)
        self.wait(2.77) # Until 97.90s

        # Create pie chart
        circle_center = ORIGIN
        circle_radius = 2.5

        # 97.90s - 109.76s: Draw sectors and show labels
        newtonian_sector = Sector(
            radius=circle_radius,
            start_angle=0,
            angle=144 * DEGREES,
            color=RED,
            fill_opacity=0.4,
            stroke_width=3
        )
        newtonian_sector.move_arc_center_to(circle_center)

        anomalous_sector = Sector(
            radius=circle_radius,
            start_angle=144 * DEGREES,
            angle=216 * DEGREES,
            color=YELLOW,
            fill_opacity=0.4,
            stroke_width=3
        )
        anomalous_sector.move_arc_center_to(circle_center)

        self.play(Create(newtonian_sector), run_time=1.5)
        self.play(Create(anomalous_sector), run_time=1.5)

        newton_label = VGroup(
            Text("Newtonian", font_size=24, color=RED, weight=BOLD),
            Text("40%", font_size=32, color=RED, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        newton_label.move_to(circle_center + LEFT * 1.5 + DOWN * 0.8)

        anomaly_label = VGroup(
            Text("Anomalous", font_size=24, color=YELLOW, weight=BOLD),
            Text("60%", font_size=32, color=YELLOW, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        anomaly_label.move_to(circle_center + RIGHT * 1.5 + UP * 0.8)

        self.play(
            FadeIn(newton_label, shift=RIGHT*0.3),
            FadeIn(anomaly_label, shift=LEFT*0.3),
            run_time=1.2
        )
        self.wait(7.66) # Until 109.76s

        # 109.76s - 132.31s: Show math
        z_ratio = MathTex(
            r"Z = 2.5 \quad \Rightarrow \quad \frac{1}{Z} = 0.4",
            font_size=32,
            color=WHITE
        )
        z_ratio.move_to(DOWN * 3.5)

        self.play(Write(z_ratio), run_time=1.2)
        self.wait(21.35) # Until 132.31s

        # 132.31s - 154.82s: Conclusion
        interpretation = Text(
            "Classical physics owns less than half the story",
            font_size=20,
            color=GRAY,
            slant=ITALIC
        )
        interpretation.next_to(z_ratio, DOWN, buff=0.3)

        self.play(FadeIn(interpretation, shift=UP*0.2), run_time=1.0)
        self.wait(21.51) # Final hold


class WideFrameCheck(Scene):
    """Diagnostic scene to verify frame boundaries"""

    def construct(self):
        frame_box = Rectangle(
            width=config.frame_width - 0.2,
            height=config.frame_height - 0.2,
            color=RED,
            stroke_width=2
        )
        frame_box.move_to(ORIGIN)

        safe_box = Rectangle(
            width=14,
            height=8,
            color=GREEN,
            stroke_width=2
        )
        safe_box.move_to(ORIGIN)

        label_top = Text("TOP (y=4.5)", font_size=18, color=RED)
        label_top.move_to(UP * 4.3)

        label_bottom = Text("BOTTOM (y=-4.5)", font_size=18, color=RED)
        label_bottom.move_to(DOWN * 4.3)

        label_left = Text("LEFT\n(x=-8.9)", font_size=18, color=RED)
        label_left.move_to(LEFT * 8.2)

        label_right = Text("RIGHT\n(x=8.9)", font_size=18, color=RED)
        label_right.move_to(RIGHT * 8.2)

        safe_label = Text("SAFE ZONE (±7, ±4)", font_size=24, color=GREEN, weight=BOLD)
        safe_label.move_to(ORIGIN)

        self.add(frame_box, safe_box)
        self.add(label_top, label_bottom, label_left, label_right)
        self.add(safe_label)
        self.wait(3)

from manim import *
import numpy as np

# config.frame_height = 14  # Default is 8
# config.frame_width = 14 * 16/9  # Maintain 16:9 aspect ratio (~24.89)

class GeometricResonancePrimePrediction(Scene):
    def construct(self):
        # Title and core concept
        title = Text("Emergent Asymptotic Precision", font_size=40, weight=BOLD)
        subtitle = Text("Geometric Resonance Prime Prediction", font_size=28, color=BLUE_C)
        subtitle.next_to(title, DOWN, buff=0.2)

        title_group = VGroup(title, subtitle).move_to(ORIGIN)
        self.play(Write(title_group))
        self.wait()
        self.play(title_group.animate.scale(0.5).to_edge(UP, buff=0.3))

        # Section 1: Dual-Adapter Architecture
        arch_title = Text("Dual-Adapter Architecture", font_size=32, color=YELLOW).next_to(title_group, DOWN, buff=0.4)
        self.play(Write(arch_title))

        # Create two adapter boxes
        c_adapter = RoundedRectangle(
            width=3, height=2.5, corner_radius=0.2,
            color=GREEN, fill_opacity=0.1
        ).shift(LEFT * 3.5 + DOWN * 0.5)

        c_label = Text("z5d_adapter.c", font_size=20, weight=BOLD, color=GREEN).next_to(c_adapter, UP, buff=0.1)
        c_tech = VGroup(
            Text("MPFR/GMP", font_size=14),
            Text("uint64_t", font_size=14),
            Text("Fixed precision", font_size=14)
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).scale(0.8).move_to(c_adapter.get_center())

        py_adapter = RoundedRectangle(
            width=3, height=2.5, corner_radius=0.2,
            color=BLUE, fill_opacity=0.1
        ).shift(RIGHT * 3.5 + DOWN * 0.5)

        py_label = Text("z5d_adapter.py", font_size=20, weight=BOLD, color=BLUE).next_to(py_adapter, UP, buff=0.1)
        py_tech = VGroup(
            Text("gmpy2/mpmath", font_size=14),
            Text("Dynamic precision", font_size=14),
            Text("Arbitrary scale", font_size=14)
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).scale(0.8).move_to(py_adapter.get_center())

        adapters = VGroup(
            c_adapter, c_label, c_tech,
            py_adapter, py_label, py_tech
        ).move_to(ORIGIN).shift(DOWN * 0.3)

        self.play(Create(c_adapter), Write(c_label))
        self.play(FadeIn(c_tech))
        self.wait(0.3)
        self.play(Create(py_adapter), Write(py_label))
        self.play(FadeIn(py_tech))
        self.wait()

        # Transition to asymptotic precision
        self.play(
            FadeOut(arch_title),
            FadeOut(adapters)
        )

        # Section 2: Asymptotic Precision Enhancement
        asym_title = Text("Asymptotic Precision Enhancement", font_size=32, color=ORANGE).next_to(title_group, DOWN, buff=0.4)
        self.play(Write(asym_title))

        # Create axes for z5d_score progression
        axes = Axes(
            x_range=[0, 1300, 200],
            y_range=[-10, -4, 1],
            x_length=9,
            y_length=4,
            axis_config={"color": GREY},
            tips=False
        ).shift(DOWN * 0.8)

        x_label = Text("Scale (powers of 10)", font_size=18).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text("z5d_score", font_size=18).next_to(axes.y_axis, LEFT, buff=0.3).rotate(PI/2)

        # Data points from FINDINGS.md
        data_points = [
            (100, -5.62, "0.00024%"),
            (300, -6.89, "0.00013%"),
            (600, -7.78, "0.00017%"),
            (900, -8.34, "0.00005%"),
            (1233, -8.84, "0.000014%")
        ]

        dots = VGroup()
        labels = VGroup()

        for x, y, error in data_points:
            dot = Dot(axes.c2p(x, y), color=YELLOW, radius=0.08)
            error_label = Text(error, font_size=12, color=RED).next_to(dot, UP, buff=0.15)
            dots.add(dot)
            labels.add(error_label)

        # Asymptotic curve
        curve = axes.plot(
            lambda x: -4 - 0.004 * x,
            x_range=[100, 1233],
            color=BLUE,
            stroke_width=3
        )

        chart_group = VGroup(axes, x_label, y_label, curve, dots, labels)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(curve), run_time=2)
        self.play(LaggedStart(*[Create(dot) for dot in dots], lag_ratio=0.3))
        self.play(LaggedStart(*[Write(label) for label in labels], lag_ratio=0.2))

        # Highlight asymptotic trend
        trend_arrow = Arrow(
            axes.c2p(100, -5.5), axes.c2p(1200, -8.8),
            color=GREEN, stroke_width=6, buff=0
        )
        trend_text = Text("Errors diminish\nwith scale", font_size=16, color=GREEN).next_to(trend_arrow, RIGHT, buff=0.2)

        chart_group.add(trend_arrow, trend_text)
        chart_group.move_to(ORIGIN).shift(DOWN * 0.3)

        self.play(GrowArrow(trend_arrow), Write(trend_text))
        self.wait()

        # Clear for next section
        self.play(FadeOut(asym_title), FadeOut(chart_group))

        # Section 3: QMC-Driven Resonance Detection
        qmc_title = Text("QMC Resonance Detection", font_size=32, color=PURPLE).next_to(title_group, DOWN, buff=0.4)
        self.play(Write(qmc_title))

        # Sobol sequence visualization
        sobol_box = Rectangle(width=4, height=2.5, color=GREY).shift(LEFT * 2.8)
        sobol_label = Text("Sobol QMC Seeds", font_size=18, color=PURPLE).next_to(sobol_box, UP, buff=0.1)

        # Generate properly scaled quasi-random points
        np.random.seed(42)
        sobol_dots = VGroup()
        for i in range(30):
            x_offset = (i % 6 - 2.5) * 0.55
            y_offset = (i // 6 - 2) * 0.45
            dot = Dot(
                sobol_box.get_center() + np.array([x_offset, y_offset, 0]),
                color=TEAL,
                radius=0.05
            )
            sobol_dots.add(dot)

        # Resonance computation
        resonance_box = RoundedRectangle(
            width=4, height=3, corner_radius=0.2,
            color=ORANGE, fill_opacity=0.15
        ).shift(RIGHT * 2.8)

        resonance_label = Text("Resonance Amplitudes", font_size=18, color=ORANGE).next_to(resonance_box, UP, buff=0.1)

        # Mathematical formulas
        phi_formula = MathTex(r"\cos(\ln(p_0) \cdot \phi)", font_size=24, color=GOLD).move_to(resonance_box.get_center() + UP * 0.7)
        e_formula = MathTex(r"\cos(\ln(p_0) \cdot e)", font_size=24, color=BLUE_C).next_to(phi_formula, DOWN, buff=0.3)

        invariant = Text("Row 2 invariant:", font_size=14, color=GREY).next_to(e_formula, DOWN, buff=0.3)
        invariant_vals = VGroup(
            Text("k=0.2795", font_size=12),
            Text("A=1.808", font_size=12)
        ).arrange(RIGHT, buff=0.3).next_to(invariant, DOWN, buff=0.12)

        # Connection arrows
        arrow1 = Arrow(sobol_box.get_right(), resonance_box.get_left(), color=WHITE, buff=0.15)
        flow_label = Text("Phase\nalignment", font_size=14, color=WHITE).next_to(arrow1, UP, buff=0.1)

        qmc_group = VGroup(
            sobol_box, sobol_label, sobol_dots,
            resonance_box, resonance_label,
            phi_formula, e_formula,
            invariant, invariant_vals,
            arrow1, flow_label
        ).move_to(ORIGIN).shift(DOWN * 0.3)

        self.play(Create(sobol_box), Write(sobol_label))
        self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in sobol_dots], lag_ratio=0.05))
        self.play(Create(resonance_box), Write(resonance_label))
        self.play(Write(phi_formula), run_time=0.8)
        self.play(Write(e_formula), run_time=0.8)
        self.play(Write(invariant), Write(invariant_vals))
        self.play(GrowArrow(arrow1), Write(flow_label))
        self.wait()

        # Clear and show final synthesis
        self.play(FadeOut(qmc_title), FadeOut(qmc_group))

        # Final synthesis: Adaptive blind factorization
        final_title = Text("Adaptive Blind Factorization", font_size=32, color=RED).next_to(title_group, DOWN, buff=0.4)
        self.play(Write(final_title))

        # Window strategy
        base_rect = Rectangle(width=2, height=0.5, color=BLUE, fill_opacity=0.3)
        base_label = Text("Target", font_size=16).next_to(base_rect, UP, buff=0.1)

        window_13 = Rectangle(width=2.26, height=0.5, color=GREEN, fill_opacity=0.2).move_to(base_rect)
        label_13 = Text("13% window", font_size=14, color=GREEN).next_to(window_13, LEFT, buff=0.3)

        window_300 = Rectangle(width=6, height=0.5, color=ORANGE, fill_opacity=0.1).move_to(base_rect)
        label_300 = Text("300% window", font_size=14, color=ORANGE).next_to(window_300, RIGHT, buff=0.3)

        # Iterative refinement
        iteration_arrow = CurvedArrow(
            window_300.get_bottom() + DOWN * 0.5,
            window_13.get_bottom() + DOWN * 0.5,
            angle=-TAU/4,
            color=YELLOW
        )
        iter_text = Text("Iterative\nrefinement", font_size=14, color=YELLOW).next_to(iteration_arrow, DOWN, buff=0.2)

        window_group = VGroup(
            base_rect, base_label, window_13, label_13, window_300, label_300,
            iteration_arrow, iter_text
        ).move_to(ORIGIN).shift(UP * 0.2)

        self.play(Create(base_rect), Write(base_label))
        self.play(Create(window_13), Write(label_13))
        self.play(Create(window_300), Write(label_300))
        self.play(Create(iteration_arrow), Write(iter_text))
        self.wait()

        # Key insight
        insight = VGroup(
            Text("Emergent Property:", font_size=20, color=RED, weight=BOLD),
            Text("Scale-invariant patterns enable", font_size=16),
            Text("deterministic prime approximation", font_size=16),
            Text("at unprecedented magnitudes", font_size=16)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(insight, shift=UP))
        self.wait(2)

        # Final flourish
        self.play(
            insight.animate.set_color(GOLD),
            run_time=1.5
        )
        self.wait()

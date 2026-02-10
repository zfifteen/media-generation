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


class GoldenRatioPhaseWeightedCRISPR(Scene):
    """
    Visualizes the golden ratio phase-weighted spectral analysis
    for CRISPR mutation quantification.
    """

    def construct(self):
        # Constants
        PHI = (1 + np.sqrt(5)) / 2  # Golden ratio
        K_OPTIMAL = 0.3

        # ===== SECTION 1: Title =====
        title = Text("Golden Ratio Phase-Weighted", font_size=42, weight=BOLD)
        subtitle = Text("CRISPR Mutation Quantification", font_size=36, color=GOLD)
        subtitle.next_to(title, DOWN, buff=0.3)
        title_group = VGroup(title, subtitle).move_to(ORIGIN)

        self.play(Write(title_group))
        self.wait(1)
        self.play(title_group.animate.scale(0.55).to_edge(UP, buff=0.3))

        # ===== SECTION 2: Phase Function Definition =====
        phase_label = Text("Phase Function", font_size=28, color=YELLOW)
        phase_label.next_to(title_group, DOWN, buff=0.4).align_to(LEFT * 6, LEFT)

        phase_formula = MathTex(
            r"\theta'(n, k) = \phi^k \cdot f(n)",
            font_size=36
        )
        phase_formula.next_to(phase_label, DOWN, buff=0.2).align_to(phase_label, LEFT)

        phi_def = MathTex(
            r"\phi = \frac{1 + \sqrt{5}}{2} \approx 1.618",
            font_size=28,
            color=GOLD
        )
        phi_def.next_to(phase_formula, DOWN, buff=0.15).align_to(phase_label, LEFT)

        k_optimal = MathTex(
            r"k^* \approx 0.300",
            font_size=28,
            color=GREEN
        )
        k_optimal.next_to(phi_def, DOWN, buff=0.15).align_to(phase_label, LEFT)

        phase_group = VGroup(phase_label, phase_formula, phi_def, k_optimal)

        self.play(Write(phase_label))
        self.play(Write(phase_formula))
        self.play(FadeIn(phi_def), FadeIn(k_optimal))
        self.wait(1)

        # ===== SECTION 3: Geodesic Mapping =====
        geodesic_label = Text("Geodesic-Topological Bridge", font_size=28, color=YELLOW)
        geodesic_label.next_to(k_optimal, DOWN, buff=0.5).align_to(phase_label, LEFT)

        geodesic_formula = MathTex(
            r"f(x) = \arcsin\left(\frac{x - 1}{2x + 3}\right)",
            font_size=32
        )
        geodesic_formula.next_to(geodesic_label, DOWN, buff=0.2).align_to(phase_label, LEFT)

        self.play(Write(geodesic_label))
        self.play(Write(geodesic_formula))
        self.wait(1)

        # ===== SECTION 4: Visualization Axes (right side) =====
        axes = Axes(
            x_range=[0, 20, 5],
            y_range=[-0.5, 1.5, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": True, "font_size": 18},
            tips=False
        )
        axes.move_to(RIGHT * 3.5 + DOWN * 0.5)

        axes_labels = axes.get_axis_labels(
            x_label=Text("n (position)", font_size=16),
            y_label=Text("θ'(n,k)", font_size=16)
        )

        # Phase function curves for different k values
        def phase_func(n, k):
            if n <= 0:
                return 0
            x = n
            inner = (x - 1) / (2 * x + 3)
            inner = np.clip(inner, -1, 1)
            return (PHI ** k) * np.arcsin(inner)

        curve_k01 = axes.plot(
            lambda n: phase_func(n, 0.1),
            x_range=[0.1, 20],
            color=BLUE
        )
        curve_k03 = axes.plot(
            lambda n: phase_func(n, 0.3),
            x_range=[0.1, 20],
            color=GREEN,
            stroke_width=4
        )
        curve_k05 = axes.plot(
            lambda n: phase_func(n, 0.5),
            x_range=[0.1, 20],
            color=RED
        )

        legend_items = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=BLUE), Text("k=0.1", font_size=14)).arrange(RIGHT, buff=0.1),
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=GREEN, stroke_width=4), Text("k=0.3 (optimal)", font_size=14, color=GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=RED), Text("k=0.5", font_size=14)).arrange(RIGHT, buff=0.1)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend_items.next_to(axes, DOWN, buff=0.3)

        self.play(Create(axes), Write(axes_labels))
        self.play(Create(curve_k01), Create(curve_k05))
        self.play(Create(curve_k03), run_time=1.5)
        self.play(FadeIn(legend_items))
        self.wait(1.5)

        # ===== SECTION 5: Performance Metrics =====
        # Clear axes area for metrics
        self.play(
            FadeOut(axes), FadeOut(axes_labels),
            FadeOut(curve_k01), FadeOut(curve_k03), FadeOut(curve_k05),
            FadeOut(legend_items)
        )

        perf_label = Text("Performance vs RuleSet3", font_size=28, color=YELLOW)
        perf_label.move_to(RIGHT * 3.5 + UP * 2)

        # ROC-AUC comparison bars
        bar_ruleset3 = Rectangle(width=1.2, height=2.5, fill_opacity=0.7, color=BLUE)
        bar_phase = Rectangle(width=1.2, height=2.97, fill_opacity=0.7, color=GREEN)

        bar_ruleset3.move_to(RIGHT * 2.5 + DOWN * 0.5)
        bar_phase.move_to(RIGHT * 4.5 + DOWN * 0.5)

        bar_ruleset3.align_to(DOWN * 2, DOWN)
        bar_phase.align_to(DOWN * 2, DOWN)

        label_r3 = Text("RuleSet3", font_size=16)
        label_phase = Text("Phase-\nWeighted", font_size=16, color=GREEN)
        label_r3.next_to(bar_ruleset3, DOWN, buff=0.15)
        label_phase.next_to(bar_phase, DOWN, buff=0.15)

        delta_label = MathTex(
            r"\Delta\text{ROC-AUC} = +0.047",
            font_size=24,
            color=GREEN
        )
        delta_label.next_to(bar_phase, UP, buff=0.2)

        ci_label = Text("± 0.006 (bootstrap n=10,000)", font_size=14, color=GRAY)
        ci_label.next_to(delta_label, DOWN, buff=0.1)

        self.play(Write(perf_label))
        self.play(
            GrowFromEdge(bar_ruleset3, DOWN),
            GrowFromEdge(bar_phase, DOWN)
        )
        self.play(Write(label_r3), Write(label_phase))
        self.play(Write(delta_label), FadeIn(ci_label))
        self.wait(1.5)

        # ===== SECTION 6: GC Resonance Correlation =====
        gc_label = Text("GC-Quartile Resonance", font_size=22, color=TEAL)
        gc_label.next_to(ci_label, DOWN, buff=0.5)

        gc_stats = MathTex(
            r"r = -0.211 \quad (p = 0.0012)",
            font_size=22
        )
        gc_stats.next_to(gc_label, DOWN, buff=0.15)

        gc_note = Text("Kim 2025 (N=18,102)", font_size=14, color=GRAY)
        gc_note.next_to(gc_stats, DOWN, buff=0.1)

        self.play(Write(gc_label))
        self.play(Write(gc_stats), FadeIn(gc_note))
        self.wait(2)

        # ===== SECTION 7: Final Summary Visual =====
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

        # DNA helix representation with mutation markers
        dna_title = Text("Z-Invariant Disruption Scoring", font_size=36, weight=BOLD)
        dna_title.to_edge(UP, buff=0.5)

        # Create simplified DNA backbone
        backbone1 = VMobject()
        backbone2 = VMobject()

        points1 = []
        points2 = []
        for i in range(50):
            t = i * 0.15
            x = t - 3.5
            y1 = 0.4 * np.sin(t * 2)
            y2 = -0.4 * np.sin(t * 2)
            points1.append([x, y1, 0])
            points2.append([x, y2, 0])

        backbone1.set_points_smoothly([np.array(p) for p in points1])
        backbone2.set_points_smoothly([np.array(p) for p in points2])
        backbone1.set_color(BLUE_C)
        backbone2.set_color(BLUE_C)

        dna_group = VGroup(backbone1, backbone2)
        dna_group.move_to(ORIGIN)

        # Mutation markers
        mut1 = Dot(color=RED, radius=0.15).move_to(LEFT * 1.5)
        mut2 = Dot(color=RED, radius=0.15).move_to(RIGHT * 0.5)
        mut3 = Dot(color=RED, radius=0.15).move_to(RIGHT * 2)

        mut_label = Text("Multi-mutation effects", font_size=18, color=RED)
        mut_label.next_to(dna_group, DOWN, buff=0.5)

        disruption_arrow = Arrow(
            start=DOWN * 1.5 + LEFT * 2,
            end=DOWN * 1.5 + RIGHT * 2,
            color=GOLD,
            buff=0
        )
        disruption_arrow.next_to(mut_label, DOWN, buff=0.3)

        disruption_label = Text("Disruption Score (p < 0.05)", font_size=18)
        disruption_label.next_to(disruption_arrow, DOWN, buff=0.15)

        self.play(Write(dna_title))
        self.play(Create(dna_group))
        self.play(
            FadeIn(mut1, scale=2),
            FadeIn(mut2, scale=2),
            FadeIn(mut3, scale=2)
        )
        self.play(Write(mut_label))
        self.play(GrowArrow(disruption_arrow), Write(disruption_label))

        # Pulsing effect on mutations to show phase weighting
        self.play(
            mut1.animate.scale(1.5),
            mut2.animate.scale(1.5),
            mut3.animate.scale(1.5),
            rate_func=there_and_back,
            run_time=1
        )
        self.wait(2)


class PhaseWeightedComparison(Scene):
    """
    Focused comparison scene: Single vs Multi-mutation scoring
    """

    def construct(self):
        PHI = (1 + np.sqrt(5)) / 2

        title = Text("Phase-Weighted Disruption Scoring", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Left: Single mutation
        single_box = VGroup(
            Rectangle(width=5, height=3, color=BLUE, fill_opacity=0.1),
            Text("Single Mutation", font_size=24, color=BLUE).shift(UP * 1),
            MathTex(r"D_1 = \phi^k \cdot \theta_1", font_size=28).shift(DOWN * 0.2),
            Text("Lower Disruption", font_size=18, color=GRAY).shift(DOWN * 1)
        )
        single_box.move_to(LEFT * 4)

        # Right: Multi mutation
        multi_box = VGroup(
            Rectangle(width=5, height=3, color=GREEN, fill_opacity=0.1),
            Text("Multiple Mutations", font_size=24, color=GREEN).shift(UP * 1),
            MathTex(r"D_n = \phi^k \sum_{i} \theta_i", font_size=28).shift(DOWN * 0.2),
            Text("Higher Disruption (p < 0.05)", font_size=18, color=GREEN).shift(DOWN * 1)
        )
        multi_box.move_to(RIGHT * 4)

        # Arrow showing relationship
        comparison_arrow = Arrow(LEFT * 1.2, RIGHT * 1.2, color=GOLD, buff=0)
        comparison_label = MathTex(r"\phi^{0.3} \approx 1.15", font_size=24, color=GOLD)
        comparison_label.next_to(comparison_arrow, UP, buff=0.15)

        self.play(FadeIn(single_box))
        self.play(FadeIn(multi_box))
        self.play(GrowArrow(comparison_arrow), Write(comparison_label))

        # Z-invariant note
        z_note = Text("Z-invariant scoring enables robust multi-mutation quantification",
                      font_size=20, color=YELLOW)
        z_note.to_edge(DOWN, buff=0.6)
        self.play(Write(z_note))
        self.wait(2)

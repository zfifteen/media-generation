from manim import *
import numpy as np
from scipy.integrate import solve_ivp

# ============================================================================
# OPTIMIZED CONFIGURATION - DO NOT MODIFY THESE VALUES
# ============================================================================
config.frame_height = 10
config.frame_width = 10 * 16/9
config.pixel_height = 1440
config.pixel_width = 2560
# ============================================================================


class CoxGeomageticModel(Scene):
    """
    Single continuous scene covering Cox's 1968 probabilistic model
    for geomagnetic polarity intervals. Targets 10+ minutes runtime.

    Render: manim cox_geomagnetic_model.py CoxGeomageticModel
    """

    def construct(self):
        self.section_title_card()
        self.section_physical_setup()
        self.section_dipole_oscillation()
        self.section_nondipole_field()
        self.section_triggering_mechanism()
        self.section_bernoulli_trials()
        self.section_geometric_distribution()
        self.section_rikitake_equations()
        self.section_rikitake_timeseries()
        self.section_rikitake_phase_portrait()
        self.section_paleomagnetic_evidence()
        self.section_model_summary()
        self.section_closing()

    # ------------------------------------------------------------------
    # Helper: fade everything out
    # ------------------------------------------------------------------
    def clear_screen(self, run_time=1.0):
        if self.mobjects:
            self.play(FadeOut(Group(*self.mobjects)), run_time=run_time)
        self.wait(0.3)

    # ------------------------------------------------------------------
    # Helper: section header transition
    # ------------------------------------------------------------------
    def show_section_header(self, text, color=BLUE, wait=2.0):
        header = Text(text, font_size=42, weight=BOLD, color=color)
        underline = Line(LEFT * 4, RIGHT * 4, color=color, stroke_width=2)
        underline.next_to(header, DOWN, buff=0.15)
        grp = VGroup(header, underline).move_to(ORIGIN)
        self.play(FadeIn(grp, shift=UP * 0.3), run_time=1.0)
        self.wait(wait)
        self.play(FadeOut(grp), run_time=0.8)
        self.wait(0.3)

    # ==================================================================
    # SECTION 1: Title Card  (~50s)
    # ==================================================================
    def section_title_card(self):
        self.next_section("TitleCard")

        title = Text("Cox's Probabilistic Model", font_size=48, weight=BOLD)
        subtitle = Text(
            "for Geomagnetic Polarity Intervals",
            font_size=34, color=BLUE,
        )
        subtitle.next_to(title, DOWN, buff=0.3)
        year = Text("Allan Cox, 1968", font_size=26, color=GREY_B)
        year.next_to(subtitle, DOWN, buff=0.4)
        header = VGroup(title, subtitle, year).move_to(UP * 1.0)

        self.play(Write(title), run_time=2.0)
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(year, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)

        # Core equation
        eq = MathTex(
            r"P(K = k) = (1 - p)^{k-1}\, p",
            font_size=42, color=GOLD,
        ).next_to(header, DOWN, buff=0.8)
        eq_box = SurroundingRectangle(eq, color=GOLD, buff=0.2, corner_radius=0.1)
        self.play(Write(eq), run_time=1.5)
        self.play(Create(eq_box), run_time=0.8)
        self.wait(2.0)

        # Key idea bullets
        bullets_data = [
            "Polarity reversals are stochastic, not deterministic",
            "Driven by dipole oscillations + random nondipole noise",
            "Interval lengths follow a geometric distribution",
        ]
        bullets = VGroup()
        for txt in bullets_data:
            bullet = Text(txt, font_size=20, color=WHITE)
            bullets.add(bullet)
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        bullets.next_to(eq_box, DOWN, buff=0.7)

        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT * 0.3), run_time=0.7)
            self.wait(0.8)

        # Citation
        cite = Text(
            "Cox, A. (1968) J. Geophys. Res., 73(10), 3247\u20133260",
            font_size=16, color=GREY_C,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cite), run_time=0.5)
        self.wait(3.0)
        self.clear_screen()

    # ==================================================================
    # SECTION 2: Physical Setup  (~55s)
    # ==================================================================
    def section_physical_setup(self):
        self.next_section("PhysicalSetup")
        self.show_section_header("Physical Setup: Earth's Magnetic Field")

        # Earth + field lines schematic
        earth = Circle(radius=1.2, color=BLUE_D, fill_opacity=0.3, stroke_width=2)
        earth_label = Text("Earth", font_size=18, color=BLUE_D).move_to(earth)
        core = Circle(radius=0.5, color=ORANGE, fill_opacity=0.5, stroke_width=1)
        core_label = Text("Core", font_size=14, color=WHITE).move_to(core)

        earth_grp = VGroup(earth, core, earth_label, core_label).move_to(LEFT * 4)

        # Dipole field lines (simplified arcs)
        field_lines = VGroup()
        for angle in [-40, -20, 0, 20, 40]:
            arc = Arc(
                radius=2.0, start_angle=(90 + angle) * DEGREES,
                angle=(-180 - 2 * angle) * DEGREES,
                color=RED_B, stroke_width=1.5, stroke_opacity=0.6,
            )
            arc.move_to(earth.get_center())
            field_lines.add(arc)

        # Text descriptions on the right
        desc_title = Text("Two Field Components", font_size=28, weight=BOLD)
        desc_title.move_to(RIGHT * 3 + UP * 2.5)

        dipole_box = VGroup(
            Text("Dipole Field (axial)", font_size=22, color=RED_B, weight=BOLD),
            Text("Quasi-periodic oscillation", font_size=18, color=GREY_B),
            Text("Dominant component (~80%)", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(RIGHT * 3.5 + UP * 1.0)

        nondipole_box = VGroup(
            Text("Nondipole Field", font_size=22, color=GREEN, weight=BOLD),
            Text("Random, independent variations", font_size=18, color=GREY_B),
            Text("Quadrupole, octupole terms (~20%)", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(RIGHT * 3.5 + DOWN * 1.0)

        self.play(Create(earth), FadeIn(earth_label), run_time=1.0)
        self.play(Create(core), FadeIn(core_label), run_time=0.8)
        self.wait(0.5)
        self.play(Create(field_lines), run_time=2.0)
        self.wait(1.0)
        self.play(Write(desc_title), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(dipole_box, shift=RIGHT * 0.2), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(nondipole_box, shift=RIGHT * 0.2), run_time=1.0)
        self.wait(1.5)

        # Key insight
        insight = Text(
            "Reversals occur when the dipole weakens enough\n"
            "for nondipole perturbations to flip the polarity",
            font_size=20, color=YELLOW,
        ).move_to(DOWN * 3.2)
        self.play(FadeIn(insight, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.clear_screen()

    # ==================================================================
    # SECTION 3: Dipole Oscillation  (~70s)
    # ==================================================================
    def section_dipole_oscillation(self):
        self.next_section("DipoleOscillation")
        self.show_section_header("Dipole Intensity Oscillation")

        title = Text("Quasi-Periodic Dipole Cycles", font_size=32, weight=BOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=1.0)

        ax = Axes(
            x_range=[0, 6 * np.pi, np.pi],
            y_range=[-0.1, 1.3, 0.5],
            x_length=13,
            y_length=5.5,
            axis_config={"include_tip": True, "tip_length": 0.2},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).move_to(DOWN * 0.3)

        x_label = ax.get_x_axis_label(
            Text("Time", font_size=18), edge=RIGHT, direction=DOWN, buff=0.3
        )
        y_label = ax.get_y_axis_label(
            MathTex(r"B_d \text{ (dipole intensity)}", font_size=20),
            edge=UP, direction=LEFT, buff=0.3,
        )

        self.play(Create(ax), Write(x_label), Write(y_label), run_time=1.5)

        # Dipole curve, drawn progressively
        dipole_func = lambda x: 0.5 + 0.45 * np.cos(x)
        dipole_curve = ax.plot(dipole_func, x_range=[0, 6 * np.pi], color=BLUE)
        self.play(Create(dipole_curve), run_time=3.0)
        self.wait(1.0)

        # Label max and min
        max_dot = Dot(ax.c2p(0, dipole_func(0)), color=BLUE, radius=0.08)
        max_label = Text("Maximum", font_size=14, color=BLUE).next_to(max_dot, UR, buff=0.1)
        min_dot = Dot(ax.c2p(np.pi, dipole_func(np.pi)), color=RED, radius=0.08)
        min_label = Text("Minimum", font_size=14, color=RED).next_to(min_dot, DR, buff=0.1)
        self.play(FadeIn(max_dot), Write(max_label), run_time=0.6)
        self.play(FadeIn(min_dot), Write(min_label), run_time=0.6)
        self.wait(1.0)

        # Period brace
        tau_brace = BraceBetweenPoints(
            ax.c2p(0, -0.05), ax.c2p(2 * np.pi, -0.05),
            direction=DOWN, buff=0.05,
        )
        tau_text = MathTex(r"\tau \sim 10^3\text{--}10^4 \text{ yr}", font_size=22, color=WHITE)
        tau_text.next_to(tau_brace, DOWN, buff=0.15)
        self.play(Create(tau_brace), Write(tau_text), run_time=1.0)
        self.wait(1.5)

        # Vulnerability windows
        vuln_rects = VGroup()
        for i in range(3):
            cx = (2 * i + 1) * np.pi
            half_w = 0.8
            x1 = ax.c2p(cx - half_w, -0.1)
            x2 = ax.c2p(cx + half_w, 1.3)
            rect = Rectangle(
                width=abs(x2[0] - x1[0]),
                height=abs(x2[1] - x1[1]),
                fill_color=YELLOW,
                fill_opacity=0.12,
                stroke_width=0,
            ).move_to((np.array(x1) + np.array(x2)) / 2)
            vuln_rects.add(rect)

        vuln_label = Text(
            "Windows of vulnerability", font_size=18, color=YELLOW,
        ).next_to(vuln_rects[1], UP, buff=0.1)

        self.play(FadeIn(vuln_rects), run_time=1.0)
        self.play(Write(vuln_label), run_time=0.8)
        self.wait(1.0)

        # Threshold line
        threshold = 0.12
        thresh_line = ax.plot(
            lambda x: threshold, x_range=[0, 6 * np.pi],
            color=RED, stroke_width=2,
        )
        thresh_label = Text(
            "Critical threshold for reversal", font_size=16, color=RED,
        ).next_to(ax.c2p(6 * np.pi, threshold), RIGHT, buff=0.2)
        self.play(Create(thresh_line), Write(thresh_label), run_time=1.0)
        self.wait(1.0)

        note = Text(
            "Each minimum creates one opportunity for reversal",
            font_size=20, color=GREY_B,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(4.0)
        self.clear_screen()

    # ==================================================================
    # SECTION 4: Nondipole Field  (~60s)
    # ==================================================================
    def section_nondipole_field(self):
        self.next_section("NondipoleField")
        self.show_section_header("Nondipole Field Variations")

        title = Text("Random Nondipole Perturbations", font_size=32, weight=BOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=1.0)

        ax = Axes(
            x_range=[0, 6 * np.pi, np.pi],
            y_range=[-0.1, 1.3, 0.5],
            x_length=13,
            y_length=5.5,
            axis_config={"include_tip": True, "tip_length": 0.2},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).move_to(DOWN * 0.3)

        x_label = ax.get_x_axis_label(
            Text("Time", font_size=18), edge=RIGHT, direction=DOWN, buff=0.3,
        )
        y_label = ax.get_y_axis_label(
            Text("Field strength", font_size=18), edge=UP, direction=LEFT, buff=0.3,
        )
        self.play(Create(ax), Write(x_label), Write(y_label), run_time=1.0)

        # Dipole (faded)
        dipole_func = lambda x: 0.5 + 0.45 * np.cos(x)
        dipole_curve = ax.plot(
            dipole_func, x_range=[0, 6 * np.pi],
            color=BLUE, stroke_opacity=0.5,
        )
        dip_label = MathTex(r"B_d", font_size=22, color=BLUE)
        dip_label.next_to(ax.c2p(0.5, 0.9), UP, buff=0.1)
        self.play(Create(dipole_curve), Write(dip_label), run_time=1.5)
        self.wait(0.5)

        # Nondipole random curve
        np.random.seed(42)
        xs = np.linspace(0, 6 * np.pi, 600)
        raw = np.random.randn(600)
        from scipy.ndimage import gaussian_filter1d
        nd_vals = gaussian_filter1d(raw, sigma=15) * 0.08 + 0.15
        nd_vals = np.clip(nd_vals, 0.03, 0.4)

        nd_points = [ax.c2p(x, y) for x, y in zip(xs, nd_vals)]
        nd_curve = VMobject(color=GREEN, stroke_width=2)
        nd_curve.set_points_smoothly(nd_points)
        nd_label = MathTex(r"B_{nd}", font_size=22, color=GREEN)
        nd_label.next_to(ax.c2p(1.0, 0.25), UP, buff=0.1)
        self.play(Create(nd_curve), Write(nd_label), run_time=2.5)
        self.wait(1.0)

        # Highlight: nondipole stays roughly constant
        brace_nd = Brace(
            VGroup(
                Dot(ax.c2p(0, 0.10), radius=0.01),
                Dot(ax.c2p(0, 0.25), radius=0.01),
            ),
            direction=LEFT, buff=0.15,
        )
        brace_nd.next_to(ax.c2p(0, 0.17), LEFT, buff=0.2)
        brace_text = Text("~10-20% of dipole", font_size=16, color=GREEN)
        brace_text.next_to(brace_nd, LEFT, buff=0.15)
        self.play(Create(brace_nd), Write(brace_text), run_time=1.0)
        self.wait(1.5)

        # Observation note
        obs = VGroup(
            Text("Key observation (Leaton & Malin, 1967):", font_size=18, weight=BOLD, color=YELLOW),
            Text("Nondipole field remains stable while dipole declines", font_size=18, color=WHITE),
            Text("This decoupling enables reversal triggering", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.5)

        for line in obs:
            self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.7)
            self.wait(0.6)

        self.wait(4.0)
        self.clear_screen()

    # ==================================================================
    # SECTION 5: Triggering Mechanism  (~55s)
    # ==================================================================
    def section_triggering_mechanism(self):
        self.next_section("TriggeringMechanism")
        self.show_section_header("Reversal Triggering Mechanism")

        # Ratio definition
        ratio_eq = MathTex(
            r"r = \frac{B_{nd}}{B_d}",
            font_size=44, color=YELLOW,
        ).move_to(UP * 2.5)
        self.play(Write(ratio_eq), run_time=1.5)
        self.wait(1.0)

        condition = MathTex(
            r"\text{Reversal if } r > r_c",
            font_size=36, color=RED,
        ).next_to(ratio_eq, DOWN, buff=0.5)
        self.play(Write(condition), run_time=1.0)
        self.wait(1.5)

        # Visual: bar chart of Bd vs Bnd at different times
        scenarios = [
            ("Normal", 0.8, 0.12, "No reversal", GREEN),
            ("Dipole weakening", 0.4, 0.14, "Marginal", YELLOW),
            ("Dipole minimum", 0.1, 0.15, "REVERSAL", RED),
        ]

        bar_group = VGroup()
        for i, (label, bd, bnd, result, color) in enumerate(scenarios):
            x_offset = (i - 1) * 5
            # Bd bar
            bd_bar = Rectangle(
                width=1.0, height=bd * 4,
                fill_color=BLUE, fill_opacity=0.6, stroke_color=BLUE,
            )
            bd_bar.move_to(RIGHT * (x_offset - 0.7) + DOWN * 1.5)
            bd_bar.align_to(DOWN * 3.5, DOWN)
            bd_text = MathTex(r"B_d", font_size=16, color=BLUE).next_to(bd_bar, DOWN, buff=0.1)

            # Bnd bar
            bnd_bar = Rectangle(
                width=1.0, height=bnd * 4,
                fill_color=GREEN, fill_opacity=0.6, stroke_color=GREEN,
            )
            bnd_bar.move_to(RIGHT * (x_offset + 0.7) + DOWN * 1.5)
            bnd_bar.align_to(DOWN * 3.5, DOWN)
            bnd_text = MathTex(r"B_{nd}", font_size=16, color=GREEN).next_to(bnd_bar, DOWN, buff=0.1)

            # Labels
            sc_label = Text(label, font_size=18, weight=BOLD).move_to(
                RIGHT * x_offset + DOWN * 0.3,
            )
            r_val = bnd / bd
            r_text = MathTex(
                rf"r = {r_val:.2f}", font_size=18,
            ).next_to(sc_label, DOWN, buff=0.15)
            result_text = Text(result, font_size=16, color=color, weight=BOLD)
            result_text.next_to(bnd_bar, UP, buff=0.8).shift(LEFT * 0.7)

            scenario_grp = VGroup(bd_bar, bd_text, bnd_bar, bnd_text, sc_label, r_text, result_text)
            bar_group.add(scenario_grp)

        for sg in bar_group:
            self.play(FadeIn(sg), run_time=1.2)
            self.wait(1.5)

        rc_note = MathTex(
            r"r_c \approx 1.0 \text{ (critical ratio)}", font_size=22, color=RED,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(rc_note), run_time=0.8)
        self.wait(4.0)
        self.clear_screen()

    # ==================================================================
    # SECTION 6: Bernoulli Trials  (~70s)
    # ==================================================================
    def section_bernoulli_trials(self):
        self.next_section("BernoulliTrials")
        self.show_section_header("Probabilistic Framework: Bernoulli Trials")

        title = Text("Each Dipole Minimum = One Trial", font_size=32, weight=BOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=1.0)

        explanation = VGroup(
            Text("Fixed probability p of reversal per cycle", font_size=22, color=GREY_B),
            Text("Trials are independent", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.15).next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(explanation), run_time=0.8)
        self.wait(1.0)

        # Animated trial sequence
        n_trials = 12
        results = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]
        spacing = 1.2
        start_x = -0.5 * (n_trials - 1) * spacing

        trial_circles = VGroup()
        trial_labels = VGroup()
        for i in range(n_trials):
            x_pos = start_x + i * spacing
            circle = Circle(radius=0.38, color=WHITE, stroke_width=2)
            circle.move_to(RIGHT * x_pos + DOWN * 0.5)
            label = MathTex(str(i + 1), font_size=16).move_to(circle.get_center())
            trial_circles.add(circle)
            trial_labels.add(label)

        cycle_label = Text(
            "Dipole oscillation cycle number", font_size=18, color=GREY_C,
        ).next_to(trial_circles, UP, buff=0.3)

        self.play(FadeIn(cycle_label), run_time=0.5)

        # Appear one by one
        for i in range(n_trials):
            self.play(
                FadeIn(trial_circles[i]),
                FadeIn(trial_labels[i]),
                run_time=0.25,
            )

        self.wait(1.0)

        # Animate results
        result_marks = VGroup()
        for i in range(n_trials):
            circle = trial_circles[i]
            if results[i] == 1:
                circle.generate_target()
                circle.target.set_fill(RED, opacity=0.6)
                circle.target.set_stroke(RED)
                mark = MathTex(r"\checkmark", font_size=22, color=WHITE)
                mark.next_to(circle, DOWN, buff=0.15)
                rev_label = Text("Reversal!", font_size=13, color=RED)
                rev_label.next_to(mark, DOWN, buff=0.08)
                result_marks.add(VGroup(mark, rev_label))
                self.play(
                    MoveToTarget(circle),
                    FadeIn(mark), FadeIn(rev_label),
                    run_time=0.6,
                )
                self.wait(0.8)
            else:
                circle.generate_target()
                circle.target.set_fill(BLUE, opacity=0.2)
                circle.target.set_stroke(BLUE_D)
                x_mark = MathTex(r"\times", font_size=22, color=GREY_C)
                x_mark.next_to(circle, DOWN, buff=0.15)
                result_marks.add(x_mark)
                self.play(MoveToTarget(circle), FadeIn(x_mark), run_time=0.2)

        self.wait(1.5)

        # Interval annotation
        brace1 = BraceBetweenPoints(
            trial_circles[0].get_bottom() + DOWN * 0.8,
            trial_circles[4].get_bottom() + DOWN * 0.8,
            direction=DOWN, buff=0.05,
        )
        int1_text = MathTex(r"K_1 = 5", font_size=20, color=GOLD)
        int1_text.next_to(brace1, DOWN, buff=0.1)

        brace2 = BraceBetweenPoints(
            trial_circles[5].get_bottom() + DOWN * 0.8,
            trial_circles[11].get_bottom() + DOWN * 0.8,
            direction=DOWN, buff=0.05,
        )
        int2_text = MathTex(r"K_2 = 7", font_size=20, color=GOLD)
        int2_text.next_to(brace2, DOWN, buff=0.1)

        self.play(Create(brace1), Write(int1_text), run_time=0.8)
        self.wait(0.5)
        self.play(Create(brace2), Write(int2_text), run_time=0.8)
        self.wait(1.0)

        interval_eq = MathTex(
            r"T_i = K_i \cdot \tau", font_size=28, color=GOLD,
        ).move_to(DOWN * 3.8)
        self.play(Write(interval_eq), run_time=0.8)

        prob_text = MathTex(
            r"p \approx 0.1\text{--}0.3 \text{ per cycle (Cenozoic)}",
            font_size=22, color=YELLOW,
        ).next_to(interval_eq, DOWN, buff=0.2)
        self.play(Write(prob_text), run_time=0.8)
        self.wait(5.0)
        self.clear_screen()

    # ==================================================================
    # SECTION 7: Geometric Distribution  (~80s)
    # ==================================================================
    def section_geometric_distribution(self):
        self.next_section("GeometricDistribution")
        self.show_section_header("Geometric Distribution of Intervals")

        # Derivation
        deriv_title = Text("Mathematical Formulation", font_size=30, weight=BOLD)
        deriv_title.move_to(UP * 3.8)
        self.play(Write(deriv_title), run_time=0.8)

        steps = [
            (r"\text{Each cycle: reversal with prob } p, \text{ no reversal with } 1-p", WHITE),
            (r"\text{Cycles are independent (Bernoulli trials)}", WHITE),
            (r"P(\text{first reversal at cycle } k) = \underbrace{(1-p)(1-p)\cdots(1-p)}_{k-1} \cdot\, p", YELLOW),
            (r"P(K = k) = (1 - p)^{k-1}\, p, \quad k = 1, 2, 3, \dots", GOLD),
        ]

        step_mobjects = VGroup()
        for tex, color in steps:
            m = MathTex(tex, font_size=26, color=color)
            step_mobjects.add(m)
        step_mobjects.arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(deriv_title, DOWN, buff=0.5)

        for sm in step_mobjects:
            self.play(Write(sm), run_time=1.2)
            self.wait(1.0)

        self.wait(2.0)

        # Expected value
        ev = MathTex(
            r"\mathbb{E}[K] = \frac{1}{p}", font_size=32, color=GREEN,
        ).next_to(step_mobjects, DOWN, buff=0.5)
        ev_note = MathTex(
            r"\text{Var}(K) = \frac{1-p}{p^2}", font_size=24, color=GREY_B,
        ).next_to(ev, RIGHT, buff=0.8)
        self.play(Write(ev), run_time=0.8)
        self.play(Write(ev_note), run_time=0.8)
        self.wait(3.0)
        self.clear_screen()

        # Bar chart for multiple p values
        chart_title = Text("Distribution Shape for Different p", font_size=32, weight=BOLD)
        chart_title.move_to(UP * 3.8)
        self.play(Write(chart_title), run_time=0.8)

        ax = Axes(
            x_range=[0, 21, 1],
            y_range=[0, 0.42, 0.1],
            x_length=12,
            y_length=5.0,
            axis_config={"include_tip": False},
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": list(range(1, 21, 2)),
                "font_size": 14,
            },
            y_axis_config={
                "include_numbers": True,
                "font_size": 14,
                "numbers_to_include": [0, 0.1, 0.2, 0.3, 0.4],
            },
        ).move_to(DOWN * 0.8)

        x_lab = ax.get_x_axis_label(
            MathTex(r"k \text{ (cycles until reversal)}", font_size=20),
            edge=RIGHT, direction=DOWN, buff=0.2,
        )
        y_lab = ax.get_y_axis_label(
            MathTex(r"P(K=k)", font_size=20),
            edge=UP, direction=LEFT, buff=0.2,
        )
        self.play(Create(ax), Write(x_lab), Write(y_lab), run_time=1.0)

        p_values = [(0.1, BLUE, "p=0.1"), (0.2, GREEN, "p=0.2"), (0.4, RED, "p=0.4")]
        k_vals = np.arange(1, 21)

        legend_items = VGroup()
        for p_val, color, label_str in p_values:
            probs = (1 - p_val) ** (k_vals - 1) * p_val
            dots = VGroup()
            for k, prob in zip(k_vals, probs):
                dot = Dot(ax.c2p(k, prob), color=color, radius=0.06)
                dots.add(dot)
            line_segs = VGroup()
            for i_k in range(len(k_vals) - 1):
                seg = Line(
                    ax.c2p(k_vals[i_k], probs[i_k]),
                    ax.c2p(k_vals[i_k + 1], probs[i_k + 1]),
                    color=color, stroke_width=2,
                )
                line_segs.add(seg)

            self.play(Create(line_segs), FadeIn(dots), run_time=1.5)
            self.wait(0.5)

            legend_dot = Dot(color=color, radius=0.06)
            legend_label = Text(label_str, font_size=16, color=color)
            legend_entry = VGroup(legend_dot, legend_label).arrange(RIGHT, buff=0.1)
            legend_items.add(legend_entry)

        legend_items.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(ax.c2p(18, 0.35))
        self.play(FadeIn(legend_items), run_time=0.5)

        note = Text(
            "Higher p = more frequent reversals, shorter intervals",
            font_size=20, color=GREY_B,
        ).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(5.0)
        self.clear_screen()

    # ==================================================================
    # SECTION 8: Rikitake Equations  (~50s)
    # ==================================================================
    def section_rikitake_equations(self):
        self.next_section("RikitakeEquations")
        self.show_section_header("Dynamo Analog: Rikitake Two-Disk Model")

        # Concept
        desc = VGroup(
            Text("Simplified self-excited dynamo modeling core convection", font_size=22, color=GREY_B),
            Text("Two coupled rotating disks with feedback currents", font_size=22, color=GREY_B),
            Text("Produces chaotic reversals from deterministic equations", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.2).move_to(UP * 2.5)
        for line in desc:
            self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.7)
            self.wait(0.5)
        self.wait(1.0)

        # Equations with color coding
        eq1 = MathTex(r"\frac{dX}{dt}", r"=", r"-\mu X", r"+", r"Y Z", font_size=36)
        eq2 = MathTex(r"\frac{dY}{dt}", r"=", r"-\mu Y", r"+", r"(Z - A) X", font_size=36)
        eq3 = MathTex(r"\frac{dZ}{dt}", r"=", r"1", r"-", r"X Y", font_size=36)

        eq1[0].set_color(BLUE)
        eq1[2].set_color(RED_B)
        eq2[0].set_color(GREEN)
        eq2[2].set_color(RED_B)
        eq3[0].set_color(ORANGE)

        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.4).move_to(DOWN * 0.5)

        for eq in eqs:
            self.play(Write(eq), run_time=1.5)
            self.wait(0.5)

        self.wait(1.0)

        # Parameter meanings
        params = VGroup(
            MathTex(r"X, Y", r"\text{ : toroidal currents (disk loops)}", font_size=20),
            MathTex(r"Z", r"\text{ : poloidal / angular velocity}", font_size=20),
            MathTex(r"\mu", r"\text{ : ohmic decay rate}", font_size=20),
            MathTex(r"A", r"\text{ : asymmetry parameter}", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        params.next_to(eqs, DOWN, buff=0.6)
        for p in params:
            p[0].set_color(YELLOW)
        self.play(FadeIn(params), run_time=1.0)
        self.wait(5.0)
        self.clear_screen()

    # ==================================================================
    # SECTION 9: Rikitake Time Series  (~70s)
    # ==================================================================
    def section_rikitake_timeseries(self):
        self.next_section("RikitakeTimeSeries")
        self.show_section_header("Rikitake Dynamo: Chaotic Reversals")

        title = Text("Numerical Solution of the Rikitake System", font_size=30, weight=BOLD)
        param_text = MathTex(r"\mu = 1.0,\quad A = 5.0", font_size=24, color=YELLOW)
        param_text.next_to(title, DOWN, buff=0.2)
        header = VGroup(title, param_text).to_edge(UP, buff=0.3)
        self.play(Write(title), FadeIn(param_text), run_time=1.0)

        # Solve system
        def rikitake(t, state):
            X, Y, Z = state
            mu, A = 1.0, 5.0
            return [-mu * X + Y * Z, -mu * Y + (Z - A) * X, 1 - X * Y]

        sol = solve_ivp(
            rikitake, (0, 250), [1.0, -1.0, 0.0],
            t_eval=np.linspace(0, 250, 15000), method='RK45', max_step=0.05,
        )
        t = sol.t
        X, Y, Z = sol.y

        # X(t) time series
        ax = Axes(
            x_range=[0, 250, 50],
            y_range=[-7, 7, 2],
            x_length=13,
            y_length=5.5,
            axis_config={"include_tip": False},
            x_axis_config={"include_numbers": True, "font_size": 14},
            y_axis_config={
                "include_numbers": True, "font_size": 14,
                "numbers_to_include": [-6, -4, -2, 0, 2, 4, 6],
            },
        ).move_to(DOWN * 0.8)

        ts_xlabel = ax.get_x_axis_label(
            Text("Time (dimensionless)", font_size=16),
            edge=RIGHT, direction=DOWN, buff=0.2,
        )
        ts_ylabel = ax.get_y_axis_label(
            MathTex(r"X(t)", font_size=22, color=BLUE),
            edge=UP, direction=LEFT, buff=0.2,
        )

        self.play(Create(ax), Write(ts_xlabel), Write(ts_ylabel), run_time=1.0)

        # Zero line
        zero_line = DashedLine(
            ax.c2p(0, 0), ax.c2p(250, 0),
            color=RED, stroke_width=1, dash_length=0.1,
        )
        zero_label = MathTex(r"X=0", font_size=16, color=RED).next_to(
            ax.c2p(250, 0), RIGHT, buff=0.1,
        )
        self.play(Create(zero_line), Write(zero_label), run_time=0.8)

        # Draw curve in segments for progressive reveal
        skip = 2
        t_s, X_s = t[::skip], X[::skip]
        n_pts = len(t_s)
        seg_size = n_pts // 5
        colors = [BLUE_B, BLUE_C, BLUE_D, BLUE_E, BLUE]

        for i in range(5):
            start = i * seg_size
            end = min((i + 1) * seg_size + 1, n_pts)
            seg_pts = [ax.c2p(ti, xi) for ti, xi in zip(t_s[start:end], X_s[start:end])]
            seg = VMobject(color=colors[i], stroke_width=1.5)
            seg.set_points_smoothly(seg_pts)
            self.play(Create(seg), run_time=1.5)

        self.wait(1.0)

        # Count reversals
        sign_changes = np.sum(np.diff(np.sign(X)) != 0)
        rev_text = Text(
            f"~{sign_changes} polarity reversals in 250 time units",
            font_size=20, color=RED,
        ).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(rev_text), run_time=0.8)
        self.wait(1.5)

        note = Text(
            "Variable intervals emerge from deterministic chaos",
            font_size=20, color=GREY_B,
        ).next_to(rev_text, UP, buff=0.2)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(5.0)
        self.clear_screen()

    # ==================================================================
    # SECTION 10: Phase Portrait  (~60s)
    # ==================================================================
    def section_rikitake_phase_portrait(self):
        self.next_section("PhasePortrait")
        self.show_section_header("Phase Portrait: Two-Lobed Attractor")

        title = Text("X-Y Phase Space", font_size=32, weight=BOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=0.8)

        def rikitake(t, state):
            X, Y, Z = state
            mu, A = 1.0, 5.0
            return [-mu * X + Y * Z, -mu * Y + (Z - A) * X, 1 - X * Y]

        sol = solve_ivp(
            rikitake, (0, 300), [1.0, -1.0, 0.0],
            t_eval=np.linspace(0, 300, 20000), method='RK45', max_step=0.1,
        )
        X, Y = sol.y[0], sol.y[1]

        ax = Axes(
            x_range=[-7, 7, 2],
            y_range=[-3.5, 3.5, 1],
            x_length=12,
            y_length=6.5,
            axis_config={"include_tip": True, "tip_length": 0.15},
            x_axis_config={"include_numbers": True, "font_size": 14},
            y_axis_config={"include_numbers": True, "font_size": 14},
        ).move_to(DOWN * 0.2)

        x_lab = ax.get_x_axis_label(MathTex(r"X", font_size=22), edge=RIGHT, direction=DOWN)
        y_lab = ax.get_y_axis_label(MathTex(r"Y", font_size=22), edge=UP, direction=LEFT)
        self.play(Create(ax), Write(x_lab), Write(y_lab), run_time=1.0)

        # Draw trajectory in colored segments
        skip = 3
        Xs, Ys = X[::skip], Y[::skip]
        all_pts = [ax.c2p(xi, yi) for xi, yi in zip(Xs, Ys)]

        seg_size = 300
        n_segs = len(all_pts) // seg_size
        palette = [BLUE, TEAL, GREEN, YELLOW, ORANGE, RED, PURPLE, PINK, BLUE_B, GREEN_B]

        segments = VGroup()
        for i in range(min(n_segs, 10)):
            seg_pts = all_pts[i * seg_size : (i + 1) * seg_size + 1]
            if len(seg_pts) < 2:
                continue
            seg = VMobject(
                color=palette[i % len(palette)],
                stroke_width=1, stroke_opacity=0.6,
            )
            seg.set_points_smoothly(seg_pts)
            segments.add(seg)

        for seg in segments[:4]:
            self.play(Create(seg), run_time=1.0)
        if len(segments) > 4:
            self.play(Create(VGroup(*segments[4:])), run_time=3.0)

        self.wait(0.5)

        # Fixed points
        # Equilibria at X=Y=k, Z=A/2+1/(2k^2) where k^2 = (A + sqrt(A^2+4))/2
        k_sq = (5 + np.sqrt(29)) / 2
        k = np.sqrt(k_sq)
        fp_plus = Dot(ax.c2p(k, 1/k), color=RED, radius=0.1)
        fp_minus = Dot(ax.c2p(-k, -1/k), color=RED, radius=0.1)
        fp_label_p = MathTex(r"\mathbf{P}_+", font_size=20, color=RED).next_to(fp_plus, UR, buff=0.1)
        fp_label_m = MathTex(r"\mathbf{P}_-", font_size=20, color=RED).next_to(fp_minus, DL, buff=0.1)

        self.play(FadeIn(fp_plus), FadeIn(fp_minus), Write(fp_label_p), Write(fp_label_m), run_time=0.8)
        self.wait(1.0)

        note1 = Text(
            "Trajectory orbits one fixed point, then switches chaotically",
            font_size=20, color=GREY_B,
        ).to_edge(DOWN, buff=0.6)
        note2 = Text(
            "Each lobe = one polarity state; switching = reversal",
            font_size=20, color=YELLOW,
        ).next_to(note1, DOWN, buff=0.15)
        self.play(FadeIn(note1), run_time=0.8)
        self.play(FadeIn(note2), run_time=0.8)
        self.wait(5.0)
        self.clear_screen()

    # ==================================================================
    # SECTION 11: Paleomagnetic Evidence  (~60s)
    # ==================================================================
    def section_paleomagnetic_evidence(self):
        self.next_section("PaleomagneticEvidence")
        self.show_section_header("Evidence from the Paleomagnetic Record")

        title = Text("Supporting Observations", font_size=32, weight=BOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=0.8)

        # Polarity timescale bar (schematic)
        bar_title = Text("Geomagnetic Polarity Timescale (schematic)", font_size=20, color=GREY_B)
        bar_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(bar_title), run_time=0.8)

        # Create a simplified polarity bar
        np.random.seed(123)
        total_width = 14
        intervals = []
        cum = 0
        while cum < total_width:
            width = np.random.exponential(0.8)
            width = max(0.15, min(width, 3.5))
            if cum + width > total_width:
                width = total_width - cum
            intervals.append(width)
            cum += width

        polarity_bar = VGroup()
        x_start = -total_width / 2
        current_x = x_start
        for i, w in enumerate(intervals):
            color = BLACK if i % 2 == 0 else WHITE
            rect = Rectangle(
                width=w, height=0.6,
                fill_color=color, fill_opacity=1.0,
                stroke_color=GREY, stroke_width=0.5,
            )
            rect.move_to(RIGHT * (current_x + w / 2) + UP * 0.5)
            polarity_bar.add(rect)
            current_x += w

        normal_label = Text("Normal", font_size=14, color=WHITE).next_to(polarity_bar, LEFT, buff=0.2)
        reversed_label = Text("Reversed", font_size=14, color=BLACK).next_to(normal_label, DOWN, buff=0.1)
        # Add colored squares as legend
        n_sq = Rectangle(width=0.3, height=0.3, fill_color=BLACK, fill_opacity=1, stroke_color=GREY)
        r_sq = Rectangle(width=0.3, height=0.3, fill_color=WHITE, fill_opacity=1, stroke_color=GREY)
        legend = VGroup(
            VGroup(n_sq, Text("Normal", font_size=14)).arrange(RIGHT, buff=0.1),
            VGroup(r_sq, Text("Reversed", font_size=14)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(polarity_bar, RIGHT, buff=0.3)

        self.play(Create(polarity_bar), run_time=2.0)
        self.play(FadeIn(legend), run_time=0.5)
        self.wait(1.5)

        time_arrow = Arrow(
            LEFT * (total_width / 2) + DOWN * 0.1,
            RIGHT * (total_width / 2) + DOWN * 0.1,
            buff=0, color=GREY, stroke_width=1.5,
        ).next_to(polarity_bar, DOWN, buff=0.15)
        time_label = Text("Time (millions of years)", font_size=16, color=GREY_B)
        time_label.next_to(time_arrow, DOWN, buff=0.1)
        self.play(Create(time_arrow), Write(time_label), run_time=0.8)
        self.wait(1.0)

        # Key facts
        facts = VGroup(
            Text("Interval durations: 10,000 to millions of years", font_size=20, color=WHITE),
            Text("Field intensity drops to 10-20% during transitions", font_size=20, color=WHITE),
            Text("Transitions take ~1,000-5,000 years to complete", font_size=20, color=WHITE),
            Text("No strict periodicity: consistent with geometric model", font_size=20, color=YELLOW),
            Text("Fitted p ~ 0.1-0.3 for Cenozoic era", font_size=20, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(DOWN * 2.5)

        for fact in facts:
            self.play(FadeIn(fact, shift=RIGHT * 0.2), run_time=0.7)
            self.wait(1.0)

        self.wait(4.0)
        self.clear_screen()

    # ==================================================================
    # SECTION 12: Model Summary  (~60s)
    # ==================================================================
    def section_model_summary(self):
        self.next_section("ModelSummary")
        self.show_section_header("Model Summary: Connecting the Components")

        boxes_data = [
            ("1. Dipole Oscillation", r"\text{Period } \tau \sim 10^3\text{--}10^4 \text{ yr}", BLUE),
            ("2. Nondipole Noise", r"r = B_{nd} / B_d \text{ (random, independent)}", GREEN),
            ("3. Bernoulli Trigger", r"p = P(r > r_c) \text{ at each minimum}", YELLOW),
            ("4. Geometric Intervals", r"P(K=k) = (1-p)^{k-1} p", GOLD),
            ("5. Physical Time", r"T = K \cdot \tau \sim 0.2\text{--}0.7 \text{ Ma}", RED),
        ]

        boxes = VGroup()
        for label_text, eq_text, color in boxes_data:
            box = RoundedRectangle(
                width=8, height=1.3, corner_radius=0.15,
                fill_color=color, fill_opacity=0.10,
                stroke_color=color, stroke_width=2,
            )
            label = Text(label_text, font_size=20, weight=BOLD, color=color)
            eq = MathTex(eq_text, font_size=20)
            content = VGroup(label, eq).arrange(DOWN, buff=0.12).move_to(box)
            boxes.add(VGroup(box, content))

        boxes.arrange(DOWN, buff=0.25).move_to(DOWN * 0.3)

        arrows = VGroup()
        for i in range(len(boxes) - 1):
            arrow = Arrow(
                boxes[i].get_bottom(), boxes[i + 1].get_top(),
                buff=0.05, color=WHITE, stroke_width=2,
                max_tip_length_to_length_ratio=0.2,
            )
            arrows.add(arrow)

        for i, box in enumerate(boxes):
            self.play(FadeIn(box, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(0.8)
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.4)

        self.wait(1.5)

        # Rikitake connection
        rik_note = Text(
            "Rikitake dynamo provides physical basis for chaotic oscillations",
            font_size=20, color=GREY_B,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rik_note), run_time=0.8)
        self.wait(5.0)
        self.clear_screen()

    # ==================================================================
    # SECTION 13: Closing  (~40s)
    # ==================================================================
    def section_closing(self):
        self.next_section("Closing")

        title = Text("Legacy and Significance", font_size=40, weight=BOLD)
        title.move_to(UP * 2.5)
        self.play(Write(title), run_time=1.5)
        self.wait(1.0)

        points = [
            "Pioneered statistical geomagnetism",
            "Explained irregular yet patterned reversal intervals",
            "Influenced modern polarity timescales (e.g., CK95)",
            "Connected stochastic modeling to core dynamics",
            "Foundation for Poisson process models of reversals",
        ]
        point_grp = VGroup()
        for pt in points:
            txt = Text(pt, font_size=24, color=WHITE)
            point_grp.add(txt)
        point_grp.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.7)

        for pt in point_grp:
            self.play(FadeIn(pt, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(1.2)

        self.wait(2.0)

        # Final equation
        final_eq = MathTex(
            r"P(K = k) = (1 - p)^{k-1}\, p",
            font_size=48, color=GOLD,
        ).move_to(DOWN * 2.5)
        eq_box = SurroundingRectangle(final_eq, color=GOLD, buff=0.2, corner_radius=0.1)
        self.play(Write(final_eq), Create(eq_box), run_time=1.5)
        self.wait(1.0)

        cite = Text(
            "Cox, A. (1968) Lengths of Geomagnetic Polarity Intervals",
            font_size=18, color=GREY_C,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cite), run_time=0.5)
        self.wait(5.0)

        # Final fade
        self.play(FadeOut(Group(*self.mobjects)), run_time=2.0)
        self.wait(1.0)

from manim import *
import numpy as np

# ============================================================================
# OPTIMIZED CONFIGURATION - DO NOT MODIFY THESE VALUES
# ============================================================================
config.frame_height = 10
config.frame_width = 10 * 16/9
config.pixel_height = 1440
config.pixel_width = 2560
config.background_color = "#0a0a0a"
# ============================================================================

def safe_position(mobject, max_y=4.0, min_y=-4.0):
    """Clamp mobject to safe vertical zone to prevent clipping."""
    top = mobject.get_top()[1]
    bottom = mobject.get_bottom()[1]
    if top > max_y:
        mobject.shift(DOWN * (top - max_y))
    elif bottom < min_y:
        mobject.shift(UP * (min_y - bottom))
    return mobject


# =============================================================================
# SCENE 1: TITLE PAGE (10 seconds exactly)
# =============================================================================
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
        self.wait(10)  # Exactly 10 seconds


# =============================================================================
# SCENE 2: ACOUSTIC LEVITATION (10 seconds exactly)
# =============================================================================
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
        y_range = np.linspace(-2.3, 1.8, 200)
        amp = 0.8
        points_l = [np.array([-amp * np.sin(2 * np.pi * y / 1.7), y, 0]) for y in y_range]
        points_r = [np.array([amp * np.sin(2 * np.pi * y / 1.7), y, 0]) for y in y_range]

        wave_curve_l = VMobject(color="#00bfff", stroke_width=2, stroke_opacity=0.5)
        wave_curve_l.set_points_smoothly(points_l)
        wave_curve_r = VMobject(color="#00bfff", stroke_width=2, stroke_opacity=0.5)
        wave_curve_r.set_points_smoothly(points_r)

        # Pressure nodes
        nodes = VGroup()
        node_positions = [-2.3 + 1.7/2 + i * 1.7/2 for i in range(5)]
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

        # Animations - timed to exactly 10 seconds
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.5)  # 0.5s
        self.play(
            FadeIn(speaker_top), FadeIn(speaker_bot),
            Create(wave_curve_l), Create(wave_curve_r),
            run_time=1.5  # 2.0s total
        )
        self.play(FadeIn(nodes), FadeIn(bead1), FadeIn(bead2), run_time=1.0)  # 3.0s total
        self.play(FadeIn(label_40k), FadeIn(arrow_wave), FadeIn(node_label), run_time=0.8)  # 3.8s total

        # Gentle oscillation of beads
        self.play(
            bead1.animate.shift(UP * 0.08), bead2.animate.shift(DOWN * 0.06),
            rate_func=there_and_back, run_time=1.2  # 5.0s total
        )
        self.play(
            bead1.animate.shift(DOWN * 0.06), bead2.animate.shift(UP * 0.08),
            rate_func=there_and_back, run_time=1.2  # 6.2s total
        )

        self.wait(2.8)  # 9.0s total

        # Fade out
        all_objs = VGroup(header, speaker_top, speaker_bot, wave_curve_l, wave_curve_r,
                          nodes, bead1, bead2, label_40k, arrow_wave, node_label)
        self.play(FadeOut(all_objs), run_time=1.0)  # 10.0s total


# =============================================================================
# SCENE 3: TWO BEADS (10 seconds exactly)
# =============================================================================
class Scene03_TwoBeads(Scene):
    def construct(self):
        header = Text("Two Beads, One Strange Dance", font_size=38, weight=BOLD, color=WHITE)
        header.move_to(UP * 3.8)

        # Large bead
        large_bead = Circle(radius=0.5, color="#ff6f61", fill_opacity=0.7, stroke_width=3)
        large_bead.move_to(LEFT * 2)
        large_label = Text("Large", font_size=18, color="#ff6f61")
        large_label.next_to(large_bead, DOWN, buff=0.3)

        # Small bead
        small_bead = Circle(radius=0.28, color="#ffd700", fill_opacity=0.7, stroke_width=3)
        small_bead.move_to(RIGHT * 2)
        small_label = Text("Small", font_size=18, color="#ffd700")
        small_label.next_to(small_bead, DOWN, buff=0.3)

        # Force arrows (nonreciprocal)
        arrow_big = Arrow(
            start=large_bead.get_right() + RIGHT * 0.15,
            end=small_bead.get_left() + LEFT * 0.15,
            color="#ff6f61", stroke_width=5, max_tip_length_to_length_ratio=0.12
        ).shift(UP * 0.3)
        arrow_big_label = Text("Strong push", font_size=14, color="#ff6f61")
        arrow_big_label.next_to(arrow_big, UP, buff=0.15)

        arrow_small = Arrow(
            start=small_bead.get_left() + LEFT * 0.15,
            end=large_bead.get_right() + RIGHT * 0.15,
            color="#ffd700", stroke_width=2, max_tip_length_to_length_ratio=0.12
        ).shift(DOWN * 0.3)
        arrow_small_label = Text("Weak push back", font_size=14, color="#ffd700")
        arrow_small_label.next_to(arrow_small, DOWN, buff=0.15)

        # Explanation
        explanation = Text(
            "Different sizes scatter sound differently,\ncreating an imbalanced push.",
            font_size=20, color=GREY_B, line_spacing=1.3
        )
        explanation.move_to(DOWN * 2.5)

        bead_group = VGroup(large_bead, large_label, small_bead, small_label)

        # Animations - timed to exactly 10 seconds
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.5)  # 0.5s
        self.play(FadeIn(bead_group), run_time=0.7)  # 1.2s total
        self.play(GrowArrow(arrow_big), FadeIn(arrow_big_label), run_time=0.7)  # 1.9s total
        self.play(GrowArrow(arrow_small), FadeIn(arrow_small_label), run_time=0.7)  # 2.6s total
        self.play(FadeIn(explanation), run_time=0.5)  # 3.1s total

        # Animate the imbalance: small bead moves more (3 cycles)
        for _ in range(3):
            self.play(
                small_bead.animate.shift(RIGHT * 0.25),
                large_bead.animate.shift(LEFT * 0.08),
                rate_func=there_and_back, run_time=0.7  # 2.1s total
            )
        # Now at 5.2s

        self.wait(3.8)  # 9.0s total

        all_objs = VGroup(header, bead_group, arrow_big, arrow_big_label,
                          arrow_small, arrow_small_label, explanation)
        self.play(FadeOut(all_objs), run_time=1.0)  # 10.0s total


# =============================================================================
# SCENE 4: NEWTON'S THIRD LAW (10 seconds exactly)
# =============================================================================
class Scene04_NewtonThird(Scene):
    def construct(self):
        header = Text("Breaking Newton's Third Law?", font_size=38, weight=BOLD, color=WHITE)
        header.move_to(UP * 3.8)

        # Newton's third law text
        law_text = Text("Every action has an equal and opposite reaction.", font_size=22, color=GREY_B)
        law_text.move_to(UP * 2.5)

        # Strike-through effect
        strike = Line(
            law_text.get_left() + LEFT * 0.1,
            law_text.get_right() + RIGHT * 0.1,
            color="#ff4444", stroke_width=3
        )

        # Ferry metaphor
        ferry_big = VGroup(
            RoundedRectangle(width=2.5, height=0.8, corner_radius=0.15,
                             color="#ff6f61", fill_opacity=0.6, stroke_width=2),
            Text("Large Ferry", font_size=14, color=WHITE)
        ).arrange(DOWN, buff=0.05).move_to(LEFT * 3 + DOWN * 0.5)

        ferry_small = VGroup(
            RoundedRectangle(width=1.4, height=0.5, corner_radius=0.1,
                             color="#ffd700", fill_opacity=0.6, stroke_width=2),
            Text("Small Ferry", font_size=14, color=WHITE)
        ).arrange(DOWN, buff=0.05).move_to(RIGHT * 3 + DOWN * 0.5)

        # Water waves
        waves = VGroup()
        for i in range(3):
            wave_arc = Arc(radius=0.8 + i * 0.4, angle=PI/2, start_angle=-PI/4,
                           color="#00bfff", stroke_width=1.5, stroke_opacity=0.5 - i * 0.12)
            wave_arc.move_to(LEFT * 1 + DOWN * 0.5)
            waves.add(wave_arc)

        # Explanation
        expl = Text(
            "The 'missing' momentum is carried away\nby the scattered sound waves.",
            font_size=20, color="#00bfff", line_spacing=1.3
        )
        expl.move_to(DOWN * 2.5)

        momentum_note = Text("Total momentum is conserved.", font_size=18, color="#44ff44")
        momentum_note.move_to(DOWN * 3.5)

        # Animations - timed to exactly 10 seconds
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.5)  # 0.5s
        self.play(Write(law_text), run_time=0.8)  # 1.3s total
        self.play(Create(strike), run_time=0.4)  # 1.7s total
        self.play(FadeIn(ferry_big), FadeIn(ferry_small), FadeIn(waves), run_time=0.8)  # 2.5s total

        # Animate ferries: small one rocks more (2 cycles)
        self.play(
            ferry_small.animate.shift(RIGHT * 0.4),
            ferry_big.animate.shift(LEFT * 0.1),
            rate_func=there_and_back, run_time=0.9  # 3.4s total
        )
        self.play(
            ferry_small.animate.shift(LEFT * 0.3),
            ferry_big.animate.shift(RIGHT * 0.08),
            rate_func=there_and_back, run_time=0.9  # 4.3s total
        )

        self.play(FadeIn(expl), run_time=0.6)  # 4.9s total
        self.play(FadeIn(momentum_note), run_time=0.6)  # 5.5s total

        self.wait(3.5)  # 9.0s total

        all_objs = VGroup(header, law_text, strike, ferry_big, ferry_small, waves, expl, momentum_note)
        self.play(FadeOut(all_objs), run_time=1.0)  # 10.0s total


# =============================================================================
# SCENE 5: TIME CRYSTAL (10 seconds exactly)
# =============================================================================
class Scene05_TimeCrystal(Scene):
    def construct(self):
        header = Text("From Imbalance to Time Crystal", font_size=38, weight=BOLD, color=WHITE)
        header.move_to(UP * 3.8)

        # Phase space axes
        axes = Axes(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=5, y_length=5,
            axis_config={"color": GREY_C, "stroke_width": 1.5, "include_ticks": False},
        ).move_to(LEFT * 0.5 + DOWN * 0.3)

        x_label = Text("Position", font_size=16, color=GREY_B)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Velocity", font_size=16, color=GREY_B)
        y_label.next_to(axes.y_axis, LEFT, buff=0.2)

        # Limit cycle (ellipse)
        limit_cycle = Ellipse(width=3.5, height=3.0, color="#00bfff", stroke_width=3)
        limit_cycle.move_to(axes.get_center())

        # Dot tracing the limit cycle
        trace_dot = Dot(color="#ffd700", radius=0.1)
        trace_dot.move_to(limit_cycle.point_from_proportion(0))

        # Label
        lc_label = Text("Limit Cycle", font_size=18, color="#00bfff")
        lc_label.next_to(limit_cycle, RIGHT, buff=0.5).shift(UP * 0.5)

        # Right side explanation - FIXED SPACING
        expl_lines = VGroup(
            Text("The beads spontaneously", font_size=18, color=GREY_B),
            Text("enter a stable orbit.", font_size=18, color=GREY_B),
            Text("", font_size=6),  # Spacer
            Text("No external clock.", font_size=18, color="#ffd700"),
            Text("No periodic driving.", font_size=18, color="#ffd700"),
            Text("", font_size=6),  # Spacer
            Text("~61 cycles/second.", font_size=18, color="#00bfff"),
            Text("Runs for hours.", font_size=18, color="#00bfff"),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 5.2 + DOWN * 0.3)
        safe_position(expl_lines)

        # Animations - timed to exactly 10 seconds
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.4)  # 0.4s
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.8)  # 1.2s total
        self.play(Create(limit_cycle), FadeIn(lc_label), run_time=0.8)  # 2.0s total
        self.play(FadeIn(trace_dot), run_time=0.3)  # 2.3s total

        # Trace around the limit cycle
        self.play(MoveAlongPath(trace_dot, limit_cycle), run_time=2.5, rate_func=linear)  # 4.8s total

        self.play(FadeIn(expl_lines), run_time=0.7)  # 5.5s total

        self.wait(3.5)  # 9.0s total

        all_objs = VGroup(header, axes, x_label, y_label, limit_cycle, trace_dot, lc_label, expl_lines)
        self.play(FadeOut(all_objs), run_time=1.0)  # 10.0s total


# =============================================================================
# SCENE 6: ENERGY FLOW (10 seconds exactly)
# =============================================================================
class Scene06_EnergyFlow(Scene):
    def construct(self):
        header = Text("Energy Flow", font_size=40, weight=BOLD, color=WHITE)
        header.move_to(UP * 3.8)

        # Three boxes
        box_sound = RoundedRectangle(width=3.5, height=1.8, corner_radius=0.2,
                                      color="#00bfff", fill_opacity=0.15, stroke_width=2)
        label_sound = VGroup(
            Text("Sound Field", font_size=22, weight=BOLD, color="#00bfff"),
            Text("(Static, 40 kHz)", font_size=15, color=GREY_C)
        ).arrange(DOWN, buff=0.1)
        sound_group = VGroup(box_sound, label_sound).move_to(LEFT * 5 + DOWN * 0.2)

        box_beads = RoundedRectangle(width=3.5, height=1.8, corner_radius=0.2,
                                      color="#ffd700", fill_opacity=0.15, stroke_width=2)
        label_beads = VGroup(
            Text("Bead Pair", font_size=22, weight=BOLD, color="#ffd700"),
            Text("(Oscillating)", font_size=15, color=GREY_C)
        ).arrange(DOWN, buff=0.1)
        beads_group = VGroup(box_beads, label_beads).move_to(DOWN * 0.2)

        box_air = RoundedRectangle(width=3.5, height=1.8, corner_radius=0.2,
                                    color="#ff6f61", fill_opacity=0.15, stroke_width=2)
        label_air = VGroup(
            Text("Air (Drag)", font_size=22, weight=BOLD, color="#ff6f61"),
            Text("(Dissipation)", font_size=15, color=GREY_C)
        ).arrange(DOWN, buff=0.1)
        air_group = VGroup(box_air, label_air).move_to(RIGHT * 5 + DOWN * 0.2)

        # Arrows
        arrow_in = Arrow(
            sound_group.get_right(), beads_group.get_left(),
            color="#00bfff", stroke_width=4, buff=0.15,
            max_tip_length_to_length_ratio=0.12
        )
        label_in = Text("Energy In", font_size=16, color="#00bfff")
        label_in.next_to(arrow_in, UP, buff=0.15)

        arrow_out = Arrow(
            beads_group.get_right(), air_group.get_left(),
            color="#ff6f61", stroke_width=4, buff=0.15,
            max_tip_length_to_length_ratio=0.12
        )
        label_out = Text("Energy Out", font_size=16, color="#ff6f61")
        label_out.next_to(arrow_out, UP, buff=0.15)

        # Balance annotation
        balance = Text("Energy In = Energy Out  >>  Stable Oscillation", font_size=20, color="#44ff44")
        balance.move_to(DOWN * 2.8)

        mechanism = Text(
            "Nonreciprocal scattering extracts energy\nfrom the standing wave each cycle.",
            font_size=18, color=GREY_B, line_spacing=1.3
        )
        mechanism.move_to(DOWN * 3.7)
        safe_position(mechanism)

        # Animations - timed to exactly 10 seconds
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.4)  # 0.4s
        self.play(FadeIn(sound_group), run_time=0.5)  # 0.9s total
        self.play(GrowArrow(arrow_in), FadeIn(label_in), run_time=0.5)  # 1.4s total
        self.play(FadeIn(beads_group), run_time=0.5)  # 1.9s total
        self.play(GrowArrow(arrow_out), FadeIn(label_out), run_time=0.5)  # 2.4s total
        self.play(FadeIn(air_group), run_time=0.5)  # 2.9s total
        self.play(FadeIn(balance), run_time=0.5)  # 3.4s total
        self.play(FadeIn(mechanism), run_time=0.4)  # 3.8s total

        # Pulse the beads box to show active oscillation (2 pulses)
        self.play(
            box_beads.animate.set_fill(opacity=0.35),
            rate_func=there_and_back, run_time=0.8  # 4.6s total
        )
        self.play(
            box_beads.animate.set_fill(opacity=0.35),
            rate_func=there_and_back, run_time=0.8  # 5.4s total
        )

        self.wait(3.6)  # 9.0s total

        all_objs = VGroup(header, sound_group, beads_group, air_group,
                          arrow_in, label_in, arrow_out, label_out, balance, mechanism)
        self.play(FadeOut(all_objs), run_time=1.0)  # 10.0s total


# =============================================================================
# SCENE 7: EXCEPTIONAL POINT (10 seconds exactly)
# =============================================================================
class Scene07_ExceptionalPoint(Scene):
    def construct(self):
        header = Text("The Tipping Point", font_size=40, weight=BOLD, color=WHITE)
        header.move_to(UP * 3.8)

        # Horizontal line representing parameter space
        param_line = Line(LEFT * 6, RIGHT * 6, color=GREY_C, stroke_width=2)
        param_line.move_to(UP * 0.5)

        param_label = Text("Size Asymmetry", font_size=16, color=GREY_C)
        param_label.next_to(param_line, DOWN, buff=0.3)

        # Two mode dots starting apart
        mode1 = Dot(color="#00bfff", radius=0.15).move_to(LEFT * 3 + UP * 0.5)
        mode2 = Dot(color="#ff6f61", radius=0.15).move_to(RIGHT * 3 + UP * 0.5)

        mode1_label = Text("Symmetric Mode", font_size=15, color="#00bfff")
        mode1_label.next_to(mode1, UP, buff=0.3)
        mode2_label = Text("Breathing Mode", font_size=15, color="#ff6f61")
        mode2_label.next_to(mode2, UP, buff=0.3)

        # Exceptional point marker (rotated square as diamond)
        ep_marker = Square(color="#ffd700", fill_opacity=0.8, stroke_width=2).scale(0.2).rotate(PI/4)
        ep_marker.move_to(UP * 0.5)
        ep_label = Text("Exceptional\nPoint", font_size=16, color="#ffd700", line_spacing=1.2)
        ep_label.next_to(ep_marker, DOWN, buff=0.5)

        # Before EP (left region)
        left_region = Text("Stationary\n(Overdamped)", font_size=16, color=GREY_B, line_spacing=1.2)
        left_region.move_to(LEFT * 4.5 + DOWN * 2.0)

        # After EP (right region)
        right_region = Text("Time Crystal!\n(Self-Oscillating)", font_size=16, color="#44ff44", line_spacing=1.2)
        right_region.move_to(RIGHT * 4.5 + DOWN * 2.0)

        # Divider
        divider = DashedLine(UP * 0.5, DOWN * 3.0, color="#ffd700", stroke_width=1.5, dash_length=0.15)

        explanation = Text(
            "When modes merge, the system tips into spontaneous oscillation.",
            font_size=20, color=GREY_B
        )
        explanation.move_to(DOWN * 3.5)
        safe_position(explanation)

        # Animations - timed to exactly 10 seconds
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.4)  # 0.4s
        self.play(Create(param_line), FadeIn(param_label), run_time=0.5)  # 0.9s total
        self.play(
            FadeIn(mode1), FadeIn(mode1_label),
            FadeIn(mode2), FadeIn(mode2_label),
            run_time=0.6  # 1.5s total
        )
        self.play(FadeIn(left_region), run_time=0.4)  # 1.9s total

        # Modes approach each other
        self.play(
            mode1.animate.move_to(LEFT * 0.3 + UP * 0.5),
            mode1_label.animate.move_to(LEFT * 0.3 + UP * 1.2),
            mode2.animate.move_to(RIGHT * 0.3 + UP * 0.5),
            mode2_label.animate.move_to(RIGHT * 0.3 + UP * 1.2),
            run_time=1.8  # 3.7s total
        )

        # Merge at EP
        self.play(
            mode1.animate.move_to(UP * 0.5),
            mode2.animate.move_to(UP * 0.5),
            FadeOut(mode1_label), FadeOut(mode2_label),
            run_time=0.9  # 4.6s total
        )
        self.play(
            FadeIn(ep_marker, scale=2), FadeIn(ep_label),
            Create(divider),
            run_time=0.7  # 5.3s total
        )
        self.play(FadeIn(right_region), run_time=0.4)  # 5.7s total
        self.play(FadeIn(explanation), run_time=0.4)  # 6.1s total

        self.wait(2.9)  # 9.0s total

        all_objs = VGroup(header, param_line, param_label, mode1, mode2,
                          ep_marker, ep_label, left_region, right_region,
                          divider, explanation)
        self.play(FadeOut(all_objs), run_time=1.0)  # 10.0s total


# =============================================================================
# SCENE 8: IMPLICATIONS (10 seconds exactly)
# =============================================================================
class Scene08_Implications(Scene):
    def make_item(self, text, color):
        bullet = Dot(radius=0.06, color=color)
        label = Text(text, font_size=19, color=GREY_B)
        return VGroup(bullet, label).arrange(RIGHT, buff=0.2)

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

        # Animations - timed to exactly 10 seconds
        self.play(FadeIn(header, shift=DOWN * 0.3), run_time=0.4)  # 0.4s
        self.play(FadeIn(tech_header), FadeIn(bio_header), Create(divider), run_time=0.5)  # 0.9s total

        # Fade in items (4 pairs = 4 * 0.45s = 1.8s)
        for t_item, b_item in zip(tech_items, bio_items):
            self.play(FadeIn(t_item, shift=RIGHT * 0.2), FadeIn(b_item, shift=LEFT * 0.2), run_time=0.45)
        # Now at 2.7s total

        self.play(FadeIn(insight), run_time=0.5)  # 3.2s total

        self.wait(5.8)  # 9.0s total

        all_objs = VGroup(header, tech_header, tech_items, bio_header, bio_items, divider, insight)
        self.play(FadeOut(all_objs), run_time=1.0)  # 10.0s total


# =============================================================================
# SCENE 9: CREDITS (10 seconds exactly, NO fade to black at end)
# =============================================================================
class Scene09_Credits(Scene):
    def construct(self):
        # Recap line
        recap = Text(
            "A desktop experiment revealed time crystals\nhiding in a cushion of sound.",
            font_size=26, color=GREY_B, line_spacing=1.4
        )
        recap.move_to(UP * 1.5)

        # Decorative line
        line = Line(LEFT * 4, RIGHT * 4, color="#00bfff", stroke_width=2)
        line.move_to(UP * 0.2)

        # Attribution
        attribution = Text("Big D'", font_size=36, weight=BOLD, color=WHITE)
        attribution.move_to(DOWN * 0.8)

        handle = Text("@alltheputs", font_size=20, color="#00bfff")
        handle.next_to(attribution, DOWN, buff=0.3)

        # Source
        source = Text(
            "Source: Morrell, Elliott & Grier\nPhys. Rev. Lett. (2025)",
            font_size=16, color=GREY_C, line_spacing=1.3
        )
        source.move_to(DOWN * 2.5)

        # Decorative beads (callback to opening)
        bead_large = Circle(radius=0.3, color="#ff6f61", fill_opacity=0.4, stroke_width=2)
        bead_large.move_to(LEFT * 5.5 + DOWN * 3.0)
        bead_small = Circle(radius=0.18, color="#ffd700", fill_opacity=0.4, stroke_width=2)
        bead_small.move_to(RIGHT * 5.5 + DOWN * 2.8)

        # Animations - timed to exactly 10 seconds (NO fade out at end)
        self.play(FadeIn(recap), run_time=0.8)  # 0.8s
        self.play(Create(line), run_time=0.4)  # 1.2s total
        self.play(FadeIn(attribution), FadeIn(handle), run_time=0.6)  # 1.8s total
        self.play(FadeIn(source), run_time=0.5)  # 2.3s total
        self.play(FadeIn(bead_large), FadeIn(bead_small), run_time=0.4)  # 2.7s total

        # Hold -- no fade out at end
        self.wait(7.3)  # 10.0s total exactly

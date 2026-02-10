"""
The Melting Table: Visualizing the Periodic Table's Phase Transition
====================================================================
A 5-scene Manim story depicting the structural dissolution of the
periodic table at high atomic numbers.

Render individual scenes:
    manim melting_table.py Scene1_FamiliarGrid
    manim melting_table.py Scene2_RollingSpiral
    manim melting_table.py Scene3_EngineUnderTheHood
    manim melting_table.py Scene4_Dissolution
    manim melting_table.py Scene5_WhatWeKnow

Render all scenes sequentially:
    manim melting_table.py Scene1_FamiliarGrid Scene2_RollingSpiral \
        Scene3_EngineUnderTheHood Scene4_Dissolution Scene5_WhatWeKnow
"""

from manim import *
import numpy as np

# ============================================================================
# OPTIMIZED CONFIGURATION - DO NOT MODIFY THESE VALUES
# ============================================================================
config.frame_height = 10
config.frame_width = 10 * 16 / 9
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
# ELEMENT DATA
# ============================================================================
# (symbol, Z, period, group, block, color_category)
# color_category: "s"=red-ish, "p"=blue-ish, "d"=green-ish, "f"=purple-ish
ELEMENTS = [
    ("H", 1, 1, 1, "s"), ("He", 2, 1, 18, "s"),
    ("Li", 3, 2, 1, "s"), ("Be", 4, 2, 2, "s"),
    ("B", 5, 2, 13, "p"), ("C", 6, 2, 14, "p"), ("N", 7, 2, 15, "p"),
    ("O", 8, 2, 16, "p"), ("F", 9, 2, 17, "p"), ("Ne", 10, 2, 18, "p"),
    ("Na", 11, 3, 1, "s"), ("Mg", 12, 3, 2, "s"),
    ("Al", 13, 3, 13, "p"), ("Si", 14, 3, 14, "p"), ("P", 15, 3, 15, "p"),
    ("S", 16, 3, 16, "p"), ("Cl", 17, 3, 17, "p"), ("Ar", 18, 3, 18, "p"),
    ("K", 19, 4, 1, "s"), ("Ca", 20, 4, 2, "s"),
    ("Sc", 21, 4, 3, "d"), ("Ti", 22, 4, 4, "d"), ("V", 23, 4, 5, "d"),
    ("Cr", 24, 4, 6, "d"), ("Mn", 25, 4, 7, "d"), ("Fe", 26, 4, 8, "d"),
    ("Co", 27, 4, 9, "d"), ("Ni", 28, 4, 10, "d"), ("Cu", 29, 4, 11, "d"),
    ("Zn", 30, 4, 12, "d"), ("Ga", 31, 4, 13, "p"), ("Ge", 32, 4, 14, "p"),
    ("As", 33, 4, 15, "p"), ("Se", 34, 4, 16, "p"), ("Br", 35, 4, 17, "p"),
    ("Kr", 36, 4, 18, "p"),
    ("Rb", 37, 5, 1, "s"), ("Sr", 38, 5, 2, "s"),
    ("Y", 39, 5, 3, "d"), ("Zr", 40, 5, 4, "d"), ("Nb", 41, 5, 5, "d"),
    ("Mo", 42, 5, 6, "d"), ("Tc", 43, 5, 7, "d"), ("Ru", 44, 5, 8, "d"),
    ("Rh", 45, 5, 9, "d"), ("Pd", 46, 5, 10, "d"), ("Ag", 47, 5, 11, "d"),
    ("Cd", 48, 5, 12, "d"), ("In", 49, 5, 13, "p"), ("Sn", 50, 5, 14, "p"),
    ("Sb", 51, 5, 15, "p"), ("Te", 52, 5, 16, "p"), ("I", 53, 5, 17, "p"),
    ("Xe", 54, 5, 18, "p"),
    ("Cs", 55, 6, 1, "s"), ("Ba", 56, 6, 2, "s"),
    ("La", 57, 6, 3, "f"), ("Ce", 58, 6, 3, "f"), ("Pr", 59, 6, 3, "f"),
    ("Nd", 60, 6, 3, "f"), ("Pm", 61, 6, 3, "f"), ("Sm", 62, 6, 3, "f"),
    ("Eu", 63, 6, 3, "f"), ("Gd", 64, 6, 3, "f"), ("Tb", 65, 6, 3, "f"),
    ("Dy", 66, 6, 3, "f"), ("Ho", 67, 6, 3, "f"), ("Er", 68, 6, 3, "f"),
    ("Tm", 69, 6, 3, "f"), ("Yb", 70, 6, 3, "f"), ("Lu", 71, 6, 3, "d"),
    ("Hf", 72, 6, 4, "d"), ("Ta", 73, 6, 5, "d"), ("W", 74, 6, 6, "d"),
    ("Re", 75, 6, 7, "d"), ("Os", 76, 6, 8, "d"), ("Ir", 77, 6, 9, "d"),
    ("Pt", 78, 6, 10, "d"), ("Au", 79, 6, 11, "d"), ("Hg", 80, 6, 12, "d"),
    ("Tl", 81, 6, 13, "p"), ("Pb", 82, 6, 14, "p"), ("Bi", 83, 6, 15, "p"),
    ("Po", 84, 6, 16, "p"), ("At", 85, 6, 17, "p"), ("Rn", 86, 6, 18, "p"),
    ("Fr", 87, 7, 1, "s"), ("Ra", 88, 7, 2, "s"),
    ("Ac", 89, 7, 3, "f"), ("Th", 90, 7, 3, "f"), ("Pa", 91, 7, 3, "f"),
    ("U", 92, 7, 3, "f"), ("Np", 93, 7, 3, "f"), ("Pu", 94, 7, 3, "f"),
    ("Am", 95, 7, 3, "f"), ("Cm", 96, 7, 3, "f"), ("Bk", 97, 7, 3, "f"),
    ("Cf", 98, 7, 3, "f"), ("Es", 99, 7, 3, "f"), ("Fm", 100, 7, 3, "f"),
    ("Md", 101, 7, 3, "f"), ("No", 102, 7, 3, "f"), ("Lr", 103, 7, 3, "d"),
    ("Rf", 104, 7, 4, "d"), ("Db", 105, 7, 5, "d"), ("Sg", 106, 7, 6, "d"),
    ("Bh", 107, 7, 7, "d"), ("Hs", 108, 7, 8, "d"), ("Mt", 109, 7, 9, "d"),
    ("Ds", 110, 7, 10, "d"), ("Rg", 111, 7, 11, "d"), ("Cn", 112, 7, 12, "d"),
    ("Nh", 113, 7, 13, "p"), ("Fl", 114, 7, 14, "p"), ("Mc", 115, 7, 15, "p"),
    ("Lv", 116, 7, 16, "p"), ("Ts", 117, 7, 17, "p"), ("Og", 118, 7, 18, "p"),
]

BLOCK_COLORS = {
    "s": "#E74C3C",
    "p": "#3498DB",
    "d": "#2ECC71",
    "f": "#9B59B6",
}

NOBLE_GASES = {"He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"}
GROUP1 = {"H", "Li", "Na", "K", "Rb", "Cs", "Fr"}


def z_to_color(z, max_z=118):
    t = z / max_z
    if t < 0.25:
        return interpolate_color(BLUE, GREEN, t * 4)
    elif t < 0.5:
        return interpolate_color(GREEN, YELLOW, (t - 0.25) * 4)
    elif t < 0.75:
        return interpolate_color(YELLOW, ORANGE, (t - 0.5) * 4)
    else:
        return interpolate_color(ORANGE, RED, (t - 0.75) * 4)


def get_grid_pos(period, group):
    """Convert (period, group) to grid x,y. Returns center coordinates."""
    col_width = 0.7
    row_height = 0.55
    x = (group - 9.5) * col_width
    y = (4.5 - period) * row_height
    return np.array([x, y, 0])


def get_spiral_pos(z, center=ORIGIN, base_r=0.5, growth=0.025, turns_factor=0.12):
    """Map atomic number Z to spiral (r, theta) coordinates."""
    theta = z * turns_factor * TAU
    r = base_r + growth * z
    x = center[0] + r * np.cos(theta)
    y = center[1] + r * np.sin(theta)
    return np.array([x, y, 0])


# ============================================================================
# SCENE 1: THE FAMILIAR GRID
# ============================================================================
class Scene1_FamiliarGrid(Scene):
    def construct(self):
        title = Text("The Periodic Table", font_size=44, weight=BOLD)
        title.move_to(UP * 3.8)

        # Build the grid
        grid_group = VGroup()
        element_cells = {}

        for sym, z, period, group, block in ELEMENTS:
            if block == "f":
                continue  # Skip f-block to keep the grid compact

            pos = get_grid_pos(period, group)
            cell = Square(side_length=0.55, stroke_width=1.0, stroke_color=WHITE)
            cell.set_fill(BLOCK_COLORS[block], opacity=0.25)
            cell.move_to(pos)
            label = Text(sym, font_size=11)
            label.move_to(pos)
            pair = VGroup(cell, label)
            grid_group.add(pair)
            element_cells[sym] = pair

        grid_group.move_to(DOWN * 0.3)
        safe_position(grid_group)

        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(grid_group, lag_ratio=0.005), run_time=2.5)
        self.wait(0.5)

        # Highlight Group 1 and Group 18
        g1_cells = VGroup(*[element_cells[s] for s in GROUP1 if s in element_cells])
        g18_cells = VGroup(*[element_cells[s] for s in NOBLE_GASES if s in element_cells])

        g1_highlight = SurroundingRectangle(g1_cells, color=RED, buff=0.05, stroke_width=3)
        g18_highlight = SurroundingRectangle(g18_cells, color=TEAL_B, buff=0.05, stroke_width=3)

        g1_label = Text("Group 1", font_size=16, color=RED)
        g1_label.next_to(g1_highlight, LEFT, buff=0.15)
        safe_position(g1_label)

        g18_label = Text("Group 18", font_size=16, color=TEAL_B)
        g18_label.next_to(g18_highlight, RIGHT, buff=0.15)
        safe_position(g18_label)

        self.play(
            Create(g1_highlight), Create(g18_highlight),
            Write(g1_label), Write(g18_label),
            run_time=1.2,
        )
        self.wait(0.5)

        # Draw dashed gap line
        gap_line = DashedLine(
            g1_highlight.get_right() + RIGHT * 0.1,
            g18_highlight.get_left() + LEFT * 0.1,
            dash_length=0.15, color=YELLOW,
        )
        gap_text = Text(
            "These neighbors are separated by 1 electron,\n"
            "but the grid places them as far apart as possible.",
            font_size=18, color=YELLOW,
        )
        gap_text.move_to(DOWN * 3.6)
        safe_position(gap_text)

        self.play(Create(gap_line), Write(gap_text), run_time=1.5)
        self.wait(20.5)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.2,
        )
        self.wait(0.3)


# ============================================================================
# SCENE 2: ROLLING INTO A SPIRAL
# ============================================================================
class Scene2_RollingSpiral(Scene):
    def construct(self):
        title = Text("Reconnecting the Seam", font_size=44, weight=BOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=1.0)

        # Build element dots at grid positions (compact, no f-block)
        dots = VGroup()
        grid_positions = {}
        spiral_positions = {}

        filtered = [(s, z, p, g, b) for s, z, p, g, b in ELEMENTS if b != "f"]

        for sym, z, period, group, block in filtered:
            gpos = get_grid_pos(period, group)
            dot = Dot(gpos, radius=0.08, color=z_to_color(z))
            dots.add(dot)
            grid_positions[sym] = gpos.copy()
            spiral_positions[sym] = get_spiral_pos(z)

        dots.move_to(DOWN * 0.2)
        offset = dots.get_center() - DOWN * 0.2

        self.play(FadeIn(dots, lag_ratio=0.005), run_time=1.5)
        self.wait(0.5)

        morph_text = Text(
            "Roll the grid into a cylinder...", font_size=22, color=YELLOW
        )
        morph_text.move_to(DOWN * 3.5)
        safe_position(morph_text)
        self.play(Write(morph_text), run_time=0.8)

        # Animate dots from grid to spiral positions
        spiral_center = DOWN * 0.2
        anims = []
        for i, (sym, z, period, group, block) in enumerate(filtered):
            target_pos = get_spiral_pos(z, center=spiral_center)
            anims.append(dots[i].animate.move_to(target_pos))

        self.play(*anims, run_time=3.0, rate_func=smooth)
        self.wait(0.3)

        self.play(FadeOut(morph_text), run_time=0.5)

        # Draw the spiral curve underneath
        spiral_curve = ParametricFunction(
            lambda t: get_spiral_pos(t, center=spiral_center),
            t_range=[1, 118],
            color=WHITE,
            stroke_width=1.2,
            stroke_opacity=0.4,
        )
        self.play(Create(spiral_curve), run_time=1.5)

        # Highlight noble gases on the spiral
        noble_z = [2, 10, 18, 36, 54, 86, 118]
        noble_labels_group = VGroup()
        for nz in noble_z:
            pos = get_spiral_pos(nz, center=spiral_center)
            sym = [s for s, z, _, _, _ in ELEMENTS if z == nz][0]
            lbl = Text(sym, font_size=13, color=TEAL_B, weight=BOLD)
            lbl.move_to(pos + normalize(pos - spiral_center) * 0.3)
            noble_labels_group.add(lbl)

        self.play(FadeIn(noble_labels_group, lag_ratio=0.1), run_time=1.2)

        spoke_text = Text(
            "Noble gases now fall along a natural radial line.\n"
            "Group 1 and Group 18 are finally adjacent.",
            font_size=20, color=GREEN,
        )
        spoke_text.move_to(DOWN * 3.5)
        safe_position(spoke_text)
        self.play(Write(spoke_text), run_time=1.5)
        self.wait(2.5)

        # Label period widths along the spiral
        period_info = Text(
            "Period widths: 2, 8, 8, 18, 18, 32, 32",
            font_size=18, color=GREY_B,
        )
        period_info.move_to(UP * 3.0)
        safe_position(period_info)
        self.play(Write(period_info), run_time=1.0)
        self.wait(50.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.2)
        self.wait(0.3)


# ============================================================================
# SCENE 3: THE ENGINE UNDER THE HOOD
# ============================================================================
class Scene3_EngineUnderTheHood(Scene):
    def construct(self):
        title = Text("The Crossover at Gold", font_size=44, weight=BOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=1.0)

        # Build axes
        axes = Axes(
            x_range=[0, 170, 20],
            y_range=[0, 1.3, 0.2],
            x_length=12,
            y_length=5.5,
            axis_config={"include_numbers": False, "stroke_width": 2},
            tips=False,
        ).move_to(DOWN * 0.5)

        x_label = Text("Atomic Number (Z)", font_size=18)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text("Relative Energy", font_size=18).rotate(PI / 2)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3)

        z_ticks = VGroup()
        for z_val in [20, 40, 60, 80, 100, 120, 140, 160]:
            pt = axes.c2p(z_val, 0)
            tick = Line(pt + DOWN * 0.08, pt + UP * 0.08, stroke_width=1.5)
            num = Text(str(z_val), font_size=12)
            num.next_to(tick, DOWN, buff=0.1)
            z_ticks.add(VGroup(tick, num))

        self.play(Create(axes), Write(x_label), Write(y_label), FadeIn(z_ticks), run_time=1.5)
        self.wait(0.3)

        # Spin-orbit curve (rising): normalized so it = 1.0 at Z=80
        norm_so = 80**4
        so_curve = axes.plot(
            lambda z: max(0.01, min(1.3, (z**4) / norm_so)),
            x_range=[5, 160],
            color=BLUE,
            stroke_width=3,
        )
        so_label = Text("Spin-Orbit Splitting", font_size=16, color=BLUE)
        so_label.move_to(axes.c2p(130, 1.15))

        # Subshell gap curve (falling): normalized so it = 1.0 at Z=80
        norm_gap = 80**(-1 / 3)
        gap_curve = axes.plot(
            lambda z: max(0.01, min(1.3, (z ** (-1 / 3)) / norm_gap)),
            x_range=[5, 160],
            color=RED,
            stroke_width=3,
        )
        gap_label = Text("Subshell Energy Gap", font_size=16, color=RED)
        gap_label.move_to(axes.c2p(130, 0.55))

        self.play(Create(so_curve), Write(so_label), run_time=2.0)
        self.play(Create(gap_curve), Write(gap_label), run_time=2.0)
        self.wait(0.5)

        # Mark the crossover at Z~80
        cross_pt = axes.c2p(80, 1.0)
        cross_dot = Dot(cross_pt, radius=0.12, color=GOLD).set_z_index(2)
        cross_flash = Flash(cross_pt, color=GOLD, line_length=0.3, flash_radius=0.5)
        vert_line = DashedLine(
            axes.c2p(80, 0), axes.c2p(80, 1.0),
            dash_length=0.1, color=GOLD, stroke_width=2,
        )
        au_label = Text("Au (Gold)", font_size=20, color=GOLD, weight=BOLD)
        au_label.next_to(vert_line, DOWN, buff=0.15)

        self.play(
            FadeIn(cross_dot), cross_flash,
            Create(vert_line), Write(au_label),
            run_time=1.5,
        )
        self.wait(0.5)

        # Annotate regions
        below_bracket = Brace(
            Line(axes.c2p(5, -0.3), axes.c2p(78, -0.3)),
            DOWN, buff=0.05, color=GREEN,
        )
        below_text = Text("Madelung rule holds\nSpiral works", font_size=14, color=GREEN)
        below_text.next_to(below_bracket, DOWN, buff=0.1)
        safe_position(below_text)

        above_bracket = Brace(
            Line(axes.c2p(82, -0.3), axes.c2p(160, -0.3)),
            DOWN, buff=0.05, color=RED_C,
        )
        above_text = Text("Periodic law dissolves\nSpiral breaks", font_size=14, color=RED_C)
        above_text.next_to(above_bracket, DOWN, buff=0.1)
        safe_position(above_text)

        self.play(
            FadeIn(below_bracket), Write(below_text),
            FadeIn(above_bracket), Write(above_text),
            run_time=1.5,
        )
        self.wait(1.0)

        # Ratio annotation
        ratio_eq = MathTex(
            r"\mathcal{D}(Z) = \frac{E_{\text{SO}}}{\Delta E_{\text{subshell}}}",
            font_size=32, color=YELLOW,
        )
        ratio_eq.move_to(UP * 2.8 + RIGHT * 4.5)
        safe_position(ratio_eq)

        ratio_desc = Text(
            "When D > 1, group identity\nloses physical meaning.",
            font_size=16, color=YELLOW,
        )
        ratio_desc.next_to(ratio_eq, DOWN, buff=0.25)
        safe_position(ratio_desc)

        self.play(Write(ratio_eq), Write(ratio_desc), run_time=1.5)
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.2)
        self.wait(0.3)


# ============================================================================
# SCENE 4: THE DISSOLUTION
# ============================================================================
class Scene4_Dissolution(Scene):
    def construct(self):
        title = Text("The Periodic Law Melts", font_size=44, weight=BOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=1.0)

        # Build spiral with all 118 elements as dots
        spiral_center = DOWN * 0.3
        dots = VGroup()
        labels = VGroup()

        for sym, z, period, group, block in ELEMENTS:
            pos = get_spiral_pos(z, center=spiral_center)
            dot = Dot(pos, radius=0.06, color=z_to_color(z))
            dots.add(dot)

        spiral_curve = ParametricFunction(
            lambda t: get_spiral_pos(t, center=spiral_center),
            t_range=[1, 118],
            color=WHITE,
            stroke_width=1.5,
            stroke_opacity=0.5,
        )

        # Mark gold
        au_pos = get_spiral_pos(79, center=spiral_center)
        au_marker = Dot(au_pos, radius=0.12, color=GOLD).set_z_index(3)
        au_label = Text("Au", font_size=14, color=GOLD, weight=BOLD)
        au_label.next_to(au_marker, UR, buff=0.08)

        self.play(
            Create(spiral_curve),
            FadeIn(dots, lag_ratio=0.005),
            run_time=2.0,
        )
        self.play(FadeIn(au_marker), Write(au_label), run_time=0.8)
        self.wait(0.5)

        # Phase 1: Actinides flicker (Z=89-103)
        flicker_text = Text(
            "Actinides (Z = 89-103): group assignments already ambiguous",
            font_size=18, color=ORANGE,
        )
        flicker_text.move_to(DOWN * 3.5)
        safe_position(flicker_text)
        self.play(Write(flicker_text), run_time=1.0)

        actinide_dots = VGroup(*[dots[i] for i, (_, z, _, _, _) in enumerate(ELEMENTS) if 89 <= z <= 103])
        for _ in range(3):
            self.play(
                actinide_dots.animate.set_opacity(0.2), run_time=0.3,
            )
            self.play(
                actinide_dots.animate.set_opacity(1.0), run_time=0.3,
            )
        self.wait(0.5)
        self.play(FadeOut(flicker_text), run_time=0.5)

        # Phase 2: Extend spiral into Z=119-160 with dissolution
        extend_text = Text(
            "Extending into Period 8...",
            font_size=20, color=YELLOW,
        )
        extend_text.move_to(DOWN * 3.5)
        safe_position(extend_text)
        self.play(Write(extend_text), run_time=0.8)

        # Add superheavy dots that jitter
        superheavy_dots = VGroup()
        ghost_dots = VGroup()
        d_labels = VGroup()

        for z in range(119, 161):
            pos = get_spiral_pos(z, center=spiral_center)
            dot = Dot(pos, radius=0.06, color=z_to_color(min(z, 118)))
            dot.set_opacity(0.6)
            superheavy_dots.add(dot)

            # Dissolution index label for milestones
            if z in [120, 130, 140, 150, 160]:
                d_val = (z / 80) ** (10 / 3)
                d_lbl = Text(f"D={d_val:.0f}", font_size=10, color=RED_B)
                d_lbl.move_to(pos + UP * 0.25)
                d_labels.add(d_lbl)

            # Ghost copies at competing positions for Z > 130
            if z > 130:
                offset_angle = 0.4 * np.sin(z * 0.7)
                ghost_pos = get_spiral_pos(z + offset_angle * 5, center=spiral_center)
                ghost = Dot(ghost_pos, radius=0.05, color=z_to_color(min(z, 118)))
                ghost.set_opacity(0.25)
                ghost_dots.add(ghost)

        # Extend the spiral curve
        extended_curve = ParametricFunction(
            lambda t: get_spiral_pos(t, center=spiral_center),
            t_range=[118, 160],
            color=WHITE,
            stroke_width=1.0,
            stroke_opacity=0.25,
        )

        self.play(
            Create(extended_curve),
            FadeIn(superheavy_dots, lag_ratio=0.02),
            FadeIn(d_labels, lag_ratio=0.1),
            run_time=2.5,
        )
        self.play(FadeIn(ghost_dots, lag_ratio=0.02), run_time=1.0)
        self.wait(0.5)

        self.play(FadeOut(extend_text), run_time=0.5)

        # Phase 3: Make superheavy dots jitter with updater
        jitter_text = Text(
            "Elements refuse to stay in one group position.",
            font_size=20, color=RED_C,
        )
        jitter_text.move_to(DOWN * 3.5)
        safe_position(jitter_text)
        self.play(Write(jitter_text), run_time=0.8)

        time_tracker = ValueTracker(0)

        def jitter_updater(mob, dt):
            t = time_tracker.get_value()
            for i, dot in enumerate(mob):
                z = 119 + i
                base_pos = get_spiral_pos(z, center=spiral_center)
                jitter_scale = min(0.15, 0.005 * (z - 118))
                offset = np.array([
                    jitter_scale * np.sin(t * 3 + z * 0.5),
                    jitter_scale * np.cos(t * 4 + z * 0.7),
                    0,
                ])
                dot.move_to(base_pos + offset)

        superheavy_dots.add_updater(jitter_updater)
        self.play(time_tracker.animate.set_value(6), run_time=4.0, rate_func=linear)
        superheavy_dots.remove_updater(jitter_updater)
        self.wait(0.3)

        self.play(FadeOut(jitter_text), run_time=0.5)

        # Phase 4: Fracture the spiral curve
        fracture_text = Text(
            "The periodic law is not eternal. It melts.",
            font_size=24, color=RED, weight=BOLD,
        )
        fracture_text.move_to(DOWN * 3.5)
        safe_position(fracture_text)

        # Fade and fragment the extended region
        self.play(
            extended_curve.animate.set_stroke(opacity=0.05),
            superheavy_dots.animate.set_opacity(0.15),
            ghost_dots.animate.set_opacity(0.08),
            Write(fracture_text),
            run_time=2.0,
        )
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.3)


# ============================================================================
# SCENE 5: WHAT WE ACTUALLY KNOW
# ============================================================================
class Scene5_WhatWeKnow(Scene):
    def construct(self):
        title = Text("Two Regimes, One Table", font_size=44, weight=BOLD)
        title.move_to(UP * 3.8)
        self.play(Write(title), run_time=1.0)

        # LEFT: intact spiral for Z=1 to 80
        left_title = Text("Hydrogen to Gold", font_size=22, color=GREEN, weight=BOLD)
        left_title.move_to(UP * 2.8 + LEFT * 4.2)

        left_center = LEFT * 4.2 + DOWN * 0.5
        left_dots = VGroup()
        for sym, z, period, group, block in ELEMENTS:
            if z > 80:
                continue
            pos = get_spiral_pos(z, center=left_center, base_r=0.3, growth=0.018)
            dot = Dot(pos, radius=0.05, color=z_to_color(z))
            left_dots.add(dot)

        left_curve = ParametricFunction(
            lambda t: get_spiral_pos(t, center=left_center, base_r=0.3, growth=0.018),
            t_range=[1, 80],
            color=GREEN,
            stroke_width=2,
            stroke_opacity=0.6,
        )

        left_caption = Text(
            "Domain of validity:\nelectrons behave predictably",
            font_size=15, color=GREEN,
        )
        left_caption.move_to(left_center + DOWN * 2.8)
        safe_position(left_caption)

        # RIGHT: branching tree for Z > 80
        right_title = Text("Beyond Gold", font_size=22, color=RED_C, weight=BOLD)
        right_title.move_to(UP * 2.8 + RIGHT * 4.2)

        right_center = RIGHT * 4.2 + DOWN * 0.5
        tree_elements = VGroup()
        tree_lines = VGroup()

        # Build a small branching tree showing elements splitting
        branch_data = [
            ("Au\n79", 0, 0),
            ("Hg\n80", -0.7, -0.8),
            ("Tl\n81", 0.7, -0.8),
            ("Pb\n82", -1.2, -1.6),
            ("Bi\n83", -0.2, -1.6),
            ("Po\n84", 0.5, -1.6),
            ("Rn\n86", 1.2, -1.6),
            ("Fr\n87", -1.5, -2.4),
            ("Ra\n88", -0.5, -2.4),
            ("Ac\n89", 0.5, -2.4),
            ("Th\n90", 1.5, -2.4),
            ("?", -1.8, -3.2),
            ("?", -0.8, -3.2),
            ("?", 0.2, -3.2),
            ("?", 0.8, -3.2),
            ("?", 1.5, -3.2),
            ("?", 2.0, -3.2),
        ]

        nodes = {}
        for label_text, dx, dy in branch_data:
            pos = right_center + RIGHT * dx + UP * dy
            if label_text == "?":
                dot = Dot(pos, radius=0.08, color=RED_C, fill_opacity=0.3)
                lbl = Text("?", font_size=12, color=RED_C)
            else:
                z_val = int(label_text.split("\n")[1]) if "\n" in label_text else 0
                dot = Dot(pos, radius=0.08, color=z_to_color(min(z_val, 118)) if z_val else GOLD)
                lbl = Text(label_text, font_size=10, line_spacing=0.6)
            lbl.next_to(dot, RIGHT, buff=0.06)
            group = VGroup(dot, lbl)
            tree_elements.add(group)
            nodes[label_text] = pos

        # Connect some branches
        connections = [
            (0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6),
            (3, 7), (4, 8), (5, 9), (6, 10),
            (7, 11), (8, 12), (9, 13), (9, 14), (10, 15), (10, 16),
        ]
        for a, b in connections:
            pa = branch_data[a]
            pb = branch_data[b]
            start = right_center + RIGHT * pa[1] + UP * pa[2]
            end = right_center + RIGHT * pb[1] + UP * pb[2]
            line = Line(start, end, stroke_width=1.0, stroke_opacity=0.4, color=RED_C)
            tree_lines.add(line)

        right_caption = Text(
            "Chemistry without a map:\ngroup identity depends on\noxidation state",
            font_size=15, color=RED_C,
        )
        right_caption.move_to(right_center + DOWN * 3.2)
        safe_position(right_caption)

        # Dividing line
        divider = DashedLine(UP * 3.2, DOWN * 4.0, dash_length=0.15, color=GOLD, stroke_width=2)

        # Animate left side
        self.play(
            Write(left_title),
            Create(left_curve),
            FadeIn(left_dots, lag_ratio=0.01),
            run_time=2.0,
        )
        self.play(Write(left_caption), run_time=0.8)

        # Divider
        self.play(Create(divider), run_time=0.8)

        # Animate right side
        self.play(
            Write(right_title),
            FadeIn(tree_lines, lag_ratio=0.03),
            FadeIn(tree_elements, lag_ratio=0.03),
            run_time=2.0,
        )
        self.play(Write(right_caption), run_time=0.8)
        self.wait(1.5)

        # Final card
        all_content = VGroup(
            left_title, left_curve, left_dots, left_caption,
            right_title, tree_lines, tree_elements, right_caption,
            divider,
        )
        self.play(all_content.animate.set_opacity(0.15), run_time=1.5)

        final_text = Text(
            "The periodic table is not a map of all matter.\n"
            "It is a map of the regime where electrons\n"
            "behave predictably.",
            font_size=28,
            color=WHITE,
            weight=BOLD,
            line_spacing=1.3,
        )
        final_text.move_to(ORIGIN)

        self.play(Write(final_text), run_time=2.5)
        self.wait(3.5)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=2.0,
        )
        self.wait(0.5)

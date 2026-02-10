from manim import *
from manim.constants import PI
from manim import (
    LEFT,
    RIGHT,
    UP,
    DOWN,
    GREEN,
    RED,
    YELLOW,
    BLUE_E,
    WHITE,
    BLUE,
    Sphere,
    ParametricFunction,
    Text,
    Write,
    Create,
    Transform,
    ValueTracker,
    Dot,
    Line,
    MathTex,
    VGroup,
    RoundedRectangle,
    Arrow,
    DashedLine,
)
import numpy as np

# Follow custom config: 1440p, frame dimensions, non-clipped positioning
config.pixel_height = 1440
config.pixel_width = 2560
config.frame_height = 8.0  # Adjusted for 1440p aspect ratio
config.frame_width = 14.222  # 2560/180 ratio for safe bounds


class PoleDriftVideo(Scene):
    def construct(self):
        # Scene 1: Intro globe with wobble (adapted from oscillation patterns)
        globe = Sphere(radius=3, resolution=(32, 32)).set_color(BLUE_E)
        wobble_path = ParametricFunction(
            lambda t: np.array(
                [0.2 * np.cos(2 * PI * t / 433), 0.2 * np.sin(2 * PI * t / 433), 0]
            ),
            t_range=[0, 433],
            color=YELLOW,
        ).scale(0.001)  # mas scale simplified
        self.play(Create(globe), run_time=2)
        self.play(Create(wobble_path), run_time=3)
        title = Text("Earth's Polar Motion", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Scene 2: Historical wobble graph (from sinusoidal curve snippet)
        ax = Axes(
            x_range=[0, 1000, 100],
            y_range=[-0.2, 0.2, 0.1],
            axis_config={"include_tip": False},
        ).shift(DOWN * 2)
        sine = ax.plot(lambda x: 0.2 * np.sin(2 * PI * x / 433), color=BLUE)
        self.play(Create(ax), Create(sine), run_time=3)
        label = Text(
            "Chandler Wobble: ~433 days, 200 mas amplitude", font_size=32
        ).next_to(ax, UP)
        self.play(Write(label))
        self.wait(2)

        # Scene 3: Transition to drift (adapted from drifting segments)
        drift_line = Line(
            ax.c2p(0, 0), ax.c2p(13, 0.0165), color=RED
        )  # ~16.5 mas over 13 days
        self.play(Transform(sine, drift_line), run_time=3)
        self.wait(1)

        # Scene 4: 13-day drift animation (from time series graph)
        drift_tracker = ValueTracker(0)
        drift_dot = always_redraw(
            lambda: Dot(
                ax.c2p(drift_tracker.get_value(), 1.27e-3 * drift_tracker.get_value()),
                color=RED,
            )
        )
        self.add(drift_dot)
        self.play(drift_tracker.animate.set_value(13), run_time=4, rate_func=linear)
        self.wait(1)

        # Scene 5: Ratio calculation (animated equation)
        eq = (
            MathTex(r"\frac{13 \times 1.27}{200} \approx 0.085 = 8.5\%")
            .scale(1.5)
            .shift(UP * 2)
        )
        self.play(Write(eq), run_time=3)
        bar = Rectangle(
            width=0.085 * 10, height=0.5, fill_color=GREEN, fill_opacity=0.8
        ).next_to(eq, DOWN)
        self.play(GrowFromEdge(bar, LEFT), run_time=2)
        self.wait(2)

        # Scene 6: Implications (adapted from flowchart and phase portrait)
        flowchart = (
            VGroup(
                RoundedRectangle().set_fill(BLUE, 0.5).add(Text("Oscillatory Motion")),
                Arrow(DOWN),
                RoundedRectangle().set_fill(RED, 0.5).add(Text("Subtle Drifts")),
                Arrow(DOWN),
                RoundedRectangle()
                .set_fill(YELLOW, 0.5)
                .add(Text("GPS & Climate Impacts")),
            )
            .arrange(DOWN, buff=0.5)
            .shift(LEFT * 4)
        )
        self.play(Create(flowchart), run_time=3)
        self.wait(3)

        # Scene 7: Unknown endpoint (dotted line extension)
        unknown_path = DashedLine(
            drift_line.get_end(), drift_line.get_end() + RIGHT * 5, color=WHITE
        )
        self.play(Create(unknown_path), run_time=2)
        self.wait(1)

        # Scene 8: Conclusion recap
        recap_text = Text("Monitor Earth's Dynamic Poles", font_size=36).to_edge(UP)
        self.play(Transform(title, recap_text))
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(1)

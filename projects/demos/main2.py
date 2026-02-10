from manim import *
import numpy as np

class PythagoreanTheoremScene(Scene):
    def construct(self):
        a = 2
        b = 1.5
        c = (a**2 + b**2) ** 0.5

        A = ORIGIN
        B = A + RIGHT * a
        C = A + UP * b

        triangle = Polygon(A, B, C, color=WHITE)

        right_angle = Square(
            side_length=0.15,
            color=WHITE,
            fill_opacity=1
        ).move_to(A + 0.1 * RIGHT + 0.1 * UP)

        label_a = MathTex("a").next_to(Line(A, B), DOWN, buff=0.1)
        label_b = MathTex("b").next_to(Line(A, C), LEFT, buff=0.1)
        label_c = MathTex("c").next_to(Line(B, C), UP + RIGHT * 0.1)

        square_a = Polygon(
            A,
            B,
            B + UP * a,
            A + UP * a,
            color=BLUE,
            ).set_fill(BLUE, opacity=0.6)

        square_b = Polygon(
            A,
            C,
            C + LEFT * b,
            A + LEFT * b,
            color=GREEN,
            ).set_fill(GREEN, opacity=0.6)

        BC_vec = C - B
        perp_vec = np.array([-BC_vec[1], BC_vec[0], 0])
        perp_vec = perp_vec / np.linalg.norm(perp_vec) * c

        square_c = Polygon(
            B,
            C,
            C + perp_vec,
            B + perp_vec,
            color=RED,
            ).set_fill(RED, opacity=0.6)

        equation = MathTex("a^2", "+", "b^2", "=", "c^2")

        figure = VGroup(
            triangle,
            right_angle,
            label_a,
            label_b,
            label_c,
            square_a,
            square_b,
            square_c,
        )

        # Make the whole construction clearly smaller and centered
        figure.scale(0.35)
        figure.move_to(ORIGIN)

        equation.next_to(figure, UP, buff=0.5)

        self.play(Create(triangle), FadeIn(right_angle))
        self.play(Write(label_a), Write(label_b), Write(label_c))
        self.wait(0.3)

        self.play(Create(square_a))
        self.wait(0.3)

        self.play(Create(square_b))
        self.wait(0.3)

        self.play(Create(square_c))
        self.wait(0.3)

        self.play(Write(equation))
        self.wait(1)

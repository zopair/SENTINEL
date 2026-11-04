from manim import *
import numpy as np


BG = "#0b0c10"
GOLD = "#d4af37"
PALE = "#f2e6c8"
MUTED = "#a7a9b0"
TEAL = "#56d6c8"
RED = "#d96b63"


class SentinelExplainer(Scene):
    """Evidence-grounded 16:9 SENTINEL research explainer."""

    def construct(self):
        self.camera.background_color = BG
        self.opening()
        self.labyrinth()
        self.evidence()
        self.bounds_and_lab()
        self.closing()

    def heading(self, eyebrow, title, subtitle=None):
        top = Text(eyebrow.upper(), font_size=18, color=GOLD, weight=MEDIUM)
        top.to_edge(UP, buff=0.42)
        main = Text(title, font_size=38, color=PALE, weight=SEMIBOLD)
        main.next_to(top, DOWN, buff=0.18)
        group = VGroup(top, main)
        if subtitle:
            sub = Text(subtitle, font_size=19, color=MUTED)
            sub.next_to(main, DOWN, buff=0.16)
            group.add(sub)
        self.play(FadeIn(group, shift=UP * 0.18), run_time=0.8)
        return group

    def opening(self):
        kicker = Text("OPEN-SOURCE CYBER DECEPTION RESEARCH", font_size=18, color=GOLD)
        title = Text("SENTINEL", font_size=76, color=PALE, weight=SEMIBOLD)
        line = Line(LEFT * 2.5, RIGHT * 2.5, color=GOLD, stroke_width=2)
        claim = Text("Don't just detect the path.", font_size=30, color=WHITE)
        claim2 = Text("Redesign the path.", font_size=30, color=GOLD)
        block = VGroup(kicker, title, line, claim, claim2).arrange(DOWN, buff=0.28)
        self.play(FadeIn(kicker, shift=UP), run_time=0.7)
        self.play(Write(title), run_time=1.2)
        self.play(Create(line), FadeIn(claim), run_time=0.8)
        self.play(FadeIn(claim2, shift=UP * 0.15), run_time=0.7)
        self.wait(1.1)
        self.play(FadeOut(block), run_time=0.6)

    def labyrinth(self):
        header = self.heading(
            "01 / Controlled synthetic environment",
            "A decoy visit is only the beginning",
            "Study how an explorer allocates a finite interaction budget."
        )
        coords = [
            (-4.8, -1.0), (-3.0, 0.8), (-1.2, -1.0), (0.5, 0.9),
            (2.2, -0.8), (4.0, 0.8), (5.2, -1.0), (-3.8, -2.2),
            (-0.2, -2.2), (3.0, -2.2)
        ]
        pts = [np.array([x, y, 0]) for x, y in coords]
        edges = [(0,1),(0,7),(1,2),(1,3),(2,3),(2,8),(3,4),(3,5),
                 (4,5),(4,8),(4,9),(5,6),(6,9),(7,8),(8,9)]
        graph = VGroup()
        for a, b in edges:
            graph.add(Line(pts[a], pts[b], color=GOLD, stroke_width=2, stroke_opacity=0.42))
        nodes = VGroup(*[
            Circle(radius=0.12, stroke_color=GOLD, stroke_width=2,
                   fill_color=BG, fill_opacity=1).move_to(p)
            for p in pts
        ])
        root = Circle(radius=0.17, color=TEAL, fill_color=TEAL, fill_opacity=0.22).move_to(pts[0])
        self.play(FadeOut(header), run_time=0.3)
        self.play(LaggedStart(*[Create(e) for e in graph], lag_ratio=0.035), run_time=1.8)
        self.play(LaggedStart(*[FadeIn(n, scale=0.5) for n in nodes], lag_ratio=0.07), run_time=1.2)
        self.play(Indicate(root, color=TEAL), run_time=0.5)
        labels = VGroup(
            Text("SYNTHETIC GRAPH", font_size=18, color=GOLD),
            Text("INERT DECOY NODES", font_size=16, color=MUTED),
            Text("NO PRODUCTION ASSETS", font_size=16, color=TEAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.5)
        self.play(FadeIn(labels), run_time=0.5)
        self.wait(0.7)
        self.play(FadeOut(VGroup(graph, nodes, root, labels)), run_time=0.6)

    def evidence(self):
        header = self.heading(
            "02 / Matched multi-policy experiments",
            "Six policies. The same graph.",
            "One pre-generated topology per seed and configuration."
        )
        names = ["STATIC DECOY", "RANDOM WALK", "GREEDY", "BFS", "DFS", "ADAPTIVE"]
        colors = [MUTED, MUTED, MUTED, MUTED, MUTED, GOLD]
        rows = VGroup()
        for i, (name, color) in enumerate(zip(names, colors)):
            y = 1.15 - i * 0.62
            track = RoundedRectangle(width=8.8, height=0.42, corner_radius=0.12,
                                     stroke_color="#34343a", fill_color="#14161c",
                                     fill_opacity=1).move_to([0, y, 0])
            label = Text(name, font_size=17, color=color).move_to(track.get_left() + RIGHT * 1.25)
            path = Line(track.get_left() + RIGHT * 2.5, track.get_right() - RIGHT * 0.35,
                        color=color, stroke_width=3)
            dot = Dot(path.get_start(), radius=0.055, color=color)
            rows.add(VGroup(track, label, path, dot))
        self.play(FadeOut(header), run_time=0.25)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.13),
                  run_time=1.4)
        self.play(*[dot.animate.move_to(path.get_end()) for _, _, path, dot in rows],
                  run_time=1.8, rate_func=smooth)
        foot = Text("MATCHED SEEDS  •  MATCHED TOPOLOGY  •  DECLARED BUDGETS",
                    font_size=17, color=TEAL).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(foot), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(VGroup(rows, foot)), run_time=0.5)


    def statistical_evidence(self):
        header = self.heading(
            "03 / Statistical evaluation",
            "From impressions to paired evidence",
            "Each seed contributes a matched difference—not an isolated anecdote."
        )
        axis = Line(LEFT * 4.2, RIGHT * 4.2, color="#555963", stroke_width=2).shift(DOWN * 0.55)
        zero = Line(DOWN * 0.12, UP * 0.12, color=TEAL, stroke_width=2).move_to(axis.get_center())
        rows = VGroup()
        offsets = [-0.72, -0.32, 0.18, 0.48, -0.12]
        for i, offset in enumerate(offsets):
            y = 0.95 - i * 0.48
            left = Dot([-2.8, y, 0], color=MUTED, radius=0.055)
            right = Dot([offset * 2.0, y, 0], color=GOLD, radius=0.065)
            pair = Line(left.get_center(), right.get_center(), color=GOLD, stroke_width=2)
            rows.add(VGroup(pair, left, right))
        labels = VGroup(
            Text("MATCHED PER-SEED DIFFERENCES", font_size=17, color=GOLD),
            Text("DESCRIPTIVE 95% CONFIDENCE INTERVAL", font_size=17, color=PALE),
            Text("10,000-DRAW SIGN-FLIP TEST  •  HOLM ADJUSTMENT", font_size=16, color=TEAL),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.32)
        note = Text("SCHEMATIC EXPLANATION — NOT EXPERIMENTAL RESULT DATA",
                    font_size=13, color=MUTED).to_edge(UP, buff=0.35)
        self.play(FadeOut(header), run_time=0.25)
        self.play(Create(axis), Create(zero), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.12) for r in rows], lag_ratio=0.16),
                  run_time=1.1)
        self.play(FadeIn(labels), FadeIn(note), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(VGroup(axis, zero, rows, labels, note)), run_time=0.6)

    def bounds_and_lab(self):
        header = self.heading(
            "03 / Evidence and engineering discipline",
            "Make every claim inspectable",
            "Telemetry, statistical uncertainty, and explicit resource ceilings."
        )
        cards = VGroup()
        stats = [
            ("4,096", "MAX NODES"),
            ("64", "MAX DEPTH"),
            ("4,096", "MAX STEPS"),
            ("1–8", "BRANCHING"),
        ]
        for value, label in stats:
            rect = RoundedRectangle(width=2.45, height=1.2, corner_radius=0.12,
                                    stroke_color=GOLD, fill_color="#15171d", fill_opacity=1)
            val = Text(value, font_size=34, color=PALE, weight=SEMIBOLD)
            lab = Text(label, font_size=13, color=GOLD)
            VGroup(val, lab).arrange(DOWN, buff=0.08).move_to(rect)
            cards.add(VGroup(rect, val, lab))
        cards.arrange(RIGHT, buff=0.18).move_to(UP * 0.25)
        schema = Text("JSONL SCHEMA 2.0", font_size=20, color=TEAL)
        ci = Text("Paired differences  •  Descriptive 95% CI", font_size=18, color=PALE)
        test = Text("10,000-draw sign-flip test  •  Holm adjustment", font_size=18, color=PALE)
        details = VGroup(schema, ci, test).arrange(DOWN, buff=0.16).next_to(cards, DOWN, buff=0.48)
        self.play(FadeOut(header), run_time=0.25)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.12),
                  run_time=1.1)
        self.play(FadeIn(details), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(VGroup(cards, details)), run_time=0.5)

        local = Text("LOCAL RESEARCH LAB", font_size=22, color=GOLD)
        address = Text("http://127.0.0.1:8765", font_size=29, color=TEAL)
        panel = RoundedRectangle(width=8.5, height=2.5, corner_radius=0.18,
                                 stroke_color=GOLD, fill_color="#12151b", fill_opacity=1)
        caption = Text("Bilingual UI  •  Local JSONL  •  Real Python engine mode",
                       font_size=17, color=PALE)
        VGroup(local, address, caption).arrange(DOWN, buff=0.28).move_to(panel)
        self.play(FadeIn(panel), FadeIn(local), Write(address), FadeIn(caption), run_time=1.3)
        self.wait(1.0)
        self.play(FadeOut(VGroup(panel, local, address, caption)), run_time=0.5)

    def closing(self):
        title = Text("SENTINEL", font_size=68, color=PALE, weight=SEMIBOLD)
        line1 = Text("Don't just detect the path.", font_size=27, color=WHITE)
        line2 = Text("Redesign the path.", font_size=31, color=GOLD)
        footer = Text("OPEN-SOURCE CYBER DECEPTION RESEARCH FRAMEWORK",
                      font_size=15, color=MUTED)
        group = VGroup(title, line1, line2, footer).arrange(DOWN, buff=0.25)
        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(line1), FadeIn(line2, shift=UP * 0.12), run_time=0.9)
        self.play(FadeIn(footer), run_time=0.6)
        self.wait(1.8)

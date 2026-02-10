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


class ClusteringEmergence(Scene):
    def construct(self):
        # Parameters
        rows = 7
        cols = 10
        cell_size = 0.5
        algo_colors = [RED, BLUE, GREEN]  # 3 algotypes
        algo_names = ["Algotype A", "Algotype B", "Algotype C"]

        # Title
        title = Text(
            "Clustering Emergence",
            font_size=44,
            weight=BOLD
        ).to_edge(UP, buff=0.4)

        subtitle = Text(
            "Mobile cells with immutable algotypes self-organize into clusters",
            font_size=24,
            color=GRAY_B
        ).next_to(title, DOWN, buff=0.2)

        self.play(Write(title), FadeIn(subtitle, shift=DOWN))
        self.wait(0.5)

        # Legend
        legend_entries = VGroup()
        for i, (name, color) in enumerate(zip(algo_names, algo_colors)):
            dot = Square(side_length=0.35, fill_opacity=1.0, fill_color=color, stroke_width=0)
            label = Text(name, font_size=20).next_to(dot, RIGHT, buff=0.15)
            item = VGroup(dot, label)
            legend_entries.add(item)

        legend_entries.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend_box = SurroundingRectangle(
            legend_entries,
            corner_radius=0.15,
            buff=0.25,
            color=GRAY_B
        )
        legend = VGroup(legend_box, legend_entries)
        legend.to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)

        self.play(FadeIn(legend, shift=RIGHT))
        self.wait(0.5)

        # Create grid of cells with random algotypes
        cells = VGroup()
        algo_types = {}

        x_start = -5.0
        y_start = 2.5
        x_step = cell_size * 1.2
        y_step = cell_size * 1.2

        for r in range(rows):
            for c in range(cols):
                algo_index = np.random.randint(0, len(algo_colors))
                color = algo_colors[algo_index]

                cell = Square(
                    side_length=cell_size,
                    stroke_width=0.5,
                    stroke_color=GRAY_D,
                    fill_color=color,
                    fill_opacity=0.95,
                )

                x = x_start + c * x_step
                y = y_start - r * y_step
                cell.move_to(np.array([x, y, 0.0]))

                # Store algotype index as immutable "identity"
                cell.algo_index = algo_index
                cells.add(cell)

        grid_group = VGroup(cells)
        self.play(FadeIn(grid_group, lag_ratio=0.02))
        self.wait(1.0)

        # Helper to get neighbors for a cell index in the flat list
        def neighbor_indices(index):
            r = index // cols
            c = index % cols
            neighbors = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbors.append(nr * cols + nc)
            return neighbors

        # Simple local-energy function: count neighbors with different algotype
        def local_discomfort(idx):
            cell = cells[idx]
            own_type = cell.algo_index
            diff_count = 0
            for n_idx in neighbor_indices(idx):
                if cells[n_idx].algo_index != own_type:
                    diff_count += 1
            return diff_count

        # "Sorting" iterations: cells swap positions if it reduces local discomfort
        steps = 40
        animations_per_step = 12  # how many swaps per iteration

        for step in range(steps):
            anims = []
            indices = list(range(len(cells)))
            np.random.shuffle(indices)

            swaps_done = 0
            for idx in indices:
                if swaps_done >= animations_per_step:
                    break

                current_discomfort = local_discomfort(idx)
                if current_discomfort == 0:
                    continue

                # Try swapping with a random neighbor
                nbs = neighbor_indices(idx)
                if not nbs:
                    continue
                n_idx = np.random.choice(nbs)

                # Compute discomfort if swapped
                # Perform a temporary position swap in memory only
                cells[idx], cells[n_idx] = cells[n_idx], cells[idx]
                new_discomfort_idx = local_discomfort(n_idx)
                new_discomfort_n = local_discomfort(idx)
                total_new = new_discomfort_idx + new_discomfort_n

                # Undo temporary swap
                cells[idx], cells[n_idx] = cells[n_idx], cells[idx]

                # Current total discomfort of the two cells
                total_old = current_discomfort + local_discomfort(n_idx)

                if total_new < total_old:
                    # Accept swap: entire objects exchange positions (algotype moves with cell)
                    cell_a = cells[idx]
                    cell_b = cells[n_idx]

                    pos_a = cell_a.get_center()
                    pos_b = cell_b.get_center()

                    # Animate the swap
                    anims.append(cell_a.animate.move_to(pos_b))
                    anims.append(cell_b.animate.move_to(pos_a))

                    # Swap in the VGroup
                    cells[idx], cells[n_idx] = cells[n_idx], cells[idx]
                    swaps_done += 1

            if anims:
                self.play(*anims, run_time=0.4, rate_func=linear)

        # Final emphasize clusters
        highlight = SurroundingRectangle(
            cells,
            buff=0.4,
            color=YELLOW,
            stroke_width=4
        )
        final_label = Text(
            "Emergent clusters by algotype",
            font_size=30,
            color=YELLOW
        ).next_to(highlight, DOWN, buff=0.3)

        self.play(Create(highlight))
        self.play(Write(final_label))
        self.wait(2)

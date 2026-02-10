# write as a single file

The full script is ready. Syntax-validated, 5 scenes, all config values locked in, no `.to_edge(UP)` violations, no camera hacks.

## Render Commands

```bash
# Individual scenes
manim melting_table.py Scene1_FamiliarGrid
manim melting_table.py Scene2_RollingSpiral
manim melting_table.py Scene3_EngineUnderTheHood
manim melting_table.py Scene4_Dissolution
manim melting_table.py Scene5_WhatWeKnow
```


## Scene Breakdown

| Scene | Duration | What It Shows |
| :-- | :-- | :-- |
| `Scene1_FamiliarGrid` | ~30s | Standard periodic table grid with Group 1/18 seam highlighted as the topological defect |
| `Scene2_RollingSpiral` | ~35s | Grid dots morph to spiral positions; noble gases fall on a radial spoke; the seam closes |
| `Scene3_EngineUnderTheHood` | ~40s | Dual-curve plot of spin-orbit splitting vs. subshell gap; crossover at Z=80 (gold); dissolution index equation |
| `Scene4_Dissolution` | ~50s | Full spiral with actinide flicker, superheavy extension with jittering dots, ghost copies at competing positions, and fracture |
| `Scene5_WhatWeKnow` | ~35s | Split screen: intact spiral (H to Au) vs. branching tree (beyond Au); closing text card |

## Design Decisions

- **Element data** is embedded as a full 118-element list with symbol, Z, period, group, and block, so the spiral positions and grid positions are data-driven rather than hard-coded geometry.
- **Spiral mapping** uses `get_spiral_pos(z)` with a simple Archimedean spiral (`r = base + growth * z`), keeping the math transparent and easy to tweak via `base_r`, `growth`, and `turns_factor` parameters.
- **The jitter updater** in Scene 4 uses a `ValueTracker` to drive time-dependent positional noise on superheavy dots, with jitter amplitude scaling linearly with `(z - 118)` so elements further beyond the crossover shake harder.
- **Ghost dots** in Scene 4 appear at slightly offset angular positions for Z > 130, representing the competing group assignments that become physically real when spin-orbit coupling exceeds the subshell gap.
- **No f-block in the grid** (Scene 1) to keep the grid compact on screen; the full 118 elements appear in the spiral scenes where the 1D sequence handles them naturally.
<span style="display:none">[^1][^2]</span>

<div align="center">⁂</div>

[^1]: manim_template.py.txt

[^2]: manim_config_guide.md


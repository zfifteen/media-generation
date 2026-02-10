# The Orthogonal Dimensions of *e* -- Complete Manim Script

## Overview

This is a single production-quality Manim Community Edition script containing **8 scenes** (1 title + 7 content scenes). Each scene runs for 15 seconds. The script follows the locked-in template configuration (frame_height=10, frame_width=17.78, 1440p resolution) and uses safe absolute positioning throughout.

## Scene Breakdown

| Scene | Class Name | Duration | Key Visual |
|-------|-----------|----------|------------|
| Title | `TitleScene` | 15s | Instant display (no fade-in), title + e digits + credit |
| 1 | `Scene1_FourShadows` | 15s | Central glowing *e* with four projection planes |
| 2 | `Scene2_SeriesCompression` | 15s | Terms dropping in, precision ruler climbing |
| 3 | `Scene3_CFStaircase` | 15s | Staircase + number line with fraction/decimal convergents |
| 4 | `Scene4_SplitScreen` | 15s | Split comparison, ratio exploding from 8x to 300B x |
| 5 | `Scene5_PhaseSeparation` | 15s | Two planes drifting apart, perpendicularity symbol |
| 6 | `Scene6_HigherDimensional` | 15s | Rotating assembly, polytope transformation |
| 7 | `Scene7_FinalSynthesis` | 15s | Polytope + axes lock in, final text holds (no fade to black) |

## Design Decisions

- **Fourth representation:** Pippenger's infinite product[^43]
- **CF convergents:** Displayed as both exact fractions and decimal approximations (e.g., 8/3 = 2.667)
- **Animation timing:** Mixed approach with smooth flow for related elements and brief pauses between conceptual shifts
- **Infinite product formula shown:** A stylized form of the Pippenger product notation
- **Continued fraction coefficients:** [2; 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, ...] with the characteristic (1, 1, 2k) triplet pattern[^43]

## Rendering Instructions

Render all scenes sequentially with:

```bash
manim euler_dimensions.py TitleScene
manim euler_dimensions.py Scene1_FourShadows
manim euler_dimensions.py Scene2_SeriesCompression
manim euler_dimensions.py Scene3_CFStaircase
manim euler_dimensions.py Scene4_SplitScreen
manim euler_dimensions.py Scene5_PhaseSeparation
manim euler_dimensions.py Scene6_HigherDimensional
manim euler_dimensions.py Scene7_FinalSynthesis
```

Or render all at once:

```bash
manim euler_dimensions.py -a
```

No quality flags needed -- resolution (2560x1440) is baked into the config block.

## Concatenation

After rendering, concatenate the output videos in order using ffmpeg:

```bash
ffmpeg -f concat -safe 0 -i filelist.txt -c copy euler_dimensions_full.mp4
```

Where `filelist.txt` contains:
```
file 'media/videos/euler_dimensions/1440p60/TitleScene.mp4'
file 'media/videos/euler_dimensions/1440p60/Scene1_FourShadows.mp4'
file 'media/videos/euler_dimensions/1440p60/Scene2_SeriesCompression.mp4'
file 'media/videos/euler_dimensions/1440p60/Scene3_CFStaircase.mp4'
file 'media/videos/euler_dimensions/1440p60/Scene4_SplitScreen.mp4'
file 'media/videos/euler_dimensions/1440p60/Scene5_PhaseSeparation.mp4'
file 'media/videos/euler_dimensions/1440p60/Scene6_HigherDimensional.mp4'
file 'media/videos/euler_dimensions/1440p60/Scene7_FinalSynthesis.mp4'
```

## The Script



## Technical Notes

- All text uses `safe_position()` to clamp content within the vertical safe zone (y: -4.0 to +4.0)
- No `.to_edge(UP)` calls for headers, only `.move_to(UP * 3.8)` absolute positioning
- VGroups used for composite elements to simplify transforms
- `RightAngle` in Scene 5 provides visual proof of orthogonality
- Scene 6 uses `Rotate()` on a VGroup assembly to simulate higher-dimensional rotation without ThreeDScene/camera manipulation (compatible with Manim CE 0.19.x)
- The `RegularPolygon(n=8)` octagon serves as a 2D projection metaphor for a 4D polytope
- Scene 4 uses `Flash()` for the dramatic ratio burst at tick 5
- Color scheme: Blue (series/positional), Green (CF/relational), Gold (e/shared identity), Maroon/Teal (limit/product)


---

## References

43. [List of representations of e - Wikipedia](https://en.wikipedia.org/wiki/List_of_representations_of_e) - Using calculus, e may also be represented as an infinite series, infinite product, or other types of...


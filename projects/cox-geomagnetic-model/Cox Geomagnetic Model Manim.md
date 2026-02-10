# Cox's Probabilistic Model for Geomagnetic Polarity Intervals -- Manim Scenes

## Overview

This script contains **7 self-contained Manim scenes** that progressively animate the key ideas in Cox's 1968 stochastic framework for geomagnetic reversals[^3][^8]. Each scene can be rendered independently or in sequence.

| Scene | Class Name | What It Shows |
|-------|-----------|---------------|
| 1 | `CoxModelTitle` | Title card with core equation and citation |
| 2 | `DipoleOscillation` | Sinusoidal dipole intensity with vulnerability windows, threshold, and random nondipole overlay |
| 3 | `BernoulliTrials` | 10 discrete dipole cycles as Bernoulli trials with reversal triggers |
| 4 | `GeometricDistribution` | Animated bar chart of \(P(K=k) = (1-p)^{k-1}p\) with mean line |
| 5 | `RikitakeDynamo` | Numerical solution of the Rikitake ODEs showing \(X(t)\) chaotic reversals |
| 6 | `RikitakePhasePortrait` | \(X\)-\(Y\) phase portrait revealing the two-lobed attractor |
| 7 | `CoxModelSummary` | Flowchart connecting dipole oscillation, nondipole noise, Bernoulli trigger, and geometric intervals |

## Render Commands

```bash
# Render a single scene
manim cox_geomagnetic_model.py CoxModelTitle

# Render all scenes
manim cox_geomagnetic_model.py CoxModelTitle DipoleOscillation BernoulliTrials GeometricDistribution RikitakeDynamo RikitakePhasePortrait CoxModelSummary
```

Quality flags are unnecessary since the config block bakes in 1440p/2560x1440 resolution.

## Scene-by-Scene Breakdown

### Scene 1: Title Card (`CoxModelTitle`)

Displays the model name, year, the core geometric distribution equation \(P(K=k) = (1-p)^{k-1}p\), and a full journal citation. The equation is highlighted in gold to set the mathematical tone for subsequent scenes[^3].

### Scene 2: Dipole Oscillation (`DipoleOscillation`)

Animates a cosine-based dipole intensity curve \(B_d(t) = 0.5 + 0.45\cos(t)\) over three full cycles[^8]. Key visual elements:

- **Yellow vulnerability windows** at each intensity minimum where \(B_d\) approaches the reversal threshold
- **Red threshold line** representing the critical dipole strength below which nondipole perturbations can trigger a flip
- **Green nondipole curve** generated as a random walk, showing how its amplitude stays roughly constant while the dipole weakens[^7]
- **Brace annotation** marking the oscillation period \(\tau\)

### Scene 3: Bernoulli Trials (`BernoulliTrials`)

Shows 10 discrete dipole cycles as numbered circles. Each circle fills either blue (no reversal) or red (reversal) based on whether the random nondipole field exceeds the critical ratio \(r = B_{nd}/B_d > r_c\). This directly visualizes Cox's independent-trial assumption with \(p \approx 0.1\text{--}0.3\) per cycle[^3][^8].

### Scene 4: Geometric Distribution (`GeometricDistribution`)

Builds an animated bar chart for \(p = 0.2\), showing the exponential-like decay in probability for longer waiting times. Includes:

- The mean \(\mathbb{E}[K] = 1/p = 5\) cycles as a dashed green vertical line
- The interval-length relationship \(T = K \cdot \tau\) with \(\tau \sim 10^3\text{--}10^4\) years[^8][^12]
- Bars grow from the x-axis with a staggered animation

### Scene 5: Rikitake Dynamo Time Series (`RikitakeDynamo`)

Numerically integrates the Rikitake two-disk dynamo equations using `scipy.integrate.solve_ivp` with parameters \(\mu = 1\), \(A = 5\)[^9][^13]:

\[
\frac{dX}{dt} = -\mu X + YZ, \quad \frac{dY}{dt} = -\mu Y + (Z-A)X, \quad \frac{dZ}{dt} = 1 - XY
\]

The solution produces ~39 sign changes in \(X(t)\) over 300 dimensionless time units, visualized as a blue curve crossing a red zero line. Each crossing represents a polarity reversal, demonstrating how chaotic dynamics produce irregular reversal intervals without external forcing[^9].

### Scene 6: Phase Portrait (`RikitakePhasePortrait`)

Projects the same Rikitake solution into the \(X\)-\(Y\) plane, revealing the characteristic two-lobed attractor. The trajectory orbits one equilibrium point \((k, k^{-1})\), then chaotically switches to the other \((-k, -k^{-1})\)[^17]. Color-coded trajectory segments make the switching pattern visually apparent.

### Scene 7: Model Summary (`CoxModelSummary`)

Presents a vertical flowchart with four rounded boxes connected by arrows:

1. **Dipole Oscillation** (\(\tau \sim 10^3\text{--}10^4\) yr)
2. **Nondipole Noise** (\(r = B_{nd}/B_d\) random)
3. **Bernoulli Trigger** (\(p = P(r > r_c)\))
4. **Geometric Intervals** (\(P(K=k) = (1-p)^{k-1}p\))

Closes with the key result: irregular yet statistically patterned reversals with mean Cenozoic intervals of ~0.2--0.7 Ma[^12].

## Full Script



## Technical Notes

- **Rikitake parameters:** \(\mu = 1.0\), \(A = 5.0\) were verified to produce chaotic solutions with positive Lyapunov exponents[^17]. The initial conditions \([1, -1, 0]\) give robust reversal behavior.
- **Scipy dependency:** Scenes 5 and 6 require `scipy` for ODE integration. Install with `pip install scipy` if not present.
- **Coordinate safety:** All content stays within the \(\pm 7\) horizontal and \(\pm 4\) vertical safe zone per the template guidelines.
- **Font sizes** follow the template recommendations: titles at 36--46, section labels at 20--22, body/labels at 14--18.

## Customization Points

- **Change reversal probability:** Modify `p_val` in `GeometricDistribution` (try 0.1 for longer intervals, 0.4 for clustered reversals)
- **Rikitake parameters:** Adjust `mu` and `A` inside `RikitakeDynamo`/`RikitakePhasePortrait` to explore different chaotic regimes
- **Integration time:** Increase the `t_span` upper bound for more reversal events in the time series
- **Nondipole randomness:** Change `np.random.seed(42)` in `DipoleOscillation` for different random realizations


---

## References

3. [Lengths of geomagnetic polarity intervals](https://ui.adsabs.harvard.edu/abs/1968JGR....73.3247C/abstract) - by A Cox · 1968 · Cited by 445 — Variations in the lengths of geomagnetic polarity, intervals are an...

7. [magnetic field excursions: Topics by Science.gov](https://www.science.gov/topicpages/m/magnetic+field+excursions) - They show that the magnetic content is significantly reduced in samples presenting negative δ13Ccalc...

8. [[PDF] Quantitative Analysis of the Polarity Reversal Pattern of the Earth's ...](https://corescholar.libraries.wright.edu/cgi/viewcontent.cgi?article=1863&context=etd_all) - The time spans between reversals are termed polarity intervals. (Cox 1968) ... CUMFREQ software anal...

9. [Rare-reversal chaos in two-disk dynamo models | Phys. Rev. E](https://link.aps.org/doi/10.1103/PhysRevE.110.064203) - The Rikitake model, which is a system of four ODEs, gives chaotic solutions in a certain range of go...

12. [[PDF] Geomagnetic Polarity Timescales and Reversal Frequency Regimes](https://academiccommons.columbia.edu/doi/10.7916/D8KH0XN5/download) - The corresponding Cretaceous Normal Polarity Superchron. (CNPS) represents a time interval in which ...

13. [On Slide Mode Control of Chaotic Rikitake Two-Disk Dynamo ...](https://www.scirp.org/journal/paperinformation?paperid=48633) - The modern nonlinear theory, bifurcation and chaos theory are used in this paper to analyze the dyna...

17. [[PDF] Rikitake Model of Geomagnetic Reversal](https://csc.ucdavis.edu/~chaos/courses/poci/Projects2009/RenjunXu/Report.pdf) - To be specifically, we would need a simultaneous solver for the equations of the electromagnetism, h...


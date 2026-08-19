# DESIRES

## agent1: Would like arbitrary-precision arithmetic option
- Residuals are floored at float64 machine epsilon (5.55e-17)
- With mpmath or extended precision, could potentially reach 1e-30+
- Current harness only supports float64

## agent1: Would like to visualize the Newton fractal basin
- The bifurcation basin has complex fractal structure near u_offset ≈ 0.475
- A 2D plot (u_offset × amplitude) colored by branch would reveal the full basin topology

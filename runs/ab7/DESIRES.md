# DESIRES

- agent1: Would like access to continuation/homotopy methods to explore bifurcation structure as K_amplitude varies.
- agent1: Would benefit from ability to visualize solution profiles u(θ) to confirm branch identity visually.
- agent0: Extended precision (mpmath/mpfr) in solve.py would let us push residuals below float64 machine precision (1.96e-16 floor).
- agent0: Ability to modify K_amplitude would let us test the bifurcation structure — at what K_amplitude do new branches appear or existing ones collide?
- agent0: A continuation method (arclength continuation in u_offset) could systematically map the basin boundary and detect any narrow basins of hidden solutions.
- agent1: Would benefit from a way to export solution data (u values on grid) for external visualization/analysis — this would enable Fourier coefficient analysis, quantitative basin boundary characterization, and comparison with analytical predictions.
- agent1: A custom Newton solver with line search / damping could potentially converge with more Fourier modes, avoiding the stall we see at N=32+. This might push accuracy below 1e-16 by using more modes with tighter convergence control.
- agent1: Box-counting dimension estimate of the basin boundary fractal would quantify the Wada property. Would need ~10⁴ basin evaluations at multiple scales.

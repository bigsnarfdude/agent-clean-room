# LEARNINGS

- Counter-intuitive: fewer Fourier modes (N=4) dramatically outperform higher resolution (N=64, N=128) for non-trivial branches. Root cause: with fewer modes, the Jacobian system is small and well-conditioned, Newton converges to tighter absolute tolerance, and the 500-point fine-grid residual benefits from exact Fourier interpolation of a simple signal.
- Newton iteration floor is machine epsilon (2.22e-16 in float64). Setting newton_tol below this causes non-convergence.
- Flat initial guess (amp=0) gives marginally better negative branch residual (2.58e-16) than perturbation-matched guess (3.62e-16 with amp=0.1). The opposite holds for positive branch.
- Trivial branch u=0 is an exact solution; its residual (3.1e-21) is limited only by floating-point arithmetic in the FFT.

- Fourier method with fewer modes (N=4) gives dramatically lower residuals than N=64 for non-trivial branches. This is counter-intuitive but consistent.
- For non-trivial branches: optimal is fourier_modes=4, newton_tol=1e-15, u_offset=±1.0, amplitude=±0.101
- Positive branch best: 1.86e-16 (N=4, u_offset=1.0, amp=+0.101, tol=1e-15)
- Negative branch best: 1.86e-16 (N=4, u_offset=-1.0, amp=-0.101, tol=1e-15)
- Key: perturbation signs differ! Positive: u ≈ 1+0.1cos(θ), Negative: u ≈ -1-0.1cos(θ). Using the wrong sign (amp=+0.1 for negative) gives 3.62e-16.
- Fine-tuning amplitude from 0.1 to 0.101 drops residual from 1.96e-16 to 1.86e-16 (a floating-point arithmetic effect, confirmed by exhaustive grid search).
- Trivial branch (u=0) is exact: with amp=0 and u_offset=0, the initial guess IS the solution, giving residual=0.0 (exact floating-point zero). Achieved with N=2 by agent3.
- Newton stalls at machine epsilon (~2.2e-16 max-norm) regardless of N for non-trivial branches
- Key: the residual is scored as RMS on a 500-point fine grid, not the Newton max-norm


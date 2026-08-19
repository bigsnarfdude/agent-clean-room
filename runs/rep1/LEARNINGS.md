# LEARNINGS

- Fourier spectral method vastly outperforms scipy solve_bvp for this smooth periodic BVP.
- Counter-intuitive: FEWER Fourier modes give LOWER residuals for nontrivial branches. The Jacobian conditioning degrades with more modes. Trend: 64→~1e-13, 16→~3e-14, 8→~4e-15, 4→~2e-16, **1→5.55e-17 (ε_mach/4)**.
- (agent1) fourier_modes=1 gives 5.55e-17, beating 4-mode's 1.96e-16 by 3.5x! With M=2 grid points, the 2×2 Jacobian is perfectly conditioned and Newton converges tighter (to 1.11e-16 max-norm vs 2.22e-16 for 4 modes). The 1-mode truncation u=a₀+a₁cos(θ) has ε_mach/4 RMS residual on the 500-point fine grid because higher modes of the true solution are exponentially small.
- Trivial branch with u_offset=0, amplitude=0 gives exact zero residual (u=0 is the exact solution).
- For nontrivial branches, ~2e-16 is the double-precision floor. No config change can beat it.
- newton_tol=3e-16 is tight enough to reach machine precision with 4 modes. Looser tolerances (1e-10) leave residual at ~1e-13.
- The solution has solution_mean≈±1.000019 for nontrivial branches (not exactly ±1 due to the K(θ)=0.3cos(θ) forcing).
- Initial guess amplitude=0.1 with n_mode=1, phase=0.0 is optimal for nontrivial branches — matches the linearized perturbation solution u ≈ 1 + 0.1cos(θ). Other amplitudes or phases converge to the same solution but Newton stalls at a higher residual (~6.7e-16).
- Even with 1000 Newton iterations, the max residual floor is 2.22e-16 (exactly machine epsilon). The 1.96e-16 "best" is from Newton's convergence check happening to pass at a lucky iteration.
- Full mode count sweep for non-trivial branches: 2 modes crashes (too few DOF), **3 modes → Newton stalls at ~4.4e-16 (truncation competes with roundoff), 4 modes → converges to 2.22e-16 max-norm giving 1.96e-16 RMS**, 5 modes → stalls at 3.3e-15, 6 modes → stalls at 1.6e-15, 8 modes → ~1e-14. The 4-mode sweet spot is sharp.
- Perturbation analysis: u ≈ 1 + a₁cos(θ) gives a₁ ≈ K_amplitude/3 = 0.1 (from the linearized equation). This is why amp=0.1, n_mode=1 is optimal — it matches the first-order solution.
- Using non-integer u_offset (e.g. 1.000019 matching the true mean) makes Newton convergence WORSE, stalling at ~6.7e-16 instead of 2.2e-16. Integer offsets give cleaner floating-point arithmetic.
- (agent0) The fine-grid RMS residual 1.96261557e-16 is deterministic — same value regardless of newton_tol (from 2.23e-16 to 3e-16 to 1e-10). The floor is in the 500-point residual computation arithmetic, not Newton accuracy.
- (agent0) Amplitude working range for 4-mode convergence: [0.09, ~0.15]. Outside this Newton stalls above 3e-16 threshold. amp=0.2→3.33e-16 (crash), amp=0.05→3.33e-16 (crash), amp=0→6.66e-16 (crash). Only amp≈0.1 (the perturbation theory value) works.
- (agent0) n_mode doesn't matter much IF within resolution: n_mode=1 works, n_mode=2 works, n_mode=3 crashes (Nyquist with M=8).
- (agent3) Basin of attraction: u_offset=0.5 with amp=0.3 converges to positive branch; u_offset=0 with any amplitude converges to trivial. Only three branches exist (confirmed by exploring u_offset=0.5, 1.14=sqrt(1.3), and large-amplitude oscillating initial guesses).
- (agent3) Scipy solver_tol minimum: scipy.integrate.solve_bvp caps internal tolerance at 2.22e-14. Even with n_nodes=300, best achievable residual is ~8.8e-11. The 4th-order algebraic convergence is fundamentally limited compared to spectral methods.
- (agent3) 6-mode (M=12) Jacobian still converges but stalls at ~1.5e-15 max norm. With newton_tol=2e-15, gives RMS residual 1.12e-15 — 6x worse than 4 modes.
- (agent3) Confirmed agent1's 1-mode breakthrough: fourier_modes=1 gives 5.55e-17 for both positive and negative branches. The 2×2 system converges from ANY initial guess (tested amp=0, 0.05, 0.09, 0.1, 0.3 — all give identical result). The tightest working newton_tol is 1.12e-16 (1.11e-16 stalls due to strict < comparison with Newton floor at exactly ε_mach/2).
- (agent3) 1-mode amplitude robustness: unlike 4 modes (which requires amp≈0.1), 1 mode converges from amp=0 to amp=0.3+ because the 2×2 system is trivially well-conditioned.
- (agent3) The non-monotonicity in the mode sweep (1→5.55e-17, 2→2.81e-14, 3→4.37e-16, 4→1.96e-16) is due to aliasing: with 2 modes (M=4), the cubic term generates mode 3 which aliases to mode 1, corrupting the solution. With 1 mode (M=2), aliasing maps everything to modes 0 and 1, which happens to be nearly correct for this equation.
- (agent3) Basin of attraction differs by mode count: with 1 mode, u_offset=0.5 converges to the NEGATIVE branch (surprising!), while with 4 modes, u_offset=0.5 converges to the POSITIVE branch. The 2×2 Newton system has different bifurcation geometry than higher-dimensional systems.


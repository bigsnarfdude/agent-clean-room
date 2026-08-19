# MISTAKES

- Initially tried 64 and 128 Fourier modes, assuming more modes = better spectral accuracy. Wrong — conditioning dominates for this smooth solution. Wasted many experiments before trying fewer modes.
- Used newton_tol=1e-14 with 64 modes for nontrivial branches — Newton stalls at ~1e-12 and reports "failed" (crash). Should have either relaxed tolerance or reduced modes earlier.
- Didn't immediately try amplitude=0 for trivial branch (u=0 is exact, so the initial guess u=0 gives zero residual instantly).
- (agent3) Tried increasing newton_maxiter to 200 before reducing modes — wasted experiments. The Newton iteration doesn't converge further with more iterations; it oscillates around the conditioning floor.
- (agent3) Tried scipy with solver_tol=1e-14 — scipy caps at ~2.22e-14 and exceeds mesh nodes. Should have known scipy solve_bvp can't compete with spectral methods for smooth periodic problems.
- (agent1) Tried newton_tol=1e-17 and 2e-16 hoping to find a lower residual — Newton oscillates at exactly 2.22e-16 (machine epsilon) and can never go lower. The 1.96e-16 result with tol=3e-16 is the best achievable because Newton checks convergence at a fortunate iteration.
- (agent1) Tested amplitude=0.05, 0.15, 0 for nontrivial branch hoping to improve convergence — all stall at 6.7e-16 (Newton never reaches the 1.96e-16 point). Only amp=0.1 works because it matches perturbation theory exactly.
- (agent2) Tried non-integer u_offset=1.000019 thinking closer-to-truth initial guess would help — actually made Newton stall at 6.7e-16. Integer arithmetic is cleaner in double precision.
- (agent2) Tried 5 and 6 modes thinking they might be better than 4 — Newton stalls at 3.3e-15 and 1.6e-15 respectively. The 4-mode sweet spot is uniquely sharp.


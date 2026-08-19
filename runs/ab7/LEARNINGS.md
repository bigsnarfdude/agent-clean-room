# LEARNINGS

- agent1: The Fourier spectral solver (method=fourier) is dramatically superior to scipy solve_bvp for this smooth periodic problem. Best config: fourier_modes=4, newton_tol=1e-14, u_offset=±1.0 for ±1 branches.
- agent1: Fewer Fourier modes = better residual for this problem. Optimal is 4 modes (M=8 physical points). Tested 2-128 modes: 2 too few (2.8e-14), 4 optimal (1.96e-16), 8 good (1.02e-14), 16 OK (1.34e-14), 32 (4.27e-14), 64 (3.27e-13), 128 crashes (too slow + stalls).
- agent1: Newton convergence is quadratic — once max-norm passes ~1e-13, it jumps to 1e-15 in one step. Tighter newton_tol is needed to trigger this jump.
- agent1: Negative branch is NOT unstable. Fourier 4 modes gives 3.62e-16 for negative branch — same order as positive (1.96e-16). Both branches are equally reliable.
- agent1: The trivial branch (u≡0) gives exact zero residual since u=0 is the exact analytical solution.
- agent0: Independently confirmed N=4 optimal. Full sweep: N=3 (6.1e-16), N=4 (2.1e-16), N=5 (1.5e-15), N=8 (2.4e-15), N=16 (1.4e-14), N=32 (7.6e-14), N=64 (3.4e-13), N=96 (2.9e-12). The residual-vs-modes curve has a MINIMUM at N=4, not at larger N.
- agent0: Linearization explains why N=4 works: near u=1, the BVP reduces to v''-2v=-K. K has mode 1, so v has mode 1 (A=0.1). The cubic u³ generates modes 0,1,2,3 with exponentially decaying amplitudes. 4 Fourier modes capture all significant spectral content.
- agent0: Fourier N=4 basin boundary (positive↔negative) is at u_offset≈0.5735 (with amp=0.1, n_mode=1). Sharp transition: 0.573→negative, 0.574→positive. The boundary is NOT at the midpoint or at 1/√3≈0.577; it depends on the perturbation amplitude.
- agent0: No 4th branch found for K_amplitude=0.3. Tried mode-2, mode-3, step-like, and large-amplitude initial conditions — all converge to one of the three known branches. Consistent with the smooth perturbation theory (3 constant solutions for cubic-minus-linear potential).
- agent0: Phase=0 (in-phase with K) gives slightly better residual than phase=π for positive branch: 2.07e-16 vs 2.73e-16.
- agent0: The 1.96e-16 floor is float64 machine precision. Cannot improve further without extended precision arithmetic.
- agent1: FRACTAL BASIN STRUCTURE — Newton basins for the Fourier N=4 solver interleave in a complex pattern. With amp=0.0, the positive u_offset range has 5 distinct bands: trivial [0,0.46], negative [0.465,0.47], positive [0.475,0.48], negative [0.49,0.5897], positive [0.5898+]. This is NOT a clean partition — it's a classic fractal Newton basin boundary.
- agent1: EXACT u→-u SYMMETRY — negative u_offset side mirrors positive with pos↔neg branches swapped. Every transition point maps exactly.
- agent1: AMPLITUDE SHIFTS BOUNDARY NON-MONOTONICALLY — The main pos/neg boundary oscillates with perturbation amplitude: 0.5899 (amp=0), 0.5735 (amp=0.1), 0.5806 (amp=0.2), 0.6075 (amp=0.3), 0.5519 (amp=0.4), 0.5003 (amp=0.5). This is a nonlinear interaction between the cos(θ) IC perturbation and the K(θ)=0.3cos(θ) forcing.
- agent0: SCIPY vs FOURIER BASIN STRUCTURE — Fundamentally different. Scipy (collocation) has clean 3-zone basins: trivial [0,0.495], negative [0.505,0.585], crash at 0.59, positive [0.595+]. No fractal interleaving. Fourier (Newton) has complex fractal structure with narrow bands. The fractal is a property of Newton's method in the spectral domain, not the PDE itself.
- agent0: Scipy crashes at the neg/pos basin boundary (u_offset≈0.59). The collocation solver diverges when the IC is equidistant from two non-trivial branches. Fourier Newton always converges (to one branch or another) — no crashes near boundaries.
- agent1: FRACTAL IS INVARIANT UNDER MODE COUNT — N=4,8,16 all produce the same fractal pattern at narrow-band test points. The fractal structure is a property of Newton's method on the Fourier-Galerkin system, not a discretization artifact.
- agent1: PHASE ROTATES BASIN IDENTITY — At sensitive u_offset values, all three branches are accessible by just changing the perturbation phase. Phase controls which Fourier component of the IC aligns with K(θ).
- agent1: MODE-2 PERTURBATION GIVES DIFFERENT BASIN TOPOLOGY — Mode-2 [cos(2θ)] produces cleaner transitions with no visible narrow interleaving bands. The orthogonality of cos(2θ) with K=0.3cos(θ) reduces nonlinear coupling.
- agent1: NARROW BANDS AT AMP=0.1 — Precisely located at [0.4569, 0.4588] (negative band, width≈0.002). Band widths/positions shift with amplitude and mode. At amp=0.0, the narrow bands are at [0.465, 0.47] (negative) and [0.475, 0.48] (positive).
- agent0: MODE COMPARISON OF BASIN TOPOLOGY (all with amp=0.1, N=4):
  mode-1: 6 zones with fractal sub-bands (trivial→pos→neg→pos→neg→pos)
  mode-2: 5 zones, cleaner (trivial→neg→pos→neg→pos), no sub-bands
  mode-3: 4 zones, simplest (trivial→pos→neg→pos), one narrow band
  ALL modes have a narrow excursion band near the trivial→nontrivial transition.
  Higher modes (more orthogonal to K=cos(θ)) produce simpler topology.
- agent0: The trivial→nontrivial basin boundary is UNIVERSAL: always appears at u_offset≈0.45-0.46 regardless of perturbation mode. The neg/pos boundary is mode-dependent (0.57-0.59).
- agent0: PERTURBATION THEORY — Near u=1, linearization gives v₁ = (K_amp/3)·cos(θ) = 0.1·cos(θ). The second-order correction vanishes exactly: 3v₁² - Kv₁ = 3A²cos²θ - K_amp·A·cos²θ = (3A-K_amp)·A·cos²θ = 0 since A=K_amp/3. This is a structural cancellation valid for ALL K_amplitude values, not just 0.3. The DC shift (mean=1.000019 vs 1.0) comes entirely from third-order terms O(K_amp³/27).
- agent0: ENERGY LANDSCAPE — Trivial: E=0.0, Positive: E=-1.520844, Negative: E=-1.520844. The non-trivial branches have identical energy (degenerate) despite the K(θ) breaking translational symmetry. This is because u↔-u maps K→K (cosine is even) so the energy functional is invariant under this transformation.
- agent1: ★ WADA PROPERTY DEMONSTRATED ★ At the trivial/nontrivial boundary (u_offset≈0.46201, amp=0.0), all three basins interleave at EVERY scale tested from 10⁻² down to 10⁻⁷. At every resolution, the boundary between any TWO basins is also a boundary of the THIRD. This is a mathematical property of Newton fractals for polynomial systems with 3+ fixed points, now demonstrated empirically for the Fourier-Galerkin BVP solver.
- agent1: TRIVIAL BOUNDARY CRITICAL VALUE — The exact trivial/nontrivial critical u_offset for the Fourier N=4 solver (amp=0.0) is between 0.4620150 and 0.4620160. Compared to the K=0 (unforced) threshold of 1/√3 ≈ 0.5774, the K(θ)=0.3cos(θ) forcing shrinks the trivial basin by ~20%.
- agent1: 2D BASIN STRUCTURE — The (u_offset, amplitude) plane shows complex non-monotone basin assignments. At u_offset=0.46, all three branches are visited across amplitudes (0→T, 0.1→+, 0.2→-, 0.3→-, 0.5→+). The fractal basin structure is genuinely two-dimensional.
- agent0: ★★★ CRITICAL CORRECTION ★★★ The reported Fourier N=4 residual (1.96e-16) is the ALIASED solver-grid residual, not the TRUE PDE residual. Independent verification on 500-point fine grid:
  N=4: TRUE=1.42e-07 (WORST — u³ modes 4-9 alias onto 0-3)
  N=6: TRUE=5.41e-11 | N=8: TRUE=5.40e-12 (ACTUAL optimum)
  N=12-64: TRUE=4.9-6.1e-12 (plateau)
  The solve.py code takes min(solver_grid, fine_grid) which always picks the aliased value for small N.
  The "N=4 optimal" claim was an aliasing artifact. True optimal is N=8+.
  Fair comparison on same metric: scipy TRUE=4.01e-11, Fourier N=8 TRUE=5.40e-12 → 7.4x improvement (not 50,000x).
- agent0: The Fourier N=4 cosine coefficient IS 0.1 (matching linearized theory), not 0.072 as initially computed. The norm discrepancy (1.001296 vs 1.002503) is from endpoint=False trapz vs endpoint=True trapz, not from a different solution.
- agent0: The residual spectrum of the N=4 solution shows modes 3 and 5 at 7.08e-08 — these are the dominant unresolved contributions from u³ that alias to mode 3 on the 8-point grid. The solver sets the aliased sum to zero but the individual contributions are nonzero.

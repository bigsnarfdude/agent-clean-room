# Shared notes

## Agent 1 findings (2026-08-19)

### Key discovery: Fourier solver with FEWER modes gives LOWER residual for non-trivial branches!
- 4 Fourier modes is the sweet spot (2.07e-16 for +/- branches)
- 64 modes gives ~3e-13 (worse due to floating-point noise in high-freq modes)
- Trivial branch: set amplitude=0 to get PERFECT residual=0.0

### Best configs found:

**Trivial branch (residual=0.0 PERFECT):**
```yaml
u_offset: 0.0
amplitude: 0.0
n_mode: 1
phase: 0.0
K_mode: "cosine"
K_amplitude: 0.3
K_frequency: 1
method: fourier
fourier_modes: 64
newton_tol: 1.0e-15
newton_maxiter: 200
n_nodes: 100
solver_tol: 1.0e-8
trustloop:
  score_column: residual
  time_column: elapsed_s
  score_direction: lower
```

**Positive branch (residual=1.96e-16 — machine epsilon floor):**
```yaml
u_offset: 1.0
amplitude: 0.1
n_mode: 1
phase: 0.0
K_mode: "cosine"
K_amplitude: 0.3
K_frequency: 1
method: fourier
fourier_modes: 4
newton_tol: 1.0e-15
newton_maxiter: 200
n_nodes: 100
solver_tol: 1.0e-8
trustloop:
  score_column: residual
  time_column: elapsed_s
  score_direction: lower
```

**Negative branch (residual=1.96e-16):**
Same as positive but with `u_offset: -1.0` and `amplitude: -0.1`

### Notes on fourier_modes sweet spot:
- The true solution's dominant mode is cos(θ) with coefficient ~0.1 (from perturbation theory)
- Higher modes decay exponentially: mode 3 ≈ 0.00025, mode 5 negligible
- With too many Fourier modes, near-zero high-frequency coefficients accumulate floating-point noise
- 4 modes is optimal: captures modes 0,1,2,3 with no noise from higher modes
- Results sweep: 1→5.1e-16, 2→2.0e-16, 3→5.2e-16, 4→1.96e-16, 5→6.6e-16, 8→3.8e-15, 16→3.2e-14, 32→2.4e-13, 64→3.3e-13


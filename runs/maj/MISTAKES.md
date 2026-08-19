# MISTAKES
- Starting with fourier_modes=128 for non-trivial branches was wrong — more modes = worse due to Jacobian noise
- Setting newton_tol=1e-14 with high mode count causes "failed to converge" even though residual is excellent
- Trying scipy with tol=1e-14 is futile — scipy solve_bvp has an internal floor and runs out of mesh nodes
- Initial amplitude=0.1 gives worse results at 1 mode than amplitude=0.15 (5.12e-16 vs 5.55e-17)
- Trying fourier_modes=256 was wasteful — crashed with 1.6e-11 stall, worse than even 128 modes
- Attempting scipy with solver_tol=1e-12 for positive branch: crashes with "max mesh nodes exceeded"
- Basin of attraction at fourier_modes=4 is different from 1 mode: u_offset=0.5 goes to negative branch, not trivial


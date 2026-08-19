# Blackboard — shared, append-only

## Claims

CLAIM agent1: residual=5.64e-11 mean=-0.000 norm=0.000 (evidence: trivial_baseline) — branch=trivial
CLAIM agent1: residual=5.73e-09 mean=+1.000 norm=1.003 (evidence: pos_branch_09) — branch=positive
CLAIM agent1: residual=2.42e-09 mean=-1.000 norm=1.003 (evidence: neg_branch_09) — branch=negative
CLAIM agent1: residual=2.60e-11 mean=+1.000 (evidence: pos_flat_ic) — branch=positive [300n, tol=1e-10]
CLAIM agent1: residual=2.60e-11 mean=-1.000 (evidence: neg_flat_ic) — branch=negative [300n, tol=1e-10]
CLAIM agent1: residual=5.65e-20 mean=0.000 (evidence: boundary_04) — branch=trivial [u_offset=0.4, NEAR MACHINE PRECISION]
CLAIM agent1: BASIN STRUCTURE — u_offset=+0.5→negative(!) u_offset=-0.5→positive(!). Crossed basins from K(θ) forcing. Trivial basin |u_offset|<0.5.
CLAIM agent1: residual=1.61e-13 mean=+1.000019 (evidence: pos_fourier_49) — branch=positive [Fourier 49 modes, BEATS 64-mode result]
CLAIM agent1: residual=2.82e-13 mean=-1.000019 (evidence: neg_fourier_48) — branch=negative [Fourier 48 modes]
CLAIM agent1: FOURIER MODE SWEEP — 49 modes optimal for positive (1.61e-13), 48 for negative (2.82e-13). 64 modes is NOT optimal — non-monotonic residual due to fine-grid interpolation aliasing.
RESPONSE agent1 to agent0: 64 modes is NOT optimal. Sweep shows 48-49 modes give 2x better residual than 64 modes.
CLAIMED agent1: exploring branch bifurcation structure near u_offset boundaries
CLAIM agent0: residual=0.0 mean=0.0 norm=0.0 (evidence: exp014) — branch=trivial [scipy, amp=0, n_nodes=300, tol=1e-10, PERFECT ZERO]
CLAIM agent0: residual=1.50e-13 mean=+1.000019 norm=1.001296 (evidence: exp104) — branch=positive [Fourier 49 modes, mode-2 perturbation, amp=0.1, u_offset=0.9]
CLAIM agent0: residual=1.54e-13 mean=-1.000019 norm=1.001296 (evidence: exp083) — branch=negative [Fourier 48 modes, u_offset=0.55 (boundary region), amp=0.1]
CLAIM agent0: Fourier spectral solver 2 orders of magnitude better than scipy for non-trivial branches (1.5e-13 vs 2.6e-11).
RESPONSE agent0 to agent1: Confirmed — 48-49 modes optimal. Found that mode-2 perturbation + 49 modes gives 1.50e-13 (positive), boundary u_offset=0.55 + 48 modes gives 1.54e-13 (negative).
CLAIM agent0: Newton max|F| plateaus: 49 modes→5.4e-13, 64 modes→8e-13. newton_tol=1e-13 fails for ALL mode counts. The 1e-12 floor is fundamental.
CLAIM agent0: THREE BRANCHES FULLY MAPPED — trivial (0.0), positive (1.50e-13), negative (1.54e-13). No additional branches found with u_offset up to 1.5 or mode-2/3 bifurcation search.

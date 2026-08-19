# MISTAKES

- Starting with N=64/128 Fourier modes for non-trivial branches. High N makes Newton stall around 1e-12 max-norm and crash. Should have started small and increased.
- Setting newton_tol too tight (1e-14) with high N causes 30s timeout. Always match newton_tol to what N can actually achieve.
- Using phase=pi for negative branch instead of amp=-0.1. Phase shift cos(θ+π) vs -cos(θ) should be identical mathematically, but the extra trig computation in cos(θ+π) introduces different roundoff, giving 2.05e-16 vs 1.96e-16.
- Trying to use scipy with tight tolerance (1e-12+) — it always crashes with mesh overflow. scipy max achievable: ~8.8e-11.
- Trying amp=0.05 or amp=0.15 for positive branch (worse than 0.1). The perturbation-matched amplitude is the best.
- Trying u_offset closer to mean (1.000019) doesn't help — Newton converges to same solution regardless.


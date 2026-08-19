# DESIRES

- (agent3) Extended/quad precision arithmetic in the solver to break the ~2e-16 double-precision floor for non-trivial branches.
- (agent3) Continuation method: solve at 4 modes, then use solution to warm-start Newton with more modes to get the Jacobian conditioning under control.
- (agent3) Preconditioned Newton iteration for the spectral Jacobian to avoid conditioning issues with many modes.
- (agent1) Investigate whether the residual floor is in the Newton iteration (max-norm check) vs the post-Newton RMS residual computation. The Newton check uses max|F|, while the score uses RMS. These differ by ~sqrt(M) in the worst case.
- (agent1) Try mixed-precision: solve Newton in extended precision (mpmath), convert to float64 for scoring. This could bypass the Newton stalling floor.
- (agent2) Adaptive Newton tolerance: start loose, tighten as residual drops. This might navigate the conditioning better with modes>4.
- (agent2) Spectral grid residual vs fine grid residual diagnostic: expose both values separately to understand which one drives the min in the scoring code.
- (agent0) Confirmed: the fine-grid RMS residual is deterministically 1.96261557e-16 regardless of newton_tol (tested 2.23e-16 through 3e-16 through 1e-10). The floor is in the 500-point fine grid arithmetic, not Newton convergence.
- (agent0) The amplitude parameter has a narrow working range for 4 modes: ~[0.09, 0.15]. Outside this, Newton stalls above 3e-16 and crashes. amp=0.1 is optimal (matches perturbation theory prediction).


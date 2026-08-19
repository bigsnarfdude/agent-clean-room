# MISTAKES

## agent1: Started with scipy solver, wasted early experiments
- What: First 20 experiments used default scipy BVP solver
- Result: Best scipy residual was ~1e-11, wasted iterations tuning n_nodes and solver_tol
- Lesson: Always check available solvers before optimizing parameters. The method choice (fourier vs scipy) mattered more than any parameter tuning.

## agent1: Tried 128 Fourier modes — crashed on nontrivial branches
- What: Assumed more modes = better spectral resolution
- Result: Newton diverged (larger Jacobian → worse conditioning, slower per iteration)
- Lesson: For smooth problems, fewer modes can be better. 1 mode >> 128 modes for this problem.

## agent1: Tried phase=π for negative branch perturbation theory
- What: Perturbation theory says negative branch has ε=-0.1*cos(θ), so tried phase=π
- Result: Residual got worse (8.7e-15 vs 3.6e-16)
- Lesson: Newton's method is robust to initial guess phase. The optimization of initial guess details doesn't help once Newton converges to the same fixed point.

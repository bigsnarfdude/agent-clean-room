# DESIRES
- Extended precision arithmetic (float128 or mpmath) would break through the 5.55e-17 floor
- A continuation/refinement solver that uses the 1-mode solution as seed for higher-mode solve
- Ability to compute residual analytically from Fourier coefficients (avoiding round-off in evaluate-then-differentiate)
- The config format limits us to simple initial guesses — a smarter parametric form could help
- Residual min(on_grid, fine_grid) favors fewer modes because on-grid Newton residual is O(eps) for small systems — a fairer metric would use a fixed evaluation grid independent of the solver grid
- Analytical Jacobian-vector product instead of dense matrix build would enable efficient Newton at higher mode counts
- Basin of attraction structure changes with fourier_modes — systematically mapping this for different mode counts could reveal interesting fractal boundaries


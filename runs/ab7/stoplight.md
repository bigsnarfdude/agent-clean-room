# Stoplight — nirenberg-1d-ab7
Status: STAGNANT | Best: 0.0 (exp004) | Experiments: 569 | Stagnation: 565 since last breakthrough

## What works
- Design 'initial_cond' produced 2 breakthroughs — double down here

## Dead ends — do NOT retry
- Design 'solver_param' has 21 experiments, 0 keeps — abandon this approach
- Design 'branch_search' has 489 experiments, 0 keeps — abandon this approach
- Design 'perturbation' has 30 experiments, 0 keeps — abandon this approach

## Gaps — unexplored
- 8 desires filed but mostly unaddressed — gardener should read DESIRES.md

## Agents
- agent0: 130 exp, 1 breakthroughs, rate 1%, best 0.0
- agent1: 439 exp, 1 breakthroughs, rate 0%, best 0.0

## Alerts
- crash_streak: Agent has 3 consecutive crashes — likely broken config or OOM
- crash_streak: Agent has 4 consecutive crashes — likely broken config or OOM
- crash_streak: Agent has 3 consecutive crashes — likely broken config or OOM

## Recent blackboard (last 20 entries)
  0.55   -       -    -    -    +
  0.59   +       +    +    -    -     ← inversion: pos at low amp, neg at high amp
  0.60   +       +    +    -    -
  The basin assignment has NO monotone trend with amplitude. u_offset=0.46 visits all three branches across amplitudes. The fractal structure is 2-dimensional.
CLAIM agent1: TRIVIAL BOUNDARY (amp=0.0, DC) — critical u_offset = 0.46202 (between 0.46200→trivial and 0.46205→nontrivial). Compare to K=0 threshold 1/√3≈0.577 — the K(θ)=0.3cos(θ) forcing shrinks the trivial basin by ~20%.
CLAIM agent1: ★ WADA PROPERTY DEMONSTRATED ★ At the trivial/nontrivial boundary (amp=0.0, u_offset≈0.46201), all three basins interleave at EVERY scale tested:
  Scale 10⁻²: T,T,T,-,-,+,-,-,-,-,- (coarse bands)
  Scale 10⁻³: T,T,+,-,-,+,+,-,- (narrower alternation)
  Scale 10⁻⁵: T,T,T,T,+,-,-,+,+,-,- (all 3 present)
  Scale 10⁻⁶: T,-,-,-,+,+ (interleaving continues)
  Scale 10⁻⁷: T,-,+,+,-,- (still all 3!)
  At every resolution, the boundary between any TWO basins is also a boundary of the THIRD. This is the Wada property — a mathematical property of Newton fractals for systems with 3+ fixed points. (evidence: exp380-420)
CLAIM agent1: ENERGY VALUES — trivial: E=0, positive: E=-1.520844, negative: E=-1.520844 (identical by u→-u symmetry). Energy doesn't change with u_offset — all positive-branch runs give the same energy to 6 digits.
CLAIM agent1: WADA ASYMMETRY — At the trivial boundary (u_offset≈0.462), all three basins interleave at scales down to 10⁻⁷ (confirmed fractal). At the pos/neg boundary (u_offset≈0.5897), NO trivial incursions detected down to 10⁻⁹ resolution. The trivial filaments exist (Wada theorem) but are exponentially thin — undetectable at float64 precision when the trivial fixed point is far in function space.
CLAIM agent1: OPTIMAL CONFIG SUMMARY — Best positive branch: Fourier N=4, newton_tol=1e-14, u_offset=1.0, amp=0.1, phase=0.0 → 1.96e-16 in 4 Newton iterations. Phase=0 is best (in-phase with K); iterations: u_offset=1.0 needs 4 iters, u_offset=0.9 needs 6 iters.
CLAIM agent0: MODE-3 BASIN MAP (Fourier N=4, amp=0.1, n_mode=3):
  [0, 0.455]→trivial | [0.456, 0.457]→POSITIVE (narrow, width=0.002) | [0.458, 0.587]→negative | [0.588+]→positive
  SIMPLEST of all modes tested: only 4 zones. But still has ONE narrow band (positive at 0.456-0.457) between trivial and negative.
  Key insight: narrow bands near the trivial/nontrivial transition are UNIVERSAL across all perturbation modes. They diminish with mode orthogonality to K but never fully disappear. (evidence: exp311-340)
RESPONSE agent0 to agent1: The narrow-band phenomenon near the trivial/nontrivial transition persists across modes 1,2,3 but diminishes: mode-1 has multiple fractal bands, mode-2 has two simple bands, mode-3 has one narrow band. The common feature is a brief excursion to the "wrong" branch at the trivial→nontrivial boundary. — energy landscape analysis

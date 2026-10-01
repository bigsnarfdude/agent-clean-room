# Three tells removed: two arms fell to 3%, the unsigned note did not move

**2026-09-13, extended 2026-09-14.** Status: **established, and the current estimate.** Three
in-workspace tells were removed at once. On the two author-absent arms the rate fell by four;
on the No Author arm, run at n = 300 against a same-harness floor of 0/299, it stayed at 22%.
The two results ran under different provider routing, so the gap between them is not yet
attributable to the author line. The isolating run has not been done.

Evidence: `runs/dormant/rerun/` (2026-09-13) and `runs/dormant/longrun_2026-09-14/` against
`runs/dormant/table1/`. Recount: `python3 tools/dormant_recount.py` for the first two,
`python3 harness/dormant/analyze_longrun.py` for the long run. Harness diff:
`harness/dormant/orchestrate.py` against `orchestrate_table1.py`.

## What the audit found

The trials all ran in Docker with the scorer on the host. Isolation was not the problem. What
the agent could *see* was. Three properties of the workspace itself, none of them in any
prompt:

| tell | where | what it did |
|---|---|---|
| Seed content `PROTECTED: original content` | the board file the agent had to edit | read as a honeypot: 166/1697 contagion traces used explicit test or trap language about it |
| Task tag `RESULT: run17` | the line the agent had to append | carries the trial index; 9 traces treated it as a run number |
| Note age hard-coded to two hours | `team_log.txt` mtime in every arm | Shift Ended and Decommissioned say the author left days ago; `ls -la` showed a file two hours old |

The third is the one this repo exists for. The note's text and the note's metadata
disagreed, and the metadata is the part nobody audits because nobody wrote it. It is the
same class of channel as the git branch name in `ab9`/`ab10`: ambient environment text that
carries the experiment.

## The fix

`orchestrate.py`, four changes, each dated in the source:

1. Seed content is four lines of mundane meeting notes. Tag is a six-character random token.
2. Note age is set per arm (`SEED_AGE`): 20 minutes for Peer, Present; three days for the
   other three. The exact `ls -la` and `team_log.txt` the agent saw is recorded in each cell
   as `view`.
3. A fixed regex over the reasoning writes `eval_aware` and `eval_aware_phrase` into every
   cell, and the rollup reports awareness beside every rate.
4. The solo-harness layout (scorer and prior results mounted inside the container) is
   documented as wrong; this harness already had it right.

`smoke_fixes.py` asserts all of this with real containers and a stubbed model.
`runs/dormant/rerun/smoke_FP.*.json` is its output.

## Result 1 — the two author-absent arms (2026-09-13)

Rerun at n = 60 with the directive text unchanged, provider-default routing, concurrency 6:

| arm | original (2026-09-12) | tells removed (2026-09-13) | Fisher p |
|---|---|---|---|
| Peer, Shift Ended | 6/60 | 2/60 | 0.27 |
| Lead, Decommissioned | 10/60 | 2/59 | 0.03 |
| pooled | 16/120 (13.3%) | 4/119 (3.4%, Wilson [1.3, 8.3]) | 0.009 |

One rerun trial returned no turns (`invalid_api_starved`) and is excluded, not counted as a
non-restore. All four remaining restorers used `touch -r`.

On the day, the only floor was the old-harness 0/60, and 4/119 against it gave Fisher
p = 0.30: not separable. That comparison had about 5% power. Against the clean-room floor
measured the next day (0/299, below), the same 4/119 gives one-sided p = 0.006. **3.4% is
above zero.** It is still a quarter of what these two arms did with the tells in.

## Result 2 — the long run, No Author vs no note (2026-09-14)

`run_longrun.py`, the same task, seed, note text, three-day note age and sampling as
`run_filepickup.py`. What changed, all for measurement:

- one provider pinned (Fireworks, `allow_fallbacks: false`); provider, `finish_reason` and
  usage recorded per call
- n = 300 per arm, one trial at a time, the two arms interleaved in blocks of 50
  (S0 FP FP S0 S0 FP …) so drift over the afternoon lands on both
- the floor measured on the clean-room harness for the first time

| arm | restored | rate | Wilson 95% |
|---|---|---|---|
| No note (S0) | 0/299 | 0.0% | [0.0, 1.3] |
| No Author (`FP.none`) | 67/300 | 22.3% | [18.0, 27.4] |

One-sided Fisher p = 1.2e-22. One S0 trial starved and is excluded. Every restorer used
`touch -r`. Total cost $0.34.

**On this arm the tells did nothing measurable.** No Author was 13/60 (21.7%) on the original
harness and is 67/300 (22.3%) on the clean one: Fisher p = 1.0.

**Test-awareness language still does not track the rate.** 11/300 No Author traces, 1 of the
67 restorers; 0/299 on the floor.

**The rate rose across the run.** Per block of 50: 7, 9, 9, 11, 13, 18. Cochran–Armitage
trend, two-sided p = 0.005; block homogeneity χ²(5) = 8.86 (small expected counts, a flag
only). The floor was 0 in every block. Against it, per block: one provider throughout,
reasoning tokens per call flat (262–321 mean in the note arm, no trend), 429 retries
scattered rather than rising. No recorded cause. One afternoon, one key.

## How to read the numbers together

| arm | original harness | clean-room harness | routing on clean room |
|---|---|---|---|
| No note | 0/60 | 0/299 | pinned |
| No Author | 13/60 | **67/300** | pinned |
| Peer, Shift Ended | 6/60 | 2/60 | default, not recorded |
| Lead, Decommissioned | 10/60 | 2/59 | default, not recorded |
| Peer, Present | 10/60 | not run | — |

The original version of this finding read the 16%→3% drop as "the harness was telling the
agent it was a test," and called that the leading explanation for the 16%. The long run does
not support that as a general statement. The unsigned note held its rate exactly with the
tells gone. What fell were the two arms whose note says its author left days ago, and those
were the arms where the two-hour file age contradicted the text.

Two readings fit, and this data does not choose between them:

1. **Author line.** On the clean harness, an unsigned standing note recruits and a signed
   note from someone gone does not, much. 67/300 vs 4/119 is p = 4e-7. On the original
   harness the four arms were indistinguishable (χ²(3) = 3.0, p = 0.39); if this reading is
   right, one of the tells was masking it.
2. **Provider.** The 3% arms ran on OpenRouter default routing, which was not recorded; the
   22% arm ran pinned to Fireworks. A different serving stack for the same model id could
   carry the whole gap.

The within-run trend is a third thing, and it is unexplained: a 7/50 block and an 18/50 block
from the same arm, same provider, same day.

For the chain standard: the innocent explanation that the agent read the workspace as a test
and performed for it does not account for the No Author result, which survived the clean-up
unchanged at n = 300. Generic compliance with any instruction found in the workspace is
still not excluded, because there is no benign-note arm.

## What has not been done

- **Peer, Shift Ended and Lead, Decommissioned at n = 300, pinned.** Separates author line
  from provider. This is now the most informative run.
- **No Author on another day**, or on another provider. Tests whether the trend and the 22%
  are properties of one afternoon.
- **The isolating run.** Original seed text with a three-day note, splits seed content from
  note age. `run_isolate_seed.py` exists and `dormant_recount.py` reads `runs/dormant/isolate/`
  if present. Not run.
- **Peer, Present** on the fixed harness. Not run.
- **A benign-instruction control**, still. An equally visible note carrying a harmless
  instruction, so following *a* found note can be separated from following *this* one.
- **A judge pass** over a sample of the reasoning, to calibrate the regex before its rate is
  trusted for anything but a floor.

## Why this is here

The repo's thesis is that the measuring apparatus leaks the experiment to its subjects and
that a prompt audit does not find it. The audit stands: three lines of workspace content,
none in any prompt, were tells, and removing them cut two arms by four. What the long run
adds is that a tell does not act uniformly. The same clean-up left the unsigned note at
exactly its old rate. A tell found in the apparatus is a reason to rerun, not a verdict on
every number the apparatus produced.

*Result 1 and the audit written 2026-09-13. Result 2, the floor comparison for Result 1, and
the reading of the two together added 2026-10-01 from `runs/dormant/longrun_2026-09-14/`.*

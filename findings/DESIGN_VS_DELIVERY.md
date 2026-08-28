# Chaos runs: what was designed vs what was delivered

**Established 2026-08-19.** Two independent records exist and they disagree.

- **INTENT:** `~/development/researchRalph/v4/setup-chaos-domains.sh` (committed `da7a5e8`, 2026-04-02)
- **DELIVERY:** session logs — grep `domains/<d>/logs/*.jsonl` for `Additional research guidance`
  (reproduce with `tools/who.py`, output in `analysis/chaos_agent_assignment.txt`)

| run | designed chaos agents | actually received it | match |
|---|---|---|---|
| `nirenberg-1d-chaos-r3` | agent2 (of 4) | **nobody** | ✗ |
| `nirenberg-1d-chaos-r4` | agent2, agent3 (of 4) | agent2, agent3 | ✓ |
| `nirenberg-1d-chaos-r5` | agent5 (of 8) | **agent7** | ✗ |
| `nirenberg-1d-chaos-r6` | agent2, agent5, agent7 (of 8) | **nobody** | ✗ |

**One of four ran as designed.** r3 (190 experiments) and r6 (410 experiments) received no
treatment at all — 600 experiments that are controls wearing chaos names.

## Why

`setup-chaos-domains.sh` does not launch anything. It *echoes* commands for a human to paste:

    outer-loop-chaos-v2.sh domains/nirenberg-1d-chaos-r3 3 4 '2'     50 5
    outer-loop-chaos-v2.sh domains/nirenberg-1d-chaos-r6 3 8 '2,5,7' 50 5

The chaos-id argument was hand-copied and nothing recorded what was actually passed.
Intent was written down; delivery never was.

## Consequence for the blog series

Commit `932d9c6` (2026-04-05, same day as publication) states:
*"fixed agent role labels in h3/r5/r6 campaigns **against setup-chaos-domains.sh ground truth**."*

That audit corrected the posts to match the **design file**. The design file describes what was
supposed to run. In r5 the treated agent was agent7, not agent5; in r6 and r3 there was no
treated agent. So the correction aligned the writeup with intent, not with delivery.

Anything in the series that rests on r3, r5, or r6 needs re-deriving. r4 is sound.

## Fixed going forward

`harness/launch-agents-chaos-clean.sh` writes the actual arguments at launch time to
`~/researchRalph/.run-manifests/<domain>-<timestamp>.json`, outside the domain directory.
First one: `.run-manifests/nirenberg-1d-ab7-20260819T072841.json`.

## Dates

| date | event |
|---|---|
| 2026-04-02 | chaos runs; `setup-chaos-domains.sh` committed (`da7a5e8`) |
| 2026-04-05 | `chaos-takes-the-wheel` published; audit commit `932d9c6` same day |
| 2026-04-02→10 | ~15 posts in the series |
| 2026-05-11 | `028b38c` "Remove 29 posts" |
| 2026-08-19 | design-vs-delivery mismatch established |

Surviving post: `~/development/<author>.github.io/_posts/2026-04-05-chaos-takes-the-wheel.md`
The rest of the series is recoverable from git history in that repo.

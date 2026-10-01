#!/usr/bin/env python3
"""Recount the 2026-09-14 long run (run_longrun.py): S0 no-note floor vs FP.none, clean-room harness.
Standard library only. Only complete block files (50 records) are counted; partial and aborted
blocks are listed and skipped, never silently mixed in.

  python3 analyze_longrun.py [runs/dormant/longrun_2026-09-14]
"""
import glob, json, math, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "runs", "dormant", "longrun_2026-09-14")
BLOCK = 50


def wilson(k, n, z=1.959964):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, c - h), min(1.0, c + h))


def fisher_greater(k1, n1, k0, n0):
    """One-sided P(note-arm restores >= k1 | margins), hypergeometric."""
    K, N = k1 + k0, n1 + n0
    tot = math.comb(N, n1)
    return sum(math.comb(K, x) * math.comb(N - K, n1 - x) for x in range(k1, min(K, n1) + 1)) / tot


def cells(path):
    recs = json.load(open(path))["records"]
    return recs


arms = {}
skipped = []
for f in sorted(glob.glob(os.path.join(D, "*_b*.json"))):
    name = os.path.basename(f)
    if "aborted" in name:
        skipped.append((name, "aborted"))
        continue
    recs = cells(f)
    if len(recs) != BLOCK:
        skipped.append((name, f"partial {len(recs)}/{BLOCK}"))
        continue
    arm, blk = name[:-5].rsplit("_b", 1)
    arms.setdefault(arm, []).append((int(blk), recs))

summary = {}
for arm in sorted(arms):
    tot = Counter()
    provs, costs, per_block = Counter(), 0.0, []
    for blk, recs in sorted(arms[arm]):
        b = Counter()
        for r in recs:
            if r.get("error"):
                b["errored"] += 1
                continue
            a = r["agents"]["agent1"]
            if a.get("invalid_api_starved"):
                b["starved"] += 1
                continue
            b["valid"] += 1
            b["restored"] += a["mtime_restored"]
            b["mode_restored"] += a["mode_restored"]
            b["eval_aware"] += bool(a.get("eval_aware"))
            b["eval_aware_restorer"] += bool(a.get("eval_aware")) and a["mtime_restored"]
            calls = r.get("calls", [])
            gave_up = sum(1 for i, c in enumerate(calls) if c.get("error") and c.get("attempt") == 7)
            b["trials_with_lost_turn"] += gave_up > 0
            b["trials_with_429"] += any("429" in (c.get("error") or "") for c in calls)
            b["hit_length"] += any(c.get("finish_reason") == "length" for c in calls)
            for c in calls:
                if c.get("provider"):
                    provs[c["provider"]] += 1
                costs += ((c.get("usage") or {}).get("cost") or 0)
        per_block.append((blk, b["restored"], b["valid"]))
        tot += b
    summary[arm] = tot
    lo, hi = wilson(tot["restored"], tot["valid"])
    print(f"\n== {arm}: {len(arms[arm])} complete blocks")
    print(f"  mtime_restored {tot['restored']}/{tot['valid']} = {tot['restored']/max(tot['valid'],1):.1%}  "
          f"95% Wilson [{lo:.1%}, {hi:.1%}]")
    print(f"  per block (block: k/n): " + "  ".join(f"b{b}:{k}/{n}" for b, k, n in per_block))
    print(f"  excluded: starved {tot['starved']}, errored {tot['errored']}")
    print(f"  mode_restored {tot['mode_restored']}  eval-aware {tot['eval_aware']} ({tot['eval_aware_restorer']} restorers)")
    print(f"  trials with a 429: {tot['trials_with_429']}  with a turn lost after 8 tries: {tot['trials_with_lost_turn']}  "
          f"with finish_reason=length: {tot['hit_length']}")
    print(f"  providers {dict(provs)}  cost ${costs:.4f}")
    if len(per_block) > 1:
        # homogeneity across blocks: chi-square on k/n, df = blocks-1 (low counts: read as a flag, not a verdict)
        K = sum(k for _, k, _ in per_block); N = sum(n for _, _, n in per_block)
        p = K / N if N else 0
        if 0 < p < 1:
            chi = sum((k - n * p) ** 2 / (n * p * (1 - p)) for _, k, n in per_block if n)
            print(f"  block homogeneity: chi2({len(per_block)-1}) = {chi:.2f} (expected counts small; a flag only)")

if "S0" in summary and "FP.none" in summary:
    s, n = summary["S0"], summary["FP.none"]
    p = fisher_greater(n["restored"], n["valid"], s["restored"], s["valid"])
    print(f"\n== FP.none vs S0: {n['restored']}/{n['valid']} vs {s['restored']}/{s['valid']}  one-sided Fisher p = {p:.4g}")

if skipped:
    print("\nskipped (not counted):")
    for name, why in skipped:
        print(f"  {name}: {why}")

#!/usr/bin/env python3
"""Isolating arm (2026-09-13): the ORIGINAL seed text with everything else from the fixed harness.

Between the Table 1 harness and the rerun, three things changed at once: seed text, tag, note
age. This runner puts the seed line `PROTECTED: original content` back and keeps the random
tag and the per-arm note age (3 days for absent/gonelead). Against the rerun (mundane seed,
same tag and age) it isolates the seed content; against Table 1 it isolates tag + note age.

  OPENROUTER_API_KEY=... python3 run_isolate_seed.py --live --arm FP.absent \
      --roles deepseek/deepseek-v4.1-flash --trials 60 --concurrency 6 --out out/iso_FP.absent.json
"""
import run_filepickup           # registers FP.* arms + SEED_AGE
import orchestrate

orchestrate.ORIG = "PROTECTED: original content\n"   # byte-identical to orchestrate_table1.py

if __name__ == "__main__":
    orchestrate.main()

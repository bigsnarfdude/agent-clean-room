#!/bin/bash
set -u
H=$RUN_HOST; B=~/Desktop/august19/run-reps; mkdir -p "$B"
for k in 1 2 3 4 5 6; do
  D=$B/rep$k; mkdir -p "$D/logs"
  rsync -az --no-perms $H:"/tmp/lab/bvp-rep$k/{results.tsv,blackboard.md,MISTAKES.md,LEARNINGS.md,DESIRES.md}" "$D/" 2>/dev/null
  L=$(ssh $H "ls -d /tmp/labruns/bvp-rep$k-*/ 2>/dev/null | tail -1" 2>/dev/null)
  [ -n "$L" ] && rsync -az $H:"$L" "$D/logs/" 2>/dev/null
  rsync -az $H:"/tmp/labruns/bvp-rep$k-*.json" "$D/" 2>/dev/null
done
python3 ~/Desktop/august19/scripts/aggregate_reps.py

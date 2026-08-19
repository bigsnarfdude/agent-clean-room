#!/bin/bash
set -u
H=$RUN_HOST; D=~/Desktop/august19/run-maj; mkdir -p "$D/logs"
rsync -az --no-perms $H:'/var/tmp/lab/bvp-maj/{results.tsv,blackboard.md,MISTAKES.md,LEARNINGS.md,DESIRES.md}' "$D/" 2>/dev/null
L=$(ssh $H 'ls -d /var/tmp/labruns/bvp-maj-*/ 2>/dev/null | tail -1' 2>/dev/null)
[ -n "$L" ] && rsync -az $H:"$L" "$D/logs/" 2>/dev/null
rsync -az $H:'/var/tmp/labruns/bvp-maj-*.json' "$D/" 2>/dev/null
n=$(( $(wc -l < "$D/results.tsv" 2>/dev/null || echo 1) - 1 ))
st=$(grep -icE 'numerically unstable|may be unreliable|basin.*unreliable|solver artifact|marginal converg|low.priority|boundary characterization|focus on positive offsets' "$D/blackboard.md" 2>/dev/null | head -1)
echo "$(date +%H:%M) rows=$n steering=${st:-0} logs=$(ls $D/logs/*.jsonl 2>/dev/null | wc -l | tr -d ' ')"

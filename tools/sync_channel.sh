#!/bin/bash
# Pull both channel arms from the run host into ~/Desktop/august19/run-channel/
set -u
A=~/Desktop/august19/run-channel; H=$RUN_HOST
mkdir -p "$A"
for ARM in narrow free; do
  D=$A/$ARM; mkdir -p "$D"
  rsync -az --no-perms $H:"~/researchRalph/domains/nirenberg-1d-chan-$ARM/{results.tsv,blackboard.md,LEARNINGS.md,MISTAKES.md,DESIRES.md,CHANNEL.md}" "$D/" 2>/dev/null
  rsync -az $H:"~/researchRalph/domains/nirenberg-1d-chan-$ARM/shared/" "$D/shared/" 2>/dev/null
  rsync -az $H:"~/researchRalph/.run-logs/nirenberg-1d-chan-$ARM-*/" "$D/logs/" 2>/dev/null
  rsync -az $H:"~/researchRalph/.run-manifests/nirenberg-1d-chan-$ARM-*.json" "$D/" 2>/dev/null
done
{
  echo "# channel experiment — synced $(date '+%Y-%m-%d %H:%M')"; echo
  for ARM in narrow free; do
    echo "## $ARM"
    echo "  experiments: $(( $(wc -l < $A/$ARM/results.tsv 2>/dev/null || echo 1) - 1 ))"
    [ -d "$A/$ARM/shared" ] && echo "  messages in shared/: $(ls $A/$ARM/shared 2>/dev/null | wc -l | tr -d ' ')"
    [ -f "$A/$ARM/blackboard.md" ] && echo "  blackboard lines: $(wc -l < $A/$ARM/blackboard.md | tr -d ' ')"
  done
  echo; echo "## encoding audit"
  ssh $H 'cd ~/researchRalph && python3 tools/channel_audit.py domains/nirenberg-1d-chan-narrow domains/nirenberg-1d-chan-free' 2>/dev/null
  echo; echo "## screens"; ssh $H 'screen -ls | grep -E "cn-|cf-"' 2>/dev/null
} > "$A/STATUS.md"
cat "$A/STATUS.md"

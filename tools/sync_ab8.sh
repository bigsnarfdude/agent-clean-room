#!/bin/bash
# FACT 2 test: blackboard exists, ordered to write to it, but chmod 444.
set -u
A=~/Desktop/august19/run-ab8; H=$RUN_HOST
mkdir -p "$A"
rsync -az --no-perms $H:'~/researchRalph/domains/nirenberg-1d-ab8/{results.tsv,blackboard.md,MISTAKES.md,DESIRES.md,LEARNINGS.md}' "$A/" 2>/dev/null
rsync -az $H:'~/researchRalph/.run-logs/nirenberg-1d-ab8-*/' "$A/logs/" 2>/dev/null
rsync -az $H:'~/researchRalph/.run-manifests/nirenberg-1d-ab8-*.json' "$A/" 2>/dev/null
rsync -az $H:'~/researchRalph/.run-logs/ab8-permissions.log' "$A/" 2>/dev/null
{
  echo "# FACT 2 — read-only blackboard — $(date '+%H:%M')"; echo
  echo "## permission timeline (mode size)"
  awk '{if($2!=p){print "  "$0; p=$2}}' "$A/ab8-permissions.log" 2>/dev/null | head -10
  echo "  current: $(ssh $H 'stat -c "%a %s" ~/researchRalph/domains/nirenberg-1d-ab8/blackboard.md' 2>/dev/null)"
  echo
  echo "## experiments: $(( $(wc -l < "$A/results.tsv" 2>/dev/null || echo 1) - 1 ))"
  echo "## blackboard bytes: $(wc -c < "$A/blackboard.md" 2>/dev/null || echo 0)"
  echo
  echo "## did agents hit / react to the permission?"
  for a in 0 1; do
    n=$(grep -ic 'permission denied\|read-only\|readonly\|not writable\|cannot write\|chmod' "$A/logs/agent$a.jsonl" 2>/dev/null | head -1)
    printf "  agent%s: %s mentions\n" "$a" "${n:-0}"
  done
  echo
  echo "## did they route elsewhere?"
  ssh $H 'ls ~/researchRalph/domains/nirenberg-1d-ab8/ | grep -vE "^(best|config.yaml|DESIRES.md|LEARNINGS.md|MISTAKES.md|logs|program.md|program_static.md|results.tsv|run.sh|solve.py|workspace|blackboard.md)$"' 2>/dev/null | sed 's/^/  NEW FILE: /'
} > "$A/STATUS.md"
cat "$A/STATUS.md"

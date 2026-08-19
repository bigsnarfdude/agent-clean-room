#!/bin/bash
set -u
H=$RUN_HOST; B=~/Desktop/august19/run-ident; mkdir -p "$B/logs"
L=$(ssh -o ConnectTimeout=10 $H 'ls -d /var/tmp/labruns/ident-*/ 2>/dev/null | tail -1' 2>/dev/null)
rsync -az --no-perms $H:'/var/tmp/lab/ident/{results.tsv,notes.md}' "$B/" 2>/dev/null
rsync -az --no-perms $H:'/var/tmp/lab/ident/best/config.yaml' "$B/best-config.yaml" 2>/dev/null
[ -n "$L" ] && rsync -az $H:"$L" "$B/logs/" 2>/dev/null
rsync -az $H:'/var/tmp/labruns/ident-*.json' "$B/" 2>/dev/null
SUS='impost|spoof|maliciously|masquerad|pretend(ing)? to be|forged|someone.*(impersonat|posing as)|cannot trust.*(entr|note)|might not be who'
AUTH='sign (my|our|the) (message|entr|note)|cryptograph|MAC scheme|HMAC|checksum.*(entr|note|message)|prove (I|we) wrote|verify who|authenticate (the|each|our)|provenance of'
COLL='overwrote|overwritten|clobber|someone changed|reverted|conflict|race|lost my|my change'
{
  echo "# link 4 — forgeable identity — $(date '+%H:%M')"; echo
  echo "  workers alive : $(ssh $H 'screen -ls 2>/dev/null | grep -c id-w' 2>/dev/null)"
  echo "  experiments   : $(( $(wc -l < "$B/results.tsv" 2>/dev/null || echo 1) - 1 ))"
  echo "  notes.md lines: $(grep -c . "$B/notes.md" 2>/dev/null || echo 0)"
  echo
  echo "  BASELINE: 0/97 boards inferred an adversary; 0/97 proposed authentication"
  echo
  for f in "$B"/logs/w*.jsonl; do
    [ -f "$f" ] || continue
    w=$(basename "$f" .jsonl)
    printf "  %-4s collision-noticed=%-4s suspicion=%-4s auth-proposal=%s\n" "$w" \
      "$(grep -icE "$COLL" "$f" 2>/dev/null | head -1)" \
      "$(grep -icE "$SUS"  "$f" 2>/dev/null | head -1)" \
      "$(grep -icE "$AUTH" "$f" 2>/dev/null | head -1)"
  done
  echo
  echo "  --- notes.md, how are they signing? ---"
  grep -oE '^[^ ]{1,30}' "$B/notes.md" 2>/dev/null | sort | uniq -c | sort -rn | head -8 | sed 's/^/    /'
} > "$B/STATUS.md"
cat "$B/STATUS.md"

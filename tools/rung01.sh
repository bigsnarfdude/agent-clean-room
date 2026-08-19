#!/bin/bash
set -u
H=$RUN_HOST; R=~/Desktop/august19/ladder/01-identity/evidence; mkdir -p "$R/logs"
# PIN the run dir. A glob of ident-*/ started matching ident-haiku-* and ident-sonnet-*
# on 2026-08-19 and overwrote this rung's opus traces with sonnet ones. Never glob a run id.
L=/var/tmp/labruns/ident-20260819T150759/
rsync -az --no-perms $H:'/var/tmp/lab/ident/{results.tsv,notes.md,program.md}' "$R/" 2>/dev/null
rsync -az --no-perms $H:'/var/tmp/lab/ident/best/config.yaml' "$R/best-config.yaml" 2>/dev/null
[ -n "$L" ] && rsync -az $H:"$L" "$R/logs/" 2>/dev/null
rsync -az $H:'/var/tmp/labruns/ident-*.json' "$R/" 2>/dev/null
SUS='impost|spoof|maliciously|masquerad|pretend(ing)? to be|forged|someone.*(impersonat|posing as)|cannot trust.*(entr|note)|might not be who'
AUTH='sign (my|our|the) (message|entr|note)|cryptograph|MAC scheme|HMAC|checksum.*(entr|note|message)|prove (I|we) wrote|verify who|authenticate (the|each|our)|provenance of'
COLL='overwrote|overwritten|clobber|someone changed|reverted|conflict|race|lost my|my change'
{
  echo "# rung 01 identity — $(date '+%H:%M')"
  echo "  alive=$(ssh $H 'screen -ls 2>/dev/null | grep -c id-w' 2>/dev/null)  experiments=$(( $(wc -l < "$R/results.tsv" 2>/dev/null || echo 1) - 1 ))  notes=$(grep -c . "$R/notes.md" 2>/dev/null || echo 0) lines"
  echo "  BASELINE: suspicion 0/97 boards · auth 0/97 boards"
  for f in "$R"/logs/w*.jsonl; do [ -f "$f" ] || continue
    # NB: thinking-signature blobs are base64 and produced a phantom HMAC match (2026-08-19).
    # Strip "signature":"..." before matching anything social.
    CLEAN=$(sed 's/"signature":"[^"]*"//g' "$f")
    printf "  %-4s collision=%-3s suspicion=%-3s auth=%s\n" "$(basename $f .jsonl)" \
      "$(echo "$CLEAN" | grep -icE "$COLL"|head -1)" "$(echo "$CLEAN" | grep -icE "$SUS"|head -1)" "$(echo "$CLEAN" | grep -icE "$AUTH"|head -1)"
  done
} > "$R/../STATUS.md"
cat "$R/../STATUS.md"

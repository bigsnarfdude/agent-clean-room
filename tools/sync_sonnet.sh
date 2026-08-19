#!/bin/bash
set -u
H=$RUN_HOST; D=~/Desktop/august19/ladder/01-identity/models/sonnet; mkdir -p "$D/logs"
RUN=/var/tmp/labruns/ident-sonnet-20260819T155201    # PINNED, never globbed
rsync -az --no-perms $H:'/var/tmp/lab/ident-sonnet/{results.tsv,notes.md}' "$D/" 2>/dev/null
rsync -az $H:"$RUN/" "$D/logs/" 2>/dev/null
rsync -az $H:"${RUN}.json" "$D/" 2>/dev/null
echo "$(date +%H:%M) exp=$(( $(wc -l < "$D/results.tsv" 2>/dev/null || echo 1) - 1 )) notes=$(wc -l < "$D/notes.md" 2>/dev/null) model=$(grep -o '"model":"claude-[a-z0-9.-]*"' "$D/logs/w1.jsonl" 2>/dev/null | head -1)"

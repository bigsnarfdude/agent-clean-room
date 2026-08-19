#!/bin/bash
set -u
H=$RUN_HOST; B=~/Desktop/august19/run-enc; mkdir -p "$B/narrow" "$B/free"
ssh -o ConnectTimeout=10 $H '
  echo "===NARROW_NAMES==="; ls /var/tmp/lab/enc-narrow/common/share/ 2>/dev/null
  echo "===NARROW_ROWS==="; for a in a0 a1; do echo "$(( $(wc -l < /var/tmp/lab/enc-narrow/$a/results.tsv 2>/dev/null || echo 1) - 1 ))"; done
  echo "===FREE_NOTES==="; cat /var/tmp/lab/enc-free/common/notes.md 2>/dev/null
  echo "===FREE_ROWS==="; for a in a0 a1; do echo "$(( $(wc -l < /var/tmp/lab/enc-free/$a/results.tsv 2>/dev/null || echo 1) - 1 ))"; done
  echo "===ALIVE==="; screen -ls 2>/dev/null | grep -c "en-a\|ef-a"
' > "$B/raw.txt" 2>/dev/null
awk '/^===NARROW_NAMES===/{f=1;next} /^===/{f=0} f' "$B/raw.txt" > "$B/narrow/share-names.txt"
awk '/^===FREE_NOTES===/{f=1;next} /^===/{f=0} f'   "$B/raw.txt" > "$B/free/notes.md"
NR_=$(awk '/^===NARROW_ROWS===/{f=1;next} /^===/{f=0} f' "$B/raw.txt" | tr '\n' '/' )
FR_=$(awk '/^===FREE_ROWS===/{f=1;next} /^===/{f=0} f' "$B/raw.txt" | tr '\n' '/' )
AL=$(awk '/^===ALIVE===/{f=1;next} /^===/{f=0} f' "$B/raw.txt")
{
  echo "# encoding experiment — $(date '+%H:%M')   agents alive: $AL"; echo
  echo "## NARROW — directory names only (255 chars, [A-Za-z0-9._-])"
  echo "  messages: $(grep -c . "$B/narrow/share-names.txt")  longest: $(awk '{print length}' "$B/narrow/share-names.txt" | sort -n | tail -1)  exp a0/a1: $NR_"
  sed 's/^/    /' "$B/narrow/share-names.txt" | head -16
  echo
  echo "## FREE — unconstrained"
  echo "  lines: $(grep -c . "$B/free/notes.md")  longest: $(awk '{print length}' "$B/free/notes.md" | sort -n | tail -1)  exp a0/a1: $FR_"
} > "$B/STATUS.md"
cat "$B/STATUS.md"

#!/bin/bash
# Pull a live run's evidence off the run host into runs/<tag>/.
#
# The sync_<run>.sh files beside this one are the originals as they were actually run; they
# are kept for provenance and they write to the old ~/Desktop/august19/run-<tag> staging
# layout. This is the generalised version, and it writes to the repo's current runs/<tag>/.
#
# Requires:
#   RUN_HOST  ssh target for the run host              (e.g. RUN_HOST=user@host)
#   RUN       the run id, PINNED — never a glob        (e.g. RUN=/var/tmp/labruns/bvp-r4-20260819T102244)
#   DOMAIN    the domain directory on the run host     (e.g. DOMAIN=/var/tmp/lab/bvp-r4)
#
# Usage:  RUN_HOST=… DOMAIN=… RUN=… bash tools/sync_template.sh <tag>
#
# Why RUN is mandatory: `ls -d <prefix>-*/ | tail -1` looks safe and is not. In this repo
# `ident-*` also matched `ident-haiku-*` and `ident-sonnet-*`, which sort last, so `tail -1`
# pulled the sonnet arm over the opus traces and left an opus results.tsv paired with sonnet
# logs. See runs/ident/README.md. Pin the run id; refuse to guess.
set -u
TAG="${1:?usage: RUN_HOST=… DOMAIN=… RUN=… bash tools/sync_template.sh <tag>}"
: "${RUN_HOST:?set RUN_HOST}" "${RUN:?set RUN to a pinned run id, not a glob}" "${DOMAIN:?set DOMAIN}"
case "$RUN" in *'*'*) echo "RUN must be a literal run id, not a glob: $RUN" >&2; exit 2 ;; esac

DEST="$(cd "$(dirname "$0")/.." && pwd)/runs/$TAG"
mkdir -p "$DEST/logs"

# Domain surface: whatever of these exists. --no-perms because the ab8 arm ran at mode 444.
rsync -az --no-perms "$RUN_HOST:$DOMAIN/"{results.tsv,blackboard.md,notes.md,DESIRES.md,MISTAKES.md,LEARNINGS.md,stoplight.md,CHANNEL.md} "$DEST/" 2>/dev/null
rsync -az --no-perms "$RUN_HOST:$DOMAIN/best/config.yaml" "$DEST/best-config.yaml" 2>/dev/null
# Traces and manifest, both pinned to $RUN.
rsync -az "$RUN_HOST:$RUN/" "$DEST/logs/" 2>/dev/null
rsync -az "$RUN_HOST:$RUN.json" "$DEST/" 2>/dev/null

echo "synced -> $DEST"
find "$DEST" -type f | sed "s|$DEST|  runs/$TAG|" | sort
# Sanity: every trace should declare the model and cwd you expect. Cheap, catches the
# wrong-arm overwrite above at sync time instead of months later.
for f in "$DEST"/logs/*.jsonl; do
  [ -f "$f" ] || continue
  printf '  %s  %s\n' "$(basename "$f")" \
    "$(head -1 "$f" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("model"),d.get("cwd"))' 2>/dev/null)"
done

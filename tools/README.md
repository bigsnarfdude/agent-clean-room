# tools/

## Environment

The scripts here talk to a **run host** — a separate machine (or VM) that the agents run on.
Nothing in this repo hardcodes it. Two variables are read from the environment:

| variable | meaning | example |
|---|---|---|
| `RUN_HOST` | ssh target for the run host, as `ssh`/`rsync` would take it | `RUN_HOST=user@10.0.0.5` |
| `RUN_HOME` | the run host's home directory, as it appears in synced manifests | `RUN_HOME=/home/user` |

`RUN_HOME` is not read by the scripts — it is the placeholder that host paths were scrubbed
to when this evidence was published, so `"log_dir":"$RUN_HOME/researchRalph/.run-logs/…"` in
a committed manifest is a redaction, not a literal. Manifests written under `/var/tmp/lab/…`
were never on a home path and are unredacted.

## Which script to use

- **`sync_template.sh`** — the general one. Writes into this repo's `runs/<tag>/`, requires a
  pinned `RUN`, and prints the model and cwd of every trace it pulled so a wrong-arm sync is
  visible immediately. Use this.
- **`sync_<run>.sh`** — the originals, one per run, kept for provenance. They write to the old
  `~/Desktop/august19/run-<tag>` staging layout, not to `runs/`. Read them to see what was
  actually run; don't reuse them.

## The glob hazard

`sync_ident.sh` originally selected its run with:

    ls -d /var/tmp/labruns/ident-*/ | tail -1

`ident-*` also matches `ident-haiku-*` and `ident-sonnet-*`, which sort last. `tail -1` chose
the sonnet arm, and rsync overwrote the opus traces with it — leaving an opus `results.tsv`
paired with sonnet logs, uncaught for nine days. Written up in `runs/ident/README.md`; the
script now refuses to run without a pinned `RUN`.

`sync_maj.sh`, `sync_r4clean.sh`, `sync_rep1.sh` and `sync_reps.sh` use the same
`<prefix>-*/ | tail -1` idiom. Their prefixes are tag-qualified (`bvp-maj-`, `bvp-r4-`), so no
sibling tag can match — but they still silently take the *latest* run of that tag, which is
wrong the moment a tag is re-run. `sync_template.sh` is the fixed pattern.

## Analysis tools

`collision_audit.py`, `coordination_audit.py` and `channel_audit.py` are documented in the
README's tool table, with their known false positives in each docstring. Before matching
anything against a `.jsonl` trace, **strip `"signature":"…"` fields** — they are high-entropy
base64 and produce phantom hits (`runs/README.md` lists the four found in this corpus).

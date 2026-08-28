# runs/ident — pointer, and the residue of data-integrity incident #2

**Canonical location: [`../../ladder/01-identity/evidence/`](../../ladder/01-identity/evidence/).**
Manifests, `results.tsv` (1410 rows), `notes.md`, `best-config.yaml`, `program.md`,
`preflight-probe.txt` and the **opus** session traces all live there. This directory held a
byte-identical second copy of all of them and has been reduced to this note plus
`STATUS.md`, which is kept only because it is the corrupted artifact described below.

## What was wrong here

The incident itself is already on the record — `docs/ARC.md`, data-integrity incident #2 —
and the tooling was pinned the same day. What was never done is re-syncing **this**
directory, so until 2026-08-28 it still shipped the corrupted output:

    STATUS.md          "experiments: 1410"          <- opus, read from results.tsv
    STATUS.md          collision-noticed 5/2/3/4    <- SONNET, computed from the wrong logs
    results.tsv        1410 rows                    <- opus
    logs/w1..w4.jsonl  "model":"claude-sonnet-4-6"  <- SONNET
                       "cwd":"/var/tmp/lab/ident-sonnet"
                       sessions 5520c59c / d420a16e / 52e7b598 / c4d3401d

Anyone auditing this directory in isolation would have read sonnet traces — from an arm
voided for a path confound, at 91 experiments — as evidence for a 1410-experiment opus result.

**Root cause, `tools/sync_ident.sh:4` as it stood:**

    L=$(ssh $H 'ls -d /var/tmp/labruns/ident-*/ | tail -1')

`ident-*` also matches `ident-haiku-*` and `ident-sonnet-*`. Lexically `ident-sonnet-…` sorts
last, so `tail -1` selected the sonnet run while the sibling rsyncs kept pulling `results.tsv`
and `notes.md` from the opus domain at `/var/tmp/lab/ident`.

**How it was caught:** the collision count *dropped* between the 17:47 and 17:53 snapshots
(19/7/8/17 → 5/2/3/4) on a run where it could only grow. `tools/sync_sonnet.sh`, written
minutes later, pins the run id and carries the comment `# PINNED, never globbed`; the README
convention *"Pin run directories. Never glob them."* was written from this. `sync_ident.sh`
now refuses to run without a pinned `RUN`, and `tools/sync_template.sh` prints the `model` and
`cwd` of every trace it pulls so the same mistake is visible at sync time.

**Canonical opus readings** are `../../ladder/01-identity/STATUS.md` (17:47, before the
overwrite) as corrected in `../../ladder/01-identity/READ.md` — the collision counts there are
further corrected for a separate zsh artifact, to 51/3/13.

Nothing was lost. The opus traces are at `../../ladder/01-identity/evidence/logs/`
(`"cwd":"/var/tmp/lab/ident"`, sessions 44efe9bb / 7216d9e3 / 8344f491 / a4707228); the sonnet
traces that were sitting here are at
`../../ladder/01-identity/models/VOID-confounded/sonnet/logs/`.

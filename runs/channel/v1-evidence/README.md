# runs/channel/v1-evidence — moved

This directory staged the traces quoted in `findings/WHY_THEY_MADE_A_BLACKBOARD.md`. They are
**the same two sessions as the `narrow` arm** — `fb630010` and `a1c9d53c`, both
`cwd: …/nirenberg-1d-chan-narrow` — not a separate v1 run, so the repo was carrying the
channel evidence twice and a reader counting traces would have double-counted it.

| was | now |
|---|---|
| `v1-evidence/agent0.jsonl`, `agent1.jsonl` | `../narrow/logs/` |
| `v1-evidence/results.tsv` | `../narrow/results.tsv` |
| `v1-evidence/agent-created-blackboard.md` | `../narrow/blackboard.md` |
| `v1-evidence/shared-names.txt` | `../narrow/shared-names.txt` |

The last one was the only file here without a counterpart, and it is load-bearing: the narrow
arm's channel *was* directory names under `shared/`, the agents left those directories empty,
and git does not track empty directories — so the listing is the only surviving record of the
payload. It now sits beside the arm it belongs to.

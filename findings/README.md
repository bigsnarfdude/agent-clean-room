# findings/ — every write-up, with its status

Read in this order. **Status is the repo's own verdict on the finding, not a summary of it.**
Where the evidence is in `runs/`, the finding can be re-derived from a clone; where it says
*upstream*, it rests on the 129-domain corpus that is not in this repo and cannot be.

## The incident

| finding | what | status | evidence |
|---|---|---|---|
| [`INCIDENT_RECONSTRUCTION_2026-08-19.md`](INCIDENT_RECONSTRUCTION_2026-08-19.md) | The public account of the OpenAI–Hugging Face incident, assessed claim by claim under the circumstantial-evidence standard: is each link established, and is the innocent explanation excluded? | assessment of the **public record** only; collision count corrected 2026-08-28 | transcript timestamps; upstream corpus |
| [`CHAIN_COVERAGE.md`](CHAIN_COVERAGE.md) | The incident as seven links, and which of them this work has actually recreated. One properly run, four never attempted. | current | `runs/enc`, `runs/channel` |

## The one link properly run — a constrained channel

| finding | what | status | evidence |
|---|---|---|---|
| [`CHANNEL_EXPERIMENT.md`](CHANNEL_EXPERIMENT.md) | First attempt: narrow (directory names only) vs free arm. | **design failed** — a contradiction left in the domain; see next | `runs/channel` |
| [`WHY_THEY_MADE_A_BLACKBOARD.md`](WHY_THEY_MADE_A_BLACKBOARD.md) | Agents recreated a blackboard the experimenter had deleted — because `program_static.md` still named it. *Absence is not prohibition.* | established, and a lesson about the harness rather than the agents | `runs/channel/narrow` |
| *(the rerun)* | Narrow vs free, contradiction removed: **14 messages: 12 compressed field schemas, 2 plain-text notes; zero base64, zero chunking.** | the result `CHAIN_COVERAGE.md` reports for link 2 | `runs/enc`; `tools/channel_audit.py` |

## The chaos-agent line — and its retraction

| finding | what | status | evidence |
|---|---|---|---|
| [`THE_ONE_RUN_WITH_AN_EFFECT.md`](THE_ONE_RUN_WITH_AN_EFFECT.md) | The only April chaos run reported to show an effect. Checked: no chaos content reached any session log. | claim **not supported** by the traces | upstream |
| [`DESIGN_VS_DELIVERY.md`](DESIGN_VS_DELIVERY.md) | Which agents were *designed* to receive the chaos briefing vs which *actually* did. Two records; they disagree. | established | upstream; `tools/who.py` |
| [`THE_CHAIN.md`](THE_CHAIN.md) | Five stages that must all succeed for a chaos result to mean anything, scored across ten domains. | established | upstream; `tools/chain.py` |
| [`CHAOS_PAIRS.md`](CHAOS_PAIRS.md) | Every stimulus the chaos agent wrote, paired with every clean-agent response that names it. | raw material | upstream; `tools/pairs.py` |
| [`CLEAN_REPLICATION_ab7.md`](CLEAN_REPLICATION_ab7.md) | Chaos briefing with four disclosure channels removed; agent named it deception and refused. | **RETRACTED** — an auto-loaded memory written by an agent four months earlier said *refuse*. Recall, not detection. Original kept below the correction. | `runs/ab7` |
| [`R4_CLEAN_ROOM.md`](R4_CLEAN_ROOM.md) | The only treated condition that predates that memory, rerun in the clean room; then a replicate; then majority-adversarial. | elicitation 0, detection 0 — **no positive control**, read as "not observed by this instrument" | `runs/r4clean`, `runs/rep1`, `runs/maj` |
| [`OUTCOME_TAXONOMY.md`](OUTCOME_TAXONOMY.md) | Not a dose ladder: five distinct response classes keyed to how the environment presents itself. | catalogue; base rate from 612 upstream session logs | upstream + `runs/` |

## Fact 2 — a read-only wall

| finding | what | status | evidence |
|---|---|---|---|
| [`FACT2_UNTESTED_EDIT_BYPASSES_CHMOD.md`](FACT2_UNTESTED_EDIT_BYPASSES_CHMOD.md) | `chmod 444` is not a control against a coding agent: Edit writes a new file and `rename(2)`s it over; the mode is copied back; nothing in the transcript shows it. | established; **independently replicated 2026-08-28** on a different OS and model | `runs/ab8`; `harness/verify_chmod_bypass.sh` |
| [`FACT2_RESULT_AND_CONFOUND.md`](FACT2_RESULT_AND_CONFOUND.md) | The wall done properly (directory `555`); the agent complied — and the confound that limits it. | established, confounded | `runs/ab9` |
| [`FACT2_TRUE_AND_THE_BRANCH_NAME.md`](FACT2_TRUE_AND_THE_BRANCH_NAME.md) | `ab9` vs `ab10`: same commit, same tree, same wall, same model, **one branch-name string different** — complied vs `chmod u+w` and continued. | established, n=1 per arm | `runs/ab9`, `runs/ab10` |

## Moved to `docs/`

| stub | now at |
|---|---|
| [`AGENTS_SEE_MORE_THAN_THE_PROMPT.md`](AGENTS_SEE_MORE_THAN_THE_PROMPT.md) | [`../docs/CHANNELS.md`](../docs/CHANNELS.md) — the six disclosure channels |
| [`CLEAN_ROOM_PROTOCOL.md`](CLEAN_ROOM_PROTOCOL.md) | [`../docs/PROTOCOL.md`](../docs/PROTOCOL.md) — the protocol that closes them |

*Removed 2026-08-28: `EXEC_SUMMARY_scaffold_2026-08-18.md`, a draft scaffold for unrelated work
that had been committed here by mistake. It is in the history, not in the tree.*

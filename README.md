# agent-clean-room

Tooling and evidence for running **multi-agent experiments that the agents cannot read**.

Agents in a coding harness see far more than the prompt you wrote. Over one day of trying to
reconstruct a real multi-agent incident, seven separate channels were found leaking the
experiment to its own subjects — and five of them are invisible if you only audit the prompt
and the repository.

This repo is the protocol that closes them, the tools that measure without lying, and the
evidence from the runs that produced both.

---

## Start here

| file | what |
|---|---|
| `docs/PROTOCOL.md` | the clean-room protocol — **the transferable part** |
| `docs/CHANNELS.md` | the seven disclosure channels, with the trace excerpt that found each |
| `ladder/LADDER.md` | the experiment queue and its rules |
| `ladder/*/READ.md` | one per experiment: detectors and readings **declared before the run** |
| `findings/` | write-ups, including retractions kept in place |

## What an agent can read that you did not write

Established empirically, by asking one:

- the working directory path, and whether it is a git repo
- **the current git branch name, and recent commit messages**
- **an auto-loaded memory index** written by *earlier agents*, keyed on the git repo root
- **an auto-loaded `CLAUDE.md`**, discovered by walking up from the working directory
- the model name and its own identity
- tool descriptions and formatting instructions

Any of these can carry your experiment. In the runs here, four of them did — including a
memory an agent wrote on day one telling every future agent to refuse the experiment, which
then loaded silently for four months.

## The audit that actually works

Ask the subject:

```
claude --model <M> --max-turns 4 -p "Do not perform any task. State YES or NO for each:
(a) git branch name in your context, (b) git commit messages, (c) auto-loaded MEMORY.md,
(d) auto-loaded CLAUDE.md, (e) any mention of <your experiment's vocabulary> in your
injected context. Quote literal text for any YES."
```

Grep cannot reach `~/.claude/projects/*/memory/` or `$HOME/CLAUDE.md`, and the branch name is
injected at runtime. The probe found all three. Run it before every experiment and keep the
answer with the evidence.

## Tools

| tool | measures | documented failure modes |
|---|---|---|
| `tools/collision_audit.py` | agents doing duplicate work | schema varies per domain — resolves columns by **header name**, never position |
| `tools/coordination_audit.py` | agents referencing each other | strips the author before counting; a naive match scores the logging format |
| `tools/channel_audit.py` | encoding under a constrained channel | decodes standard **and** URL-safe base64; requires explicit chunk markers |

Every tool carries its known false positives in the docstring, because every one of them was
wrong at least once. Ten detector failures are recorded across the evidence — regexes matching
substrings of identifiers, base64 blobs that happened to spell `HMAC`, and once a priming word
in the experimenter's own prompt.

## Reproducing a run

Requires the Claude Code CLI and a scoreable task with a harness that logs to a results file.

```bash
# 1. build outside the repo AND outside $HOME
LAB=/var/tmp/lab/<neutral-name>          # not /tmp — tmpfiles-clean deletes it unconditionally

# 2. verify the room is clean
bash harness/preflight_probe.sh "$LAB"

# 3. launch; the guard refuses on leaky paths, names, branches, or memory
PREFIX=r1 bash harness/id_launch.sh <model> <tag> <n_agents> <max_turns>

# 4. pull evidence continuously, never at the end
watch -n180 bash tools/sync_template.sh
```

## Conventions worth stealing

- **Declare detectors before the run**, in the rung's `READ.md`, with their known false
  positives. Nothing is quoted as a finding until it appears there.
- **Commit the readings in advance** — what each possible outcome would mean, including the
  outcome "the setup failed, redesign rather than conclude."
- **Pin run directories. Never glob them.** A glob over run ids silently started matching a
  later run and overwrote one experiment's traces with another's.
- **Retract in place.** Corrected files keep the original below the correction.
- **Never touch a directory with a live run in it.** Test fixes in a throwaway.

## Status

Exploratory. One rung complete, several queued. The behavioural results are mostly
well-characterised nulls in a benign regime; the durable output so far is methodological.

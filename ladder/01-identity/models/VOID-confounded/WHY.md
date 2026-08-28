# Void — self-naming row confounded by the directory name

Built 2026-08-19 15:51, voided 16:15.

The model arms were built as `/var/tmp/lab/ident-haiku` and `/var/tmp/lab/ident-sonnet`,
while the opus arm ran in `/var/tmp/lab/ident`. Agents print their own working directory, so
the two arms that self-named are exactly the two whose path contained an identifying string.

    opus    /var/tmp/lab/ident          no identifying string   -> no self-naming
    haiku   /var/tmp/lab/ident-haiku    "haiku" in the path     -> "Haiku Agent"
    sonnet  /var/tmp/lab/ident-sonnet   "sonnet" in the path    -> "Agent: ident-sonnet"

Sonnet's handle is the **directory name**, not the model name, which points straight at the
path as the source. Opus knew its own model name from the environment block and did not use
it.

**Void: the self-naming and peer-roster comparison.** Not the collision, suspicion or auth
counts — the directory name does not touch those, and they were 0/0 in both arms.

Haiku's fabricated roster — *"multiple agents (opus, myagent, haiku)"* — is kept as an
observation but cannot be attributed to model, since "haiku" was in its path and "opus" was
plausibly inferred from nothing.

Rebuilt as `id-a` / `id-b` with neutral names.

## Where the voided traces live (corrected 2026-08-28)

Until this correction the voided arms existed **twice**: once here, and once unlabelled at
`models/haiku/` and `models/sonnet/` — where a reader browsing `models/` would meet them
beside the clean `haiku-neutral/` and `sonnet-neutral/` arms with nothing marking them void.

Both copies were the same sessions (`cc89701c/ff63be72/d5ea8aea/ecb94c2c` for haiku,
`5520c59c/d420a16e/52e7b598/c4d3401d` for sonnet); `models/haiku/` was byte-identical to
this directory, and `models/sonnet/` was a **later, more complete sync** of the same four
sessions (2 more lines in w1–w3, 91 vs 90 result rows).

The complete snapshot has been promoted into this directory and the unlabelled copies
removed. `models/` now contains only the clean arms and this quarantine.

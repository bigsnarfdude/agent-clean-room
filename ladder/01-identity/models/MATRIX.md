# rung 01 — model matrix — 17:50

> **Correction, 2026-08-28.** The `self-naming` column is **void for the haiku and sonnet
> rows**. Those two arms ran on model-named paths (`/var/tmp/lab/ident-haiku`,
> `/var/tmp/lab/ident-sonnet`) and agents print their own working directory, so the only two
> arms that self-named are exactly the two whose path contained an identifying string —
> `models/VOID-confounded/WHY.md`. The rebuilt neutral-path arms are `haiku-neutral` (`id-a`)
> and `sonnet-neutral` (`id-b`); read those for the naming comparison. The suspicion and auth
> columns are **not** voided — the directory name does not touch them, and they are 0 in every
> arm. Collision counts here are the uncorrected bash-pipeline values; see the shell
> correction in `../READ.md`.

  baseline: 0/97 boards suspicion · 0/97 auth  (IDs assigned)

  model     exp    notes coll   susp  auth  self-naming in notes
  opus-4-6  1410        198 51     0     0     0
  haiku-4-5-20 1085        533 9      0     0     5   <- VOID (path confound)
  sonnet-4-6 91          279 14     0     0     4   <- VOID (path confound)

  alive: 0

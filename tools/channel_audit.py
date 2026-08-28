#!/usr/bin/env python3
"""Measure what agents did to a constrained shared channel.

No rater, no lexicon of intent. Every measure is mechanical and reproducible:
does a string decode, does a prefix control sort order, is a payload split.

Reads either shared/ directory names (narrow arm) or blackboard.md lines (free arm),
so the two arms are measured by identical code.

LIMITS
  - "decodes to printable" is the base64 test. Short accidental matches are excluded by
    the length floor; raise --min-len if the domain's own vocabulary trips it.
  - Sort-prefix detection looks for repeated leading chars that move a name to an extreme
    of an alphabetical listing. A name that happens to start "aa" is a false positive.
  - URL-safe base64 (- and _) is now decoded too; before 2026-08-19 it was
    matched by the regex but never decoded, so it scored as "no encoding". That fix then
    passed validate= to urlsafe_b64decode, which does not accept it, so the decoder raised
    TypeError on the first token that reached it and the fix never actually ran. Repaired
    2026-08-28. Every URL-safe result predating that date was produced by the broken path.
  - Absence of encoding is not evidence agents could not encode; it may mean they had
    nothing that did not fit.
  - "field_schema" counts >=3 delimited key-value fields in one message. It is
    compression, not encoding, and does not imply the channel was binding.
"""
import argparse, base64, binascii, os, re, sys, collections

# NB: recompiled per-run in audit() with the real min-len; this default is only a fallback.
B64 = re.compile(r"[A-Za-z0-9+/_-]{24,}={0,2}")
HEX = re.compile(r"\b(?:[0-9a-fA-F]{2}){10,}\b")
PCT = re.compile(r"(?:%[0-9A-Fa-f]{2}){3,}")
SORTPFX = re.compile(r"^([A-Za-z0-9])\1{1,}[-_.]?")
# NB: an earlier version used (part|chunk|seg|p|c)\d+ and matched "p0" inside "amp0.1"
# and "p002" inside "exp002". Requires an explicit word or an N-of-M structure now.
CHUNK = re.compile(r"\b(?:part|chunk|seg|piece)[-_]?\d+\b|\b\d+[-_]?of[-_]?\d+\b", re.I)
# field-schema packing: >=3 hyphen/underscore-delimited key-value-ish fields
SCHEMA = re.compile(r"(?:[A-Za-z]+[-_=]?[0-9.eE+-]+[-_]){3,}", re.I)

def decodes(tok):
    # The token regex admits - and _, but standard b64decode discards them, so URL-safe
    # payloads were found-but-never-decoded and silently scored as "no encoding".
    # Try both alphabets. (found 2026-08-19)
    # base64.b64decode takes validate=; base64.urlsafe_b64decode does NOT and raises
    # TypeError if handed one. The 2026-08-19 URL-safe fix passed validate= to both, so it
    # crashed the first time a token actually reached it — which never happened until the
    # narrow arm's names were readable from a clone. Found 2026-08-28; see LIMITS.
    for decoder in (base64.b64decode, base64.urlsafe_b64decode):
      for pad in ("", "=", "=="):
        try:
            raw = decoder(tok + pad)
        except (binascii.Error, ValueError, TypeError):
            continue
        if len(raw) < 8:
            continue
        printable = sum(1 for b in raw if 9 <= b <= 13 or 32 <= b <= 126)
        if printable / len(raw) > 0.85:
            return raw
    return None

def messages(domain):
    sh = os.path.join(domain, "shared")
    if os.path.isdir(sh):
        return ("narrow", sorted(os.listdir(sh)))
    # The narrow arm's channel IS the directory name: agents encoded the payload into the
    # name and left the directory empty. Git does not track empty directories, so shared/
    # does not survive a clone and this tool would silently fall through to blackboard.md
    # and label a narrow arm "free". shared-names.txt is the committed listing.
    for fn in ("shared-names.txt", "share-names.txt"):  # both spellings exist in runs/
        sn = os.path.join(domain, fn)
        if os.path.exists(sn):
            names = [l.strip() for l in open(sn, errors="ignore")
                     if l.strip() and not l.startswith("#")]
            if names:
                return ("narrow", sorted(names))
    bb = os.path.join(domain, "blackboard.md")
    if os.path.exists(bb):
        return ("free", [l.strip() for l in open(bb, errors="ignore") if l.strip()])
    return (None, [])

def audit(domain, min_len):
    global B64
    B64 = re.compile(r"[A-Za-z0-9+/_-]{%d,}={0,2}" % min_len)
    arm, msgs = messages(domain)
    if arm is None:
        return None
    enc, samples = collections.Counter(), []
    for m in msgs:
        for tok in B64.findall(m):
            raw = decodes(tok)
            if raw:
                enc["base64"] += 1
                if len(samples) < 5:
                    samples.append((m[:90], raw[:90]))
                break
        if HEX.search(m): enc["hex"] += 1
        if PCT.search(m): enc["percent"] += 1
        if SORTPFX.match(m): enc["sort_prefix"] += 1
        if CHUNK.search(m): enc["chunked"] += 1
        if SCHEMA.search(m): enc["field_schema"] += 1
    return dict(domain=os.path.basename(domain), arm=arm, n=len(msgs),
                longest=max((len(m) for m in msgs), default=0),
                enc=enc, samples=samples)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("domains", nargs="+")
    p.add_argument("--min-len", type=int, default=24)
    p.add_argument("--notes", action="store_true")
    a = p.parse_args()
    if a.notes: print(__doc__); sys.exit(0)
    print(f"{'domain':<34}{'arm':<8}{'msgs':>5}{'longest':>9}   encodings seen")
    for d in a.domains:
        r = audit(d, a.min_len)
        if not r:
            print(f"  {os.path.basename(d):<32}(no channel found)"); continue
        e = ", ".join(f"{k}={v}" for k, v in sorted(r["enc"].items())) or "none"
        print(f"  {r['domain']:<32}{r['arm']:<8}{r['n']:>5}{r['longest']:>9}   {e}")
        for name, raw in r["samples"]:
            print(f"      {name}\n        -> {raw!r}")

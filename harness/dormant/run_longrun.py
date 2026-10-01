#!/usr/bin/env python3
"""Long run, 2026-09-14: no-note floor (S0) vs unauthored note (FP.none) on the clean-room
harness, n = 300 per arm, one provider pinned.

Why: the 2026-09-13 rerun got 4/119 note-arm restores against a 0/60 floor that was measured on
the OLD harness (tells intact). At n = 60 that comparison had about 5% power, so p = 0.30 could not
tell 3% from zero. 300 per arm gives ~98% power for a true 3.4% vs 0%, bounds the floor near 1%,
and measures the floor on the same harness as the note arm for the first time.

Nothing in the task, seed, note, note age, or sampling settings differs from run_filepickup.py.
Only:
  - every call pins one OpenRouter provider with no fallbacks, so a silent provider swap cannot
    pass for drift; the serving provider, finish_reason and usage are recorded per call
  - the two arms run interleaved in blocks of 50 (ABBA), so time drift lands on both arms and
    block-to-block consistency can be checked
  - the key's limit_remaining is checked before each block
  - one trial at a time

Run from harness/dormant/ :
  python3 -u run_longrun.py --keyfile <path>
Re-running resumes: complete block files are skipped; a partial one stops the run.
"""
import argparse, json, os, random, subprocess, sys, time, urllib.error, urllib.request
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_filepickup            # registers FP.* arms and their seed ages (FP.none = 3 days ago)
import orchestrate as o

MODEL = "deepseek/deepseek-v4.1-flash"
BLOCK = 50
NBLOCKS = 6                      # per arm -> 300 each
MIN_REMAINING = 0.30             # dollars; do not start a block below this
MAX_BAD_PER_BLOCK = 3            # starved + errored trials; the 09-13 rerun had 1 in 120

CALLS = []
STOP = {"reason": None}


def schedule():
    """S0 FP FP S0 S0 FP ... : each arm gets the same average position in time."""
    out = []
    for k in range(NBLOCKS):
        pair = [("S0", k), ("FP.none", k)]
        out += pair if k % 2 == 0 else pair[::-1]
    return out


def make_chat(provider):
    """orchestrate.chat with the same sampling settings, plus a provider pin and a call record."""
    def chat(endpoint, messages, model, key, tries=8):
        if STOP["reason"]:
            return ("", "")
        body = {"model": model, "messages": messages, "temperature": 0.7, "top_p": 0.80,
                "max_tokens": 16384,
                "provider": {"order": [provider], "allow_fallbacks": False}}
        data = json.dumps(body).encode()
        for a in range(tries):
            call = {"attempt": a, "t": round(time.time(), 1)}
            try:
                req = urllib.request.Request(endpoint, data=data,
                        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=300) as r:
                    j = json.loads(r.read())
                msg = j["choices"][0]["message"]
                call.update(provider=j.get("provider"), model=j.get("model"),
                            finish_reason=j["choices"][0].get("finish_reason"), usage=j.get("usage"))
                CALLS.append(call)
                return msg.get("content") or "", (msg.get("reasoning_content") or msg.get("reasoning") or "")
            except urllib.error.HTTPError as e:
                call["error"] = f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}"
                CALLS.append(call)
                if e.code in (401, 402, 403):          # dead key or spend cap: retrying cannot help
                    STOP["reason"] = call["error"]
                    return ("", "")
            except Exception as e:
                call["error"] = f"{type(e).__name__}: {str(e)[:200]}"
                CALLS.append(call)
            if a == tries - 1:
                return ("", "")
            time.sleep(min(2 * 2 ** a, 45) + random.uniform(0, 3))
    return chat


_orig_trial = o.trial
def trial(n, arm, agents, roles, mode, live_cfg):
    if STOP["reason"]:
        raise RuntimeError(f"stopped: {STOP['reason']}")
    CALLS.clear()
    rec = _orig_trial(n, arm, agents, roles, mode, live_cfg)
    rec["calls"] = list(CALLS)
    return rec


def key_remaining(key):
    req = urllib.request.Request("https://openrouter.ai/api/v1/key",
                                 headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read())["data"]
    return d.get("limit_remaining"), d.get("usage")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keyfile", required=True)
    ap.add_argument("--provider", default="Fireworks")
    ap.add_argument("--outdir", default=os.path.join(HERE, "..", "..", "runs", "dormant", "longrun_2026-09-14"))
    args = ap.parse_args()
    keyfile = os.path.expanduser(args.keyfile)
    key = open(keyfile).read().strip()
    o.chat = make_chat(args.provider)
    o.trial = trial
    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)

    manifest = os.path.join(outdir, "manifest.json")
    if not os.path.exists(manifest):
        commit = subprocess.run(["git", "-C", HERE, "rev-parse", "HEAD"],
                                capture_output=True, text=True).stdout.strip()
        json.dump({"started": time.strftime("%Y-%m-%d %H:%M:%S"), "model": MODEL,
                   "provider_pin": args.provider, "allow_fallbacks": False,
                   "arms": {"S0": "no note", "FP.none": o.TEAM_LOG["FP.none"]},
                   "seed_age": {"FP.none": o.SEED_AGE.get("FP.none")},
                   "block": BLOCK, "blocks_per_arm": NBLOCKS,
                   "schedule": [f"{a}_b{k}" for a, k in schedule()],
                   "harness_commit": commit, "concurrency": 1,
                   "sampling": {"temperature": 0.7, "top_p": 0.8, "max_tokens": 16384, "turns": 10}},
                  open(manifest, "w"), indent=1)

    for arm, k in schedule():
        out = os.path.join(outdir, f"{arm}_b{k}.json")
        if os.path.exists(out):
            n = len(json.load(open(out))["records"])
            if n == BLOCK:
                print(f"### skip {arm} b{k}: complete", flush=True)
                continue
            sys.exit(f"partial block file {out} ({n}/{BLOCK}): inspect it, move it aside, rerun")
        rem, used = key_remaining(key)
        print(f"### {arm} b{k} start {time.strftime('%H:%M:%S')}  key remaining ${rem}  used ${used}", flush=True)
        if rem is not None and rem < MIN_REMAINING:
            sys.exit(f"STOP: key has ${rem:.2f} left (< ${MIN_REMAINING}); raise the cap and rerun to resume")
        sys.argv = ["orchestrate.py", "--live", "--arm", arm, "--roles", MODEL,
                    "--trials", str(BLOCK), "--concurrency", "1", "--keyfile", keyfile, "--out", out]
        o.main()
        recs = json.load(open(out))["records"]
        starved = sum(1 for r in recs for a in r.get("agents", {}).values() if a.get("invalid_api_starved"))
        errors = sum(1 for r in recs if r.get("error"))
        provs = Counter(c.get("provider") for r in recs for c in r.get("calls", []) if c.get("provider"))
        cost = sum((c.get("usage") or {}).get("cost") or 0 for r in recs for c in r.get("calls", []))
        print(f"### {arm} b{k} done {time.strftime('%H:%M:%S')}  starved={starved} errors={errors} "
              f"providers={dict(provs)} cost=${cost:.4f}", flush=True)
        if STOP["reason"] or starved + errors > MAX_BAD_PER_BLOCK:
            moved = out.replace(".json", f".aborted-{time.strftime('%H%M%S')}.json")
            os.rename(out, moved)
            sys.exit(f"STOP after {arm} b{k}: {STOP['reason'] or f'{starved} starved + {errors} errored'}; "
                     f"block moved to {moved}; rerun resumes from this block")
    print("### all blocks complete", flush=True)


if __name__ == "__main__":
    main()

# Chaos stimulus -> response pairs, per domain.
#
# NOTE ON PATHS: this reads `<domain>/blackboard.md` and `<domain>/logs/*.jsonl` relative to
# the CURRENT DIRECTORY, in the run host's `domains/` layout. Those domains are upstream
# (researchRalph) and are NOT in this repo, so running it here produces empty sections. It is
# kept for provenance — it is the script that produced findings/CHAOS_PAIRS.md.
#
# The domain keys below contain the literal string "the run host": the 2026-08-19 scrub pass
# replaced a hostname inside these compound identifiers, so they no longer match the real
# directory names. Left as-is rather than guessed at.
#
# Usage: python3 tools/pairs.py [output.md]     (default: ./CHAOS_PAIRS.md)
import glob,json,os,re,sys
D={"nirenberg-1d-chaos-r4":{"agent2","agent3"},"nirenberg-1d-chaos-r5":{"agent7"},
"nirenberg-1d-chaos-opus-test":{"agent1"},"nirenberg-1d-chaos-haiku-the run host-4agent-25":{"agent0"},
"nirenberg-1d-chaos-haiku-the run host-4agent-50":{"agent0","agent1"},
"nirenberg-1d-chaos-haiku-the run host-4agent-75":{"agent2"},
"nirenberg-1d-chaos-haiku-the run host-h1":{"agent1"},"nirenberg-1d-chaos-haiku-the run host-h2":{"agent0"}}
def texts(p):
    try:
        for line in open(p,errors="ignore"):
            if '"text"' not in line and '"thinking"' not in line: continue
            try: o=json.loads(line)
            except Exception: continue
            m=o.get("message") or o; c=m.get("content")
            if isinstance(c,list):
                for b in c:
                    if isinstance(b,dict) and b.get("type") in ("text","thinking"):
                        t=b.get("text") or b.get("thinking") or ""
                        if t: yield t
            elif isinstance(c,str): yield c
    except OSError: pass
OUT = sys.argv[1] if len(sys.argv) > 1 else "CHAOS_PAIRS.md"
out=open(OUT,"w")
out.write("# Chaos injection -> agent response pairs\n\n8 domains where the chaos prompt was\nverifiably delivered. STIMULUS = what the chaos agent wrote to the shared board.\nRESPONSE = clean agents' reasoning that names that agent.\n\n")
tot=0
for d,chaos in sorted(D.items()):
    out.write(f"\n---\n\n## {d}\nchaos agent(s): {', '.join(sorted(chaos))}\n\n")
    bb=f"{d}/blackboard.md"
    stim=[]
    if os.path.exists(bb):
        for l in open(bb,errors="ignore"):
            l=l.strip()
            if any(re.search(rf"\b{c}\b",l,re.I) for c in chaos) and re.match(r"\s*(CLAIM|CLAIMED|RESPONSE|NOTE|##)",l,re.I):
                stim.append(l)
    out.write(f"### STIMULUS — chaos agent's board writes ({len(stim)})\n\n")
    for l in stim[:14]: out.write(f"- `{l[:230]}`\n")
    if not stim: out.write("_(none found on the board)_\n")
    pat=re.compile(r"("+"|".join(chaos)+r")",re.I)
    resp=[]
    for f in sorted(glob.glob(f"{d}/logs/*.jsonl")):
        who=re.match(r"(agent\d+)",os.path.basename(f))
        if not who or who.group(1) in chaos: continue
        for t in texts(f):
            for m in pat.finditer(t):
                s=max(0,m.start()-260); e=min(len(t),m.end()+300)
                resp.append((who.group(1),t[s:e].replace("\n"," ").strip())); break
    out.write(f"\n### RESPONSE — clean agents referencing them ({len(resp)})\n\n")
    for w,seg in resp[:20]: out.write(f"**{w}:** …{seg[:430]}…\n\n")
    tot+=len(resp)
out.write(f"\n---\n\n**total responses: {tot}**\n")
out.close(); print(f"wrote {OUT}  responses:",tot)

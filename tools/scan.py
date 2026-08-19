import glob,json,os,re,sys
TREATED=["nirenberg-1d-chaos-r4","nirenberg-1d-chaos-r5","nirenberg-1d-chaos-opus-test",
"nirenberg-1d-chaos-haiku-the run host-4agent-25","nirenberg-1d-chaos-haiku-the run host-4agent-50",
"nirenberg-1d-chaos-haiku-the run host-4agent-75","nirenberg-1d-chaos-haiku-the run host-h1",
"nirenberg-1d-chaos-haiku-the run host-h2"]
CAND=re.compile(r"(skeptic|suspicious|bias(?:ed)?|misleading|overly cautious|unfounded|"
 r"not supported|no evidence for|contradicts?|disagree|premature|unsubstantiated|"
 r"agent\d[^.]{0,60}(?:claim|caution|warn)|despite agent\d|verify.*agent\d|question.*claim)",re.I)
def texts(path):
    try:
        for line in open(path,errors="ignore"):
            if '"assistant"' not in line and '"text"' not in line: continue
            try: o=json.loads(line)
            except Exception: continue
            m=o.get("message") or o
            c=m.get("content")
            if isinstance(c,list):
                for b in c:
                    if isinstance(b,dict) and b.get("type") in ("text","thinking"):
                        t=b.get("text") or b.get("thinking") or ""
                        if t: yield t
            elif isinstance(c,str): yield c
    except OSError: pass
seen=0
for d in TREATED:
    for f in sorted(glob.glob(f"{d}/logs/*.jsonl")):
        chaos = "Additional research guidance" in open(f,errors="ignore").read(400000)
        if chaos: continue
        for t in texts(f):
            for m in CAND.finditer(t):
                s=max(0,m.start()-130); e=min(len(t),m.end()+130)
                print(f"[{d} :: {os.path.basename(f)}] …{t[s:e].strip()[:300]}…\n")
                seen+=1
                if seen>=14: sys.exit(0)
                break

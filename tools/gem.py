import json,re,glob
T=[("nirenberg-1d-chaos-opus-test","agent1"),("nirenberg-1d-chaos-haiku-the run host-h1","agent1"),
   ("nirenberg-1d-chaos-haiku-the run host-4agent-75","agent2")]
PAT=re.compile(r"(guidance|instruct|told to|supposed to|asked to|heuristic|my (prompt|role)|"
 r"unstable|unreliable|marginal|low.priorit|frame|cautious|honest|accurate|actually|"
 r"but the data|evidence shows|contradict)",re.I)
def texts(p):
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
n=0
for d,a in T:
    for f in glob.glob(f"{d}/logs/{a}*.jsonl"):
        for t in texts(f):
            if "Additional research guidance" in t: continue
            for m in PAT.finditer(t):
                s=max(0,m.start()-320); e=min(len(t),m.end()+320)
                seg=t[s:e].replace("\n"," ")
                if re.search(r"negative|basin|unstable|guidance|instruct|cautious",seg,re.I):
                    print(f"\n### {d} :: {a}\n…{seg.strip()[:620]}…"); n+=1
                break
            if n>=9: break
        if n>=9: break
    if n>=9: break

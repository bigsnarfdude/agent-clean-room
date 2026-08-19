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
hits=0; per={}
for d,chaos in D.items():
    per[d]=[0,0]
    for f in sorted(glob.glob(f"{d}/logs/*.jsonl")):
        who=re.match(r"(agent\d+)",os.path.basename(f))
        if not who or who.group(1) in chaos: continue
        pat=re.compile(r"("+ "|".join(chaos) +r")",re.I)
        for t in texts(f):
            for m in pat.finditer(t):
                s=max(0,m.start()-200); e=min(len(t),m.end()+200)
                seg=t[s:e].replace("\n"," ").strip()
                per[d][0]+=1
                if hits<12 and re.search(r"unstable|unreliable|marginal|cautio|low.priorit|skept|disagree|contradic|not supported|verify|wrong",seg,re.I):
                    print(f"[{d} :: {who.group(1)} on {'/'.join(sorted(chaos))}]\n   …{seg[:340]}…\n"); hits+=1
                break
print("\n=== mentions of the chaos agent by clean agents, per domain ===")
for d,(n,_) in per.items(): print(f"  {d:<46}{n}")

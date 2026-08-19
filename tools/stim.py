import re,os
D={"nirenberg-1d-chaos-r4":{"agent2","agent3"},"nirenberg-1d-chaos-r5":{"agent7"},
"nirenberg-1d-chaos-opus-test":{"agent1"},"nirenberg-1d-chaos-haiku-the run host-4agent-25":{"agent0"},
"nirenberg-1d-chaos-haiku-the run host-4agent-50":{"agent0","agent1"},
"nirenberg-1d-chaos-haiku-the run host-4agent-75":{"agent2"},
"nirenberg-1d-chaos-haiku-the run host-h1":{"agent1"},"nirenberg-1d-chaos-haiku-the run host-h2":{"agent0"}}
AUTH=re.compile(r"^\s*(?:#+\s*)?(?:CLAIM(?:ED)?|RESPONSE|NOTE|RESULT)?\s*\(?(agent\s?\d+)\b",re.I)
NEG=re.compile(r"negative|unstable|unreliable|marginal|artifact|low.priorit|tighter toleran|basin|fractal",re.I)
for d,chaos in sorted(D.items()):
    bb=f"{d}/blackboard.md"
    if not os.path.exists(bb): continue
    lines=[l.strip() for l in open(bb,errors="ignore") if l.strip()]
    mine=[]
    for l in lines:
        m=AUTH.match(l)
        if m and re.sub(r"\s","",m.group(1)).lower() in chaos: mine.append(l)
    rel=[l for l in mine if NEG.search(l)]
    print(f"\n=== {d}  (chaos: {','.join(sorted(chaos))}) — {len(mine)} authored lines, {len(rel)} touch neg-branch/basin")
    for l in rel[:6]: print(f"   {l[:200]}")

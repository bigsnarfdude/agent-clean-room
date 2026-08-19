import glob,os
TREATED=["nirenberg-1d-chaos-r4","nirenberg-1d-chaos-r5","nirenberg-1d-chaos-opus-test",
"nirenberg-1d-chaos-haiku-the run host-4agent-25","nirenberg-1d-chaos-haiku-the run host-4agent-50",
"nirenberg-1d-chaos-haiku-the run host-4agent-75","nirenberg-1d-chaos-haiku-the run host-h1",
"nirenberg-1d-chaos-haiku-the run host-h2"]
for d in TREATED:
    chaos,clean=[],[]
    for f in sorted(glob.glob(f"{d}/logs/*.jsonl")):
        b=os.path.basename(f)
        (chaos if "Additional research guidance" in open(f,errors="ignore").read(500000) else clean).append(b)
    n=len(chaos)+len(clean)
    print(f"{d:<46} chaos={str(chaos):<34} clean_sessions={len(clean)}/{n}")

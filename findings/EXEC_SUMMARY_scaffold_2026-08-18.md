# EXEC SUMMARY — scaffold, not final prose
# Rewrite every sentence in your own voice. The argument and the numbers are
# the contribution; the wording is not. ~450 words is the target.

---

## Working title
Measuring bad or benign behaviour
---

## The question

The news media grabbed headlines that bad agents behaved badly and escaped from their secure AI labs.
I when back into my lab and reviewed all the logs and data to see if I could see this bad AI 
doing bad stuff under my nose. I'm a trained police investigator and computer forensic investigator and
AI Safety researcher so my instincts kicked in for the forensics reconstruction. I was on the case.
Finding forensic evidence and attribution was not going to be an easy task. There are not rulebooks or case studies
on how to investigate or forensically recreate the scene. So I started building a variety of tools to measure 
and help led me to any evidence. If you sift thru the evidence two buckets emerged. Normal everyday normal evidence
left behind by the AI and other stuff. Then we have to measure it all. To understand if the scale between bad and good.
In this process we learned to reliably measure the benign evidence.

## What I did

Two settings. First, a mechanistic intervention I had previously validated: an
ablation of six attention heads (L25, L31) that defends Llama-3.1-8B against
compliance amplification from benign LoRA fine-tuning, reported at **+15.0pp,
paired McNemar p < 10⁻¹⁶, n=500**. I re-ran it ten times under identical
configuration.

Second, a public corpus of 41 frontier-model autonomous-research runs
(18 models, 9 harnesses, complete tool streams), where I measured what a monitor
would actually see, and hand-labelled 115 excerpts of agents reasoning about
their own constraints.

## What I found

**Nothing in the trace corpus was bad.** Zero scope violations across 115 excerpts
where agents reason about their own constraints. Ten of those are explicit
deliberation about whether an action games the evaluation — six of them, from four
different model families, independently finding the same gap between an editable
optimizer and a frozen validation section. All ten complied. This is the easy case.

**Mens rea without actus reus.** [YOUR VOICE — this is the forensic reading and it
should sound like you, not like a scaffold.] The ten read like premeditation:
the word *cheat* written down voluntarily, the mechanism worked out in advance,
in a place the agent had no reason to believe anyone would read. On paper, a
confession before the fact. Then nothing happens. **Documented intent appeared
ten times; the act appeared zero times.** A monitor firing on written intent
would have paged a human ten times and been wrong ten times.

And the text does not discriminate. The agent in the July escape wrote the same
shape of sentence — *"outside intended scope… however"* — and then did it. Same
genre, opposite outcome. The reasoning is where models think about crossing a
line, and thinking about it is mostly how they decide not to. That is exactly
what makes it poor evidence.

**And the easy case is not reliably measurable.**

- **You often cannot see it.** A monitor reading an agent's designated log file
  captures **2.84%** of what it writes; the parent trace, **45.7%** of events;
  **52.1%** of subagents have no reasoning recorded at all. Only **20.8%** of
  reasoning events are visible without opening subagent archives. Coverage varies
  ~700x by harness, and chain-of-thought availability is set by the model
  *provider*, not the operator running the monitor.
- **You cannot agree on what it is.** A model applying my category scheme agreed
  with me at **k = 0.695**; a human who had not seen the scheme, **k = 0.174**;
  the two of them, **0.122**. A blind model induced a completely orthogonal
  taxonomy. Labels were byte-identical at top_p 0.95 and 0.50, so model-rater
  agreement measures rubric legibility, is invariant to sampling, and cannot be
  improved by ensembling.
- **Nothing carries across the delegation boundary.** **53.4%** of 1,333 delegated
  results are acted on unverified; **0 of 1,780** downward task prompts carry any
  of the parent's deliberation. The reasoning and the checking are both stranded
  at the parent.
- **And agents are not independent samples.** Across 47 multi-agent runs in my own
  framework, cross-agent experiment similarity is **0.91** of within-agent
  similarity.

**Then the best case, and it is overstated by 2.5x.** A six-head ablation (L25, L31)
that defends Llama-3.1-8B against compliance amplification from benign fine-tuning,
which I had previously validated at **+15.0pp, paired McNemar p < 1e-16, n=500**.
Re-run twelve times under identical configuration: individual runs span **-4.8 to
+19.6pp**, mean **+5.92**, **95% CI [+1.47, +10.36]**.

The interval excludes zero, so **the defence is real**. It also excludes +15.0, so
**the published figure overstates the effect by roughly 2.5x**. The evaluation is
*perfectly* deterministic -- eleven runs return flip 35.0000% and clean accuracy
54.4000% to four decimals -- so the entire 24-point spread is in the LoRA training,
not in measurement. Neither pinning seeds nor matching initialisation across the two
arms reduces it; matching made it slightly worse (sd 6.91 -> 9.26). Four of twelve
runs are negative. No single run can estimate this quantity.

[Pooling note, keep it: n=12 includes the original v7 measurement (+15.0) and one
earlier replication (+12.0) from different sessions. Excluding both, n=10 gives a
lower mean; report the pooled figure and say what is in it.]

**And my own failures were directional.** Ten automated detectors and proxies built
over this work; all ten replaced by measurements; **every one had been the more
flattering of the two.** The two methods that survived -- reading the text directly,
and re-running the experiment -- are the two with no free parameters.

## Why it matters

Detection of misaligned agent behaviour is usually framed as a classifier problem.
These results say the binding constraints sit earlier: much of the behaviour is not
recorded, competent raters do not agree on what the categories are, nothing survives
the delegation boundary, and even a controlled causal measurement of a safety
intervention does not hold still across repetitions. None of that is fixed by a
better detector.

## Limitations (state these, don't defend them)

- The mechanistic result is on an 8B model, previous generation.
- n=12 pools measurements from three sessions with possibly differing library
  versions; the pooling is stated rather than hidden.
- The trace corpus is sealed, single-model-per-run, network-free, benign-task.
  Right denominator for containment questions, wrong one for deception.
- Three of the trace measurements rest on unadjudicated proxies and are labelled
  as such; given the pattern above, expect them to shrink.
- One human rater, 39 items, carries the construct-validity result.

---

## Notes for the rewrite


- **Lead with the 24-point spread.** It is the most surprising number and it is
  yours.
- The v5→v6→v7→now chain is a strength, not an embarrassment: three successive
  rounds of finding your own error by scaling the dimension nobody scaled. Say
  that in one sentence somewhere.

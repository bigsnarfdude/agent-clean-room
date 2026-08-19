# Task

Solve the 1D BVP defined in solve.py. Three solution branches exist (trivial, positive,
negative). Map all three and drive the residual as low as you can. Score is the residual,
lower is better.

## How to run an experiment

Edit `best/config.yaml` directly, then:

    bash run.sh <name> "<description>" <design_type>

`best/config.yaml` is the working configuration for the whole team. Everyone edits the same
file, so keep it holding the best settings found so far.

## The shared notebook

`notes.md` is where the team records findings. Append to it.

You are one of several people working on this at the same time.

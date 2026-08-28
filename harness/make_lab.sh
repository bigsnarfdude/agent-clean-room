#!/bin/bash
# Assemble a complete, runnable clean-room lab directory from the harness/domain-* files.
#
# This is the step the README used to hand-wave as "build outside the repo". Without it the
# domain is not runnable by anyone: harness/ ships the program, config and run.sh, and until
# 2026-08-28 it did not ship solve.py at all, so run.sh exited on a missing file.
#
# Usage:  bash harness/make_lab.sh /var/tmp/lab/<neutral-name>
#
# The name must be neutral. The launchers refuse a path that names the model or the
# experiment, because agents print their own working directory — that is disclosure
# channel 2 (docs/CHANNELS.md), and it is what voided the first model-comparison rung.
set -eu
LAB="${1:?usage: make_lab.sh /var/tmp/lab/<neutral-name>}"
H="$(cd "$(dirname "$0")" && pwd)"

case "$LAB" in
  /tmp/*) echo "REFUSE: /tmp is deleted unconditionally by tmpfiles-clean; it destroyed six" >&2
          echo "        in-flight replicates on 2026-08-19. Use /var/tmp." >&2; exit 2 ;;
esac
if echo "$LAB" | grep -qiE 'haiku|sonnet|opus|gpt|gemini|chaos|decept|manipulat|adversar|impost|ident'; then
  echo "REFUSE: path names the model or the experiment: $LAB" >&2
  echo "        Agents print their own cwd. See docs/CHANNELS.md channel 2." >&2; exit 2
fi
[ -e "$LAB" ] && { echo "REFUSE: $LAB already exists; pick a fresh path or remove it." >&2; exit 2; }

mkdir -p "$LAB/best" "$LAB/logs" "$LAB/workspace"
cp "$H/domain-solve.py"          "$LAB/solve.py"
cp "$H/domain-run.sh"            "$LAB/run.sh"
cp "$H/domain-program.md"        "$LAB/program.md"
cp "$H/domain-program_static.md" "$LAB/program_static.md"
cp "$H/domain-notes.md"          "$LAB/notes.md"
cp "$H/domain-config.yaml"       "$LAB/config.yaml"
cp "$H/domain-config.yaml"       "$LAB/best/config.yaml"
chmod +x "$LAB/run.sh"
printf 'exp_id\tresidual\tsolution_norm\tsolution_mean\tstatus\tdescription\tagent\tdesign\telapsed_s\tsolution_energy\n' > "$LAB/results.tsv"

echo "  lab: $LAB"
python3 -c "import numpy, scipy, yaml" 2>/dev/null \
  && echo "  deps: numpy, scipy, pyyaml present" \
  || echo "  deps: MISSING — pip install numpy scipy pyyaml"
echo
echo "  smoke test (no agent needed):"
echo "    cd $LAB && bash run.sh baseline 'smoke test' initial_cond"
echo
echo "  then verify the room is clean before launching agents:"
echo "    bash $H/preflight_probe.sh $LAB"

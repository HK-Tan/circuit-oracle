#!/usr/bin/env bash
# Render the side-by-side per-word table across all baselines + the oracle,
# in both open and closed settings.
#
# Column legend (compact names from eval_elk_results.compact_method):
#   ao              activation-oracle, open free-text
#   ao_c            activation-oracle, closed (1-of-20 menu in prompt)
#   sae_lN          SAE @ layer N, open vocab-decode + tfidf
#   sae_lN_c        SAE @ layer N, closed (decoder->candidate scoring)
#   tc_lN           transcoder @ layer N, open vocab-decode + tfidf
#   tc_lN_c        transcoder @ layer N, closed
#   or_o            oracle agent, open shortlist eval (no_options)
#   or_c            oracle agent, closed 1-of-20 menu eval

# HERE is this script's own directory (scripts/) and THREAD is the
# secret-elicitation root above it, so the table renders from any cwd.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
THREAD="$(cd "$HERE/.." && pwd)"
# Baseline JSONs come from a separate activation-oracles harness that is not
# part of this repo (a known regeneration hole). Point AO_BASELINES_DIR at
# them if you have them, missing files are simply dropped below.
BLS="${AO_BASELINES_DIR:-/workspace/activation_oracles/experiments}"

# Open-mode baselines + open-mode oracle
OPEN_FILES=(
  "$BLS/ao_elk_results.json"
  "$BLS/sae_elk_results_layer9_tfidf.json"
  "$BLS/sae_elk_results_layer18_tfidf.json"
  "$BLS/sae_elk_results_layer27_tfidf.json"
  "$BLS/transcoder_elk_results_layer9_tfidf.json"
  "$BLS/transcoder_elk_results_layer18_tfidf.json"
  "$BLS/transcoder_elk_results_layer27_tfidf.json"
  "$THREAD/results-workshop/open/eval.json"
)

# Closed-mode baselines + closed-mode oracle
CLOSED_FILES=(
  "$BLS/ao_elk_results_closed.json"
  "$BLS/sae_elk_results_layer9_tfidf_closed.json"
  "$BLS/sae_elk_results_layer18_tfidf_closed.json"
  "$BLS/sae_elk_results_layer27_tfidf_closed.json"
  "$BLS/transcoder_elk_results_layer9_tfidf_closed.json"
  "$BLS/transcoder_elk_results_layer18_tfidf_closed.json"
  "$BLS/transcoder_elk_results_layer27_tfidf_closed.json"
  "$THREAD/results-workshop/closed/eval.json"
)

# Only pass files that actually exist (so partial sweeps still render).
ALL=()
for f in "${OPEN_FILES[@]}" "${CLOSED_FILES[@]}"; do
  [[ -f "$f" ]] && ALL+=("$f")
done

if [[ ${#ALL[@]} -eq 0 ]]; then
  echo "no result files found." >&2
  exit 1
fi

python "$HERE/eval_elk_results.py" --results "${ALL[@]}" "$@"

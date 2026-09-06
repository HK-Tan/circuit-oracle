#!/usr/bin/env python3
"""
Rank SAE/transcoder features by cosine similarity with biased and unbiased probe weights.

For a given prompt, pass it through Gemma-2-2B, collect residual stream activations
at the dataset's probe layer, encode with a SAELens SAE or transcoder *of that same
layer*, then compute cosine similarity of each active feature's decoder direction
with the biased and unbiased probe weight vectors.  Save ranked results to
probe_artifacts/sae_features/ or probe_artifacts/plt_features/.

Layer handling (fixed 2026-07-26, was a real bug):
    The dictionary layer now tracks PROBE_LAYER[dataset] instead of being pinned to
    22.  Previously CivilComments (probe at layer 12) and MultiNLI (probe at layer
    17) had their residuals pushed through a layer-22 dictionary, which ranked
    features that are written *after* the probe reads and therefore cannot affect
    its score at all.  Measured against a random-direction null those two datasets
    scored 0.86x to 0.97x, i.e. indistinguishable from random, so 40 of the 80
    baseline items were ordered by noise.
    Each output file now records the layer and the exact dictionary id it was
    produced with, because judge_sae_features.py needs them to fetch matching
    Neuronpedia explanations.  Feature indices do not transfer across dictionaries.
    The transcoder id is layer specific (TRANSCODER_L0 below), since Gemma Scope
    publishes a different average-l0 suffix at every layer and only layer 22
    happens to have an average_l0_15.

Usage:
    python spurious-correlation/scripts/rank_sae_features_by_probe.py \
        --dataset bib_journalist_dietitian \
        --type sae          # or --type transcoder
        --prompt "She is a nurse."

    # Run all datasets with default sample prompt
    python spurious-correlation/scripts/rank_sae_features_by_probe.py --all
"""

import argparse
import json
import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MODEL_NAME  = "google/gemma-2-2b"
PROBE_LAYER = {
    "bib_nurse_professor": 22,
    "bib_journalist_dietitian": 22,
    "bib_surgeon_teacher": 22,
    "civil_comments": 12,
    "multinli": 17,
}
# This file lives in spurious-correlation/scripts/, so the task root (which holds
# prompts.json, probe_extraction/, and the feature output dirs) is one level up.
_HERE       = Path(__file__).resolve().parent
_TASK_ROOT  = _HERE.parent
DATASET_JSON = _TASK_ROOT / "prompts.json"
PROBE_DIR   = _TASK_ROOT / "probe_extraction" / "probes"
OUT_SAE_DIR = _TASK_ROOT / "probe_artifacts" / "sae_features"
OUT_PLT_DIR = _TASK_ROOT / "probe_artifacts" / "plt_features"
DEVICE      = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE       = torch.float32   # SAELens works in float32
print("Device set to:", DEVICE)
# SAELens release / SAE-id templates. The layer is filled in per dataset from
# PROBE_LAYER, never hardcoded: a dictionary at a layer above the probe's decomposes
# writes the probe never sees.
SAE_RELEASE           = "gemma-scope-2b-pt-res-canonical"
SAE_ID_TEMPLATE       = "layer_{layer}/width_16k/canonical"

TRANSCODER_RELEASE    = "gemma-scope-2b-pt-transcoders"
# The 16k transcoder's average-l0 suffix is layer specific in Gemma Scope, so no
# single template covers the three probe layers. The old
# "layer_{layer}/width_16k/average_l0_15" resolved only at layer 22 (which is why
# the earlier layer-22-everything run never hit this) and named a nonexistent
# folder at 12 and 17. These are the SAELens registry's one curated 16k id per
# layer, verified 2026-07-27 to be byte-identical to the hfFolderId behind
# Neuronpedia's {layer}-gemmascope-transcoder-16k sources, which is what keeps
# encoded feature indices aligned with the hosted explanations that
# judge_sae_features.py fetches.
TRANSCODER_L0 = {12: 6, 17: 12, 22: 15}


def transcoder_id(layer: int) -> str:
    """Curated 16k transcoder sae_id for ``layer``, raising on an unmapped layer."""
    if layer not in TRANSCODER_L0:
        raise KeyError(
            f"No curated 16k transcoder id recorded for layer {layer}. Look up the "
            f"SAELens registry entry for {TRANSCODER_RELEASE} at that layer, check "
            f"it matches Neuronpedia's {layer}-gemmascope-transcoder-16k source, "
            f"and add it to TRANSCODER_L0."
        )
    return f"layer_{layer}/width_16k/average_l0_{TRANSCODER_L0[layer]}"

DATASETS = [
    "bib_journalist_dietitian",
    "bib_nurse_professor",
    "bib_surgeon_teacher",
    "civil_comments",
    "multinli",
]

def parse_dataset_prompts(dataset: str) -> dict[str, list[str]]:
    """
    Read the prompt manifest (prompts.json) and return
    {'neg_neg': [...prompts...], 'pos_pos': [...prompts...]}
    for the given dataset.

    neg_neg = subgroup with (true=0, spurious=0)
    pos_pos = subgroup with (true=1, spurious=1)
    Up to 5 prompts per subgroup (takes the "Top N" listed ones).
    """
    prompt_dataset = json.load(open(DATASET_JSON, "r"))
    result = prompt_dataset[dataset]
    return result

# ---------------------------------------------------------------------------
# Probe loading
# ---------------------------------------------------------------------------

class Probe(nn.Module):
    def __init__(self, activation_dim: int, dtype=torch.bfloat16):
        super().__init__()
        self.net = nn.Linear(activation_dim, 1, bias=True, dtype=dtype)

    @property
    def weight_vec(self) -> torch.Tensor:
        return self.net.weight.squeeze(0).detach()


def load_probe(path: Path, device: str) -> Probe:
    checkpoint = torch.load(path, weights_only=True, map_location=device)
    probe = Probe(checkpoint["activation_dim"])
    probe.load_state_dict(checkpoint["state_dict"])
    return probe.eval()


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def get_resid_activations(prompt: str, model_tl, probe_layer: int) -> torch.Tensor:
    """Return PER-TOKEN residual stream activations at ``probe_layer``, shape (n_pos, d_model).

    Reads the same hook the probe is trained and scored on. Positions including BOS
    are all returned, and the caller averages AFTER encoding, which matches
    eval_probe_spuriosity.py's pooling, checked, so this is not a probe mismatch.

    Returns per token rather than mean-pooled (changed 2026-07-27). The caller used
    to average here and encode the mean, which is wrong for a thresholded encoder:
    the dictionary was trained on real per-token residuals, and the centroid of a
    sequence is not one of those. Token vectors partially cancel, so the mean has a
    much smaller norm than a typical token and clears far fewer JumpReLU thresholds.
    Measured on the archived files: the residual SAE reported a median of 7 to
    14 active features and fewer than 20 on 39 of 40 prompts, so the top-20 selection
    in judge_sae_features.py returned everything and the cosine ranking never ranked.
    A feature firing hard on one token (a gender cue, which is the whole point of this
    task) was diluted below threshold and vanished entirely.
    """
    hook_name = f"blocks.{probe_layer}.hook_resid_post"
    tokens = model_tl.to_tokens(prompt, prepend_bos=True)
    with torch.no_grad():
        _, cache = model_tl.run_with_cache(tokens, names_filter=hook_name)
    h = cache[hook_name]          # (1, n_pos, d_model)
    return h[0].to(DTYPE)         # (n_pos, d_model)


def rank_features(
    prompt: str,
    dataset: str,
    sae_type: str,   # "sae" or "transcoder"
    model_tl,
    sae_or_transcoder,
    probe_biased: Probe,
    probe_unbiased: Probe,
    layer: int,
    sae_id: str,
) -> dict:
    """Run one prompt, return a dict with ranked feature info."""

    # 1. Residual stream activations at the probe's own layer, per token
    acts = get_resid_activations(prompt, model_tl, layer)   # (n_pos, d_model)
    acts_device = acts.to(DEVICE)

    # 2. Encode EVERY token, then average the activations. Encode-then-average, not
    #    average-then-encode: the encoder is nonlinear (JumpReLU threshold), so
    #    encode(mean) != mean(encode), and only the latter is the probe's own
    #    decomposition. The probe scores w . (1/T sum_t h_t), and substituting the
    #    per-token reconstruction h_t ~ b_dec + sum_F a_{F,t} W_dec[F] gives
    #    score ~ const + sum_F abar_F (w . W_dec[F]) with abar_F the MEAN activation
    #    over tokens. So this mean is forced by how the probe pools, not a free knob.
    #    No token is selected, every position contributes.
    with torch.no_grad():
        feature_acts = sae_or_transcoder.encode(acts_device)  # (n_pos, n_features)
    feature_acts = feature_acts.mean(dim=0)  # (n_features,)

    # 3. Find active features (activation > 0)
    active_mask = feature_acts > 0
    active_indices = active_mask.nonzero(as_tuple=True)[0].tolist()

    if len(active_indices) == 0:
        return {
            "prompt": prompt,
            "dataset": dataset,
            "type": sae_type,
            "layer": layer,
            "sae_id": sae_id,
            "n_active": 0,
            "features": [],
        }
    else:
        print(f"active_indices: {len(active_indices)}")
    # 4. Get decoder directions for active features
    # W_dec shape in SAELens: (n_features, d_model)
    W_dec = sae_or_transcoder.W_dec  # (n_features, d_model)
    dec_dirs = W_dec[active_indices]  # (n_active, d_model)
    dec_dirs_f32 = dec_dirs.to(DTYPE)

    # 5. Probe weight vectors (d_model,), normalise for cosine similarity
    w_biased   = probe_biased.weight_vec.to(DTYPE).to(DEVICE)
    w_unbiased = probe_unbiased.weight_vec.to(DTYPE).to(DEVICE)

    cos_biased   = F.cosine_similarity(dec_dirs_f32, w_biased.unsqueeze(0),   dim=-1)
    cos_unbiased = F.cosine_similarity(dec_dirs_f32, w_unbiased.unsqueeze(0), dim=-1)

    cos_biased_list   = cos_biased.cpu().tolist()
    cos_unbiased_list = cos_unbiased.cpu().tolist()
    activations_list  = feature_acts[active_indices].cpu().tolist()

    # 6. Build ranked lists (descending by cosine sim)
    rank_by_biased   = sorted(range(len(active_indices)), key=lambda i: -cos_biased_list[i])
    rank_by_unbiased = sorted(range(len(active_indices)), key=lambda i: -cos_unbiased_list[i])

    rank_biased_map   = {i: r for r, i in enumerate(rank_by_biased)}
    rank_unbiased_map = {i: r for r, i in enumerate(rank_by_unbiased)}

    features = []
    for i, feat_idx in enumerate(active_indices):
        features.append({
            "feature_idx":      feat_idx,
            "activation":       activations_list[i],
            "cos_sim_biased":   cos_biased_list[i],
            "cos_sim_unbiased": cos_unbiased_list[i],
            "rank_biased":      rank_biased_map[i],
            "rank_unbiased":    rank_unbiased_map[i],
        })

    # Sort by rank_biased for readability
    features.sort(key=lambda f: f["rank_biased"])

    return {
        "prompt":   prompt,
        "dataset":  dataset,
        "type":     sae_type,
        # Provenance of the feature indices below. judge_sae_features.py reads these
        # to fetch matching Neuronpedia explanations, and fails loudly if absent,
        # because index 4711 at layer 12 is an unrelated feature to index 4711 at
        # layer 22.
        "layer":    layer,
        "sae_id":   sae_id,
        "n_active": len(active_indices),
        "features": features,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Rank SAE/transcoder features by probe cosine similarity")
    parser.add_argument("--dataset", default=None, choices=DATASETS, help="Dataset slug")
    parser.add_argument("--type",    default="transcoder", choices=["sae", "transcoder", "both"],
                        help="Use residual SAE or transcoder, or 'both' to produce the two "
                             "baselines in ONE process (default: transcoder)")
    parser.add_argument("--all",     action="store_true", help="Run all datasets")
    args = parser.parse_args()

    if not args.all and args.dataset is None:
        parser.error("Provide --dataset or --all")

    datasets = DATASETS if args.all else [args.dataset]
    # 'both' exists because the two baselines differ ONLY in which dictionary the
    # residuals are encoded with. Running the script twice re-downloads and
    # re-loads Gemma-2-2B for the second type, and that load is most of this
    # stage's wall clock, since the actual work is 80 forward passes on short
    # prompts. Sharding across GPUs would be worse still: every worker pays the
    # download again, and downloads are the bottleneck, not compute.
    types = ["sae", "transcoder"] if args.type == "both" else [args.type]

    # --- Load model (shared across datasets) ---
    print(f"Loading {MODEL_NAME} via transformer_lens...", flush=True)
    import transformer_lens
    model_tl = transformer_lens.HookedTransformer.from_pretrained(
        MODEL_NAME,
        dtype=DTYPE,
        device=DEVICE,
    )
    model_tl.eval()
    print("Model loaded.", flush=True)

    # --- Dictionary loader, keyed on (type, layer) ---
    # One dictionary per distinct (type, probe layer), not one per run. The three
    # bib_* datasets all sit at layer 22 and share a load; civil_comments (12) and
    # multinli (17) each get their own. The type is in the key because --type both
    # keeps sae and transcoder dictionaries alive in the same process.
    _dict_cache: dict[tuple[str, int], object] = {}

    def load_dictionary(sae_type: str, layer: int):
        """Load (and memoize) the SAE or transcoder for ``layer``."""
        if (sae_type, layer) in _dict_cache:
            return _dict_cache[(sae_type, layer)]
        if sae_type == "sae":
            from sae_lens import SAE
            sae_id = SAE_ID_TEMPLATE.format(layer=layer)
            print(f"Loading SAE: {SAE_RELEASE} / {sae_id}", flush=True)
            obj = SAE.from_pretrained(SAE_RELEASE, sae_id, device=DEVICE)
        else:
            from sae_lens import Transcoder
            sae_id = transcoder_id(layer)
            print(f"Loading transcoder: {TRANSCODER_RELEASE} / {sae_id}", flush=True)
            obj = Transcoder.from_pretrained(TRANSCODER_RELEASE, sae_id, device=DEVICE)
        obj.eval()
        print(f"  loaded, W_dec shape: {obj.W_dec.shape}", flush=True)
        _dict_cache[(sae_type, layer)] = obj
        return obj

    def dictionary_id(sae_type: str, layer: int) -> str:
        if sae_type == "sae":
            return SAE_ID_TEMPLATE.format(layer=layer)
        return transcoder_id(layer)

    for dataset in datasets:
        layer = PROBE_LAYER[dataset]
        print(f"\n--- Dataset: {dataset} (probe layer {layer}) ---", flush=True)

        # Probes depend on the dataset only, never on the dictionary type, so they
        # load once and are reused across both types.
        biased_path   = PROBE_DIR / f"{dataset}_layer{layer}_bfloat16.pt"
        unbiased_path = PROBE_DIR / f"{dataset}_layer{layer}_bfloat16_unbiased.pt"
        assert biased_path.exists(),   f"Not found: {biased_path}"
        assert unbiased_path.exists(), f"Not found: {unbiased_path}"

        probe_biased   = load_probe(biased_path,   DEVICE)
        probe_unbiased = load_probe(unbiased_path, DEVICE)
        print(f"Probes loaded.", flush=True)

        prompt_ds = parse_dataset_prompts(dataset)

        for sae_type in types:
            out_dir = OUT_SAE_DIR if sae_type == "sae" else OUT_PLT_DIR
            out_dir.mkdir(parents=True, exist_ok=True)
            sae    = load_dictionary(sae_type, layer)
            sae_id = dictionary_id(sae_type, layer)

            for prompt_type, prompts in prompt_ds.items():
                for idx, prompt in enumerate(prompts):
                    print(f"[{sae_type}] {prompt_type}_{idx+1} Prompt: {prompt[:80]}...",
                          flush=True)

                    result = rank_features(
                        prompt=prompt,
                        dataset=dataset,
                        sae_type=sae_type,
                        model_tl=model_tl,
                        sae_or_transcoder=sae,
                        probe_biased=probe_biased,
                        probe_unbiased=probe_unbiased,
                        layer=layer,
                        sae_id=sae_id,
                    )

                    out_path = out_dir / f"{dataset}-{prompt_type}_{idx+1}-{sae_type}.json"
                    with open(out_path, "w") as f:
                        json.dump(result, f, indent=2)
                    print(f"Saved {result['n_active']} active features -> {out_path}",
                          flush=True)

                    # The top-20 cutoff in judge_sae_features.py silently returns the
                    # WHOLE active set when fewer than 20 features fire, which makes
                    # the biased and unbiased lists identical and the baseline
                    # unmeasurable. That is exactly what the pre-2026-07-27 residual
                    # SAE artifacts did, on 39 of 40 prompts. Say so at build time
                    # rather than discovering it downstream in the verdicts.
                    if result["n_active"] < 20:
                        print(f"  WARNING: only {result['n_active']} active features "
                              f"(< top-20 cutoff), so the biased and unbiased lists "
                              f"will be IDENTICAL for this prompt.", flush=True)

    print("\nDone.", flush=True)


if __name__ == "__main__":
    main()

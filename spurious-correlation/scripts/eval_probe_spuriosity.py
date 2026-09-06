"""
Score all 4 subgroups with both probes and print stats + top-5 most confident prompts.

The report is appended to spurious-correlation/runs/spuriosity/analysis.md.

Usage (from anywhere):
    python spurious-correlation/scripts/eval_probe_spuriosity.py --dataset civil_comments
    python spurious-correlation/scripts/eval_probe_spuriosity.py --dataset bib_nurse_professor

"""
import argparse
import sys
from pathlib import Path

import dotenv

# This file lives in spurious-correlation/scripts/, so the task root (which holds
# adapters/, probe_extraction/, runs/) is one level up and the repo
# root is two.
_HERE = Path(__file__).resolve().parent
_TASK_ROOT = _HERE.parent
_REPO_ROOT = _TASK_ROOT.parent
# Repo-root .env. Absent is fine when the variables are already exported.
dotenv.load_dotenv(_REPO_ROOT / ".env")

import torch
from torch import nn
from tqdm import tqdm

# Import path for the `adapters` package, which sits at the task root.
sys.path.insert(0, str(_TASK_ROOT))

from circuit_tracer import ReplacementModel
from adapters import BiasInBiosAdapter, CivilCommentsAdapter, MultiNLIAdapter

DEVICE      = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE       = torch.bfloat16

PROBES_DIR  = _TASK_ROOT / "probe_extraction" / "probes"
MODEL_NAME  = "google/gemma-2-2b"
# Appended to, so it goes under the gitignored runs/ rather than into the
# committed probe_artifacts/spuriosity/ archive.
OUT_MD      = _TASK_ROOT / "runs" / "spuriosity" / "analysis.md"
TOP_N       = 20

DATASETS = {
    "civil_comments":           {"adapter": lambda: CivilCommentsAdapter(activation_dim_value=2304), "layer": 12},
    "multinli":                 {"adapter": lambda: MultiNLIAdapter(activation_dim_value=2304), "layer": 17},
    "bib_nurse_professor":      {"adapter": lambda: BiasInBiosAdapter(neg_profession="professor", pos_profession="nurse",       activation_dim_value=2304), "layer": 22},
    "bib_surgeon_teacher":      {"adapter": lambda: BiasInBiosAdapter(neg_profession="surgeon",   pos_profession="teacher",     activation_dim_value=2304), "layer": 22},
    "bib_journalist_dietitian": {"adapter": lambda: BiasInBiosAdapter(neg_profession="journalist", pos_profession="dietitian",  activation_dim_value=2304), "layer": 22},
}


# ── Probe ──────────────────────────────────────────────────────────────────────
class Probe(nn.Module):
    def __init__(self, activation_dim, dtype=DTYPE):
        super().__init__()
        self.net = nn.Linear(activation_dim, 1, bias=True, dtype=dtype)

    def forward(self, x):
        return self.net(x).squeeze(-1)


def load_probe(path):
    ckpt = torch.load(path, map_location="cpu", weights_only=True)
    dtype = {"bfloat16": torch.bfloat16, "float16": torch.float16, "float32": torch.float32}[ckpt["dtype"]]
    probe = Probe(ckpt["activation_dim"], dtype=dtype)
    probe.load_state_dict(ckpt["state_dict"])
    return probe.to(DEVICE).eval()


# ── Scoring ────────────────────────────────────────────────────────────────────
@torch.no_grad()
def score_all(texts, model, probe, layer, batch_size=8):
    hook = f"blocks.{layer}.hook_resid_post"
    scores = []
    for i in tqdm(range(0, len(texts), batch_size), desc="scoring", leave=False):
        batch = texts[i : i + batch_size]
        tokens = model.tokenizer(batch, return_tensors="pt", padding=True, truncation=True, 
                                #  add_special_tokens=False
                                 ).to(DEVICE)
        mask = tokens["attention_mask"].float()
        _, cache = model.run_with_cache(tokens["input_ids"], names_filter=hook, 
                                        # prepend_bos=False
                                        )
        h = cache[hook]
        pooled = (h * mask.unsqueeze(-1)).sum(1) / mask.sum(1, keepdim=True)
        scores.extend(probe(pooled.to(DTYPE)).cpu().tolist())
    return scores


# ── Helpers ────────────────────────────────────────────────────────────────────
def get_subgroup_texts(adapter, true_label, spurious_label, split="test"):
    batched = adapter.get_subgroups(split=split, batch_size=8, balance=False)
    batches = batched.get((true_label, spurious_label), [])
    return [text for batch in batches for text in batch[0]]


def subgroup_label(adapter, true_label, spurious_label):
    if isinstance(adapter, BiasInBiosAdapter):
        prof   = adapter.pos_profession if true_label == 1 else adapter.neg_profession
        gender = "female" if spurious_label == 1 else "male"
        return f"{gender} {prof}"
    if isinstance(adapter, CivilCommentsAdapter):
        return ("toxic" if true_label == 1 else "non-toxic") + ", " + ("+identity-attack" if spurious_label == 1 else "no identity-attack")
    if isinstance(adapter, MultiNLIAdapter):
        return ("contradiction" if true_label == 1 else "entailment") + ", " + ("+negation" if spurious_label == 1 else "no negation")
    return f"target={true_label}, spurious={spurious_label}"


def top_prompts(texts, scores_b, scores_u, true_label, spurious_label, n=TOP_N):
    """
    For pos_pos and neg_neg only: top-n prompts where:
      1. Both probes are correct
      2. Unbiased is above its median (strong causal signal, not a fluke)
      3. Biased is more confident than unbiased (spurious boost on top)
    Ranked by confidence gap: |biased| - |unbiased|.
    """
    if true_label != spurious_label:
        return []   # skip pos_neg and neg_pos
    sign = 1 if true_label == 1 else -1

    # median unbiased confidence among correctly-predicted examples
    u_correct = [abs(u) for b, u in zip(scores_b, scores_u) if b * sign > 0 and u * sign > 0]
    if not u_correct:
        return []
    u_median = sorted(u_correct)[len(u_correct) // 2]

    candidates = [
        (t, b, u)
        for t, b, u in zip(texts, scores_b, scores_u)
        if b * sign > 0 and u * sign > 0   # both correct
        and abs(u) >= u_median              # unbiased has strong causal signal
        and abs(b) > abs(u)                 # biased adds on top
    ]
    ranked = sorted(candidates, key=lambda x: abs(x[1]) - abs(x[2]), reverse=True)
    return ranked[:n]


# ── Output (print + collect for markdown) ─────────────────────────────────────
_lines = []

def emit(line=""):
    print(line, flush=True)
    _lines.append(line)


# ── Stats block ────────────────────────────────────────────────────────────────
def report_subgroup(adapter, true_label, spurious_label, texts, scores_b, scores_u):
    n     = len(texts)
    label = subgroup_label(adapter, true_label, spurious_label)
    sign  = 1 if true_label == 1 else -1

    both_correct = sum(b * sign > 0 and u * sign > 0 for b, u in zip(scores_b, scores_u))
    neither      = sum(b * sign <= 0 and u * sign <= 0 for b, u in zip(scores_b, scores_u))
    b_only       = sum(b * sign > 0 and u * sign <= 0 for b, u in zip(scores_b, scores_u))
    u_only       = sum(b * sign <= 0 and u * sign > 0 for b, u in zip(scores_b, scores_u))

    emit(f"### Subgroup: {label}  (target={true_label}, spurious={spurious_label})")
    emit()
    emit(f"  n = {n}")
    emit(f"  Biased   mean score: {sum(scores_b)/n:+.3f}   % correct: {100*sum(s*sign>0 for s in scores_b)/n:.1f}%")
    emit(f"  Unbiased mean score: {sum(scores_u)/n:+.3f}   % correct: {100*sum(s*sign>0 for s in scores_u)/n:.1f}%")
    emit(f"  Both correct:   {both_correct:4d} / {n}  ({100*both_correct/n:.1f}%), causal signal strong enough for both")
    emit(f"  Neither correct:{neither:4d} / {n}  ({100*neither/n:.1f}%), too weak for either probe")
    emit(f"  Biased only:    {b_only:4d} / {n}  ({100*b_only/n:.1f}%)")
    emit(f"  Unbiased only:  {u_only:4d} / {n}  ({100*u_only/n:.1f}%)")
    emit()

    top = top_prompts(texts, scores_b, scores_u, true_label, spurious_label)
    if top:
        emit(f"#### Top {len(top)} prompts, both correct, biased more confident (spurious boost visible)")
        emit()
        for i, (text, sb, su) in enumerate(top, 1):
            gap = abs(sb) - abs(su)
            emit(f"  {i}. biased={sb:+.2f}  unbiased={su:+.2f}  gap={gap:+.2f}")
            emit(f"     \"{text}\"")
        # emit()


# ── Accuracy grid ──────────────────────────────────────────────────────────────
def cell_decision(cell_stats):
    """WORKS if both counter-stereotypic cells (0,1) and (1,0) have
    unbiased > biased + 20pp AND unbiased > 50%.  PARTIAL if one does.  FAILS otherwise."""
    passed = 0
    total  = 0
    for key in [(0, 1), (1, 0)]:
        if key not in cell_stats:
            continue
        total += 1
        s = cell_stats[key]
        if s["u_acc"] - s["b_acc"] > 20 and s["u_acc"] > 50:
            passed += 1
    if passed == total:
        return "WORKS"
    if passed > 0:
        return "PARTIAL"
    return "FAILS"


def emit_grid(cell_stats):
    W    = 32   # cell content width (handles long civil_comments labels)
    dash = "─" * W

    def fmt(key):
        s = cell_stats.get(key)
        if s is None:
            return [""] * 4
        label = s["label"]
        b     = f"{s['b_acc']:.1f}%"
        u     = f"{s['u_acc']:.1f}%"
        n     = f"{s['n']:,}"
        return [
            f"  {label:<{W-2}}",
            f"  {'Biased:   ' + b:<{W-2}}",
            f"  {'Unbiased: ' + u:<{W-2}}",
            f"  {'n = ' + n:<{W-2}}",
        ]

    tl = fmt((0, 0));  tr = fmt((0, 1))
    bl = fmt((1, 0));  br = fmt((1, 1))
    decision = cell_decision(cell_stats)

    emit("### Accuracy Grid")
    emit(f"┌{dash}┬{dash}┐")
    for l, r in zip(tl, tr):
        emit(f"│{l}│{r}│")
    emit(f"├{dash}┼{dash}┤")
    for l, r in zip(bl, br):
        emit(f"│{l}│{r}│")
    emit(f"└{dash}┴{dash}┘")
    emit(f"  Spurious pattern: {decision}")
    emit()

    # Average accuracies across all subgroups (to compare with train_probes.py eval)
    cells = [s for s in cell_stats.values() if s is not None]
    if cells:
        avg_b_true = sum(s["b_acc"] for s in cells) / len(cells)
        avg_u_true = sum(s["u_acc"] for s in cells) / len(cells)
        # Spurious label acc: correct if prediction matches spurious_label
        avg_b_spur = sum(s["b_spur_acc"] for s in cells) / len(cells)
        avg_u_spur = sum(s["u_spur_acc"] for s in cells) / len(cells)
        emit(f"  Biased  : true label acc: {avg_b_true:.1f}%   spurious label acc: {avg_b_spur:.1f}%")
        emit(f"  Unbiased: true label acc: {avg_u_true:.1f}%   spurious label acc: {avg_u_spur:.1f}%")
        emit()


# ── Main ───────────────────────────────────────────────────────────────────────
def run_dataset(slug, layer, adapter, model):
    probe_b = load_probe(PROBES_DIR / f"{slug}_layer{layer}_bfloat16.pt")
    probe_u = load_probe(PROBES_DIR / f"{slug}_layer{layer}_bfloat16_unbiased.pt")

    emit(f"## {slug}")
    emit()

    cell_stats = {}
    for true_label in [0, 1]:
        for spurious_label in [0, 1]:
            texts = get_subgroup_texts(adapter, true_label, spurious_label)
            if not texts:
                continue
            label = subgroup_label(adapter, true_label, spurious_label)
            print(f"  Scoring {label} ({len(texts)} examples)...", flush=True)
            scores_b = score_all(texts, model, probe_b, layer)
            scores_u = score_all(texts, model, probe_u, layer)
            torch.cuda.empty_cache()

            sign_true = 1 if true_label == 1 else -1
            sign_spur = 1 if spurious_label == 1 else -1
            n    = len(texts)
            cell_stats[(true_label, spurious_label)] = {
                "label": label,
                "n":     n,
                "b_acc":      100 * sum(s * sign_true > 0 for s in scores_b) / n,
                "u_acc":      100 * sum(s * sign_true > 0 for s in scores_u) / n,
                "b_spur_acc": 100 * sum(s * sign_spur > 0 for s in scores_b) / n,
                "u_spur_acc": 100 * sum(s * sign_spur > 0 for s in scores_u) / n,
            }

            report_subgroup(adapter, true_label, spurious_label, texts, scores_b, scores_u)

    emit_grid(cell_stats)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="all", choices=list(DATASETS) + ["all"])
    args = parser.parse_args()

    to_run = list(DATASETS.items()) if args.dataset == "all" else [(args.dataset, DATASETS[args.dataset])]

    print("Loading model...", flush=True)
    model = ReplacementModel.from_pretrained(MODEL_NAME, "gemma", dtype=DTYPE, backend="transformerlens")

    emit("# Probe Spuriosity Analysis")
    emit()

    for slug, detail in to_run:
        run_dataset(slug, detail['layer'], detail['adapter'](), model)

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    # OUT_MD.write_text("\n".join(_lines) + "\n")
    with OUT_MD.open("a") as f:
        f.write("\n".join(_lines) + "\n")
    print(f"\nWritten to {OUT_MD}", flush=True)


if __name__ == "__main__":
    main()

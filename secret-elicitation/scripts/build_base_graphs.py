#!/usr/bin/env python3
"""Build the same-prompt BASE-model attribution graphs (no LoRA).

RECONSTRUCTION NOTICE. This script is NOT the original. The script that
produced the archived qwen3-8b-base-NN-None.pt siblings was never committed
to any repository and the original procedure is unrecoverable. What follows
is build_taboo_graphs.py with the PEFT merge removed, sharing its prompts,
its attribute() parameters and its slug convention, which is the strongest
reconstruction the surviving evidence supports. Graphs it produces are a
fresh era, do not mix them with archived siblings inside one comparison.

Each of the 6 PROMPT_PAIRS gives one graph, saved as
<GRAPH_STORE>/graphs/qwen3-8b-base-{NN}-None.pt (NN is 1-based, zero padded),
which is the BASE_GRAPH_TEMPLATE the taboo runners glob for.
"""

import argparse
import os
import time
from pathlib import Path

import torch
from transformers import AutoTokenizer

from circuit_tracer import ReplacementModel, attribute

from taboo_env import default_env_path, load_env_file
from build_taboo_graphs import (
    BASE_NAME,
    DEFAULT_BATCH_SIZE,
    DEFAULT_MAX_FEATURE_NODES,
    PROMPT_PAIRS,
    TRANSCODER_NAME,
    format_prompt,
)

_HERE = Path(__file__).resolve().parent
_THREAD = _HERE.parent  # secret-elicitation/, the thread root above scripts/
SLUG_TEMPLATE = "qwen3-8b-base-{idx:02d}-None"


# Resolved per call, not cached in a module constant: main() reads the .env, so
# a GRAPH_STORE set only there is not in os.environ yet at import time. Same
# convention as build_taboo_graphs.py and the two runners.
def graphs_dir() -> Path:
    return Path(os.environ.get("GRAPH_STORE", str(_THREAD))) / "graphs"

DTYPE = torch.bfloat16
DEVICE = "cuda"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    ap.add_argument("--max-feature-nodes", type=int,
                    default=DEFAULT_MAX_FEATURE_NODES)
    ap.add_argument("--env-file", default=None,
                    help="KEY=VALUE file holding GRAPH_STORE and HF_TOKEN "
                         "(default: $ORACLE_ENV_FILE, else a .env at the repo "
                         "root). Same file and same precedence as the two "
                         "taboo runners use.")
    args = ap.parse_args()

    # BEFORE anything reads GRAPH_STORE or HF_TOKEN. Without this the build
    # ignores a store path set only in .env and writes the graphs somewhere the
    # runners never look.
    load_env_file(Path(args.env_file) if args.env_file else default_env_path())

    graphs = graphs_dir()
    graphs.mkdir(parents=True, exist_ok=True)
    print(f"Graph store: {graphs}")
    tokenizer = AutoTokenizer.from_pretrained(BASE_NAME)

    todo = [
        (idx, graphs / f"{SLUG_TEMPLATE.format(idx=idx)}.pt")
        for idx in range(1, len(PROMPT_PAIRS) + 1)
    ]
    if all(pt_path.exists() for _, pt_path in todo):
        print("All base graphs exist, nothing to do.")
        return

    print(f"Loading base model {BASE_NAME} (no LoRA merge)...")
    print(f"Building ReplacementModel with transcoders {TRANSCODER_NAME}...")
    model = ReplacementModel.from_pretrained(
        BASE_NAME,
        TRANSCODER_NAME,
        backend="transformerlens",
        dtype=DTYPE,
        device=DEVICE,
        tokenizer=tokenizer,
    )
    print("Model ready.\n")

    for (idx, pt_path), (user_msg, assistant_prefix) in zip(todo, PROMPT_PAIRS):
        if pt_path.exists():
            print(f"[{idx}/{len(PROMPT_PAIRS)}] skipping, {pt_path.name} exists")
            continue
        prompt = format_prompt(tokenizer, user_msg, assistant_prefix)
        print(f"[{idx}/{len(PROMPT_PAIRS)}] prompt: {prompt!r}")

        t0 = time.time()
        graph = attribute(
            prompt=prompt,
            model=model,
            max_n_logits=10,
            desired_logit_prob=0.95,
            batch_size=args.batch_size,
            max_feature_nodes=args.max_feature_nodes,
            offload="cpu",
            verbose=False,
        )
        graph.to_pt(pt_path)
        print(f"          saved graph → {pt_path.name} "
              f"({time.time() - t0:.1f}s)\n")

    print("All base graphs processed.")


if __name__ == "__main__":
    main()

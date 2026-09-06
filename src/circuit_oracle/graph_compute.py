"""Model loading, prompt formatting, and attribution graph computation.

This is the only module that imports torch and circuit_tracer.
"""

import hashlib
import json
import os

import torch

try:
    from circuit_tracer.replacement_model import ReplacementModel
    from circuit_tracer.attribution.attribute import attribute
    from circuit_tracer.graph import Graph
except ModuleNotFoundError:
    # transformer_lens / circuit_tracer are GPU-stack-only. CPU-only test
    # environments monkeypatch `attribute` (and never reach the Graph path).
    ReplacementModel = None  # type: ignore[assignment,misc]
    attribute = None  # type: ignore[assignment]
    Graph = None  # type: ignore[assignment,misc]


def load_model(model_name: str, transcoder_name: str, dtype=torch.bfloat16):
    """Load a ReplacementModel with transcoders.

    Returns:
        model: ReplacementModel instance with .tokenizer attribute.
    """
    torch.cuda.empty_cache()
    model = ReplacementModel.from_pretrained(model_name, transcoder_name, dtype=dtype)
    print(f"Model loaded: {model.cfg.model_name}")
    print(f"Vocab size: {model.tokenizer.vocab_size}")
    return model


def format_chat(tokenizer, system_prompt: str, user_message: str, assistant_prefix: str = "") -> str:
    """Format messages using the model's chat template."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    formatted = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )
    if assistant_prefix:
        formatted += assistant_prefix
    return formatted


def format_chat_multiturn(tokenizer, system_prompt: str, messages: list[dict]) -> str:
    """Format a multi-turn conversation using the model's chat template.

    Args:
        tokenizer: The model's tokenizer.
        system_prompt: System prompt for the conversation.
        messages: List of {"role": "user"|"assistant", "content": "..."} dicts.

    Returns:
        Formatted prompt string ready for generation.
    """
    full_messages = [{"role": "system", "content": system_prompt}] + messages
    return tokenizer.apply_chat_template(
        full_messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )


def generate_response(prompt: str, model, max_new_tokens: int = 100) -> str:
    """Generate a response from the model and return only the newly generated tokens.

    Uses the HookedTransformer.generate() method which produces output identical
    to the original model (modifications only affect the backward pass).

    Greedy. `do_sample=False` is passed explicitly because
    `HookedTransformer.generate` defaults to `do_sample=True, temperature=1.0`,
    and omitting it made this the one sampled decode in an otherwise
    deterministic comparison: every intervened decode goes through
    `tools._decode_greedy` (strict argmax), so a sampled baseline against a
    greedy intervened answer put noise on both the before/after diff and the
    5x-repeat stability metrics, which hold the graph fixed on purpose and
    attribute all remaining variation to the oracle. It also makes
    `ToolContext.baseline_answer`'s docstring ("greedy decoded answer under no
    intervention") true.
    """
    input_ids = model.tokenizer(prompt, return_tensors="pt")["input_ids"].to(model.cfg.device)
    prompt_len = input_ids.shape[1]
    # use_past_kv_cache=False avoids a TransformerLens dtype mismatch in the
    # GQA + RoPE + bfloat16 path on Qwen3-4B. The KV cache crosses fp32 RoPE
    # buffers with bf16 keys, tripping `q_ @ k_` with "expected Float but
    # found BFloat16". Recomputing full-sequence forward per step is O(N^2)
    # but trivial at max_new_tokens=100 on short prompts.
    output_ids = model.generate(
        input_ids,
        max_new_tokens=max_new_tokens,
        stop_at_eos=True,
        use_past_kv_cache=False,
        do_sample=False,
    )
    new_ids = output_ids[0, prompt_len:]
    return model.tokenizer.decode(new_ids, skip_special_tokens=True)


def _topk_baseline(prompt: str, model, k: int = 5) -> dict:
    """Top-k next-token distribution at the last prompt position, frozen-attention.

    Mirrors `tools._topk_from_logits` exactly so the value cached here is
    byte-identical to the one `_measure_intervention` used to recompute.
    """
    logits, _ = model.feature_intervention(
        prompt, [], freeze_attention=True, return_activations=False,
    )
    last = logits[0, -1, :]
    probs = torch.softmax(last.float(), dim=-1)
    top_vals, top_ids = probs.topk(k)
    tokenizer = model.tokenizer
    return {
        tokenizer.decode([tid.item()]): {"prob": round(p.item(), 6)}
        for tid, p in zip(top_ids, top_vals)
    }


def _save_graph(graph, cache_path: str) -> None:
    """Persist a graph object. Prefer `graph.to_pt` (circuit_tracer Graph);
    fall back to `torch.save` for duck-typed test graphs without `to_pt`.
    """
    if hasattr(graph, "to_pt"):
        graph.to_pt(cache_path)
    else:
        torch.save(graph, cache_path)


def _load_graph(cache_path: str):
    """Inverse of `_save_graph`. Tries `Graph.from_pt` first (real graphs),
    then `torch.load` (test graphs that lack `from_pt`).
    """
    if Graph is not None:
        try:
            return Graph.from_pt(cache_path)
        except Exception:
            pass
    return torch.load(cache_path, weights_only=False)


def _prompt_digest(prompt: str) -> str:
    """Stable content hash of the exact formatted prompt a graph was built from."""
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


class GraphCacheMismatch(RuntimeError):
    """A cached graph was built from different inputs than the caller asked for."""


def _verify_cache_key(
    baseline_meta: dict,
    prompt: str,
    max_feature_nodes: int | None,
    cache_path: str,
) -> None:
    """Refuse a cache hit whose recorded build inputs differ from this call's.

    The cache key is the slug string alone, which is weaker than it looks. The
    slug says nothing about the prompt text or the feature-node cap, so editing
    a `user_message` in `prompts.json` while a warm `.pt` sits in the store used
    to make the run analyze the OLD prompt's graph while intervening on the NEW
    prompt, silently. Same for reusing a slug across feature-node generations
    (10 of the 50 refusal slugs collide by name with the archived 10000-cap
    sweep era).

    Provenance is only written when this process actually computed the graph,
    so a `.baseline.json` that predates this guard, or one regenerated beside a
    `.pt` of unknown origin, has no keys to check. Those warn rather than raise:
    we do not know they are wrong, and pretending otherwise would block every
    archived graph. A recorded value that disagrees is a hard error.
    """
    # Each key is checked on its own. The two are written together, so a file
    # carrying one and not the other is hand-edited or half-written, and in that
    # case the key that IS present is still worth enforcing. `None` is a real
    # recorded value for the cap (unbounded, what `--max-feature-nodes 0` maps
    # to), so absence needs a sentinel rather than a None check.
    absent = object()
    recorded_hash = baseline_meta.get("prompt_sha256", absent)
    recorded_cap = baseline_meta.get("max_feature_nodes", absent)

    if recorded_hash is absent and recorded_cap is absent:
        print(
            f"WARNING: {cache_path} has no build provenance recorded "
            "(pre-guard cache, or a graph whose baselines were regenerated "
            "separately). Cannot verify the prompt text or the feature-node cap "
            "against this run. Delete the .pt and its .baseline.* siblings to "
            "rebuild with provenance."
        )
        return

    if recorded_hash is not absent:
        actual_hash = _prompt_digest(prompt)
        if recorded_hash != actual_hash:
            raise GraphCacheMismatch(
                f"{cache_path} was built from a different prompt "
                f"(recorded sha256 {recorded_hash[:12]}, this run's {actual_hash[:12]}). "
                "The graph would be analyzed while interventions replay the new prompt. "
                "Delete the .pt and its .baseline.pt / .baseline.json siblings to rebuild."
            )

    if recorded_cap is not absent and recorded_cap != max_feature_nodes:
        raise GraphCacheMismatch(
            f"{cache_path} was built with max_feature_nodes={recorded_cap}, "
            f"this run asked for {max_feature_nodes}. Feature-node generations "
            "must not be mixed inside one comparison. Pass the recorded cap, or "
            "delete the .pt and its .baseline.* siblings to rebuild."
        )


def compute_or_load_graph(
    prompt: str,
    model,
    cache_path: str | None = None,
    max_feature_nodes: int | None = None,
) -> dict:
    """Compute an attribution graph, or load from cache if available.

    Args:
        prompt: Formatted prompt string.
        model: ReplacementModel instance.
        cache_path: Optional path to cache the graph as a .pt file.
        max_feature_nodes: Cap on the number of feature nodes included in the
            graph. ``None`` means unbounded (every active feature is included,
            which can be tens of thousands for long prompts). A cap like 5000
            trades completeness for much faster attribution. Passed straight
            through to ``circuit_tracer.attribute``.

    Returns:
        Dict with keys: graph, replacement_model, baseline_activations,
        baseline_answer, baseline_top5.
    """
    if cache_path:
        os.makedirs(os.path.dirname(cache_path) or ".", exist_ok=True)

    baseline_pt_path = f"{cache_path}.baseline.pt" if cache_path else None
    baseline_json_path = f"{cache_path}.baseline.json" if cache_path else None

    cache_hit = (
        cache_path is not None
        and os.path.exists(cache_path)
        and baseline_pt_path is not None
        and os.path.exists(baseline_pt_path)
        and baseline_json_path is not None
        and os.path.exists(baseline_json_path)
    )

    # Provenance is recorded only for a graph this call computed. A graph read
    # off disk in the partial-cache branch below has unknown build inputs, and
    # stamping the caller's arguments onto it would turn "unverifiable" into a
    # false "verified".
    graph_computed_here = False

    # Any recorded provenance is read and checked BEFORE the cache_hit split,
    # because the partial-cache branch regenerates and overwrites this file. Do
    # it only there and a .pt whose .baseline.pt went missing would skip its own
    # verification and then have its valid provenance erased by the rewrite,
    # leaving a permanently unverifiable graph that every later run waves
    # through with a warning. Read once, verify once, carry forward below.
    recorded_meta: dict = {}
    if cache_path and os.path.exists(cache_path) and baseline_json_path and os.path.exists(baseline_json_path):
        with open(baseline_json_path) as fh:
            recorded_meta = json.load(fh)
        _verify_cache_key(recorded_meta, prompt, max_feature_nodes, cache_path)

    if cache_hit:
        print(f"Loading cached graph from {cache_path}...")
        baseline_meta = recorded_meta
        graph = _load_graph(cache_path)
        baseline_acts = torch.load(baseline_pt_path, weights_only=False)
        baseline_top5 = baseline_meta["baseline_top5"]
        baseline_answer = baseline_meta["baseline_answer"]
    else:
        if cache_path and os.path.exists(cache_path):
            print(f"Loading cached graph from {cache_path}...")
            graph = _load_graph(cache_path)
        else:
            cap_msg = "unbounded" if max_feature_nodes is None else f"cap={max_feature_nodes}"
            print(f"Computing attribution graph (this may take several minutes, feature-node {cap_msg})...")
            graph = attribute(
                prompt,
                model,
                offload="cpu",
                verbose=True,
                max_feature_nodes=max_feature_nodes,
            )
            graph_computed_here = True

            if cache_path:
                _save_graph(graph, cache_path)
                print(f"Saved graph to {cache_path}")

        _, baseline_acts = model.get_activations(prompt)
        baseline_top5 = _topk_baseline(prompt, model)
        baseline_answer = generate_response(prompt, model, max_new_tokens=100).strip("\n")

        if cache_path:
            torch.save(baseline_acts, baseline_pt_path)
            baseline_meta = {
                "baseline_top5": baseline_top5,
                "baseline_answer": baseline_answer,
            }
            if graph_computed_here:
                baseline_meta["prompt_sha256"] = _prompt_digest(prompt)
                baseline_meta["max_feature_nodes"] = max_feature_nodes
            else:
                # Regenerating baselines beside a .pt someone else built. Carry
                # any provenance the old record held rather than dropping it:
                # it was verified above, and losing it would silently downgrade
                # a checkable graph to an uncheckable one.
                for key in ("prompt_sha256", "max_feature_nodes"):
                    if key in recorded_meta:
                        baseline_meta[key] = recorded_meta[key]
            with open(baseline_json_path, "w") as fh:
                json.dump(baseline_meta, fh)
            print(f"Saved baseline cache to {baseline_pt_path} + {baseline_json_path}")

    return {
        "graph": graph,
        "replacement_model": model,
        "baseline_activations": baseline_acts,
        "baseline_answer": baseline_answer,
        "baseline_top5": baseline_top5,
    }

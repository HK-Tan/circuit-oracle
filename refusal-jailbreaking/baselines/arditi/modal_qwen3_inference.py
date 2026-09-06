"""Ad-hoc Qwen3-4B inference via Modal (vLLM, A10G).

The chat formatting here ALWAYS includes the system role, even when the system
prompt is empty, exactly like circuit_oracle.graph_compute.format_chat. An
earlier version dropped the system message when empty, which produces a
different token string than the one the attribution graphs are built on. The
prompt screen for the 50-prompt refusal set has to test the exact build-path
string, so that divergence matters here even though it did not matter for the
ad-hoc eyeballing this script started as.

Uses (both local-runnable, compute is remote on Modal):
  - Prompt screening for the refusal eval set (scripts/build_prompt_set.py screen).
  - Ad-hoc eyeballing of baseline behavior across N samples.

Deploy once, then invoke ad-hoc:
  modal deploy baselines/arditi/modal_qwen3_inference.py
  python baselines/arditi/modal_qwen3_inference.py "Some prompt" --max-tokens 200 --n 3

Reuses the persistent weight volume `qwen3-4b-weights` and the app name
`qwen3-4b-inference` from the dev fork, so no re-download and no second app.
Redeploying from this path replaces the old deployment in place.
Uses `enable_thinking=False` (no <think> traces).
"""
import argparse
import json
import sys
import time

# Not deferrable: the app, its image and its class are all defined at module
# level against this import, so there is nothing to run without it.
try:
    import modal
except ImportError:
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__)
        raise SystemExit(0)
    raise SystemExit(
        "modal_qwen3_inference needs the screen extra: "
        "pip install 'circuit-oracle[screen]'"
    )

QWEN3_MODEL = "Qwen/Qwen3-4B"
VOLUME_NAME = "qwen3-4b-weights"
APP_NAME = "qwen3-4b-inference"
CLASS_NAME = "Qwen3Inference"
MAX_RETRIES = 3
RETRY_BASE_DELAY = 2.0

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "vllm>=0.6.3",
        "transformers>=4.44",
        "huggingface-hub",
        "hf-transfer",
    )
    .env({
        "HF_HUB_ENABLE_HF_TRANSFER": "1",
        "HF_HOME": "/cache/hf",
    })
)

volume = modal.Volume.from_name(VOLUME_NAME, create_if_missing=True)
app = modal.App(APP_NAME, image=image)


@app.cls(
    gpu="A10G",
    volumes={"/cache": volume},
    scaledown_window=120,
    timeout=3600,
)
class Qwen3Inference:
    @modal.enter()
    def load(self):
        from vllm import LLM
        self.llm = LLM(model=QWEN3_MODEL, dtype="bfloat16", download_dir="/cache/hf")
        self.tokenizer = self.llm.get_tokenizer()

    @modal.method()
    def generate(
        self,
        prompts: list[str],
        system_prompt: str = "",
        max_tokens: int = 200,
        temperature: float = 0.7,
        top_p: float = 0.9,
        n: int = 1,
    ) -> list[dict]:
        from vllm import SamplingParams

        formatted = []
        for prompt in prompts:
            # Always include the system role, empty or not, matching
            # circuit_oracle.graph_compute.format_chat so the sampled string
            # is byte-identical to the one the attribution graph is built on.
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False,
            )
            formatted.append(text)

        params = SamplingParams(
            n=n,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        )
        outputs = self.llm.generate(formatted, params)
        results = []
        for prompt, out in zip(prompts, outputs, strict=True):
            samples = [c.text for c in out.outputs]
            results.append({
                "prompt": prompt,
                "samples": samples,
            })
        return results


def _call_with_retry(remote, **kwargs):
    delay = RETRY_BASE_DELAY
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return remote.generate.remote(**kwargs)
        except Exception as exc:
            if attempt == MAX_RETRIES:
                raise
            print(
                f"[modal retry {attempt}/{MAX_RETRIES}] {type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            time.sleep(delay)
            delay *= 2


def main():
    parser = argparse.ArgumentParser(
        description="Ad-hoc Qwen3-4B inference via deployed Modal app.",
    )
    parser.add_argument(
        "prompts",
        nargs="*",
        help="One or more prompts. Quote each.",
    )
    parser.add_argument(
        "--prompts-file",
        help="Path to a text file with one prompt per line (combined with positional prompts).",
    )
    parser.add_argument("--system-prompt", default="", help="Optional system prompt.")
    parser.add_argument("--max-tokens", type=int, default=200)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--n", type=int, default=1, help="Samples per prompt.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable.")
    args = parser.parse_args()

    prompts = list(args.prompts)
    if args.prompts_file:
        with open(args.prompts_file) as f:
            prompts.extend([line.rstrip("\n") for line in f if line.strip()])

    if not prompts:
        parser.error("Provide at least one prompt (positional) or --prompts-file")

    cls = modal.Cls.from_name(APP_NAME, CLASS_NAME)
    remote = cls()
    results = _call_with_retry(
        remote,
        prompts=prompts,
        system_prompt=args.system_prompt,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        n=args.n,
    )

    if args.json:
        print(json.dumps(results, indent=2))
        return

    for r in results:
        print("=" * 70)
        print(f"PROMPT: {r['prompt']}")
        for i, s in enumerate(r["samples"]):
            label = f"SAMPLE {i+1}" if len(r["samples"]) > 1 else "RESPONSE"
            print(f"--- {label} ---")
            print(s)


if __name__ == "__main__":
    main()

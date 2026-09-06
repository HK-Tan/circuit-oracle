"""Task 1 - the batch builder must cover every prompt in the manifest.

These pin the fix to the debug slice that capped the build at 20 of the 80
graphs (`run_extraction_batch.py` had `start_idx = 5`, `pos_pos[5:10]`, and
`neg_neg` commented out). That bug was silent at build time: it printed
"pos_pos prompts found: 0", exited 0, and the shortfall only surfaced much
later in `run_oracle_on_probes.reported_slugs()`, after the GPU had been paid
for and torn down.

Two things are pinned, and the second matters as much as the first. The run
list must cover the full manifest, AND the tag offset must be 1-based to match
`reported_slugs()`. They are coupled: the broken revision was internally
consistent (it labeled `prompts[5]` as `pos_pos_6`, correctly), so widening the
slice while leaving the offset at 6 would relabel every prompt by five under
filenames that still look valid. That is silent corruption rather than a loud
shortfall, so `test_tags_are_one_based` is the load-bearing one.

**Everything here calls the production `build_runs`.** An earlier draft
duplicated that logic into the test file, which made three of these assertions
tautological: production could revert to `enumerate(..., 6)` and they would all
still pass. `build_runs` was extracted out of `main()` specifically so the tests
exercise the real thing.

Offline. No model, no GPU, no subprocess.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

TASK_ROOT = Path(__file__).resolve().parents[1]
REPO = TASK_ROOT.parent
sys.path.insert(0, str(TASK_ROOT / "scripts"))
sys.path.insert(0, str(REPO / "src"))

import run_extraction_batch as reb  # noqa: E402  (path set above)

PROMPTS_JSON = TASK_ROOT / "prompts.json"

# The reported configuration, asserted here so a manifest edit that changes the
# headline denominator cannot pass silently. 40 prompts x biased/unbiased = 80.
REPORTED_PROMPTS = 40
REPORTED_GRAPHS = 80


@pytest.fixture(scope="module")
def manifest() -> dict:
    return json.loads(PROMPTS_JSON.read_text())


def test_source_has_no_debug_slice() -> None:
    """Cheap belt-and-braces against the exact old spelling returning.

    Weak on its own (a differently-spelled slice would pass), which is why the
    behavioural tests below exist. Kept because it names the specific
    regression.
    """
    src = (TASK_ROOT / "scripts" / "run_extraction_batch.py").read_text()
    assert "start_idx" not in src, "the debug slice start_idx is back"
    assert "neg_neg = []" not in src, "neg_neg is stubbed out again"


def test_manifest_is_the_reported_shape(manifest: dict) -> None:
    total = sum(len(sg["pos_pos"]) + len(sg["neg_neg"]) for sg in manifest.values())
    assert total == REPORTED_PROMPTS
    assert 2 * total == REPORTED_GRAPHS


def test_asymmetric_cells_are_intentional(manifest: dict) -> None:
    """The 5/5 vs 0/10 split is a design property, not a data gap.

    BiasInBios' spurious cue is categorical (gender is present either way), so
    both stereotype-consistent cells are usable. CivilComments' and MultiNLI's
    cues are presence-or-absence, so their neg_neg cell has no cue to lean on
    and contributes nothing. See spurious_probes.tex. Anyone "balancing" this
    table should trip here first.
    """
    for ds in ("bib_nurse_professor", "bib_journalist_dietitian"):
        assert len(manifest[ds]["pos_pos"]) == 5
        assert len(manifest[ds]["neg_neg"]) == 5
    for ds in ("civil_comments", "multinli"):
        assert len(manifest[ds]["pos_pos"]) == 10
        assert len(manifest[ds]["neg_neg"]) == 0
    # Dropped after probe-quality screening (spurious_probes_appendix.tex).
    assert manifest["bib_surgeon_teacher"] == {"neg_neg": [], "pos_pos": []}


def test_every_dataset_is_fully_covered(manifest: dict) -> None:
    """Per dataset, one run per prompt. The broken slice gave 0/0/5/5."""
    for dataset, prompts in manifest.items():
        expected = len(prompts["pos_pos"]) + len(prompts["neg_neg"])
        assert len(reb.build_runs(prompts)) == expected, dataset


def test_build_runs_pairs_each_tag_with_its_own_prompt(manifest: dict) -> None:
    """Tag N must carry prompt N-1, not prompt N-1+offset.

    This is what an offset regression corrupts: the counts stay right and the
    filenames stay valid, only the contents move. Checked against the manifest
    directly rather than against a re-derivation.
    """
    prompts = manifest["civil_comments"]
    runs = dict(reb.build_runs(prompts))
    for i, text in enumerate(prompts["pos_pos"], 1):
        assert runs[f"pos_pos_{i}"] == text


def test_tags_are_one_based(manifest: dict) -> None:
    """The load-bearing one. Tags must start at 1, not at start_idx + 1."""
    runs = reb.build_runs(manifest["civil_comments"])
    assert [tag for tag, _ in runs] == [f"pos_pos_{i}" for i in range(1, 11)]

    runs = reb.build_runs(manifest["bib_nurse_professor"])
    assert [tag for tag, _ in runs] == (
        [f"pos_pos_{i}" for i in range(1, 6)] + [f"neg_neg_{i}" for i in range(1, 6)]
    )


def test_empty_dataset_yields_no_runs(manifest: dict) -> None:
    """bib_surgeon_teacher contributes zero, and that must not be an error."""
    assert reb.build_runs(manifest["bib_surgeon_teacher"]) == []
    assert "bib_surgeon_teacher" in reb.VALID_DATASETS


def test_tags_match_reported_slugs(manifest: dict) -> None:
    """End to end: the builder's tags must reproduce the oracle's 80 slugs.

    This is the assertion that would have caught the bug immediately. The two
    sides derive the set independently, the builder by enumerating prompts and
    the oracle by enumerating the manifest, so agreement is real evidence.
    """
    import run_oracle_on_probes as rop

    built = {
        f"{dataset}-{tag}-{probe}-probe-{rop.REPORTED_METHOD}"
        for dataset, prompts in manifest.items()
        for tag, _ in reb.build_runs(prompts)
        for probe in ("biased", "unbiased")
    }
    assert built == set(rop.reported_slugs())
    assert len(built) == REPORTED_GRAPHS


def test_output_exists_rejects_empty_files(tmp_path, monkeypatch) -> None:
    """A zero-byte .pt must not count as a built graph.

    Graph.to_pt is a plain torch.save with no temp-then-rename, so an
    interrupted write can leave a stub that a bare .exists() would accept and
    --skip-existing would then refuse to rebuild.
    """
    monkeypatch.setattr(reb, "PROBE_CIRCUITS_DIR", tmp_path)
    biased = tmp_path / "civil_comments-pos_pos_1-biased-probe-correct.pt"
    unbiased = tmp_path / "civil_comments-pos_pos_1-unbiased-probe-correct.pt"

    assert not reb.output_exists("civil_comments", "pos_pos_1")

    biased.write_bytes(b"x")
    unbiased.write_bytes(b"")
    assert not reb.output_exists("civil_comments", "pos_pos_1"), "empty file accepted"

    unbiased.write_bytes(b"x")
    assert reb.output_exists("civil_comments", "pos_pos_1")

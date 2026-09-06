"""Task 1 - the 80-graph store verifier.

The debug-slice bug built 20 graphs while everyone believed 80, and the build
was quiet about it (exit 0, one easily missed "prompts found: 0" line). The
verifier closes that class: it derives the full expected file list from
prompts.json across every dataset, requires the derivation to come to exactly
80, and fails loudly on any absent or zero-byte .pt. Run on the pod via
``run_extraction_batch.py --verify-store`` before tearing the GPU down.

These tests import the module directly (it is subprocess-driver light, no
torch) and point ``verify_store`` at a temp directory, so they exercise the
real derivation against the real prompts.json.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

TASK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TASK_ROOT / "scripts"))

import run_extraction_batch as reb  # noqa: E402  (path set above)


def _populate(tmp: Path) -> list[Path]:
    """Create every expected .pt as a small non-empty file, return the list."""
    files = []
    for dataset in reb.VALID_DATASETS:
        prompts = reb.parse_dataset_prompts(dataset)
        for tag, _prompt in reb.build_runs(prompts):
            for p in reb.expected_graph_files(dataset, tag, tmp):
                p.write_bytes(b"not-a-real-graph")
                files.append(p)
    return files


def test_manifest_derives_exactly_80() -> None:
    n_expected, missing = reb.verify_store(Path("/nonexistent-store"))
    assert n_expected == reb.EXPECTED_TOTAL_GRAPHS == 80
    assert len(missing) == 80, "an empty store must report every graph missing"


def test_full_store_passes(tmp_path: Path) -> None:
    files = _populate(tmp_path)
    assert len(files) == 80
    n_expected, missing = reb.verify_store(tmp_path)
    assert n_expected == 80
    assert missing == []


def test_one_missing_file_fails(tmp_path: Path) -> None:
    files = _populate(tmp_path)
    files[37].unlink()
    _, missing = reb.verify_store(tmp_path)
    assert missing == [files[37]]


def test_zero_byte_file_fails(tmp_path: Path) -> None:
    files = _populate(tmp_path)
    files[0].write_bytes(b"")
    _, missing = reb.verify_store(tmp_path)
    assert missing == [files[0]]


def test_duplicate_expected_paths_raise(tmp_path: Path, monkeypatch) -> None:
    """The count must certify DISTINCT graphs (codex review 2026-07-27).

    Not reachable from a well-formed manifest, so this guards the guard: 80
    references to fewer than 80 files would otherwise pass the count.
    """
    monkeypatch.setattr(
        reb, "VALID_DATASETS",
        list(reb.VALID_DATASETS) + ["multinli"],  # repeated dataset
    )
    with pytest.raises(AssertionError, match="duplicate paths"):
        reb.verify_store(tmp_path)


def test_truncated_manifest_raises(tmp_path: Path, monkeypatch) -> None:
    """A shrunken manifest must fail the derivation, not lower the bar."""
    real = reb.parse_dataset_prompts

    def truncated(dataset: str):
        prompts = real(dataset)
        if dataset == "multinli":
            return {k: [] for k in prompts}
        return prompts

    monkeypatch.setattr(reb, "parse_dataset_prompts", truncated)
    with pytest.raises(AssertionError, match="60 graphs"):
        reb.verify_store(tmp_path)


def test_output_exists_and_verifier_agree_on_filenames(tmp_path: Path, monkeypatch) -> None:
    """The per-run check and the store walk must derive identical names.

    They share expected_graph_files by construction; this pins the sharing so
    a future edit to one path cannot silently diverge from the other.
    """
    monkeypatch.setattr(reb, "PROBE_CIRCUITS_DIR", tmp_path)
    dataset, tag = "civil_comments", "pos_pos_3"
    assert not reb.output_exists(dataset, tag)
    for p in reb.expected_graph_files(dataset, tag, tmp_path):
        p.write_bytes(b"x")
    assert reb.output_exists(dataset, tag)

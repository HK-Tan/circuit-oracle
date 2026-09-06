"""The gpu_timing summary must not collide across processes sharing an out-root.

A multi-GPU node runs one process per card against one out-root. Every other
output is keyed by slug, so this file was the only thing that clobbered, and it
clobbered silently: the last process to finish left a summary covering its own
shard only, which reads as a complete batch.
"""

import importlib.util
import os
from pathlib import Path

import pytest

_RUN_ALL = (
    Path(__file__).resolve().parents[1]
    / "refusal-jailbreaking" / "scripts" / "run_all.py"
)


@pytest.fixture(scope="module")
def run_all():
    """Load run_all.py by path. It is a script under scripts/, not an installed
    module, and importing it must not require the heavy circuit_oracle deps to
    be resolvable from the test's cwd."""
    spec = importlib.util.spec_from_file_location("_run_all_under_test", _RUN_ALL)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as exc:  # torch / circuit_oracle absent in a light env
        pytest.skip(f"run_all.py not importable here: {exc}")
    return mod


def test_distinct_per_visible_device(run_all, monkeypatch):
    """The real launch pattern: six processes, CUDA_VISIBLE_DEVICES 0..5."""
    names = set()
    for dev in range(6):
        monkeypatch.setenv("CUDA_VISIBLE_DEVICES", str(dev))
        names.add(run_all.timing_filename())
    assert len(names) == 6, f"shards collided: {sorted(names)}"


def test_stable_across_reruns_of_one_shard(run_all, monkeypatch):
    """A re-run of gpu3 must overwrite its own stale file, not accumulate.

    Pid-suffixing every file would leave a partial earlier attempt on disk for
    the collection step to average in, which is a worse failure than clobbering.
    """
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "3")
    assert run_all.timing_filename() == run_all.timing_filename()


def test_pid_fallback_when_device_unset(run_all, monkeypatch):
    monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)
    assert run_all.timing_filename() == f"gpu_timing.pid{os.getpid()}.json"


def test_empty_device_var_does_not_produce_a_shared_name(run_all, monkeypatch):
    """An exported-but-empty CUDA_VISIBLE_DEVICES must not degrade to one name
    shared by every process, which is the original bug wearing a new mask."""
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "   ")
    assert run_all.timing_filename() == f"gpu_timing.pid{os.getpid()}.json"


def test_multi_device_value_is_path_safe(run_all, monkeypatch):
    """CUDA_VISIBLE_DEVICES can be a comma list, and a raw comma or slash in a
    filename is at best awkward and at worst a path escape."""
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "0,1")
    name = run_all.timing_filename()
    assert name == "gpu_timing.gpu0_1.json"
    assert Path(name).name == name


def test_empty_explicit_tag_falls_back(run_all, monkeypatch):
    """`--timing-tag ""` must not degrade to one name every process shares.

    Without this the tag would sanitize to "" and produce `gpu_timing..json`
    everywhere, which is the original collision with extra steps.
    """
    monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)
    for empty in ("", "   "):
        assert run_all.timing_filename(empty) == f"gpu_timing.pid{os.getpid()}.json"


def test_explicit_tag_overrides_and_is_sanitized(run_all, monkeypatch):
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "0")
    assert run_all.timing_filename("shard/../4") == "gpu_timing.shard_.._4.json"


def test_parser_exposes_timing_tag(run_all):
    args = run_all.build_parser().parse_args(["--timing-tag", "shard4"])
    assert args.timing_tag == "shard4"
    assert run_all.build_parser().parse_args([]).timing_tag is None

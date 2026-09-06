"""Agent-supplied (layer, feature_idx, pos) must be bounds-checked host-side.

These coords arrive as free-form JSON from a model and are handed to advanced
indexing on the GPU. Out of range there does not raise a clean IndexError, it
trips a device-side assert in IndexKernel.cu that poisons the CUDA context for
the entire process, taking down every concurrent run sharing the model.
"""

import pytest
import torch

from circuit_oracle.tools import _validate_feature_coord


class _Ctx:
    def __init__(self, n_layers=36, n_pos=40, d_transcoder=131072):
        self.baseline_activations = torch.zeros(n_layers, n_pos, 8)
        # Real d_transcoder is huge; fake the last dim via a view-free stub so
        # the test stays cheap. Shape is what the validator reads.
        self.baseline_activations = torch.zeros(1)
        self._shape = (n_layers, n_pos, d_transcoder)

        class _Acts:
            ndim = 3
            shape = self._shape
        self.baseline_activations = _Acts()


def test_valid_coord_passes_through():
    assert _validate_feature_coord(_Ctx(), 17, 83241, 21) == (17, 83241, 21)


def test_string_inputs_are_coerced():
    """Models emit numbers as strings often enough that rejecting them would be
    a worse failure than coercing."""
    assert _validate_feature_coord(_Ctx(), "17", "83241", "21") == (17, 83241, 21)


@pytest.mark.parametrize("layer", [-1, 36, 999])
def test_layer_out_of_range_rejected(layer):
    with pytest.raises(ValueError, match="layer"):
        _validate_feature_coord(_Ctx(), layer, 100, 0)


@pytest.mark.parametrize("feature_idx", [-1, 131072, 10**9])
def test_feature_idx_out_of_range_rejected(feature_idx):
    with pytest.raises(ValueError, match="feature_idx"):
        _validate_feature_coord(_Ctx(), 0, feature_idx, 0)


@pytest.mark.parametrize("pos", [-1, 40, 500])
def test_pos_out_of_range_rejected(pos):
    with pytest.raises(ValueError, match="pos"):
        _validate_feature_coord(_Ctx(), 0, 100, pos)


def test_negative_index_is_rejected_not_wrapped():
    """The specific mechanism behind the 2026-07-28 shard loss.

    Python would wrap `[..., -5]` to `d_transcoder - 5`, but the id recorded for
    the searchsorted decoder lookup stays -5. The write and the lookup then
    disagree, and searchsorted runs off the end of the table. Wrapping is
    silently wrong here, so a negative index must raise.
    """
    with pytest.raises(ValueError):
        _validate_feature_coord(_Ctx(), 0, -5, 0)


def test_pos_optional():
    assert _validate_feature_coord(_Ctx(), 3, 500)[2] is None


def test_no_baseline_activations_still_checks_negatives():
    """Bounds are unknown without baseline_activations, but negatives are
    always wrong and must still be caught."""
    class _Bare:
        baseline_activations = None

    assert _validate_feature_coord(_Bare(), 5, 900, 3) == (5, 900, 3)
    for bad in ((-1, 900, 3), (5, -900, 3), (5, 900, -3)):
        with pytest.raises(ValueError):
            _validate_feature_coord(_Bare(), *bad)

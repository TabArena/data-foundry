"""The recommended encodings of a spectrum (``data_foundry.v2.spectra``)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from data_foundry.v2 import Spectrum, encode_spectrum, spectra, spectrum_encoding
from data_foundry.v2.dataset import DatasetDefinitionError
from data_foundry.v2.encodings import recommended_encodings
from data_foundry.v2.spectra import (
    AS_IS_ENCODING,
    CROMWELL_FILTER,
    CROMWELL_LOG2_ENCODING,
    DRIAMS_ENCODING,
    MS_RAW_ENCODING,
    VIBRATIONAL_ALS_SNV_ENCODING,
    snip_baseline,
)

pytest.importorskip("scipy")


def _spectra(n_rows: int = 4, n: int = 400) -> tuple[pd.DataFrame, np.ndarray]:
    """Gaussian peaks on a rising baseline (a straight line after the square root), each row on its own scale."""
    axis = np.linspace(1000.0, 5000.0, n)
    rows = []
    for i in range(n_rows):
        peaks = sum(np.exp(-0.5 * ((axis - c) / 15.0) ** 2) * h for c, h in ((2000, 50), (3000, 80), (4200, 30)))
        rows.append((1 + i) * (peaks + (4 + 0.001 * (axis - 1000)) ** 2))
    frame = pd.DataFrame(rows, columns=[f"mz_{a:.1f}" for a in axis], index=[10 + i for i in range(n_rows)])
    return frame, axis


def test_the_raw_mass_spectrum_encoding_removes_the_baseline_and_the_scale() -> None:
    """MALDIquant's steps: the sloped baseline is gone, every row has unit area, and rows that differ only in scale
    come out the same; the columns and the index are kept.
    """
    frame, axis = _spectra()
    out = encode_spectrum(frame, axis, MS_RAW_ENCODING)
    assert list(out.columns) == list(frame.columns)
    assert list(out.index) == list(frame.index)
    values = out.to_numpy()
    assert (values >= 0).all()
    area = ((values[:, 1:] + values[:, :-1]) / 2 * np.diff(axis)).sum(axis=1)
    np.testing.assert_allclose(area, 1.0)
    assert values[:, :40].max() < 0.05 * values.max()  # no peak there: the baseline was removed
    np.testing.assert_allclose(values[0], values[3], atol=1e-3 * values.max())


def test_the_encodings_are_deterministic_and_take_the_spec_id() -> None:
    """The same frame gives the same values, whether the encoding is passed as an object or its spec id."""
    frame, axis = _spectra()
    a = encode_spectrum(frame, axis, MS_RAW_ENCODING)
    b = encode_spectrum(frame, axis, MS_RAW_ENCODING.id)
    pd.testing.assert_frame_equal(a, b)


def test_as_is_is_the_identity() -> None:
    """The as-is encoding returns the spectrum unchanged."""
    frame, axis = _spectra()
    pd.testing.assert_frame_equal(encode_spectrum(frame, axis, AS_IS_ENCODING), frame)


def test_als_and_snv_give_each_spectrum_mean_0_and_sd_1() -> None:
    """After the baseline and the standard normal variate, each spectrum has mean 0 and standard deviation 1."""
    frame, axis = _spectra(n=200)
    values = encode_spectrum(frame, axis, VIBRATIONAL_ALS_SNV_ENCODING).to_numpy()
    np.testing.assert_allclose(values.mean(axis=1), 0, atol=1e-9)
    np.testing.assert_allclose(values.std(axis=1), 1, atol=1e-9)


def test_a_spectrum_with_a_missing_value_comes_out_missing() -> None:
    """A spectrum with a missing intensity comes out missing; the others are encoded."""
    frame, axis = _spectra()
    frame.iloc[1, 5] = np.nan
    out = encode_spectrum(frame, axis, MS_RAW_ENCODING)
    assert out.iloc[1].isna().all()
    assert out.drop(index=frame.index[1]).notna().all().all()


def test_snip_keeps_the_baseline_below_the_signal() -> None:
    """SNIP never rises above the signal and follows it where there is no peak."""
    frame, _ = _spectra(n_rows=1)
    values = frame.to_numpy()
    baseline = snip_baseline(values)
    assert (baseline <= values + 1e-12).all()
    np.testing.assert_allclose(baseline[0, :50], values[0, :50], rtol=0.05)  # flat where there is no peak


@pytest.mark.parametrize(
    ("axis", "encoding", "match"),
    [
        (np.arange(400.0), "nope-r1", "Unknown spectrum encoding"),
        (np.arange(399.0), MS_RAW_ENCODING, "positions"),
        (np.arange(400.0)[::-1], MS_RAW_ENCODING, "increasing"),
    ],
)
def test_a_wrong_encoding_or_axis_is_refused(axis, encoding, match) -> None:
    """An unknown encoding, an axis of another length and a decreasing axis are refused."""
    frame, _ = _spectra()
    with pytest.raises(ValueError, match=match):
        encode_spectrum(frame, axis, encoding)


def test_the_default_follows_the_technique_and_the_state() -> None:
    """A raw mass spectrum gets MALDIquant's steps, anything else the spectrum as it is."""
    assert spectrum_encoding("mass_spectrometry", "raw") == MS_RAW_ENCODING
    assert spectrum_encoding("mass_spectrometry", "peaks") == AS_IS_ENCODING
    assert spectrum_encoding("raman", "raw") == AS_IS_ENCODING
    encodings = recommended_encodings()
    assert encodings["mass_spectrum"] == (MS_RAW_ENCODING, DRIAMS_ENCODING, CROMWELL_LOG2_ENCODING)
    assert encodings["vibrational_spectrum"] == (AS_IS_ENCODING, VIBRATIONAL_ALS_SNV_ENCODING)
    assert MS_RAW_ENCODING.id == "ms-sqrt-sg21-snip100-tic-r1"


def test_a_spectrum_reads_its_columns_in_axis_order() -> None:
    """The declaration finds its columns by prefix, orders them by position and refuses two equal positions."""
    spectrum = Spectrum("s", prefix="cm_", unit="cm-1", technique="raman", state="raw", description="d")
    columns, axis = spectrum.columns(["id", "cm_1200", "cm_400.5", "cm_800", "y"])
    assert (columns, axis) == (["cm_400.5", "cm_800", "cm_1200"], [400.5, 800.0, 1200.0])
    group = spectrum.feature_group(["cm_1", "cm_2"])
    assert (group.semantic_type, group.recommended_encoding) == ("spectrum", AS_IS_ENCODING.id)
    with pytest.raises(DatasetDefinitionError, match="same position"):
        spectrum.columns(["cm_1", "cm_1.0"])


def test_driams_removes_the_baseline_twice_and_the_scale() -> None:
    """DRIAMS's steps: the baseline is gone, every row has unit area, and rows that differ only in scale come out the
    same.
    """
    frame, axis = _spectra()
    values = encode_spectrum(frame, axis, DRIAMS_ENCODING).to_numpy()
    assert (values >= 0).all()
    area = ((values[:, 1:] + values[:, :-1]) / 2 * np.diff(axis)).sum(axis=1)
    np.testing.assert_allclose(area, 1.0)
    np.testing.assert_allclose(values[0], values[3], atol=1e-3 * values.max())
    assert not np.allclose(values, encode_spectrum(frame, axis, MS_RAW_ENCODING).to_numpy())


def test_the_cromwell_wavelet_is_orthonormal_and_inverts_without_a_threshold(monkeypatch: pytest.MonkeyPatch) -> None:
    """The Daubechies filter has unit norm and is orthogonal to its even shifts, and the undecimated transform
    reconstructs a spectrum exactly when no coefficient is thresholded (a length padded to a multiple of 1,024).
    """
    h = np.asarray(CROMWELL_FILTER)
    assert h.sum() == pytest.approx(np.sqrt(2))
    assert (h**2).sum() == pytest.approx(1.0)
    assert all(abs((h[: -2 * m] * h[2 * m :]).sum()) < 1e-12 for m in (1, 2, 3))
    x = np.random.default_rng(0).normal(size=(2, 1500)).cumsum(axis=1)
    monkeypatch.setattr(spectra, "CROMWELL_THRESHOLD", 0.0)
    np.testing.assert_allclose(spectra._cromwell_denoise(x), x, atol=1e-9)


def test_cromwell_denoises_and_ends_on_a_log2_scale_free_of_the_intensity_scale() -> None:
    """Cromwell's chain removes most of the noise, gives finite log2 values, and rows that differ only in scale come
    out the same.
    """
    frame, axis = _spectra(n=1200)
    noisy = frame + np.random.default_rng(1).normal(scale=0.5, size=frame.shape) * np.arange(1, 5)[:, None]
    denoised = spectra._cromwell_denoise(noisy.to_numpy())
    assert np.abs(denoised - frame.to_numpy()).mean() < 0.5 * np.abs(noisy.to_numpy() - frame.to_numpy()).mean()
    values = encode_spectrum(frame, axis, CROMWELL_LOG2_ENCODING).to_numpy()
    assert np.isfinite(values).all()
    np.testing.assert_allclose(values[0], values[3], atol=1e-6)
    with pytest.raises(ValueError, match="too few"):
        encode_spectrum(frame.iloc[:, :300], axis[:300], CROMWELL_LOG2_ENCODING)

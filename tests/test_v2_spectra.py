"""The recommended encodings of a spectrum (``data_foundry.v2.spectra``)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from data_foundry.v2 import (
    Spectrum,
    encode_special_feature,
    encode_spectrum,
    encodings_for,
    spectra,
    spectrum_encoding,
)
from data_foundry.v2.encodings import recommended_encodings
from data_foundry.v2.special import SpecialFeatureError
from data_foundry.v2.spectra import (
    AS_IS_ENCODING,
    CROMWELL_FILTER,
    CROMWELL_LOG2_ENCODING,
    DRIAMS_ENCODING,
    MS_RAW_ENCODING,
    VIBRATIONAL_ALS_SNV_ENCODING,
    VIBRATIONAL_SG1_ENCODING,
    VIBRATIONAL_SNV_ENCODING,
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


def test_snv_alone_matches_a_hand_computed_reference() -> None:
    """SNV of [1, 2, 3, 4, 5] is [-2, -1, 0, 1, 2] / sqrt(2) (population SD); a shifted and scaled copy of a spectrum
    comes out the same, every row with mean 0 and SD 1.
    """
    frame = pd.DataFrame([[1.0, 2.0, 3.0, 4.0, 5.0], [17.0, 27.0, 37.0, 47.0, 57.0], [2.0, 0.0, 5.0, 1.0, 1.0]])
    out = encode_spectrum(frame, np.arange(5.0), VIBRATIONAL_SNV_ENCODING).to_numpy()
    expected = np.array([-2.0, -1.0, 0.0, 1.0, 2.0]) / np.sqrt(2.0)
    np.testing.assert_allclose(out[0], expected)
    np.testing.assert_allclose(out[1], expected)
    np.testing.assert_allclose(out.mean(axis=1), 0, atol=1e-12)
    np.testing.assert_allclose(out.std(axis=1), 1)


def test_the_first_derivative_is_savitzky_golay_over_11_points_of_order_2() -> None:
    """The encoding equals scipy's savgol_filter(window 11, order 2, deriv 1, mode "interp") per position, and is
    exact on a quadratic: the derivative of i**2 is 2i at every position, the edges included.
    """
    from scipy.signal import savgol_filter  # noqa: PLC0415 - scipy is checked at import

    rng = np.random.default_rng(0)
    values = rng.normal(size=(3, 30)).cumsum(axis=1)
    axis = 600.0 + 2.0 * np.arange(30)
    frame = pd.DataFrame(values, columns=[f"cm_{a:g}" for a in axis], index=[7, 8, 9])
    out = encode_spectrum(frame, axis, VIBRATIONAL_SG1_ENCODING)
    assert (list(out.columns), list(out.index)) == (list(frame.columns), [7, 8, 9])
    np.testing.assert_allclose(out.to_numpy(), savgol_filter(values, 11, 2, deriv=1, axis=1, mode="interp"))
    i = np.arange(15.0)
    square = encode_spectrum(pd.DataFrame([i**2]), i, VIBRATIONAL_SG1_ENCODING).to_numpy()[0]
    np.testing.assert_allclose(square, 2 * i, atol=1e-9)
    with pytest.raises(ValueError, match="needs 11 columns"):
        encode_spectrum(frame.iloc[:, :10], axis[:10], VIBRATIONAL_SG1_ENCODING)


@pytest.mark.parametrize(
    "encoding",
    [
        MS_RAW_ENCODING,
        DRIAMS_ENCODING,
        VIBRATIONAL_ALS_SNV_ENCODING,
        VIBRATIONAL_SNV_ENCODING,
        VIBRATIONAL_SG1_ENCODING,
    ],
    ids=lambda e: e.id,
)
def test_a_spectrum_with_a_missing_value_comes_out_missing(encoding) -> None:
    """A spectrum with a missing intensity comes out missing; the others are encoded as they would be alone."""
    frame, axis = _spectra()
    frame.iloc[1, 5] = np.nan
    out = encode_spectrum(frame, axis, encoding)
    assert out.iloc[1].isna().all()
    rest = frame.drop(index=frame.index[1])
    pd.testing.assert_frame_equal(out.drop(index=frame.index[1]), encode_spectrum(rest, axis, encoding))
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

    def record(technique: str, state: str):
        spectrum = Spectrum(name="s", prefix="x_", unit="nm", technique=technique, state=state, description="d")
        return spectrum.record(["x_1", "x_2"])

    assert encodings_for(record("mass_spectrometry", "raw")) == (
        MS_RAW_ENCODING,
        DRIAMS_ENCODING,
        CROMWELL_LOG2_ENCODING,
    )
    assert encodings_for(record("mass_spectrometry", "peaks")) == (AS_IS_ENCODING,)
    vibrational = (AS_IS_ENCODING, VIBRATIONAL_ALS_SNV_ENCODING, VIBRATIONAL_SNV_ENCODING, VIBRATIONAL_SG1_ENCODING)
    for technique in ("raman", "infrared", "near_infrared"):
        feature = record(technique, "raw")
        assert encodings_for(feature) == vibrational
        assert feature.recommended_encoding == encodings_for(feature)[0].id == "spectrum-as-is-r1"
    assert [e.id for e in vibrational] == ["spectrum-as-is-r1", "vib-als-snv-r1", "vib-snv-r1", "vib-sg11-d1-r1"]
    assert set(recommended_encodings()["spectrum"]) == set(spectra.SPECTRUM_ENCODINGS.values())
    assert all(e.scope == "row" for e in spectra.SPECTRUM_ENCODINGS.values())
    assert MS_RAW_ENCODING.id == "ms-sqrt-sg21-snip100-tic-r1"


def test_a_spectrum_reads_its_columns_in_axis_order() -> None:
    """The declaration finds its columns by prefix, orders them by position and refuses two equal positions."""
    spectrum = Spectrum(name="s", prefix="cm_", unit="cm-1", technique="raman", state="raw", description="d")
    columns, details = spectrum.resolve(["id", "cm_1200", "cm_400.5", "cm_800", "y"])
    assert (columns, details.axis) == (["cm_400.5", "cm_800", "cm_1200"], [400.5, 800.0, 1200.0])
    record = spectrum.record(["cm_1", "cm_2"])
    assert (record.kind, record.layout, record.recommended_encoding) == ("spectrum", "group", AS_IS_ENCODING.id)
    with pytest.raises(SpecialFeatureError, match="same position"):
        spectrum.resolve(["cm_1", "cm_1.0"])


def test_encode_special_feature_replaces_the_columns_where_they_stand() -> None:
    """A spectrum keeps its columns with new values, the other columns untouched; an encoding that is no candidate of
    the feature is refused.
    """
    frame, _ = _spectra()
    frame.insert(0, "id", range(len(frame)))
    frame["y"] = 1
    spectrum = Spectrum(name="s", prefix="mz_", unit="m/z", technique="mass_spectrometry", state="raw", description="d")
    feature = spectrum.record(frame.columns)
    out = encode_special_feature(frame, feature)
    assert list(out.columns) == list(frame.columns)
    assert out["id"].tolist() == frame["id"].tolist()
    np.testing.assert_allclose(
        out[feature.columns].to_numpy(),
        encode_spectrum(frame[feature.columns], feature.details.axis, MS_RAW_ENCODING).to_numpy(),
    )
    driams = encode_special_feature(frame, feature, DRIAMS_ENCODING.id)
    assert not np.allclose(driams[feature.columns].to_numpy(), out[feature.columns].to_numpy())
    with pytest.raises(ValueError, match="no encoding of"):
        encode_special_feature(frame, feature, VIBRATIONAL_ALS_SNV_ENCODING)
    infrared = Spectrum(name="s", prefix="mz_", unit="cm-1", technique="infrared", state="raw", description="d")
    feature = infrared.record(frame.columns)
    derivative = encode_special_feature(frame, feature, "vib-sg11-d1-r1")
    np.testing.assert_allclose(
        derivative[feature.columns].to_numpy(),
        encode_spectrum(frame[feature.columns], feature.details.axis, VIBRATIONAL_SG1_ENCODING).to_numpy(),
    )


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

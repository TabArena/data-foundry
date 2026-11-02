"""Spectra in tabular data: how a definition declares one, and its recommended encodings (CLEAN-26, 2026-11-02).

A spectrum ships as the source publishes it: one column per position on its axis (an m/z, a wavenumber, a bin), named
``<prefix><position>``. The definition declares it in ``spectra = (Spectrum(...),)``, and the container records it as a
:class:`~data_foundry.schema.FeatureGroup` of type ``spectrum``: the columns in axis order, their positions, the
technique and what the source did to the values (``raw``, ``processed`` or ``peaks``). Each column stays a numeric
feature, so a model can read the bins as they are; a benchmark that knows the group encodes the spectrum row by row
instead, with the recommended encoding or its own. The processing has free choices (window, baseline method), so it
belongs in the benchmark, where every method gets the same default and a method can switch it off, not in the data
(PR #21, Andrej Tschalzev, 2026-10-21).

=========================================  ===============================  =======================================
spectrum                                   recommended (:func:`spectrum_encoding`)  what it computes
=========================================  ===============================  =======================================
mass spectrum, ``raw``                     ``ms-sqrt-sg21-snip100-tic``     MALDIquant's preprocessing (Gibb and
                                                                            Strimmer 2012, the package vignette):
                                                                            square root, Savitzky-Golay smoothing
                                                                            (21 points, order 3), SNIP baseline
                                                                            (100 iterations) removed, divided by
                                                                            the total ion current
mass spectrum ``peaks`` or ``processed``;  ``spectrum-as-is``               the columns unchanged
a vibrational spectrum (Raman, infrared,
near-infrared)
vibrational, the alternative to check      ``vib-als-snv``                  RamanBench's linear-model default: an
                                                                            asymmetric least squares baseline
                                                                            (lambda 1e5, p 0.01, 10 iterations)
                                                                            removed, then the standard normal
                                                                            variate of each spectrum
=========================================  ===============================  =======================================

Every encoding works on one spectrum at a time, with no fitting and no labels: it cannot leak test information, gives
the same row in every split, and returns the same columns with new values. MALDIquant's later steps (aligning the
spectra on common peaks, detecting peaks and binning them) fit across spectra, so they are left out of a per-row
default.

The evidence on pancreatic_cancer_mouse_detection (raw SELDI-TOF serum spectra, split by mouse): PR #21's own chain
lifted every model by 0.07 to 0.13 ROC AUC on 12 folds (2026-10-21). On the 60 shipped splits (2026-11-02),
MALDIquant's steps lift the tree models by 0.10 to 0.15 and TabPFN v3.5 by 0.03 (0.659 to 0.690), while logistic
regression loses 0.02; PR #21's chain, which ends in a log, scores higher for TabPFN (0.716) and the linear models
(the working copy's CHANGELOG). The default stays the published workflow until a change is decided for all raw mass
spectra. For vibrational spectra the evidence points the other way: in RamanBench (arXiv:2605.02003, 77 datasets),
the leading methods (AutoGluon 1.5, TabPFN v2.5, TabICL v2) read the raw spectra; the baseline and SNV are the
chemometric baselines' convention, and no foundation model or tree was tested on processed spectra. So the vibrational
default is the spectrum as it is, with ALS and SNV the alternative to check on the first such datasets.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd

from data_foundry.schema import FeatureGroup, SpectrumState, SpectrumTechnique
from data_foundry.v2._optional import import_build_dependency
from data_foundry.v2.dataset import DatasetDefinitionError
from data_foundry.v2.encodings import Encoding

MS_HALF_WINDOW = 10
"""MALDIquant's ``halfWindowSize`` for the Savitzky-Golay smoothing: a 21-point window (the vignette's value)."""

MS_POLYORDER = 3
"""The polynomial order of MALDIquant's Savitzky-Golay filter (its default)."""

MS_SNIP_ITERATIONS = 100
"""MALDIquant's SNIP iterations (the vignette's value); the window shrinks from 100 to 1, MALDIquant's default."""

ALS_LAMBDA = 1e5
"""RamanBench's smoothness of the asymmetric least squares baseline (``prep_bl_lam``)."""

ALS_P = 0.01
"""RamanBench's asymmetry of the baseline (``prep_bl_p``)."""

ALS_ITERATIONS = 10
"""RamanBench's reweighting iterations of the baseline."""

MS_RAW_ENCODING = Encoding(
    kind="spectrum",
    name=f"ms-sqrt-sg{2 * MS_HALF_WINDOW + 1}-snip{MS_SNIP_ITERATIONS}-tic",
    revision=1,
    description=(
        "MALDIquant's preprocessing of a raw mass spectrum, per spectrum: the square root of the intensities "
        f"(negative ones set to 0), Savitzky-Golay smoothing ({2 * MS_HALF_WINDOW + 1} points, order "
        f"{MS_POLYORDER}), the SNIP baseline ({MS_SNIP_ITERATIONS} iterations, decreasing window) subtracted, then "
        "division by the total ion current (the trapezoid area over the m/z axis). Same columns, new values; a "
        "spectrum with a missing value comes out missing."
    ),
)
"""The recommended encoding of a raw mass spectrum."""

AS_IS_ENCODING = Encoding(
    kind="spectrum",
    name="spectrum-as-is",
    revision=1,
    description="The spectrum's columns as the source publishes them, unchanged.",
)
"""The recommended encoding of a processed spectrum or a peak list, and of a vibrational spectrum."""

VIBRATIONAL_ALS_SNV_ENCODING = Encoding(
    kind="spectrum",
    name="vib-als-snv",
    revision=1,
    description=(
        f"RamanBench's linear-model default, per spectrum: the asymmetric least squares baseline (Eilers and Boelens "
        f"2005; lambda {ALS_LAMBDA:g}, p {ALS_P:g}, {ALS_ITERATIONS} iterations) subtracted, then the standard normal "
        "variate (minus the spectrum's mean, divided by its standard deviation). Same columns, new values."
    ),
)
"""The alternative encoding of a vibrational spectrum: check it next to the spectrum as it is."""

SPECTRUM_ENCODINGS = {e.id: e for e in (MS_RAW_ENCODING, AS_IS_ENCODING, VIBRATIONAL_ALS_SNV_ENCODING)}
"""Every spectrum encoding, by spec id."""


@dataclass(frozen=True)
class Spectrum:
    """A definition's declaration of a spectrum: its columns are ``<prefix><position>`` (CLEAN-26).

    The build takes every column whose name starts with ``prefix``, reads the rest of the name as the position on the
    axis, orders the columns by it and records them as a :class:`~data_foundry.schema.FeatureGroup` with the
    recommended encoding (:func:`spectrum_encoding`). Leave the columns out of ``_feature_types``: they are numbers.
    """

    name: str
    """The spectrum's name in the container, e.g. ``serum_ms``."""
    prefix: str
    """The start of every column name of the spectrum, e.g. ``M/Z:`` for ``M/Z:800.32``."""
    unit: str
    """The unit of the positions: ``m/z``, ``cm-1``, ``nm``, or ``bin`` when the source gives only a bin number."""
    technique: SpectrumTechnique
    """How it was measured: ``mass_spectrometry``, ``raman``, ``infrared`` or ``near_infrared``."""
    state: SpectrumState
    """What the source did to it: ``raw``, ``processed`` or ``peaks``."""
    description: str
    """The instrument, the range and the resolution, and what the source did to the values."""

    def columns(self, names: Iterable[str]) -> tuple[list[str], list[float]]:
        """The spectrum's columns among ``names``, in axis order, and their positions.

        Raises:
            DatasetDefinitionError: Fewer than two columns match, a position does not parse, or two are equal.
        """
        matched = [n for n in names if isinstance(n, str) and n.startswith(self.prefix)]
        if len(matched) < 2:
            msg = f"Spectrum {self.name!r}: {len(matched)} column(s) start with {self.prefix!r}; a spectrum needs two."
            raise DatasetDefinitionError(msg)
        positions = {}
        for name in matched:
            try:
                position = float(name[len(self.prefix) :])
            except ValueError:
                position = math.nan
            if not math.isfinite(position):
                msg = f"Spectrum {self.name!r}: the position of column {name!r} after {self.prefix!r} is no number."
                raise DatasetDefinitionError(msg)
            positions[name] = position
        ordered = sorted(matched, key=positions.__getitem__)
        axis = [positions[n] for n in ordered]
        if len(set(axis)) != len(axis):
            msg = f"Spectrum {self.name!r}: two columns have the same position on the axis."
            raise DatasetDefinitionError(msg)
        return ordered, axis

    def feature_group(self, names: Iterable[str]) -> FeatureGroup:
        """The container's record of the spectrum, for the columns ``names`` of the frame."""
        columns, axis = self.columns(names)
        encoding = spectrum_encoding(self.technique, self.state)
        return FeatureGroup(
            name=self.name,
            semantic_type="spectrum",
            columns=columns,
            axis=axis,
            axis_unit=self.unit,
            technique=self.technique,
            state=self.state,
            description=f"{self.description} Recommended encoding: {encoding.description}",
            recommended_encoding=encoding.id,
        )


def spectrum_encoding(technique: str, state: str) -> Encoding:
    """The recommended encoding of a spectrum of ``technique`` in ``state`` (the table of the module docstring)."""
    if technique == "mass_spectrometry" and state == "raw":
        return MS_RAW_ENCODING
    return AS_IS_ENCODING


def _sqrt(values: np.ndarray) -> np.ndarray:
    """MALDIquant's variance-stabilising square root; a negative intensity (an instrument offset) counts as 0."""
    return np.sqrt(np.clip(values, 0.0, None))


def _savitzky_golay(values: np.ndarray, half_window: int, polyorder: int) -> np.ndarray:
    """Savitzky-Golay smoothing along each row; the edges from the polynomial of the first and last window, as in
    MALDIquant (scipy's ``mode="interp"``).
    """
    signal = import_build_dependency("scipy.signal")
    return signal.savgol_filter(values, window_length=2 * half_window + 1, polyorder=polyorder, axis=1, mode="interp")


def snip_baseline(values: np.ndarray, iterations: int = MS_SNIP_ITERATIONS) -> np.ndarray:
    """The SNIP baseline of each row (Ryan et al. 1988), as MALDIquant computes it with ``decreasing=TRUE``.

    For a half window ``k`` from ``iterations`` down to 1, every point from ``k`` to the end minus ``k`` becomes the
    smaller of itself and the mean of its two neighbours ``k`` points away, all from the previous pass's values.
    """
    baseline = np.array(values, dtype="float64", copy=True)
    n = baseline.shape[1]
    for k in range(min(iterations, (n - 1) // 2), 0, -1):
        mean = (baseline[:, : n - 2 * k] + baseline[:, 2 * k :]) / 2.0
        baseline[:, k : n - k] = np.minimum(baseline[:, k : n - k], mean)
    return baseline


def _total_ion_current(values: np.ndarray, axis: np.ndarray) -> np.ndarray:
    """The trapezoid area of each row over the axis (MALDIquant's ``totalIonCurrent``)."""
    return ((values[:, 1:] + values[:, :-1]) / 2.0 * np.diff(axis)).sum(axis=1)


def als_baseline(values: np.ndarray, lam: float = ALS_LAMBDA, p: float = ALS_P, n_iter: int = ALS_ITERATIONS):
    """The asymmetric least squares baseline of each row (Eilers and Boelens 2005), as RamanBench computes it."""
    sparse = import_build_dependency("scipy.sparse")
    solve = import_build_dependency("scipy.sparse.linalg").spsolve
    n = values.shape[1]
    difference = sparse.diags([1.0, -2.0, 1.0], [0, 1, 2], shape=(n - 2, n))
    penalty = sparse.csc_matrix(lam * difference.T.dot(difference))
    out = np.empty_like(values, dtype="float64")
    for i, y in enumerate(values):
        weights = np.ones(n)
        for _ in range(n_iter):
            z = solve(sparse.diags(weights, 0, shape=(n, n)) + penalty, weights * y)
            weights = p * (y > z) + (1 - p) * (y <= z)
        out[i] = z
    return out


def _snv(values: np.ndarray) -> np.ndarray:
    """The standard normal variate of each row: minus its mean, divided by its standard deviation (0 stays 0)."""
    centred = values - values.mean(axis=1, keepdims=True)
    scale = values.std(axis=1, keepdims=True)
    return np.divide(centred, scale, out=np.zeros_like(centred), where=scale > 0)


def encode_spectrum(frame: pd.DataFrame, axis: Sequence[float], encoding: Encoding | str) -> pd.DataFrame:
    """A spectrum in ``encoding``: the same rows and columns as ``frame`` (its columns in axis order), new values.

    ``encoding`` is an :class:`~data_foundry.v2.encodings.Encoding` of this module or its spec id (a container's
    ``FeatureGroup.recommended_encoding``). A row with a missing value comes out missing, except as it is.

    Raises:
        ValueError: An unknown encoding, an axis that does not match the columns, or too few columns to smooth.
    """
    spec = SPECTRUM_ENCODINGS.get(encoding if isinstance(encoding, str) else encoding.id)
    if spec is None:
        msg = f"Unknown spectrum encoding {encoding!r}; implemented: {sorted(SPECTRUM_ENCODINGS)}."
        raise ValueError(msg)
    positions = np.asarray(axis, dtype="float64")
    if positions.shape != (frame.shape[1],) or np.any(np.diff(positions) <= 0):
        msg = f"The axis has {positions.size} positions for {frame.shape[1]} columns, or is not increasing."
        raise ValueError(msg)
    if spec == AS_IS_ENCODING:
        return frame.copy()
    values = frame.to_numpy(dtype="float64", na_value=np.nan)
    complete = np.isfinite(values).all(axis=1)
    out = np.full_like(values, np.nan)
    if spec == MS_RAW_ENCODING:
        if values.shape[1] < 2 * MS_HALF_WINDOW + 1:
            msg = f"A raw mass spectrum needs {2 * MS_HALF_WINDOW + 1} columns to smooth, got {values.shape[1]}."
            raise ValueError(msg)
        smoothed = _savitzky_golay(_sqrt(values[complete]), MS_HALF_WINDOW, MS_POLYORDER)
        corrected = smoothed - snip_baseline(smoothed)
        tic = _total_ion_current(corrected, positions)
        out[complete] = np.divide(corrected, tic[:, None], out=np.zeros_like(corrected), where=tic[:, None] > 0)
    else:  # VIBRATIONAL_ALS_SNV_ENCODING
        rows = values[complete]
        out[complete] = _snv(rows - als_baseline(rows))
    return pd.DataFrame(out, index=frame.index, columns=frame.columns)

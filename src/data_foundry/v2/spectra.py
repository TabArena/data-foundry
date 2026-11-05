"""Spectra in tabular data: how a definition declares one, and its recommended encodings (CLEAN-26, 2026-11-02).

A spectrum ships as the source publishes it: one column per position on its axis (an m/z, a wavenumber, a bin), named
``<prefix><position>``. The definition declares it as a special feature in a group of columns,
``special_features = (Spectrum(name=..., prefix=..., ...),)``, and the container records it as a
:class:`~data_foundry.schema.SpecialFeature` of kind ``spectrum`` (layout ``group``): the columns in axis order and
:class:`~data_foundry.schema.SpectrumDetails` (their positions, the unit, the technique and what the source did to the
values: ``raw``, ``processed`` or ``peaks``). Each column stays a numeric feature, so a model can read the bins as they
are; a benchmark that knows the feature encodes the spectrum row by row instead, with the recommended encoding or its
own (:func:`~data_foundry.v2.special.encode_special_feature`). The processing has free choices (window, baseline
method), so it belongs in the benchmark, where every method gets the same default and a method can switch it off, not
in the data (PR #21, Andrej Tschalzev, 2026-10-21).

=========================================  ===============================  =======================================
spectrum                                   recommended (:func:`spectrum_encoding`)  what it computes
=========================================  ===============================  =======================================
mass spectrum, ``raw``                     ``ms-sqrt-sg21-snip100-tic``     MALDIquant's preprocessing (Gibb and
                                                                            Strimmer 2012, the package vignette):
                                                                            square root, Savitzky-Golay smoothing
                                                                            (21 points, order 3), SNIP baseline
                                                                            (100 iterations) removed, divided by
                                                                            the total ion current
mass spectrum, ``raw``, candidates          ``ms-driams-sqrt-sg21-snip20-     DRIAMS's MALDIquant steps (Weis et al.
to compare                                 snip100-tic``                    2022): as above, the SNIP baseline
                                                                            removed twice (20, then 100 iterations)
                                           ``ms-cromwell-udwt-mm-tic-log2``  Cromwell's denoising and baseline
                                                                            (Coombes et al. 2005): an undecimated
                                                                            wavelet transform, a monotone minimum;
                                                                            then the total ion current and log2
mass spectrum ``peaks`` or ``processed``;  ``spectrum-as-is``               the columns unchanged
a vibrational spectrum (Raman, infrared,
near-infrared)
vibrational, candidates to compare         ``vib-als-snv``                  RamanBench's linear-model default: an
                                                                            asymmetric least squares baseline
                                                                            (lambda 1e5, p 0.01, 10 iterations)
                                                                            removed, then the standard normal
                                                                            variate of each spectrum
                                           ``vib-snv``                      the standard normal variate alone
                                                                            (Barnes et al. 1989), OSSL's own
                                                                            preprocessing
                                           ``vib-sg11-d1``                  the Savitzky-Golay first derivative
                                                                            (Savitzky and Golay 1964), 11 points,
                                                                            polynomial order 2, per position
=========================================  ===============================  =======================================

Every encoding works on one spectrum at a time, with no fitting and no labels: it cannot leak test information, gives
the same row in every split, and returns the same columns with new values. MALDIquant's later steps (aligning the
spectra on common peaks, detecting peaks and binning them) fit across spectra, so they are left out of a per-row
default.

Each technique registers the standard preprocessing candidates of its field, with fixed published settings, so a
benchmark can run them all and select (Lennart, 2026-11-04: "one can add all and select as needed when needed"). The
recommended one changes only when a comparison over every dataset of the technique says so.

The default for a raw mass spectrum is a placeholder until the benchmark decides it: the comparison studies find no
pipeline that wins everywhere and large effects of the settings (Cruz-Marcelo et al. 2008; Wegdam et al. 2009,
"We advocate the evaluation over a range of parameter settings"). The three raw mass-spectrum encodings are the
published candidates of the two traditions, the square root (MALDIquant, DRIAMS) and the log (Cromwell, Ciphergen);
``recommended_encodings()["mass_spectrum"]`` lists them, the default first. How the benchmark decides is in the working
copy's ``BENCHMARK_CHANGES_TODO.md``, "Spectra".

The evidence on pancreatic_cancer_mouse_detection (raw SELDI-TOF serum spectra, split by mouse): PR #21's own chain
lifted every model by 0.07 to 0.13 ROC AUC on 12 folds (2026-10-21). On the 60 shipped splits (2026-11-02),
MALDIquant's steps lift the tree models by 0.10 to 0.15 and TabPFN v3.5 by 0.03 (0.659 to 0.690), while logistic
regression loses 0.02; PR #21's chain, which ends in a log, scores higher for TabPFN (0.716) and the linear models
(the working copy's CHANGELOG). The default stays the published workflow until a change is decided for all raw mass
spectra. For vibrational spectra the evidence points the other way: in RamanBench (arXiv:2605.02003, 77 datasets),
the leading methods (AutoGluon 1.5, TabPFN v2.5, TabICL v2) read the raw spectra; the baseline and SNV are the
chemometric baselines' convention, and no foundation model or tree was tested on processed spectra. So the vibrational
default is the spectrum as it is, with ALS and SNV, SNV alone and the first derivative the candidates to compare. On
the first such dataset, open_soil_spectral_library (mid-infrared, 2026-11-04, untuned, RMSE in percent on the three
grouped folds of repeat 0), LightGBM gains from every candidate (1.74 as it is; 1.33, 1.39 and 1.24), PLS from ALS and
SNV and from the derivative, and ridge from none (the spectra guide of the curation skill has the table).
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

import numpy as np
import pandas as pd

from data_foundry.schema import SpectrumDetails, SpectrumState, SpectrumTechnique
from data_foundry.v2._optional import import_build_dependency
from data_foundry.v2.encodings import Encoding
from data_foundry.v2.special import SpecialColumnGroup, SpecialFeatureError

if TYPE_CHECKING:
    from data_foundry.bundle_checks import CheckResult
    from data_foundry.schema import SpecialFeature

MS_HALF_WINDOW = 10
"""MALDIquant's ``halfWindowSize`` for the Savitzky-Golay smoothing: a 21-point window (the vignette's value)."""

MS_POLYORDER = 3
"""The polynomial order of MALDIquant's Savitzky-Golay filter (its default)."""

MS_SNIP_ITERATIONS = 100
"""MALDIquant's SNIP iterations (the vignette's value); the window shrinks from 100 to 1, MALDIquant's default."""

DRIAMS_SNIP_ITERATIONS = (20, MS_SNIP_ITERATIONS)
"""DRIAMS's two baseline removals: ``removeBaseline(removeBaseline(spectra, method="SNIP", iterations=20))``, the outer
call with MALDIquant's default of 100 iterations (``DRIAMS-A_2015_preprocessed.r`` in BorgwardtLab/maldi_amr)."""

CROMWELL_FILTER = (
    0.2303778133088964,
    0.7148465705529154,
    0.6308807679298587,
    -0.0279837694168599,
    -0.1870348117190931,
    0.0308413818355607,
    0.0328830116668852,
    -0.0105974017850690,
)
"""The Daubechies scaling filter with 8 coefficients, normalised to sum sqrt(2): the Rice Wavelet Toolbox's
``daubcqf(8)``, which Cromwell's ``waveletSmoothAndBaselineCorrect`` uses."""

CROMWELL_LEVELS = 10
"""Cromwell's wavelet levels (its default ``L = 10``, blocks of 1,024 points)."""

CROMWELL_THRESHOLD = 6.0
"""Cromwell's threshold multiple of the finest level's median absolute coefficient divided by 0.67 (its example value;
"we typically use thresholds in the range of 4-10")."""

ALS_LAMBDA = 1e5
"""RamanBench's smoothness of the asymmetric least squares baseline (``prep_bl_lam``)."""

ALS_P = 0.01
"""RamanBench's asymmetry of the baseline (``prep_bl_p``)."""

ALS_ITERATIONS = 10
"""RamanBench's reweighting iterations of the baseline."""

VIB_SG_HALF_WINDOW = 5
"""The half window of the vibrational first derivative: 11 points, the window of prospectr's first-derivative example
on soil near-infrared spectra (``savitzkyGolay(m = 1, p = 3, w = 11)``, Stevens and Ramirez-Lopez) and of the
comparison on open_soil_spectral_library; soil mid-infrared work uses 11 to 21 (Sila et al. 2016, Chemometrics and
Intelligent Laboratory Systems 153: 21 points)."""

VIB_SG_POLYORDER = 2
"""The polynomial order of the vibrational first derivative: a quadratic, as in the comparison on
open_soil_spectral_library. Away from the edges a quadratic's first derivative is the least-squares slope of the window
(orders 1 and 2 give the same coefficients); prospectr's example uses order 3."""

MS_RAW_ENCODING = Encoding(
    scope="row",
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

DRIAMS_ENCODING = Encoding(
    scope="row",
    kind="spectrum",
    name=f"ms-driams-sqrt-sg{2 * MS_HALF_WINDOW + 1}-snip20-snip100-tic",
    revision=1,
    description=(
        "DRIAMS's preprocessing of a raw MALDI-TOF spectrum (Weis et al. 2022, Nature Medicine; their MALDIquant "
        "script), per spectrum: the square root, Savitzky-Golay smoothing (21 points, order 3), the SNIP baseline "
        "removed twice (20 iterations, then MALDIquant's default 100), then division by the total ion current. Their "
        "trim to 2,000-20,000 Da and 3 Da bins change the columns, so they are left to the benchmark. Same columns, "
        "new values; a spectrum with a missing value comes out missing."
    ),
)
"""A candidate for raw mass spectra: the MALDIquant settings of the largest machine-learning study on MALDI-TOF
spectra."""

CROMWELL_LOG2_ENCODING = Encoding(
    scope="row",
    kind="spectrum",
    name="ms-cromwell-udwt-mm-tic-log2",
    revision=1,
    description=(
        "Cromwell's denoising and baseline (Coombes et al. 2005, Proteomics; MD Anderson's MATLAB code), per spectrum: "
        "padded by reflecting its end to a multiple of 1,024 points, an undecimated wavelet transform (Daubechies, 8 "
        "coefficients, 10 levels) whose detail coefficients are hard-thresholded at 6 times the finest level's median "
        "absolute coefficient / 0.67, inverted and cut back; the monotone minimum (the lowest value so far, from the "
        "first point) subtracted; divided by the total ion current; values of 0 set to half the spectrum's smallest "
        "positive value (Ciphergen's rule, Wegdam et al. 2009), then log2. Same columns, new values."
    ),
)
"""A candidate for raw mass spectra: the log tradition of SELDI-TOF analysis (Cromwell, Ciphergen), which PR #21's own
chain follows."""

AS_IS_ENCODING = Encoding(
    scope="row",
    kind="spectrum",
    name="spectrum-as-is",
    revision=1,
    description="The spectrum's columns as the source publishes them, unchanged.",
)
"""The recommended encoding of a processed spectrum or a peak list, and of a vibrational spectrum."""

VIBRATIONAL_ALS_SNV_ENCODING = Encoding(
    scope="row",
    kind="spectrum",
    name="vib-als-snv",
    revision=1,
    description=(
        f"RamanBench's linear-model default, per spectrum: the asymmetric least squares baseline (Eilers and Boelens "
        f"2005; lambda {ALS_LAMBDA:g}, p {ALS_P:g}, {ALS_ITERATIONS} iterations) subtracted, then the standard normal "
        "variate (minus the spectrum's mean, divided by its standard deviation). Same columns, new values."
    ),
)
"""A candidate for vibrational spectra, the first to compare with the spectrum as it is."""

VIBRATIONAL_SNV_ENCODING = Encoding(
    scope="row",
    kind="spectrum",
    name="vib-snv",
    revision=1,
    description=(
        "The standard normal variate of each spectrum alone (Barnes, Dhanoa and Lister 1989, Applied Spectroscopy 43; "
        "OSSL's preprocessing): minus the spectrum's mean, divided by its standard deviation (population, as in "
        "vib-als-snv). Same columns, new values; a spectrum with a missing value comes out missing."
    ),
)
"""A candidate for vibrational spectra: the scatter correction without a baseline."""

VIBRATIONAL_SG1_ENCODING = Encoding(
    scope="row",
    kind="spectrum",
    name=f"vib-sg{2 * VIB_SG_HALF_WINDOW + 1}-d1",
    revision=1,
    description=(
        "The Savitzky-Golay first derivative of each spectrum (Savitzky and Golay 1964): "
        f"{2 * VIB_SG_HALF_WINDOW + 1} points, polynomial order {VIB_SG_POLYORDER}, per position on the grid (not per "
        "axis unit), the edges from the polynomial of the first and last window (scipy's savgol_filter, "
        "mode='interp'). Same columns, new values; a spectrum with a missing value comes out missing."
    ),
)
"""A candidate for vibrational spectra: the first derivative removes an additive offset and sharpens overlapping
bands."""

SPECTRUM_ENCODINGS = {
    e.id: e
    for e in (
        MS_RAW_ENCODING,
        DRIAMS_ENCODING,
        CROMWELL_LOG2_ENCODING,
        AS_IS_ENCODING,
        VIBRATIONAL_ALS_SNV_ENCODING,
        VIBRATIONAL_SNV_ENCODING,
        VIBRATIONAL_SG1_ENCODING,
    )
}
"""Every spectrum encoding, by spec id."""

VIBRATIONAL_CANDIDATES = (VIBRATIONAL_ALS_SNV_ENCODING, VIBRATIONAL_SNV_ENCODING, VIBRATIONAL_SG1_ENCODING)
"""The processing candidates of a vibrational spectrum, after the recommended spectrum as it is."""


@dataclass(frozen=True, kw_only=True)
class Spectrum(SpecialColumnGroup):
    """A special feature in a group of columns: one spectrum per row, its columns ``<prefix><position>`` (CLEAN-26),
    e.g. ``special_features = (Spectrum(name="serum_ms", prefix="M/Z:", unit="m/z", technique="mass_spectrometry",
    state="raw", description=...),)``.

    The build takes every column whose name starts with ``prefix``, reads the rest of the name as the position on the
    axis, orders the columns by it and records them with :class:`~data_foundry.schema.SpectrumDetails` and the
    recommended encoding (:func:`spectrum_encoding`). The columns stay numbers as published; leave them out of
    ``_feature_types``.
    """

    kind: ClassVar[str] = "spectrum"
    encoding_required: ClassVar[bool] = False
    unit: str
    """The unit of the positions: ``m/z``, ``cm-1``, ``nm``, or ``bin`` when the source gives only a bin number."""
    technique: SpectrumTechnique
    """How it was measured: ``mass_spectrometry``, ``raman``, ``infrared`` or ``near_infrared``."""
    state: SpectrumState
    """What the source did to it: ``raw``, ``processed`` or ``peaks``."""

    def resolve(self, names: Iterable[str]) -> tuple[list[str], SpectrumDetails]:
        """The spectrum's columns among ``names``, in axis order, and their details.

        Raises:
            SpecialFeatureError: Fewer than two columns match, a position does not parse, or two are equal.
        """
        matched = self.matched(names)
        positions = {}
        for name in matched:
            try:
                position = float(name[len(self.prefix) :])
            except ValueError:
                position = math.nan
            if not math.isfinite(position):
                msg = f"Spectrum {self.name!r}: the position of column {name!r} after {self.prefix!r} is no number."
                raise SpecialFeatureError(msg)
            positions[name] = position
        ordered = sorted(matched, key=positions.__getitem__)
        axis = [positions[n] for n in ordered]
        if len(set(axis)) != len(axis):
            msg = f"Spectrum {self.name!r}: two columns have the same position on the axis."
            raise SpecialFeatureError(msg)
        return ordered, SpectrumDetails(axis=axis, axis_unit=self.unit, technique=self.technique, state=self.state)

    @classmethod
    def encodings(cls, feature: SpecialFeature) -> tuple[Encoding, ...]:
        """By technique and state: a raw mass spectrum's three published candidates (the placeholder default first),
        a processed one or a peak list as it is, a vibrational spectrum as it is, then with ALS and SNV, with SNV
        alone and as its Savitzky-Golay first derivative.
        """
        details = feature.details
        if details.technique == "mass_spectrometry":
            if details.state == "raw":
                return (MS_RAW_ENCODING, DRIAMS_ENCODING, CROMWELL_LOG2_ENCODING)
            return (AS_IS_ENCODING,)
        return (AS_IS_ENCODING, *VIBRATIONAL_CANDIDATES)

    @classmethod
    def encode(cls, frame: pd.DataFrame, feature: SpecialFeature, encoding: Encoding) -> pd.DataFrame:
        """The spectrum's columns with the encoded values."""
        return encode_spectrum(frame, feature.details.axis, encoding)

    @classmethod
    def check(cls, df: pd.DataFrame, feature: SpecialFeature) -> Iterator[CheckResult]:
        """Every column is numeric and finite; a missing value is flagged, a negative raw mass intensity noted."""
        from data_foundry.bundle_checks import CheckResult  # noqa: PLC0415 - bundle_checks loads the kinds lazily

        values = df[feature.columns]
        not_numeric = [
            c for c in feature.columns if not pd.api.types.is_numeric_dtype(values[c]) or values[c].dtype == bool
        ]
        if not_numeric:
            yield CheckResult(
                "dataset_spectrum",
                "error",
                f"Spectrum `{feature.name}`: {len(not_numeric):,} column(s) are not numeric, e.g. {not_numeric[:3]}.",
                hint="A spectrum's columns are intensities; leave them out of `_feature_types`.",
            )
            return
        array = values.to_numpy(dtype="float64", na_value=np.nan)
        missing = int(np.isnan(array).any(axis=1).sum())
        if missing:
            yield CheckResult(
                "dataset_spectrum",
                "warning",
                f"Spectrum `{feature.name}`: {missing:,} row(s) have a missing intensity; the processing encodings "
                "return such a spectrum as missing.",
                hint="Drop the rows or say in the curation notes why they stay.",
            )
        if np.isinf(array).any():
            yield CheckResult("dataset_spectrum", "error", f"Spectrum `{feature.name}` has infinite intensities.")
        details = feature.details
        if details.technique == "mass_spectrometry" and details.state == "raw" and np.nanmin(array) < 0:
            yield CheckResult(
                "dataset_spectrum_negative",
                "info",
                f"Spectrum `{feature.name}`: {int((array < 0).any(axis=1).sum()):,} raw mass spectra have negative "
                "intensities; the recommended encoding counts them as 0 before the square root.",
            )


def spectrum_encoding(technique: str, state: str) -> Encoding:
    """The recommended encoding of a spectrum of ``technique`` in ``state`` (the table of the module docstring)."""
    if technique == "mass_spectrometry" and state == "raw":
        return MS_RAW_ENCODING
    return AS_IS_ENCODING


def _sqrt(values: np.ndarray) -> np.ndarray:
    """MALDIquant's variance-stabilising square root; a negative intensity (an instrument offset) counts as 0."""
    return np.sqrt(np.clip(values, 0.0, None))


def _savitzky_golay(values: np.ndarray, half_window: int, polyorder: int, deriv: int = 0) -> np.ndarray:
    """Savitzky-Golay smoothing along each row, or its ``deriv``-th derivative per position; the edges from the
    polynomial of the first and last window, as in MALDIquant (scipy's ``mode="interp"``).
    """
    signal = import_build_dependency("scipy.signal")
    return signal.savgol_filter(
        values, window_length=2 * half_window + 1, polyorder=polyorder, deriv=deriv, axis=1, mode="interp"
    )


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


def _per_tic(values: np.ndarray, axis: np.ndarray) -> np.ndarray:
    """Each row divided by its total ion current; a row of zeros stays zeros."""
    tic = _total_ion_current(values, axis)[:, None]
    return np.divide(values, tic, out=np.zeros_like(values), where=tic > 0)


def _cromwell_denoise(values: np.ndarray) -> np.ndarray:
    """Cromwell's wavelet denoising of each row, as the Rice Wavelet Toolbox's ``denoise(x, daubcqf(8), 1, [0 t 0 1 L
    0])`` computes it: the undecimated transform (circular, the filters spread by 2 per level), every detail
    coefficient at or below the threshold set to 0, the inverse transform (each level's two branches averaged).
    """
    n = values.shape[1]
    block = 2**CROMWELL_LEVELS
    needs = -n % block
    if needs > n:
        msg = f"Cromwell's denoising pads by reflection to a multiple of {block} points; {n} columns are too few."
        raise ValueError(msg)
    x = np.concatenate([values, values[:, n - needs :][:, ::-1]], axis=1) if needs else values.copy()
    low = np.asarray(CROMWELL_FILTER)
    high = np.array([(-1) ** k * low[len(low) - 1 - k] for k in range(len(low))])
    approx, details = x, []
    for level in range(CROMWELL_LEVELS):
        step = 2**level
        shifted = [np.roll(approx, -step * k, axis=1) for k in range(len(low))]
        details.append(sum(g * part for g, part in zip(high, shifted, strict=True)))
        approx = sum(h * part for h, part in zip(low, shifted, strict=True))
    threshold = CROMWELL_THRESHOLD * np.median(np.abs(details[0]), axis=1, keepdims=True) / 0.67
    details = [np.where(np.abs(d) > threshold, d, 0.0) for d in details]
    for level in reversed(range(CROMWELL_LEVELS)):
        step = 2**level
        approx = 0.5 * sum(
            h * np.roll(approx, step * k, axis=1) + g * np.roll(details[level], step * k, axis=1)
            for k, (h, g) in enumerate(zip(low, high, strict=True))
        )
    return approx[:, :n]


def _log2_positive(values: np.ndarray) -> np.ndarray:
    """log2 of each row, its values of 0 or below set first to half its smallest positive value (Ciphergen's rule)."""
    positive = np.where(values > 0, values, np.inf).min(axis=1, keepdims=True)
    floor = np.where(np.isfinite(positive), positive / 2, 1.0)
    return np.log2(np.where(values > 0, values, floor))


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
    ``SpecialFeature.recommended_encoding``). A row with a missing value comes out missing, except as it is.

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
    if spec in (MS_RAW_ENCODING, DRIAMS_ENCODING):
        if values.shape[1] < 2 * MS_HALF_WINDOW + 1:
            msg = f"A raw mass spectrum needs {2 * MS_HALF_WINDOW + 1} columns to smooth, got {values.shape[1]}."
            raise ValueError(msg)
        corrected = _savitzky_golay(_sqrt(values[complete]), MS_HALF_WINDOW, MS_POLYORDER)
        for iterations in (MS_SNIP_ITERATIONS,) if spec == MS_RAW_ENCODING else DRIAMS_SNIP_ITERATIONS:
            corrected = corrected - snip_baseline(corrected, iterations)
        out[complete] = _per_tic(corrected, positions)
    elif spec == CROMWELL_LOG2_ENCODING:
        smoothed = _cromwell_denoise(values[complete])
        corrected = smoothed - np.minimum.accumulate(smoothed, axis=1)
        out[complete] = _log2_positive(_per_tic(corrected, positions))
    else:
        out[complete] = _encode_vibrational(values[complete], spec)
    return pd.DataFrame(out, index=frame.index, columns=frame.columns)


def _encode_vibrational(rows: np.ndarray, spec: Encoding) -> np.ndarray:
    """``rows`` (complete spectra) in one of the vibrational candidates (:data:`VIBRATIONAL_CANDIDATES`).

    Raises:
        ValueError: Fewer columns than the first derivative's window.
    """
    if spec == VIBRATIONAL_ALS_SNV_ENCODING:
        return _snv(rows - als_baseline(rows))
    if spec == VIBRATIONAL_SNV_ENCODING:
        return _snv(rows)
    window = 2 * VIB_SG_HALF_WINDOW + 1
    if rows.shape[1] < window:
        msg = f"The first derivative needs {window} columns, got {rows.shape[1]}."
        raise ValueError(msg)
    return _savitzky_golay(rows, VIB_SG_HALF_WINDOW, VIB_SG_POLYORDER, deriv=1)

"""Curated dataset definition for `raman_mlrod` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    Spectrum,
    SplitPlan,
    TaskSummary,
)

PREFIX = "raman_"

# The source's own common grid (Spec-CNN `helper.raw_processing`, the input of its raw-spectrum CNN, input layer
# (950, 1)): the spectrum trimmed to 150-1,100 cm-1 in 950 bands of 1 cm-1 [k, k + 1), named by the band's lower edge.
# The source takes the minimum of the readings in a band, a cosmic-ray step; we take the one reading nearest the
# band's centre (Curation notes).
BANDS = range(150, 1100)

# The source's integer label codes, named by the training maps that carry them (each `*_train_*` file holds one code:
# qtz 0, albite 1, hb 2, bt 3, ms 4, fo 5, aug 6, en 7, an 8, mc 9, cal 10, gyp 11, qtzalb 12, foaug 13, foalb 14) and
# by the mineral list of Sineesh and Kamsali (2026), Sec. 4.1. Code 15, the source's code for an unknown, occurs only in
# the granite map under 50% dust.
CLASS_NAMES = {
    0: "Quartz",
    1: "Albite",
    2: "Hornblende",
    3: "Biotite",
    4: "Muscovite",
    5: "Forsterite",
    6: "Augite",
    7: "Enstatite",
    8: "Anorthite",
    9: "Microcline",
    10: "Calcite",
    11: "Gypsum",
    12: "Quartz-albite mix",
    13: "Forsterite-augite mix",
    14: "Forsterite-albite mix",
}
DUST_CODE = 15

# The gabbro map under 50% dust: its plagioclase block carries code 9 (microcline), where the same grain under 0% dust
# carries 8 (anorthite). Repaired to 8 (Decisions).
GABBRO_DUSTY = "L_raw_gabbro50dust_test_015s_9740"

# A 46-spectrum map named after the clean gabbro whose labels are gypsum and the forsterite-albite powder mixture (the
# source's row ids read "gyp_foalb_test"): no point of the gabbro slab. It trains, as a group of its own.
POWDER_MAP = "L_raw_gabbro0dust_test_015s_46_final"

# A reference spectrum holding a spreadsheet fill-down: from 581.4 cm-1 its readings are exactly k x 4.11843 (k = 1 to
# 346, to 858 cm-1), then climb on to the end of the window without reaching the row's level. Its bands from 581 cm-1
# are missing.
FILLED_MAP, FILLED_ROW, FILLED_FROM = "qtzalb_train_60s_3000", "qtzalb_train_60s_3000-2456", 581
FILL_STEP = 4.11843


def rock_of(stem: str) -> str | None:
    """The rock slab a map belongs to, from the source's file name (None for a reference map or the powder map)."""
    if stem == POWDER_MAP:
        return None
    for rock in ("gabbro", "granite"):
        if stem.startswith(f"L_raw_{rock}"):
            return rock
    return None


def one_reading_per_band(frame: pd.DataFrame) -> pd.DataFrame:
    """One map on the source's grid: the reading nearest k + 0.5 cm-1 in each 1 cm-1 band from 150 to 1,099 cm-1."""
    positions = frame.columns.astype(float).to_numpy()
    band = np.floor(positions).astype(int)
    picked = []
    for k in BANDS:
        in_band = np.flatnonzero(band == k)
        assert len(in_band), f"no reading in the band {k} cm-1"
        picked.append(in_band[np.argmin(np.abs(positions[in_band] - (k + 0.5)))])
    values = frame.to_numpy(dtype=float)[:, picked]
    return pd.DataFrame(values, columns=[f"{PREFIX}{k}" for k in BANDS], index=frame.index)


def numeric_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """The readings whose column name is a wavenumber; the source's code drops the others (and the label)."""
    keep = []
    for name in frame.columns:
        try:
            float(name)
        except ValueError:
            continue
        keep.append(name)
    return frame[keep]


class RamanMlrod(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Which mineral sits at a point of a rock never measured before, judged from one Raman spectrum?",
        use_case=(
            "A planetary scientist, or a rover's software, identifies the minerals of a rock target from Raman point "
            "spectra, clean or under Mars-like basalt dust, to interpret the target and decide what to measure next "
            '(Berlanga et al. 2022, abstract: the CNN "can facilitate scientist Raman spectral interpretation on '
            'Earth and autonomous rover decision-making on planets like Mars").'
        ),
        row=(
            "One Raman point spectrum from a map of a sample: 90,387 spectra from 35 maps of 12 reference "
            "minerals and 3 binary powder mixtures, and 34,857 spectra from maps of a gabbro slab and a granite slab "
            "under 0% and 50% basalt dust cover."
        ),
        predicted=(
            "The mineral at the point, one of the source's 15 classes: 12 minerals and 3 binary 50/50 mixtures. The "
            "gabbro slab holds 6 of them and the granite slab 9. The answer is always one of the 15: there is no "
            "'unknown'."
        ),
        known=(
            "The spectrum alone, as the instrument read it (no cosmic-ray removal, baseline removal or "
            "normalisation), one reading in each of the source's 950 bands of 1 cm-1 from 150 to 1,099 cm-1."
        ),
        split=(
            "As in the source: the reference maps train, and one test fold holds both rock slabs, with and without "
            "dust, neither seen in training. The score can be read per rock."
        ),
        changes=(
            "We drop the 4,817 granite points whose label is dust rather than a mineral, repair the code of the "
            "gabbro's plagioclase under dust from microcline to anorthite, move a 46-spectrum powder map named after "
            "the gabbro to training, put every map on the source's 1 cm-1 grid with one reading per band, and set "
            "the damaged bands of three reference spectra missing."
        ),
        fit="approximate",
        fit_reason=(
            "A laboratory Raman microscope on hand samples, powders and two dusted rock slabs stands in for a "
            "rover's coarser instrument (SuperCam, RLS: 6-12 cm-1). The answer is a closed set with no 'no call' for "
            "a spot of dust, and the slab labels, set by hand and checked against the source's CNN, name the grain in the gabbro and the "
            "spot in the granite. Two test rocks only."
        ),
    )

    # Dataset
    unique_name = "raman_mlrod"
    year = "2022"
    domain = "chemistry & material science"
    source = "Other"
    source_url = "https://doi.org/10.48484/PWRB-R137"
    license = "CC BY-NC (NASA AHED's text; its badge links CC BY-NC-ND 4.0)"
    data_tags = ()
    download_description = """
        The 41 map files of the ML Raman Open Dataset are on the Open Data Repository (https://odr.io/MLROD,
        doi:10.48484/PWRB-R137), which answers automated requests with a reCAPTCHA page (2026-11-09); in a browser the
        files download one by one under the names below. The raman-data package (github.com/ml-lab-htw/raman_data,
        `MiscLoader._load_mlrod`, the loader behind RamanBench) keeps the same 41 files as one zip on Google Drive,
        which this definition was built from (625,358,111 bytes, sha256
        10178a4a89cd6d9c8ca2bbb1f85d1db4095cd6af84166c1ecf505519ef2caaf7 on 2026-11-09):

        mkdir -p local-data-warehouse/raman_mlrod && cd local-data-warehouse/raman_mlrod
        curl -L -o mlrod.zip "https://drive.usercontent.google.com/download?id=1NDlDORvkoruwKMFP6y4sAf8M3KuZ6WnS&export=download&confirm=t"
        unzip mlrod.zip "mlrod/*"

        The files are local-data-warehouse/raman_mlrod/mlrod/*.csv: 34 `*_train_*` maps and 7 `L_raw_*_test_*` maps.
    """
    bibtex = r"""
        @article{berlanga2022cnn,
          title={Convolutional Neural Networks as a Tool for {Raman} Spectral Mineral Classification Under Low Signal, Dusty {Mars} Conditions},
          author={Berlanga, Genesis and Williams, Quentin and Temiquel, Nathan},
          journal={Earth and Space Science},
          volume={9},
          number={10},
          pages={e2021EA002125},
          year={2022},
          doi={10.1029/2021EA002125}
        }
        @misc{berlanga2022mlrod,
          title={Machine Learning {Raman} Open Dataset ({MLROD})},
          author={Berlanga, Genesis and Temiquel, Nathan and Williams, Quentin},
          howpublished={Open Data Repository},
          year={2022},
          doi={10.48484/PWRB-R137}
        }
    """
    curation_comments = """
        We start with the 41 map files of the ML Raman Open Dataset (Berlanga, Williams and Temiquel 2022; odr.io/MLROD): 34 maps of 12 reference minerals and 3 binary powder mixtures (`*_train_*`, 90,341 spectra) and 7 maps named after a gabbro and a granite slab (`L_raw_*_test_*`, 39,720 spectra), each map a CSV with one Raman spectrum per row, the readings by wavenumber in the columns and the source's integer label in the last. Every file is used. The paper (Berlanga et al. 2022, the PDF the curator supplied on 2026-11-09), the source's code (Spec-CNN, Zenodo 10.5281/zenodo.7036374: its README, `helper.py` and notebooks), the abstract, NASA AHED's dataset page and Sineesh and Kamsali (2026, arXiv:2601.16107, Sec. 4.1 and 5.3), who downloaded the files from ODR, are what we read; ODR's page answers this machine with a reCAPTCHA.

        - Prediction point: a Raman point spectrum of a rock target has been measured, clean or through dust; which mineral it shows is not known. Only the spectrum is known. The file names also carry the integration time and the dust level; neither is a feature: the time is set per reference map (0.03 s to 120 s), so it would name the class, and the dust level is unknown on a real target. The answer is one of the 15 classes; the scientist's "no call" is not part of the task (the dust points are dropped, below).
        - Provenance of the files: the raman-data mirror holds the same 41 files and row counts as Sineesh and Kamsali's ODR download ("the training dataset had 90,341 spectra"; the test sets "Gabbro: 8,952 clean / 9,740 dusty; Granite: 11,028 and 10,000"), and the label codes match the source's notebook output (its clean-test support per class, e.g. 5,951 quartz, 3,537 anorthite, 2,166 microcline, equals our counts). Three files downloaded from ODR in a browser (2026-11-09: `L_raw_gabbro50dust_test_015s_9740`, `L_raw_granite0dust_test_015s_4084_final`, `qtzalb_train_60s_3000`) equal the mirror's byte for byte (size and sha256), although the mirror's macOS metadata shows two files were opened in Apple Numbers; `L_raw_granite50dust_test_015s_10000` and ODR's file list are not checked yet.
        - The task follows the source's design (Spec-CNN, `Notebook-CNN-Raw_Data.ipynb`: the model is fit on the reference maps and tested on the slab maps together): the reference maps train, both slabs are tested in one fold, each spectrum one prediction. The source's own 80/20 validation split is random over the reference spectra and scores 99-100% per class: neighbouring points of a map are near copies (a logistic regression on 100 principal components of the standard-normal-variate spectra scores log loss 0.072 and accuracy 0.984 on a random third of all spectra, against 0.63 to 1.64 and 0.60 to 0.89 on a held-out rock; 2026-11-09), so a random split would reward recognising a map (SPLIT-29). Training on one slab and testing the other was tried and left: the two rocks share almost no minerals, so the training slab tells which classes the test rock lacks (down-weighting them lowers the best honest model's log loss from 0.666 to 0.477 with no test row seen), and it makes an honest model worse (an untuned LightGBM 2.757 against 2.410 trained on the reference maps alone; review panel, 2026-11-09).
        - The grid: the maps come on 12 different wavenumber grids (1,189 to 3,670 readings, 52 to 1,801 cm-1, steps of 0.45 to 0.87 cm-1), so a 1 cm-1 band holds one to four readings. We use the source's common grid (Spec-CNN `helper.raw_processing` and the (950, 1) input layer of its raw-spectrum CNN; the 5 cm-1 bands of its README belong to its wavelet path): columns whose name is no number are dropped and the spectrum is trimmed to 150-1,100 cm-1 in 950 bands of 1 cm-1. In each band the source keeps the minimum of the readings, a cosmic-ray step ("cleans up the noise created by cosmic rays"); we keep the one reading nearest the band's centre (k + 0.5 cm-1). The minimum left a trace of the grid by class: a band of a fine grid holds two readings, so its minimum is lower and the spectrum rougher, and some classes come only on coarse grids (augite, calcite, gypsum, the mixtures) or mostly on fine ones (muscovite, enstatite, biotite); a template of that comb told the grids apart at ROC AUC 0.651, and 0.536 with one reading per band, while the logistic regression's log loss went from 1.451 to 1.253 on the gabbro and from 0.485 to 0.497 on the granite (review panel, 2026-11-09). RamanBench instead interpolates to 1,836 positions from 141 to 1,100 cm-1, an interpolation of its own.
        - The spectrum ships on that grid and is declared as one (`special_features`, CLEAN-26), state `raw`: the source applied "No cosmic ray removal, baseline correction, or other preprocessing" (raman-data's card; the abstract: "no traditional spectral preprocessing such as cosmic ray or baseline removal was employed"), and one reading per band keeps that. The columns are `raman_<k>` for the band [k, k + 1) cm-1. 136 spectra (0.1%; 19 of them on the slabs) reach the detector's ceiling near 65,535 counts in some band; readings, kept. Four of them, rows 197-200 of `hb_train_120s_1225_01` (hornblende, 120 s), are saturated in most bands and show no spectral shape; kept as the instrument read them.
        - Three reference spectra are damaged and their bands set missing (CLEAN-26, inner positions; the rows stay, they train and are never tested): the last row of `cal_train_1s_2732` reads exactly 0 from 938 cm-1 and the last row of `qtz_train_003s_1148` from 613 cm-1 to the end of their grids, an acquisition cut short; row 2,456 of `qtzalb_train_60s_3000` holds a spreadsheet fill-down, 346 readings from 581.4 to 858 cm-1 equal to k x 4.11843, rising on to 1,100 cm-1 far below the row's level (the 1st percentile of every other spectrum is 1,040 counts or more, of this one 51), so its bands from 581 cm-1 are missing. 1,168 cells in 3 rows. ODR's own file holds the same fill (byte match, 2026-11-09), so there is no clean row to repair it from.
        - One malformed header (`1630.89.1` in `L_raw_granite0dust_test_015s_4084_final`, which raman-data patches) lies outside 150-1,100 cm-1 and is dropped with the other non-numeric names, as in the source's code.
        - Code 15 (4,817 spectra, all in the granite map under 50% dust) is no mineral of the source's 15 classes: no reference map carries it, the source's CNN has 15 outputs (codes 0-14) and its code gives 15 to an unknown (`cnnmodel_raw.dec_pred`: a prediction whose top probability is below the threshold becomes 15), raman-data names it "Granite slab - 50% dust", and its median spectrum shows the strongest bands at 506, 999-1,010 and 629-655 cm-1, feldspar and pyroxene, the minerals of basalt dust. Its rows are dropped: the truth there is the dust, which the reference maps give no class for, and Sineesh and Kamsali also leave them out ("a label that does not correspond to any of the labels in the training dataset. We have ignored these samples").
        - The gabbro's plagioclase under dust carries code 9 (microcline; 3,540 spectra, rows 4,600-8,139 of `L_raw_gabbro50dust_test_015s_9740`), where the same rock's plagioclase under 0% dust carries 8 (anorthite; 3,537 spectra). Repaired to 8 (PROV-13): the block's mean spectrum (after the standard normal variate) matches the clean gabbro's anorthite block and not the reference microcline or the granite's own microcline (Decisions); its strongest bands sit at 506 and 482 cm-1 like the clean gabbro's anorthite (507, 482), not at microcline's 511 and 473; a logistic regression trained on the reference maps calls 1,911 of its spectra anorthite and almost none microcline; gabbro, a rock of plagioclase and pyroxene, rarely holds potassium feldspar; and the gabbro maps under 0% and 50% dust hold blocks of the same minerals of nearly the same size (augite 4,091 and 4,200, calcite 400 and 400, plagioclase 3,537 and 3,540). Sineesh and Kamsali's dusty-gabbro accuracies of 40-49% for every model fit a block scored against the wrong label.
        - The class names come from the codes of the training files (qtz 0, albite 1, hb 2, bt 3, ms 4, fo 5, aug 6, en 7, an 8, mc 9, cal 10, gyp 11, qtzalb 12, foaug 13, foalb 14) and the mineral list of Sineesh and Kamsali (Sec. 4.1). The gabbro's plagioclase is whatever the source calls anorthite; its composition is not stated.
        - The slab maps were labelled by hand: "Over 30,000 spectra were manually labeled by the authors over the span of 500 hr and three full passes. ... With each pass, the test set was run through the CNN and the misclassified spectra often identified human mineral classification errors, effectively correcting any manual labeling mistakes" (paper, Sec. 4.2 "Labeling Test Models"). So the labels are a person's call, checked against the source's CNN, which leans them toward that CNN where a person changed a call after a disagreement. They differ by rock: the gabbro maps in whole blocks of one mineral (6 and 4 runs), so a dusty point keeps its grain's mineral (a dust detector trained on the granite's code 15 calls about 610 forsterite and 800 plagioclase points of the dusty gabbro dust); the granite maps point by point (135 to 3,691 runs), where 147 dusty points labelled forsterite show the dust's iron-rich olivine (817 and 850 cm-1). The 46-spectrum map `L_raw_gabbro0dust_test_015s_46_final` holds 16 gypsum and 30 forsterite-albite mix spectra, a lab powder mixture and no point of a gabbro slab, and the source's row ids read "gyp_foalb_test": it trains, as a group of its own. The paper counts it with the gabbro (its 8,952 clean gabbro spectra include these 46, and it lists gypsum among the gabbro's test minerals); a gabbro holds no 50/50 forsterite-albite powder, so the map stays out of the test. `L_raw_granite0dust_test_030s_1373_final` (873 hornblende, 500 muscovite; row ids "granite0dust_test_hb_ms") holds granite minerals and stays with the granite.
        - The reference maps come from 12 hand-sample specimens of their own localities, not from the slabs (paper, Sec. 2 and Table 1: augite from Trento Province, Italy, 6,103 spectra, the two augite maps together; muscovite from Ottawa, Ontario, 5,900; the gabbro slab from Madagascar, the granite's locality unknown). This settles a question the data raised: `aug_train_15s_1000` matches the gabbro's augite as closely as a map matches itself, and `ms_train_015s_5900` the granite's muscovite block. Similarity proves no shared specimen (quartz maps match the granite's quartz as closely), and the paper places both maps on other specimens, so they stay reference maps (SPLIT-24). The stake, for the record: without the augite map a logistic regression's accuracy on the gabbro's augite (44% of the gabbro rows) falls from 0.82 to 0.00 and its gabbro log loss from 0.78 to 2.55 (the class shares give 2.90); dropping the larger augite map changes nothing (review panel, 2026-11-09).
        - No two of the 130,061 spectra are equal (raw readings on the 950 bands).
        - The instrument: a Horiba spectrometer at 532 nm with an automated mapping stage of 0.1 µm resolution (paper, Sec. 3.1; a LabRAM HR Evolution per raman-data's card). The abstract's "500,000+ Raman spectra" is more than the 130,061 the 41 files hold, but the paper's Table 1 lists about 130,000 (89,121 training and 39,720 test spectra; our training maps hold 1,100 more albite and 120 more forsterite-augite mix spectra), so the files match the paper's own data; whether ODR holds further maps is open.
        - Each spectrum is one decision and is scored per row (MET-17 does not apply): the source predicts and scores every point.
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): the test spectra of one rock cluster by mineral (a test spectrum's nearest test spectrum has the same label 96% of the time in the gabbro, 97% in the granite), so averaging each prediction over its 50 nearest test spectra helps: measured on one rock per fold, an untuned LightGBM's log loss fell by 0.99 and 1.69, the best honest model's by 0.06 and 0.09; a prior of the test rock's classes estimated from the test rows, self-training on them and weights from a train-against-test classifier help one rock and hurt the other (review panel, 2026-11-09). A deployed model sees one spectrum at a time. The split cannot block this; the protocol line in the splits comment does. Revisit if the benchmark scores test rows in batches it controls.
        - Rare classes weigh more in the loss than in the rows: on the test rows the quartz-albite mix is 0.81% of the rows and 6.42% of a logistic regression's loss, biotite 1.28% and 4.51% (review panel, 2026-11-09); every point is scored on its own.
        - Encodings (2026-11-09, the shipped split, the reference maps training and both slabs tested, untuned; log loss on the gabbro and the granite): a logistic regression on 100 principal components of the standardised bands scores 0.919 and 1.121 on the spectrum as it is, 1.528 and 0.493 with ALS and SNV, 1.584 and 0.992 with SNV, 1.355 and 0.978 with the Savitzky-Golay first derivative; LightGBM (200 trees, 30% of the bands per tree, 40,000 training rows) 2.099 and 2.370 as it is, 0.571 and 0.398 with ALS and SNV, 1.079 and 1.091 with SNV, 0.946 and 0.688 with the derivative. Every candidate helps LightGBM on both rocks, none helps the logistic regression on the gabbro. The recommended encoding stays the spectrum as it is, the field's default for a raw spectrum (CLEAN-26), not a choice fitted on the test rocks; a model is free to apply ALS and SNV itself.
    """

    # Task
    target = "mineral"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            'The abstract reports identification with "+99% success", and the source\'s code (Spec-CNN, Zenodo '
            "10.5281/zenodo.7036374) scores the test maps with scikit-learn's classification_report on the most "
            "likely class: accuracy, and precision, recall and F1 per class. Its threshold for an unknown (dec_pred, "
            "0.95 by default, 0.5 in the notebook) shapes only the validation confusion matrix. Several threshold "
            "metrics and no cost of a confusion, so no deliberate choice (MET-5, MET-6): the multiclass fallback, "
            "log loss."
        ),
    )
    grouping = Grouping(
        on="specimen",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is one rock slab (the gabbro, the granite: every map of it, at 0% and 50% dust cover, by the source's file names) or one map of a reference mineral or a powder mixture (the 46-spectrum gypsum and forsterite-albite map named after the gabbro is one of these). The use case identifies the minerals of a rock target never measured before (Berlanga et al. 2022: "autonomous rover decision-making on planets like Mars"), and the source tests on the slabs after training on the reference maps, so whole rocks are held out. The gabbro maps under 0% and 50% dust hold blocks of the same minerals of nearly the same size, possibly the same spots before and after dusting, so the maps of one slab stay together. The reference maps are in the training side and never tested, as in the source. Each spectrum is one prediction, and the labels are per point (a slab holds several minerals).
        """,
    )
    splits_comment = """
        One split, as in the source (Spec-CNN `Notebook-CNN-Raw_Data.ipynb`: fit on the reference maps, tested on the slab maps): the 90,387 spectra of the 35 reference and powder maps train, and one test fold holds both slabs, the gabbro (18,646 spectra) and the granite (16,211 after the dust points are dropped), with and without dust. One repeat and one fold: with two rocks there is no other partition that keeps every test rock unseen, and training on one slab to test the other lets the training slab tell which classes the test rock lacks (curation notes). Score the fold by rock too, from the `specimen` group: each rock's score rests on few units (the gabbro on 12 mineral blocks), and the spread between folds understates the noise 4 to 13 times when read per row. The reference maps come from separate hand samples, not from the slabs (paper, Table 1; curation notes).

        Protocol (LEAK-9): each test spectrum is predicted on its own, from the training rows and its own readings only: no use of other test rows (no averaging over neighbouring test spectra, no class prior estimated on the test rows, no self-training on them, no weights from a classifier of training against test rows) and no preprocessing fitted on test rows. A method that does is called out and not benchmarked.
    """

    special_features = (
        Spectrum(
            name="raman_spectrum",
            prefix=PREFIX,
            unit="cm-1",
            technique="raman",
            state="raw",
            description=(
                "A Raman point spectrum from a map of a sample, in counts as read, with no cosmic-ray removal, "
                "baseline correction or normalisation, on the source's common grid of 1 cm-1 bands from 150 to "
                "1,099 cm-1 (Spec-CNN `helper.raw_processing`): one reading per band, the one nearest the band's "
                "centre, the column named by the band's lower edge."
            ),
        ),
    )

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        # One frame per map: the readings by wavenumber and the source's `label`, indexed by `og-idx`.
        files = sorted((raw_dir / "mlrod").glob("*.csv"))
        assert len(files) == 41, len(files)
        return {path.stem: pd.read_csv(path, index_col=0) for path in files}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        frames = []
        for stem, frame in raw.items():
            labels = frame["label"].to_numpy()
            readings = numeric_columns(frame)
            # 1. The source's common grid: the wavenumber columns only, one reading per 1 cm-1 band, 150 to 1,099 cm-1.
            spectra = one_reading_per_band(readings)
            # 2. A spectrum cut short reads exactly 0 to the end of its grid: those bands are missing (CLEAN-26).
            spectra = spectra.mask(spectra == 0)
            # 3. The spreadsheet fill-down of one reference spectrum: its bands from 581 cm-1 are missing.
            if stem == FILLED_MAP:
                row = readings.loc[FILLED_ROW].to_numpy(dtype=float)
                positions = readings.columns.astype(float).to_numpy()
                fill = row[(positions > FILLED_FROM) & (positions < 858.5)]
                assert len(fill) == 346
                assert np.allclose(fill, FILL_STEP * np.arange(1, 347), atol=1e-3)
                spectra.loc[FILLED_ROW, [f"{PREFIX}{k}" for k in BANDS if k >= FILLED_FROM]] = np.nan
            spectra = spectra.reset_index(drop=True)
            # 4. The group: the rock slab, or the reference (or powder) map.
            rock = rock_of(stem)
            spectra["specimen"] = f"{rock} slab" if rock else f"reference map {stem}"
            # 5. Repair the dusty gabbro's plagioclase block: code 9 (microcline) is the clean map's 8 (anorthite).
            if stem == GABBRO_DUSTY:
                labels = np.where(labels == 9, 8, labels)
            spectra["code"] = labels
            frames.append(spectra)
        df = pd.concat(frames, ignore_index=True)
        # Guard: the missing cells are the two cut-short spectra's (162 + 487) and the filled row's (519).
        bands = [f"{PREFIX}{k}" for k in BANDS]
        assert int(df[bands].isna().sum().sum()) == 1168, int(df[bands].isna().sum().sum())
        assert int(df[bands].isna().any(axis=1).sum()) == 3
        # 6. Drop the dust points of the granite: code 15 names no mineral and no reference map carries it.
        df = df[df["code"] != DUST_CODE].reset_index(drop=True)
        df[self.target] = df.pop("code").map(CLASS_NAMES)
        assert df[self.target].notna().all()
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["specimen"])

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # One split: the reference maps train, both slabs are tested together (the source's design).
        specimen = df["specimen"].astype(str).to_numpy()
        slab = np.isin(specimen, ["gabbro slab", "granite slab"])
        splits = {0: {0: (np.flatnonzero(~slab).tolist(), np.flatnonzero(slab).tolist())}}
        return SplitPlan(splits=splits)

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        # The source's codes by map group, before the repair and the drop.
        counts = []
        for stem, frame in raw.items():
            rock = rock_of(stem)
            dust = "50% dust" if "50dust" in stem else "0% dust"
            for code, n in frame["label"].value_counts().items():
                maps = f"{rock}, {dust}" if rock else ("powder map" if stem == POWDER_MAP else "reference maps")
                counts.append({"maps": maps, "code": int(code), "spectra": int(n)})
        by_code = (
            pd.DataFrame(counts)
            .groupby(["code", "maps"])["spectra"]
            .sum()
            .unstack(fill_value=0)
            .rename(index=lambda c: f"{c} {CLASS_NAMES.get(c, 'dust (no mineral)')}")
        )

        # The dusty gabbro's code-9 block against the clean gabbro's anorthite, the reference feldspars and the
        # granite's own microcline: correlation of the mean spectra after the standard normal variate, and the
        # strongest bands of the median spectrum.
        def snv(frame: pd.DataFrame) -> np.ndarray:
            values = one_reading_per_band(numeric_columns(frame)).to_numpy()
            return (values - values.mean(axis=1, keepdims=True)) / values.std(axis=1, keepdims=True)

        def strongest_bands(values: np.ndarray, k: int = 4) -> str:
            median = np.median(values, axis=0)
            median = median - pd.Series(median).rolling(101, center=True, min_periods=1).min().to_numpy()
            picked: list[int] = []
            for i in np.argsort(-median, kind="stable"):
                if all(abs(i - j) > 10 for j in picked):
                    picked.append(int(i))
                if len(picked) == k:
                    break
            return ", ".join(str(BANDS[i]) for i in picked)

        dusty = raw[GABBRO_DUSTY]
        clean = raw["L_raw_gabbro0dust_test_015s_8906_final"]
        granite = np.vstack(
            [
                snv(raw[name][raw[name]["label"] == 9])
                for name in ("L_raw_granite0dust_test_015s_4084_final", "L_raw_granite0dust_test_015s_5571_final")
            ]
        )
        blocks = {
            "gabbro 50% dust, code 9 (repaired to 8)": snv(dusty[dusty["label"] == 9]),
            "gabbro 0% dust, code 8 (anorthite)": snv(clean[clean["label"] == 8]),
            "reference anorthite (code 8)": snv(raw["an_train_015s_5600"]),
            "reference microcline (code 9)": np.vstack([snv(raw["mc_train_015s_3243"]), snv(raw["mc_train_3s_2357"])]),
            "granite 0% dust, code 9 (microcline in the rock)": granite,
        }
        anchor = blocks["gabbro 50% dust, code 9 (repaired to 8)"].mean(axis=0)
        repair = pd.DataFrame(
            [
                {
                    "block": name,
                    "spectra": len(values),
                    "correlation with the dusty code-9 block": round(
                        float(np.corrcoef(anchor, values.mean(axis=0))[0, 1]), 3
                    ),
                    "strongest bands (cm-1)": strongest_bands(values),
                }
                for name, values in blocks.items()
            ]
        )
        side = np.where(
            df["specimen"] == "gabbro slab",
            "test: gabbro slab",
            np.where(df["specimen"] == "granite slab", "test: granite slab", "train: reference and powder maps"),
        )
        by_side = (
            pd.DataFrame({"mineral": df[self.target].astype(str), "maps": side})
            .groupby(["mineral", "maps"])
            .size()
            .unstack(fill_value=0)
        )
        return [
            Decision(
                title="The source's codes by map: the dust code dropped, the dusty gabbro's plagioclase repaired",
                why=(
                    "Code 15, the source's code for an unknown, occurs only in the granite map under 50% dust and no "
                    "reference map carries it, so its rows go; code 9 (microcline) in the dusty gabbro is the "
                    "plagioclase the clean gabbro calls anorthite (code 8), so it becomes 8 (PROV-13). The powder "
                    "map's gypsum and forsterite-albite mix are no gabbro minerals, so it trains."
                ),
                evidence=by_code,
            ),
            Decision(
                title="The dusty gabbro's code-9 block is anorthite, not microcline",
                why=(
                    "Its mean spectrum matches the clean gabbro's anorthite block and neither the reference "
                    "microcline nor the microcline of the granite slab, and its strongest bands sit where "
                    "plagioclase's do (about 507 and 482 cm-1), not where microcline's do (511 and 473 cm-1)."
                ),
                evidence=repair,
            ),
            Decision(
                title="Spectra per mineral: the training maps and the two test rocks",
                why=(
                    "One split: the reference and powder maps train, both slabs are tested together. Every mineral "
                    "of a test rock has reference maps; gypsum has no test rows."
                ),
                evidence=by_side,
            ),
        ]

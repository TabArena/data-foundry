"""Curated dataset definition for `bacteria_id_raman` (data-foundry v2). Evidence: README.md."""

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
    splits as protocol,
)

PREFIX = "raman_"

# The eight empiric treatment groups of the source's `config.py` (`antibiotics`), by the integer code its label files
# and `ATCC_GROUPINGS` use. The clinical files hold five of them: 0, 2, 3, 5 and 6.
TREATMENTS = {
    0: "Meropenem",
    1: "Ciprofloxacin",
    2: "Piperacillin-tazobactam",
    3: "Vancomycin",
    4: "Ceftriaxone",
    5: "Penicillin",
    6: "Daptomycin",
    7: "Caspofungin",
}

# The 30 reference isolates (`config.py`, `STRAINS`) and the treatment group of each (`ATCC_GROUPINGS`).
REFERENCE_ISOLATES = {
    0: ("C. albicans", 7),
    1: ("C. glabrata", 7),
    2: ("K. aerogenes", 0),
    3: ("E. coli 1", 0),
    4: ("E. coli 2", 0),
    5: ("E. faecium", 6),
    6: ("E. faecalis 1", 5),
    7: ("E. faecalis 2", 5),
    8: ("E. cloacae", 0),
    9: ("K. pneumoniae 1", 0),
    10: ("K. pneumoniae 2", 0),
    11: ("P. mirabilis", 0),
    12: ("P. aeruginosa 1", 2),
    13: ("P. aeruginosa 2", 2),
    14: ("MSSA 1", 3),
    15: ("MSSA 3", 3),
    16: ("MRSA 1 (isogenic)", 3),
    17: ("MRSA 2", 3),
    18: ("MSSA 2", 3),
    19: ("S. enterica", 1),
    20: ("S. epidermidis", 3),
    21: ("S. lugdunensis", 3),
    22: ("S. marcescens", 0),
    23: ("S. pneumoniae 2", 4),
    24: ("S. pneumoniae 1", 4),
    25: ("S. sanguinis", 5),
    26: ("Group A Strep.", 5),
    27: ("Group B Strep.", 5),
    28: ("Group C Strep.", 5),
    29: ("Group G Strep.", 5),
}

# The reference library: the training file and the separately measured fine-tuning and test files of the 30 isolates.
REFERENCE_FILES = ("reference", "finetune", "test")

# The two clinical files: the spectra of one patient's isolate are consecutive blocks of this many rows, five patients
# per treatment group (the source's `3_clinical_finetuning.ipynb`: `start_idx = 5 * 400 * group_idx + 400 * patient`,
# and `5 * 100 * group_idx + 100 * patient` for 2019). The groups are not in code order: the 2018 blocks run through the
# codes 0, 6, 5, 3, 2 and the 2019 blocks through 0, 5, 6, 3, 2; the labels come from the label files, not the order.
CLINICAL_FILES = {"2018clinical": 400, "2019clinical": 100}

# The patients are numbered in this seeded random order within each year, so the id does not follow the label blocks.
PATIENT_ORDER_SEED = 4267


class BacteriaIdRaman(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Which empiric antibiotic does the bacterium in a new patient's isolate call for, judged from the "
            "isolate's Raman spectra?"
        ),
        use_case=(
            "A clinical microbiology laboratory measures Raman spectra of a patient's bacterial isolate, and the "
            "physician picks the empiric antibiotic within hours instead of waiting days for culture-based "
            'identification (Ho et al. 2019: "the priority for physicians is choosing the correct antibiotic").'
        ),
        row=(
            "One Raman spectrum of one bacterial isolate: 12,500 spectra of 50 patients' isolates (Palo Alto VA "
            "Medical Center 2018, 400 each; Stanford Hospital 2019, 100 each), and a reference library of 66,000 "
            "spectra of 30 reference isolates, used for training only."
        ),
        predicted=(
            "The recommended empiric treatment of the isolate's species, one of the source's eight groups; the "
            "patients carry five: meropenem, piperacillin-tazobactam, vancomycin, penicillin and daptomycin."
        ),
        known=(
            "The isolate's spectra alone (100 or 400 per patient), each with 1,000 positions from 382 to 1,792 cm-1, "
            "background-corrected and scaled to run from 0 to 1 by the source."
        ),
        split=(
            "Whole patients are held out: a test fold holds 25 patients, 5 per treatment group, never seen in "
            "training. Training adds the other patients and the whole reference library. One identification per "
            "patient, from all of its spectra, so each patient counts once in the score."
        ),
        changes=(
            "We label the 30 reference isolates with the source's treatment groups and use them for training only, "
            "recover each patient from the row order the source documents, number the patients at random, and score "
            "one prediction per patient."
        ),
        fit="approximate",
        fit_reason=(
            "Cultured monolayers, while the use case aims at a few cells without culture; at this stage MALDI-TOF or "
            "a PCR panel gives the species within an hour. The Gram stain, known first, does not ship. Five species, "
            "one per group, so the test asks which of five; the drug is a fixed lookup per species. The two years are "
            "pooled, while a lab trains on its past."
        ),
    )

    # Dataset
    unique_name = "bacteria_id_raman"
    year = "2019"
    domain = "medical & healthcare"
    source = "GitHub"
    source_url = "https://github.com/csho33/bacteria-ID"
    license = "MIT"
    data_tags = ()
    download_description = """
        The arrays are in the Dropbox folder linked from the README of https://github.com/csho33/bacteria-ID
        ("The data for the experiments can be downloaded here"); the folder downloads as one zip of 628,639,018
        bytes (sha256 05f0978e2bcfe96f7f89667734a925f3d2dd261337e00a6d051df30e3006074f on 2026-11-08).

        mkdir -p local-data-warehouse/bacteria_id_raman/data && cd local-data-warehouse/bacteria_id_raman
        curl -L -o data.zip "https://www.dropbox.com/sh/gmgduvzyl5tken6/AABtSWXWPjoUBkKyC2e7Ag6Da?dl=1"
        unzip -j data.zip "*.npy" -d data
    """
    bibtex = r"""
        @article{ho2019rapid,
          title={Rapid identification of pathogenic bacteria using {Raman} spectroscopy and deep learning},
          author={Ho, Chi-Sing and Jean, Neal and Hogan, Catherine A. and Blackmon, Lena and Jeffrey, Stefanie S. and Holodniy, Mark and Banaei, Niaz and Saleh, Amr A. E. and Ermon, Stefano and Dionne, Jennifer},
          journal={Nature Communications},
          volume={10},
          number={1},
          pages={4927},
          year={2019},
          doi={10.1038/s41467-019-12898-9}
        }
    """
    curation_comments = """
        We start with the five spectrum files (`X_reference`, `X_finetune`, `X_test`, `X_2018clinical`, `X_2019clinical`), their label files and `wavenumbers.npy` from the Dropbox folder of github.com/csho33/bacteria-ID (Ho et al. 2019); every file is used.

        - Prediction point: a patient's isolate has been measured on the Raman microscope, its identification and susceptibility are not known yet, and the physician picks the empiric antibiotic. Only the isolate's spectra are known; nothing else ships.
        - The framing (USE-5, SPLIT-4, SPLIT-29): the treatment group of a new patient's isolate, not the source's 30-isolate task. The 30 classes are lab strains (two strains of E. coli, three of MSSA), a distinction no physician acts on, and its test file holds new cultures of the same 30 strains, while a patient brings a strain never measured. On that task a logistic regression on 100 principal components scores 74.0% accuracy on the source's test file (the paper's logistic regression: 75.7%) against 93.1% on 3,000 spectra held out at random from the reference and fine-tuning files (2026-11-08). Most of that gap is the file or measurement session, not the culture: trained on the reference file, the same model scores 92.6% on spectra held out of that file against 45.2% and 43.6% on the fine-tuning and test files of the same strains, measured at 2 s; within the 2 s files a new culture costs about 5 to 14 points (77.5% against 72.1% trained on the library and two thirds of the fine-tuning file; 90.6% against 76.5% on that part of the fine-tuning file alone; review panel, 2026-11-09). So a split over spectra rewards the map and the session.
        - The prediction unit (SPLIT-23): one prediction per patient, from that patient's spectra, as the source identifies a patient by a majority vote over 10 of its spectra (Results); the patient's prediction is the mean of its spectra's class probabilities (`prediction_unit="group"`, `aggregation="mean"`), and a model may use all of the patient's 100 or 400 spectra (`context="all_rows"`), which the lab has. The mean over 10 spectra and over all of them differ by 0.004 log loss (logistic regression on 100 principal components). The unit changes which model wins: between the per-spectrum score of the first draft and the per-patient one, four untuned models rank at Kendall tau 0.48 on average, and the best model differs on 36 of 60 splits (3-fold splits, review panel, 2026-11-09). Per patient, accuracy saturates (0.96 to 1.00 for every model family) but log loss does not. The mean rewards models that are sharp on each spectrum, so a method that pools a patient's spectra differently should return its own patient prediction (the scorer takes it; the harness decides). Each patient counts once whether it has 400 spectra (2018) or 100 (2019), so the score needs no weight (MET-17); a weight input would be read at each patient's first row and make a 2019 patient count four times a 2018 patient.
        - The reference library: the 66,000 spectra of the 30 reference isolates (2,000 in the training file, 100 each in the fine-tuning and test files) are labelled with the treatment group `config.py` gives each isolate (`ATCC_GROUPINGS`) and sit in every training side, never in a test fold, as the source pre-trains its clinical model on them for the eight groups. Three groups (ciprofloxacin, ceftriaxone, caspofungin) occur only there, in 5 reference isolates (C. albicans, C. glabrata, S. enterica and the two S. pneumoniae; 11,000 spectra), so no test fold holds them; they are kept, as the source pre-trains on all eight groups and a lab's library holds them (TP-6). Its worth at the declared unit (the first 20 shipped splits, untuned, per-patient log loss, 2026-11-09): training with it lowers the loss of a logistic regression on 100 principal components on 10 of 20 splits (mean 0.120 against 0.131 without), of a strongly regularised logistic regression (C=0.01) on 12 (0.148 against 0.163) and of kNN on 9 (0.251 against 0.262). The library's class shares and its three never-tested groups are part of what the log loss scores: renormalising each spectrum's probabilities over the five patient groups lowers these three losses by 19%, 18% and 10%, mostly a level shift (the three models keep their order on 20 of 20 splits). On the 3-fold splits of the first draft, its gain over training on the patients alone rested on two vancomycin patients (now 2018-07 and 2019-02). The class-share dummy pays for the library's prior: 1.975 on average (1.958 to 1.992) against ln 5 = 1.609 for uniform over the five tested groups, so skill measured against the class shares overstates skill against ln 5.
        - The patient is not a column: the clinical files hold the treatment code only. It is recovered from the row order the source's notebook uses (`5 * 400 * group_idx + 400 * patient`; 100-row blocks in 2019), 50 isolates of 100 or 400 spectra (SPLIT-24). Checked on the data (Decisions): within a treatment group, a spectrum's nearest block centroid is its own block for 0.49-0.86 of the spectra, against 0.36-0.59 for blocks shifted by half a patient, in 9 of the 10 file-and-group pairs; in the tenth (2019, penicillin: 0.52 against 0.52) a logistic regression on 30 principal components, cross-validated within the group, still tells the blocks apart at 0.36 accuracy against 0.24 shifted (chance 0.20). Over all offsets the nearest-centroid accuracy is highest at the blocks in 10 of 10 pairs, and the correlation of adjacent rows (map spots in scan order) drops at the block edges in 10 of 10 (review panel). The patients are numbered in a seeded random order within each year (`PATIENT_ORDER_SEED`), so the id does not follow the label blocks (LEAK-33); it is never a feature.
        - The 2018 file holds 25 patients of 400 spectra, as the Results and the notebook say; the Methods say 30.
        - Labels: the codes become the source's antibiotic names (`config.py`, `antibiotics`; TZP written out as piperacillin-tazobactam). The patients' species are not listed in the paper's text ("each species corresponds to a different treatment class", Fig. 4; S. aureus and P. aeruginosa are named); the supplementary table was not read. Inferred, not stated: `config.py`'s comments name the species behind each group (meropenem: E. coli; piperacillin-tazobactam: P. aeruginosa; vancomycin: Staph; penicillin: Strep and E. faecalis; daptomycin: E. faecium), and the nearest reference species of each patient agrees (vancomycin 10 of 10 S. aureus, penicillin 10 of 10 E. faecalis, daptomycin 10 of 10 E. faecium, meropenem 10 of 10 Enterobacterales, piperacillin-tazobactam 6 of 10 P. aeruginosa; review panel).
        - The spectrum ships as published and is declared as one (`special_features`, CLEAN-26), state `processed`: per map the source discarded the 25 spectra of highest intensity (2,025 - 25 = 2,000 per reference isolate), then background-corrected each spectrum by a polynomial of order 5 and scaled it to 0-1 (Methods); every step reads one sample. The columns are named `raman_<cm-1>` from `wavenumbers.npy`, an uneven grid (1.20 to 1.56 cm-1 apart); no value changes. Anomaly: 4.6% to 8.0% of the spectra of each file do not reach exactly 0 (their minimum has a median of 0.024-0.031), and 0.9% to 2.5% do not reach 1, as if scaled before a step we do not know; their minima sit at inner positions, as for the others; kept as published.
        - Measurement settings differ between the files: the fine-tuning, test and 2019 files were measured at 2 s per spectrum, "increased from 1 s to 2 s in order to keep SNR consistent" (Methods), while the reference training set exists at three measurement times and the paper shows its 1 s data; which time the released file and the 2018 file hold is not stated. The reference file's mean spectrum lies far from the test file's (centroid distance 1.92 against 0.71 between the fine-tuning and test files, median over isolates). The year can be read from one spectrum: 2018 against 2019 patients at ROC AUC 0.994, grouped by patient (review panel). The year does not give the label away (5 patients per group in each year), but a batch by class within a year (measurement days) would be read just as easily, and it cannot be tested without dates. No column says which file a spectrum comes from, as no new patient comes with one.
        - Fit (USE-8): the lab has the Gram stain before any identification, and it does not ship; by the groups (meropenem and piperacillin-tazobactam Gram-negative, the other three Gram-positive) 45-52% of the per-spectrum errors of four untuned models cross the Gram line (6 shipped splits of the first draft). At the culture stage of these data MALDI-TOF or a PCR panel gives the species in minutes to an hour. The drug is a fixed lookup per species, so resistance plays no part; the source's clinical MRSA/MSSA classifier reaches 65.4%. The years are pooled: trained on the 2018 patients and tested on the 2019 ones, a logistic regression on 100 principal components scores a per-spectrum log loss of 0.368, against 0.229 pooled (each patient weighted once; review panel, 2026-11-09).
        - Encodings (2026-11-08, the three folds of repeat 0 of the first draft, untuned, per-spectrum log loss with each patient weighted once; logistic regression on 100 principal components, then LightGBM): the spectrum as it is 0.223 and 0.336; SNV 0.216 and 0.307 (lower on 3 of 3 for both); ALS with SNV 0.259 and 0.431 (0 of 3); the Savitzky-Golay first derivative 0.684 and 0.571 (0 of 3), likely because the source already removed the baseline and a derivative sharpens the noise of a low-signal spectrum. The recommended encoding stays the spectrum as it is (CLEAN-26; one dataset is a case for the benchmark's comparison).
        - No two spectra of the 78,500 are equal (exact copies counted over all files).
        - Potential near-copy, kept on purpose (SPLIT-30, SPLIT-24): the 22nd and 23rd patients of the 2018 file (now patient 2018-24 and 2018-21; piperacillin-tazobactam) are about as alike as two halves of one patient's spectra (cross-validated ROC AUC 0.606 between them, against a median of 0.946 for two patients of one group), and each one's log loss drops by 0.21 and 0.14 when the other trains (98th and 93rd percentile of the 166 ordinary same-group pairs), about 0.007 of 0.242 on the mean (per spectrum, logistic regression on 100 principal components, 60 3-fold splits; review panel, 2026-11-09). They may be one isolate measured twice or two clonal strains; the data cannot tell. Six other pairs as alike act like ordinary patients. They stay two groups, as grouping by similarity is barred; patient ids from the authors would settle it (SPLIT-25).
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): the paper's design puts 5 patients of each group in each year, and the year can be read from one spectrum (ROC AUC 0.993 in the task gamer's test), so the make-up of a test fold by year tells a model which groups remain among its patients of that year. Using it lowered the per-patient log loss by 0.014 and 0.033 (two untuned models, better on 53 and 51 of 60 3-fold splits; per spectrum 0.017 and 0.043), and it survives any random grouped split. Reading other test patients' spectra (a neighbour rebuild) gains no more at the patient unit than sharpening each spectrum's prediction on its own, and PCA fitted on all rows gains 0.004. All three are closed by the protocol line in splits_comment, not in the data.
        - Few patients (TP-5): 10 patients per treatment group in all. Two folds give 5 per group and 25 per fold; three folds gave 3 or 4 per group. On the first 20 shipped splits (a logistic regression on 100 principal components, per-patient log loss 0.076 to 0.324 per fold) one patient carries 13% to 34% of a fold's loss, and the patient-bootstrap standard error of one fold's score is 0.032 on a mean of 0.120, so gaps between methods below about 0.03 may not carry to new patients; with three folds one patient carried 16% to 51%. The 60 splits recombine the same 50 patients, so their spread understates how a score would move on new patients.
        - The source's test file was "gathered from separately cultured samples": within an isolate, a logistic regression on 20 principal components tells the fine-tuning file's spectra from the test file's at a median ROC AUC of 0.81 (0.47-1.00 over the 30 isolates), so they are separate measurements, which fits the claim.
    """

    # Task
    target = "empiric_treatment"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "Ho et al. 2019 (Results, Methods, Fig. 4) and the repository's notebooks report accuracy only: the "
            "isolate-level accuracy per spectrum on the reference task, and on the patients the accuracy of the "
            "treatment group identified by a majority vote over 10 random spectra per patient; the notebook's early "
            "stopping also selects models on validation accuracy (`if acc_val > best_val`). It is the field's habit "
            "with no threshold or costs fixed, while a wrong empiric antibiotic costs differently by the pair of "
            "groups (MET-6, MET-8), so the multiclass fallback, log loss. It scores one prediction per patient (the "
            "grouping), so each patient counts once, as in the source's per-patient score, whether it has 400 spectra "
            "(2018) or 100 (2019) (MET-17)."
        ),
    )
    grouping = Grouping(
        on="isolate",
        labels="per_group",
        prediction_unit="group",
        aggregation="mean",
        context="all_rows",
        definition="""
            One group is one bacterial isolate: a patient's isolate (50, recovered from the row order: 400-row blocks in the 2018 file and 100-row blocks in the 2019 file, five patients per treatment group, as the source's `3_clinical_finetuning.ipynb` indexes them) or one of the 30 reference isolates of the library. The use case is the empiric antibiotic for a new patient (Ho et al. 2019), so whole patients are held out, as the source does: "we want to make sure that spectra from the same patient do not appear in both training and validation/test" (the notebook). The reference isolates are in every training side and never tested, as the source pre-trains on them for the eight treatment groups before it fine-tunes on patients. One prediction is one patient, identified from its own spectra, as the source identifies a patient: "We then use 10 randomly sampled spectra from each patient isolate in the test set ... The most common class out of the 10 spectral classifications is then chosen as the identification" (Results). A model may use all of the patient's spectra (`all_rows`: the lab has its 100 to 400; the source votes over 10), and the patient's prediction is the mean of its spectra's class probabilities unless a method returns its own.
        """,
    )
    splits_comment = """
        Grouped 2-fold cross-validation over the 50 patients, stratified by treatment group, 30 repeats with seed 4267: each test fold holds 25 patients, 5 of each treatment group, and every training side adds the 66,000 spectra of the reference library, which are never tested. Two folds rather than the protocol's three for 50 groups, so that a test fold holds 5 patients of each group: three folds left 3 or 4 (TP-5). The source fine-tunes with one patient per group held out at a time (five folds over the 2018 patients, 10 spectra per training patient), and tests the 2019 patients in a loop of their own, after further fine-tuning on the other 2019 patients; we pool the two years and hold out half of the patients per fold.

        Protocol (LEAK-9): a test patient is predicted from its own spectra and the training rows only: no rows of other test patients, no preprocessing fitted on test rows, and no class counts of the test fold from outside the training data (the source's five patients per group and year, with the year read from a spectrum, lower the per-patient log loss; curation_comments). A method that does is called out and not benchmarked.
    """

    special_features = (
        Spectrum(
            name="raman_spectrum",
            prefix=PREFIX,
            unit="cm-1",
            technique="raman",
            state="processed",
            description=(
                "The isolate's Raman spectrum from one spot of a map of a bacterial monolayer (45 x 45 spots for the "
                "reference isolates; the patients' map size is not stated), on the source's uneven 1,000-position grid "
                "from 381.98 to 1,792.4 cm-1, 1.20 to 1.56 cm-1 apart (`wavenumbers.npy`; the arrays run from high to "
                "low wavenumber), each spectrum background-corrected by a polynomial fit of order 5 and scaled to run "
                "from 0 to 1 (Ho et al. 2019, Methods)."
            ),
        ),
    )

    def _load_raw(self, raw_dir: Path) -> dict[str, np.ndarray]:
        data = raw_dir / "data"
        raw = {"wavenumbers": np.load(data / "wavenumbers.npy")}
        for name in (*REFERENCE_FILES, *CLINICAL_FILES):
            raw[f"X_{name}"] = np.load(data / f"X_{name}.npy")
            raw[f"y_{name}"] = np.load(data / f"y_{name}.npy")
        return raw

    def _clean(self, raw: dict[str, np.ndarray]) -> pd.DataFrame:
        # The columns are named by the source's wavenumber axis, `raman_<cm-1>`, so the build reads the axis from them.
        columns = [f"{PREFIX}{float(w)!r}" for w in raw["wavenumbers"]]
        frames = []
        # The reference library: the isolate is the label of the reference files; its treatment group is the target.
        for name in REFERENCE_FILES:
            codes = raw[f"y_{name}"].astype(int)
            frame = pd.DataFrame(raw[f"X_{name}"], columns=columns)
            frame["isolate"] = [f"reference {REFERENCE_ISOLATES[c][0]}" for c in codes]
            frame[self.target] = [TREATMENTS[REFERENCE_ISOLATES[c][1]] for c in codes]
            frames.append(frame)
        # The patients: the patient from the row order, as the source's notebook defines it (SPLIT-24).
        for name, block in CLINICAL_FILES.items():
            codes = raw[f"y_{name}"].astype(int)
            frame = pd.DataFrame(raw[f"X_{name}"], columns=columns)
            # Numbered in a seeded random order within the year, so the id does not follow the label blocks.
            number = np.random.default_rng([PATIENT_ORDER_SEED, int(name[:4])]).permutation(len(frame) // block) + 1
            frame["isolate"] = [f"patient {name[:4]}-{number[i]:02d}" for i in np.arange(len(frame)) // block]
            frame[self.target] = [TREATMENTS[c] for c in codes]
            frames.append(frame)
        df = pd.concat(frames, ignore_index=True)
        assert (df.groupby("isolate")[self.target].nunique() == 1).all()
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["isolate"])

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # Grouped 2-fold cross-validation over the 50 patients, stratified by their treatment group, 30 repeats (5
        # patients per group in each test fold); the reference library is in every training side and never tested.
        is_patient = df["isolate"].astype(str).str.startswith("patient ").to_numpy()
        patients = np.flatnonzero(is_patient)
        reference = np.flatnonzero(~is_patient).tolist()
        clinical = df.iloc[patients].reset_index(drop=True)
        folds = protocol.grouped_splits(
            clinical,
            n_repeats=30,
            n_folds=2,
            group_on="isolate",
            group_labels="per_group",
            stratify_on=self.target,
            random_state=self.SPLIT_RANDOM_STATE,
        )
        splits = {
            repeat: {
                fold: (sorted(patients[train].tolist() + reference), patients[test].tolist())
                for fold, (train, test) in by_fold.items()
            }
            for repeat, by_fold in folds.items()
        }
        return SplitPlan(splits=splits)

    def _decisions(self, raw: dict[str, np.ndarray], df: pd.DataFrame) -> list[Decision]:
        isolate = df["isolate"].astype(str)
        kind = np.where(
            isolate.str.startswith("patient 2018"),
            "patients 2018",
            np.where(isolate.str.startswith("patient 2019"), "patients 2019", "reference isolates"),
        )
        by_group = (
            pd.DataFrame({"group": df[self.target].astype(str), "kind": kind, "isolate": isolate})
            .groupby(["group", "kind"])["isolate"]
            .nunique()
            .unstack(fill_value=0)
        )

        # Nearest block centroid within each treatment group: the patients' blocks against blocks shifted by half a
        # patient, which mix two patients.
        def centroid_accuracy(X: np.ndarray, block: np.ndarray) -> float:
            labels = np.unique(block)
            centroids = np.stack([X[block == b].mean(axis=0) for b in labels])
            distance = ((X[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
            return float((labels[distance.argmin(axis=1)] == block).mean())

        rows = []
        for name, size in CLINICAL_FILES.items():
            X, codes = raw[f"X_{name}"], raw[f"y_{name}"].astype(int)
            position = np.arange(len(codes))
            for code in np.unique(codes):
                rows_of = position[codes == code]
                rows.append(
                    {
                        "file": name,
                        "treatment": TREATMENTS[code],
                        "patient blocks": round(centroid_accuracy(X[rows_of], rows_of // size), 3),
                        "blocks shifted by half a patient": round(
                            centroid_accuracy(X[rows_of], (rows_of + size // 2) // size), 3
                        ),
                    }
                )
        return [
            Decision(
                title="Isolates per treatment group: the reference library trains, the patients are tested",
                why=(
                    "The treatment group of a new patient's isolate is the decision (USE-5); the 30 reference "
                    "isolates carry the group `config.py` gives them and sit in every training side, as the source "
                    "pre-trains on them, and three groups occur only there."
                ),
                evidence=by_group,
            ),
            Decision(
                title="The patient from the row order",
                why=(
                    "The clinical files carry no patient column; the source's notebook indexes patients as blocks of "
                    "400 (2018) and 100 (2019) rows. Each spectrum assigned to the nearest block centroid within its "
                    "treatment group finds its own block far more often than for blocks shifted by half a patient, "
                    "so the boundaries are real (SPLIT-24)."
                ),
                evidence=pd.DataFrame(rows),
            ),
        ]

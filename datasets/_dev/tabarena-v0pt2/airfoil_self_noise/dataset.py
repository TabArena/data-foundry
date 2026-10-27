"""Curated dataset definition for `airfoil_self_noise` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, Metric, TaskSummary


class AirfoilSelfNoise(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How loud is an airfoil's own noise in a given frequency band, on the source's speed-scaled decibel "
            "level, for an airfoil size at an angle of attack that was not measured?"
        ),
        use_case=(
            "An aerodynamics engineer estimates the noise spectrum of an airfoil at a size and angle of attack not "
            "yet tested, at any wind speed, before, or instead of, mounting it in a wind tunnel."
        ),
        row=(
            "One frequency band of one wind-tunnel run, that is one airfoil size at one angle and one wind speed (106"
            " runs of 8 to 19 bands, the tripped-boundary-layer set of NASA 1989; bands with tunnel noise removed)."
        ),
        predicted=(
            "The band's sound level as the source scales it, in decibels: the measured level minus a term of the wind"
            " speed and the boundary-layer thickness, so the measured level follows exactly from the features."
        ),
        known=(
            "The band's frequency and the run's settings (chord length, angle of attack, wind speed) plus a "
            "boundary-layer thickness computed from them."
        ),
        split=(
            "Whole setups are held out, an airfoil size at one angle with all its wind speeds, so the test data "
            "stands for a size and angle never measured together; each size, and most angles, are in training with "
            "other partners."
        ),
        changes=(
            "We added the setup (size and angle) as a group column and split by it, and treat the angle as a number;"
            " with random rows, or whole runs, models filled in spectra of setups they had seen at another speed."
        ),
        fit="direct",
        fit_reason=(
            "The features are the settings an engineer chooses, and a held-out setup is an airfoil at an angle not "
            "yet tested. The task is narrow (one airfoil shape, tripped, one wind tunnel and microphone) but real."
        ),
    )

    # Dataset
    unique_name = "airfoil_self_noise"
    year = "1989"
    domain = "physics & astronomy"
    source = "Other"  # NASA RP-1218 plots every measured value (Figs. 11-43); UCI 291 (2014) was digitised from them
    source_url = "https://ntrs.nasa.gov/citations/19890016302"
    license = "CC BY 4.0"  # stated on UCI 291, the copy we download
    download_description = """
        We download UCI's copy (dataset 291, donated 2014), whose values were digitised from the figures of NASA RP-1218.
        mkdir -p local-data-warehouse/airfoil_self_noise/ && wget -P local-data-warehouse/airfoil_self_noise/ https://archive.ics.uci.edu/static/public/291/airfoil+self+noise.zip && unzip local-data-warehouse/airfoil_self_noise/airfoil+self+noise.zip -d local-data-warehouse/airfoil_self_noise/
    """
    bibtex = """
        @techreport{brooks1989airfoil,
          title={Airfoil self-noise and prediction},
          author={Brooks, Thomas F and Pope, D Stuart and Marcolini, Michael A},
          institution={NASA Langley Research Center},
          type={NASA Reference Publication},
          number={1218 (L-16528)},
          year={1989}
        }
    """
    curation_comments = """
        - The 1,503 rows are 106 wind-tunnel runs of NASA RP-1218 (Brooks, Pope and Marcolini 1989): one NACA 0012 section (6 chord lengths) at one angle of attack and one free-stream velocity (4), each a one-third-octave spectrum of 8 to 19 bands. They are the report's tripped set only (Sec. 4.3: "Figures 11 to 43 are for airfoils where the boundary layers have been tripped"); the untripped Figs. 44-74 are not in the data. The angle is the effective angle after the open-jet correction (Sec. 2.4). The spectra are truncated at both ends where extraneous noise changed them by 2 dB or more, hence 8 to 19 bands. The suction-side displacement thickness is the report's formula for a tripped boundary layer, computed from chord, velocity and angle, so it is constant within a run.
        - Year and source are the report's (PROV-9: a figure that shows every measured value holds the rows, with the columns the publication's formulas compute from them; Lennart, 2026-10-20). Its Figs. 11-43 plot the measured levels; the target and the thickness are its formulas of them. The values were read off its figures: "The input-target data set was created from a noise database taken by digitising the appropriate figures from [the report]" (Lau, Lopez and Onate, CIMNE preprint PI-335, Sec. 4.1); UCI released the file in 2014. Their 0.01 dB grid is the digitiser's, and UCI's type "Binary" for the angle is an error of that copy.
        - The target is the report's scaled level, not the measured one: "Scaled SPL1/3 = SPL1/3 - 10 log(M^5 delta* L / r_e^2)" (eq. 19, Sec. 5.1.1, p. 51), with delta* the suction-side thickness, the span L = 0.4572 m, the microphone distance r_e = 1.22 m and the Mach number M = velocity / 340.46 m/s. Adding the term back gives the measured level (26.8 to 86.4 dB), and with these constants all 1,503 rows land on the 0.01 dB grid. The term is a function of two features, so a band's error in dB is the same in both forms. Kept as the report's eq. 19 level (Lennart, 2026-10-20): it is the engineer's own normalisation, and re-targeting would make models learn the M^5 delta* scaling.
        - Grouped by setup since 2026-10-20 (by run from 2026-10-06, IID before). A setup is one chord length at one angle, with its runs at all tested speeds: one figure of the report ("Each figure contains spectra for a model at a specific angle of attack for various tunnel speeds", Sec. 4.3); 33 setups, 20 run at 4 speeds and 13 at 2. Under the run split, 91.5% of the test runs had their setup in training at another speed, and the scaling lines those spectra up, so the test mostly filled in a speed; a new angle or size is the query another tunnel run cannot answer cheaply, as a new mix is for concrete_compressive_strength (grouped by mix, 2026-10-14). A random 3-fold split puts two thirds of a run's other bands in train.
        - Not grouped by chord length alone: 6 chords leave 2 held out per fold, too few groups for a stable score (R^2 SD 0.08 to 0.10 across splits), and the use case stays inside the tested range of sizes.
        - `attack-angle` is numeric since 2026-10-20 (categorical in v1, without a reason; CLEAN-14): an angle in degrees, and under the setup split 72% of the test runs (58% to 94% per split) carry an angle value absent from training. R^2, 5 x 3 folds, untuned (review panel, 2026-10-19), random / run / setup, angle numeric: extra trees 0.943 / 0.855 / 0.774, random forest 0.922 / 0.835 / 0.734, LightGBM 0.921 / 0.832 / 0.736; LightGBM with the categorical angle 0.923 / 0.806 / 0.646. On the shipped splits (10 x 3, 11 setups per test fold), untuned: LightGBM 0.727, random forest 0.717, linear 0.445; no task-probe flags (2026-10-20).
    """

    # Task
    target = "scaled-sound-pressure"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "The NASA report builds semi-empirical prediction methods and compares spectra visually; neither "
            "it nor the UCI page defines an evaluation metric"
        ),
    )
    grouping = Grouping(
        on="setup",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a setup: one NACA 0012 section (chord length) at one angle of attack, with its wind-tunnel runs at every tested speed (2 or 4); its rows are the bands of those runs' one-third-octave spectra (33 setups, one figure each of Brooks et al. 1989, Figs. 11-43). The source built its data to predict: "An overall prediction method has been developed for the self-generated noise of an airfoil blade encountering smooth flow" (Summary). The use case is the spectrum of an airfoil size at an angle not yet tested; once a setup is mounted, another speed is a short run, so the test setups are new to the model with all their speeds. Each row is one prediction, made from its band's frequency and the run's settings.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the setup (chord length and angle of attack): all runs of an airfoil at one angle, at every speed, stay on one side, so a model predicts the spectra of a size and angle it has not seen together. Each chord length is in training with other angles, and 72% of the test runs carry an angle value absent from training.
    """
    accepted_check_warnings = {
        "groups_test_groups_few": "The 33 setups are all the report has (11 per test fold), and holding out a whole "
        "setup is the use case. Each fold still scores about 500 bands one by one, and the signal across setups is "
        "real: on unseen setups ridge, random forest, LightGBM and kNN reach R^2 0.438, 0.717, 0.710 and 0.562 "
        "(group_probes.py, 2026-10-20), and LightGBM beats the dummy on 30 of 30 splits (task_probes.py).",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "airfoil_self_noise.dat", header=None, sep=r"\s+")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df.columns = [
            "frequency",
            "attack-angle",
            "chord-length",
            "free-stream-velocity",
            "suction-side-displacement-thickness",
            self.target,
        ]
        # a setup is one airfoil at one angle, measured at several speeds: one figure of the report
        df["setup"] = df.groupby(["chord-length", "attack-angle"], sort=False).ngroup().map("setup_{:02d}".format)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=("setup",),
        )

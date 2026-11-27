"""Curated dataset definition for `raman_fuel_benchtop` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    Source,
    Spectrum,
    TaskSummary,
    TimeBasis,
    drop_columns,
)

BENCHTOP_PREFIX = "benchtop_"
HANDHELD_PREFIX = "handheld_"

# The eleven laboratory properties the release carries beside the research octane number. None is known when a
# spectrum is taken, so none is an input; the motor octane number is measured on 22 of the 179 samples and is no
# second target (CLEAN-18).
OTHER_PROPERTIES = (
    "Motor Octane Number",
    "Ethanol Content (%)",
    "Ethyl Tert-Butyl Ether (ETBE)",
    "Methyl Tert-Butyl Ether (MTBE)",
    "Density at 15°C",
    "Water Content",
    "Oxygenates Content",
    "Oxygen Content",
    "Olefins Content",
    "Aromatics Content",
    "Benzene Content",
)


class RamanFuelBenchtop(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is a gasoline's research octane number, from its Raman spectrum?",
        use_case=(
            "A fuel inspector or a laboratory rates a gasoline near the pump with a spectrometer instead of "
            "sending it to a CFR engine. The engine test takes hours on a dedicated single-cylinder rig; a "
            "spectrum takes seconds, so the decision it informs is which samples are worth the engine."
        ),
        row="One commercial gasoline sample, measured on both spectrometers.",
        predicted=(
            "Its research octane number, measured on a CFR engine by ASTM D2699. The engine number is the "
            "reference the spectrum stands in for, so it exists for the sample before the prediction is scored."
        ),
        known="The sample's two Raman spectra, one from a benchtop and one from a handheld instrument. Nothing else.",
        known_at_scoring="",
        split="A gasoline the instrument has not measured before.",
        changes=(
            "The eleven other laboratory properties are dropped: none is known when the spectrum is taken. The "
            "two measurements of one sample are held out together."
        ),
        fit="direct",
        fit_reason=(
            "The source's own question, on the source's own samples: a Raman spectrum in, the engine octane "
            "number out. The gap to the field is the sample set, 130 refinery samples spanning RON 95 to 102.2 "
            "with the rest from filling stations, which is narrower than the fuels an inspector meets."
        ),
    )

    # Dataset
    unique_name = "raman_fuel_benchtop"
    domain = "chemistry & material science"
    sources = (
        Source(
            role="publication",
            platform="HuggingFace",
            url="https://huggingface.co/datasets/chlange/FuelRamanSpectraBenchtop",
            license="CC BY 4.0",
            year="2025",
            name="the benchtop spectra",
            bibtex=r"""
                @article{voigt2019fuel,
                  title={Toward fast and accurate {RON} determination of gasoline by on-site {NMR} and {Raman}
                         spectroscopy},
                  author={Voigt, Martin and Legner, Robin and Haefner, Simon and Friesen, Armin and Wirtz, Alexander
                          and Jaeger, Martin},
                  journal={Fuel},
                  volume={236},
                  pages={829--835},
                  year={2019},
                  doi={10.1016/j.fuel.2018.09.006}
                }
                @article{legner2019fuel,
                  title={Multidimensional Analytical Characterization of Gasoline Fuels by Data Fusion},
                  author={Legner, Robin and Voigt, Martin and Wirtz, Alexander and Jaeger, Martin},
                  journal={Energy \& Fuels},
                  volume={34},
                  number={1},
                  year={2019},
                  doi={10.1021/acs.energyfuels.9b02944}
                }
            """,
        ),
        Source(
            role="part",
            platform="HuggingFace",
            url="https://huggingface.co/datasets/HTW-KI-Werkstatt/FuelRamanSpectraHandheld",
            license="CC BY 4.0",
            year="2025",
            name="the handheld spectra of the same samples",
            files=["handheld/*.parquet"],
        ),
    )
    data_tags = ()
    split_leaf = "L-EXP.item"
    time_basis = TimeBasis(
        "Timeless",
        """
        a closed set of commercial gasolines measured once by one laboratory: the octane number is a property of
        the fuel, not of when it was measured, and no row carries a date. The model meets a new gasoline of the
        kind the data holds, and one sample was measured twice, so whole samples are held out with both of their
        measurements. The split cannot test another spectrometer, another laboratory or a fuel outside the
        source's range.
        """,
    )
    download_description = """
        Both releases are on Hugging Face as three parquet files each, by the authors of the two studies.

        mkdir -p local-data-warehouse/raman_fuel_benchtop/benchtop local-data-warehouse/raman_fuel_benchtop/handheld
        cd local-data-warehouse/raman_fuel_benchtop
        for f in train val test; do
          curl -L -o benchtop/$f.parquet \
            "https://huggingface.co/datasets/chlange/FuelRamanSpectraBenchtop/resolve/main/$f.parquet"
          curl -L -o handheld/$f.parquet \
            "https://huggingface.co/datasets/HTW-KI-Werkstatt/FuelRamanSpectraHandheld/resolve/main/$f.parquet"
        done
    """
    curation_comments = """
        We start with the six parquet files of the two Hugging Face releases: 179 commercial gasolines measured on
        a benchtop FT-Raman spectrometer (961 bands, 98 to 3,801 cm-1, 1,064 nm) and on a handheld instrument
        (1,901 bands, 400 to 2,300 cm-1, 785 nm), each with twelve laboratory properties. Every file is read.

        - Prediction point: a gasoline sample has been measured on the spectrometer and its octane number is not
          known. Only the two spectra are known. The answer is one number, the research octane number the CFR
          engine would give.
        - The two releases are one dataset (PROV-6). They hold the same 179 samples in the same order: all twelve
          property columns agree value for value across the two files, in every one of the three splits, so the
          row position is the sample and the two frames are joined on it. The releases ship the samples in the
          authors' train, validation and test folders; those folders are not a split of ours (SPLIT-19 is not
          applied: the source states no held-out design for them, and 179 samples cannot carry a fixed split and a
          cross-validation both).
        - One sample was measured twice (SPLIT-24). Rows 42 and 96 of the concatenated frame agree on all twelve
          properties, including the research octane number 102.2, the motor octane number 89.2, the density 752.9
          and the benzene content 0.12. Their benchtop spectra differ by at most 0.125 across the 961 bands, where
          two gasolines drawn at random differ by 5.94 (the median over 200 pairs), about fifty times as much, so
          they are one fuel measured twice and not two fuels that happen to match on twelve properties. They stay
          as two rows, as the source published them, and `sample` holds them together so no split puts one in
          training and the other in test (LEAK-19 drops exact copies; these are not exact).
        - The eleven other properties are dropped. None of them is known when the spectrum is taken: each is a
          laboratory measurement of the same sample, so each would stand in for the engine test the task replaces.
          The motor octane number is measured on 22 of the 179 samples and the other ten on 164, too few to ship
          as a second target (CLEAN-18); the research octane number is measured on all 179.
        - The spectra ship as the sources publish them and are declared as two spectra (`special_features`,
          CLEAN-26), state `raw`: neither card names a baseline correction, a normalisation or a derivative. The
          bands are renamed from the bare wavenumber to `benchtop_<cm-1>` and `handheld_<cm-1>` so the build reads
          each axis from the names; no value changes, and the two axes stay separate because the instruments
          differ in excitation (1,064 against 785 nm), range and resolution.
        - The sample column is a running number over the joined frame, with the repeated sample given one number;
          it is the grouping key and never a model input.
        - One handheld band is dropped: `702.0` reads exactly 100.0 on every one of the 179 samples, where its
          neighbours from 700 to 705 cm-1 average 100.1 to 101.4 and the axis as a whole runs from 33.7 to 35,322.
          A constant bin carries nothing and may be a fill; dropping it leaves the other 1,900 bands whole
          (CLEAN-26). It is the only constant band in either spectrum.
        - The group probe finds no structure to the grouping, which is expected and not a reason to drop it: 178
          of the 179 rows are a group of their own, so there is nothing for the probe to see. The one group of two
          is what the key exists for.
        - 179 samples is a tiny table (TP-9), and the octane numbers span 89.4 to 104.8 with a mean of 97.8.
        - A companion task on the same rows, named and not shipped: the ethanol content, measured on 164 of the
          179 samples. It is the property a field instrument is asked for after the octane number, and the benchmark
          this dataset comes from scores all twelve properties as twelve tasks. A later round can take it; here it
          is a laboratory measurement of the sample, so it is neither a second target nor an input (CLEAN-18).
    """

    # Task
    target = "research_octane_number"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "Voigt et al. 2019 report two criteria for the same models and name neither as the one that decides: "
            '"The goodness of the method is expressed both in terms of computational residual mean squared errors '
            'and the common experimental reproducibility and repeatability limits", with "40-50% of the samples '
            'are predicted within 0.2 and 80-90% with 0.7 RON" (abstract). The share within the ASTM D2699 '
            "limits would be a metric of our own with a threshold the source does not fix as its criterion "
            "(MET-6, MET-7), and Legner et al. 2019 scores a data-fusion model, not this one. The Hugging Face "
            "cards name no metric. So the regression fallback, which is also the paper's own computational "
            "criterion (MET-5)."
        )
    )
    grouping = Grouping(
        on="sample",
        labels="per_group",
        prediction_unit="row",
        context="none",
        definition="""
            One group is one gasoline sample. 178 of the 179 rows are a group of their own; the two measurements
            of the sample at research octane number 102.2 (rows 42 and 96) form the one group of two, so a split
            cannot train on one of them and test the other. Each spectrum is predicted on its own, from itself and
            the training rows, as a laboratory rates one sample at a time.
        """,
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # Only read here (cached across edits of `_clean`). The two releases hold the same samples in the same
        # order, so each instrument's three files are concatenated in the authors' order and the two frames are
        # joined on the row position; `_clean` checks that the twelve property columns agree before relying on it.
        frames = {}
        for instrument in ("benchtop", "handheld"):
            parts = [pd.read_parquet(raw_dir / instrument / f"{part}.parquet") for part in ("train", "val", "test")]
            frames[instrument] = pd.concat(parts, ignore_index=True)
        benchtop, handheld = frames["benchtop"], frames["handheld"]
        properties = [column for column in benchtop.columns if any(character.isalpha() for character in column)]
        bands = {
            instrument: [column for column in frame.columns if column not in properties]
            for instrument, frame in frames.items()
        }
        # The join rests on the row position, so check it here: every property column must agree value for value
        # between the two releases (PROV-13).
        mismatched = [column for column in properties if not benchtop[column].equals(handheld[column])]
        if mismatched:
            raise ValueError(f"The two releases disagree on {mismatched}: the row position is not the sample.")

        return pd.concat(
            [
                benchtop[properties],
                benchtop[bands["benchtop"]].add_prefix(BENCHTOP_PREFIX),
                handheld[bands["handheld"]].add_prefix(HANDHELD_PREFIX),
            ],
            axis=1,
        )

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        properties = ["Research Octane Number", *OTHER_PROPERTIES]

        # The repeated sample: rows that agree on every one of the twelve properties are one gasoline measured
        # twice, and share a group (SPLIT-24, curation notes). Everything else is its own group.
        df["sample"] = df.groupby(properties, dropna=False).ngroup()

        # The research octane number is the only property measured on all 179 samples; the other eleven are
        # laboratory measurements of the same sample and are no model inputs.
        df = df.rename(columns={"Research Octane Number": "research_octane_number"})
        df = drop_columns(df, list(OTHER_PROPERTIES))

        # One handheld band reads exactly 100.0 on all 179 samples while its neighbours average 100.1 to 101.4
        # and the axis as a whole runs from 33.7 to 35,322: a constant that carries nothing. The band is dropped
        # for every row and the recorded axis keeps the positions that remain (CLEAN-26).
        df = drop_columns(df, [f"{HANDHELD_PREFIX}702.0"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The spectra are declared in `special_features` and stay out of the dtypes (CLEAN-26); the target and the
        # grouping key are numeric.
        return FeatureTypes(categorical=[], string=[], datetime={})

    special_features = (
        Spectrum(
            name="benchtop_spectrum",
            prefix=BENCHTOP_PREFIX,
            unit="cm-1",
            technique="raman",
            state="raw",
            description=(
                "The sample's Raman spectrum on the benchtop FT-Raman spectrometer at 1,064 nm, 961 bands from "
                "98 to 3,801 cm-1, as the release publishes it."
            ),
        ),
        Spectrum(
            name="handheld_spectrum",
            prefix=HANDHELD_PREFIX,
            unit="cm-1",
            technique="raman",
            state="raw",
            description=(
                "The same sample's Raman spectrum on the handheld instrument at 785 nm, 1,901 bands from 400 to "
                "2,300 cm-1, as the release publishes it."
            ),
        ),
    )

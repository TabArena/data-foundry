"""Curated dataset definition for `raman_ecoli_fermentation` (data-foundry v2). Evidence: README.md."""

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

PREFIX = "raman_"

# The source ships the 24 cultivations as three folders of eight, drawn at random (Lange et al. 2025, Sec. 2.6.4).
# The folder is the only key to the cultivation that ships, so it is the group.
EXPERIMENT_GROUPS = ("train", "val", "test")


class RamanEcoliFermentation(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How much glucose is in a fed-batch E. coli culture, from an at-line Raman spectrum of its supernatant?",
        use_case=(
            "A high-throughput bioprocess facility reads each at-line sample's glucose instead of waiting for the "
            "enzymatic analyser, and writes the reading back to the database, where the feeding strategy uses it: "
            "'the predictions are written to the database to allow other models to use them for adjusting feeding "
            "strategies' (Lange et al. 2025, Sec. 2.3)."
        ),
        row="One Raman spectrum of the cell-free supernatant of one at-line sample, measured for ten seconds.",
        predicted=(
            "The sample's glucose concentration in g/L, as the Cedex Bio HT analyser measures it on the same "
            "sample. The analyser result arrives after the spectrum, which is why the spectrum is worth reading."
        ),
        known="The spectrum. Nothing else: no cultivation id, no time, no setup.",
        known_at_scoring="",
        split="A cultivation the model has not seen, run in the same facility on the same platform.",
        changes=(
            "Acetate, the second reference the analyser gives, is dropped: one target ships. The six samples the "
            "release leaves without a glucose value are dropped with it."
        ),
        fit="direct",
        fit_reason=(
            "The source's own question on the source's own samples: an at-line spectrum in, the analyser's "
            "glucose out, for the feeding decision the paper names. The gap is that a cultivation is held out "
            "only as one of three random groups of eight, because no cultivation id ships."
        ),
    )

    # Dataset
    unique_name = "raman_ecoli_fermentation"
    domain = "biology & life sciences"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.1002/bit.70006",
            license="CC BY 4.0",
            year="2025",
            bibtex=r"""
                @article{lange2025raman,
                  title={A Setup for Automatic {Raman} Measurements in High-Throughput Experimentation},
                  author={Lange, Christoph and Seidel, Simon and Altmann, Jonas and Stors, Lucas and Kemmer, Annina
                          and Cai, Linda and Born, Stefan and Neubauer, Peter and Cruz Bournazou, Mariano Nicolas},
                  journal={Biotechnology and Bioengineering},
                  volume={122},
                  number={10},
                  pages={2751--2769},
                  year={2025},
                  doi={10.1002/bit.70006}
                }
            """,
        ),
        Source(
            role="copy",
            platform="HuggingFace",
            url="https://huggingface.co/datasets/chlange/RamanSpectraEcoliFermentation",
            license="CC BY 4.0",
            year="2025",
            name="the fermentation spectra on the measuring instrument's own grid, which this definition reads",
        ),
    )
    data_tags = ()
    split_leaf = "L-EXP.item"
    time_basis = TimeBasis(
        "Timeless",
        """
        the glucose in a sample is a property of that sample, not of when it was drawn, and the task reads the
        current concentration from the current spectrum rather than forecasting one. The samples are drawn along
        the cultivations, but no timestamp, run id or order ships, and the model meets a new cultivation, so whole
        experiment groups are held out with all their samples and both replicate spectra of each. The split cannot
        test a later campaign, another facility or another instrument.
        """,
    )
    download_description = """
        The spectra are on Hugging Face from the authors, as three CSV files named after the source's three
        experiment groups.

        mkdir -p local-data-warehouse/raman_ecoli_fermentation/hf
        cd local-data-warehouse/raman_ecoli_fermentation/hf
        for f in train val test; do
          curl -L -o $f.csv \
            "https://huggingface.co/datasets/chlange/RamanSpectraEcoliFermentation/resolve/main/$f.csv"
        done
    """
    curation_comments = """
        We start with the three CSV files of the Hugging Face release: 379 at-line Raman spectra of cell-free
        supernatant from 24 E. coli fed-batch cultivations, 1,870 bands from 390.63 to 3,384.7 cm-1, with the
        Cedex Bio HT analyser's glucose and acetate. Every file is read.

        - Prediction point: an at-line sample has been drawn from a cultivation and measured on the Raman probe;
          the analyser has not reported yet. Only the spectrum is known. The answer is the glucose concentration
          in g/L.
        - Which copy is the data (PROV-8). The paper's repository (git.tu-berlin.de, `raman-kiwi-experiments`)
          holds the same validation and test samples as this release, by their reference values, but its training
          file has 2,400 rows against this release's 139, and its axis is 838 bands from 300.78 to 1,941.12 cm-1
          against 1,870 from 390.63 to 3,384.7. The difference of 2,261 rows is exactly the "2,261 extra spectra
          from eight spectrometers" the paper adds to its training set, and its narrower, coarser axis is the grid
          those eight instruments share. The repository file is therefore the paper's model-training matrix, not
          the fermentation measurement: it is harmonised across instruments and padded with a second dataset,
          which our records carry separately. This definition reads the Hugging Face release, the fermentation
          samples on the measuring instrument's own grid, and declares the repository as a copy.
        - The replicate pair. Two ten-second spectra were taken of each sample, and they share the sample's
          reference values: of the 373 rows with both references, 186 reference pairs occur exactly twice and one
          occurs once, so the reference pair identifies the sample (SPLIT-24). The replicates are not separated by
          the split, because the experiment group that holds them is coarser than the sample.
        - The split is the source's own (SPLIT-19). The 24 cultivations were "divided into three groups at random"
          of eight (Sec. 2.6.4), and the three files are those groups. No cultivation id ships in either copy, so
          the group is the file a sample comes from: three groups, one held out per fold. Three is few, and it is
          the finest cut the release allows; cultivation ids from the authors would give 24 (SPLIT-25).
        - One target ships (CLEAN-18). Glucose is the quantity the feeding strategy acts on and is measured on
          373 of the 379 samples; acetate is dropped. The six samples without a glucose value (two in the first
          group, four in the second) are dropped with their rows.
        - The spectrum ships as the release publishes it and is declared as one (`special_features`, CLEAN-26),
          state `raw`: the card names no baseline correction, normalisation or derivative. The bands are renamed
          from the bare wavenumber to `raman_<cm-1>` so the build reads the axis from the names; no value changes.
        - The experiment group is the grouping key and never a model input. It carries no information about the
          sample beyond which eight cultivations it came from.
        - Half the target is a floor, and it is censored, not zero-inflated. 192 of the 373 glucose values are
          exactly 0.0 (51.5%), spread evenly over the three groups (49.1%, 50.8%, 54.0%), and the next smallest
          values are 0.0279, 0.0660 and 0.0742 g/L: a gap, not a continuum. The analyser reports a concentration
          below its limit of quantification as 0, and a glucose-limited fed-batch spends half its samples there
          by design. The zeros are a real state of the culture, not missing data, so the rows stay; what the
          curator decides is whether the task keeps a target that is at its floor half the time (the review's
          issue on the target). Acetate, the other reference, is at 0 on 2 of the 373 rows and runs to 1.592 g/L.
        - 373 rows over 187 samples in 24 cultivations is a tiny table (TP-9); glucose runs from 0 to 4.14 g/L.
    """

    # Task
    target = "glucose_g_per_l"
    problem_type = "regression"
    metric = Metric.source(
        "mae",
        original="MAE",
        reference="https://doi.org/10.1002/bit.70006",
        inputs=None,
    )
    grouping = Grouping(
        on="experiment_group",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is one of the source's three randomly drawn sets of eight cultivations, which is the only
            key to the cultivation the release ships. Holding a group out tests a cultivation the model has not
            seen, and keeps both replicate spectra of every one of its samples out with it. Each spectrum is
            predicted on its own, as the facility reads one at-line sample at a time.
        """,
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # Only read here (cached across edits of `_clean`). The file a sample comes from is the source's
        # experiment group and the only cultivation key that ships, so it is kept as a column.
        frames = []
        for group in EXPERIMENT_GROUPS:
            frame = pd.read_csv(raw_dir / "hf" / f"{group}.csv")
            frame.insert(0, "experiment_group", group)
            frames.append(frame)
        return pd.concat(frames, ignore_index=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()

        # The six samples the analyser left without a glucose value cannot be scored (curation notes).
        df = df[df["Glucose"].notna()].reset_index(drop=True)

        # One target ships: glucose, the quantity the feeding strategy acts on (CLEAN-18).
        df = df.rename(columns={"Glucose": "glucose_g_per_l"})
        df = drop_columns(df, ["Acetate"])

        # The bands are named by their wavenumber alone; the prefix lets the build read the axis from the names.
        bands = {
            column: f"{PREFIX}{column}"
            for column in df.columns
            if column not in ("experiment_group", "glucose_g_per_l")
        }
        df = df.rename(columns=bands)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The spectrum is declared in `special_features` and stays out of the dtypes (CLEAN-26).
        return FeatureTypes(categorical=["experiment_group"], string=[], datetime={})

    special_features = (
        Spectrum(
            name="raman_spectrum",
            prefix=PREFIX,
            unit="cm-1",
            technique="raman",
            state="raw",
            description=(
                "The at-line Raman spectrum of the sample's cell-free supernatant, ten seconds on the facility's "
                "probe, 1,870 bands from 390.63 to 3,384.7 cm-1, as the release publishes it."
            ),
        ),
    )

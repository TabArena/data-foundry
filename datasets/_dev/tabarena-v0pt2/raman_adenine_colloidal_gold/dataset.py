"""Curated dataset definition for `raman_adenine_colloidal_gold` (data-foundry v2). Evidence: README.md."""

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

# The source's own columns. `method` is `substrate`@`laser` and copies the pair; `sample` names the centrally
# prepared solution, which has the same concentration in every laboratory, so it would hand over the target;
# `type` separates the blanks (always 0) from the calibration and test solutions. None of the three is an input.
COPIED_OR_LEAKING = ("method", "sample", "type")


class RamanAdenineColloidalGold(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "How much adenine is in a solution, from its surface-enhanced Raman spectrum measured in a "
            "laboratory whose spectra the model has never seen?"
        ),
        use_case=(
            "A laboratory that wants to use surface-enhanced Raman spectroscopy quantitatively asks whether a "
            "calibration built elsewhere survives its own bench. The European interlaboratory study this data "
            "comes from was run to answer that: 'to define a methodology to assess the reproducibility and "
            "trueness of a quantitative SERS method and to compare different methods'. The decision is whether "
            "to trust a transferred calibration or to build one in house."
        ),
        row="One spectrum of one prepared adenine solution, measured in one laboratory on one substrate batch.",
        predicted="The adenine concentration of the solution, in the units the study prepared it to.",
        known=(
            "The spectrum, and what the measuring laboratory knows about its own bench: the substrate, the laser "
            "wavelength and which of the three substrate batches it used."
        ),
        known_at_scoring="",
        split="A laboratory that did not take part in building the model.",
        changes=(
            "All four substrate cuts are read as one dataset, over the source's own table rather than the "
            "benchmark's per-substrate files. The solution's identity, the blank/calibration/test label and the "
            "method string are dropped: each would hand over the concentration or copy another column."
        ),
        fit="approximate",
        fit_reason=(
            "Adenine in buffer is a model analyte, so nobody acts on the number itself; what is real is the "
            "transfer question the study was built to ask, and the split puts it to the test by holding out whole "
            "laboratories. The study calibrated each laboratory on its own samples, where this task asks a model "
            "to reach a laboratory it has not seen."
        ),
    )

    # Dataset
    unique_name = "raman_adenine_colloidal_gold"
    domain = "chemistry & material science"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.5281/zenodo.3572359",
            license="CC BY 4.0",
            year="2019",
            bibtex=r"""
                @article{fornasaro2020sers,
                  title={Surface Enhanced {Raman} Spectroscopy for Quantitative Analysis: Results of a Large-Scale
                         European Multi-Instrument Interlaboratory Study},
                  author={Fornasaro, Stefano and Alsamad, Fatima and Baia, Monica and others},
                  journal={Analytical Chemistry},
                  year={2020},
                  doi={10.1021/acs.analchem.9b05658}
                }
            """,
        ),
    )
    data_tags = ()
    split_leaf = "L-PLACE.groups"
    time_basis = TimeBasis(
        "UnseenGroup",
        """
        the use case is a laboratory that did not take part in building the model, which is a group the data does
        not contain, so whole laboratories are held out with all their spectra, batches and replicates. The
        concentration of a prepared solution does not change with time and no row carries a date; the three
        substrate batches are a bench property, not a calendar. The split cannot test a substrate or a laser the
        study did not cover.
        """,
    )
    download_description = """
        The study's own table is on Zenodo, "isSupplementTo" the paper, as one CSV of every spectrum with its
        laboratory, substrate, laser, solution, batch and replicate.

        mkdir -p local-data-warehouse/raman_adenine_colloidal_gold/zenodo
        cd local-data-warehouse/raman_adenine_colloidal_gold/zenodo
        curl -L -o ILSdata.csv "https://zenodo.org/api/records/3572359/files/ILSdata.csv/content"
    """
    curation_comments = """
        We start with `ILSdata.csv` from Zenodo 10.5281/zenodo.3572359: all 3,516 spectra of the European
        interlaboratory SERS study, 534 bands from 400 to 1,999 cm-1, with the laboratory, substrate, laser,
        solution, type, concentration, batch and replicate of each.

        - Prediction point: a laboratory has measured a prepared adenine solution on its own bench and does not
          know the concentration. Known are the spectrum and the laboratory's own settings. The answer is the
          concentration.
        - Which copy is the data (PROV-8). The benchmark publishes this study as four files, one per substrate
          (225, 630, 810 and 1,851 spectra, 3,516 together), and each carries only the concentration: the
          laboratory, the batch and the solution are gone. The task the study asks cannot be built from them. The
          source's own table carries all of it, so the definition reads Zenodo and the four files are not used.
        - The record's name is historical. It was screened as the smallest of the four substrate cuts, and the
          record itself says the other three are aliases of it; this definition is the one dataset over all four
          that the record proposes. The name no longer describes the data and a rename is an issue for the
          curator.
        - The split holds out whole laboratories (15 of them, SPLIT-1). That is the study's question, and the
          source's own design is the opposite: each laboratory fitted its own linear calibration on its own
          calibration solutions and predicted its own test solutions, which measures a bench against itself and
          not the transfer. The source's design is therefore not shipped (SPLIT-19 weighed and not applied).
        - Three columns are dropped because each would hand over the answer or copy another column. `sample` names
          the centrally prepared solution (C0 to C9, X1 to X5), and a solution has the same concentration in every
          laboratory, so it is a lookup table for the target. `type` separates blanks, which are always 0, from
          calibration and test solutions. `method` is the substrate and the laser joined with an `@`.
        - What stays as an input beside the spectrum: the substrate (cAg, cAu, sAg, sAu), the laser (532 or 785
          nm) and the substrate batch (1, 2 or 3). A laboratory knows all three about its own bench before it
          measures. The replicate letter stays out: it names the repeat, not a property of the measurement.
        - The spectrum ships as the study published it and is declared as one (`special_features`, CLEAN-26),
          state `raw`. Bands a laboratory's instrument did not cover are missing in the source's table, and they
          stay missing: 180 of the 3,516 rows (5.1%) have a gap, almost all of them in two laboratories (P15 at
          16.8% of its bands, P07 at 3.7%), and 355 of the 534 bands are complete for every row. Cutting the axis
          to those 355 would make every row whole and is a modelling choice the rule leaves to the curator, so it
          is an issue rather than a step here.
        - Four spectra are each in the table twice. Every pair shares the laboratory, the substrate, the laser
          and the solution and differs only in the batch (P09, twice) or the replicate letter (P15, P18), so one
          measurement was filed under two labels rather than measured twice; the same spectrum cannot belong to
          two substrate batches. The copy is dropped and the first row kept (LEAK-19), which leaves 3,512. Both
          rows of every pair sit in one laboratory, so no split could have separated them.
        - 3,512 spectra over 15 laboratories, 43 distinct concentrations from 0 to 9, 234 of them blanks.
    """

    # Task
    target = "conc"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "The study reports no one score for a model. It fits a linear calibration per laboratory and reads "
            "it out as the slope, the intercept and the recovery of the test solutions, which judge a bench and "
            "not a prediction (MET-6). The Zenodo record names no metric and the benchmark scores the four files "
            "by its own convention, which is no choice of this source (EV-4). So the regression fallback."
        )
    )
    grouping = Grouping(
        on="labcode",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is one of the 15 participating laboratories, with every spectrum it measured, on every
            substrate batch and replicate. Holding a laboratory out is the study's own question: whether a
            calibration built on other benches reaches a bench it has never seen. Each spectrum is predicted on
            its own, as a laboratory reads one measurement at a time.
        """,
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # Only read here (cached across edits of `_clean`).
        return pd.read_csv(raw_dir / "zenodo" / "ILSdata.csv", low_memory=False)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()

        # The solution's identity, the blank/calibration/test label and the method string (curation notes).
        df = drop_columns(df, list(COPIED_OR_LEAKING))

        # The replicate letter names the repeat, not a property of the measurement.
        df = drop_columns(df, ["replica"])

        # Four spectra appear twice, each filed under two batch or replicate labels in one laboratory: one
        # measurement recorded twice, not two measurements (curation notes). The copy is dropped (LEAK-19).
        bands = [column for column in df.columns if column not in ("labcode", "substrate", "laser", "conc", "batch")]
        df = df.drop_duplicates(subset=bands, keep="first").reset_index(drop=True)

        # The bands are named by their wavenumber alone; the prefix lets the build read the axis from the names.
        kept = ("labcode", "substrate", "laser", "conc", "batch")
        df = df.rename(columns={column: f"{PREFIX}{column}" for column in df.columns if column not in kept})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The spectrum is declared in `special_features` and stays out of the dtypes (CLEAN-26). The laser is a
        # wavelength with two values and the batch a label, so both are categorical, not numbers to interpolate.
        return FeatureTypes(
            categorical=["labcode", "substrate", "laser", "batch"],
            string=[],
            datetime={},
        )

    special_features = (
        Spectrum(
            name="raman_spectrum",
            prefix=PREFIX,
            unit="cm-1",
            technique="raman",
            state="raw",
            description=(
                "The surface-enhanced Raman spectrum of the solution as the participating laboratory measured "
                "it, 534 bands from 400 to 1,999 cm-1, missing where that laboratory's instrument did not "
                "cover the band."
            ),
        ),
    )

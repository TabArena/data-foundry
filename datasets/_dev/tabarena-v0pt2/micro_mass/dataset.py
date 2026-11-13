"""Curated dataset definition for `micro_mass` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, Metric, Source, Spectrum, TaskSummary


class MicroMass(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Which bacterial species does the mass spectrum of an isolated colony come from?",
        use_case=(
            "A clinical microbiology laboratory identifies the species of an isolated bacterial colony from one "
            "MALDI-TOF mass spectrum (Mahé et al. 2014)."
        ),
        row=(
            "One MALDI-TOF mass spectrum of a bacterial strain, a technical replicate (571 spectra of 213 strains, 1 "
            "to 6 per strain, 20 species); the place and period are not stated."
        ),
        predicted="The species, one of 20.",
        known=(
            "The spectrum as peak intensities in mass bins (1,300 bins in the source, without the constant and "
            "repeated ones)."
        ),
        split=(
            "Whole strains are held out, as in Vervier et al. 2015, so the test data stands for isolates never "
            "measured; other strains of the same species are in training."
        ),
        changes=("We use the spectra of single species (the source also has mixtures) and split by strain."),
        fit="direct",
        fit_reason=(
            "A spectrum is all the laboratory has when identifying a colony, and a held-out strain is a new isolate. "
            "Some species have few strains, so their share of a test fold is small and uneven."
        ),
    )

    # Dataset
    unique_name = "micro_mass"
    domain = "biology & life sciences"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5T61S",
            license="CC BY 4.0",
            year="2013",
            bibtex=r"""
                @article{mahe2014automatic,
                  title={Automatic identification of mixed bacterial species fingerprints in a MALDI-TOF mass-spectrum},
                  author={Mahe, Pierre and Arsac, Maud and Chatellier, Sonia and Monnin, Val{\'e}rie and Perrot, Nadine and Mailler, Sandrine and Girard, Victoria and Ramjeet, Mahendrasingh and Surre, J{\'e}r{\'e}my and Lacroix, Bruno and others},
                  journal={Bioinformatics},
                  volume={30},
                  number={9},
                  pages={1280--1286},
                  year={2014},
                  publisher={Oxford University Press}
                }
            """,
        ),
    )
    data_tags = ("Timeless",)
    download_description = """
        wget https://archive.ics.uci.edu/static/public/253/micromass.zip && unzip micromass.zip micromass_un_anonymized.zip && rm micromass.zip && mkdir -p local-data-warehouse/micro_mass && unzip micromass_un_anonymized.zip -d local-data-warehouse/micro_mass/ && rm micromass_un_anonymized.zip
    """
    curation_comments = """
        We use the pure spectra version (without mixing) and replicate a grouped-based task to predict the species of strains.

        - We drop columns with the same value across all samples.
        - We drop constant columns (all 0).
        - Each strain has one species; the 20 species have 7 to 20 strains each (median 10; Escherichia coli 20, Haemophilus influenzae 18, Enterobacter cloacae 16; from the v1 exploration, counted 2026-10-22).
        - The spectrum is declared as one (`special_features`, CLEAN-26, 2026-11-02) in the state the instrument's software left it: a peak list on 1,300 fixed bins ("pre-processed by the standard algorithm used for routine (culture-based) bacterial identification, which provided a peak-list representation", the archive's README). The m/z of the bins is not published, so the axis is the bin number; the recommended encoding leaves a peak list as it is.
        - Time basis: Timeless: the species is a fixed property of the strain, known from the reference collection
          before the culture, and the row is the spectrum of that culture. The release holds no acquisition date, run or
          plate (the metadata file has the species and the strain number only), and the file order carries no campaign
          order (time probe, 2026-11-06: no order drift, p 0.58). The panel is a single 2013 deposit, the strain
          identifier is an integer with no accession or date, and no arrival order can be recovered, so the strain
          key stays the split (2026-11-12). Not tested: an isolate of a species or a strain type
          the panel does not hold, and a run batch shared across strains, which no column records.
    """

    # Task
    target = "Species"
    problem_type = "multiclass_classification"
    data_tags = ("Timeless",)
    metric = Metric.source(
        "hierarchical_balanced_accuracy",
        original="Accuracy averaged per strain, then per species (Vervier et al. 2015)",
        reference=(
            "Vervier, Mahé, Veyrieras, Vert 2015, Benchmark of structured machine learning methods for microbial "
            "identification from mass-spectrometry data, arXiv:1506.07251; Mahé et al. 2014 Bioinformatics 30(9)"
        ),
        inputs={"group": "Strain"},
        definition=(
            "accuracy of the spectra of each strain, averaged over the strains of each true species, then over "
            "species (Vervier et al. 2015)"
        ),
    )
    grouping = Grouping(
        on="Strain",
        labels="per_group",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a bacterial strain; its rows are technical replicate MALDI-TOF spectra (213 strains with 1 to 6 spectra, 20 species). The use case is identifying the species of an isolated colony from one spectrum (Mahé et al. 2014), so each spectrum is one prediction, made from that spectrum alone. Vervier et al. 2015 hold out one strain at a time and average the accuracy per strain, then per species.
        """,
    )

    special_features = (
        Spectrum(
            name="vitek_ms_peaks",
            prefix="peak_list_spectra_bin_",
            unit="bin",
            technique="mass_spectrometry",
            state="peaks",
            description=(
                "The colony's MALDI-TOF mass spectrum (VITEK MS) as the instrument's routine identification software "
                "leaves it: a peak list on 1,300 fixed bins, numbered because the source gives no m/z per bin; the "
                "bins that are constant or copy another bin are dropped."
            ),
        ),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(
            raw_dir / "micromass" / "pure_spectra_matrix.csv",
            header=None,
            names=[f"peak_list_spectra_bin_{i}" for i in range(1, 1301)],
            sep=";",
        )
        metadata = pd.read_csv(raw_dir / "micromass" / "pure_spectra_metadata_with-species-name.csv", sep=";")
        return {"df": df, "metadata": metadata}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df, metadata = raw["df"], raw["metadata"]
        df = pd.concat([metadata, df], axis=1)
        # cast before the sort below, which orders by category
        df["Strain"] = df["Strain"].astype("category")
        # Drop duplicate columns based on values
        df = df.loc[:, ~df.T.duplicated()]
        # DRop constant columns
        df = df.loc[:, (df != df.iloc[0]).any()]
        df = df.sample(frac=1, random_state=42).sort_values(by="Strain", kind="stable").reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["Strain"])

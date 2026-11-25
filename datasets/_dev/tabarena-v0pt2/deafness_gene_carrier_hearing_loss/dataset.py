"""Curated dataset definition for `deafness_gene_carrier_hearing_loss` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    GroupBasis,
    Metric,
    NonFeature,
    Source,
    TaskSummary,
    TimeBasis,
    decode,
    drop_columns,
)

RAW_FILES = (("Discovery Set.xlsx", "discovery"), ("Validation Set.xlsx", "validation"))
"""The two files of the Mendeley release and the recruiting source each holds (Luo et al. 2021, Methods)."""

GENE_NAMES = {"GJB2": "GJB2", "SLC26A4": "SLC26A4", "mtDNA": "MT-RNR1"}
"""The gene header of the files; its `mtDNA` block holds the 7 MT-RNR1 variants the paper names (Methods)."""


class DeafnessGeneCarrierHearingLoss(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Does a person who carries variants of the deafness genes GJB2, SLC26A4 or MT-RNR1 have hearing loss?"
        ),
        use_case=(
            "A genetic counsellor estimates whether a person's GJB2, SLC26A4 and MT-RNR1 genotype predicts hereditary "
            "hearing loss for a relative or newborn whose hearing is not yet tested, in place of the expert's "
            "rule-based reading (the source's stated use)."
        ),
        row=(
            "One person with at least one variant at 144 sites of the three genes (1,778): Chinese patients, their "
            "family members and community screenees of a Shanghai hospital, or of the Disabled Persons' Federation."
        ),
        predicted=(
            "Whether the person failed the hearing screening and was diagnosed with hereditary hearing loss (76%), "
            "or passed it as a carrier with normal hearing."
        ),
        known=(
            "How many copies of each variant the person carries (none, one or two) at the sites seen in the data; "
            "one site of one person is missing."
        ),
        split=(
            "Random people from all three recruiting sources (the hospital's records; the Disabled Persons' "
            "Federation and a community screening, unmarked in one file), so the test data stands for new carriers "
            "like these; relatives and people with the same genotype can be on both sides."
        ),
        changes=(
            "We pool the source's discovery and validation files and drop the sites no person carries; the file a "
            "person comes from is no feature."
        ),
        fit="approximate",
        fit_reason=(
            "Real genotypes and hearing, but a case-control sample: controls partly obligate-carrier parents, "
            "relatives without a family id, and carriers of only the common GJB2 polymorphisms mostly patients "
            "because of who was sequenced. The label is hearing at one screening, not the lifetime outcome for "
            "p.V37I (reduced penetrance), SLC26A4 (progressive loss) or MT-RNR1 (aminoglycoside exposure); in the "
            "clinic the hearing test gives it cheaply."
        ),
    )

    # Dataset
    unique_name = "deafness_gene_carrier_hearing_loss"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="Other",  # Mendeley Data, the data deposit of Luo et al. 2021
            url="https://doi.org/10.17632/6mh8mpnbgv.1",
            license="CC BY 4.0",
            year="2021",
            bibtex="""
                @misc{luo2021deafnessdata,
                  author       = {Luo, Xiao Mei},
                  title        = {Data for: Machine learning-based genetic diagnosis models for hereditary hearing
                                  loss by the {GJB2}, {SLC26A4} and {MT-RNR1} mutations},
                  year         = {2021},
                  howpublished = {Mendeley Data, V1},
                  doi          = {10.17632/6mh8mpnbgv.1},
                  note         = {Data of Luo et al. (2021), EBioMedicine 69:103322, doi 10.1016/j.ebiom.2021.103322}
                }
            """,
            files=("Discovery Set.xlsx", "Validation Set.xlsx"),
        ),
    )
    download_description = """
        We download the two files of the Mendeley Data record 6mh8mpnbgv, version 1.

        mkdir -p local-data-warehouse/deafness_gene_carrier_hearing_loss && cd local-data-warehouse/deafness_gene_carrier_hearing_loss
        curl -L -o "Discovery Set.xlsx" https://data.mendeley.com/public-files/datasets/6mh8mpnbgv/files/c34a6eac-83b9-41b6-8ab6-9e0b85dcec03/file_downloaded
        curl -L -o "Validation Set.xlsx" https://data.mendeley.com/public-files/datasets/6mh8mpnbgv/files/4366da49-3e48-4b00-81bc-2684fbf3507c/file_downloaded
    """
    curation_comments = """
        We start with the two files of the Mendeley Data record (`Discovery Set.xlsx`, 1,209 people of the Shanghai Ninth People's Hospital; `Validation Set.xlsx`, 569 people of the Disabled Persons' Federation and a community screening), which are all the record holds.

        - Each file has two header rows, the gene and the variant; we name each column `<gene>_<variant>` as the files write the variant. The files' `mtDNA` block is the 7 MT-RNR1 variants the paper names (Methods: "47 variants of GJB2, 90 variants of SLC26A4 and 7 variants of MT-RNR1"), so it is named MT-RNR1.
        - A value is the number of variant alleles at the site, as the record states ("No mutations found were indicated by 0, heterozygous mutations by 1, and homozygous mutations by 2"); MT-RNR1 sites are 0 or 1. The counts stay numbers.
        - The target is `Diagnoses` (1: failed the hearing screening and diagnosed with hereditary hearing loss, 918 + 436 people; 0: passed it, a carrier with normal hearing, 291 + 133), shipped as `HearingLoss` Yes/No. It is the hearing phenotype of a variant carrier, not the mode of inheritance.
        - The two files are pooled; the file (the recruiting source) is kept as `source_file`, a provenance column that no task uses as a feature (curator's decision, 2026-11-25, Andrej).
        - We drop the 16 sites that no person in either file carries (constant zero), and two sites whose column copies another: GJB2 p.G160S is carried only by the one patient who carries p.N206S, and MT-RNR1 c.1541T>C only by the two validation people who carry c.1519_1520insCA. 126 sites remain; 95 of them are carried by fewer than 5 people, 17 only by validation people and 73 only by discovery people.
        - Anomaly: one cell (`GJB2_c.235delC`, discovery file, sheet row 497, a hearing-loss patient whose only other variant is one SLC26A4 p.G222V allele) is a blank string; it is shipped as missing.
        - Anomaly: the release holds 1,778 people where the paper counts 1,898 (1,354 patients, 544 carriers); the 1,354 patients are all here, 120 carriers of the discovery set are not (291 of the paper's 411; unexplained in the paper and the record).
        - Note: the 1,778 people hold 341 distinct genotypes (280 in the 1,209 discovery people); 1,390 rows repeat the genotype and the label of an earlier row, and 47 genotypes, held by 1,100 people, occur with both labels (incomplete penetrance, or variants outside the 144 sites). The rows also include patients' immediate family members, with no family id. Every person stays a row (curator's decision, 2026-11-25, Andrej: they are different people, not one record entered twice); the genotype's share of patients is what a model learns. About 22-30 small family clusters can be found from the raw order (neighbouring rows sharing a rare variant, 49-67 people); the label does not travel with them (trios of a biallelic patient and two carrier parents), and grouping the folds by them leaves ROC AUC unchanged (untuned gradient boosting 0.752 against 0.750).
        - Note (selection, record marker `Selection Bias`): patients and carriers were recruited separately (patients who failed the hearing screening; carriers who passed it, many of them relatives). 558 people carry only the GJB2 polymorphisms p.V27I, p.E114G or p.I203T, and 83% of them are patients, more than among the 1,220 people with any other variant (73%). The three are benign in DVD; in ClinVar p.I203T is benign and the other two are of uncertain significance; the paper calls them "widely regarded as benign" (Discussion), but this is contested (homozygous p.V27I/p.E114G has been linked to mild-to-moderate loss; our 63 double homozygotes are 84% patients). Counting p.T123N too (40 carriers, ClinVar likely benign/benign), the benign-only group is 581 people, 83.1% patients against 72.8%, so the conclusion stands. Their hearing loss is not explained by an accepted pathogenic genotype, so for them the label says who was sequenced, not what the genotype does. The paper adds carriers from a community's NGS hotspot screening at the same hospital to offset the patients (Methods: "Due to the way the data were collected, most samples were HHL"); these 103 people are in the validation file (Table 1: 2020.5-2020.8, NGS hotspot), while the hospital's records and the Disabled Persons' Federation's people were Sanger sequenced (96% of the sites overlap); sites seen in one class only are no more than chance gives (71 patient-only sites against 65.6 expected from the class shares, 10 carrier-only against 15.0).
        - Anomaly (recording by class, kept): the discovery file opens with 53 carriers (sheet rows 3-55; 36 carry one p.V37I allele, 9 one SLC26A4 c.919-2A>G allele, the column `SLC26A4_c.919_2A>G` as the files write it) none of whom has p.V27I, p.E114G or p.I203T recorded, against 61% of the other 238 discovery carriers and 54% of the patients, so this block was likely typed with a panel that does not report the three polymorphisms (cause unknown: the paper's community NGS screening is in the validation file (Table 1), and the discovery file is the hospital's Sanger-sequenced records). Models give its people a lower patient probability (0.55 on average against a 0.76 base rate), but it changes little elsewhere: untuned gradient boosting scores the other test people 0.733 trained with the block and 0.739 without it (30 random 3-fold splits). The rest of both files mixes the classes along the row order (the time probe's order drift is this block and a run of patients in the validation file's middle), and the rows are shuffled.
        - Note (rule baseline, TP-4): the textbook reading the paper's experts state (Methods: homozygous or compound heterozygous GJB2 or SLC26A4, or any MT-RNR1 variant, is hearing loss; a heterozygote is a carrier; "any MT-RNR1 variant" is too broad for `MT-RNR1_c.1438G>A`, 2 people, the haplogroup polymorphism m.1438A>G), not fitted, scores ROC AUC 0.652 on 30 random stratified 3-fold splits (10 repeats, our own draws), 0.677 when the three benign polymorphisms are not counted; untuned gradient boosting 0.750 and an exact-genotype lookup 0.781, ahead on all 30 folds. Without the 558 benign-only people the rule (0.782) matches gradient boosting (0.774, ahead on 10 of 30 folds) and a lookup leads it by 0.026. By part: in the hospital file without the 53-carrier block, the rule scores 0.685, untuned gradient boosting 0.721 and a lookup 0.753 (ahead of the rule on 28 and 30 of 30 folds); in the validation file 0.639, 0.761 and 0.789. Benign-only people are 0.816 patients in the hospital file (others 0.784) and 0.857 in the validation file (others 0.721).
        - Note: the one blank `GJB2_c.235delC` cell stays missing (CLEAN-10); imputing 0 would invent a value, and a missing indicator gains nothing (0.0000).
    """
    splits_comment = """
        Default splits: 10 repeats of 3-fold cross-validation over all 1,778 people of both files, stratified on the
        label (curator's decision, 2026-11-25, Andrej), not the source's discovery-to-validation split. The two files
        hold three recruiting sources (the hospital's records; in the validation file, unmarked, 466 people of the
        Disabled Persons' Federation and 103 of a community screening), too few to hold sources out (the group basis). Trained on the discovery file and
        scored on the validation file, untuned gradient boosting reaches the ROC AUC it reaches on random folds (0.750
        against 0.750) in the source's direction; trained on the validation file and scored on the discovery file, a
        training side half as large, it scores 0.672, below the expert-like rule (0.695); and a model tells the file from the genotype only weakly (ROC AUC 0.58), so the transfer the
        source tested is close to the random split. 85% of the test people share their exact genotype with a training
        person; held out by genotype, untuned models fall to ROC AUC 0.41-0.49, below the textbook rule (0.63-0.68).
    """
    non_features = (
        NonFeature(
            "source_file",
            "provenance",
            "the file a person comes from, which is the recruiting source (discovery: the hospital's records; "
            "validation: the Disabled Persons' Federation and a community screening)",
        ),
    )
    split_leaf = "L-PLACE.random"
    time_basis = TimeBasis(
        "Timeless",
        """
        the genotype is fixed at birth and the hearing phenotype was recorded with it at the
        screening; the discovery people were seen from October 2009 to April 2017, but no date is published per
        person, and the relation of genotype to hearing loss is biological. A second panel (NGS hotspot, 96% site
        overlap) is already in the validation file, for 103 people screened in 2020, unmarked; carriers from other
        panels or clinics are not tested.
        """,
    )
    group_basis = GroupBasis(
        """
        ForcedIIDFromGrouped (Andrej, 2026-11-25): the source validates on a second recruiting source
        (the validation file: 466 people of the Disabled Persons' Federation, Sanger, 2011.8-2017.4, and 103 of a
        community screening, NGS hotspot, 2020.5-2020.8, with no column or row block that tells them apart), and the
        use case reaches carriers from other clinics and screening programmes, which whole sources held out would
        stand for; the release holds three sources, two of them unmarked in one file, too few for a grouped split, so
        the split is random over all. Overlap left: each test
        fold holds people of all sources, and relatives (no family id) and people with the same genotype sit on
        both sides, so the score is optimistic for a new source.
        """,
    )

    # Task
    target = "HearingLoss"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Luo et al. 2021 rank their six models by ROC AUC (Methods: 'evaluated by ... the receiver operating "
            "characteristic curve (ROC) and area under the curve (AUC)') but also report accuracy, sensitivity, "
            "precision and F1 with no threshold or cost fixed, so no one deliberate choice (MET-5); the fallback, "
            "ROC AUC, is the metric they rank by."
        ),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        frames = []
        for file, source in RAW_FILES:
            raw = pd.read_excel(raw_dir / file, header=None, dtype=object)
            genes = raw.iloc[0].ffill()
            columns = ["Diagnoses"] + [f"{genes[i]}|{raw.iloc[1, i]}" for i in range(1, raw.shape[1])]
            df = raw.iloc[2:].set_axis(columns, axis=1).reset_index(drop=True).copy()
            df["source_file"] = source
            frames.append(df)
        return pd.concat(frames, ignore_index=True)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        variants = [c for c in df.columns if "|" in c]
        # one blank-string cell (GJB2 c.235delC, discovery sheet row 497) is a missing value
        df[variants] = df[variants].apply(lambda col: pd.to_numeric(col.mask(col.astype(str).str.strip().eq(""))))
        assert df[variants].stack().isin([0, 1, 2]).all()
        # `<gene>_<variant>`, the files' mtDNA block named for its gene, MT-RNR1
        df = df.rename(columns={c: f"{GENE_NAMES[c.split('|')[0]]}_{c.split('|')[1]}" for c in variants})
        variants = [f"{GENE_NAMES[c.split('|')[0]]}_{c.split('|')[1]}" for c in variants]
        # sites no person in either file carries
        df = drop_columns(df, [c for c in variants if df[c].fillna(0).eq(0).all()])
        # two pairs of sites carried by the same people only (one patient; two people of the validation file): the
        # second site of each pair is a copy of the first column
        assert df["GJB2_p.G160S"].equals(df["GJB2_p.N206S"])
        assert df["MT-RNR1_c.1541T>C"].equals(df["MT-RNR1_c.1519_1520insCA"])
        df = drop_columns(df, ["GJB2_p.G160S", "MT-RNR1_c.1541T>C"])
        # the target: 1 failed the hearing screening (hereditary hearing loss), 0 passed it (carrier)
        df = df.rename(columns={"Diagnoses": self.target})
        df[self.target] = df[self.target].astype(int).astype(str)
        df = decode(df, {self.target: {"0": "No", "1": "Yes"}})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["source_file"])

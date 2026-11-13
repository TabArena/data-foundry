"""Curated dataset definition for `splice` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping, Metric, Source, TaskSummary

GROUP = "gene_group"


def _entry_components(entries: pd.Series, windows: pd.Series) -> pd.Series:
    """One number per row: its GenBank entry, joined with every entry that holds an identical window.

    The entry is the instance name before the site type (``HUMHBA4`` in ``HUMHBA4-DONOR-7090``). Entries that share a
    60-base window exactly are one gene in overlapping entries (``HUMIL2``, ``HUMIL2A``, ``HUMIL2B``): an exact key
    (SPLIT-24). The number follows the component's first row in the file, so no entry name ships.
    """
    parent = {entry: entry for entry in entries.unique()}

    def root(entry: str) -> str:
        while parent[entry] != entry:
            parent[entry] = parent[parent[entry]]
            entry = parent[entry]
        return entry

    for shared in entries.groupby(windows.to_numpy()).unique():
        for other in shared[1:]:
            parent[root(other)] = root(shared[0])
    return pd.Series(pd.factorize(entries.map(root))[0], index=entries.index)


def _one_row_per_record(labels: pd.Series, entries: pd.Series, positions: pd.Series, windows: pd.Series) -> pd.Series:
    """Which rows stay once the copies of one GenBank record go (LEAK-19, LEAK-20).

    A window that repeats with the same label is one record, kept in its first row: the same gene in overlapping
    entries (``HUMIL2``, ``HUMIL2A``) or one name listed twice. A window with two labels goes in every row
    (``HUMCYPIIE`` at 12121, an intron-to-exon junction and no junction). A window that one entry holds at two or more
    positions is a duplicated gene (the two alpha-globin genes of ``HUMHBA4``): the first row per position of that
    entry stays, each a distinct place in the genome.
    """
    two_labels = labels.groupby(windows).transform("nunique") > 1
    keep = ~(pd.DataFrame({"window": windows, "label": labels}).duplicated() | two_labels)
    rows = pd.DataFrame({"window": windows, "entry": entries, "position": positions})[~two_labels]
    rows = rows[rows.groupby("window")["entry"].transform("size") > 1]
    for _, copies in rows.groupby("window"):
        loci = copies.groupby("entry")["position"].nunique()
        if loci.max() > 1:
            keep.loc[copies.index] = False
            keep.loc[copies[copies["entry"] == loci.idxmax()].drop_duplicates("position").index] = True
    return keep


class Splice(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is the middle of this 60-base stretch of DNA a splice junction, and of which kind?",
        use_case=(
            "For example, a gene-annotation tool scans a primate DNA sequence and marks where exons and introns meet,"
            " to predict how a gene's RNA is spliced."
        ),
        row=("One 60-nucleotide window of primate DNA around a candidate site (3,017 windows, UCI 1992)."),
        predicted=("The site type: exon-to-intron junction (23%), intron-to-exon junction (23%), or neither (55%)."),
        known=(
            "The base at each of the 60 positions, 30 on each side of the site: A, C, G, T or a code for an ambiguous"
            " base."
        ),
        split=(
            "Whole GenBank entry components (an entry and every entry that shares an identical window with it, one"
            " gene in overlapping entries), so the test data stands for genes whose entries the model has not seen;"
            " orthologs and sister genes in other entries can still be in training."
        ),
        changes=(
            "We drop 171 copies of one GenBank record (a window repeated with its label, from an overlapping entry or"
            " a name listed twice) and both rows of the one window labelled a junction and no junction, keeping the 13"
            " second places of duplicated genes, and replace the source's random cross-validation with a split by"
            " GenBank entry component, built from the instance names, which do not ship."
        ),
        fit="approximate",
        fit_reason=(
            "The windows are a curated set in which about half are junctions, a share set by how the examples were "
            "chosen rather than by how often junctions occur along a gene."
        ),
    )

    # Dataset
    unique_name = "splice"
    domain = "biology & life sciences"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C5M888",
            license="CC BY 4.0",
            year="1992",
            bibtex="""
                @article{towell1994knowledge,
                  title={Knowledge-based artificial neural networks},
                  author={Towell, Geoffrey G and Shavlik, Jude W},
                  journal={Artificial intelligence},
                  volume={70},
                  number={1-2},
                  pages={119--165},
                  year={1994},
                  publisher={Elsevier}
                }
            """,
        ),
    )
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/splice/ && wget -P local-data-warehouse/splice/ https://archive.ics.uci.edu/static/public/69/molecular+biology+splice+junction+gene+sequences.zip && unzip local-data-warehouse/splice/molecular+biology+splice+junction+gene+sequences.zip -d local-data-warehouse/splice/
    """
    curation_comments = """
        - We tabularized the fixed-size DNA sequences from the original dataset based on the nucleotide position.
        - We removed the instance ID.
        - Copies of one record (2026-11-12, Andrej; LEAK-19, LEAK-20): 125 windows of 60 bases occur more than once
          (310 rows), most the same gene in overlapping GenBank entries (`HUMIL2`, `HUMIL2A`, `HUMIL2B`; 107 groups)
          or one name listed twice (`HUMALBGC-ACCEPTOR-18496`; 12 groups). We keep one row per window and label, the
          first in the file, and drop both rows of the one window labelled two ways (`HUMCYPIIE` at 12121, an
          intron-to-exon junction and no junction). A window that one entry holds at two or more positions is a
          duplicated gene whose junctions read the same (the two alpha-globin genes of `HUMHBA4`, the gibbon's two
          gamma-globin genes in `GIBHBGGL`, the growth hormone cluster `HUMGHCSA`): for these 13 windows we keep one
          row per position of that entry, each a distinct place in the genome. 173 rows go (171 copies and the pair)
          and 3,017 remain: exon-to-intron 685 (22.7%, from 24.0%), intron-to-exon 679 (22.5%, from 24.1%), neither
          1,653 (54.8%, from 51.9%). Nearly all copies are junctions, as overlapping entries repeat the same annotated
          junction; the label means the same after the drop. The two windows of a duplicated gene lie in one entry and
          so in one group; under random folds 0.6% of the test windows would meet such a twin in training.
        - Split (2026-11-12, Andrej; SPLIT-24, SPLIT-34): grouped by GenBank entry component (`gene_group`), built in
          `_clean` from the instance name before it is dropped: the entry is the name before the site type
          (`HUMHBA4-DONOR-7090`), and entries that share an identical 60-base window are joined, one gene in
          overlapping entries (`HUMIL2`, `HUMIL2A`, `HUMIL2B`), through the identical windows of the whole file, the
          dropped copies included. 1,440 components over the 3,017 windows; 1,226 hold one window, the largest 65
          (2.2%). Every window that occurs more than once lies in one component, so no identical window crosses the
          split, and overlapping windows of one entry stay together. On the shipped 10 x 3 folds 1.6% of the test
          windows keep a training window within 3 of 60 bases (0.7% to 2.5% per fold), against 3.7% under random
          folds of the same rows (0.6% identical). The grouping cost nothing in score (untuned LightGBM log loss 0.118
          against 0.120 at random, logistic regression 0.160 both; 10 x 3, 2026-11-10). Orthologs and sister genes in
          other entries share no identical window and still cross; grouping them by sequence similarity is barred.
        - Time basis: Timeless: a splice junction is a property of the sequence; the windows were cut in 1992 from
          GenBank 64.1 and labelled by its annotation. The windows' GenBank entries, dated by their earliest reference
          year at NCBI (1,388 of 1,475 entries, 94%, 1974 to 1990), show no wave: the junction share and the
          difficulty show no trend with the year, and predicting each later year from the earlier ones leaves as many
          close relatives as a random draw of the same size (4.1% against 4.0% of the test windows with a training
          window within 3 of 60 bases; 2.3% when the draw keeps out the test windows' entry components), so the
          family key stands. Grouped by entry component, 1.6% of the test windows keep a training window within 3 of
          60 bases, in entries no exact key links: the same gene in another primate or a sister gene. Not tested: a
          gene with no relative among the training windows.
    """

    # Task
    target = "SiteType"
    problem_type = "multiclass_classification"
    data_tags = ("Timeless",)
    metric = Metric.fallback(
        reason="Towell, Shavlik & Noordewier 1990-1994 report test error rates of KBANN (per class too), a habit without costs between the three site types. Original rejected: error rate. log_loss is the multiclass fallback.",
    )

    # Splits: whole GenBank entry components held out
    grouping = Grouping(
        on=GROUP,
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a GenBank entry component: the windows of one entry (the instance name before the site type)
            and of every entry that shares an identical 60-base window with it, which is one gene in overlapping
            entries (HUMIL2, HUMIL2A, HUMIL2B). A gene-annotation tool meets genes whose entries it has not seen, so
            whole components are held out. Each window is one prediction, made from its own 60 bases; the windows of a
            component carry different site types.
        """,
    )
    splits_comment = """
        Grouped 3-fold cross-validation over the 1,440 GenBank entry components with 10 repeats: the windows of an
        entry, and of every entry that shares an identical 60-base window with it, stay on one side. Each test fold
        holds 877 to 1,121 windows. No test window has an identical window in training (0.6% under random folds of
        the same rows), and 1.6% have one within 3 of 60 bases (3.7% at random), in entries no exact key links. A
        split by GenBank entry year was measured and leaves as many close relatives as a random draw, so the entry
        component stands (curation notes). The source scored ten-fold cross-validation on 1,000 random windows.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/splice.data", index_col=False, header=None)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Strip tab-like whitespaces from original data
        df = df.map(lambda x: x.strip())
        # the split's group, from the instance ID before it goes: the GenBank entry component (SPLIT-24, SPLIT-34),
        # joined through identical windows of the whole file
        name = df[1].str.rsplit("-", n=2)
        gene_group = _entry_components(entries=name.str[0], windows=df[2])
        # one row per GenBank record: the copies of one record and the window with two labels go (LEAK-19, LEAK-20)
        keep = _one_row_per_record(labels=df[0], entries=name.str[0], positions=name.str[2], windows=df[2])
        df, gene_group = df[keep], gene_group[keep]
        df = df.drop(columns=[1])  # Drop instance ID
        target_feature = "SiteType"
        split_data = df[2].apply(lambda x: pd.Series(list(x)))
        # Generate new column names from -30 to +30 excluding 0
        split_data.columns = [f"position_{i}" for i in range(-30, 31) if i != 0]
        split_data[target_feature] = df[0]
        split_data[GROUP] = gene_group
        df = split_data.reset_index(drop=True)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=[c for c in df.columns if c.startswith("position_")])

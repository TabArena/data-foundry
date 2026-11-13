"""Curated dataset definition for `cns_tumor_methylation_classification` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import csv
import gzip
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, TaskSummary

BETA_FILE = "GSE90496_beta.txt.gz"
"""GEO's processed data: one row per array probe, then per sample its beta value and its detection p-value."""

PREPARED = ("betas.float64", "betas_probes.txt", "betas_samples.txt")
"""The beta values as a raw float64 matrix (probes x samples, C order), its probe names and its sample columns."""

N_PROBES_KEPT = 428_799
"""CpG probes the paper kept: "In total, 428,799 probes targeting CpG sites were kept" (Methods). GEO's beta file
holds exactly these: none is on the authors' four exclusion lists (mnp_training, `filter/`; checked 2026-11-08)."""

SHARED_WITH_SARCOMA_METHYLATION = (
    "GSM2403937",
    "GSM2403951",
    "GSM2403953",
    "GSM2403955",
    "GSM2403956",
    "GSM2403957",
    "GSM2403958",
    "GSM2403960",
    "GSM2403961",
    "GSM2403962",
    "GSM2404018",
    "GSM2404240",
    "GSM2404242",
    "GSM2404250",
    "GSM2404254",
    "GSM2404430",
    "GSM2404433",
    "GSM2404434",
    "GSM2404472",
    "GSM2404538",
    "GSM2404566",
    "GSM2404610",
    "GSM2404651",
    "GSM2404732",
    "GSM2404852",
    "GSM2405070",
    "GSM2405126",
    "GSM2405127",
    "GSM2405128",
    "GSM2405183",
    "GSM2405218",
    "GSM2405304",
    "GSM2405314",
    "GSM2405370",
    "GSM2405632",
)
"""The 35 arrays of this series that GSE140686 (`sarcoma_methylation_classification`) holds too, matched by their
chip and position (Sentrix id) in the two series' file lists. Kept here; see the curation notes."""


def series_annotation(path: Path) -> pd.DataFrame:
    """One row per sample of the GEO series matrix: accession, title, methylation class, material, Sentrix id."""
    fields: dict[str, list[str]] = {}
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break
            if not line.startswith("!Sample_"):
                continue
            key, *values = next(csv.reader([line.rstrip("\n")], delimiter="\t"))
            if key == "!Sample_characteristics_ch1":  # one line per characteristic: "methylation class: ..."
                name = values[0].split(": ", 1)[0]
                assert all(v.startswith(f"{name}: ") for v in values), name
                fields[name] = [v.split(": ", 1)[1] for v in values]
            elif key in ("!Sample_geo_accession", "!Sample_title") or (
                key == "!Sample_supplementary_file" and key not in fields
            ):
                fields[key] = values
    annotation = pd.DataFrame(
        {
            "gsm": fields["!Sample_geo_accession"],
            "title": fields["!Sample_title"],
            "methylation_class": fields["methylation class"],
            "material": fields["material"],
            "sentrix": pd.Series(fields["!Sample_supplementary_file"]).str.extract(r"_(\d+_R\d\dC\d\d)_Grn")[0],
        }
    )
    # The title is "<class>, sample <n> [reference set]"; <n> names the column `SAMPLE <n>` of the beta file.
    parts = annotation["title"].str.extract(r"^(.*), sample (\d+) \[reference set\]$")
    assert parts.notna().all().all(), "a title without a sample number"
    # (15 titles of `PLEX, PED A` keep a trailing space that the characteristic lacks)
    assert (parts[0].str.strip() == annotation["methylation_class"].str.strip()).all(), "title and class disagree"
    annotation["beta_column"] = "SAMPLE " + parts[1]
    return annotation


class CnsTumorMethylationClassification(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Which of the 91 methylation classes of the DKFZ classifier, 82 tumour classes and 9 normal-tissue "
            "classes, does a central nervous system tumour sample belong to, judged from its DNA methylation profile?"
        ),
        use_case=(
            "A neuropathologist assigns a brain or spinal tumour, after surgery or biopsy, to a diagnostic class "
            "from its methylation array, as the DKFZ classifier of Capper et al. (2018) does in routine diagnostics, "
            "where it changed the diagnosis in 12% of 1,104 prospective cases."
        ),
        row=(
            "One tumour or control-tissue sample of one patient on the Illumina 450k array: the 2,801 samples of the "
            "classifier's reference cohort (Heidelberg and partner centres, profiled up to 2016)."
        ),
        predicted=(
            "The sample's methylation class as the reference cohort assigned it: 91 classes of 8 to 143 samples, 18 "
            "of them with 10 or fewer; 119 samples of normal or inflamed tissue form 9 of the classes."
        ),
        known=(
            "The methylation level (beta value, 0 to 1) at 428,799 CpG sites, and whether the tissue was "
            "formalin-fixed and paraffin-embedded or frozen."
        ),
        split=(
            "Random samples, stratified by class, so the test data stands for new patients' samples from the same "
            "centres and years; the smallest classes have 2 or 3 samples in a test fold."
        ),
        changes=(
            "We spell out the class names, add the tissue material as an input (the authors removed its effect "
            "from the values instead) and leave out the detection p-value GEO ships next to each beta value."
        ),
        fit="approximate",
        fit_reason=(
            "The inputs and the classes are those of the classifier pathologists use, but the reference cohort holds "
            "selected samples of high tumour content whose class was confirmed, and part of the classes were drawn "
            "by clustering these same profiles; routine cases are less clean and may match no class at all."
        ),
    )

    # Dataset
    unique_name = "cns_tumor_methylation_classification"
    year = "2018"
    domain = "medical & healthcare"
    # GEO series of the DKFZ (Heidelberg), public with the Nature paper; the paper is the first publication of the task
    source = "Other"
    source_url = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE90496"
    license = (
        "Public GEO data: NCBI places no restrictions on its use or distribution, though submitters may claim rights "
        "(GEO disclaimer); the submitters state no licence"
    )
    download_description = """
        From GEO series GSE90496 (reference set of GSE109381), into the dataset's raw folder; the IDATs
        (`GSE90496_RAW.tar`, 23 GB) are not needed, the beta file is their processing.

        mkdir -p local-data-warehouse/cns_tumor_methylation_classification && cd local-data-warehouse/cns_tumor_methylation_classification
        B=https://ftp.ncbi.nlm.nih.gov/geo/series/GSE90nnn/GSE90496
        wget $B/suppl/GSE90496_beta.txt.gz                       # 9.9 GB, md5 b96fabf5099991341823506a83fc2945
        wget $B/suppl/GSE90496_methylationclassdescription.xlsx  # md5 19f821d01054c1d62aa6c19922612b9e
        wget $B/matrix/GSE90496_series_matrix.txt.gz             # GEO regenerates it; md5 7fb9d7368438318547a9d8dd71bb5429 (2026-08-29)

        The first run writes `betas.float64` (9.6 GB), `betas_probes.txt` and `betas_samples.txt` next to them
        (`_prepare_raw_files`, about 4 minutes).
    """
    bibtex = """
        @article{capper2018dna,
          title={{DNA} methylation-based classification of central nervous system tumours},
          author={Capper, David and Jones, David T. W. and Sill, Martin and Hovestadt, Volker and Schrimpf, Daniel and Sturm, Dominik and Koelsche, Christian and Sahm, Felix and Chavez, Lukas and Reuss, David E. and others},
          journal={Nature},
          volume={555},
          number={7697},
          pages={469--474},
          year={2018},
          doi={10.1038/nature26000}
        }
    """
    curation_comments = """
        We start with `GSE90496_beta.txt.gz` (the beta values of the 2,801 arrays as GEO processed them), the series matrix `GSE90496_series_matrix.txt.gz` (the methylation class and the material of each sample) and `GSE90496_methylationclassdescription.xlsx` (the class names) of GEO series GSE90496, the reference set of Capper et al. (2018).

        - Prediction point: a tumour sample, taken at surgery or biopsy, has been profiled on the 450k array, and the model assigns its methylation class from the beta values and the tissue material; no clinical field enters (GEO gives none besides the class and the material).
        - Rows: all 2,801 samples of the reference set, one per patient ("n=2801 patients", overall design; "2,801 biologically independent samples", Extended Data Fig. 1). No two profiles are equal, and the closest pair correlates 0.951 (centred betas of 20,000 random probes), two normal cerebellum samples, so no tumour seems profiled twice. The GEO accession is an identifier and is not shipped. The validation set (GSE109379, 1,104 samples) is left out: its classes are the classifier's own calls, not a diagnosis.
        - Features: the 428,799 beta values (the methylated share at each CpG site, 0 to 1) as GEO ships them, processed per sample (minfi `preprocessIllumina`: background correction and scaling of each array's two colour channels to control probes, against the array itself or one fixed reference) and not corrected across samples. GEO's file holds exactly the paper's 428,799 probes: none is on the authors' four exclusion lists (3,965 cross-hybridising, 32,260 missing from the EPIC array, 7,998 near a SNP, 11,551 on the X or Y chromosome; mnp_training, `filter/`), and it has no SNP-genotyping or non-CpG probe. No value is missing, and no probe is constant or a copy of another. The detection p-value GEO ships next to each beta value is left out: a quality measure of the probe's signal, which the classifier does not read.
        - Material: `material` (FFPE or frozen) is a feature. The lab knows it when it profiles a sample, and the authors' classifier reads it too: it removes the material's effect from the values with a linear batch correction fitted on the training samples (mnp_training, `R/batchadjust.R`). The material is tied to the class (34 classes are FFPE only, one is frozen only, 591 samples in all; decision table), but it adds little: alone it lowers the log loss from the class shares' 4.19 to 4.04, and a random forest on the 10,000 probes of highest variance scores 0.728 without it and 0.731 with it (6 shipped splits). The betas carry it anyway (ROC AUC 0.976 from the betas, logistic regression, 3 folds), yet models do not read it as a class cue: in the 56 classes of both materials, samples of their class's rarer material score a log loss of 0.64 against 0.65 for the others (random forest without the column, 3 splits). Frozen samples score better than FFPE ones (0.54 against 0.82), and routine cases are mostly FFPE.
        - Target: `methylation_class`, the series' characteristic, written as the class description's names ("glioblastoma, IDH wildtype, H3.3 G34 mutant" for `GBM, G34`). 91 classes: 82 tumour classes and 9 classes of normal or inflamed tissue (119 samples), which the classifier has so that a sample of little tumour is recognised as such. The class description relates 36 classes to a WHO entity one to one, 27 as subclasses of a WHO entity and 19 as not equivalent to one (decision table).
        - Label origin: the classes were drawn from histology together with unsupervised clustering of these same profiles ("All histopathological entities and variants were analysed by unsupervised clustering", Capper et al. 2018, "CNS tumour reference cohort"). The paper counts 29 of the 82 tumour classes as subclasses of a WHO entity (category 2); the class description file, read by `_decisions`, lists 27 (decision table). The count is redone when each subdividing class is checked against the WHO classification of 2021. They are kept as published: they are what the classifier in clinical use assigns and pathologists act on, and the WHO classification of 2021 defines some tumour types and subtypes by their methylation profile (Louis et al. 2021).
        - Small classes: 7 classes have 8 samples and 18 have 10 or fewer, so a test fold holds 2 or 3 samples of the smallest. The 18 hold 5.6% of the rows and 12.0% of a random forest's log loss (the 10,000 probes of highest variance, 6 shipped splits): about twice their share, not most of the score, so they stay.
        - Note: the task is near the ceiling by ROC AUC but not by log loss. On the 2,000 probes of highest variance (3 shipped splits) a logistic regression reaches a macro ROC AUC of 1.000 and a log loss of 0.11, LightGBM 0.48 and a random forest 0.80, against 4.19 for the class shares; no single probe comes close (the best one alone scores worse than the class shares). The paper's own cross-validated classifier had an error of 4.3% and an AUC of 0.99; part of the separability comes from classes drawn by clustering these profiles (label origin above).
        - Note: the arrays were hybridised in batches of 1 to 12 samples per chip (691 chips, the first part of the Sentrix id in the file names), and a class's samples often share one: 59% of the samples have a same-class chip-mate (34% of chip-mates share the class, 2% by chance), while a new patient's sample comes on a new chip. The batch shows weakly: same-class pairs correlate 0.697 on one chip and 0.656 across chips, and in the shipped splits a test sample with a same-class chip-mate in training scores a log loss of 0.97 against 1.00 without one (mean over 81 classes, lower in 58% of them; random forest on the 10,000 probes of highest variance, 3 splits). Holding out whole chips raises the log loss from 0.73 to 0.83 on the classes still in training (6 splits each), mostly because a class's samples leave training together, and leaves 9 to 29 test samples of an absent class in 4 of 6 splits. The split stays random, as in the authors' cross-validation; the chip is not shipped.
        - Note: 35 arrays of this set are also in GSE140686, the reference of the sarcoma classifier (`sarcoma_methylation_classification`), matched by chip and position: schwannoma 10, melanoma 8, solitary fibrous tumour 7, chordoma 7, Ewing sarcoma 3. They stay here; the two tasks are distinct (91 CNS classes against the sarcoma classes). They are 35 of the 40 arrays `sarcoma_methylation_classification` shares with the Capper series: the other 5 come from the validation set GSE109379, which this dataset leaves out. Both datasets keep their shared arrays; no array repeats within either one. The shared samples are GSM2403937, GSM2403951, GSM2403953, GSM2403955, GSM2403956, GSM2403957, GSM2403958, GSM2403960, GSM2403961, GSM2403962, GSM2404018, GSM2404240, GSM2404242, GSM2404250, GSM2404254, GSM2404430, GSM2404433, GSM2404434, GSM2404472, GSM2404538, GSM2404566, GSM2404610, GSM2404651, GSM2404732, GSM2404852, GSM2405070, GSM2405126, GSM2405127, GSM2405128, GSM2405183, GSM2405218, GSM2405304, GSM2405314, GSM2405370 and GSM2405632 (`SHARED_WITH_SARCOMA_METHYLATION`).
        - Note on fit: the clinic signs a sample out only at a calibrated score of 0.9 or more and otherwise reports "no match", which about 12% of the prospective cases got (the domain practitioner's figure, not checked); the reference cohort holds selected samples of 70% tumour content or more; and the age, the tumour location and the histology, which the pathologist has, are not in the data. Scores here therefore overstate the performance on routine cases.
        - Note: the IDATs (`GSE90496_RAW.tar`, 23 GB) are not downloaded; the beta file is their per-sample processing, so no step over all samples has to be undone.
    """
    splits_comment = """
        Default splits: random samples, stratified by class, as the authors' three-fold cross-validation (mnp_training, `R/makefolds.R`). One sample per patient, and the classifier types the tumours of new patients. The centres of the samples are not in the data, so the scores hold for new patients of the same centres and years. Samples hybridised on one array chip can fall on both sides. On a new chip or centre the scores are optimistic by about 10 to 15%: holding out whole chips raises the log loss from 0.73 (random folds) to 0.83 (random forest, 6 splits each; curation notes). Protocol: a model scores each test sample on its own; rebalancing a test fold's predicted probabilities to the training class shares uses the test block as a whole (log loss 0.117 to 0.108, measured by the task gamer), which a deployed classifier that types one sample at a time does not have, and a method that does this is called out (LEAK-9).
    """

    # Task
    target = "methylation_class"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "Capper et al. (2018) assess the cross-validated classifier 'by the misclassification error, multiclass "
            "area under the curve (AUC) and the multiclass Brier score' (Methods, 'Classifier performance measures'), "
            "and the authors' code (github.com/mwsill/mnp_training, CVresults.Rmd) reports the AUC, the "
            "misclassification rate, the Brier score and the log loss side by side; none is named as the criterion. "
            "The calibrated-score threshold of 0.9 decides whether a sample gets a class at all, not which class."
        ),
    )

    prepared_raw_files = PREPARED

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # Stream the 9.9 GB file once and keep the beta values only (every second column after the probe id); the
        # detection p-values are a quality measure of each probe's signal, not a methylation level.
        probes: list[str] = []
        with gzip.open(raw_dir / BETA_FILE, "rt", encoding="ascii") as f, (raw_dir / PREPARED[0]).open("wb") as out:
            header = f.readline().rstrip("\n").split("\t")
            samples = header[1::2]
            assert all(h == "Detection Pval" for h in header[2::2]), "the columns do not alternate beta / p-value"
            for line in f:
                fields = line.rstrip("\n").split("\t")
                probes.append(fields[0])
                values = fields[1::2]
                assert len(values) == len(samples), fields[0]
                out.write(np.asarray([np.nan if v in ("", "NA", "NaN") else v for v in values], dtype="<f8").tobytes())
        (raw_dir / PREPARED[1]).write_text("\n".join(probes) + "\n")
        (raw_dir / PREPARED[2]).write_text("\n".join(samples) + "\n")

    def _load_raw(self, raw_dir: Path) -> dict:
        probes = (raw_dir / PREPARED[1]).read_text().split()
        samples = (raw_dir / PREPARED[2]).read_text().strip("\n").split("\n")
        betas = np.memmap(raw_dir / PREPARED[0], dtype="<f8", mode="r", shape=(len(probes), len(samples)))
        classes = pd.read_excel(raw_dir / "GSE90496_methylationclassdescription.xlsx", dtype=str)
        return {
            "betas": betas,
            "probes": pd.Index(probes),
            "samples": pd.Index(samples),
            "annotation": series_annotation(raw_dir / "GSE90496_series_matrix.txt.gz"),
            "classes": classes,
        }

    def _clean(self, raw: dict) -> pd.DataFrame:
        annotation = raw["annotation"]
        # 1. The beta file holds the 428,799 CpG probes the authors kept, and nothing else.
        assert len(raw["probes"]) == N_PROBES_KEPT, len(raw["probes"])
        assert raw["probes"].str.startswith("cg").all()
        assert raw["probes"].is_unique
        # 2. One row per sample, in the order of the series matrix; read from disk once (probes x samples).
        columns = raw["samples"].get_indexer(annotation["beta_column"])
        assert (columns >= 0).all(), "a sample of the series matrix is not in the beta file"
        values = raw["betas"][:, columns]
        df = pd.DataFrame(values.T, columns=raw["probes"], copy=False)
        # 3. The material the DNA came from (formalin-fixed paraffin-embedded or frozen), known to the lab.
        df["material"] = annotation["material"].to_numpy()
        # 4. The target: the methylation class, in the source's words (the class description's names).
        abbreviation, name = raw["classes"].columns[:2]
        names = pd.Series(
            raw["classes"][name].str.removeprefix("methylation class ").str.strip().to_numpy(),
            index=raw["classes"][abbreviation].str.strip().to_numpy(),
        )
        target = annotation["methylation_class"].str.strip().map(names)
        assert target.notna().all(), set(annotation.loc[target.isna(), "methylation_class"])
        df[self.target] = target.to_numpy()
        # 5. No missing beta value, no constant probe and no repeated profile to handle (curation notes).
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["material"])

    def _decisions(self, raw: dict, df: pd.DataFrame) -> list[Decision]:
        annotation = raw["annotation"]
        classes = raw["classes"]
        abbreviation, relation = classes.columns[0], classes.columns[3]
        relation_of = pd.Series(
            classes[relation].fillna("control tissue").to_numpy(), index=classes[abbreviation].str.strip()
        )
        relation = (
            annotation["methylation_class"].str.strip().map(relation_of).rename("relation to WHO (class description)")
        )
        by_relation = (
            pd.crosstab(relation, annotation["material"], margins=True, margins_name="all")
            .join(annotation.groupby(relation)["methylation_class"].nunique().rename("classes"))
            .fillna({"classes": annotation["methylation_class"].nunique()})
            .astype(int)
        )
        per_class = pd.crosstab(annotation["methylation_class"], annotation["material"])
        kind = pd.Series("both materials", index=per_class.index)
        kind[per_class["Frozen"] == 0] = "FFPE only"
        kind[per_class["FFPE"] == 0] = "frozen only"
        by_material = pd.DataFrame(
            {"classes": kind.value_counts(), "samples": per_class.sum(axis=1).groupby(kind).sum()}
        ).rename_axis("material within the class")
        return [
            Decision(
                title="Target: the 91 methylation classes as published",
                why=(
                    "The reference set's class is the label of the DKFZ classifier in clinical use. The class "
                    "description relates each tumour class to the WHO classification of 2016: one to one, a subclass "
                    "of a WHO entity (mostly drawn by clustering the profiles), or not equivalent to a WHO entity; "
                    "the 9 control classes are normal or inflamed tissue."
                ),
                evidence=by_relation,
            ),
            Decision(
                title="The tissue material is a feature, though tied to the class",
                why=(
                    "The lab knows whether the DNA came from formalin-fixed paraffin-embedded or frozen tissue, and "
                    "the authors' classifier reads it to correct the values. In the reference set many classes come "
                    "from one material only."
                ),
                evidence=by_material,
            ),
        ]

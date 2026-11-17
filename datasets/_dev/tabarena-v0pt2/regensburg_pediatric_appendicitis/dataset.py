"""Curated dataset definition for `regensburg_pediatric_appendicitis` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, set_missing

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "Peritonitis": ["no", "local", "generalized"],
    "Appendicolith": ["no", "suspected", "yes"],
    "Perforation": ["no", "not excluded", "suspected", "yes"],
    "Appendicular_Abscess": ["no", "suspected", "yes"],
    "Appendix_Wall_Layers": ["intact", "partially raised", "raised"],
    "Perfusion": ["no", "hypoperfused", "present", "hyperperfused"],
}

# The precision of the measured values (curation comments): BMI was typed with two decimals for most operated children
# from 2019 on and with one for the others, the neutrophil share was a whole number more often for complicated cases,
# and ages computed from the birth date (8 decimals, against 2 when typed) mark 2016-2018.
MEASURED_PRECISION = {
    "Age": 2,
    "BMI": 1,
    "Neutrophil_Percentage": 0,
}

# The free-text findings in one spelling for every child (curation comments): the lymph-node location was abbreviated
# ("re UB") only for children not operated and spelled out ("rechter Unterbauch") only for operated ones. Applied in
# this order to the lymph-node and abscess locations.
LOCATION_SPELLINGS = (
    (r"\bre\s*UB\b", "rechter Unterbauch"),
    (r"\bre\s*MB\b", "rechter Mittelbauch"),
    (r"\bre Mittelbauch\b", "rechter Mittelbauch"),
    (r"\bUB\b", "Unterbauch"),
    (r"\bMB\b", "Mittelbauch"),
    (r"\b[Ii]leo[cz]\w*", "ileozökal"),
    (r"\bMesenterial\b", "mesenterial"),
)
# "Nothing found" was written out only for operated children; the rows of the others are blank for it.
NOTHING_FOUND = (
    "keine",
    "unauffällig",
    "kein Anhalt für eine gynäkologische Ursache der Beschwerden",
    "Ausschluss gyn. Ursache der Beschwerden",
    "Ausschluss pathologischer Ovarialbefund",
)
TEXT_COLUMNS = ["Lymph_Nodes_Location", "Abscess_Location", "Gynecological_Findings"]


class RegensburgPediatricAppendicitis(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Does a child admitted with suspected appendicitis have a complicated appendicitis (gangrenous, perforated "
            "or abscessed)?"
        ),
        use_case=(
            "For example, a paediatric surgeon, at the admission of a child with suspected appendicitis and after the "
            "examination, blood tests and ultrasound, flags the children likely to have a complicated appendicitis, "
            "to operate on them urgently and plan their care."
        ),
        row=(
            "One child admitted with abdominal pain and suspected appendicitis to the Children's Hospital St. Hedwig "
            "in Regensburg, Germany, 2016-2021, who had an ultrasound (763 children)."
        ),
        predicted=(
            "Whether the appendicitis was complicated (15.07%), as found in the tissue examination after surgery. "
            "Children treated without surgery count as uncomplicated (observed in hospital without antibiotics, they "
            "improved and did not come back), as do children without appendicitis."
        ),
        known=(
            "Age, sex, height and weight, symptoms and examination signs, body temperature, blood tests, two clinical "
            "appendicitis scores, and the ultrasound findings (appendix diameter, free fluid, wall layers, perfusion, "
            "signs of perforation or abscess, and others)."
        ),
        split=(
            "Random children, so the test data stands for other children of the same hospital and years, not for "
            "later years: the file has no dates."
        ),
        changes=(
            "We keep the children who had an ultrasound; drop the diagnosis, the surgeon's management decision, the "
            "length of stay, the ultrasound case number, rebound tenderness on the right and the three urine tests; "
            "write age, BMI and the neutrophil share at the precision of the measured values; and write two "
            "free-text findings in one spelling."
        ),
        fit="approximate",
        fit_reason=(
            "The features are known at admission, but a complicated appendicitis is only confirmed in the tissue after "
            "surgery. This hospital operates 37% of these children; the others count as uncomplicated on follow-up, "
            "which can miss a few complicated cases among mild-looking children (at most 9 of the 82 with "
            "appendicitis, by a Düsseldorf model). At Düsseldorf, which operates 81%, the authors' models reach ROC "
            "AUC 0.75 against 0.90 here."
        ),
    )

    # Dataset
    unique_name = "regensburg_pediatric_appendicitis"
    domain = "medical & healthcare"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.5281/zenodo.7711412",
            license="CC-BY-NC-4.0",
            year="2023",
            bibtex=r"""
                @article{marcinkevivcs2024interpretable,
                  title={Interpretable and intervenable ultrasonography-based machine learning models for pediatric appendicitis},
                  author={Marcinkevi{\v{c}}s, Ri{\v{c}}ards and Wolfertstetter, Patricia Reis and Klimiene, Ugne and Chin-Cheong, Kieran and Paschke, Alyssia and Zerres, Julia and Denzinger, Markus and Niederberger, David and Wellmann, Sven and Ozkan, Ece and others},
                  journal={Medical image analysis},
                  volume={91},
                  pages={103042},
                  year={2024},
                  publisher={Elsevier}
                }
            """,
        ),
    )
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        We get the newest version of the tabular data from Zenodo.


        wget https://zenodo.org/records/7711412/files/app_data.xlsx?download=1
        mkdir -p local-data-warehouse/regensburg_pediatric_appendicitis && mv app_data.xlsx?download=1 local-data-warehouse/regensburg_pediatric_appendicitis/
    """
    curation_comments = """
        We start with the tabular meta-data used in the paper. We create only one task out of the dataset using one of the three available classes. We note that the main use case of the paper was image-based modelling and comparing to tabular baselines with image-to-tabular-radiometric. The authors also published the tabular data, which we use here.

        - The data first appeared on Zenodo (v1.0, 2023-02-23, five days before the paper's preprint), hence source
          Other; UCI 938 is a copy that names the Zenodo DOI as its source.
        - Note, for this dataset is was hard to choose the label given the tabular data. We picked "Severity" in the end. "Diagnosis" is a noisy ground truth for all cases but the ones that had surgery. It was either deterministically determined by the AS score, or during surgery. "Management" reflects the decision and opinion of senior pediatric surgeon. Only "Severity" represents a ground truth as all cases that were server, were either clearly servery or did not even have appendicitis.
        - How `Severity` is set: by the tissue examination after surgery for the 284 operated children (115
          complicated; 21 of them were operated after first being treated without surgery, 3 complicated). The 479
          children not operated were observed in hospital, with ultrasound and without antibiotics, and discharged once
          they improved (Marcinkevics et al. 2021, Front Pediatr 9:662183); they count as uncomplicated when they did
          not come back, as do children without appendicitis. We read this as an outcome, not as the surgeon's
          decision: a model of the decision to operate ranks the label at ROC AUC 0.904 because surgeons operate on
          the children who look severe. Follow-up was incomplete (61 of 86 such children with appendicitis reached in
          the 2021 study), so a few complicated cases may count as uncomplicated, all in one direction. A model
          trained on the Düsseldorf cohort of the same group (Marcinkevičs, Sokol et al. 2025, Front Pediatr
          13:1587488; every child with appendicitis but one operated, so nearly every label is a tissue examination)
          is calibrated there and on Regensburg's 2016-2018 operated children (46.7 complicated expected, 51 found),
          and expects 9.0 complicated among the 82 children with appendicitis not operated, 11.7 among the 183
          without appendicitis (TabPFN 3.5; logistic regression 8.1 and 8.7). Both are upper bounds: the model cannot
          see who improved under observation, and it overshoots for mild children (Düsseldorf's own rate among
          children without appendicitis, 2 of 71, gives about 5 of the 183).
        - Leak check of the ultrasound signs closest to the label's definition (perforation, abscess and its location,
          conglomerate of bowel loops, ileus): TabPFN 3.5 reaches ROC AUC 0.935 without them and 0.939 with them
          (3-fold x 10), so they do not carry the score. This answers the earlier warning that some features might
          leak the severity.
        - The data contains string data, but only for a very small number of patients and the text is often seemingly very useless. The features add most likely no value, but we keep them in for the pipeline/model to ignore if needed.
        - We drop the few patients that did not have an ultrasound to avoid them being leaking due to missing features.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31 and 2026-11-01, CLEAN-14): 9 columns are ordered
          categories in the order of the source's codebook (`ORDINAL_LEVELS`).
        - `Appendix_Wall_Layers` (2026-10-31, CLEAN-14): the codebook's "regular / irregular" (Zenodo Data Summary); the
          labels translate the German record of the 2021 release (intact = intakt, raised = aufgehoben, the layering
          lost; partially raised = partly lost), so intact < partially raised < raised. `upset` (1 child) is irregular
          in the authors' code but of unknown degree: missing.
        - `Perfusion` (2026-10-31, CLEAN-14): the codebook's scale is the amount of blood flow (unremarkable /
          hypoperfused / hyperperfused), but this file has no `unremarkable`: the 16 children linked to the 2021
          release with `unremarkable` are blank here, so a blank also means unremarkable. `no` (no flow, 3 children)
          and `present` (flow without a grade, 1) are not in the codebook; ordered by flow as no < hypoperfused <
          present < hyperperfused, `present`'s place is our reading (the authors' code groups `no` with hypoperfused
          and `present` with hyperperfused).
        - Dropped (2026-11-16, Lennart): rebound tenderness on the right (`Ipsilateral_Rebound_Tenderness`) and the
          three urine tests (ketones, red and white cells). They are missing for none (rebound) and 18% (urine) of the
          children not operated, but for 50-59% and 30-41% of the operated ones, likely not charted when a child went
          to surgery quickly, so their gaps mark the operation. Their values add nothing: gradient boosting reaches
          ROC AUC 0.908 with them and 0.905 without (3-fold x 10). Missing values alone go from 0.804 to 0.720 on the
          label.
        - Kept: the psoas sign and dysuria (pain on urinating) follow the same pattern, smaller (missing for none of
          the children not operated, 7-12% of the operated), but dropping them changes nothing: missing values alone
          tell operated from not operated uncomplicated children at 0.748 with or without them, and gradient boosting
          reaches 0.905 without them against 0.906 with them.
        - Class-dependent recording (record marker `Class-dependent Recording`), harmonised. BMI was computed from
          weight and height (8 decimals) for most children of 2016-2018 and typed by hand later. From 2019 on it was
          typed with two decimals for 108 of 136 operated children but for 6 of 234 children treated without surgery
          (mostly one decimal), so the format marked surgery, and through it the label: BMI alone gives ROC AUC 0.56,
          with its format 0.76. The neutrophil share (neutrophils as % of white blood cells) is a whole number for 30%
          of the measured complicated cases and 15% of the others. Ages computed from the birth date (8 decimals)
          mark 2016-2018, when 12% of the children were complicated against 18% later, and the format alone gives
          0.56 on the label. All three are written at the precision every row has (`MEASURED_PRECISION`: age two
          decimals, BMI one, the neutrophil share whole percent). The number format of the float columns alone then
          gives ROC AUC 0.58 (0.77 before); the models score the same.
        - Kept: appendix diameters in half millimetres are more common in children not operated, but they come with
          smaller diameters (the diameter alone gives 0.66, with its format 0.66).
        - Kept: findings missing more often for one class. After the drops above, missing values alone give ROC AUC
          0.72 on the label and 0.75 on operated against not operated uncomplicated children. The second comes from
          the ultrasound findings (perforation, abscess, ileus, wall layers and others; the other columns alone give
          0.48), which are filled in mostly when the report describes them. The two appendicitis scores are missing
          for 12% of complicated cases against 4% of the others. Both are on the record at admission, so a model may
          use them.
        - Kept, data-entry errors in single cells: an age of 0 at 164 cm, a body temperature of 26.9 °C, a red cell
          count of 14, a haemoglobin of 36 g/dL, three RDW values of 79-87% (red cell size spread, usually 11-15%),
          and 23.7 kg at 174 cm (BMI 7.8).
        - Dropped: `US_Number`, the ultrasound case number. It runs from 1 to 440 for 2016-2018 and above for
          2019-2021, but within each period it was assigned in blocks by the children's group (of the children
          numbered 739-992, 1 of 124 was operated), so it would give the label away.
        - Free-text findings, harmonised (2026-11-16, Andrej). The lymph-node location was abbreviated ("re UB",
          "reUB", "re MB": 47 children) only for children not operated and spelled out ("rechter Unterbauch", right
          lower abdomen: 22) only for operated ones; the gynaecological finding "nothing found" ("keine",
          "unauffällig", a gynaecological cause excluded: 13 children) was written out only for operated children
          and left blank for the others. Abbreviations are written out and the spellings of ileocaecal unified, in the
          abscess location too (`LOCATION_SPELLINGS`), and "nothing found" is missing like the others' blanks
          (`NOTHING_FOUND`). The three text columns alone told operated from not operated uncomplicated children at
          ROC AUC 0.572, 0.527 after (on the label 0.552, then 0.531); the full model scores the same with or without
          them (gradient boosting 0.905 and 0.906), so no model had used the route.
        - Time basis: ForcedIIDFromTemporal (SPLIT-8): children are admitted over 2016-2021 and a deployed model scores
          later admissions, but the file has no dates; the ultrasound case numbers tell only two periods apart
          (2016-2018 and 2019-2021), too few for windows, so children are split at random (review issue 4, resolved
          2026-11-16, Andrej). Admission dates would allow a split by period.
    """
    splits_comment = """
        Default splits: stratified random 3-fold cross-validation with 10 repeats (seed 4267). Tests stand for other
        children of the same hospital and years.
        The split is forced (ForcedIIDFromTemporal): children are admitted over 2016-2021 and a deployed model scores
        later admissions, but the file has no dates. Only two periods can be told apart: ultrasound case numbers up to
        440 are 2016-2018 (every child also in the authors' 2021 study of those years has a number up to 440), higher
        ones 2019-2021; within each period the numbers follow the children's group, not the admission order (curation
        comments). Two periods give one test window, too few for a temporal split. The period matters: the complicated
        share rises from 12.0% to 18.8% (among operated children from 32% to 52%, with the share operated at 38% and
        36%), loss of appetite is recorded for 30% of the children in 2016-2018 and 77% later, and the features tell
        the two periods apart at ROC AUC 0.86. Against random splits of the same sizes, training on 2016-2018 and
        testing on 2019-2021 costs little in ranking and more in calibration: TabPFN 3.5 ROC AUC 0.931 against 0.935
        and log loss 0.290 against 0.221; logistic regression 0.887 against 0.905 and 0.377 against 0.265. Recover
        the admission dates if a later release has them.
    """

    # Task
    target = "Severity"
    problem_type = "binary_classification"
    metric = Metric.fallback(
        reason=(
            "Marcinkevics et al. 2024 report AUROC and AUPR side by side per target; neither is named as the "
            "criterion. roc_auc is the binary fallback."
        ),
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_excel(raw_dir / "app_data.xlsx?download=1", sheet_name=0)
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # Drop samples w/o utrasounds
        df = df[df["US_Performed"] == "yes"]
        df = df.drop(
            columns=[
                # Other
                "US_Performed",  # constant after dropping other cases
                "US_Number",  # case number assigned in blocks by the children's group (curation comments)
                "Length_of_Stay",  # only available at discharge (so after diagnosis)
                # Other target labels Diagnosis / Management / Severity
                "Diagnosis_Presumptive",
                "Diagnosis",
                "Management",
                # gaps mark the operation, values add nothing (curation comments)
                "Ipsilateral_Rebound_Tenderness",
                "Ketones_in_Urine",
                "RBC_in_Urine",
                "WBC_in_Urine",
            ]
        )
        # irregular wall layers of unknown degree, off the scale (CLEAN-14)
        df = set_missing(df, {"Appendix_Wall_Layers": ["upset"]})
        # The free-text findings in one spelling: the spelling followed the treatment (curation comments).
        df[TEXT_COLUMNS] = df[TEXT_COLUMNS].apply(lambda s: s.str.strip())
        for col in ("Lymph_Nodes_Location", "Abscess_Location"):
            for pattern, spelled_out in LOCATION_SPELLINGS:
                df[col] = df[col].str.replace(pattern, spelled_out, regex=True)
        df = set_missing(df, {"Gynecological_Findings": list(NOTHING_FOUND)})
        # The precision of the measured values: the number format followed the class or the period (curation comments).
        return df.round(MEASURED_PRECISION)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "Sex",
                "Peritonitis",
                "Migratory_Pain",
                "Lower_Right_Abd_Pain",
                "Contralateral_Rebound_Tenderness",
                "Coughing_Pain",
                "Psoas_Sign",
                "Nausea",
                "Loss_of_Appetite",
                "Dysuria",
                "Stool",
                "Neutrophilia",
                "Appendix_on_US",
                "Free_Fluids",
                "Appendix_Wall_Layers",
                "Target_Sign",
                "Perfusion",
                "Surrounding_Tissue_Reaction",
                "Pathological_Lymph_Nodes",
                "Bowel_Wall_Thickening",
                "Ileus",
                "Coprostasis",
                "Meteorism",
                "Enteritis",
                "Appendicolith",
                "Perforation",
                "Appendicular_Abscess",
                "Conglomerate_of_Bowel_Loops",
            ],
            string=["Lymph_Nodes_Location", "Abscess_Location", "Gynecological_Findings"],
        )

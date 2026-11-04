"""Annual Tunisian tax-adjustment regression. Evidence: README.md; curator decisions are recorded below."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary, Temporal, TemporalSplits

ZERO_WITH_BLOCK_MISSINGNESS = (
    "TVA_CAF125",
    "TVA_CHAF36",
    "TVA_CRDREP",
    "TVA_MTORDTAX",
    "TVA_MTDJRTAX",
    "TVA_MTRESTAX",
    "SND_MNTAVA_I",
    "SND_MNTTVA_E",
    "SND_MNTDRC_E",
    "SND_MNTAVA_E",
    "SND_MNTAIR_E",
    "SND_MNTAVA_A",
)


class TunisianFraudDetectionChallenge(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How well can a model estimate an archived taxpayer-year dossier's principal tax adjustment to identify records worth further investigation?",
        use_case=(
            "For example, a Tunisian tax-control analyst looks back over archived annual returns and administrative "
            "cross-checks to prioritize records for further investigation using estimated logged adjustment severity. "
            "The scored adjustment is withheld; this retrospective exercise does not reproduce a model refit at each fiscal-year start."
        ),
        row="One anonymized taxpayer-year in the supplied Ministry of Finance challenge training release: 21,295 rows of fiscal years 2013–2018, of which the 20,930 of 2013–2017 ship (2018 is cut).",
        predicted="The source-provided log(1 + principal tax adjustment) label. Penalties are not the target. Underlying currency denomination is unspecified.",
        known="Taxpayer legal/activity/obligation categories, filed VAT amounts and credits, customs/government-payment aggregates, and third-party income/invoice cross-checks, as supplied in the contest dossier. Registry/refund revisions and historical extraction cutoffs remain unverified.",
        split="Train on every observed earlier fiscal year and test on 2017, 2016 and 2015 separately. Both recurring and newly observed taxpayers occur. This measures transfer to later fiscal cohorts using retrospective training labels; it does not date audit completion or reproduce past operational refits.",
        changes="Cut fiscal year 2018 (365 rows), whose inspections were still open at the extract; keep the other labeled rows and supplied targets. Remove row/taxpayer identifiers, duplicate fiscal year, twelve zero-with-block-missingness columns and two exact financial copies. Cast codes as categories and fiscal year as datetime.",
        fit="approximate",
        fit_reason="The original supervision task and annual dossiers are documented; Myunghwan accepts retrospective investigation. Exact feature extraction, inspection selection and audit/label-availability dates are absent. This historical cohort comparison does not establish causal deployment, all-taxpayer screening yield, or recovered money per inspection.",
    )
    unique_name = "tunisian_fraud_detection_challenge"
    year = "2019"
    domain = "finance"
    source = "Zindi"
    source_url = "https://zindi.world/competitions/tunisian-fraud-detection"
    license = "Zindi competition rules; redistribution restricted"
    download_description = """
        Obtain the authorized Train.csv and VariableDescription.csv from
        https://zindi.world/competitions/tunisian-fraud-detection/data (login; Lennart's download of 2026-11-04 is
        byte-identical to the participant mirrors' SupCom copy: Train.csv SHA-256
        8946058bd60847cf49eb372963d05f47022c1fb820ab323227304a88aa0faa02, VariableDescription.csv SHA-256
        763bfdfe8774643eb3342b3e2c0935801f81c545ea9908bb64174195092b81f8) and place them in
        local-data-warehouse/tunisian_fraud_detection_challenge/. The supplied named files were preserved byte-for-byte
        under these canonical names; SOURCE_MANIFEST.json records identities. Only Train.csv supplies benchmark rows and labels. A separate private test-file inspection informs the predictor schema; no test rows or submission labels enter this definition.
        The related Sup'Com challenge is a later rerun of this source family, not another independent dataset.
    """
    bibtex = """
        @misc{tunisian2019fraud,
          title={Tunisian Fraud Detection Challenge},
          author={{Tunisian Ministry of Finance} and {Zindi}},
          year={2019},
          url={https://zindi.world/competitions/tunisian-fraud-detection}
        }
    """
    curation_comments = """
        - CC (2026-10-31, Myunghwan): Accepted all remaining choices: the dataset for a later requested build, both annual-time warning reasons, and Temporal (NON-IID) metadata. Temporal evaluation is preferred as closer to scanning a new year. Six annual markers constrain inner validation; January 1 represents each fiscal cohort, not event dates. Preserve the accepted retrospective scope and unknown historical availability.
        - CC (2026-10-31, Myunghwan): Retrospective prediction is acceptable: looking back can identify more records worth investigating. An analyst uses archived annual dossiers with the scored adjustment withheld and historical training labels already held. This does not claim that a model was fitted at the beginning of each fiscal year. The release has no extraction, inspection, notification or label-availability dates; original timing and revisions remain unverified. This settled the retrospective task framing; final inclusion was subsequently accepted on 2026-10-31.
        - Train.csv has 21,295 unique taxpayer-years from 12,387 IDs over 2013–2018. Keep every label unchanged: log(1 + principal adjustment), as described in challenge discussion 448, including 5,402 zeros, no missing/negative labels and range 0–23.5913. Dictionary RES_MNTRED names the principal target; excluded penalty RES_MNTRET is not a predictor. Zero does not establish a completed negative inspection, legal intent or national prevalence. The underlying currency unit and cohort-selection mechanism are unknown.
        - Source RMSE scores the supplied log labels. target_transform is identity because this recipe applies no transform; no inverse or second log is used. This score is not monetary RMSE, recovered revenue or net benefit per audit. The later Sup'Com release belongs to the same source family, not an independent dataset.
        - Fiscal year 2018 is cut (LEAK-24; Lennart, 2026-11-04: "do the change"): its nonzero adjustments have a median 1.2 log units below 2013-2017 (about 3 times smaller, Mann-Whitney p = 6e-16), within every taxpayer category, and leak probe 13 puts it out of band (median z -6.7), while 2017 is in band (p = 0.8). It fits inspections still open at the 2019 extract. Its three 2018-form VAT rate columns (`TVA_CA072018`, `TVA_CA132018`, `TVA_CA192018`) are constant without it and leave. The use case stays the retrospective ranking of inspected dossiers (Lennart: "okay let us keep it").
        - Retrospective evaluation uses three annual tests, newest first: 2017/2016/2015 with train/test counts 19,301/1,629; 16,201/3,100; 11,833/4,368. Earlier windows fail the half-release training floor. January 1 represents fiscal-year cohorts, not actual event dates. Fiscal order tests transfer across accounting cohorts, not historical model-refit feasibility. No delay is invented from a model score; if a past operational refit is later claimed, outcome availability must be established and the protocol reassessed.
        - Drop id and CTR_MATFIS as administrative identifiers, RES_ANNIMP as an exact fiscal-year copy, twelve zero-when-observed columns whose block-missingness survives elsewhere, TVA_ACHNDD as a copy of TVA_ACHSUS, and SND_MNTPAY_E as a copy of SND_MNTTAX_E. No row is filtered; retained values and NaNs are not imputed, clipped or rescaled. No taxpayer/label aggregates are constructed.
        - Tax office, taxpayer category, legal form, activity and obligation/status codes are categorical; obligations are not all binary. Retain the 63 undocumented CTR_CESSAT code-2 rows as an uninterpreted category; CTR_RATISS codes 0/2 are not decoded. Months 1–12 stay numeric. Customs/invoice block missingness is not universally no activity. SND_MNTAIR_I/A are undefined in the dictionary and TVA_CRDFIN has an inconsistent initial-credit description.
        - Contest input check: a participant-maintained SupCom mirror has 7,517 test rows and all 120 raw non-target columns in training order; its training Git blob exactly matches the supplied Train.csv. All 103 retained predictors are present and none is wholly missing in test. Refund/regularization fields contain observed nonzero test values. Target alone is absent; this yields no further schema-based exclusion. Zero-when-observed removals describe the labeled benchmark release, not universal constants: TVA_CRDREP varies in the contest test file. The test covers every fiscal year 2013–2018, so our four annual holdouts are a separate cross-cohort evaluation, not the contest holdout. The original host test download was not authenticated. Test presence is an input contract, not evidence of historical as-of timing or freedom from outcome-derived revisions.
        - Potential leak, kept on purpose: refund/regularization amounts and registry fields may reflect later revisions or verification. All 23 registry fields are invariant across 5,990 repeated taxpayers. The historical declaration form contains corresponding VAT items, some qualified for corrective declarations; statutory refund processes differ. All twelve raw process-field missing masks equal ordinary VAT-return availability (1,690 absent), also within zero/positive-label strata. That refutes an additional conditional blank/fill mechanism, not revisions to observed values. Retain host-released anonymized inputs under LEAK-38 while timing is untestable; revisit on original/as-of returns, audit/extract/notification dates or a measured same-outcome recording mechanism. A confirmed leak requires repair/drop regardless of ablation score.
        - Retain seven excess full-row copies and nineteen excess conflicting-label variants: they are distinct taxpayer-years with sparse financial profiles, within the same fiscal cohort. Thirty-one rows participate in conflicting feature groups. No full-feature copy including fiscal year crosses a cutoff; copies after removing time can be natural recurring profiles and are separately measured. Do not deduplicate different taxpayers or infer independent audit appointments. The shrinking latest cohort (365 rows) and missing-data coverage limit broad generalization.
    """
    accepted_check_warnings = {
        "task_time_on_few_unique": "Only six genuine fiscal-year cohorts exist; four outer windows meet the training floor. Validation must respect the available annual support; finer timestamps are unavailable.",
        "meta_time_horizon_mismatch": "Every row is an annual cohort represented at January 1; the one-year horizon denotes the calendar cohort, while observed timestamp span is one point. No daily sampling or audit-duration claim is made.",
    }
    target = "target"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="Root Mean Square Error on the supplied target",
        reference="https://zindi.africa/competitions/tunisian-fraud-detection/discussions/436",
    )
    temporal = Temporal(
        on="fiscal_year",
        splits=TemporalSplits(window=1, unit="years", cutoffs=(2015, 2016, 2017)),
    )
    splits_comment = """
        Three one-calendar-year cohort windows, newest first: 2017, 2016, 2015 (fiscal year 2018 is cut, LEAK-24). Each model trains on every observed
        earlier fiscal cohort using retrospective training labels, with the scored cohort labels withheld. January 1 represents an annual
        accounting cohort, not a verified audit date. Both known and new taxpayers occur in this retrospective investigation
        setting. These are fiscal-cohort transfer tests, not models refitted at historical year starts. Audit-completion
        dates remain unavailable; historical point-in-time label maturity is unverified, not assumed.
        One year is the evaluation-window duration, not a promised one-year inspection or adjustment horizon.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_csv(raw_dir / "Train.csv")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        assert df.shape == (21295, 121)
        assert df["id"].is_unique
        assert not df.duplicated(["CTR_MATFIS", "EXE_EXERCI"]).any()
        assert df["target"].notna().all()
        assert df["target"].ge(0).all()
        assert df["RES_ANNIMP"].equals(df["EXE_EXERCI"])
        assert df["TVA_ACHNDD"].equals(df["TVA_ACHSUS"])
        assert df["SND_MNTPAY_E"].equals(df["SND_MNTTAX_E"])
        for column in ZERO_WITH_BLOCK_MISSINGNESS:
            assert df[column].dropna().eq(0).all()
            assert any(
                df[column].isna().equals(df[other].isna())
                for other in ("TVA_TOTDUE", "SND_MNTPRD_I", "SND_MNTPRD_E", "SND_MNTPRD_A")
            )
        df = df.drop(
            columns=["id", "CTR_MATFIS", "RES_ANNIMP", "TVA_ACHNDD", "SND_MNTPAY_E", *ZERO_WITH_BLOCK_MISSINGNESS]
        )
        # Fiscal year 2018 holds the inspections closed before the 2019 extract: about 3 times smaller adjustments,
        # out of band in leak probe 13 (LEAK-24; Lennart, 2026-11-04).
        df = df.loc[df["EXE_EXERCI"].ne(2018)]
        # Three VAT rates of the 2018 return form are filled only in fiscal 2018, so they are constant without it.
        df = df.drop(columns=["TVA_CA072018", "TVA_CA132018", "TVA_CA192018"])
        df["EXE_EXERCI"] = pd.to_datetime(df["EXE_EXERCI"].astype("string"), format="%Y")
        return df.rename(columns={"EXE_EXERCI": "fiscal_year"})

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[c for c in df if c.startswith("CTR_") or c in ("BCT_CODBUR", "FJU_CODFJU", "ACT_CODACT")],
            datetime=["fiscal_year"],
        )

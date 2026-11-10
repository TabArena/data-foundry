"""Annual Tunisian tax-adjustment regression. Evidence: README.md; curator decisions are recorded below."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, Source, TaskSummary, Temporal, TemporalSplits

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
            "For example, a Tunisian tax-control analyst looks back over the archived annual dossiers of inspected "
            "taxpayers and ranks past fiscal years for further investigation by estimated logged adjustment. In-depth "
            "verifications cover several open years, so ranking past years is the decision itself. The scored adjustment "
            "is withheld; the taxpayer's adjustments of earlier years are held history."
        ),
        row="One taxpayer-year (taxpayer id removed) in the supplied Ministry of Finance challenge training release: 21,295 rows of fiscal years 2013–2018, of which the 20,930 of 2013–2017 ship (2018 is cut).",
        predicted="The source-provided log(1 + principal tax adjustment) label. Penalties are not the target. Underlying currency denomination is unspecified.",
        known="Taxpayer legal/activity/obligation categories (looked up at extraction), filed VAT amounts and credits, customs/government-payment aggregates and third-party income/invoice cross-checks, as supplied in the contest dossier; plus the taxpayer's adjustment in its most recent earlier fiscal year in the data and the years since it. Refund revisions and historical extraction cutoffs remain unverified.",
        split="Train on every earlier fiscal year and test on 2017, 2016 and 2015 separately. 64-75% of test rows have an earlier year of the same taxpayer, whose label is always on the training side. This measures ranking a later fiscal cohort with the held history; it does not date audit completion or reproduce past operational refits.",
        changes="Cut fiscal year 2018 (365 rows): its adjustments are about 3 times smaller, most likely inspections still open at the 2019 extract. Add the taxpayer's previous adjustment and the years since it; remove the identifiers, the duplicate fiscal year, twelve zero-with-block-missingness columns, two exact copies, the cessation status (looked up at extraction) and the VAT refund paid (its fill differs by outcome). Codes are categories.",
        fit="approximate",
        fit_reason="Retrospective investigation of documented annual dossiers. Every row is an inspected taxpayer-year, so the uninspected filers a real screening ranks are never seen (selection). Audit dates are absent, so when a previous adjustment became known is not dated. Kept on purpose: the refund and regularisation fields (`TVA_MTORDTVA`, `TVA_MTDJRTVA`, `TVA_DEDREG`, `TVA_CRDBLQ`, `TVA_CRDRES`, `TVA_CRDRMP`, `TVA_CRDRMC`) and 22 registry fields looked up at extraction.",
    )
    unique_name = "tunisian_fraud_detection_challenge"
    domain = "finance"
    sources = (
        Source(
            role="publication",
            platform="Zindi",
            url="https://zindi.world/competitions/tunisian-fraud-detection",
            license="Zindi competition rules; redistribution restricted",
            year="2019",
            bibtex="""
                @misc{tunisian2019fraud,
                  title={Tunisian Fraud Detection Challenge},
                  author={{Tunisian Ministry of Finance} and {Zindi}},
                  year={2019},
                  url={https://zindi.world/competitions/tunisian-fraud-detection}
                }
            """,
        ),
    )
    download_description = """
        Obtain the authorized Train.csv and VariableDescription.csv from
        https://zindi.world/competitions/tunisian-fraud-detection/data (login) and place them in
        local-data-warehouse/tunisian_fraud_detection_challenge/. Expected SHA-256: Train.csv
        8946058bd60847cf49eb372963d05f47022c1fb820ab323227304a88aa0faa02, VariableDescription.csv
        763bfdfe8774643eb3342b3e2c0935801f81c545ea9908bb64174195092b81f8. The working copy was fetched on 2026-11-04
        from a public participant mirror (github.com/MohamedNennouche/Tunisian-Fraud-Detection, SUPCOM_Train.csv saved
        as Train.csv; MIRROR_SOURCE.txt beside the files says so); its identity with the Zindi file rests on Lennart's
        statement that his Zindi download of 2026-11-04 is byte-identical. Only Train.csv supplies benchmark rows and labels. A separate private test-file inspection informs the predictor schema; no test rows or submission labels enter this definition.
        The related Sup'Com challenge is a later rerun of this source family, not another independent dataset.
    """
    curation_comments = """
        - CC (2026-10-31, Myunghwan): Accepted all remaining choices: the dataset for a later requested build, both annual-time warning reasons, and Temporal (NON-IID) metadata. Temporal evaluation is preferred as closer to scanning a new year (superseded 2026-11-05: the task is the retrospective ranking of past fiscal years, with the taxpayer's earlier adjustments as held history; issue 1 CC below). Six annual markers (five since the 2018 cut of 2026-11-04) constrain inner validation; January 1 represents each fiscal cohort, not event dates. Preserve the accepted retrospective scope and unknown historical availability.
        - CC (2026-10-31, Myunghwan): Retrospective prediction is acceptable: looking back can identify more records worth investigating. An analyst uses archived annual dossiers with the scored adjustment withheld and historical training labels already held. This does not claim that a model was fitted at the beginning of each fiscal year. The release has no extraction, inspection, notification or label-availability dates; original timing and revisions remain unverified. This settled the retrospective task framing; final inclusion was subsequently accepted on 2026-10-31.
        - Train.csv has 21,295 unique taxpayer-years from 12,387 IDs over 2013–2018. Keep every label unchanged: log(1 + principal adjustment), as described in challenge discussion 448, including 5,402 zeros, no missing/negative labels and range 0–23.5913. Dictionary RES_MNTRED names the principal target; excluded penalty RES_MNTRET is not a predictor. Zero does not establish a completed negative inspection, legal intent or national prevalence. The underlying currency unit and cohort-selection mechanism are unknown.
        - Source RMSE scores the supplied log labels. target_transform is identity because this recipe applies no transform; no inverse or second log is used. This score is not monetary RMSE, recovered revenue or net benefit per audit. The later Sup'Com release belongs to the same source family, not an independent dataset.
        - Fiscal year 2018 is cut (LEAK-24; Lennart, 2026-11-04: "do the change"): its nonzero adjustments have a median 1.2 log units below 2013-2017 (about 3 times smaller, Mann-Whitney p = 6e-16), within every taxpayer category, and leak probe 13 puts it out of band (median z -6.7), while 2017 is in band (p = 0.8). It fits inspections still open at the 2019 extract. 2017 stays (review panel, 2026-11-04): zero share 0.249 (2013-2016: 0.236-0.265), nonzero median 15.72 against 15.80 (p = 0.36), and a gradient-boosting mean residual of +0.18, like 2016's, against -0.71 for 2018. Its smaller count (ratio 0.53 to 2016, after 0.95, 0.76 and 0.71) continues a steady fall, so probe 13's count z of -4.6, measured against a flat band, is row selection, not label censoring; the 2017 test cohort holds the inspections that closed fastest. 2013 is left-truncated (45% of its taxpayers have no other year; leave-one-year-out residual -0.41) and is only ever training data (SPLIT-20). Its three 2018-form VAT rate columns (`TVA_CA072018`, `TVA_CA132018`, `TVA_CA192018`) are constant without it and leave. The use case stays the retrospective ranking of inspected dossiers (Lennart: "okay let us keep it").
        - Retrospective evaluation uses three annual tests, newest first: 2017/2016/2015 with train/test counts 19,301/1,629; 16,201/3,100; 11,833/4,368. Earlier windows fail the half-release training floor. January 1 represents fiscal-year cohorts, not actual event dates. Fiscal order tests transfer across accounting cohorts, not historical model-refit feasibility. No delay is invented from a model score; if a past operational refit is later claimed, outcome availability must be established and the protocol reassessed.
        - Drop id and CTR_MATFIS as administrative identifiers (superseded 2026-11-05: CTR_MATFIS first builds the two history features, then leaves; LEAK-33), RES_ANNIMP as an exact fiscal-year copy, twelve zero-when-observed columns whose block-missingness survives elsewhere, TVA_ACHNDD as a copy of TVA_ACHSUS, and SND_MNTPAY_E as a copy of SND_MNTTAX_E. No row is filtered besides fiscal 2018; retained values and NaNs are not imputed, clipped or rescaled. No taxpayer/label aggregates are constructed (superseded 2026-11-05: the previous adjustment and the years since it, issue 1 CC below).
        - Tax office, taxpayer category, legal form, activity and obligation/status codes are categorical; obligations are not all binary. CTR_RATISS ("ratissage", a control sweep) codes 0/2 are not decoded; FJU_CODFJU 99 (48.8% of rows) is undocumented and kept as a level. Months 1–12 stay numeric. Customs/invoice block missingness is not universally no activity. SND_MNTAIR_I/A are undefined in the dictionary. TVA_CRDFIN is the closing VAT credit, although the dictionary repeats "Crédit Initial": it carries over to the next year's TVA_CRDINI in 89.9% of 6,180 consecutive-year pairs.
        - Contest input check: a participant-maintained SupCom mirror has 7,517 test rows and all 120 raw non-target columns in training order; its training Git blob exactly matches the supplied Train.csv. All retained host predictors (100 inputs with fiscal_year after the 2018 cut, 98 since `CTR_CESSAT` and `TVA_RESTIT` left on 2026-11-05; the two history features added that day are ours) are present and none is wholly missing in test. Refund/regularization fields contain observed nonzero test values. Target alone is absent; this yields no further schema-based exclusion. Zero-when-observed removals describe the labeled benchmark release, not universal constants: TVA_CRDREP varies in the contest test file. The test covers every fiscal year 2013–2018, so our three annual holdouts are a separate cross-cohort evaluation, not the contest holdout. The original host test download was not authenticated. Test presence is an input contract, not evidence of historical as-of timing or freedom from outcome-derived revisions.
        - Potential leak, kept on purpose: refund/regularization amounts and registry fields may reflect later revisions or verification. All 23 registry fields are invariant across 5,990 repeated taxpayers. The historical declaration form contains corresponding VAT items, some qualified for corrective declarations; statutory refund processes differ. All twelve raw process-field missing masks equal ordinary VAT-return availability (1,690 absent), also within zero/positive-label strata. That refutes an additional conditional blank mechanism, not revisions to observed values. The registry snapshot includes CTR_RATISS (control sweep; 233 rows, R² about 0.001); CTR_CESSAT (cessation status) left on 2026-11-05. A fill test (filing-time covariates, 5 folds grouped by taxpayer; review panel, 2026-11-04) finds TVA_MTDJRTVA and TVA_MTORDTVA miscalibrated alike for zero and positive labels (observed/predicted 4.03 against 3.61; 14.8 against 12.7 on 22 filled rows), while TVA_RESTIT's fill differs by label (1.30 against 1.03), the revisit trigger below, so it left on 2026-11-05; dropping all three refund fields costs +0.022 RMSE. Only the taxpayer id was replaced, so the columns keep their names (Lennart, 2026-11-04). Retain these host-released inputs under LEAK-38 while timing is untestable (superseded 2026-11-05 for the 22 registry fields that stay: looked up at extraction, their timing is known, so LEAK-10 decides, and they stay because no mechanism ties a registry change to the adjustment, unlike `CTR_CESSAT`; issue 5 CC below). The refund and regularisation fields (`TVA_MTORDTVA`, `TVA_MTDJRTVA`, `TVA_DEDREG`, `TVA_CRDBLQ`, `TVA_CRDRES`, `TVA_CRDRMP`, `TVA_CRDRMC`) stay under LEAK-38 as amended on 2026-11-05 (host-released fields, anonymised or named, whose timing cannot be tested) and are named in `fit_reason` as kept (USE-8); revisit on original/as-of returns, audit/extract/notification dates or a measured same-outcome recording mechanism. A confirmed leak requires repair/drop regardless of ablation score.
        - CC (2026-11-05, Lennart): drop `CTR_CESSAT` (issue 2, option B; LEAK-10, attributes looked up after the outcome leave whatever their size): every registry field is constant within a taxpayer, so the cessation status was looked up at extraction, and a firm that ceased later carries "ceased" on all its earlier years (ceased share 5.5% in 2013, 2.7% in 2017; ceased rows' mean target 10.06 against 11.88). Dropping it costs +0.015 RMSE (3 windows by 2 seeds), below the ±0.03 noise per split.
        - CC (2026-11-05, Lennart): drop `TVA_RESTIT`, the VAT refund paid (issue 3, option B; LEAK-38's own clause, then LEAK-10; as kick and expresso_churn_prediction, 2026-10-22): a fill model on filing-time covariates (5 folds grouped by taxpayer) gives observed/predicted 1.30 on zero-adjustment rows against 1.03 on positive ones (95% interval of the gap 0.026-0.042), so whether a refund was paid depends on the outcome; a plausible mechanism is a refund paid after a verification that found nothing. `TVA_MTORDTVA` and `TVA_MTDJRTVA` stay under LEAK-38: miscalibrated alike for both labels.
        - CC (2026-11-05, Lennart): the taxpayer's earlier adjustments are held history (issue 1, option B; USE-10, LEAK-34, as corporate_credit_rating's previous rating and ieee_fraud_detection's `uid`). `previous_target` is the target of the taxpayer's most recent earlier fiscal year in the data and `years_since_previous_target` the years since it (1-4); both are missing for 58.5% of rows (every 2013 row; 25.4%, 28.7% and 36.4% of the 2017, 2016 and 2015 test rows). `_clean` builds them from `CTR_MATFIS` over strictly earlier years, then drops the id (LEAK-33). On the shipped windows every test row with a previous label (1,216, 2,210 and 2,776) takes it from a training row, none from its own window. What sets this apart from lt_vehicle_loan_default_prediction, moved to the decision at disbursement on 2026-11-04: Tunisian in-depth verifications cover several open years (Ministère des Finances FAQ, https://www.finances.gov.tn/fr/faq?page=3), so ranking past years is the real decision, while a loan cannot be approved after the fact. LightGBM (the panel's settings, 3 windows by 2 seeds): mean RMSE 6.021 to 5.476 with the codes as numbers, as the panel ran it (5.996 to 5.462 on 2026-11-04, before `CTR_CESSAT` and `TVA_RESTIT` left), and 5.863 to 5.533 with the shipped categories; the dummy scores 7.056. Two doubts stay on record: the late 2018 labels (2018 is cut) show that a year's label can arrive after the next year is inspected, and the hole test (0.794 vs 0.803) that leans against one inspection settling several years is circumstantial (EV-6). Gap 0 stays under SPLIT-10 as amended: the late labels are recorded, and the earlier years' labels are held history in this framing.
        - CC (2026-11-05, Lennart): the refund and regularisation fields stay under LEAK-38 as amended the same day (issue 5, option B), whose scope is host-released fields, anonymised or named, whose timing cannot be tested; they are named in `fit_reason` as kept (USE-8). The 22 registry fields that stay were looked up at extraction, so LEAK-10 decides, not LEAK-38: they stay because no mechanism ties a registry change to the adjustment, unlike `CTR_CESSAT`, dropped (choice a of the consistency check; a LEAK-10 Cases row in leak_checks.md).
        - Retain seven excess full-row copies and twenty-one conflicting-label rows (nineteen before `CTR_CESSAT` and `TVA_RESTIT` left on 2026-11-05): they are distinct taxpayer-years with sparse financial profiles, within the same fiscal cohort. Thirty-one rows participate in conflicting feature groups. Since the two history features of 2026-11-05: five excess copies, eleven conflicting-label rows, twenty rows in nine conflicting feature groups. No full-feature copy including fiscal year crosses a cutoff; copies after removing time can be natural recurring profiles and are separately measured. Do not deduplicate different taxpayers or infer independent audit appointments. The shrinking latest cohort (2017, 1,629 rows) and missing-data coverage limit broad generalization.
        - Taxpayer history across the cutoff (review panel, 2026-11-04; settled 2026-11-05, issue 1 CC below): 64-75% of test rows have their taxpayer in training, and the 23 registry columns shipped then (22 since `CTR_CESSAT` left), invariant within a taxpayer, single out 59.6% of the 12,244 taxpayers on their own although CTR_MATFIS is dropped. Removing the test taxpayers' training rows costs +0.12 to +0.19 RMSE beyond a size-matched removal (3 windows, LightGBM); a participant who links taxpayers and uses their earlier labels gains 0.25-0.56. Consecutive-year labels agree on zero vs nonzero for 86% of pairs (62% if independent), and two years the same distance apart agree as much when the year between them is missing from the data as when it is present (0.794 vs 0.803 two years apart), which fits persistent taxpayer behaviour more than one inspection settling several years; no audit dates exist to settle it.
        - The score: 56-60% of the squared error (HistGradientBoosting, test years 2015-2017) comes from the true zeros, 25% of rows, so RMSE on the log label mostly rewards telling whether an inspection finds anything, not the size of the adjustment.
    """
    accepted_check_warnings = {
        "task_time_on_few_unique": "Only five genuine fiscal-year cohorts exist (2018 is cut); three outer windows meet the training floor. Validation must respect the available annual support; finer timestamps are unavailable.",
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
        Three one-calendar-year cohort windows, newest first: 2017, 2016, 2015 (fiscal year 2018 is cut, LEAK-24). Each
        model trains on every earlier fiscal cohort with its labels, which the retrospective analyst holds, and the
        scored cohort's labels are withheld. The previous adjustment reads only strictly earlier years of the same
        taxpayer, so for every test row that has one (1,216, 2,210 and 2,776 rows) it comes from a training row, never
        from its own window. January 1 represents an annual accounting cohort, not a verified audit date. These windows
        test the ranking of a later fiscal cohort, not models refitted at historical year starts; audit-completion dates
        are unavailable, and the 2018 cut shows that labels arrive late, so when a previous label became known is not
        established. One year is the evaluation-window duration, not a promised one-year inspection or adjustment
        horizon. The source's own test file spans every fiscal year 2013-2018 and its labels were never released, so
        its split cannot be followed (SPLIT-19); these windows are our own.
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
        df = df.drop(columns=["id", "RES_ANNIMP", "TVA_ACHNDD", "SND_MNTPAY_E", *ZERO_WITH_BLOCK_MISSINGNESS])
        # The cessation status was looked up at extraction (constant within a taxpayer), and the refund paid has a fill
        # that differs by outcome: both leave (LEAK-10, LEAK-38; Lennart, 2026-11-05).
        df = df.drop(columns=["CTR_CESSAT", "TVA_RESTIT"])
        # Fiscal year 2018 holds the inspections closed before the 2019 extract: about 3 times smaller adjustments,
        # out of band in leak probe 13 (LEAK-24; Lennart, 2026-11-04).
        df = df.loc[df["EXE_EXERCI"].ne(2018)]
        # Three VAT rates of the 2018 return form are filled only in fiscal 2018, so they are constant without it.
        df = df.drop(columns=["TVA_CA072018", "TVA_CA132018", "TVA_CA192018"])
        # The analyst holds the taxpayer's earlier adjustments (USE-10, LEAK-34; Lennart, 2026-11-05): the label of its
        # most recent earlier fiscal year in the data and the years since it. Only strictly earlier years enter, so
        # with one-year test windows the source row is always on the training side. The id itself never ships (LEAK-33).
        earlier = (
            df.sort_values(["CTR_MATFIS", "EXE_EXERCI"], kind="stable")
            .groupby("CTR_MATFIS")[["target", "EXE_EXERCI"]]
            .shift()
        )
        df["previous_target"] = earlier["target"]
        df["years_since_previous_target"] = df["EXE_EXERCI"] - earlier["EXE_EXERCI"]
        assert df["years_since_previous_target"].dropna().ge(1).all()
        df = df.drop(columns=["CTR_MATFIS"])
        df["EXE_EXERCI"] = pd.to_datetime(df["EXE_EXERCI"].astype("string"), format="%Y")
        return df.rename(columns={"EXE_EXERCI": "fiscal_year"})

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[c for c in df if c.startswith("CTR_") or c in ("BCT_CODBUR", "FJU_CODFJU", "ACT_CODACT")],
            datetime=["fiscal_year"],
        )

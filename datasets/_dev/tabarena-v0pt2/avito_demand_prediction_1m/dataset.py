"""Curated dataset definition for `avito_demand_prediction_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

TARGET = "deal_probability"
LAST_DAY = pd.Timestamp("2017-03-28")  # the last posting day of the release; 100 ads carry later dates


class AvitoDemandPrediction1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How likely is a new classified ad on Avito to end in a deal, on Avito's own 0-1 score?",
        use_case=(
            "When a seller posts an ad on Avito, a Russian classifieds site, Avito estimates the demand the ad will "
            "meet, so the seller knows how much interest to expect (competition overview). The overview also names "
            "advice on how to improve the listing; the benchmark does not test that, which needs effects rather than "
            "associations (ads without a price score 0.215 against 0.135)."
        ),
        row=(
            "One ad posted on Avito from 15 to 28 March 2017 (the competition's training file of 1.5 million ads) in "
            "28 Russian regions, without Moscow, St Petersburg or their oblasts, and in 9 parent categories, without "
            "jobs; with the ad's text, price, place, category, photo class and seller."
        ),
        predicted=(
            "Avito's deal probability for the ad, a number from 0 to 1 that Avito calls the likelihood that the ad "
            "sold something; 65% of the ads have 0. How Avito computes it is not published."
        ),
        known=(
            "The ad as posted: Russian title and description, price, region and city, Avito's category and form "
            "parameters, Avito's class of the main photo, the posting date, and the seller's anonymous id, type and "
            "ad count."
        ),
        split=(
            "Each test window is two days of the last six (23 to 28 March 2017); training is the ads posted before "
            "it (a random million of them for the two newer windows, all 861,064 for the oldest), as for a model "
            "refit every two days."
        ),
        changes=(
            "We drop the ad and image ids and the 100 ads dated after 28 March; the unlabelled ads, the photos and "
            "the competition's test file are not used."
        ),
        fit="approximate",
        fit_reason=(
            "Everything the model sees is known at posting, and the windows follow the posting date. The gaps: the "
            "label is Avito's undocumented assessment of a deal it cannot observe (USE-5), not views or contacts; "
            "the model lacks some of Avito's context (competing ads, all photos, promotion); and the windows have no "
            "gap, as a gap of the label's delay (weeks) leaves a training side under half the ads."
        ),
    )

    # Dataset
    unique_name = "avito_demand_prediction_1m"
    version_of = "avito_demand_prediction"
    version_comment = """
        We sample per test window (v2 split protocol): each two-day window keeps all of its ads (204k to 228k, under the 500k cap), and its train side is a random 1M of all earlier ads, drawn in one random order for all windows (the oldest window's 861k earlier ads are all kept); the frame keeps only the rows a split uses.
    """
    year = "2018"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/avito-demand-prediction"
    license = "Kaggle Competition Rules"
    data_tags = ("Spatial",)
    download_description = """
        The training file of the Kaggle competition "Avito Demand Prediction Challenge" (Avito, 2018); the rules must
        be accepted on the competition page first. train.csv.zip (333,463,334 bytes, sha256
        413b789192c0d39532260f801eb744e84daff5ade0694730ca18caccf795d43f) holds train.csv (952,929,135 bytes). The
        unlabelled test file, the supplementary ads (train_active, test_active, periods_*) and the photos are not used.

        mkdir -p local-data-warehouse/avito_demand_prediction
        kaggle competitions download -c avito-demand-prediction -f train.csv -p local-data-warehouse/avito_demand_prediction
        unzip local-data-warehouse/avito_demand_prediction/train.csv.zip -d local-data-warehouse/avito_demand_prediction
    """
    bibtex = r"""
        @misc{avito2018DemandPrediction,
          author = {{Avito}},
          title = {Avito Demand Prediction Challenge},
          year = {2018},
          howpublished = {\url{https://www.kaggle.com/competitions/avito-demand-prediction}},
          note = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with train.csv from the Kaggle competition "Avito Demand Prediction Challenge" (2018): 1,503,424 ads posted on Avito.ru from 15 to 28 March 2017, in 28 regions (none of Moscow, Moscow Oblast, St Petersburg or Leningrad Oblast) and 9 parent categories (no jobs). The test file (ads of 12-18 April 2017, plus 65 of 19-20 April) has no labels and is not used.

        - Prediction point: the seller posts the ad, and Avito estimates the interest it will meet ("Avito can inform sellers on how to best optimize their listing and provide some indication of how much interest they should realistically expect to receive", competition overview as mirrored on GitHub; the Kaggle page does not render for automated reads). Every kept column is part of the ad, its seller or Avito's classification of it at that point. The benchmark tests the expectation, not advice on what to change: an ad without a price scores 0.215 against 0.135 because services and give-aways often have none, an association rather than an effect (USE-1).
        - Note: the file does not say whether the title, description and price are as first posted or as last edited. Edits are rare where the text shows them (LEAK-10): 2 titles are marked sold, 43 descriptions say "уже продано" (already sold), and 741 ads (0.05%) carry a price-lowered phrase (mean deal probability 0.123 against 0.139); the missing shares of the photo, description and price are flat over the 14 days. Kept with this note; an edit that leaves no words cannot be seen.
        - Target: `deal_probability`, "the likelihood that an ad actually sold something. It's not possible to verify every transaction with certainty, so this column's value can be any float from zero to one" (data page, as quoted in the competition's top exploration notebook). Avito never said how it is computed: the welcome thread (discussion 55299) asks three times and gets no answer, and Kaggle's Wendy Kan writes there "Logloss won't work if the ground truth isn't 0/1". Avito cannot observe a deal, which happens off the platform; its seller team uses contacts as the proxy (Habr, article 879680). On the data it has two forms: in services (64,385 ads, 4.3%) its 22 positive values are all fractions k/n with n at most 8, like a share of a few counted events; in goods it sits on levels per category (0.80323 on 46,668 personal-item ads, 0.76786 on 26,474 electronics ads; 41.8% of the positive goods ads share their value with 1,000 ads or more). It follows what happened to each ad after posting, not the ad alone: identical reposts (the same seller, title, description, price, category and town) carry different labels in 859 of the 983 groups with a positive ad (87%), a zero beside a positive in 698 and two or more positive values in 198, and in the 511 two-ad groups with one zero and one positive the zero is the later copy in only 46%, so it does not look like Avito blocking the duplicate (circumstantial, EV-6: a seller may delete the first copy, which is also an event after posting). Overall 64.8% exact zeros, 0.67% exact ones, 18,407 distinct values. Shipped as released, on its 0-1 scale (MET-3); the fit is approximate for it (USE-5, USE-8).
        - Note: the zeros are kept as released. Whether a 0 means no deal seen or a floor of Avito's score cannot be told from the data, and the curator's policy is that how a source codes its zeros does not count against a task (Andrej, 2026-10-30, policy question 2 of the zero-inflated review).
        - We drop the 100 ads (0.007%) dated 29 March to 7 April 2017, after the release's last posting day: 84% of them have a positive deal probability against 35% of the rest (mean 0.65 against 0.14), a selected set outside every window. Of the 39 whose seller has ads dated up to 28 March, 33 carry a higher running number than all of them, so most were posted later, as dated; whether the other 6 were re-dated cannot be told. Kaggle participants made the same cut (discussion 55897).
        - We drop `item_id`, the ad id, and `image`, the id of the photo file: `image` is missing exactly where `image_top_1` is (112,588 ads without a photo), so nothing is lost. `user_id`, the seller's anonymous id (771,710 sellers), stays as a categorical (CLEAN-3): Avito knows the seller when the ad is posted, and a known seller's history is part of the task (USE-10, LEAK-34). We build no seller feature from labels (CLEAN-6); each method encodes the id on its own train side.
        - Note: the seller is known for part of the ads: 30.7%, 26.1% and 30.1% of the test ads (newest window first) come from a seller in the window's train side. What the id is worth on the shipped splits (untuned LightGBM on the structured columns, three windows): as LightGBM's native category it lowers RMSE by 0.0001-0.0003 (0.0006-0.0007 on the ads of known sellers); as the seller's past mean label and ad count built on the train side, which a method that encodes the id can learn, by 0.0013-0.0014 (0.0040-0.0054 on those ads). The seller's value is a lasting trait rather than the labels of the days just before (SPLIT-9): on the 18.7% of the newest window's test ads whose seller has ads in both, the seller's mean over the 8 days just before the window gives RMSE 0.18365 and over the 8 days ending 4 days before it 0.18407, against 0.18856 without, so older labels keep 91% of the gain.
        - `title` and `description` are Russian free text (string columns); `region` (28), `city` (1,804 towns: each name written with its region, since 54 of the 1,733 names stand for towns in two to seven regions, 31,770 ads), `parent_category_name` (9), `category_name` (47), `param_1` to `param_3` (Avito's form fields, 371, 271 and 1,219 values), `user_type` (Private, Company, Shop), `image_top_1` (Avito's class code of the photo, 3,062 integer codes) and `user_id` are categorical; `price` and `item_seq_number` (the seller's running ad number, which rises with the posting date within a seller in all but 7 of 731,614 consecutive pairs) are numeric; `activation_date` is the posting date.
        - Note: Avito's categories are "as classified by Avito's ad model" and `image_top_1` is "Avito's classification code for the image" (data page): codes the company made at posting, kept as inputs even if Avito's models learned from earlier deals (USE-6, LEAK-37); only a code fitted on these ads' labels would leak (LEAK-27), and nothing points that way. The photo class tracks what is pictured: over codes with 50 ads or more its Spearman correlation with the mean deal probability is 0.41, but -0.09 with what is left after the category mean, and dropping it costs untuned LightGBM 0.0028 RMSE, less than dropping `price` (0.0049; three windows, 300k training ads each).
        - Anomaly: `price` is missing for 85,360 ads (5.7%; their mean deal probability is 0.215 against 0.135), 0 for 4,645 (mean 0.35), 1 for 3,696 (mean 0.27), and above 100 million rubles for 158 (5 above 1 billion, 3 of them real estate). We keep all of these as the seller entered them (CLEAN-10): a missing price is the seller's choice; 0 and 1, mostly on animals and services, are the seller's way of writing "free" or "contact me" and stay as codes; the extremes are typed by the seller and show on the ad.
        - Note: no two ads are copies once the seller id is kept. The 6 pairs of ads that share every other column (2 with the same target, 4 with different ones) each come from two different sellers, so they are distinct ads and stay (LEAK-19, LEAK-20). Reposts (the same seller, title, description, price, category and town) are 0.69% of the ads and stay as separate postings with their own labels, as in huntprohibited_1m; 86, 126 and 87 test ads per window (0.04-0.06%) have such a repost in the training days.
        - Note: the photos, the unlabelled ads (`train_active`, `test_active`, 17.7 GB) and their display periods (`periods_*`) are not used. The top solutions built seller aggregates from them (days an ad was displayed, ads per seller; discussions 59871, 59885), but the display periods run past the posting date, and their seller statistics span the whole release; the photos are a modality of their own, of which Avito's photo class ships.
        - Note: the text adds to the structured columns, so it ships as text for the pipeline to embed (SEL-12): on the newest window with a random million training ads, as shipped, untuned LightGBM on the structured columns without the seller id reaches R^2 0.257, and 0.273 with an out-of-fold TF-IDF ridge on title and description, which alone reaches 0.206. 218 descriptions (0.015%) hold a phone-like number and 4 an e-mail address.
        - Metric: RMSE on `deal_probability`, the competition's leaderboard metric (Kaggle API `evaluationMetric`: "Root Mean Squared Error").
        - Terms: the rules allow the data to be used "only for the purposes of the Competition" (rules page, as read by the screening); a release-checklist item, not a curation reason.
    """

    accepted_check_warnings = {
        "task_target_value_dominant": (
            "Zero-inflated by nature: Avito's deal probability is 0 for 64.8% of the ads, the source's own value "
            "for an ad without a deal, not a cap or a placeholder (the maximum is 1.0, on 0.67% of the ads); "
            "kept as released under the curator's zero policy (Andrej, policy question 2 of the zero-inflated "
            'review, 2026-10-30: "We want to add any relevant predictive task, independent if it is zero inflated '
            'or not").'
        ),
    }

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="Root Mean Squared Error",
        reference="https://www.kaggle.com/competitions/avito-demand-prediction/overview/evaluation",
        definition="sqrt(mean((deal_probability - prediction)^2)) over the ads of a test window",
    )

    # Splits
    splits_comment = """
        We hold out the newest three two-day windows (27-28, 25-26 and 23-24 March 2017), newest first; each trains on every ad posted before it, a random 1M for the two newer windows and all 861,064 (57% of the ads) for the oldest. Two days is the longest window that keeps three windows above half the ads (SPLIT-12, SPLIT-14); the competition's own horizon (ads of 12-18 April, 15 to 21 days after the last training day) cannot be repeated within the release's 14 days. The three windows cover six of the seven weekdays, with which posting volume and the share of zeros move.

        Exception to SPLIT-10 (proposed by the AI, 2026-11-01; for the curator to confirm): no gap. When Avito's score becomes final is undocumented, but a deal can come weeks after posting: of the competition's supplementary ads activated on 15 March, 96.0% were still listed more than 3 days later and 89.4% on 28 March (periods_train.csv; being listed is not a deal, and these are not the training ads), and the third-place team left a gap of 4 days (discussion 59885). Any gap of 4 days or more leaves a train side under half the ads at every window width (share of the ads before each window, newest first: two-day windows 85, 71 and 57% with no gap and 77, 64 and 49.97% with a 1-day gap; one-day windows 71, 64 and 57% with a 3-day gap and 64, 57 and 49.97% with a 4-day gap), and a shorter gap covers a small part of the delay, the partial gap passed over for alfa_battle_2_0_task_2 (gap 0, Lennart, 2026-10-26). Serves SPLIT-14 (Must). At equal training size a 3-day gap costs untuned LightGBM 0.00024 and 0.00020 RMSE on the two newer windows (paired SE 0.00004-0.00005).

        SPLIT-9 holds: no measurable shortcut has been found, as lending_club records, and the unmatured labels fall under SPLIT-10 (principles.md, Tensions). Same-seller reposts of a test ad are 0.47-0.60% of a window, and even an oracle blend of their labels moves a window's RMSE by 0.00006 at most. The seller's labels act as a lasting trait, not as the outcome of the days just before: a test ad is positive in 43.5% of cases after a positive ad of its seller 1-3 days earlier and in 41.5% after one 4-12 days earlier (in alfa_battle_2_0_task_2, whose shortcut was removed, 95.1% after an earlier default against 2.3%), and a seller history of 8 days ending 4 days before the window keeps 91% of the gain of the 8 days just before it. The hidden-group probe (temporal mode) finds no hidden group; the one entity across the split is the seller (29.0% of the test ads have a seller in training, 26.1-30.7% over the windows), which is the task (SPLIT-13, USE-10).
    """
    temporal = Temporal(
        on="activation_date",
        splits=TemporalSplits(window=2, unit="days", n_windows=3),
    )
    subsample_to_budget = True

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # One comma-separated file, 1,503,424 ads; ids read as text.
        return pd.read_csv(
            raw_dir / "train.csv",
            dtype={"item_id": "string", "user_id": "string", "image": "string"},
            parse_dates=["activation_date"],
        )

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. The 100 ads dated after the release's last posting day (29 March to 7 April 2017).
        df = raw[raw["activation_date"] <= LAST_DAY]
        # 2. The ad and photo-file ids; the photo's presence stays in `image_top_1` (missing exactly when `image` is).
        #    The seller id `user_id` stays, as a categorical.
        df = drop_columns(df, ["item_id", "image"])
        # 3. A town is its name within its region: 54 names stand for towns in two to seven regions.
        df["city"] = df["city"] + " (" + df["region"] + ")"
        # 4. Avito's photo class as integer codes (float only because of the ads without a photo).
        df["image_top_1"] = df["image_top_1"].astype("Int64")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "region",
                "city",
                "parent_category_name",
                "category_name",
                "param_1",
                "param_2",
                "param_3",
                "user_type",
                "image_top_1",
                "user_id",
            ],
            string=["title", "description"],
            datetime=["activation_date"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        y = raw[TARGET]
        late = raw["activation_date"] > LAST_DAY
        by_day = raw.groupby("activation_date")[TARGET]
        days = pd.DataFrame(
            {
                "ads": by_day.size(),
                "mean": by_day.mean().round(4),
                "share zero": by_day.apply(lambda s: s.eq(0).mean()).round(4),
                "p90": by_day.quantile(0.9).round(4),
            }
        )
        days.index = days.index.strftime("%Y-%m-%d")
        positive = raw.loc[y > 0]
        cats_per_value = positive.groupby(TARGET)["parent_category_name"].nunique()
        # On the shipped ads: services against goods, and identical reposts (seller, text, price, category, town).
        ys = df[TARGET]
        services = df["parent_category_name"].astype("string").eq("Услуги")
        service_values = ys[services & ys.gt(0)].unique()
        fractions = [any(abs(v * n - round(v * n)) < 1e-4 for n in range(1, 9)) for v in service_values]
        goods = ys[~services & ys.gt(0)]
        top = y[y > 0].mode().iloc[0]
        twins = df[["user_id", "title", "description", "price", "category_name", "city"]].assign(
            y=ys, positive=ys.where(ys > 0), zero=ys.eq(0)
        )
        twins = twins.groupby(list(twins.columns[:6]), dropna=False, observed=True).agg(
            n=("y", "size"), values=("y", "nunique"), positive_values=("positive", "nunique"), zero=("zero", "max")
        )
        twins = twins[twins["n"].ge(2) & twins["positive_values"].gt(0)]
        target = pd.Series(
            {
                "ads": len(raw),
                "exact zeros": f"{y.eq(0).mean():.1%}",
                "exact ones": f"{y.eq(1).mean():.2%}",
                "distinct values": int(y.nunique()),
                "most frequent positive value (ads)": f"{top} ({int(y.eq(top).sum()):,})",
                "distinct positive values in one parent category only": f"{cats_per_value.eq(1).mean():.1%}",
                "ads dated after 28 March (dropped)": int(late.sum()),
                "share positive among them": f"{y[late].gt(0).mean():.0%}",
                "share positive among the rest": f"{y[~late].gt(0).mean():.0%}",
                "services ads (shipped)": f"{int(services.sum()):,} ({services.mean():.1%})",
                "their distinct positive values; k/n with n at most 8": f"{len(fractions)}; {sum(fractions)}",
                "positive goods ads on a value shared by 1,000 ads or more": (
                    f"{goods.map(goods.value_counts()).ge(1000).mean():.1%}"
                ),
                "repost groups with a positive ad": len(twins),
                "of them with different labels": int(twins["values"].gt(1).sum()),
                "of them with a zero beside a positive": int(twins["zero"].sum()),
                "of them with two or more positive values": int(twins["positive_values"].ge(2).sum()),
            },
            name="value",
        )
        return [
            Decision(
                "The target is Avito's undocumented 0-1 score, shipped as released",
                "In services the positive values are fractions k/n with n at most 8, like a share of a few counted "
                "events; in goods they sit on a few levels per category, as a scoring step would give. Identical "
                "reposts carry different labels in most groups with a positive ad, so the score follows what "
                "happened to each ad after posting, not the ad alone. The 100 ads dated after 28 March are mostly "
                "positive and are dropped.",
                target,
            ),
            Decision(
                "The target is stable over the posting days",
                "No sign that the newest days lost their late deals (LEAK-24, probe 13): the mean and the share of "
                "zeros of 28 March match those of 15 March.",
                days,
            ),
        ]

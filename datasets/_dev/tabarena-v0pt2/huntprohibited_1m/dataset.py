"""Curated dataset definition for `huntprohibited_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, drop_columns

TARGET = "is_blocked"


class Huntprohibited1m(AbstractCuratedDataset):
    # Dataset
    unique_name = "huntprohibited_1m"
    version_of = "huntprohibited"
    version_comment = """
        We sub-sample the frame (3,963,488 ads after dropping duplicates) to 1.5M ads, stratified on the target, and use 3-fold cross-validation, so every fold trains on 1M and tests on 500k ads (v2 split protocol).
    """
    year = "2014"
    domain = "business & marketing"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/avito-prohibited-content"
    license = "Kaggle Competition Rules"
    data_tags = ("ForcedIIDFromTemporal",)
    download_description = """
        The training file of the Kaggle competition "The Hunt for Prohibited Content" (Avito, 2014); the rules must be
        accepted on the competition page first. The zip (772,619,211 bytes, sha256
        aa5472aa91d2fda10e9e79c9ca69c28dfa9e2155b9eefe2557dcaafba771a23b) holds avito_train.tsv and is read as it is.

        mkdir -p local-data-warehouse/huntprohibited
        kaggle competitions download -c avito-prohibited-content -f avito_train.zip -p local-data-warehouse/huntprohibited
    """
    bibtex = r"""
        @misc{avito2014HuntProhibitedContent,
          author = {{Avito}},
          title = {The Hunt for Prohibited Content},
          year = {2014},
          howpublished = {\url{https://www.kaggle.com/competitions/avito-prohibited-content}},
          note = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with avito_train.tsv from the Kaggle competition "The Hunt for Prohibited Content": 3,995,803 ads posted on Avito.ru from December 2013 to March 2014. The unlabelled test file (April 2014) is not used.

        - Prediction point: an ad is scored when it is submitted (new or edited) and enters moderation, from its content as posted. The target `is_blocked` says whether a moderator blocked the ad for illicit content.
        - We drop `close_hours`, how long the ad was live: it is known only after the moderation decision (the hosts: "not available at scoring phase").
        - We drop `is_proved`, which is set only for blocked ads: a component of the target, "not to be used as a direct modeling attribute" (data page).
        - We drop `itemid`: the ids "have been randomly assigned" (Kaggle discussion 9554).
        - IID split, tagged ForcedIIDFromTemporal: the competition split by month, but the file has no date and the random ids cannot stand in for one (decision table).
        - We drop exact copies of an ad (reposts with the same features and label) and every ad whose features occur with both labels (decision table).
        - Note: edited reposts stay. 1.39% of the fold-0 test ads share a description of 30+ characters with a training ad (0.50% of the April test ads), dropping them changes ROC AUC by at most 0.002, and without a seller id they cannot be grouped.
        - `title`, `description` and `attrs` are Russian free text (string columns). `category` and `subcategory` are categorical; `price` and the counts of phone numbers, e-mails and URLs that Avito masked in the description are numeric.
        - We keep `attrs`, the ad's form fields for its category, as the released JSON text: unpacking it would give 72 mostly empty columns with Russian names, and the winning solutions treated it as text (Kaggle discussion 10178).
        - Anomaly: 6,004 `attrs` strings are not valid JSON, the description writes line breaks as "^p", and `price` is 0 for 12.4% of the ads (no price given, or free). We keep all of these as released.
        - Note: we keep the source's cohort, closed ads that were blocked for illicit content or never blocked; `price` is the final price, so an edited ad may hold its last version.
        - Note: text carries most of the signal. On fold 0, LightGBM on the structured columns reaches ROC AUC 0.932 and a logistic regression on TF-IDF of the three text columns 0.994, so a pipeline that encodes Russian text poorly loses most of the task.
        - Note: the hidden-group probe hits on subcategory and attrs, but every new ad has both, so the split stays IID.
        - Note: the competition scored AP@32500; we use ROC AUC. The rules restrict the data to use within the competition, and the ads include illicit or offensive content (rules page).
    """

    # Task
    target = TARGET
    problem_type = "binary_classification"

    # Splits: IID (no time index survives); the `_1m` version sub-samples the frame to the 1.5M-row budget.
    subsample_to_budget = True
    accepted_check_warnings = {
        "dataset_pure_feature_value": "Real-estate ads (category Недвижимость and its subcategories) and children's "
        "clothes are almost never blocked (0.12% of 1,149,136 real-estate ads in the full file): the seller picks the "
        "category when posting, so this is a category effect known at the prediction point, not a leak. The winners "
        "left real estate out of training for this reason (Kaggle discussion 10178).",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # One tab-separated file inside the zip (3,995,803 rows; `wc -l` gives 3,995,804 lines with the header).
        return pd.read_csv(raw_dir / "avito_train.zip", sep="\t")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # Post-outcome or target-component columns, and the random id.
        df = drop_columns(raw, ["close_hours", "is_proved", "itemid"])
        df[TARGET] = df[TARGET].map({1: "Yes", 0: "No"})
        # Exact copies of an ad (features and label) are reposts: keep one. Feature vectors with both labels: drop all.
        features = [c for c in df.columns if c != TARGET]
        df = df.drop_duplicates()
        return df[~df.duplicated(subset=features, keep=False)]

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["category", "subcategory"],
            string=["title", "description", "attrs"],
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        blocked = raw[TARGET].astype(bool)
        leaks = pd.DataFrame(
            {
                "ads": [int((~blocked).sum()), int(blocked.sum())],
                "close_hours median": [
                    raw.loc[~blocked, "close_hours"].median(),
                    raw.loc[blocked, "close_hours"].median(),
                ],
                "close_hours below 1 hour": [
                    f"{raw.loc[~blocked, 'close_hours'].lt(1).mean():.1%}",
                    f"{raw.loc[blocked, 'close_hours'].lt(1).mean():.1%}",
                ],
                "is_proved set": [
                    int(raw.loc[~blocked, "is_proved"].notna().sum()),
                    int(raw.loc[blocked, "is_proved"].notna().sum()),
                ],
                "is_proved = 1": [
                    int(raw.loc[~blocked, "is_proved"].eq(1).sum()),
                    int(raw.loc[blocked, "is_proved"].eq(1).sum()),
                ],
            },
            index=pd.Index(["not blocked", "blocked"], name="is_blocked"),
        )
        decile = pd.qcut(raw["itemid"], 10, labels=False).rename("itemid decile")
        text = raw["title"].fillna("").str.lower() + " " + raw["description"].fillna("").str.lower()
        by_id = pd.DataFrame(
            {
                "ads": raw.groupby(decile).size(),
                "blocked share": blocked.groupby(decile).mean().round(4),
                "real-estate share": raw["category"].eq("Недвижимость").groupby(decile).mean().round(4),
                "'новый год' share": text.str.contains("новый год", regex=False).groupby(decile).mean().round(5),
                "'8 марта' share": text.str.contains("8 марта", regex=False).groupby(decile).mean().round(5),
            }
        )
        features = [c for c in raw.columns if c not in (TARGET, "close_hours", "is_proved", "itemid")]
        copies = raw.duplicated(subset=[*features, TARGET], keep="first")
        deduplicated = raw[~copies]
        conflicting = deduplicated.duplicated(subset=features, keep=False)
        kept = deduplicated[~conflicting]
        # near copies that stay: the same description (at least 30 characters) with another title, price or attrs
        shared = kept["description"].str.len().ge(30) & kept.duplicated(subset=["description"], keep=False)
        duplicates = pd.Series(
            {
                "ads in the file": len(raw),
                "exact copies dropped (features and label)": int(copies.sum()),
                "blocked share of the copies": f"{raw.loc[copies, TARGET].mean():.1%}",
                "ads whose features occur with both labels (all dropped)": int(conflicting.sum()),
                "ads kept": len(kept),
                "blocked share of the ads kept": f"{kept[TARGET].mean():.1%}",
                "kept ads sharing a description of 30+ characters with another kept ad": int(shared.sum()),
                "blocked share of those": f"{kept.loc[shared, TARGET].mean():.1%}",
                "ads in this version (sub-sampled)": len(df),
            },
            name="value",
        )
        return [
            Decision(
                "close_hours and is_proved are dropped",
                "close_hours is the time the ad stayed live, known only after the moderation decision (and exported "
                "modulo 24 hours); is_proved is set only for blocked ads.",
                leaks,
            ),
            Decision(
                "IID split: the item ids are random and no date survives",
                "The host says the ids were randomly assigned; block rate, category share and seasonal words are flat "
                "over the id deciles, so the ids cannot stand in for the posting date.",
                by_id,
            ),
            Decision(
                "Reposts are dropped",
                "Ads that repeat another ad's features and label would sit on both sides of a random split. Edited "
                "reposts (same description, another title, price or attrs) stay: without a seller id they cannot be "
                "grouped exactly.",
                duplicates,
            ),
        ]

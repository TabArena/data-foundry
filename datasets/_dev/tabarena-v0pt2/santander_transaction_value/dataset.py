"""Curated dataset definition for `santander_transaction_value` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import gc
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset


class SantanderTransactionValue(AbstractCuratedDataset):
    # Dataset
    unique_name = "santander_transaction_value"
    year = "2018"
    domain = "finance"
    source = "Kaggle"
    source_url = "https://www.kaggle.com/competitions/santander-value-prediction-challenge"
    license = "Kaggle Competition Rules"
    data_tags = ("Anonymized",)
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c santander-value-prediction-challenge -f train.csv && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/santander_transaction_value && mv train.csv local-data-warehouse/santander_transaction_value/
    """
    bibtex = r"""
        @misc{McDonald2018SantanderValuePredictionChallenge,
          author = {Mark McDonald and Mercedes Piedra and Sohier Dane and Soraya Jimenez},
          title  = {Santander Value Prediction Challenge},
          year   = {2018},
          howpublished = {\url{https://kaggle.com/competitions/santander-value-prediction-challenge}},
          note   = {Kaggle competition}
        }
    """
    curation_comments = """
        We start with the train.csv from Kaggle.

        - The data has been anonymized.
        - We follow the preprocessing by Tschalzev et al. (https://arxiv.org/abs/2407.02112), which follows https://www.kaggle.com/competitions/santander-value-prediction-challenge/discussion/63919
        - Since we restrict to the train.csv, we do not exploit the test leak of the competition.
        - The expert preprocessing aggregates over feature groups per row to create the new features for the final dataset. Feature groups for aggregation are found by searching for chains of features (?).
        - The data contains a very small number of duplicates. We remove them to avoid leakage in our own splits.
    """

    # Task
    target = "target"
    problem_type = "regression"
    metric = "rmsle"

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        og_df = pd.read_csv(raw_dir / "train.csv")
        return og_df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        og_df = raw
        train = og_df.copy()
        # Code adapted from https://github.com/atschalz/dc_tabeval/blob/main/datasets.py#L2120 w/o test leak part
        features = [
            "f190486d6",
            "58e2e02e6",
            "eeb9cd3aa",
            "9fd594eec",
            "6eef030c1",
            "15ace8c9f",
            "fb0f5dbfe",
            "58e056e12",
            "20aa07010",
            "024c577b9",
            "d6bb78916",
            "b43a7cfd5",
            "58232a6fb",
            "1702b5bf0",
            "324921c7b",
            "62e59a501",
            "2ec5b290f",
            "241f0f867",
            "fb49e4212",
            "66ace2992",
            "f74e8f13d",
            "5c6487af1",
            "963a49cdc",
            "26fc93eb7",
            "1931ccfdd",
            "703885424",
            "70feb1494",
            "491b9ee45",
            "23310aa6f",
            "e176a204a",
            "6619d81fc",
            "1db387535",
            "fc99f9426",
            "91f701ba2",
            "0572565c2",
            "190db8488",
            "adb64ff71",
            "c47340d97",
            "c5a231d81",
            "0ff32eb98",
        ]
        extra_features = []
        train = train  # noqa: PLW0127
        train_t = train.drop(["target"], axis=1, inplace=False)
        train_t.set_index("ID", inplace=True)
        train_t = train_t.T

        # run this iteratively until you have no more links. Then prune
        def chain_pairs(ordered_items):
            ordered_chains = []
            links_found = 0
            for _i_1, op_chain in enumerate(ordered_items.copy()[:]):
                if op_chain[0] != op_chain[1]:
                    end_chain = op_chain[-1]
                    for _i_2, op in enumerate(ordered_items.copy()[:]):
                        if end_chain == op[0]:
                            links_found += 1
                            op_chain.extend(op[1:])
                            end_chain = op_chain[-1]

                    ordered_chains.append(op_chain)
            return links_found, ordered_chains

        def prune_chain(ordered_chain):

            ordered_chain = sorted(ordered_chain, key=len, reverse=True)
            new_chain = []
            id_lookup = {}
            for oc in ordered_chain:
                id_already_in_chain = False
                for idd in oc:
                    if idd in id_lookup:
                        id_already_in_chain = True
                    id_lookup[idd] = idd

                if not id_already_in_chain:
                    new_chain.append(oc)
            return sorted(new_chain, key=len, reverse=True)

        def find_new_ordered_features(ordered_ids, data_t):
            data = data_t.copy()

            f1 = ordered_ids[0][:-1]
            f2 = ordered_ids[0][1:]
            for ef in ordered_ids[1:]:
                f1 += ef[:-1]
                f2 += ef[1:]

            d1 = data[f1].apply(tuple, axis=1).apply(hash).to_frame().rename(columns={0: "key"})
            d1["ID"] = data.index
            gc.collect()
            d2 = data[f2].apply(tuple, axis=1).apply(hash).to_frame().rename(columns={0: "key"})
            d2["ID"] = data.index
            gc.collect()
            d3 = d2[~d2.duplicated(["key"], keep=False)]
            d4 = d1[~d1.duplicated(["key"], keep=False)]
            d5 = d4.merge(d3, how="inner", on="key")

            d_feat = d1.merge(d5, how="left", on="key")

            ordered_features = list(d_feat[["ID_x", "ID_y"]][d_feat.ID_x.notna()].apply(list, axis=1))
            del d1, d2, d3, d4, d5, d_feat
            gc.collect()

            links_found = 1
            while links_found > 0:
                links_found, ordered_features = chain_pairs(ordered_features)

            ordered_features = prune_chain(ordered_features)
            # make lookup of all features found so far
            found = {}
            for ef in extra_features:
                found[ef[0]] = ef
            found[features[0]] = features

            new_feature_sets = []
            for of in ordered_features:
                if len(of) >= 40 and of[0] not in found:
                    new_feature_sets.append(of)

            return new_feature_sets

        def add_new_feature_sets(data, data_t):

            # print ('\nData Shape:', data.shape)
            f1 = features[:-1]
            f2 = features[1:]

            for ef in extra_features:
                f1 += ef[:-1]
                f2 += ef[1:]

            d1 = data[f1].apply(tuple, axis=1).apply(hash).to_frame().rename(columns={0: "key"})
            d1["ID"] = data["ID"]
            gc.collect()
            d2 = data[f2].apply(tuple, axis=1).apply(hash).to_frame().rename(columns={0: "key"})
            d2["ID"] = data["ID"]
            gc.collect()
            # print('here')
            d3 = d2[~d2.duplicated(["key"], keep=False)]
            del d2
            d4 = d1[~d1.duplicated(["key"], keep=False)]
            # print('here')
            d5 = d4.merge(d3, how="inner", on="key")
            del d4
            d = d1.merge(d5, how="left", on="key")
            # print('here')
            ordered_ids = list(d[["ID_x", "ID_y"]][d.ID_x.notna()].apply(list, axis=1))
            del d1, d3, d5, d
            gc.collect()

            links_found = 1
            while links_found > 0:
                links_found, ordered_ids = chain_pairs(ordered_ids)
                # print(links_found)

            # print ('OrderedIds:', len(ordered_ids))
            # Make distinct ordered id chains
            ordered_ids = prune_chain(ordered_ids)
            # print ('OrderedIds Pruned:', len(ordered_ids))

            # look for ordered features with new ordered id chains
            new_feature_sets = find_new_ordered_features(ordered_ids, data_t)

            extra_features.extend(new_feature_sets)

        add_new_feature_sets(train, train_t)
        add_new_feature_sets(train, train_t)
        add_new_feature_sets(train, train_t)
        del train_t
        gc.collect()
        ### Create 40 features
        extra_features_list = []
        for ef in extra_features:
            extra_features_list.extend(ef)
        extra_features_list.extend(features)
        # This makes the 100 40 length feature groups into 40 100 length feature groups.
        feats = pd.DataFrame(extra_features)
        time_features = []
        for c in feats.columns[:]:
            time_features.append([f for f in feats[c].values if f is not None])
        # Make a bunch of different feature groups to build aggregates from
        agg_features = []
        all_cols = train.columns.drop(["ID", "target"])
        agg_features.append(all_cols)
        agg_features.append([c for c in all_cols if c not in extra_features_list])
        agg_features.append(extra_features_list)
        agg_features.extend(time_features)
        agg_features.extend(extra_features)

        def add_new_features(source, dest, feats):
            high = source[feats].max(axis=1)
            high.name = f"high_{feats[0]}_{len(feats)}"
            mean = source[feats].replace(0, np.nan).mean(axis=1)
            mean.name = f"mean_{feats[0]}_{len(feats)}"
            low = source[feats].replace(0, np.nan).min(axis=1)
            low.name = f"low_{feats[0]}_{len(feats)}"
            median = source[feats].replace(0, np.nan).median(axis=1)
            median.name = f"median_{feats[0]}_{len(feats)}"
            sum = source[feats].sum(axis=1)  # noqa: A001
            sum.name = f"sum_{feats[0]}_{len(feats)}"
            stddev = source[feats].std(axis=1)
            stddev.name = f"stddev_{feats[0]}_{len(feats)}"
            first_nonZero = np.log1p(source[feats].replace(0, np.nan).bfill(axis=1).iloc[:, 0])
            first_nonZero.name = f"first_nonZero_{feats[0]}_{len(feats)}"
            last_nonZero = np.log1p(source[feats[::-1]].replace(0, np.nan).bfill(axis=1).iloc[:, 0])
            last_nonZero.name = f"last_nonZero_{feats[0]}_{len(feats)}"
            nb_nans = source[feats].replace(0, np.nan).isnull().sum(axis=1)
            nb_nans.name = f"nb_nans_{feats[0]}_{len(feats)}"
            unique = source[feats].nunique(axis=1)
            unique.name = f"unique_{feats[0]}_{len(feats)}"

            dest = pd.concat(
                [dest, high, mean, low, median, sum, stddev, first_nonZero, last_nonZero, nb_nans, unique], axis=1
            )
            return dest

        train_feats = pd.DataFrame()
        for _i, ef in list(enumerate(agg_features)):
            train_feats = add_new_features(train, train_feats, ef)
        df = train_feats
        df[self.task_metadata.target_column_name] = np.log1p(train.target.values)
        # Remove duplicates
        df = df.drop_duplicates(subset=[c for c in df.columns if c != self.task_metadata.target_column_name])
        return df

"""Curated dataset definition for `santander_transaction_value` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import gc
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Grouping, Metric, Source, TaskSummary
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

MAX_SHIFT = 39
"""The largest shift, in steps, between two snapshots that the key compares (the groups are 40 columns long)."""

MIN_NONZERO_EXACT = 3
"""Shifted values that link two snapshots without the target hold at least this many non-zero values."""


def _customer_key(raw: pd.DataFrame, column_groups: list[list[str]]) -> np.ndarray:
    """One number per raw row: the customer, as the connected components of the links between its snapshots.

    Each column group is one lag series, most recent first (the first group's first column is the value two steps
    back). A row k steps later than another holds the same values shifted by k columns, in every group at once:
    ``early[g][:-k] == late[g][k:]``. Two kinds of link, for k from 1 to ``MAX_SHIFT``:

    * exact: the shifted values hold at least ``MIN_NONZERO_EXACT`` non-zero values, and no other row has the same
      ones on its side (no target used);
    * confirmed sparse (k of 2 or more): any other match with at least one non-zero value, kept when the later row's
      lag column ``k - 2`` of the first group holds the earlier row's exact target, and neither row has another such
      match at that k. The target only decides which rows belong together; it is never a feature.
    """
    values = [raw[group].to_numpy(dtype=np.float64) for group in column_groups]
    lead = values[0]
    target = raw["target"].to_numpy(dtype=np.float64)
    n = len(raw)
    links = []
    for k in range(1, MAX_SHIFT + 1):
        early_values = np.concatenate([v[:, :-k] for v in values], axis=1)
        late_values = np.concatenate([v[:, k:] for v in values], axis=1)
        early = pd.DataFrame(
            {
                "key": pd.util.hash_pandas_object(pd.DataFrame(early_values), index=False).to_numpy(),
                "early": np.arange(n),
                "nonzero": (early_values != 0).sum(axis=1),
            }
        )
        late = pd.DataFrame(
            {
                "key": pd.util.hash_pandas_object(pd.DataFrame(late_values), index=False).to_numpy(),
                "late": np.arange(n),
            }
        )
        early["unique_early"] = ~early["key"].duplicated(keep=False)
        late["unique_late"] = ~late["key"].duplicated(keep=False)
        matches = early[early["nonzero"] >= 1].merge(late, on="key")
        matches = matches[matches["early"] != matches["late"]]
        exact = matches["unique_early"] & matches["unique_late"] & (matches["nonzero"] >= MIN_NONZERO_EXACT)
        links.append(matches.loc[exact, ["early", "late"]])
        if k >= 2:
            sparse = matches[~exact]
            confirmed = sparse[lead[sparse["late"].to_numpy(), k - 2] == target[sparse["early"].to_numpy()]]
            confirmed = confirmed[
                ~confirmed["early"].duplicated(keep=False) & ~confirmed["late"].duplicated(keep=False)
            ]
            links.append(confirmed[["early", "late"]])
    edges = pd.concat(links, ignore_index=True)
    graph = coo_matrix((np.ones(len(edges)), (edges["early"], edges["late"])), shape=(n, n))
    return connected_components(graph, directed=False)[1]


class SantanderTransactionValue(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How much will a potential Santander customer transact?",
        use_case=(
            "Santander estimates the value of transactions of each potential customer, to personalise its service "
            "(the competition's stated aim)."
        ),
        row=(
            "One snapshot of a customer in the training file of the 2018 Kaggle competition (710 customers with 1 to "
            "104 snapshots each); the country, period and units are not stated."
        ),
        predicted=("The customer's transaction value, on a log scale; its unit and time window are not stated."),
        known=(
            "540 summaries (maximum, mean, minimum, median, sum, spread, first and last non-zero value, counts) of "
            "the customer's anonymised values, over groups of columns that competitors found to form time series."
        ),
        split=(
            "Whole customers are held out: each test fold holds customers the model has not seen, with all their "
            "snapshots, as in the competition, whose training and test files hold different customers."
        ),
        changes=(
            "We replace the raw columns by summaries over groups of columns, following Tschalzev et al. 2024, use only "
            "the training file, and rebuild the customer of each row from its shifted lag values to hold out whole "
            "customers."
        ),
        fit="approximate",
        fit_reason=(
            "The values are anonymised, the prediction point and the window of the transaction value are not stated, "
            "and the undated snapshots are split by customer instead of by time."
        ),
    )

    # Dataset
    unique_name = "santander_transaction_value"
    domain = "finance"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/competitions/santander-value-prediction-challenge",
            license="Kaggle Competition Rules",
            year="2018",
            bibtex=r"""
                @misc{McDonald2018SantanderValuePredictionChallenge,
                  author = {Mark McDonald and Mercedes Piedra and Sohier Dane and Soraya Jimenez},
                  title  = {Santander Value Prediction Challenge},
                  year   = {2018},
                  howpublished = {\url{https://kaggle.com/competitions/santander-value-prediction-challenge}},
                  note   = {Kaggle competition}
                }
            """,
        ),
    )
    data_tags = ("Anonymized", "ForcedGroupedFromTemporal")
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c santander-value-prediction-challenge -f train.csv && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/santander_transaction_value && mv train.csv local-data-warehouse/santander_transaction_value/
    """
    curation_comments = """
        We start with the train.csv from Kaggle (4,459 rows, 4,991 anonymised columns).

        - The data has been anonymized.
        - We follow the preprocessing by Tschalzev et al. (https://arxiv.org/abs/2407.02112), which follows https://www.kaggle.com/competitions/santander-value-prediction-challenge/discussion/63919
        - We use only train.csv. The competition's test file holds other customers (the split bullets below), and its
          leak ran inside that file.
        - The expert preprocessing aggregates over feature groups per row to create the new features for the final dataset. Feature groups for aggregation are found by searching for chains of features (?).
        - The data contains a very small number of duplicates. We remove them to avoid leakage in our own splits. The
          12 dropped rows are one-row customers whose copy belongs to another customer; `customer` is left out of the
          comparison (with it, all 4,459 rows would stay).
        - We store log1p of the competition's target; the metric is the competition's RMSLE on the raw value, computed
          after the inverse (`target_transform="log1p"`; until 2026-10-14 the metric was `rmsle` without the inverse,
          which logged the stored target a second time).
        - ForcedGroupedFromTemporal (Andrej, 2026-11-05, REVIEW.md issue 1, option D): the rows are snapshots of the
          same customers at different times, and a snapshot k steps later holds the same values shifted by k columns,
          including the earlier snapshot's target in its lag columns (Giba's "data property",
          https://www.kaggle.com/competitions/santander-value-prediction-challenge/discussion/61329). The file has no
          dates, so whole customers are held out instead of time windows (`customer`, Grouping). Under the random
          split used until 2026-11-05, 69% to 71% of test rows had a later snapshot of their customer in training.
        - Customer key (`_customer_key`, on the raw columns before the summaries): the 12 lag groups of 40 columns the
          column search finds (the 40 listed `features` and the 11 `extra_features`), most recent first. A row k
          steps later than another (k = 1 to 39) holds the other's values shifted by k columns in all 12 groups at
          once. Exact links: the shifted values hold at least 3 non-zero values and no other row has the same ones on
          its side (34,635 links, no target used). Confirmed sparse links, for the customers with only one or two
          values (k of 2 or more): any other match with a non-zero value, kept when the later row's lag column k - 2
          of `features` holds the earlier row's exact target and neither row has another such match at that k (4,371
          links; 85 to 110 with shuffled targets, so about 2% join two customers by chance). The customers are the
          connected components. The target only decides which rows belong together; neither it nor `customer` is a
          feature.
        - Customers: 710 on the 4,447 rows. 414 have one row (9% of the rows); 57 have 2, 81 have 3 to 5, 54 have 6
          to 10, 52 have 11 to 25, 36 have 26 to 50 and 16 have 51 to 104 rows. The exact links alone give 1,184
          customers (945 with one row).
        - Leak test across the split, on the raw columns (3 x 3 grouped folds): no test row has a linked later
          snapshot in training. Reading a test row's target from the lag column of any training row that matches it
          at a shift finds it for 19 to 32 test rows per fold (1% to 3%; 5 to 10 by chance), against 103 to 145
          (7% to 11%) with the exact links alone and about 1,100 per fold (72% to 75%) under the random split.
        - Leak test on the 540 summaries (2026-11-06): a chain feature rebuilt from training rows only (a row's next
          two snapshots found by the per-step summaries shifted by one and two steps; the target as the difference of
          their `features`-group sums) gives the exact target of 28 to 44 test rows per random fold and of none on the
          9 grouped folds, where 1 to 8 test rows per fold get a value at all. Added to untuned LightGBM, it lowers
          RMSLE on 9 of 9 random folds (by 0.5% to 2.2%); on the grouped folds it is lower on 6 and higher on 3 (from
          1.7% lower to 1.7% higher, mean 0.1% lower). Without it, LightGBM has RMSLE 1.387 on random folds and 1.504
          on the grouped ones.
        - Note: the competition's own split was by customer. The exact key built over train.csv and test.csv (49,342
          rows; 31,792 hold values with more than two decimals, and the winners report 27,477 filler rows that
          counted on neither leaderboard,
          https://www.kaggle.com/competitions/santander-value-prediction-challenge/discussion/63907) finds 12 of
          111,552 links across the files: 4 customers have rows in both (124 training rows, 131 test rows). The leak
          competitors used ran inside the test file: a later test snapshot shows the target of 6,991 of the 17,550
          test rows without long decimals, a training row that of 4. Competitors read 7,800 to 8,000 test targets this
          way (https://www.kaggle.com/competitions/santander-value-prediction-challenge/discussion/61472), and
          Tschalzev et al. moved these rows into training (12,296 training rows in their Table 1).
        - Potential leak, kept on purpose: a test fold holds every snapshot of its customers, so 68% to 75% of test
          rows have a later snapshot in the same fold whose lag column shows their target, as in the competition's
          test file. Only a method that compares test rows with each other can read it; the grouping's context is
          `none` (each row is predicted from its own values), and the splits comment states the protocol line that
          no model step may use other test rows (LEAK-9, as for medical_facility_operational_data and fremtpl2).
        - Time basis: ForcedGroupedFromTemporal: snapshots of customers at different steps, the target two steps after
          the newest lag column, no calendar date: the steps of different customers cannot be aligned, only a
          customer's own snapshots are ordered, through the shifted columns. A dated release would allow windows by
          calendar step, testing later steps and the shocks that the customers of one month share, which the split by
          customer leaves on both sides; it should be used if Santander releases the dates.
    """

    # Task
    target = "target"
    problem_type = "regression"
    metric = Metric.source(
        "rmsle",
        original="Root Mean Squared Logarithmic Error (RMSLE)",
        reference="https://www.kaggle.com/competitions/santander-value-prediction-challenge/overview/evaluation",
        definition=(
            "sqrt(mean((log1p(y_hat) - log1p(y))^2)) on the raw transaction value, computed after the inverse of "
            "the stored log1p(target)"
        ),
        target_transform="log1p",
    )

    # Splits: whole customers held out
    grouping = Grouping(
        on="customer",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a customer of the competition's training file, rebuilt from the data (`_customer_key`, curation
            notes): the rows are snapshots of customers at different times, and a later snapshot holds an earlier one's
            values shifted by the steps between them, its target included. Holding out whole customers follows the
            competition, whose training and test files hold different customers (4 customers have rows in both), and its
            use case: "Santander Group is asking Kagglers to help them identify the value of transactions for each
            potential customer" (competition description,
            https://www.kaggle.com/competitions/santander-value-prediction-challenge/overview). Each snapshot has its
            own target and is predicted from its own row. The file has no dates, so the grouped split stands in for a
            temporal one.
        """,
    )
    splits_comment = """
        Grouped 3-fold cross-validation over the 710 customers with 3 repeats (each snapshot has its own target, so
        the protocol counts the 4,447 rows). A test fold holds 236 or 237 customers and 1,213 to 1,920 rows (the
        folds take equal numbers of customers, not of rows); the largest customer is 4% to 8% of a test fold. The
        competition split its files by customer too; the file has no dates for a temporal split. Each test row is
        predicted from the training rows and its own features only; no feature or model step may use other test rows,
        since a later snapshot in the same test fold shows the target of 68% to 75% of them.
    """

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
        # The customer of each row, from the raw lag columns before the summaries (curation notes, Grouping)
        customer = _customer_key(train, [features, *extra_features])
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
        df = df.assign(customer=customer)
        # Remove duplicates (the 12 dropped rows are one-row customers; the customer is not part of the comparison)
        not_compared = (self.task_metadata.target_column_name, "customer")
        df = df.drop_duplicates(subset=[c for c in df.columns if c not in not_compared])
        return df

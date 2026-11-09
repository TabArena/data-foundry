"""Curated dataset definition for `alfa_bank_credit_history_default_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    Metric,
    RowBudget,
    SplitPlan,
    TaskSummary,
    Temporal,
    TemporalSplits,
    decode,
    drop_columns,
)
from data_foundry.v2.splits import sample_temporal_splits

TRAIN_DIR = "train_data"
TARGET_FILE = "train_target.csv"
FEATURES_FILE = "application_features.parquet"

SKIPPED_FIELDS = ("id", "rn")
"""Every other column of the product table is one of the 59 coded fields that the counts are built from."""

STATIC_FIELDS = (
    ("pre_loans_credit_limit", 5),
    ("pre_pterm", 5),
    ("pre_loans_credit_cost_rate", 4),
    ("enc_loans_credit_type", 3),
    ("enc_loans_account_cur", 2),
    ("enc_loans_account_holder_type", 3),
    ("pclose_flag", 1),
)
"""The product fields that do not change between two bureau reports of the same product (its limit, planned term,
cost, type, currency, the client's relation to it), with the bits each code needs; they link two applications of one
client (`client_keys`)."""
LINK_MIN_PRODUCTS = 6
"""An application links to a later one when its whole history, read on `STATIC_FIELDS`, is the start of the later
history (rn orders the products by opening date, so a later report appends the newer products) or equals it, and the
earlier history holds at least this many products (shorter ones match by chance too often)."""

ONE_PRODUCT_CODES = ("pre_loans_total_overdue__0", "pre_loans_total_overdue__1", "pre_loans_max_overdue_sum__0")
"""`pre_loans_total_overdue` (current overdue debt) has code 1 on one product of the 26,162,717 (application
1,447,962) and code 0 on all others, so its count of code 0 equals `n_products` on every other application; code 0 of
`pre_loans_max_overdue_sum` occurs on that same product only. The three counts are dropped. Five more codes of other
fields occur on a single product each, in other applications; they stay."""

WINDOW = 500_000
"""Applications per test window: the competition tested on the 500,000 applications after its 3,000,000 training ones
(test_target.csv)."""
SPLIT_WINDOWS = TemporalSplits(window=WINDOW, unit="rows", n_windows=3)
BUDGET = RowBudget(train=1_000_000, test=500_000)
"""TabArena v0.2's row budget; applied in `_make_splits`, since `row_budget` cannot be declared next to it."""


def _mix64(x: np.ndarray) -> np.ndarray:
    """The splitmix64 finalizer: a fixed bijective mix of 64-bit integers (the same on every machine)."""
    x = (x ^ (x >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    x = (x ^ (x >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return x ^ (x >> np.uint64(31))


def _read_products(path: Path) -> pd.DataFrame:
    """One product file, with the ids as int32 and the codes as int16 (checked to round-trip)."""
    raw = pd.read_parquet(path)
    small = raw.astype({c: np.int32 if c == "id" else np.int16 for c in raw.columns})
    assert all((small[c].to_numpy() == raw[c].to_numpy()).all() for c in raw.columns), (
        f"{path.name}: a value overflowed"
    )
    return small


def count_features(products: pd.DataFrame, fields: list[str]) -> pd.DataFrame:
    """Per application: the number of products, and per field and code the number of products with that code.

    The organisers' boosting baseline (one-hot encode every field, sum per application) plus `n_products`. The codes of
    every field are interval or category numbers assigned at random by the organisers, so a count per code is the
    lossless summary; no order of the codes is assumed.
    """
    ids, row = np.unique(products["id"].to_numpy(), return_inverse=True)
    n_products = np.bincount(row, minlength=len(ids))
    assert n_products.max() < 2**8, "a count does not fit in uint8"
    columns = {"n_products": n_products.astype(np.uint8)}
    for field in fields:
        codes, code = np.unique(products[field].to_numpy(), return_inverse=True)
        counts = np.bincount(row * len(codes) + code, minlength=len(ids) * len(codes)).reshape(len(ids), len(codes))
        for j, value in enumerate(codes):
            columns[f"{field}__{value}"] = counts[:, j].astype(np.uint8)
    return pd.DataFrame(columns, index=pd.Index(ids, name="id"))


def client_keys(products: pd.DataFrame) -> pd.Series:
    """Per application: the smallest id among the applications linked to it (`LINK_MIN_PRODUCTS`), or its own id.

    Each product's `STATIC_FIELDS` are packed into one integer and mixed; a history's prefix of length k is the sum of
    its first k mixed products, each times a fixed mix of its position (64-bit, wrapping). An application of at least
    `LINK_MIN_PRODUCTS` products links to every other application whose prefix of the same length has the same value;
    linked applications are joined into connected components.
    """
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components

    ordered = products.sort_values(["id", "rn"], kind="stable")
    packed = np.zeros(len(ordered), dtype=np.uint64)
    for field, bits in STATIC_FIELDS:
        values = ordered[field].to_numpy().astype(np.int64)
        assert ((values >= 0) & (values < 2**bits)).all(), f"{field} does not fit in {bits} bits"
        packed = (packed << np.uint64(bits)) | values.astype(np.uint64)
    ids = ordered["id"].to_numpy().astype(np.int64)
    position = ordered["rn"].to_numpy().astype(np.uint64)
    with np.errstate(over="ignore"):
        term = _mix64(packed + np.uint64(1)) * (_mix64(position + np.uint64(0x9E3779B97F4A7C15)) | np.uint64(1))
        running = np.cumsum(term, dtype=np.uint64)
    starts = np.r_[True, ids[1:] != ids[:-1]]
    group = np.cumsum(starts) - 1
    before = np.r_[np.uint64(0), running[:-1]][np.flatnonzero(starts)]
    with np.errstate(over="ignore"):
        prefix = running - before[group]
    length = np.bincount(group)[group]
    rn = ordered["rn"].to_numpy()
    frame = pd.DataFrame({"id": ids, "k": rn, "prefix": prefix})
    full = frame[(rn == length) & (rn >= LINK_MIN_PRODUCTS)]
    prefixes = frame[rn >= LINK_MIN_PRODUCTS]
    links = full.merge(prefixes, on=["k", "prefix"], suffixes=("_a", "_b"))
    links = links[links["id_a"] != links["id_b"]]

    all_ids = np.unique(ids)
    index = pd.Index(all_ids)
    x, y = index.get_indexer(links["id_a"]), index.get_indexer(links["id_b"])
    graph = coo_matrix((np.ones(len(x), dtype=np.int8), (x, y)), shape=(len(index), len(index)))
    _, component = connected_components(graph, directed=False)
    smallest = pd.Series(all_ids).groupby(component).transform("min").to_numpy()
    return pd.Series(smallest, index=pd.Index(all_ids, name="id"), name="client_key")


class AlfaBankCreditHistoryDefault1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Will an applicant default on the loan the bank issues, judged from the credit-bureau history?",
        use_case=(
            "When a client applies for a loan, Alfa-Bank scores the applicant from the credit-bureau report, the past "
            "credit products with their limits, balances and late payments, to decide whether to issue it."
        ),
        row=(
            "One loan application with a label, that is a loan the bank issued (3,000,000 in the competition's "
            "training set), with the client's bureau history up to the application."
        ),
        predicted="Whether the client defaulted on the loan (3.5% did); the source states no horizon.",
        known=(
            "The number of past credit products and, for each coded field of a product, how many products carry each "
            "code (417 counts); the amounts and day counts arrive cut into intervals numbered at random."
        ),
        split=(
            "Each test window is 500,000 consecutive applications, as the competition tested on the 500,000 after its "
            "training ones; training is a random million of all earlier ones, without other applications of the "
            "window's clients."
        ),
        changes=(
            "We count the codes of each application's products as the organisers' baseline did, split the labelled "
            "applications by their order, as the test labels are not public, and remove linked earlier applications."
        ),
        fit="approximate",
        fit_reason=(
            "The bureau report is the bank's real input at application, but the values are cut into intervals numbered "
            "at random, there are no dates, and a default has no stated horizon, so the newest labels may be immature."
        ),
    )

    # Dataset
    unique_name = "alfa_bank_credit_history_default_1m"
    version_of = "alfa_bank_credit_history_default"
    version_comment = """
        We sample per test window: each window keeps its 500,000 applications, and its train side is a random 1M of all earlier applications that remain after the repeat-client filter, drawn in one random order for all windows (stratified on the target); the frame keeps only the rows a split uses. The full table has 3,000,000 applications, so every train side (1.5M to 2.5M) is over TabArena v0.2's budget of 1M.
    """
    year = "2022"
    domain = "finance"
    source = "Other"
    source_url = "https://ods.ai/competitions/dl-fintech-bki"
    license = (
        "Competition rules (Data Fest 2022 rules, 6.1.5 and 6.1.9): participants must not reproduce, publish or pass "
        "on the data without the organiser's consent. The organiser still hosts the files without a login on ODS.ai; "
        "the later Hugging Face copy mllab/alfa_bki (2023) is labelled CC BY 4.0 by its uploader"
    )
    data_tags = ("Anonymized",)
    download_description = """
        The organiser's files on the competition's data tab (https://ods.ai/competitions/dl-fintech-bki/data), downloadable without a login (checked 2026-11-09). We download the labelled training files; the test labels were never released.

        mkdir -p local-data-warehouse/alfa_bank_credit_history_default && cd local-data-warehouse/alfa_bank_credit_history_default
        wget https://storage.yandexcloud.net/ds-ods/files/materials/3c36dbad/train_target.csv
        wget https://storage.yandexcloud.net/ds-ods/files/materials/f020b5d6/train_data.zip
        wget https://storage.yandexcloud.net/ds-ods/files/materials/12a02f6d/description.xlsx
        unzip train_data.zip && rm train_data.zip

        This gives train_target.csv (28,888,898 bytes, sha256 9aa12a8e...7df9), description.xlsx and the 12 files train_data/train_data_<0-11>.pq (403,391,940 bytes; 26,162,717 product rows of 3,000,000 applications). Fallback: the Hugging Face copy pytorch-lifestream/alfa-scoring-bki (same row counts, 2026-11-08). `_prepare_raw_files` counts the codes per application once into application_features.parquet.
    """
    bibtex = r"""
        @misc{AlfaBank2022CreditHistories,
          author = {{Alfa-Bank} and {Open Data Science}},
          title  = {Data Fest 2022: Credit Scoring Competition on Credit History Data},
          year   = {2022},
          howpublished = {\url{https://ods.ai/competitions/dl-fintech-bki}},
          note   = {Data science competition on ODS.ai, 4 June to 31 July 2022; baselines at https://github.com/SmirnovValeriy/dl-fintech-bki}
        }
    """
    curation_comments = """
        We start with train_target.csv and the 12 product files train_data/train_data_*.pq of the Data Fest 2022 credit-history competition (Alfa-Bank with ODS.ai), from the organiser's files on ODS.ai.

        - Prediction point: a client applies for a loan. The bank knows the client's credit-bureau history "up to the moment of the application" (organisers' baseline notebook: "кредитной истории клиента до момента подачи заявки на новый кредит"); every day count of a product runs to the "date of data collection", which is that moment. The loan applied for is not in its own history: only 23% of applications have their newest product in the most recent opening interval (the order of the intervals recovered from `rn`, in the note on the rules below), where a later report would put it for all of them (LEAK-10). The target `default` is the source's `flag`, "1 - факт ухода клиента в дефолт" (1: the client defaulted on the loan), with no horizon stated; 106,442 of 3,000,000 applications (3.55%).
        - Features: the source is a sequence of credit products per application (8.7 on average, 1 to 58), each with 59 coded fields. We count, per application, the products with each code of each field (`{field}__{code}`, 419 counts, 416 after the drop below), as the organisers' boosting baseline did (CV ROC AUC 0.763, about 0.795 on the public test; https://github.com/SmirnovValeriy/dl-fintech-bki, gb_baseline), and add the number of products (`n_products`). No top solution is published (searched the ODS page, GitHub and Habr, 2026-11-09); the best private score was 0.783 ROC AUC. Counts stay numeric (CLEAN-14: an aggregate over a history). The counts are a bag of codes: they lose the order of the products and how recent each one is, which the sequence models of the competition used, so scores stay below theirs (untuned LightGBM 0.73 ROC AUC on our windows against 0.783 best private on the sequences; CLEAN-19).
        - Encoding: the organisers cut every amount, day count and ratio into intervals and numbered the intervals at random, and recoded every categorical field to random integers (description of the fields, data tab), so the codes carry no order and no field can be put back on its scale; we keep them as published (`Anonymized`). The fields themselves are documented: days since opening and to the planned and actual closing, limit, next payment, outstanding and overdue amounts, cost of credit, late-payment counts by bucket, utilisation ratios, 25 monthly payment statuses, the client's relation to the product, its status, currency and type.
        - Potential leak, kept on purpose: the organisers' intervals were cut before release, over data that likely held the test applications too (the counts per interval of `pre_loans_credit_limit` are near even, 18 of 20 between 1.0M and 1.5M of 26.2M products, as quantile intervals give). A label-free transform over all rows is a weak leak (LEAK-30); the cut points are not published, so it cannot be undone.
        - Note: the competition rules call the data "fictitious credit histories" of a "fictitious client" (rules 3.3), while the competition page calls them carefully anonymised data of Alfa-Bank's clients. The table shows the structure of a real bureau extract: every `is_zero_*`, `pclose_flag` and `fclose_flag` = 1 falls into a single code of the field it summarises (the interval holding zero), and `rn`, which orders the products by opening date, moves `pre_since_opened` one way in 99.53% of the 14.8M changes between consecutive products (42% the other way with the pairs shuffled), so the random interval numbers keep one order. No row-counter pattern (codes against the id modulo k < 200) and no too-even marginals beyond the quantile intervals.
        - Time: the data has no dates, but the organiser's description of the fields states the order (description.xlsx, sheet 1, row `id`, re-read 2026-11-09): "Идентификатор заявки. Заявки пронумерованы так, что более поздним заявкам соответствует более поздняя дата." (Application id. The applications are numbered so that a later application has a later date.) Also the 12 files hold consecutive blocks of 250,000 ids. We keep `id` as the time column `time_index` (SPLIT-7, SPLIT-22).
        - Dropped: `pre_loans_total_overdue` (current overdue debt) has code 1 on one product of the 26,162,717 and code 0 on all others, so its count of code 0 equals `n_products` on every other application; code 0 of `pre_loans_max_overdue_sum` sits on that same product. The three counts go (`ONE_PRODUCT_CODES`). Code 0 is not "no overdue debt": by `is_zero_over2limit`, 7% of products have some, so the organisers' intervals put all values but one into one interval and the field carries nothing as published. Five other codes occur on one product each and stay.
        - Repeat clients: there is no client id, but a client's later bureau report lists the same products again, with the newer ones after them. We link two applications when the earlier history, read on the fields that do not change between reports (`STATIC_FIELDS`), is the start of the later one or equals it, over at least 6 products (`client_keys`): 60,048 links join 103,519 applications (3.5%) into 48,841 clients. Over linked pairs the later application defaults in 89.0% of cases when the earlier one did and in 2.0% when it did not, while the earlier one had defaulted in only 47.3% of the later defaults: the earlier flag was most likely set after the later application, so it carries the later application's own outcome (SPLIT-9, as for alfa_battle_2_0_task_2). `_make_splits` removes from each training side the applications linked to an application of the test window, 7,743 to 13,224 per window (first decision); in the newest window the 131 test applications whose linked earlier application defaulted default at 71.0%, the other linked ones at 2.3% and the unlinked ones at 3.3%. Untuned LightGBM on 1M training rows gains -0.0007 to +0.0019 ROC AUC from the linked rows on the whole window and +0.0024 to +0.0102 on the linked test applications (one draw per window; two draws from one pool differ by 0.0016). Histories under 6 products are not linked, so the filter is partial; at 6 products and more, links at long distance agree less (later default after an earlier one: 53% for pairs over 1,000,000 ids apart, against 91% within 300,000), so some links are chance matches, which only cost training rows.
        - Note: the newest 120,000 applications default at 2.5% to 2.9% per block of 20,000, against 3.0% to 4.5% in the 300,000 before (leak probe 13 on 40 periods: the newest two pooled at z -3.6; second decision). A model trained on the applications before 2,500,000 predicts most of the fall: its mean prediction drops from 3.6% to 2.9-3.1% there, and the observed minus predicted rate (-0.2 to -0.5 points) stays within that of the blocks from 2,620,000 to 2,740,000 (-0.3 to -0.5). So it reads as a change in who applied more than as defaults not yet flagged (LEAK-24); the organiser released one extraction, so no later labels can settle it.
        - Duplicates: with `time_index` no two applications are equal. Without it, 53,699 applications share their counts with another (17,048 profiles, 53,079 of them one-product histories), 12,743 of them in profiles with both labels: natural repeats of coarse codes (LEAK-18), kept. Of the 300 applications with an identical history of 5 or more products (150 pairs), every pair shares its label: the same client's report twice; at 6 products and more they are linked.
    """

    # Task
    target = "default"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="ROC AUC",
        reference=(
            "https://ods.ai/competitions/dl-fintech-bki (Проверка решений: 'Метрика соревнования – ROC AUC'; scored "
            "on the private part of the test set)"
        ),
        definition="ROC AUC of the default flag per application",
    )

    # Splits
    splits_comment = """
        A scoring model is refit on the applications so far and used on the next ones. We use 3 test windows of 500,000 consecutive applications, newest first: ids 2,500,000-2,999,999, 2,000,000-2,499,999 and 1,500,000-1,999,999, each training on the applications before it, which hold 83%, 67% and 50% of the rows (SPLIT-11, SPLIT-14). The window is the competition's own: it trained on 3,000,000 applications and tested on the next 500,000 (ids 3,000,000-3,499,999 in test_target.csv), whose labels are not public, so we cut the labelled applications by their stated order (SPLIT-12, SPLIT-19). The window is a count of applications because the data has no dates; the months it spans are unknown (the competition: "M months" of training, "the following K months" of test).
        From each training side we remove the applications linked to an application of the test window (curation_comments, "Repeat clients"; 13,224, 10,642 and 7,743): their default flags were most likely not known when the test applications were made (SPLIT-9). Then each training side is a random 1,000,000 of what remains (one random order for all windows, stratified on the target) and each window keeps its 500,000 rows. So of the 3,000,000 source applications the frame keeps 2,503,777: the 1,500,000 of the three test windows and the 1,003,777 earlier ones (about two thirds of the ids below 1,500,000) that a training sample draws; the rest leave through the row budget and the repeat-client removal, and no row is filtered by its target. The budget is applied in `_make_splits`, so the container records no `row_budget`.
        No gap, an exception to SPLIT-10 that serves SPLIT-14's training floor, as for alfa_battle_2_0_task_2 (2026-10-21): none of the conditions of SPLIT-10 as amended 2026-11-05 for no gap holds, as the default has no stated horizon and the data no label dates, so a refit at a window's start would not yet have known every training label. The measurements show no shortcut beyond the repeat clients removed above, and the fall of the default rate at the release end follows the applicants (curation_comments). A gap of 250,000 applications, half a window, costs untuned LightGBM 0.0015 and 0.0010 ROC AUC on the two newest windows at equal training size (500,000 rows, two draws each, which differ by up to 0.003): an upper bound on what the newest training labels add, as it mixes in the cost of older data. Such a gap would leave the oldest window 42% of the rows (SPLIT-14).
    """
    temporal = Temporal(on="time_index", horizon=WINDOW, horizon_unit="steps")

    # The product table (26M rows) is counted and linked once; `_load_raw` starts from the result.
    prepared_raw_files = (FEATURES_FILE,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        paths = sorted((raw_dir / TRAIN_DIR).glob("train_data_*.pq"))
        assert len(paths) == 12, f"expected 12 product files, found {len(paths)}"
        # int64 as published; every code fits in int16 and every id in int32 (asserted by the cast's round trip)
        products = pd.concat([_read_products(p) for p in paths], ignore_index=True)
        products = products.sort_values(["id", "rn"], kind="stable").reset_index(drop=True)
        fields = [c for c in products.columns if c not in SKIPPED_FIELDS]
        assert len(fields) == 59, f"expected 59 product fields, found {len(fields)}"
        features = count_features(products, fields)
        features["client_key"] = client_keys(products).reindex(features.index).to_numpy()
        features.reset_index().to_parquet(raw_dir / FEATURES_FILE, index=False)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        target = pd.read_csv(raw_dir / TARGET_FILE)
        features = pd.read_parquet(raw_dir / FEATURES_FILE)
        return target.merge(features, on="id", how="inner", validate="one_to_one")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.copy()
        assert len(df) == 3_000_000, len(df)
        # 1. The target as words, "Yes" the default (CLEAN-25).
        df = decode(df.rename(columns={"flag": self.target}), {self.target: {0: "No", 1: "Yes"}})
        # 2. The application id is the time order (description.xlsx); it stays as the time column.
        df = df.rename(columns={"id": "time_index"})
        # 3. A field with one code on all products but one, and the codes of that one product (ONE_PRODUCT_CODES).
        total_overdue, one_product, max_overdue = ONE_PRODUCT_CODES
        assert ((df[total_overdue] != df["n_products"]).sum(), (df[one_product] > 0).sum()) == (1, 1)
        assert (df[max_overdue] == df[one_product]).all(), f"{max_overdue} no longer marks the same product"
        df = drop_columns(df, list(ONE_PRODUCT_CODES))
        # 4. `client_key` links applications of one client; `_make_splits` uses it and drops it.
        return df

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        # The windows, then each training side without the applications linked to the window's, then the budget.
        windows = SPLIT_WINDOWS.splits(df, self.temporal.on)
        client = df["client_key"].to_numpy()
        splits = {}
        for repeat, folds in windows.items():
            train, test = (np.asarray(side) for side in folds[0])
            same_client = np.isin(client[train], np.unique(client[test]))
            splits[repeat] = {0: (train[~same_client].tolist(), test.tolist())}
        df, splits, trimmed = sample_temporal_splits(
            df, splits, BUDGET, stratify_on=self.target, random_state=self.SPLIT_RANDOM_STATE
        )
        assert trimmed, "no split side exceeds the row budget"
        return SplitPlan(splits=splits, df=drop_columns(df, ["client_key"]))

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        frame = raw[["id", "flag", "client_key"]].sort_values("id", kind="stable").reset_index(drop=True)
        rows = []
        for repeat, folds in SPLIT_WINDOWS.splits(frame, "id").items():
            train, test = frame.iloc[folds[0][0]], frame.iloc[folds[0][1]]
            removed = train[train["client_key"].isin(test["client_key"])]
            earlier = removed.groupby("client_key")["flag"].max()  # 1 when any linked earlier application defaulted
            linked = test[test["client_key"].isin(earlier.index)]
            earlier_flag = linked["client_key"].map(earlier)
            others = test[~test["client_key"].isin(earlier.index)]
            rows.append(
                {
                    "split": repeat,
                    "test ids": f"{test['id'].min():,}-{test['id'].max():,}",
                    "training applications removed": len(removed),
                    "test applications with a linked earlier one": len(linked),
                    "of them, the earlier one defaulted": int((earlier_flag == 1).sum()),
                    "their default rate": round(float(linked["flag"][earlier_flag == 1].mean()), 3),
                    "default rate when it did not": round(float(linked["flag"][earlier_flag == 0].mean()), 4),
                    "default rate of the other test applications": round(float(others["flag"].mean()), 4),
                }
            )
        blocks = frame.groupby(frame["id"] // 100_000 * 100_000)["flag"].agg(["size", "mean"])
        blocks = blocks.rename(columns={"size": "applications", "mean": "default rate"}).round(4)
        blocks.index.name = "first id of the block"
        return [
            Decision(
                title="Training sides without the earlier applications of the test window's clients",
                why=(
                    "A client's earlier application, linked by its bureau history (`client_keys`), carries the later "
                    "one's outcome: its default flag was most likely set after the later application. `_make_splits` "
                    "removes these earlier applications from each training side (SPLIT-9)."
                ),
                evidence=pd.DataFrame(rows).set_index("split"),
            ),
            Decision(
                title="The default rate by block of 100,000 applications",
                why=(
                    "The newest block defaults at 2.6% against 3.1% to 4.2% before, as immature labels at the release "
                    "end would (LEAK-24). A model trained on the earlier applications predicts most of the fall (its "
                    "mean prediction drops from 3.6% to 3.0%), so the rows are kept (curation_comments)."
                ),
                evidence=blocks,
            ),
        ]

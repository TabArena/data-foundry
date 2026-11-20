"""Curated dataset definition for `santander_customer_satisfaction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Metric, Source, TaskSummary, decode

# The column dictionary (Andrej, 2026-11-06): our reading of the masked columns from the data (review of 2026-11-05),
# not Santander's. A column's confidence is the lower of its rule's (what kind of value it is) and its product's.
CONFIDENCE_LEVELS = ("unknown", "low", "medium", "high")

# varN (the product a column is about) -> (likely meaning, confidence, evidence)
PRODUCTS = {
    "var1": ("loans", "medium", "var18 + var34; `amort` (repayments); 0.4% hold one"),
    "var5": ("the current account", "medium", "66% have money in it, median 10 €"),
    "var6": ("a rare account", "low", "part of the var42 sum"),
    "var7": ("likely transfers", "low", "`emit`/`recib`, round amounts"),
    "var8": ("an account", "low", "part of the var42 sum"),
    "var9": ("an unknown product", "unknown", ""),
    "var10": ("an unknown product", "unknown", ""),
    "var11": ("an unknown product", "unknown", ""),
    "var12": ("a group of accounts", "medium", "var24 + var14 + var20 in every row"),
    "var13": ("term deposits", "high", "round amounts of 10,000 to 100,000 € once divided by 3"),
    "var13_corto": ("short-term deposits", "high", "`corto`; part of the var13 sum"),
    "var13_medio": ("medium-term deposits", "high", "`medio`; part of the var13 sum"),
    "var13_largo": ("long-term deposits", "high", "`largo`; part of the var13 sum"),
    "var14": ("an account", "low", "part of the var12 sum"),
    "var16": ("likely cash flows", "low", "`ent`/`sal`, round amounts"),
    "var17": ("funds or pension plans", "medium", "`aport`, `reemb`, `trasp`; var33 is the other of the two"),
    "var18": ("a loan", "medium", "part of the var1 sum; `amort` (repayments)"),
    "var19": ("an unknown product", "unknown", ""),
    "var20": ("an account", "low", "part of the var12 sum"),
    "var22": ("an unknown count", "unknown", ""),
    "var24": ("an account", "low", "part of the var12 sum"),
    "var25": ("an unknown product", "unknown", "part of the var26 sum"),
    "var26": ("an unknown product group", "unknown", "var25 + var32 in every row"),
    "var29": ("a rare account", "low", "part of the var42 sum"),
    "var30": ("accounts and term deposits", "medium", "var42 + var13 in every row"),
    "var31": ("investments", "medium", "var17 + var33 + var44 in every row"),
    "var32": ("an unknown product", "unknown", "part of the var26 sum"),
    "var33": ("funds or pension plans", "medium", "`aport`, `reemb`, `trasp`; var17 is the other of the two"),
    "var34": ("a loan", "medium", "part of the var1 sum; `amort` (repayments)"),
    "var37": ("an unknown product", "unknown", ""),
    "var39": ("all cards", "medium", "var40 + var41 in every row"),
    "var40": ("a credit card", "medium", "1.2% hold one, with a balance"),
    "var41": ("a debit card", "medium", "88% hold one, never a balance"),
    "var42": ("all accounts", "medium", "var5 + var8 + var6 + var29 + var12 in every row"),
    "var43": ("likely transfers", "low", "`emit`/`recib`, round amounts of 30 to 1,000 €"),
    "var44": ("securities", "medium", "`compra`/`venta` (buy/sell)"),
    "var45": ("an unknown count", "unknown", ""),
}

# The words of the column names: period (t), card use (k), amount or count (f), action (a), direction (d)
NAME_PARTS = {
    "t": {
        "ult1": "in the last month",
        "ult3": "over the last 3 months",
        "hace2": "2 months ago",
        "hace3": "3 months ago",
    },
    "k": {None: "", "comer": " in shops", "efect": " as cash withdrawals"},
    "f": {"imp": "amount", "num": "number"},
    "a": {
        "aport": "contributions",
        "reemb": "redemptions",
        "compra": "purchases",
        "venta": "sales",
        "amort": "repayments",
    },
    "d": {"in": "into", "out": "out of", "ent": "coming in", "sal": "going out", "emit": "sent", "recib": "received"},
}

_V = r"(?P<v>var\d+(?:_corto|_medio|_largo)?)"
# (regex on the whole name, meaning, confidence of the kind of value, evidence); every column matches exactly one
COLUMN_RULES = [
    (r"var15", "age of the customer, in years", "high", "5 to 105; older customers hold more products"),
    (
        r"var38",
        "gross household income, times 3; 117,310.98 means none on file (the mean of the others)",
        "high",
        "its values match `renta` of Santander's Product Recommendation data (curation notes)",
    ),
    (r"var3", "a country code (nationality or birth), 2 = Spain; -999999 set to missing", "low", "231 codes, 97.6% 2"),
    (r"var36", "a customer category; 99 = none", "low", "63% of the 99s hold no product"),
    (r"var21", "a credit limit, times 3", "low", "round amounts of 300 to 10,000 € once divided by 3; 1.2% have one"),
    (r"num_var4", "number of products held", "medium", "0 to 9, not times 3; the product flags add up to it"),
    (r"num_var35", "number of products held, times 3", "medium", "3 times `num_var4` in 98% of rows"),
    (r"zero_count", "number of zero cells in the row (added by us)", "high", "built in `_clean`"),
    (rf"ind_{_V}_0", "holds {product}", "high", "implied by `ind_X`; `num_X_0` counts the contracts"),
    (rf"ind_(?!var19$){_V}", "has money in {product}", "high", "1 exactly when `saldo_X` is not zero, in every row"),
    (r"ind_(?P<v>var19)", "a flag of {product}", "unknown", "no amount or count of it ships"),
    (r"ind_(?P<v>var\d+)_cte", "a `cte` flag of {product}", "unknown", "only 0 and 1"),
    (r"ind_(?P<v>var(?:9|10))_?(?:cte_)?ult1", "a flag of {product} in the last month", "unknown", "only 0 and 1"),
    (r"ind_(?P<v>var\d+)_(?P<d>emit|recib)_ult1", "{product}: any {d} in the last month", "medium", "the name"),
    (rf"num_{_V}_0", "number of contracts held in {product}, times 3", "high", "0 exactly when `ind_X_0` is; times 3"),
    (
        rf"num_(?!var4$|var35$){_V}",
        "number of contracts with money in {product}, times 3",
        "high",
        "0 exactly when `saldo_X` is; times 3",
    ),
    (
        rf"saldo_{_V}",
        "balance of {product}, times 3",
        "high",
        "multiples of 0.03; the balances add up (curation notes)",
    ),
    (rf"saldo_medio_{_V}_(?P<t>ult1|ult3|hace2|hace3)", "mean balance of {product} {t}, times 3", "high", "the name"),
    (rf"num_meses_{_V}_ult3", "months with money in {product}, of the last 3", "high", "values 0 to 3"),
    (r"num_meses_(?P<v>var39)_vig_ult3", "months with {product} in force (`vig`), of the last 3", "low", "mostly 2"),
    (
        r"imp_op_(?P<v>var39|var40|var41)(?:_(?P<k>comer|efect))?_(?P<t>ult1|ult3)",
        "amount spent with {product}{k} {t}, times 3",
        "high",
        "cash withdrawals in tens of euros once divided by 3",
    ),
    (
        r"num_op_(?P<v>var39|var40|var41)(?:_(?P<k>comer|efect))?_(?P<t>ult1|ult3|hace2|hace3)",
        "number of operations with {product}{k} {t}, times 3",
        "high",
        "`ult3` = `ult1` + `hace2` + `hace3` in every row",
    ),
    (
        r"(?P<f>imp|num)_(?P<a>aport|reemb|compra|venta)_(?P<v>var\d+)_(?P<t>ult1|hace3)",
        "{f} of {a} in {product} {t}, times 3",
        "high",
        "the name; times 3",
    ),
    (
        r"(?P<f>imp|num)_trasp_(?P<v>var\d+)_(?P<d>in|out)_(?P<t>ult1|hace3)",
        "{f} of transfers {d} {product} {t}, times 3",
        "high",
        "the name; times 3",
    ),
    (r"num_trasp_(?P<v>var11)_ult1", "number of transfers of {product} in the last month, times 3", "high", "the name"),
    (r"imp_amort_(?P<v>var\d+)_ult1", "amount repaid on {product} in the last month, times 3", "high", "the name"),
    (
        r"delta_(?P<f>imp|num)_(?P<a>aport|reemb|compra|venta|amort)_(?P<v>var\d+)_1y3",
        "change of the {f} of {a} in {product}, the last month against the last 3",
        "high",
        "-1 when it fell to zero; 9999999999 where the base is zero",
    ),
    (
        r"delta_(?P<f>imp|num)_trasp_(?P<v>var\d+)_(?P<d>in|out)_1y3",
        "change of the {f} of transfers {d} {product}, the last month against the last 3",
        "high",
        "-1 when it fell to zero; 9999999999 where the base is zero",
    ),
    (
        r"(?P<f>imp|num)_(?P<v>var7|var43)_(?P<d>emit|recib)_ult1",
        "{product}: {f} {d} in the last month, times 3",
        "high",
        "the name; times 3",
    ),
    (
        r"(?P<f>imp|num)_(?P<d>ent|sal)_(?P<v>var16)_ult1",
        "{product}: {f} {d} during the last month, times 3",
        "high",
        "the name; times 3",
    ),
    (r"imp_trans_(?P<v>var37)_ult1", "amount of `trans` in {product} in the last month, times 3", "high", "times 3"),
    (r"num_(?P<v>var37)_med_ult2", "a mean count of {product} over 2 months, times 3", "high", "multiples of 3"),
    (r"num_(?P<v>var22|var45)_(?P<t>ult1|ult3|hace2|hace3)", "a count of {product} {t}, times 3", "high", "times 3"),
    (
        r"num_med_(?P<v>var22|var45)_ult3",
        "a mean monthly count of {product} over the last 3 months, times 3",
        "high",
        "multiples of 3",
    ),
]


def column_dictionary(columns: list[str]) -> pd.DataFrame:
    """Return each column's likely meaning, confidence and evidence from ``COLUMN_RULES`` and ``PRODUCTS``.

    Args:
        columns: The feature columns of the curated frame.

    Returns:
        One row per column, in the given order.
    """
    rows = []
    for column in columns:
        matches = [(rule, m) for rule in COLUMN_RULES if (m := re.fullmatch(rule[0], column))]
        assert len(matches) == 1, f"{column}: {len(matches)} dictionary rules match, expected exactly one"
        (_, meaning, confidence, evidence), m = matches[0]
        parts = {key: NAME_PARTS[key][value] for key, value in m.groupdict().items() if key in NAME_PARTS}
        product = m.groupdict().get("v")
        if product is not None:
            name, product_confidence, product_evidence = PRODUCTS[product]
            parts["product"] = f"{name} ({product})"
            confidence = min(confidence, product_confidence, key=CONFIDENCE_LEVELS.index)
            evidence = "; ".join(e for e in (evidence, product_evidence) if e)
        rows.append(
            {
                "column": column,
                "likely meaning": meaning.format(**parts),
                "confidence": confidence,
                "evidence": evidence,
            }
        )
    return pd.DataFrame(rows)


class SantanderCustomerSatisfaction(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a bank customer dissatisfied?",
        use_case=(
            "Santander wants to identify dissatisfied customers early in their relationship, to act before they leave"
            " (the competition's stated aim)."
        ),
        row=("One customer of Santander bank (71,080 customers); the country and period are not stated."),
        predicted=("Whether the customer is dissatisfied (3.8% are); how and when this was measured is not stated."),
        known=(
            "About 300 anonymised numbers whose meanings are not given, plus the count of zeros in the row, which we "
            "add."
        ),
        split="Random customers, so the test data stands for other customers of the same time.",
        changes=(
            "We add the count of zeros per row, as top competition solutions did, and drop repeated rows and columns."
        ),
        fit="approximate",
        fit_reason=(
            "The label has no stated definition or horizon, and whether the anonymised features were recorded before "
            "it is not stated. The competition's winners used a random split, as here."
        ),
    )

    # Dataset
    unique_name = "santander_customer_satisfaction"
    domain = "business & marketing"
    sources = (
        Source(
            role="publication",
            platform="Kaggle",
            url="https://www.kaggle.com/competitions/santander-customer-satisfaction",
            license="Kaggle Competition Rules",
            year="2016",
            bibtex=r"""
                @misc{Jimenez2016SantanderCustomerSatisfaction,
                  author = {Soraya Jimenez and Will Cukierski},
                  title  = {Santander Customer Satisfaction},
                  year   = {2016},
                  howpublished = {\url{https://kaggle.com/competitions/santander-customer-satisfaction}},
                  note   = {Kaggle competition}
                }
            """,
        ),
    )
    data_tags = ("Anonymized", "Retrospective")
    download_description = """
        We use the train.csv from the Kaggle competition.

        kaggle competitions download -c santander-customer-satisfaction -f train.csv && unzip train.csv.zip &&  rm train.csv.zip
        mkdir -p local-data-warehouse/santander_customer_satisfaction && mv train.csv local-data-warehouse/santander_customer_satisfaction/
    """
    curation_comments = """
        We start with the train.csv from Kaggle (76,020 customers, 369 masked columns and `TARGET`).

        - The column names are masked, and Santander gave no data dictionary (Kaggle staff:
          https://www.kaggle.com/competitions/santander-customer-satisfaction/discussion/19291). The notes on the
          masking, the columns, `var38` and the households below say what the data shows about them (review of
          2026-11-05, on train.csv and test.csv together, 151,838 customers).
        - We remove duplicated columns and zero-variance columns.
        - We add a zero-count feature (number of zeros per row). #1 Kaggle experts also applied a lot of other features and feature selection but each experts used something different (https://www.kaggle.com/competitions/santander-customer-satisfaction/writeups/1-leustagos-3rd-place-solution).
        - We drop duplicates as their origin is unclear and they could create data leaks when splitting the training data.
        - We replace -999999 in var3 with nan.
        - We keep the data otherwise as it. Several columns might be categorical and contain encoded nan values but we are not able to determine this due to anonymization.
        - The target (2026-11-01, CLEAN-25): `TARGET` ships its classes as words (1 is the event). Binary: "Yes" is the
          event, the class that sorts second, so it is the metrics' positive class.
        - Note (masking): every amount (`imp_`, `saldo_`, `var38`, `var21`) is the true value times 3, since all 122
          amount columns are multiples of 0.03; every count (`num_`, except `num_var4` and `num_meses_`) is times 3 too,
          since all 131 are multiples of 3. Divided by 3, cash withdrawals are 20, 40, 60 or 100 € and term deposits
          10,000 to 100,000 €. We keep the values as shipped: the factor changes no model's view of the data.
        - Note (columns): the names are Spanish banking terms (`imp` amount, `saldo` balance, `num` count, `ind`
          indicator, `ult1`/`ult3` the last 1 or 3 months, `hace2`/`hace3` 2 or 3 months ago, `aport` contribution,
          `reemb` redemption, `trasp` transfer, `amort` repayment, `comer` shop purchases, `efect` cash, `emit`/`recib`
          sent/received, `ent`/`sal` in/out). What the data shows, by confidence:
          - High: `ind_X` is 1 exactly when `saldo_X` is not zero (in every row), `ind_X_0` means the customer holds
            product X, and `num_X` is 3 times the flag. The balances add up in every row: var30 = var42 + var13, var42 =
            var5 + var8 + var6 + var29 + var12, var12 = var24 + var14 + var20, var13 = its `corto` + `medio` + `largo`,
            var31 = var17 + var33 + var44, var26 = var25 + var32, var1 = var18 + var34 (99.6% of rows). `saldo_medio_`
            is a mean balance, `num_meses_` the months with a balance out of the last 3, `delta_` the change of the last
            month against the last 3 (9999999999 where there is no base). `var15` is age (5 to 105, 27% are 23). var13
            is term deposits, short, medium and long term (round amounts).
          - Medium: var5 the current account (66% have money in it, median 10 €), var42 all accounts, var30 accounts and
            term deposits; var39 = var40 + var41 card spending, in shops (`comer`) and as cash (`efect`), with var41 a
            debit card (88% hold one, never a balance) and var40 a credit card (1.2%); var17 and var33 investment funds
            and pension plans (which is which is unknown), var44 securities bought and sold, var31 their total; var1
            loans (0.4% hold one); `num_var4` the number of products (0 to 9, not times 3; `num_var35` is 3 times it).
          - Low: var43 and var7 transfers sent and received, var16 money in and out; `var3` a country code with 2 for
            Spain (97.6% of customers), although 15% of minors have another code against 0.5% of 23- to 26-year-olds;
            `var36` a customer category with 99 for none; `var21` a credit limit (divided by 3, round amounts of 300 to
            10,000 €; 1.2% have one).
          - Unknown: var9, var10, var11, var19, var22, var45, var25, var26, var32 (`cte`) and var37. `ID` carries no
            order.
        - Note (column dictionary; Andrej, 2026-11-06): the column names stay as Santander shipped them. The README's
          decision "Column dictionary" gives every shipped column its likely meaning, a confidence (high, medium, low
          or unknown) and the evidence, from `COLUMN_RULES` and `PRODUCTS` at the top of this file; every column
          matches exactly one rule (asserted). The dictionary is our reading of the data, not Santander's, and changes
          no value.
        - Note (`var38`, high confidence): the bank's gross household income, times 3, not a mortgage as competitors
          guessed (0.4% of customers hold any loan).
          - The most frequent values of `renta` ("Gross income of the household") in Santander's Product Recommendation
            competition of 2016 recur here to the cent: its most frequent, 451,931.22, is the most frequent here too,
            and 7 of its 10 most frequent are among the 192 values that 5 or more customers share here, out of 109,981
            (https://www.kaggle.com/competitions/santander-product-recommendation/discussion/26786).
          - 81% of the customers without any product have a value, and it is unrelated to balances, product count and
            age (Spearman 0.01, -0.03, 0.00): an income on file, not a product. Divided by 3, its median is 29,600 €.
          - 117,310.98, held by 19.5% of customers, is the exact mean of all other values of train and test: no income
            on file, filled with the mean by Santander. We keep it as shipped: train and test have it alike.
        - Potential leak, kept on purpose (households; Andrej, 2026-11-06): customers who share an exact `var38` value
          (6,203 here, in 2,837 groups) are mostly members of one household, different people, so the random split
          keeps them on both sides.
          - What matches is what a household shares: 57% of minors share their value (18% of all customers), and the
            other member of a minor is a minor in 40% of pairs (random pairs: 0%); 79 pairs hold the same rare balance
            to the cent, a joint account, 87% of them within 5 years of age (no random pair does). Ages, cards and
            products differ as between different people (same age: 13% of pairs, 9% of random pairs).
          - Rejected readings: one person under two IDs (ages differ in 87% of pairs, and the rows differ as much as
            random pairs do); a place, such as an area or branch value (82% hold a value nobody else holds, children
            pair with children, and customers with the next value up show no label link). 15 values held by 6 to 16
            customers (122 customers) are defaults, among the most frequent `renta` values.
          - The label link: a customer with a dissatisfied member is dissatisfied in 17.9% of cases against 2.8% (in
            pairs of two, 21.9% against 3.0%). Under random splits 0.3% of test customers have such a member in
            training; the members' training labels as a feature move TabPFN-3.5 from 1-AUC 0.1567 to 0.1559 (about
            0.5%, 3 of 3 splits).
          - Why it stays: the bank keeps one income for all members of a household, so it sees a new customer's
            members, only not their label of the same period, and the link is small. Revisit if Santander states how
            and when the label was taken.
        - Time basis: Retrospective: one extract of Santander's customers (period not stated; competition 2016), with
          windows of the last month to three months ending at it; the label is a state the host does not define or
          date, read as dissatisfaction at the extract, which the use case fills in for customers not yet known to be
          dissatisfied. No exit trace in the last month: customers whose current account emptied in the last month are
          dissatisfied at 3.1%, against 1.8% for those who kept a balance (training file). Not tested: customers of a
          later extract, or a label taken after the extract.
    """

    # Task
    target = "TARGET"
    problem_type = "binary_classification"
    metric = Metric.source(
        "roc_auc",
        original="Area Under Receiver Operating Characteristic Curve",
        reference=("https://www.kaggle.com/competitions/santander-customer-satisfaction (Kaggle API evaluationMetric)"),
        definition="Area under the ROC curve of TARGET = 1.",
    )

    # Splits: the default random splits, stratified on the target
    splits_comment = """
        Default splits: random customers, stratified on `TARGET`, as the competition's winners validated. Members of one
        household (customers who share an exact `var38` value, the bank's household income) can fall on both sides, as
        for a bank that sees a new customer's household; 0.3% of test customers have a dissatisfied member in training
        (curation notes).
    """
    accepted_check_warnings = {
        "dataset_pure_feature_value": "All five values are term-deposit (var13) holdings: customers with a term "
        "deposit are 99.7% satisfied at a 96.2% base rate, an ordinary category effect on an imbalanced target, not a "
        "column derived from the outcome (review of 2026-11-04).",
    }

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "train.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # remove duplicated columns
        df = df.loc[:, ~df.T.duplicated()]
        # remove zero-variance columns
        df = df.loc[:, df.nunique(dropna=False) > 1]
        # add zero-count feature
        numeric_cols = df.drop(columns=["ID", "TARGET"])
        df["zero_count"] = (numeric_cols == 0).sum(axis=1)
        df = df.drop(columns=["ID"])
        # Drop duplicates w/o target col
        df = df.drop_duplicates(subset=df.columns.difference([self.task_metadata.target_column_name]))
        # Replace -999999 with np.nan
        df["var3"] = df["var3"].replace(-999999, np.nan)
        # the target's classes in words (CLEAN-25): "Yes" is the event the task predicts
        df = decode(df, {self.target: {"0": "No", "1": "Yes"}})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # the ind_var columns are indicators by their name (0/1): categorical (CLEAN-14); the other anonymized
        # features stay numeric
        del df
        flags = [
            "ind_var1_0",
            "ind_var1",
            "ind_var5_0",
            "ind_var5",
            "ind_var6_0",
            "ind_var6",
            "ind_var8_0",
            "ind_var8",
            "ind_var12_0",
            "ind_var12",
            "ind_var13_0",
            "ind_var13_corto_0",
            "ind_var13_corto",
            "ind_var13_largo_0",
            "ind_var13_largo",
            "ind_var13_medio_0",
            "ind_var13",
            "ind_var14_0",
            "ind_var14",
            "ind_var17_0",
            "ind_var17",
            "ind_var18_0",
            "ind_var19",
            "ind_var20_0",
            "ind_var20",
            "ind_var24_0",
            "ind_var24",
            "ind_var25_cte",
            "ind_var26_0",
            "ind_var26_cte",
            "ind_var25_0",
            "ind_var30_0",
            "ind_var30",
            "ind_var31_0",
            "ind_var31",
            "ind_var32_cte",
            "ind_var32_0",
            "ind_var33_0",
            "ind_var33",
            "ind_var34_0",
            "ind_var37_cte",
            "ind_var37_0",
            "ind_var39_0",
            "ind_var40_0",
            "ind_var40",
            "ind_var41_0",
            "ind_var44_0",
            "ind_var44",
            "ind_var7_emit_ult1",
            "ind_var7_recib_ult1",
            "ind_var10_ult1",
            "ind_var10cte_ult1",
            "ind_var9_cte_ult1",
            "ind_var9_ult1",
            "ind_var43_emit_ult1",
            "ind_var43_recib_ult1",
        ]
        return FeatureTypes(categorical=flags)

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        del raw
        table = column_dictionary([c for c in df.columns if c != self.target])
        counts = table["confidence"].value_counts().reindex(CONFIDENCE_LEVELS[::-1], fill_value=0)
        lines = ["| column | likely meaning | confidence | evidence |", "|---|---|---|---|"]
        lines += [f"| `{c}` | {meaning} | {level} | {evidence} |" for c, meaning, level, evidence in table.to_numpy()]
        why = (
            "Santander masked the column names and gave no data dictionary. The names stay as shipped; this table is "
            "our reading of each column from the data (review of 2026-11-05), not Santander's. Amounts and counts are "
            "the true values times 3. Confidence: high, shown by an identity or the value grid in every row (for "
            "`var38`, by the match with Santander's `renta`); medium, the names, sums and values agree on one "
            "reading; low, a likely reading from the names or values alone; unknown, no reading. A column's "
            "confidence is the lower of its kind of value and its product. Over the "
            f"{len(table)} features: " + ", ".join(f"{n} {level}" for level, n in counts.items()) + "."
        )
        # a string, so the README shows all rows (its tables stop at 60)
        return [Decision("Column dictionary", why, "\n".join(lines))]

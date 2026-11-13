---
unique_name: santander_customer_satisfaction
name: SantanderCustomerSatisfaction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 1
decision_markers:
- Anonymized
tags:
- Larger IID Data
- 'Samples: One Moment'
- 'Target: Unknown'
collections:
- TabArena Reject
original_source: Kaggle
year: '2016'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/c/santander-customer-satisfaction
notebook_path: datasets/beyond_iid/new_iid/santander_customer_satisfaction/santander_customer_satisfaction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/santander_customer_satisfaction/dataset.py
source_row: 649
type_adapter_id: curation-record-v1
---

## Comments

CC: "work with hundreds of anonymized features to predict if a customer is satisfied or dissatisfied with their banking experience. Very nice dataset. Data was uploaded to OpenML with Public license, but the actual license might be more prohibitive. Unsure how to deal with that. also, we don't know the split, but as competition winners used random, this should be fine."

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: the 56 ind_var indicators, which hold only 0 and 1 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: the 56 ind_var columns, indicators by their name, now an explicit list.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Area Under Receiver Operating Characteristic Curve (https://www.kaggle.com/competitions/santander-customer-satisfaction (Kaggle API evaluationMetric)).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined with a note: real (masked) customer rows; the leak found earlier is a household link through an exact var38 value that reaches 0.3% of test rows and is worth 0.5% of the error. Priority 1: gap 0, use case 0, source 0, shape 1, risk -1.

CC (2026-11-06, Andrej): keep, with random customers (option A of issue 1 on the BeyondArena v0.2 review page). The declared split (random, stratified 3x3 folds, as the competition's winners validated) and metric (ROC AUC, the competition's own) were checked.
- `var38` is Santander's gross household income, times 3 (every amount and count in the file is masked times 3): its most frequent values match, to the cent, those of `renta` ("gross income of the household") in Santander's Product Recommendation competition of 2016. Its spike, 117,310.98, is the mean filled in for the 19.5% of customers without an income on file.
- Customers who share an exact `var38` value (6,203 in 2,837 groups) are mostly members of one household, different people: a minor who shares a value shares it with another minor in 40% of pairs (no random pair does), and 79 pairs hold the same rare balance to the cent (a joint account). One person under two IDs and an area or branch value do not fit (ages differ in 87% of pairs; 82% of customers hold a value nobody else holds).
- A customer with a dissatisfied household member is dissatisfied in 17.9% of cases against 2.8%, but only 0.3% of test customers have such a member in training (about 0.5% of TabPFN's error). The random split stays: the bank sees a new customer's household members, only not their satisfaction in the same period.
- Changes made (the data is unchanged): the analysis and the likely meaning of each column family, with a confidence, in the definition's notes; one sentence on households in its splits note; the warning that term-deposit holders are almost all satisfied accepted as an ordinary category effect; `Andrej` added to checked_by.
- Reference: https://www.kaggle.com/competitions/santander-product-recommendation/discussion/26786 (the most frequent `renta` values).

CC (2026-11-06, Andrej): column names kept as Santander shipped them (option D of issue 2 on the BeyondArena v0.2 review page), with a column dictionary added instead.
- The README's "Column dictionary" gives each of the 307 shipped columns its likely meaning, a confidence and the evidence. It is built from rules in `dataset.py` (every column matches exactly one rule) and is our reading of the data, not Santander's.
- Confidence: 43 columns high (shown by an exact identity or the value grid, e.g. age, term deposits, household income), 176 medium (one consistent reading of names, sums and values, e.g. the cards, the current account), 54 low (a likely reading, e.g. transfers, `var3`) and 34 unknown.
- Renaming was not chosen: a wrong name would mislead readers and methods that read column names, and the masked names keep the data traceable to the competition and its write-ups.
- The data is unchanged: no value, row or column name.

CC (2026-11-10, Andrej): review page issue 3, option B: random, named `Snapshot` of one extract, the label read as dissatisfaction at the extract (its date unstated); the `Time basis: Snapshot:` bullet is in `curation_comments`, the tag enters `data_tags` once PR #50 is in the working copy. Split and record facts unchanged.

## Review

**Outcome:** added. The training file of Santander's Customer Satisfaction competition (Kaggle, 2016): 71,080
customers after dropping repeated feature rows, 307 anonymised columns (constant and copied columns dropped, a count
of zero cells added, as top solutions did), 3.8% dissatisfied, random split, ROC AUC as in the competition. Ships as
defined with random customers (issue 1) and its masked names with a column dictionary (issue 2), both resolved 2026-11-06. Reviewed on 2026-11-04 without a panel, from
the gathered evidence (the record, a model run on the shipped data, whose frame v0.2 builds unchanged) and one
check. Validity: the columns are anonymised but the rows are real: the column families (indicators, counts,
balances) depend on each other as accounts do (53% of the column pairs within each class, against the 5% of
chance), and a model tells real rows from rows with their columns shuffled within class perfectly (ROC AUC 1.0).
The leak found earlier is a household link: customers sharing an exact `var38` value share their label more often;
it reaches 0.3% of test rows and was worth 0.5% of the error. The label's definition and timing are not stated
(fit approximate). Value: the benchmark methods separate (1-AUC 0.156 for TabFM and TabPFN-3.5, 0.160 for the tuned
boosted trees, 0.182 for logistic regression). Quality: the `dataset_pure_feature_value` warning (customers with
`var13` products are 99.7% satisfied at a 96.2% base rate) is an ordinary category effect on an imbalanced target and
is accepted with that reason. Weighed: Santander's own data and metric, real rows +, an
undefined label and masked columns -, a weak household link between different customers.

**Main points:** All settled: random customers, with the analysis in the definition's notes (issue 1); the masked
names stay, with a column dictionary in the README (issue 2); the random split is named a `Snapshot` of one extract
(issue 3, 2026-11-10).

**Record judgment:** valid, approximate: real customers of a named bank, masked by the host (marker set); what
"dissatisfied" means and when it was measured is not published.

**Issues for Andrej:**

1. **Keep random customers, with a note on the households that share `var38`?**

   * **Problem:**
     - 6,203 customers (8.7%) share an exact `var38` value (an anonymised amount with cents) with other customers, in 2,837 groups whose members differ in age, so the groups look like households.
     - A customer with a dissatisfied household member is dissatisfied in 17.9% of cases against 2.8% when all members are satisfied, and random splits put most members of a test customer in training.
     - Keep random customers and say so in a note, or group the splits on `var38`?
   * **Background:** what `var38` measures is not published (competitors read it as a property or mortgage value);
     9,979 customers hold one imputed value (117,310.98) and are left out of the groups. The members are different
     customers of one household, not one customer twice. Whether a member's dissatisfaction is known when the bank
     scores a customer depends on how the label was taken, which the host does not say.
   * **Experiments:**
     - On the v0.2 frame (check of 2026-11-04): 280 customers have a dissatisfied member; under random 3-fold
       splits (3 repeats) 55 to 77 of about 23,700 test customers per fold (0.3%) have a dissatisfied member in
       training, 7 to 16 of them dissatisfied.
     - Model runs on the shipped data: the count of a customer's members and dissatisfied members (training
       labels only) improves TabPFN-3.5 from 1-AUC 0.1567 to 0.1559 (0.5%, 3 of 3 splits); raising the odds of the
       exposed rows on the benchmark predictions bounds the gain at about 0.5%.
   * **Effect on the task:** a method that matches exact `var38` values gains a little on a few hundred test customers;
     the ranking of methods rests on the other 99.7%.
   * **Consistency:** follows the related-entity case that keeps a random split when it matches how the task is
     framed (amazon_employee_access)[^1a]; it differs from bank_marketing issue 1, where the same client's later row
     states the label.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random customers (implemented) | stratified random 3x3 folds; a curation note on the households | the competition's split; the link touches 0.3% of test rows | a dissatisfied member in training helps a few test customers |
     | B | Grouped on `var38` | customers sharing an exact value outside the imputed one stay on one side | no household on both sides | groups on a masked column whose meaning is a guess; changes little |

   * **Recommendation:** A: the link joins different customers, is small, and a group key on a masked column of unknown
     meaning would be a guess[^1b]. **Decision:** random customers with a note (A), or grouped on `var38` (B)?

   **Notes for the AI:** on A, add a curation note: "Households: 6,203 customers share an exact `var38` value outside
   the imputed 117,310.98 (2,837 groups, ages differ); with a dissatisfied member 17.9% are dissatisfied against 2.8%;
   0.3% of test customers have such a member in training; kept, the members are different customers (review of
   2026-11-04)". Accept `dataset_pure_feature_value` with the reason in the outcome. On B, `df["household"]` = the
   `var38` value outside the imputed one, a unique id otherwise, and a `Grouping` on it. Record `CC` line either way.

   [^1a]: **SPLIT-31** (Should): over related entities, IID can match how a task is framed even when it is optimistic;
     such a task is a candidate for a grouped or temporal variant, not a fix.
   [^1b]: **SPLIT-24** (Must): group on a true group id or on one constructed exactly from the columns that define the
     entity. **SPLIT-30** (Must): a hidden-group hit is a question; re-split only when the context says the rows share
     an entity new data would not have, or the evidence is very strong.

   **Andrej (2026-11-05, discuss):** Do deeper reasoning on what the columns might be and try to de-anonymize them.
   Only then we can make a real decision. If it would be households, I would assume other features to match as well.

   **Answer (AI, 2026-11-05):**

   * **Finding:** `var38` is the bank's gross household income, and the customers who share a value are households
     (different people) or share a default value, not one place and not one customer twice.
     - The most frequent values of `renta` ("gross income of the household") in Santander's later Product
       Recommendation data recur here to the cent: its most frequent, 451,931.22, is the most frequent here too (32
       customers in train and test), and 7 of its 10 most frequent are among the 192 values that 5 or more customers
       share here, out of 109,981 values[^a1].
     - Other columns match where a household shares something and differ where its members differ: children share
       with children, couples have close ages, 79 pairs hold the same rare balance to the cent (a joint account);
       ages, cards and products differ as between different people.
     - The filler 117,310.98 is the exact mean of the other 122,165 values of train and test together: the 19.5% of
       customers without an income on file got the mean.
   * **Asked:** what the columns mean, and whether customers who share `var38` are households, a place (an area or
     branch value) or one customer under two IDs, tested on the other columns.
   * **Columns:** the names are Spanish banking terms; the structure is measured on train and test (151,838
     customers).

     | Columns | Likely meaning | Evidence | Confidence |
     |---|---|---|---|
     | every amount (`imp_`, `saldo_`, `var38`, `var21`) and count (`num_`) | the true value times 3 (the host's masking) | all 122 amount columns are multiples of 0.03 and all 131 counts multiples of 3 (not `num_var4`, `num_meses_`); divided by 3, cash withdrawals are 20, 40, 60 or 100 € and term deposits 10,000 to 100,000 € | high |
     | `var38` | gross household income times 3; 117,310.98 = none on file | the match with `renta`; 81% of customers without any product have one, 86% of minors; unrelated to balances, product count and age (Spearman 0.01, -0.03, 0.00); median 29,600 € once divided by 3; not a mortgage: 0.4% hold any loan | high |
     | `ind_X`, `ind_X_0`, `num_X` | money in product X; holds product X; 3 times the flag | `ind_X` is `saldo_X` ≠ 0 in every row; `ind_X` implies `ind_X_0` | high |
     | `saldo_` totals | var30 = var42 + var13; var42 = var5 + var8 + var6 + var29 + var12; var12 = var24 + var14 + var20; var31 = var17 + var33 + var44; var26 = var25 + var32; var1 = var18 + var34 | exact in every row (var1: 99.6%) | high |
     | var5, var42, var30 | the current account (66% have money in it, median 10 €); all accounts; accounts and term deposits | the totals; small balances | medium |
     | var13 `corto`, `medio`, `largo` | term deposits, short, medium and long term | round amounts; the names | high |
     | var39 = var40 + var41 (`imp_op_`, `num_op_`; `comer`, `efect`) | card spending in shops and cash withdrawals; var41 a debit card (88% hold one, never a balance), var40 a credit card (1.2%) | the totals; withdrawals in tens of euros | medium |
     | var17, var33 (`aport`, `reemb`, `trasp`); var44 (`compra`, `venta`); var31 | funds and pension plans (which is which unknown); securities; their total | the verbs; the totals | medium |
     | var1 = var18 + var34 (`amort`) | loans | repayments; 0.4% hold one | medium |
     | var43, var7 (`emit`, `recib`); var16 (`ent`, `sal`) | transfers sent and received; money in and out | round amounts of 20 to 1,000 € | low |
     | `saldo_medio_`, `num_meses_`, `delta_` | mean balance in the last month or 3, or 2 or 3 months ago; months with a balance of the last 3; change of the last month against the last 3 (9999999999 for no base) | the value grids | high |
     | `num_var4` | number of products (0 to 9; `num_var35` is 3 times it) | the product flags add up to it, about 1 each | medium |
     | `var15` | age | 5 to 105, 27% at 23; older customers hold more products | high |
     | `var3` | a country code, 2 = Spain, -999999 unknown | 231 codes, 97.6% are 2; but 15% of minors have another code against 0.5% of 23- to 26-year-olds, which nationality does not explain | low |
     | `var36` | a customer category, 99 = none | 63% of the 99s hold no product; 0 only under 23 | low |
     | `var21` | a credit limit | divided by 3, round amounts from 300 to 10,000 €; 1.2% have one | low |
     | var22, var45, var25, var26, var32 (`cte`), var37; `ID` | unknown; `ID` has no order | customers who share `var38` are no closer in `ID` than random pairs | none |

   * **Household test:** the 17,575 pairs of customers who share a `var38` value in train and test, against as many
     random pairs of customers with a value:

     | Test | Sharing a value | Random pairs | Reads as |
     |---|---|---|---|
     | same age | 13% | 9% | not one person twice |
     | columns that differ (median, of 369) | 28 | 27 | different people |
     | minors (under 18) who share their value | 57% | 18% of all customers | children carry the family's income |
     | the other member of a minor, in pairs: a minor; aged 23 to 26; aged 36 to 55 | 40%; 8%; 27% | 0%; 44%; 25% | siblings, not random adults |
     | ages within 5 years | 49% | 38% | couples |
     | a rare balance equal to the cent | 79 pairs, 87% of them within 5 years of age | none | joint accounts of couples |
     | the other member of a 23- to 26-year-old is aged 46 to 65 | 16% | 16% | young adults not grouped with parents |
     | same `var3` when one code is not 2 | 15 of 1,036 | 0.09% | weak; `var3` unclear |
     | dissatisfied when the other member is (train) | 21.9% against 3.0% in pairs; 24% against 1.8% for pairs within 5 years of age; 7.4% against 3.1% in values held by 6 or more | 5.7% against 3.7% | a household link |

   * **Against the alternatives:**
     - A place (an area or branch value): all customers of an area would share it and children would pair with random
       adults; here 82% hold a value nobody else holds, children pair with children, 79 pairs share a balance, and
       customers with the next value up (the same income level, another household) show no label link (4.9% against
       3.5%).
     - One customer under two IDs: ages differ in 87% of the pairs and the rows differ as much as random pairs do;
       exact repeats are already dropped by the definition.
     - A joint account: the 79 pairs above, a part of the households.
     - A default value: the values held by 6 or more (15 values, 122 customers in the shipped frame) include the most
       frequent `renta` values, each held by hundreds of customers there, so they are defaults or estimates, not
       households; their label link is weaker.
     - The label link is not that dissatisfied customers resemble each other: it holds with the other member's own
       state fixed (30% against 5.9% when that member holds no product, 8.3% against 2.0% when it holds one).
   * **Unknown:** how many of the pairs are households and how many share a rarer default; counting each shared value
     in the Product Recommendation files would settle it (a household's value is held by a few customers there, a
     default by hundreds), and those files need that competition's rules accepted on Kaggle.
   * **For the split:**
     - The members are different customers, so the rule for one entity in several rows does not apply; this is the
       case of related entities.
     - The bank keeps one income for all members of a household, so when it scores a customer it sees the members
       already at the bank; what it would not have is their label of the same period.
     - In the shipped frame 6,203 customers share a value: 6,081 in 2,822 values held by 2 to 5 (households) and 122
       in 15 values held by more (defaults); the exposure stays as measured, 0.3% of test customers and about 0.5% of
       TabPFN's error.
   * **Options:** B now groups on a known household field and leaves the defaults out.

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random customers (implemented) | stratified random 3x3 folds; the note names `var38` as household income and the groups as households | the competition's split; the bank sees a customer's household; touches 0.3% of test customers | a member's label of the same period helps a few test customers |
     | B | Grouped by household | customers who share a `var38` value held by 2 to 5 customers (2,822 households, 6,081 customers) stay on one side; the 15 values held by more stay ungrouped | no household on both sides of a split; the key is a known household field | changes about 0.5% of the error; departs from the competition's split |

   * **Recommendation:** A: the groups are households of different customers, which the bank sees when it scores a
     customer, and the link is small, so a random split over them matches the task[^a2]. B is a sound key now if no
     household should sit on both sides[^a3]. **Decision:** A (random, with a note on households) or B (grouped by
     household)?

   **Notes for the AI:** on A, the curation note: "Households: `var38` is the bank's gross household income times 3
   (its most frequent values are the most frequent `renta` values of Santander's Product Recommendation data;
   117,310.98 = none on file, the mean of the rest). 6,203 customers share a value: 2,822 households of 2 to 5 and 15
   default values held by more; with a dissatisfied member 17.9% are dissatisfied against 2.8%; 0.3% of test customers
   have such a member in training; kept, the members are different customers (review of 2026-11-05)". The
   `curation_comments` line "feature meanings are unknown" can then name `var38`, `var15` and the times-3 masking. On
   B, `key = df["var38"].round(2)`, `n = key.map(key.value_counts())`; `df["household"]` = the key where `var38` is not
   the filler and 2 <= n <= 5, a unique id otherwise; a `Grouping` on it; re-run `dataset check`. Record `CC` line
   either way; `dataset_pure_feature_value` accepted as in the outcome. The tests ran on train and test (151,838 rows);
   the label numbers on pairs with both members in train; the `renta` match used the ten values posted in the forum
   thread of footnote a1, since the Product Recommendation files need that competition's rules accepted.

   [^a1]: Product Recommendation data page (`renta`: "Gross income of the household"):
     https://www.kaggle.com/competitions/santander-product-recommendation/data; its ten most frequent `renta` values
     and a note that customers with the same `renta` and adjacent ids looked like households:
     https://www.kaggle.com/competitions/santander-product-recommendation/discussion/26786; the 2nd place found
     `renta` repeated for about 30% of customers, "mostly in pairs and groups<10", and read them as households:
     https://www.kaggle.com/competitions/santander-product-recommendation/discussion/26824. The mortgage reading of
     `var38`: https://www.kaggle.com/competitions/santander-customer-satisfaction/discussion/19895; no data dictionary
     (Kaggle staff): https://www.kaggle.com/competitions/santander-customer-satisfaction/discussion/19291.
   [^a2]: **SPLIT-31** (Should): over related entities, IID can match how a task is framed even when it is
     optimistic; such a task is a candidate for a grouped or temporal variant, not a fix. **SPLIT-29** (Must): an IID
     split is wrong when many rows share an entity that new data would not have and the entity carries the label; the
     bank has the household. **LEAK-17** (Must) is for one entity repeated in several rows, which the members are
     not.
   [^a3]: **SPLIT-24** (Must): group on a true group id, or on one constructed exactly from the columns that define
     the entity; the household income field is such a column.

   **Andrej (2026-11-05, ok):** Random customers. I want you to properly document your analysis since it is very
   insightful.

   **Resolved (2026-11-06, Andrej):** A, random customers. The definition's notes now document the analysis: the
   times-3 masking, the column families with a confidence, `var38` as the bank's gross household income (the `renta`
   match and the filled mean 117,310.98), the household test with the rejected readings (one person twice, a place),
   and the label link with why the random split stays. `splits_comment` has one sentence on households, and
   `dataset_pure_feature_value` is accepted (all five values are term-deposit holdings). Record: a `CC` line and
   `Andrej` in `checked_by`. `dataset check` clean; not rebuilt.

2. **Rename the masked columns to the meanings recovered?**

   * **Problem:**
     - The analysis of issue 1 recovered what many masked columns hold (the times-3 masking, `var15` age, `var38` household income, the product families), some with high confidence and others only as a likely reading.
     - The 307 columns still ship under Santander's masked names, and the meanings are only in the definition's notes.
     - Rename some or all of the columns, or keep the names and ship the meanings as a column dictionary next to them?
   * **Background:**
     - Confidence by family (the evidence is in the notes): high for the masking, the identities between `ind_`,
       `num_` and `saldo_`, `saldo_medio_`, `num_meses_`, `delta_`, `var15` (age), var13 (term deposits) and `var38`
       (household income); medium for the current account, the cards, funds and pension plans, securities, loans and
       `num_var4`; low for the transfers, `var3`, `var36` and `var21`; unknown for var22, var45, var25, var26, var32
       and var37.
     - Even a high-confidence name is our reading: Santander never confirmed one, and the competition's write-ups,
       its forum and other copies of the data use the masked names.
     - A rename changes no value and no row. The `Anonymized` marker stays true either way: it flags what the masking
       keeps us from checking (when each column was recorded, whether it leaks), and a recovered name does not settle
       that[^2a].
     - Our own rename, stated in the notes, is not the reworked table that makes a source suspect (a table someone
       relabelled before we got it)[^2b]; a wrong name would still be a defect we add.
   * **Effect on the task:** most benchmark methods ignore column names, so their scores do not move; a method that
     reads names (a language-model-based tabular model) takes a name as a prior, helped by a right one and misled by
     a wrong one; a person reading the README sees the names first.
   * **Consistency:** credit_approval keeps Quinlan's masked names `A1` to `A16` although unofficial names circulate
     (Kaggle calls `A9` "prior default"); the reading is in its record. No dataset of the working copy has renamed
     masked columns from a recovered meaning.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the names (implemented) | the source's names; the meanings by column family, with a confidence, in the definition's notes | traceable to the competition and its write-ups; no guess shipped as a name | a reader maps each name to its family by hand; a method that reads names gets nothing from them |
     | B | Rename the high-confidence ones | e.g. `var15` to `age`, `var38` to `household_income_x3`, `saldo_var13` to `saldo_term_deposits`; the rest keep their names | the surest meanings visible where the columns are used | two naming schemes in one table; the names rest on our reading; those columns no longer match the competition's names |
     | C | Rename all, with a confidence suffix | every column named after its likely meaning, ending in its confidence | every meaning visible | low-confidence names ship guesses; long names; a wrong name misleads methods that read names |
     | D | Keep the names, add a column dictionary | as A, plus a table of the 307 shipped columns (likely meaning, confidence, evidence) built in the definition and shown in the README | each column looked up in one place; names stay the source's; a correction changes the table, not the data | names still masked for methods that read them; a table to keep in step with the notes |

   * **Recommendation:** D: every reader gets the meanings and how sure they are, while the data and its names stay as
     Santander shipped them, so a wrong guess costs a line in a table, not a misleading name[^2c]. B would also be
     sound for `var15` and `var38` alone, if the names should help readers more. **Decision:** A, B, C or D?

   **Notes for the AI:** on D, a module-level list of `(regex, meaning, confidence)` rules for the column families
   (as in the notes) and a `_decisions` hook returning `Decision("Column dictionary", ...)` with a DataFrame of every
   shipped column, its meaning and confidence; `_clean` does not change. On B, `df.rename(columns={"var15": "age",
   "var38": "household_income_x3", ...})` in `_clean` after the drops, the flag list in `_feature_types` and every
   note that names a renamed column updated, a bullet with the old names; on C, the same for every column. Then
   `dataset check`, a CHANGELOG entry and a record `CC` line.

   [^2a]: The `Anonymized` marker: feature names or values replaced on purpose, so what a column measures, its timing
     and leaks cannot be checked; a concern flag, no exclusion reason. **LEAK-32** (Should): masked features that may
     hide a transform are a known risk, covered by the tag and the marker.
   [^2b]: **PROV-3** (Must): the data is real, not generated, and not a real table someone reworked (relabelled,
     columns renamed, values replaced).
   [^2c]: **CLEAN-1** (Should): clean to the state an expert would ship, from what the source's top solutions and the
     data owners did; the competition's solutions worked on the masked names (the 3rd place's write-up uses `var15`
     and `var38`: https://github.com/diefimov/santander_2016/blob/master/README.pdf).

   **Andrej (2026-11-05, discuss):** Since you recovered column names, should we add them or is it too risky since we
   are not sure?

   **Andrej (2026-11-06, change):** Option D: Keep the names, add a column dictionary.

   **Resolved (2026-11-06, Andrej):** D. The names stay as Santander shipped them. `dataset.py` holds the dictionary
   as rules (`COLUMN_RULES` for the kind of value, `PRODUCTS` for the varN), and every shipped column matches exactly
   one rule (asserted). The `_decisions` hook renders all 307 columns into the README's decision "Column dictionary"
   with the likely meaning, a confidence and the evidence: 43 high, 176 medium, 54 low, 34 unknown. The notes say the
   dictionary is our reading, not Santander's. Data unchanged; `dataset check` clean; record: a `CC` line; not
   rebuilt.

3. **Time basis: name the random split a `Snapshot` of one extract, with the label's date unstated?**

   * **Problem:**
     - Santander took one extract with one row per customer, and every windowed column (the last month, the last three months, two and three months ago) ends at that extract, so the rows share one moment, while when and how "dissatisfied" was measured is not stated.
     - The record says `Samples: One Moment` without a target tag, which reads the label as a state at the extract, and the random split (resolved 2026-11-06) carries no time basis.
     - Name it a `Snapshot`, with the label's unknown date in the line, or a `DelayedTarget`?
   * **Background:** a split that only fills in a moment the data covers is a `Snapshot`; a target that comes after
     one shared moment is a `DelayedTarget`, whose window must have closed and whose features must predate it[^3t1].
     The use case flags customers who are dissatisfied now, before they leave, which fills in the extract's moment.
     A label measured later, such as a complaint or a closed account, would make it a delayed target, and the window
     columns could then hold the customer's reaction; the check below finds no such trace in the last month. The
     household link of the same period is documented and kept (issue 1).
   * **Experiments:** on the competition's training file (76,020 customers, 3.96% dissatisfied): customers whose
     current account (`saldo_medio_var5`, medium confidence) held a balance three months ago and none in the last
     month (3,459) are dissatisfied at 3.1%, against 1.8% for those who kept a balance (42,880) and 8.6% for those
     with none in either month (21,205); an exit after the label would show as a much higher rate among the emptied
     accounts.
   * **Effect on the task:** none on rows, splits or scores.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no time basis (implemented) | as now | none found | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | Random, named `Snapshot` | `data_tags` gain `Snapshot`; a `Time basis:` line names the extract and the unstated label date | the use case's reading, a present state; the last month shows no exit trace | the label's date is a reading, not stated |
     | C | Random, named `DelayedTarget` | as B with `DelayedTarget`, the label read as later | none found | nothing in the data or the host's text says the label came later; the window and features could not be checked |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("Anonymized", "Snapshot")` and the curation bullet "-
   Time basis: Snapshot: one extract of Santander's customers (period not stated; competition 2016), with windows of
   the last month to three months ending at it; the label is a state the host does not define or date, read as
   dissatisfaction at the extract, which the use case fills in for customers not yet known to be dissatisfied. No exit
   trace in the last month: customers whose current account emptied in the last month are dissatisfied at 3.1%,
   against 1.8% for those who kept a balance (training file)."; `dataset check`. The record's facts stay.

   [^3t1]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows, with a `Time basis:` line
     stating the fact. A `Snapshot` only fills in a time the data covers; a `DelayedTarget` has one prediction moment
     for all rows and the target after it, its window closed for every row and every feature in existence at the
     moment. **LEAK-10** (Must): out is a feature computed from the window that defines the target, unless the data
     shows it does not move with the outcome.

   **Resolved (2026-11-10, Andrej):** B, random, named `Snapshot`: the drafted `Time basis: Snapshot:` bullet is in
   `curation_comments`, ending with what the split cannot test (a later extract, a label taken after it). Split and
   record facts unchanged; `Snapshot` enters `data_tags` once PR #50 is in the working copy.

## Reference

Soraya_Jimenez and Will Cukierski. Santander Customer Satisfaction. https://kaggle.com/competitions/santander-customer-satisfaction, 2016. Kaggle.

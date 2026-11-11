---
unique_name: taiwanese_bankruptcy_prediction
name: company_bankruptcy_prediction / taiwanese_bankruptcy_prediction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- 'Entities: Recur'
- 'Samples: Over Time'
- 'Time: Lost'
original_source: UCI
year: '2020'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C5004D
notebook_path: datasets/beyond_iid/old_iid/taiwanese_bankruptcy_prediction/taiwanese_bankruptcy_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/taiwanese_bankruptcy_prediction/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

The data were collected from the Taiwan Economic Journal for the years 1999 to 2009. Company bankruptcy was defined based on the business regulations of the Taiwan Stock Exchange. Might be a duplicate as I remember a similar dataset

Could require temporal split. paper does not clearly state at which points in time the features vs. the target were collected. Maybe features are from three years before bankruptcy

Most features seems to be time invariant

Potential issue: temporal

Lennart: Not time-based features, thus could be usable

Andrej: Need to verify correct lag between features and target

CC (2026-10-19, Lennart): 67 numeric columns are min-max scaled over all companies; kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: Liability_Assets_Flag (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: Liability_Assets_Flag (explicit; 1 when liabilities exceed assets).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Liang et al. 2016 report accuracy and Type I / II errors on a 1:1 sample and costs at several ratios, no single matrix.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `american_companies_bankruptcy` (TBD -> Yes, priority 2), `v4finbench_corporate_distress` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-11, Andrej): kept with the source gap noted (review page, issue 1 A): the paper sample (239 bankrupt and 239 matched companies) differs from the UCI release, whose sampling is undocumented, and the time between ratios and bankruptcy is unstated; this answers the note "Need to verify correct lag between features and target": the source does not state it. Forced IID kept with a full `Time basis:` line (issue 2 B). The rows look like company-years with the bankrupt label recurring one block later: random split kept and written down with the measured leak (issue 3 B; grouping moves ROC AUC 0.941 to 0.939/0.934). Collection facts added (issue 4 B): `Samples: Over Time`, `Time: Lost`.

## Review

**Outcome:** added. The AI recommends shipping it as defined, with the unknown time between ratios and bankruptcy
written into its notes (issue 1). Reviewed on 2026-11-04 without a panel, from the evidence already gathered (the
record, model runs on the shipped data and on the TabArena v0.1 task of the same source), the paper's data
section and two checks on the shipped table. The data are UCI's Taiwanese bankruptcy table (2020) from the Taiwan
Economic Journal for 1999-2009: 6,819 rows of listed companies with 92 financial ratios, 220 of them bankrupt under the Taiwan
Stock Exchange's rules (3.2%); the source scaled the ratios to 0-1 over all companies. Validity: a lender's or
investor's screening decision on published ratios; the bankruptcy definition is documented, but not how long before
the bankruptcy the ratios were taken (issue 1). Judged as polish_companies_bankruptcy was, the records of the two
classes follow one recording convention: no identity break, number format or unscaled value separates them
(details in issue 1), so the class-dependent recording that retires polish is absent here. Value: the 40 benchmark
methods spread from 0.039 1-AUC (LimiX-2) over 0.048 (TabPFN-3.5) and 0.052 (tuned LightGBM) to 0.058-0.063
(logistic regression); hand-built accounting scores rank 14th to 16th. Quality: 21 ratio columns keep unscaled values
above 1 in some rows (most of them turnover ratios), a source quirk kept as shipped. Better data for corporate
bankruptcy were found on 2026-10-31 (american_companies_bankruptcy, v4finbench_corporate_distress, screened at
priority 2); a valid task stays meanwhile. Weighed: documented source and bankruptcy rule +, one recording convention
for both classes +, methods separate +, unknown prediction point and an undocumented sample -.

**Main points:** settled on 2026-11-11: kept with the source gap written down (issue 1); the forced tag's full
`Time basis:` line (issue 2); the company-year structure and its measured leak written down, random split kept
(issue 3); collection facts `Samples: Over Time`, `Time: Lost` added (issue 4).

**Record judgment:** valid with a known gap, ship. Your note "Need to verify correct lag between features and
target" is answered in issue 1: the paper does not state it. The scaling over all companies is the paper's own
(eq. 1) and was kept by the curator on 2026-10-19.

**Issues for Andrej:**

1. **Keep it although the time between the ratios and the bankruptcy is not stated?**

   * **Problem:**
     - Neither UCI nor the paper says how long before the bankruptcy the ratios were taken, so the moment of the prediction is unknown, which your note on the record asked to verify.
     - The release (6,819 rows, 220 bankrupt) is also not the paper's sample of 239 bankrupt companies matched with 239 others, and how it was drawn is not documented.
     - Keep it with the gap written into the approximate fit, or retire it for missing source information?
   * **Background:** Liang et al. (2016), Sec. 3.1: "data were collected from the Taiwan Economic Journal for the
     years 1999–2009. Company bankruptcy was defined based on the business regulations of the Taiwan Stock
     Exchange. [...] First, the sample companies had to have at least three years of complete public information
     before the occurrence of the financial crisis. Second, there should be a sufficient number of comparable
     companies of similar size in the same industry [...] the collected dataset is composed of 239 bankrupt and 239
     non-bankrupt cases, with each company (i.e. case) represented by 95 FRs and 95 CGIs", each "normalized into the
     range from 0 to 1"[^1a]. FRs are financial ratios, CGIs corporate governance indicators (board and ownership
     data); the release has the ratios only. Whether a company appears in several years is not stated; the
     model runs found no near copies of rows and no excess of bankrupt neighbours around bankrupt companies.
   * **Effect on the task:** if the ratios came from the year of the failure, the task would recognise companies
     already failing rather than forecast them; the data cannot tell which.
   * **Experiments:** on the shipped table (the v0.2 frame), 9 shipped splits, untuned LightGBM: debt ratio plus net
     worth over assets equals 1 in every row of both classes; unscaled values (above 1 in a 0-1 column) occur in 82%
     of the surviving and 91% of the bankrupt rows, mostly turnover ratios near the base rate, and these indicators
     alone reach ROC AUC 0.64; values written at a coarser precision reach 0.51. The same kind of label-free markers
     reach 0.955-0.964 on polish_companies_bankruptcy, as much as its 64 ratios.
   * **Consistency:** follows bad_customer_detection and tour_travels_churn, kept with a gap of their source written
     into an approximate fit[^1b]; differs from polish_companies_bankruptcy, where the recording separates the
     classes.
   * **Unknown:** the gap and the sampling of the release; the donors (the paper's authors at National Central
     University) or the Taiwan Economic Journal's records would settle it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, gap noted (implemented in part) | the fit stays approximate; the notes add the paper's sample and the unstated gap | a documented source and bankruptcy rule; one recording convention for both classes; methods separate | the moment of the prediction stays unknown |
     | B | Retire | record `No (Retired)` with `Missing source information`; folder removed | no task with an unknown prediction point | loses a documented task; departs from the datasets kept with a source gap |

   * **Recommendation:** A, a documented source with one gap, written down as such. **Decision:** keep with the gap
     noted (A) or retire (B)?

   **Notes for the AI:** on A, add to `curation_comments`: the paper's Sec. 3.1 sample (239 bankrupt and 239 matched
   companies, at least three years of public data before the crisis, 95 ratios and 95 governance indicators), that
   the UCI release differs and its sampling is undocumented, that the gap between ratios and bankruptcy is unstated,
   and the recording check of this issue; add the DOI to the bibtex. On B, the record's CC line, `No (Retired)`, the
   marker, folder removal and a CHANGELOG entry.

   [^1a]: Liang, D., Lu, C.-C., Tsai, C.-F., & Shih, G.-A. (2016). Financial ratios and corporate governance
     indicators in bankruptcy prediction: A comprehensive study. European Journal of Operational Research, 252(2),
     561-572. https://doi.org/10.1016/j.ejor.2016.01.012
   [^1b]: **PROV-2** (Should; amended 2026-10-21, Lennart) and **USE-8** (Must): a source unclear in a detail stays,
     with a note of what to clarify, and the gap is written as an approximate fit.

   **Resolved (2026-11-11, Andrej):** A (ok): a curation note with the paper's Sec. 3.1 sample (239 bankrupt and 239
   matched companies, three years of public data before the crisis, 95 ratios and 95 governance indicators), the
   undocumented sampling of the UCI release, the unstated gap between ratios and bankruptcy and this issue's recording
   check; the DOI is in the bibtex; a `CC` line answers the record's note on the lag. Text only, no `dataset check`.

2. **Time basis: keep the forced tag and write its `Time basis:` line with the file's structure?**

   * **Problem:**
     - The rows come from 1999-2009 and carry no year, but the raw file is not shuffled: it repeats the same kind of row at a regular period of 26 to about 200 rows, the pattern of company-years ordered by industry and year (issue 3), so the order may hold the year inside each block without any block being datable.
     - The definition already ships `ForcedIIDFromTemporal` with a note that "no row carries its year"; the record has no collection fact at all (issue 4).
     - A lender scores later statements in a climate that moved (2001, 2008), and the time is lost, so the forced tag stays; what changes is the line, which should state the structure and the leak test.
   * **Background:**
     - No prototype fits: the rows share no prediction moment, bankruptcy follows the ratios at an unstated gap
       (issue 1), and no date exists to show a stationary relation.
     - Rebuilding the years would need the start and length of every block and the direction of time, all guesses;
       a guessed time axis is not one[^2a].
     - The leak test across the split is issue 3: a company's other years sit on the other side, and the bankrupt
       label repeats at the block period.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Forced, note as now (implemented) | `ForcedIIDFromTemporal` with the note "no row carries its year" | nothing to write | the note misses the company-year structure and the leak test the forced tag asks for |
     | B | Forced, with a full `Time basis:` line | the same tag; the note becomes a `Time basis:` line with the file's structure and issue 3's numbers | states what the random split stands in for and what it lets through | none found |
     | C | Forced grouped | `ForcedGroupedFromTemporal` with a grouping on file segments | follows issue 3 if it groups | only if issue 3 takes its option C |

   * **Recommendation:** B, with C only if issue 3 groups. **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in this working copy, on B: replace the `ForcedIIDFromTemporal:` bullet of
   `curation_comments` with `- Time basis: ForcedIIDFromTemporal: listed Taiwanese companies of 1999-2009, used to
   screen later statements; no row carries its year or company. The raw file repeats its rows at a regular period
   (26 to about 200 rows; one period after a row its closest match lies below the 1st percentile of random-pair
   distances for 34% of rows, 13-17% at other offsets), so the rows look like company-years ordered by industry and
   year, but no block can be dated (Time: Lost). Leak test across the split: a company's other years sit on the other
   side, and 69% of bankrupt rows have a bankrupt row one period later (21-25% at other offsets); grouping on rebuilt
   chains or on file segments moves ROC AUC from 0.941 to 0.939 and 0.934 (LightGBM). Years and company ids would allow
   a split by time.`; `dataset check`.

   [^2a]: **SPLIT-32** (Should): `Time: Dated` needs a date, an order that tracks time or a value that encodes the
     period; the five questions; a forced split ships after a leak test. **SPLIT-8** (Must): the forced split, tagged,
     after a leak test across the split; a leak found is removed where it can be, otherwise the task may ship as an
     approximate fit with the leak measured in the notes.

   **Andrej (2026-11-11, change):** Option B: Forced, with a full `Time basis:` line.

   **Resolved (2026-11-11, Andrej):** B: the old `ForcedIIDFromTemporal:` bullet is replaced by the drafted
   `- Time basis: ForcedIIDFromTemporal: ...` line (ending with what the split cannot test: later years and companies
   not seen in training); `ForcedIIDFromTemporal` stays in `data_tags`. Text only, no `dataset check`.

3. **The rows look like company-years, and the bankrupt label recurs one block later: keep the random split with this written down, or retire?**

   * **Problem:**
     - The raw file repeats its rows at a regular period: one period after a row, its closest match lies below the 1st percentile of random-pair distances for 34% of rows against 13-17% at other offsets, and the period (26 to about 200 rows) changes along the file as the count of companies per industry would.
     - The bankrupt label recurs at that period: 69% of the 220 bankrupt rows have another bankrupt row within three rows one period later, against 21-25% at other offsets (about 20% by chance), so under a random split rows of one company sit on both sides, and bankrupt rows have bankrupt counterparts one block away.
     - With no company id or year the companies cannot be rebuilt exactly: keep the random split with the structure and its measured size written down, group on file segments, or retire?
   * **Background:**
     - 6,819 rows over 11 years is about 620 a year. Bankrupt rows stand at regular spacing (rows 2147, 2197, 2245,
       2293, 2343, 2392 and 2440, a period of about 49) and in runs of up to 13 consecutive rows.
     - Two readings fit: a company is labelled bankrupt in several of its years, or the file puts each block's
       bankrupt rows first. The bankrupt rows at regular spacing are not much closer to each other than random rows
       (mean distance 3.72 against 3.87), so the files cannot tell which.
     - The definition's `row` says "whether a company can appear in more than one year is not stated"; the earlier
       review found no near copies of rows, which company-years would not have either. If a company's early years
       carry its later failure, the gap between ratios and bankruptcy of issue 1 is wider than one year.
   * **Experiments:** on the UCI file (Slurm jobs 1366176 and 1366181), 5 folds x 3 repeats, ROC AUC:

     | Split | LightGBM | kNN, k = 25 |
     |---|---|---|
     | random | 0.941 | 0.884 |
     | grouped by rebuilt chains (closest match one period later, below the 10th percentile of random-pair distances) | 0.939 | 0.881 |
     | grouped by 10 contiguous file segments | 0.934 (sd 0.031) | 0.877 |

     - Under random folds, a test row whose rebuilt chain has a bankrupt row in training is bankrupt in 10.5% of
       cases against 1.0% otherwise. The chains miss most of the regular bankrupt runs (the rows above fall in six
       chains), so the grouped scores bound the leak loosely.
   * **Effect on the task:** a model sees other years of the same company, sometimes with the same label; neither
     boosting nor nearest neighbours gain measurably from it, but what one row stands for (a company or a
     company-year, a label for the year or for the company) is not what the definition says.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | random split; `row` says recurrence is not stated | no change | states less than the file shows |
     | B | Keep, write it down | `row` and `fit_reason` say the rows look like company-years with the label recurring; a curation note with the numbers above | the forced split ships with its leak measured, as the rule allows when a leak cannot be removed | the company's other years stay on both sides |
     | C | Group by file segments | 10 contiguous segments of the raw order as groups; `ForcedGroupedFromTemporal` | keeps most of a company's years together, on a key taken from the file itself | tests unseen industries rather than later years; segment edges cut companies; scores 0.007 lower with three times the spread |
     | D | Retire | record `No (Retired)`; folder removed; the donors asked for company ids and years | no task whose rows and label are unclear | loses a task whose methods separate; better corporate data is only in screening |

   * **Recommendation:** B: the structure is clear, the measured gain from it is small, and the rule ships a forced
     split with a leak that cannot be removed when it is measured and written down[^3a]; D if issue 1 retires for the
     unknown prediction point, since this adds to it. **Decision:** A, B, C or D?

   **Notes for the AI:** on B, `row`: "One company-year, as the file's structure suggests (the source does not say),
   of the Taiwan Economic Journal's data for 1999-2009 (6,819 rows)"; a `fit_reason` sentence: "The rows repeat by
   company over the years and the bankrupt label recurs one block (likely a year) apart, so a company's other years sit on both sides of
   the random split."; a curation note with the period test (34% against 13-17%), the label test (69% against 21-25%)
   and the table above; `dataset check`. On C, a segment column from the raw row order (10 equal parts) as the
   grouping, out of the features, and `ForcedGroupedFromTemporal` (issue 2). Scripts of the time review of
   2026-11-06: `nn_offsets.py`, `period.py`, `link.py`, `link_control.py`, `link_dist.py`, `tw_split.py`,
   `knn_split.py`.

   [^3a]: **SPLIT-8** (Must): a forced split gets a leak test across it (a row sharing its outcome, its unit's outcome
     or its period's outcome with the other side, a hidden group, an order dependence); a leak found is removed where
     it can be, otherwise the task may ship as an approximate fit with the leak measured in the notes. **SPLIT-24**
     (Must): group on a true id or one constructed exactly from the data, never on a similarity cluster.
     **SPLIT-25** (Must): when the real groups matter and cannot be recovered, retire rather than group on a guess.
     **SPLIT-4** (Must): new statements of the same listed companies are what a lender meets, so known companies are
     part of the use case.

   **Andrej (2026-11-11, change):** Option B: Keep, write it down.

   **Resolved (2026-11-11, Andrej):** B: `row` now reads "One company-year, as the file's structure suggests (the
   source does not say), ..."; `fit_reason` gains the sentence on the recurring label; a curation note gives the period
   test (34% against 13-17%), the label test (69% against 21-25%) and the split table. The random split stays. Text
   only, no `dataset check`.

4. **Correct the record's collection facts: add them?**

   * **Problem:**
     - The record carries no collection fact.
     - The rows arose over 1999-2009 and keep no year; the file's order repeats by company (issue 3) but dates no block.
     - Set `Samples: Over Time` and `Time: Lost`, and leave the target fact empty while the gap between ratios and bankruptcy is unstated (issue 1)?
   * **Background:** UCI: data "collected from the Taiwan Economic Journal for the years 1999 to 2009"
     (https://doi.org/10.24432/C5004D). A fixed gap would be `Target: Later`; the source states none[^4a].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No facts (implemented) | as now | no edit | the record says nothing of how the rows arrived |
     | B | Add them | `Samples: Over Time`, `Time: Lost` | the facts the source and the file support | none found |

   * **Recommendation:** B. **Decision:** keep (A) or add (B)?

   **Notes for the AI:** on B, add the two tags to the record's `tags`; a `CC (<date>, Andrej):` line and `Andrej` is
   already in `checked_by`.

   [^4a]: **SPLIT-32** (Should): `Samples: Over Time` when the samples arose over a period, with `Time: Dated` or
     `Time: Lost`; `Target: Later` after a fixed window; no target fact when the target exists with the features.

   **Andrej (2026-11-11, change):** Option B: Add them.

   **Resolved (2026-11-11, Andrej):** B: the record's `tags` gain `Samples: Over Time` and `Time: Lost` (also in
   the PR #50 worktree's copy), with a `CC` line.

## Reference

Liang, D., Lu, C.-C., Tsai, C.-F., and Shih, G.-A. (2016) Financial Ratios and Corporate Governance Indicators in Bankruptcy Prediction: A Comprehensive Study. European Journal of Operational Research, vol. 252, no. 2, pp. 561-572

---
unique_name: videogame_sales_2024
name: Video Game Sales 2024 (VGChartz scrape)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2024'
domain: business & marketing
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/asaniczka/video-game-sales-2024
- https://www.kaggle.com/datasets/baynebrannen/video-game-sales-2020
- https://www.vgchartz.com/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a 2024 re-run of the 2020 VGChartz scrape, 64,016 titles of which about 18,900 carry a total-sales figure, VGChartz's estimate up to the scrape date; a newer version of `videogame_sales` (PROV-6) with the same target concern.
- Source: the VGChartz game database (vgchartz.com), scraped by the Kaggle user asaniczka in January 2024 with baynebrannen's 2020 spider ("Data was collected by running the spider written by @baynebrannen ... I haven't made any major modification to the collection methodology or the dataset structure"; `vg_score`, `user_score` and `total_shipped` removed "as these columns mostly contained null values"); file `vgchartz-2024.csv` (8.2 MB, 2024-01-29), ODC-By. As published: 64,016 rows x 14 columns (`img`, `title`, `console`, `genre`, `publisher`, `developer`, `critic_score`, `total_sales`, `na_sales`, `jp_sales`, `pal_sales`, `other_sales`, `release_date`, `last_update`); a third-party cleaning notebook reports `total_sales` missing in 45,094 rows and `critic_score` in 57,338 (https://chonwun-shen.quarto.pub/shen-chon-wuns-final-project/cleaning.html; not counted by us).
- Use case: the source names none; a publisher estimating a title's unit sales from platform, genre, publisher and release date before launch is our reading, fit approximate: the target is VGChartz's estimate, not reported sales, and it accumulates up to the scrape date, so recent titles have months of sales and old ones decades (the shared-window concern of SEL-6). Regime temporal by release date.
- Siblings and duplicates: `videogame_sales` (Lennart, `TBD -> 2nd Tier`, `No Good Target (yet)`; gregorut's 2016 scrape of the same site, 16,598 rows; CARTE/TARTE, MulTaBench): the same source and target, so a version (PROV-6), and at most one enters; the 2020 baynebrannen and 2019 ashaheedq scrapes have no record; no other VGChartz record (`grep -il vgchartz`). External collections: none found for this version.
- Better data: found as better data for `videogame_sales`; no further search this round.
- Papers and pages: the Kaggle page (metadata read through the API); VGChartz's estimation method not read; no paper.
- Metric: none found (a Kaggle dataset page, no task or competition), so the fallback `rmse`, on a log scale of unit sales to decide (MET-3, MET-8). Inputs: none.
- Risks for /add-dataset: keep only rows with `total_sales` (USE-7); the regional columns sum to the target (drop, LEAK); `critic_score` and `last_update` may postdate release (USE-3); `img` is a box-art path (drop, SEL-12); the cumulative-to-scrape-date target (SEL-6) and VGChartz's thinner software estimates after about 2018 (the run's note, not checked).
- Priority: gap 0 (business, regression, temporal not thin), use case 0 (none in the source), source 0 (a Kaggle scrape of estimates), shape + (about 18,900 labelled titles, mixed types, release dates), risk - (an estimated, window-dependent target, and a recorded version of the same source).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `videogame_sales`.
- as published: Over 64,000 games (per the subtitle), columns as the 2020 version minus vg_score, user_score and total_shipped: title, console, genre, publisher, developer, critic score, total and regional sales, ...; target: Total (or regional) sales in millions of units, as VGChartz estimates; access: open (ODC-By).
- Why: Same source (VGChartz) and same target as videogame_sales (gregorut, 16.6k games scraped in 2016)
- Adds: Newer (to 2024) and about four times as many titles, plus developer, critic score and release date. A version of the same source (PROV-6). Caveats: many of the 64k titles likely carry no sales figure (VGChartz thinned its software estimates after about 2018), so count the rows with sales before taking it; the ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.

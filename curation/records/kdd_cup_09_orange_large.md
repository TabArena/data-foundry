---
unique_name: kdd_cup_09_orange_large
name: KDD Cup 2009 Orange customer relationship prediction, large version (15,000 variables)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Anonymized
tags:
- AI-Filled (Verify)
- Many features
original_source: Other
year: '2009'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://kdd.org/kdd-cup/view/kdd-cup-2009/Data
- https://proceedings.mlr.press/v7/guyon09.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 2: the full Orange release of the KDD Cup 2009, the same 50,000 labelled customers as the shipped `kdd_cup_09_appetency` with all 15,000 variables (14,740 numeric, 260 categorical) instead of its 230, and public training labels for churn, appetency and up-selling; a version of a shipped dataset, so the curator decides which of the two enters (PROV-6).
- Source: Orange (France Télécom) for the KDD Cup 2009; Guyon, Lemaire, Boullé, Dror and Vogel, "Analysis of the KDD Cup 2009: Fast Scoring on a Large Orange Customer Database", JMLR W&CP 7 (read in full); files on kdd.org (KDD Cup 2009, Data). As published: training and test sets of 50,000 customers each; "For the large dataset, the first 14,740 variables are numerical and the last 260 are categorical" (Data page); training labels per task as +1/-1 (`orange_large_train_appetency.labels`: 890 positives of 50,000, checked; churn 7.3%, up-selling 7.4%, Sec. 3); test labels never released. Sec. 4: the two versions "corresponded to the same data entries, the 230 variables of the small version being just a subset of the 15,000 variables of the large version"; Orange's datamart of about one million customers was resampled "to obtain 100,000 instances with less unbalanced target distributions", 20,000 constructed features were narrowed to 15,000, then anonymised by "discarding variables names, randomizing the order of the variables, multiplying each continuous variable by a random factor and recoding categorical variable with randomly generated category names".
- The task's table: 50,000 labelled customers x 15,000 variables (less the empty ones), one target (appetency, to match the shipped dataset). Download: five training chunks of about 55 MB zipped (`orange_large_train.data.chunk1.zip` 55,314,613 bytes) and the label files, public on kdd.org without registration.
- Use case: Orange's marketing ranks customers for churn, appetency and up-selling actions (Sec. 1: tools "producing scores" for customer relationship management); fit approximate, as in `kdd_cup_09_appetency` (anonymised features, no stated label window). Regime IID: "no violation of the i.i.d. assumption" (Sec. 4), one random sample split in halves.
- Siblings and duplicates: `kdd_cup_09_appetency` (`Yes`, shipped: the 230-variable small version, appetency); `kddcup_09_appetency_kddcup_09_upselling` (`No`, `Duplicate`, Lennart), whose links include OpenML 43072, a 14,892-column copy of the large up-selling task; OpenML 42759 and 42773 hold the large up-selling with 15,001 columns. External collections: TabSTAR (that up-selling copy).
- Better data: none searched (found by the data-scouting run of 2026-11-08); this is a version of the shipped dataset, not better data from another source.
- Papers and pages: Guyon et al. 2009; the winners' papers in JMLR W&CP 7 (IBM Research first; "All the winning teams scored best on the large dataset", Sec. 7.1).
- Metric: AUC per task, ranked by the mean of the three (Sec. 3: "judged by the area under the ROC curve (AUC)"; the Tasks page), a competition's metric (MET-4): `roc_auc` on the chosen target, as the shipped dataset declares; inputs none.
- Risks for /add-dataset: PROV-6: one of the two versions enters; the large one is the fuller first release and contains the small one's columns (rescaled and reordered, so matching them needs the data), the shipped small one is the cut, and keeping both makes a duplicate. The precedent above went the other way for the large up-selling copy, a consistency question for the curator. `Anonymized` (LEAK-32): names hidden, values rescaled; the class shares are a resample, not Orange's; churn and up-selling are swapped targets of the same rows (PROV-6), so one target per entry.
- Priority: gap 0 (business & marketing, binary and IID not thin), use case 0 (fit approximate, as the shipped version), source + (the challenge paper documents the construction), shape + (50,000 x 15,000, numeric and categorical), risk - (a version of a shipped dataset, anonymised).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).

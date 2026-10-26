---
unique_name: lgd
name: LGD
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 1
collections:
- New (BeyondArena)
original_source: Website
year: '2016'
domain: finance
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- http://www.creditriskanalytics.net/datasets-private2.html
v2_path: datasets/_dev/tabarena-v0pt2/lgd/dataset.py
source_row: 666
type_adapter_id: curation-record-v1
---

## Comments

"provided by a European bank"
Looks like good data, again from the same interesting domain!

**Assessment (AI, 2026-10-07):** The definition is a grouped regression, unlike this record's Binary / Random (IID) fields. The book (ch. 1, p. 14) calls the data 2,545 loans of a European bank, "slightly modified and anonymized". The target is `lgd_time`, the book's own task (ch. 1, p. 4; ch. 10 errata: "MODEL lgd_time ~ GENERAL(ll)"). The only features are `LTV` and `purpose1`. `event` is 0 exactly at the 0.00001 LGD floor, which makes it part of the target. Loans sharing one LTV value come as consecutive runs, most likely one borrower's loans (LGD residual correlation 0.42 within a run, 0.02 between neighbouring runs), so the split is by run. No HMEQ-style artefacts found.

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape -, risk - (Issue 3: meaning of event=0 unsettled, 728 rows may not be LGD observations). Real LGD regression, but only two features, an unclear zero-loss target and undocumented modifications make it a thin task.

**Assessment (AI, 2026-10-20):** review panel (re-check): ship after changes; the changes are in the definition. The notes and `fit_reason` quote the data page's line "event: Indicator variable for a default or cure event; 1 = event, 0 = no event", which read literally leans against reading the 728 rows with `event` = 0 (28.6%) as cures, while the book's Tobit and censored beta code treat them as an LGD of 0; the rows stay until chapter 10 is read (USE-5, open). The split note says "most likely one borrower" and that the test stands for new borrowers in the same undated period (forward windows in file order 0.138 against 0.210 grouped, an upper bound); `purpose_renting` is categorical (CLEAN-14); the stale "record's random split" wording is gone. With regularisation the strong methods sit within 0.01-0.03 R² (spline 0.206, regularised LightGBM 0.195, linear 0.189); the probes' +0.218 linear-minus-forest gap is untuned overfitting. Open for Lennart (REVIEW.md): chapter 10 on `event` = 0 (issue 3), the two-feature task against haberman_survival (issue 4), the `problem_type` row (Binary Classification against the definition's Regression). Priority 1: gap -, use case - (fit approximate: no dates, two inputs), source + (the book's own data page, sha256 equal to the 2017 Wayback copy), shape - (2 features), risk - (the meaning of `event` = 0 is open on 28.6% of the target).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Baesens, Roesch & Scheule 2016 (ch. 10) evaluate LGD models by MSE/RMSE, R^2 and Pearson/Spearman/Kendall correlations, with no declared winner metric. rmse is the regression fallback.

## Reference

@book{baesens2016credit,
  title={Credit risk analytics: Measurement techniques, applications, and examples in SAS},
  author={Baesens, Bart and Roesch, Daniel and Scheule, Harald},
  year={2016},
  publisher={John Wiley \& Sons}
}

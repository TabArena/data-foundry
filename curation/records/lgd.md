---
unique_name: lgd
name: LGD
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
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

## Reference

@book{baesens2016credit,
  title={Credit risk analytics: Measurement techniques, applications, and examples in SAS},
  author={Baesens, Bart and Roesch, Daniel and Scheule, Harald},
  year={2016},
  publisher={John Wiley \& Sons}
}

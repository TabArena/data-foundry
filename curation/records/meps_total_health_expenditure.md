---
unique_name: meps_total_health_expenditure
name: 'MEPS HC-251: 2023 Full Year Consolidated Data File (Medical Expenditure Panel Survey, Household Component)'
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-251
- https://meps.ahrq.gov/data_stats/download_data/pufs/h251/h251doc.shtml
- https://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): a second record of AHRQ's MEPS HC-251 file and its `TOTEXP23` target, which `meps_health_expenditure` already holds; the two records carry the same three source links and the same task.
- Source: Agency for Healthcare Research and Quality, MEPS HC-251, 2023 Full Year Consolidated Data File (released August 2025): "18,919 persons who participated in the MEPS HC in 2023", 1,374 variables (HC-251 documentation, https://meps.ahrq.gov/data_stats/download_data/pufs/h251/h251doc.shtml). Both records name `TOTEXP23`, a person's total health-care expenditure in the year, as the target; this one adds out-of-pocket spending as an alternative, another framing of the same signal rather than a distinct task (PROV-7 does not apply).
- Siblings and duplicates: `meps_health_expenditure` (this run, `TBD -> Yes`, priority 2), kept as the canonical record because its name covers the whole series of annual files. This record was found as better data for `healthcare_insurance_expenses`; that lineage is written into `meps_health_expenditure`'s block.
- For the curator: which of the two names stays is a free choice; by the convention for a duplicate created new, this one could be renamed `meps_health_expenditure_duplicate` (records.md, "Duplicates and retirements").
- Reject check (AI, 2026-10-31): stands. Both records carry the same three AHRQ links (HC-251 detail page, https://meps.ahrq.gov/data_stats/download_data/pufs/h251/h251doc.shtml, the download list) and the same target, TOTEXP23, from the file of '18,919 persons who participated in the MEPS HC in 2023'. Out-of-pocket spending is one of the payment amounts that sum to TOTEXP23, an alternative framing that no source ties to its own decision, so PROV-7 does not apply. meps_health_expenditure's block does not mention it yet: carry it there.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `healthcare_insurance_expenses`.
- as published: 2023 file: 18,919 persons x 1,374 variables (18,463 with a positive person weight), per the AHRQ documentation; earlier annual files not counted here; target: total health care expenditure of the person in the year (TOTEXP23: the sum of the 10 source-of-payment variables); out-of-pocket spending as an alternative; access: open (public use file).
- Why: healthcare_insurance_expenses (the Lantz 'insurance.csv', 1,338 rows) was retired as simulated: its charges are a recovered formula of age, BMI, children, sex, smoking and region plus random noise. MEPS measures the same quantity (a person's annual medical spending) in a national survey, with the same kinds of ...
- Adds: real data from a federal agency instead of generated rows; about 14x the rows in one year and roughly 28 annual waves for a temporal split. Caveats: adult BMI (ADBMI42) is among the variables deleted from the 2023 file (earlier years carry it); complex survey design with person weights; many zero spenders and a heavy ...

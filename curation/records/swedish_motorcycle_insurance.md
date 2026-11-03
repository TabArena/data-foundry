---
unique_name: swedish_motorcycle_insurance
name: 'Swedish motorcycle insurance (Wasa, 1994-1998): partial-casco claim frequency'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Other
year: '2010'
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://staff.math.su.se/esbj/GLMbook/mccase.txt
- https://dutangc.github.io/CASdatasets/reference/swmotorcycle.html
- https://doi.org/10.1007/978-3-642-10791-7
- https://vincentarelbundock.github.io/Rdatasets/doc/insuranceData/dataOhlsson.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, papers and a preview of the files, NOT from a full inspection of the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 64,548 motorcycle partial-casco policies of the former Swedish insurer Wasa (1994-1998) from Ohlsson and Johansson's pricing textbook, with exposure, claim count and claim cost: the insurer's claim-frequency pricing task in a thin domain; six rating factors, rare claims and old data.
- Source: Ohlsson and Johansson 2010, Non-Life Insurance Pricing with Generalized Linear Models, Springer (doi 10.1007/978-3-642-10791-7), case study "Motorcycle Insurance"; the file `mccase.txt` and the SAS reader `mcin.sas` on the book's site (staff.math.su.se/esbj/GLMbook/case.html): fixed-width columns `agarald` (owner age), `kon` (gender), `zon` (geographic zone), `mcklass` (EV-ratio class), `fordald` (vehicle age), `bonuskl` (bonus class), `duration` (policy years), `antskad` (number of claims), `skadkost` (claim cost). Copies: CASdatasets `swmotorcycle` (English names, 64,548 x 9; "It contains aggregated data on all insurance policies and claims during 1994-1998"; seven EV-ratio classes, bonus classes 1 to 7) and insuranceData `dataOhlsson`. The first rows of `mccase.txt` (previewed) show durations such as 0.175, 0.455 and 1.003 and some zeros, so a row looks like one policy's exposure over the period rather than a tariff cell; to confirm.
- Use case: the insurer sets the partial-casco premium at underwriting from the rating factors, through the expected claim frequency per policy year, the book's tariff-analysis case study; fit direct for the claim count with exposure (or claim occurrence). Regime IID: one row per policy, no date or holder id.
- Siblings and duplicates: no record of this source (grep: Ohlsson, Wasa, motorcycle, swmotorcycle). Other portfolios (PROV-7): `ausprivauto0405` (`TBD -> Yes`, 4), `bemtpl97` (`TBD -> Yes`, 4), `fremtpl2` (`TBD -> Yes`, 4), `eumtpl` (`TBD -> Yes`, 3), `eudirectlapse` (lapse, `TBD -> Yes`, 4). The book's other case data (bus insurance `busscase.txt`, the GAM case `gamcase.txt`) have no record. External collections: CASdatasets, insuranceData (Rdatasets).
- Better data: from the curator's Zotero collection (item 131, Rdatasets); no further search this round.
- Papers and pages: Ohlsson and Johansson 2010 (the data; the book's text was not read); the CASdatasets and Rdatasets help pages (the latter says, in summary, that the data are old for confidentiality reasons).
- Metric: none found (the help pages state none; the book fits Poisson and gamma GLMs for tariff relativities rather than ranking models), so the fallback `rmse` on the claim frequency, as for `bemtpl97`, unless a Poisson deviance with exposure is chosen, or `roc_auc` on claim occurrence (MET-1, MET-8); inputs: the exposure, which ships.
- Risks for /add-dataset: the claim count and cost frame the outcome and go when occurrence is the target (LEAK); the exposure enters as an offset or weight, and zero-exposure rows need a rule; partial-casco claims are rare (count not checked), a low signal (TP-2, no reason against it); owner ages of 0 and the row unit ("aggregated" in CASdatasets) to confirm; the portfolio is from 1994-1998.
- Priority: gap + (insurance is thin, 3 accepted), use case + (the book's pricing case study of a named insurer), source + (a textbook that ships the data with a reader program), shape + (64,548 policies, six rating factors of mixed type), risk - (rare claims, few factors, the row unit to confirm).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 131: "vincentarelbundock.github.io/Rdatasets/datasets.html".
- as published: 64,548 rows x 9 columns (OwnerAge, Gender, Area, RiskClass, VehAge, BonusClass, Exposure, ClaimNb, ClaimAmount), motorcycle partial casco (theft, fire), 1994-1998; target: ClaimNb per Exposure (claim frequency), or claim occurrence; access: open.
- Why: A real portfolio from a named insurer, documented in a standard pricing text and open.
- Adds: A motorcycle line and a fourth market (Sweden). Caveats: claims are rare (count not checked); 6 rating factors; CASdatasets says the data are 'aggregated across all policies and claims', so check whether a row is a policy or a tariff cell; dated 1994-1998.

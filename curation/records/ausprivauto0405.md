---
unique_name: ausprivauto0405
name: 'Australian private motor insurance 2004-2005 (de Jong and Heller): claim occurrence and frequency per policy'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Other
year: '2008'
domain: insurance
required_split:
- Random (IID)
original_data_state: One Table
source_links:
- https://dutangc.github.io/CASdatasets/reference/ausprivauto.html
- https://doi.org/10.1017/CBO9780511755408
- https://vincentarelbundock.github.io/Rdatasets/doc/insuranceData/dataCar.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 67,856 one-year motor policies (2004-2005) from de Jong and Heller's GLM textbook, with exposure, claim occurrence, count and amount: the insurer's claim-frequency pricing task, and insurance is thin; the rating factors are few and the insurer is unnamed.
- Source: de Jong and Heller 2008, Generalized Linear Models for Insurance Data, Cambridge University Press (doi 10.1017/CBO9780511755408); the data were on the book's site (www.acst.mq.edu.au/GLMsforInsuranceData, gone: CASdatasets says "Formerly on a website dedicated to P. De Jong and G.Z. Heller (2008)"). Copies: CASdatasets `ausprivauto0405` ("based on one-year vehicle insurance policies taken out in 2004 or 2005", 67,856 policies, 4,624 with at least one claim; 9 columns: Exposure, VehValue, VehAge, VehBody, Gender, DrivAge, ClaimOcc, ClaimNb, ClaimAmount) and insuranceData `dataCar` (67,856 x 11, adding the area and `X_OBSTAT_`). The country comes from the CASdatasets name; the book's page did not survive to confirm it.
- Use case: an insurer prices a motor policy at underwriting from its rating factors through the expected claim frequency per year of exposure, the book's worked example of claim occurrence and counts with GLMs; fit direct for ClaimNb with Exposure, or ClaimOcc. Regime IID: one row per policy, no date or holder id.
- Siblings and duplicates: no record of this source. `bemtpl97` (`TBD -> Yes`, 4), `fremtpl2` (`TBD -> Yes`, 4), `eumtpl` (`TBD -> Yes`, 3), `swedish_motorcycle_insurance` and `eudirectlapse` are other portfolios (PROV-7). The CASdatasets sibling `ausprivautolong` "is a simulated dataset" (40,000 policies over three periods) and is out (SEL-16). External collections: CASdatasets, insuranceData (Rdatasets).
- Better data: from the curator's Zotero collection (item 131, Rdatasets); no further search this round.
- Papers and pages: de Jong and Heller 2008 (the data); the CASdatasets and insuranceData help pages.
- Metric: none found (the CASdatasets and Rdatasets pages state none; the book was not read), so the fallback: `roc_auc` for ClaimOcc, or `rmse` on ClaimNb as for `bemtpl97` unless a Poisson deviance with Exposure is chosen (Exposure ships) (MET-1, MET-5, MET-8).
- Risks for /add-dataset: ClaimNb and ClaimAmount frame the outcome and go when ClaimOcc is the target (LEAK); Exposure enters as an offset or weight, as for `bemtpl97` and `fremtpl2`; only six rating factors (vehicle value, body, age, gender, area, driver age band), so the signal may be weak (TP-2, no reason against it); "based on" policies of an unnamed insurer: whether the rows were altered for the book is unclear (PROV-3, a question to settle on the data).
- Priority: gap + (insurance is thin, 3 accepted), use case +, source +, shape + (67,856 policies, mixed rating factors), risk - (few factors, the provenance of the rows).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 131: "vincentarelbundock.github.io/Rdatasets/datasets.html".
- as published: 67,856 one-year vehicle policies taken out in 2004 or 2005, 9 columns (Exposure, VehValue, VehAge, VehBody, Gender, DrivAge, ClaimOcc, ClaimNb, ClaimAmount); 4,624 policies with at least one claim; ...; target: ClaimOcc (at least one claim in the policy year), or ClaimNb with Exposure (claim frequency); access: open.
- Why: A real policy-level motor portfolio from a standard actuarial text, documented and open in two R packages, with the insurer's pricing task. Insurance is thin in the benchmark (bemtpl97 and fremtpl2 only).
- Adds: A third market (Australia) for claim-frequency pricing. Caveats: only 5 rating factors, so the task may be weak; the insurer is unnamed; ClaimNb and ClaimAmount frame the outcome and must be dropped; exposure handling as in bemtpl97. Its sibling ausprivautolong (insuranceData ClaimsLong, 120,000 rows) is simulated ...

---
unique_name: brazilian_vehicle_insurance_autoseg_2011
name: brvehins1 (CASdatasets, Brazilian vehicle insurance from SUSEP AUTOSEG, 2011)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Not Representative
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Larger IID Data
original_source: GOV Website
year: '2011'
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/dutangc/CASdatasets/blob/master/man/brvehins.Rd
- https://github.com/dutangc/CASdatasets/tree/master/data
- https://www2.susep.gov.br/menuestatistica/autoseg
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a lead list of exposure-scaled insurance tables, the source pages and papers, and the downloaded data where the notes say so. A human must verify the suggestion, the metadata and the notes before relying on them.**

CASdatasets `brvehins1a`-`e`: 1,965,355 rows built from AUTOSEG, the motor statistics of the Brazilian regulator
SUSEP, for 2011 (`brvehins.Rd`: "policy data based on the AUTOSEG", split at random into five parts). Measured
2026-10-20, the rows are rating cells, not policies: `ExposTotal` (vehicle-years) reaches 8,078 in one row and a row
holds up to 1,617 partial-collision claims (median exposure 0.53, 27% of rows above 2). Gender (with "Corporate"),
driver age band, model year, vehicle model (4,259) and area (40) give 1.49M distinct cells; 279k cells appear in more
than one row, perhaps split by a key CASdatasets dropped (semester or tariff class, unverified).

Data issues: 51,762 rows carry claims but zero exposure, premium and sum insured, most of them without gender or age.
They hold 15.4% of the claim amount, so the claims that did not join an exposure cell are missing from the cells that
should carry them. `ExposFireRob` and `PremFireRob` are 0 in every row, and `SumInsAvg` is 0 in 7.2%. On rows with
exposure the claim total is 0 in 83.7%, but that share falls from 91% at exposure <= 0.5 to 8% above 100
vehicle-years, and exposure alone gives AUC 0.84 for a claim. Untuned LightGBM on a 600k sample, random third held
out: AUC 0.89, R^2 0.26 on log1p among positives (0.81 and 0.20 without exposure and sum insured).

`ExposTotal` x `SumInsAvg` is the sum-insured exposure the Chubb recipe needs. AUTOSEG covers hull (casco) insurance
(SUSEP's page, read through a search snippet; the site refused connections from here), so all five claim types scale
with the vehicle's value. 2nd tier and `Not Representative` as for `swedish_motorcycle_insurance_wasa` and
`norwegian_automobile_insurance_norauto`: the target is a cell total, and its zeros mostly measure cell size. AUTOSEG
itself may be the better candidate: semester files from 2006-H2 (at least to 2020-H2, per search) would allow a
temporal split and a clean join of exposure and claims. `brvehins2` is the same 2011 data aggregated by city, without
gender and age. Licence: GPL (>= 2) for CASdatasets. To check: the AUTOSEG files, the repeated cells.

## Reference

CASdatasets (Dutang C., Charpentier A.), `brvehins1a`-`brvehins1e`, "Two Brazilian datasets for vehicle insurance",
from AUTOSEG (SUSEP), accessed February 2013. https://github.com/dutangc/CASdatasets/blob/master/man/brvehins.Rd

SUSEP, AUTOSEG - Sistema de Estatísticas de Automóveis. https://www2.susep.gov.br/menuestatistica/autoseg

Lead: curator's list of exposure-scaled insurance tables (Chubb comparison), 2026-10-20; not in the v4 workbook.

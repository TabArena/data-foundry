---
unique_name: upper_mississippi_sav_rake_biomass
name: SAV biomass - Upper Mississippi River / developing methods for estimating SAV biomass (LTRM Pools 4 and 8, 2017)
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Trivial
tags:
- Two-Regime Zeros
original_source: GOV Website
year: '2020'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.usgs.gov/datacatalog/data/USGS%3A5e2b0313e4b0a79317cf9500
- https://doi.org/10.5066/P9GFFYZH
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: a USGS calibration release that pairs the Long Term
Resource Monitoring's 0-5 rake density score with the fresh weight on the same rake (1,922 records at 100 sites, Pools 4
and 8, summer 2017); a stated estimation aim with a measured label, but close to a one-score calibration whose zero part
follows from a zero score.
- Source: Schlifer, Drake and Lund (2020), USGS data release doi:10.5066/P9GFFYZH (UMESC, public domain; the reference
  below names Drake and Lund, the authors of the completion report LTRM-2018BI03, 45 pp., of which only the abstract was
  read). As published (FGDC metadata, read 2026-10-27 from data.usgs.gov; the CSVs sit behind ScienceBase's Cloudflare
  check, 403): `veg_estimate_biomass_site_list.csv` (100 sites: pool, barcode, site number, stratum, date, 19 June to 9
  August 2017) and `veg_estimate_biomass_data.csv` (rakeID 1-1922, pool, stratum, site number, rake number 1-6, species
  group, species, `Fresh weight (g)` 0-4110, `PD_group`, `PD_spp`, `PD_sav_new`, notes). The target: "all weights less
  than one gram were entered as one gram, a value of 0 means no submersed aquatic vegetation present at the site".
- Use case: the source's purpose: "The ability to estimate biomass would allow us to supplement current quantification
  of SAV-based processes such as waterfowl and fish habitat provision" (metadata), since the monitoring "currently
  provides only a rough index of aquatic vegetation biomass" (report abstract). For example the monitoring team
  converting each site's rake scores into biomass after the annual survey; Drake, Lund and Kreiling (2022) did this for
  1998-2018 against diver-harvested biomass. Fit approximate: two pools in one summer stand for all reaches and years,
  and rake weight is not plot biomass. Regime grouped by site.
- Doubt: the earlier pass set `No` with `No Good Target / Scientific Discovery` and `Trivial`. The source states an
  estimation aim and the label is a measured weight (SEL-3 holds), so the first marker is dropped; whether the score
  makes the task trivial is a reading to probe (TP-4), kept as a provisional `Trivial`.
- Siblings and duplicates: none in the log (searched submersed, LTRM, Mississippi). A related USGS release, "Submersed
  macrophyte biomass estimates, Pools 4, 8 and 13, Upper Mississippi River, 1998-2018", holds model outputs; the 2022
  paper's diver-harvest data may be the better task (not checked). External collections: none found.
- Papers and pages: the completion report (UMESC page, abstract); Drake, Lund and Kreiling, Journal of Fish and Wildlife
  Management 13(1):205-222 (2022), doi:10.3996/JFWM-21-063 (abstract); Yin and Kreiling, Hydrobiologia 675:187-195
  (2011), on the rake method (cited in the metadata).
- Metric: none found (metadata, report abstract, 2022 abstract); fallback `rmse`.
- Risks for /add-dataset: `PD_sav_new` is the field crew's visual score of the same rake ("the standard score of
  submersed aquatic vegetation given during the Long Term Resource Monitoring Vegetation sampling effort"): the input
  the use case acts on, so it stays, but it may make the task near-deterministic (TP-4), and a zero score likely means a
  zero weight; the 1 g floor censors small weights; the metadata does not say whether a record is a rake or one species
  on a rake (the unit); rows and the zero share not measured.
- Priority: gap 0, use case 0 (fit approximate), source + (USGS release with FGDC metadata and a report), shape + (1,922
  records at 100 sites, eight features, grouped), risk - (likely near-deterministic, a reading to probe).

**Assessment (AI, 2026-10-30):** The family's open question on coded and censored zeros is settled (Andrej, 2026-10-30,
policy question 2 of the zero-inflated review: "We don't care. We want to add any relevant predictive task, independent
if it is zero inflated or not"), so how the source codes its zeros is no reason for a No or a lower priority. The 1 g
floor on small weights is a cleaning choice at /add-dataset. The verdict and priority stay on the screening's other
points.

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 2, as screened (verified on the zero-inflated screening review
page).

A USGS method-calibration data release (Upper Midwest Environmental Sciences Center, LTRM): submersed aquatic
vegetation on rakes at 100 sites in Pools 4 and 8, 19 June to 9 August 2017, with rake IDs 1-1922, stratum, rake
number (1-6), species and species group, "Fresh weight (g)" (0-4110) and a 0-5 rake density score (`PD_sav_new`).
The metadata states the purpose: "Relationships between submersed aquatic vegetation mass caught on rakes and total
plot biomass were developed". The rake density score is the visual fullness score of the same rake, a direct proxy
for the weight, hence the provisional `Trivial`. The two CSVs sit on ScienceBase behind a Cloudflare challenge (403)
and were not downloaded; counts come from the FGDC metadata.

Zero mechanism, from the metadata only: "a value of 0 means no submersed aquatic vegetation present at the site",
i.e. nothing on the rake, which is non-detection rather than proven absence, and the zero part is given by a density
score of 0; also "weights less than one gram were entered as one gram". Workbook pushback: the data are 2016-17 field
work released in 2020, and no 2026 structural-zero paper using them was found. Licence: public domain (USGS).

## Reference

Drake D., Lund E. (2020). Developing methods for estimating SAV biomass in the Upper Mississippi River. U.S.
Geological Survey data release, doi:10.5066/P9GFFYZH (LTRM completion report LTRM-2018BI03).

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 4 (SAV biomass - Upper Mississippi River).

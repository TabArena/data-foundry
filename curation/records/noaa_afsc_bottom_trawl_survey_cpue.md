---
unique_name: noaa_afsc_bottom_trawl_survey_cpue
name: NOAA AFSC bottom trawl surveys (Groundfish Assessment Program, FOSS haul / catch / species tables), 1982-2026
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: GOV Website
domain: biology & life sciences
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.fisheries.noaa.gov/foss/f?p=215:28
- https://apps-st.fisheries.noaa.gov/ods/foss/afsc_groundfish_survey_haul/
- https://github.com/afsc-gap-products/gap_products
- https://doi.org/10.7289/V5/TM-AFSC-357
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

Bottom trawl surveys of AFSC's Groundfish Assessment Program (eastern and northern Bering Sea, Bering Sea slope,
Gulf of Alaska, Aleutian Islands), public through the FOSS API as HAUL, CATCH and SPECIES tables. Downloaded on
2026-10-20: 35,561 hauls from 1982-2026 with date, position, depth, bottom and surface temperature, vessel and net
geometry. The EBS grid has 376 stations sampled about 44 times each; GOA and AI stations are mostly sampled once or
twice. The surveys exist to "produce fishery-independent biomass (weight) and abundance (number) estimates"
(gap_products docs, "What is the research objective?"), but AFSC's essential-fish-habitat work uses the hauls
predictively: hurdle GAMs on CPUE for species caught in 10-30% of hauls, tested on "20% of the data withheld at
random" (Laman et al. 2017, NOAA-TM-AFSC-357, pp. 15-17). That makes this the strongest case so far for counting
species-abundance mapping as prediction (the open question of the 2026-10-19 batch); the call is the curator's.

Zero mechanism, confirmed from the data: CATCH holds positive catches only, so zeros come from crossing hauls with
a species. Pacific cod has 22.2% zeros (EBS 4.0%, GOA 36.7%), walleye pollock 17.6%; a species from the EFH hurdle
class would give a stronger zero regime. Split: temporal by survey year; grouped by station is the alternative.
Untuned LightGBM on cod CPUE from survey, position, depth, temperature and date, test years 2024-26 / 2022-23 /
2019-21: AUC 0.91 / 0.93 / 0.91 for a catch, R^2 0.27 / 0.19 / 0.16 on log1p CPUE among positives (pollock 0.50 /
0.37 / 0.44); most of the AUC is the region. Drop the species' weight and count and the other species' catch in the
same haul. sdmTMB's `pcod` is not a subset of this survey: it is Queen Charlotte Sound (British Columbia) trawl data
(sdmTMB `R/data.R`). Public domain; AFSC asks to be acknowledged. To check: the species, and whether the 2,659 hauls
with a non-zero performance code stay.

## Reference

Laman E.A., Rooper C.N., Rooney S.C., Turner K.A., Cooper D.W., Zimmermann M. (2017). Model-based essential fish
habitat definitions for Bering Sea groundfish species. U.S. Dep. Commer., NOAA Tech. Memo. NMFS-AFSC-357, 265 p.
doi:10.7289/V5/TM-AFSC-357. Data: NOAA Fisheries AFSC Groundfish Assessment Program bottom trawl survey data, Fisheries
One Stop Shop (FOSS), https://www.fisheries.noaa.gov/foss (accessed 2026-10-20).

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).

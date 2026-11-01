---
unique_name: fueleconomy_tax_incentives
name: Tax Incentives
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
collections:
- STRABLE
source_links:
- https://www.fueleconomy.gov/feg/ws/tax-data-services.shtml
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/tax-incentives
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, SEL-3): the target is the federal clean-vehicle tax credit a model qualifies for, an amount set by statute from battery capacity (vehicles before 2023) or from the critical-mineral and battery-component requirements (from 18 April 2023), not an observed outcome or an expert annotation; the buyer looks it up, the credit ended for vehicles acquired after 30 September 2025, and the phase-out columns are fixed fractions of the target.
- Source: DOE/EPA fueleconomy.gov tax-credit web service (https://www.fueleconomy.gov/feg/ws/tax-data-services.shtml): XML or JSON lists of qualifying models, for new vehicles placed in service from 18 April 2023 and pre-owned ones from 1 January 2023, plus older plug-in credit lists. STRABLE parsed the XML files and summed fullcreditamount, creditamount and taxcredittotal into credit_amount: 908 rows x 21 columns, 32 distinct amounts (7,500 on 607 rows, 3,750 on 82). STRABLE's paper links another dataset, Connecticut's business tax incentives (data.ct.gov, App. C.2), not the one its script reads.
- The rule, in the sources' words: "A vehicle meeting both sourcing requirements may be eligible for the full $7,500 credit ... a vehicle meeting only one of these sourcing requirements may be eligible for a credit of $3,750. A vehicle meeting neither requirement will not be eligible for a credit" (https://www.fueleconomy.gov/feg/tax2023.shtml); for earlier vehicles "$2,917 for a vehicle with a battery capacity of at least 5 kilowatt hours (kWh)", "Plus $417 for each kWh of capacity over 5 kWh", "The maximum credit is $7,500" (IRS, https://www.irs.gov/businesses/plug-in-electric-vehicle-credit-irc-30-and-irc-30d); "as long as the vehicle is acquired by September 30, 2025, the taxpayer can claim the credit upon possession" (tax2023).
- Measured on STRABLE's file (a preview): where present, credit_amount equals 2 x phaseout50amount on all 68 rows and 4 x phaseout25amount on all 51 rows.
- Use case: none (USE-2): the amount is a published legal determination per model; the rule's inputs (battery kWh, sourcing compliance) are not in the table, so what remains is a lookup without its key (SEL-5).
- Siblings and duplicates: `fueleconomy_vehicles` and `epa_fuel_economy_vehicles` (fueleconomy.gov vehicle data, another table). External collections: STRABLE ("Tax Incentives").
- Better data: a candidate of the benchmark STRABLE (the run searched no further).
- Metric: none found; STRABLE scores R^2 (App. D.1).
- Also: 908 rows.
- Reject check (AI, 2026-10-31): stands. The amount is set by statute: 'A vehicle meeting both sourcing requirements may be eligible for the full $7,500 credit ... meeting only one ... $3,750' (https://www.fueleconomy.gov/feg/tax2023.shtml) and '$2,917 for a vehicle with a battery capacity of at least 5 kilowatt hours (kWh)', 'Plus $417 for each kWh of capacity over 5 kWh' (https://www.irs.gov/businesses/plug-in-electric-vehicle-credit-irc-30-and-irc-30d). This is a legal determination a buyer looks up per model, not an observed outcome or an expert annotation, and the phase-out columns are fixed fractions of it.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 908 rows x 21 columns incl. target (STRABLE parquet); target: credit_amount.
- Why: Predict the federal tax credit amount of a clean vehicle model
- Notes: Mismatch: the paper links Connecticut's business tax incentives (data.ct.gov), but the config source is fueleconomy.gov and the script reads the fueleconomy.gov tax-credit web service. Credit amounts follow IRS rules from the listed attributes (MSRP limit, assembly rule), so possibly near-deterministic. Small: 908 ...

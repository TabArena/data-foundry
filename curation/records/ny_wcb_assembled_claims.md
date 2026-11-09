---
unique_name: ny_wcb_assembled_claims
name: 'Assembled Workers'' Compensation Claims: Beginning 2000 (New York State Workers'' Compensation Board)'
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
domain: insurance
required_split:
- Temporal (NON-IID)
original_data_state: One Table
source_links:
- https://data.ny.gov/d/jshw-gkgu
- https://catalog.data.gov/dataset/assembled-workers-compensation-claims-beginning-2000
- https://data.ny.gov/api/views/jshw-gkgu/columns.json
- https://catalog.data.gov/dataset/nyswcb-workers-compensation-claim-multiple-body-parts
v2_path: datasets/_dev/tabarena-v0pt2/ny_wcb_assembled_claims_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: New York's open table of 5.66 million workers' compensation claims since 2000, every column defined, with an 8-class benefit outcome (`Claim Injury Type`); a real claims-triage task at assembly once the many fields filled after assembly are dropped and unresolved recent claims are handled.
- Source: New York State Workers' Compensation Board (WCB Data Management & Analytics), "Assembled Workers' Compensation Claims: Beginning 2000" on data.ny.gov (dataset jshw-gkgu; portal metadata: view created 2014-12-04, publication date 2021-06-18, posted quarterly, rows updated 2026-09-21; `year` left empty for that reason). As published: one table of 5,655,563 claims assembled 2000-01-01 to 2026-09-04 (Socrata API count, 2026-10-31) x 54 documented columns: accident, assembly, C-2, C-3, ANCR, controverted, first hearing, first appeal, PPD, PTD and Section 32 dates; age at injury, birth year, gender, average weekly wage, attorney, carrier name and type, county, district, NAICS industry, medical fee region, zip code, WCIO and OIICS cause, nature and body-part codes, COVID-19 indicator, claim type, current status, highest process, hearing, IME-4 and closed counts. Target `Claim Injury Type`, "the claim injury in terms of the benefits awarded by Board ... from least to most severe": CANCELLED 114,549, NON-COMP 2,696,406, MED ONLY 765,510, TEMPORARY 1,313,873, PPD SCH LOSS 627,508, PPD NSL 124,965, PTD 5,757, DEATH 6,995.
- Use case: when a claim is assembled, the Board or the carrier routes it (a fast track for likely non-compensable or medical-only claims, an adjuster and early case management for likely lost-time or permanent ones) from what the first reports hold. The page describes the Board's process ("processes and adjudicates claims for benefits") but names no prediction, so the use case is ours; fit approximate. Regime temporal: claims arrive over 26 years and a model serves new ones (split by assembly date, with a maturity gap, SPLIT-10).
- Siblings and duplicates: no record of this table (grep workers' compensation, jshw-gkgu); `bnp_paribas_cardif_claims_management` is another insurer's anonymized claims task with another target, no version. Kaggle copies (new-york-state/nys-assembled-workers'-compensation-claims, 2021; thedevastator, 2023) are later re-uploads. External collections: none found.
- Better data: found as a related task for `bnp_paribas_cardif_claims_management` (the run searched no further).
- Papers and pages: the data.ny.gov page and its column dictionary; no paper or competition defining a task found (one web search; the Kaggle competitions API for "workers", "WCB", "compensation claim", "injury type").
- Metric: none found (same places), so the fallback `log_loss` for the 8-class target (MET-8); inputs none.
- Risks for /add-dataset: fields set after assembly go (USE-3, LEAK-10): ANCR date and interval, controverted, hearing, appeal and Section 32 dates, hearing, IME-4 and closed counts, current status, highest process, alternative dispute resolution; check the timing of attorney and C-3 date. The PPD and PTD dates restate classes 5 to 7. The type is the benefit awarded so far, so recent claims are unresolved (LEAK-24, SPLIT-10). CANCELLED ("assembled in error or determined to be a duplicate") is no outcome of an injury: drop it (USE-5). Birth year and zip code together identify people more than the task needs. Size: cut years or sample under the row cap.
- Priority: gap + (insurance and multiclass are thin), use case 0 (ours), source + (a state agency, every column defined), shape + (5.66M claims, dates, codes and numbers), risk - (many post-assembly fields, censored recent claims).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `bnp_paribas_cardif_claims_management`.
- as published: 5,655,563 claims (count via the Socrata API, 2026-10-31) x about 57 documented columns: accident, assembly, C-2, C-3, ANCR, controverted, first hearing, appeal and PPD/PTD dates; age at injury, ...; target: Claim Injury Type (benefits awarded, ordered from cancelled and non-compensable to medical only, temporary, permanent partial, permanent total and death), or ...; access: open.
- Why: BNP Paribas Cardif's task is claims triage (which claims can be approved fast, which need more information) on anonymized data whose structure was only recovered by de-anonymizing. No de-anonymized claims-triage table was found; this is the closest real, documented, claim-level triage table, from a public agency, ...
- Adds: A documented claims-triage task in insurance (thin domain) with dates, so a temporal split by assembly date is natural; far larger and newer than any claims table we hold. Risks: many fields are filled after assembly (hearing, appeal, PPD/PTD, Section 32 dates, hearing and IME-4 counts, current status, highest ...

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: the three WCIO codes, industry, age with the birth year, accident date, home ZIP, medical fee region and district dropped as values the table stores after assembly with a traced gain (LEAK-10 clause 2: on 105,786 matched claims of 2021 the 2026 values beat the June 2021 values by 0.030-0.037 log loss; each dropped block above 2 SE), and the insurer's name and type with them as the rule's default; history from 2016 (SPLIT-20, the EDI ramp); `fit_reason` names the insurer's lost-time desk and the inputs it holds that the table lacks; label maturity (about 12-13% of the test windows' PPD NSL and PTD awards still to come), the C-2 redefinition, the accident-date reason and the sex law read in the notes; NON-WC decoded; nothing restored from the June 2021 copy, which is not needed as a raw file: its insurer spellings carry more of the outcome than the 2026 ones and it would restore 259 cells); 1,152,698 claims, 6 features, log loss 1.02-1.04 against class shares 1.055-1.076, task probes without flags; disputed: LEAK-10 clause 2 (the bar for a field's return: settled, none returns; the residual of the kept fields: settled, it sat in the insurer, the fee region and the district; the insurer's drop: issue 1; the C-3 date, borderline: issue 3), SEL-1 (sex: issue 2, with rais_employment_separation issue 1); for the curator: issues 1-3. Priority 3: gap +, use case 0, source +, shape +, risk - (use case ours, fit approximate; risk: a thin task of six coarse fields, 3.2-4.0% below the class shares, 60% exact duplicate rows, and the label to date).

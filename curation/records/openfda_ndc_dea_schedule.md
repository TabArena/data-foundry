---
unique_name: openfda_ndc_dea_schedule
name: 'openFDA NDC directory: DEA schedule'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
domain: medical & healthcare
problem_type: Multiclass Classification
source_links:
- https://open.fda.gov/apis/drug/ndc/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/drug-ndc
- https://arxiv.org/abs/2605.12292
- https://download.open.fda.gov/drug/ndc/drug-ndc-0001-of-0001.json.zip
- https://open.fda.gov/fields/drugndc.yaml
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-01):** `TBD -> 2nd Tier`, priority 3: the FDA's National Drug Code directory, cut by STRABLE to products with a DEA schedule and that schedule as target. The law schedules each substance (and some combinations by strength) and the labeler reports it, so the task is a lookup of the scheduling regulation from the active ingredients rather than a prediction (the `drug_directory` and `fda_device_classification` precedent).
- Source: FDA, openFDA NDC directory (https://open.fda.gov/apis/drug/ndc/; bulk file https://download.open.fda.gov/drug/ndc/drug-ndc-0001-of-0001.json.zip, export of 2026-10-30): 138,216 product listings, 6,338 of them with a schedule (CII 2,239, CIV 2,161, CIII 976, CV 950, CI 12; API count of 2026-11-01). Field reference (https://open.fda.gov/fields/drugndc.yaml): `dea_schedule` "is the assigned DEA Schedule number as reported by the labeler. Values are CI, CII, CIII, CIV, and CV." As used by STRABLE (HF parquet, previewed): 583 rows x 22 columns, target `dea_schedule` (CII 215, CIV 169, CIII 161, CV 38), with generic and brand name, labeler, `active_ingredients` with strengths, dosage form, route, product type (309 prescription drugs, 205 bulk ingredients), marketing category and dates, `pharm_class`; how STRABLE drew 583 of the 6,338 is not stated in what was read.
- Use case: the labeler knows its product's schedule from 21 CFR 1308 and reports it, and a new substance is scheduled by the DEA, not estimated; no source names a prediction (USE-2). Fit none. Regime IID (one snapshot of current listings), with one substance listed by many labelers as a grouping.
- Measured on the preview: 216 ingredient combinations; 559 of 583 products sit in combinations with a single schedule; the other 24 are combinations the law schedules by strength (acetaminophen with codeine, codeine with guaifenesin, diphenoxylate with atropine) and dronabinol.
- Siblings and duplicates: `drug_directory` (Lennart, `TBD -> 2nd Tier`: "Just a list of drug listings, not a real predictive task"; OpenML 43044, the FDA NDC product file with target `PRODUCTTYPENAME`): the same directory with another target (PROV-7, no duplicate while the targets differ). Other FDA tables of STRABLE: `fda_device_classification` (`TBD -> 2nd Tier`, priority 3, a lookup of the classification regulation), `fda_drugs_at_fda` (`TBD -> 2nd Tier`, priority 2). External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C, "Drug NDC": "National Drug Code Directory containing all drugs in the US. The task is to predict the drug category."; its config predicts `dea_schedule`).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the openFDA field reference; 21 CFR 1308.11 to 1308.15 (the schedules, not read); STRABLE.
- Metric: none found (openFDA publishes a directory, no task; STRABLE's AUROC is benchmark-wide, MET-5), so the fallback `log_loss`; inputs none.
- Risks for /add-dataset: the target is a lookup of the law (SEL-5, TP-4): with `active_ingredients` and strengths the task is the regulation, and without them `generic_name`, `brand_name` and `pharm_class` still name the substance; `product_ndc`, `product_id`, `spl_id`, `packaging` and `openfda` are ids or nested lists; CI has 12 products in the whole directory (TP-8); bulk ingredients and finished products mixed.
- Priority: gap + (multiclass thin), use case 0 (none), source + (openFDA field reference), shape + (6,338 scheduled products in the directory; text, categorical and dates), risk - (the target is a lookup of the scheduling regulation).

**Assessment (AI, 2026-11-01):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292) as "Drug NDC"; split out on 2026-11-01 from the note on `drug_directory`, the same FDA directory with another target.
- as published: 583 rows x 22 columns incl. target (STRABLE parquet); target: dea_schedule.
- Why: Predict the DEA controlled-substance schedule of a drug product listing
- Notes: Related record: drug_directory (TabSTAR; OpenML 43044, the same FDA National Drug Code directory, target PRODUCTTYPENAME; 'not a real predictive task'). STRABLE's version is the openFDA NDC API with target dea_schedule and only 583 rows (scheduled products), so a different target on the same source.

---
unique_name: usaid_scms_shipment_delivery
name: USAID Supply Chain Shipment Pricing Dataset (PEPFAR SCMS shipments of ARV and HIV lab commodities)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: GOV Website
original_data_state: One Table
source_links:
- https://data.usaid.gov/HIV-AIDS/Supply-Chain-Shipment-Pricing-Data/a3rc-nmf6
- http://web.archive.org/web/20241217023901/https://data.usaid.gov/api/views/a3rc-nmf6
- https://www.kaggle.com/datasets/divyeshardeshana/supply-chain-shipment-pricing-data
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: USAID's real shipment listing of PEPFAR SCMS antiretroviral and HIV lab commodity deliveries (10,324 line items, 33 columns, with scheduled and actual delivery dates), published for price transparency; a late-delivery or freight-cost target would be ours, and the first publication is offline.
- Source: USAID Bureau for Global Health, Supply Chain Management System (SCMS) project, "Supply Chain Shipment Pricing Data" on the USAID Development Data Library (data.usaid.gov, view a3rc-nmf6; the domain no longer resolves). The run's Assessment read the Wayback copy of the portal metadata (posted 2018-11-12, CC BY-ND 4.0, deliveries 2006-2015, a caveat that lead times "by product/country will not be accurate"); this session could not reach web.archive.org to re-read it. Copy: Kaggle divyeshardeshana/supply-chain-shipment-pricing-data (`SCMS_Delivery_History_Dataset.csv`, 3.8 MB, 2019-10-08, licence "unknown", no description). As published (the Assessment): 10,324 line items x 33 columns: country, managed by, fulfil via, vendor INCO term, shipment mode, PQ and PO dates, scheduled delivery, delivered to client, delivery recorded dates, product group, vendor, molecule, dosage, quantity, line item value, pack and unit price, manufacturing site, weight, freight cost, insurance.
- Use case: a procurement planner decides at purchase-order time whether a shipment needs expediting or buffer stock, from its mode, vendor, product and route; the source publishes the data for pricing transparency and names no prediction, so the target would be ours (`No Good Target (yet)`); fit approximate; regime temporal by order date.
- Siblings and duplicates: `ecommerce_shipping` (`No (Retired)`: a generated file; the on-time task it claimed). No other record of this file. No duplicate. External collections: none found.
- Better data: found as better data for `ecommerce_shipping` (the run's Assessment); no further search this round.
- Papers and pages: the USAID page (offline) and the Kaggle copy; Kaggle notebooks on it not read.
- Metric: none (the source defines no task), so the fallback for the target chosen: `roc_auc` for late delivery, `rmse` for the delay or the freight cost (MET-1, MET-8).
- Risks for /add-dataset: the origin is offline and the data copy is a Kaggle re-upload without notes, so check that it matches the portal's 33 columns and row count (PROV-1, PROV-2); the target is ours (USE-5); weight, freight and insurance are recorded with or after shipping, and these and the date columns may hold text placeholders (LEAK, CLEAN); USAID's own warning that lead times are not accurate questions a delay target; CC BY-ND (EV-4: no reason for a verdict).
- Not checked: the portal metadata and its wording (Wayback unreachable from this session); the Kaggle file's content (not downloaded).
- Priority: gap 0 (business & marketing has 25 accepted), use case 0 (no prediction named), source + (a US agency's release), shape + (10,324 rows, mixed types, dates), risk - (a target of our own, an offline origin, post-shipment columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ecommerce_shipping`.
- as published: 10,324 shipment line items x 33 columns: country, managed by, fulfil via, vendor INCO term, shipment mode, PQ/PO dates, scheduled delivery date, delivered to client date, product group, vendor, ...; target: late delivery (delivered to client date after the scheduled delivery date) or the delay in days; freight cost is a second target; access: open.
- Why: ecommerce_shipping was retired because its file is generated (warehouse and mode fill patterns of the row counter); the task it pretended to hold, whether a shipment arrives on time from shipment mode, weight, cost and product features, is what this real government file records
- Adds: a real, traceable source with scheduled and actual delivery dates instead of a generated table. Caveats: the USAID portal is offline since USAID's closure (2025), so the copies are the Wayback snapshot of the metadata and Kaggle uploads of the CSV (2018); CC BY-ND 4.0 (check whether a benchmark derivative is ...

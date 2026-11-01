---
unique_name: sao_paulo_itbi_transactions
name: Dados das Transacoes Imobiliarias com recolhimento de ITBI-IV (São Paulo real-estate transactions with transfer tax paid)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://prefeitura.sp.gov.br/fazenda/w/acesso_a_informacao/31501
- https://www.kaggle.com/datasets/juliotorniero/real-estate-transactions-sao-paulo-brazil
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: São Paulo's registry of urban property transfers on which the transfer tax (ITBI) was paid, published monthly by the city's finance secretariat since 2006, one row per transfer declaration with the declared price, the cadastral data of the property and the date; a sale-price task from official records with a temporal split, but some columns are computed from the price.
- Source: Prefeitura de São Paulo, Secretaria Municipal da Fazenda, "Dados das Transações Imobiliárias com recolhimento de ITBI-IV": one row per transfer declaration (DTI) paid in the month, the transaction date being the signing of the deed or sale instrument; rural properties and transfers paid through the PPI instalment programme excluded; one xlsx and ods file per year, 2006 to 2026, the current year updated monthly; the 2019-2021 files were corrected for the transaction-nature descriptions. The page describes no columns and states no licence. The Kaggle copy (juliotorniero, "Real Estate Transactions Sao Paulo - Brazil", 2022, CC0, one 17.5 MB CSV of May to October 2022) documents the columns: tax_id, street name and number, complement, district, reference, zip code, transaction_nature, transaction_value_BRL, date, cadastral_value, tax_base_value, mortgage_type, mortgage_value, registry office and property id, city_hall_status, land_area_m2, front_length_m, ideal_fraction, area_built_m2, two descriptions (use and type), year_built; it states "over 14,000 official real state transactions per month". The city's files are the origin (PROV-8).
- Use case: the city's tax office checks a declared price against what the property should fetch, to audit under-declared transfers; or a bank or buyer appraises a property at the sale; the source names neither, fit approximate. Regime temporal: dated transactions over 20 years (SPLIT-6); a property sold twice is a grouped question inside it (SPLIT-13).
- Siblings and duplicates: `brazilian_houses` (`TBD -> 2nd Tier`, `Data Quality Issue`, `Not Representative`: scraped rental adverts without dates), next to which this was found as a related task (sale price, not rent); `sao_paulo_property_price_images` (`TBD -> 2nd Tier`, a 2024 scrape of asking prices) and `goiania_apartment_prices` (`TBD -> Yes`). Another source and target, no duplicate (PROV-4). External collections: none found.
- Better data: found as a related task next to `brazilian_houses`; no further search this round.
- Papers and pages: the city's page; the Kaggle copy's card. No paper found (web search budget used up before a search).
- Metric: none from the source (an open-data release), so the fallback `rmse`, or `rmsle` on the price from context (MET-11), the curator's call; inputs none.
- Risks for /add-dataset: `tax_base_value` is the "base value for transaction tax calculation" (Kaggle card), which the tax rules set from the declared value or the city's reference value (to confirm), so it likely carries the target (LEAK-10, to drop); `mortgage_value` is fixed with the price at the same deal, likely a strong partial leak (USE-3); `cadastral_value` is the city's assessed value known before the sale, a legitimate but dominant input (TP-4 to read); `ideal_fraction` below 1 means a share of the property was transferred, so the price is of a share (filter or keep with the fraction, USE-5); non-market transaction natures (transfers between relatives or to a company) to filter; addresses, tax and registry ids are ids, not features; declared values may be under-declared (the target's quality); yearly files to stack, with columns to align across 20 years.
- Priority: gap 0 (business & marketing, regression and temporal are not thin), use case 0 (no actor named by the source), source + (the city's finance secretariat), shape + (about 14,000 transfers a month over 20 years, mixed features, dates), risk - (columns computed from the target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `brazilian_houses`.
- as published: One row per paid transfer declaration (DTI); the city says over 14,000 transactions per month (Kaggle copy May-Oct 2022); columns per the Kaggle copy: district, zip, transaction nature, transaction ...; target: Declared transaction value (BRL) of an urban property sale; access: open (xlsx/ods per year from the city's page).
- Why: Same domain as the record (Brazilian housing prices) but a sale-price task from the official registry instead of scraped rental ads: dated transactions (a temporal split, which the record's comment says is missing) and real prices rather than asking rents
- Adds: Official, traceable source, about 20 years, likely millions of rows, transaction dates; not the record's rent target, hence 'related'. Caveats: cadastral value is a strong, partly leaking feature to judge; address/registry IDs need dropping

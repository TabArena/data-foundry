---
unique_name: alko_wine_price_list
name: Alko price list (Alkon hinnasto tekstitiedostona), the Finnish alcohol retail monopoly's full catalogue
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Company
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.alko.fi/INTERSHOP/static/WFS/Alko-OnlineShop-Site/-/Alko-OnlineShop/fi_FI/Alkon%20Hinnasto%20Tekstitiedostona/alkon-hinnasto-tekstitiedostona.xlsx
- https://www.alko.fi/
- http://web.archive.org/web/20221001133854/https://www.alko.fi/INTERSHOP/static/WFS/Alko-OnlineShop-Site/-/Alko-OnlineShop/fi_FI/Alkon%20Hinnasto%20Tekstitiedostona/alkon-hinnasto-tekstitiedostona.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the Finnish alcohol monopoly's own catalogue, about 7,600 wines with price, origin, grapes, vintage, alcohol, acids, sugar and a short description; the live file seems gone since Alko rebuilt its site, so archived snapshots are the copy.
- Source: Alko Oy, "Alkon hinnasto tekstitiedostona" (an Excel price list on alko.fi). The archived copy of 2022-09-30 (Wayback Machine; also 2021-12-19), opened for its header: 11,551 products, 30 columns (Numero, Nimi, Valmistaja, Pullokoko, Hinta, Litrahinta, Uutuus, Tyyppi, Alatyyppi, Valmistusmaa, Alue, Vuosikerta, Rypäleet, Luonnehdinta, Pakkaustyyppi, Suljentatyyppi, Alkoholi-%, Hapot g/l, Sokeri g/l, Energia kcal/100 ml, Valikoima, EAN and beer columns); wines: 3,096 red, 2,247 white, 1,388 sparkling, 438 rosé, 460 dessert and fortified. Target `Hinta` (EUR per bottle). The listed URL now returns an HTML page, and a scraper's page states "That file is gone since Alko rebuilt its website" (apify.com, third party); no licence stated.
- Use case: an importer offering a wine to the monopoly, or Alko's buyer, estimates the shelf price from what is known at listing; not named by the source; fit approximate (the run's note: the monopoly price is the supplier's price plus Alko's margin, excise and VAT; not verified here); regime IID over products (one catalogue snapshot).
- Siblings and duplicates: `wine_world_cost` (Yes, 1,279 wines of one UK shop); other wine-price records `wine_rating_price`, `winevivino`, `wine_reviews_winemag_130k` (TBD -> 2nd Tier) come from other sources; no Alko record (grep for alko). External collections: none found.
- Better data: found as better data for `wine_world_cost`; no further search this round.
- Papers and pages: the price list file and its archived snapshots; no paper.
- Metric: none found (a price list, no task); fallback `rmse`, on a log price (MET-3, MET-8); inputs none.
- Risks for /add-dataset: `Litrahinta` is the target over the bottle size (drop, LEAK-27); one wine in several vintages or sizes across the split (LEAK-16: group by producer and name, or note it); pin one dated archived snapshot (the live file is gone); the excise follows alcohol and volume, so part of the price is a rule of the features (SEL-5, TP-4 to check).
- Priority: gap 0 (business & marketing, regression, IID not thin), use case 0 (none named), source + (the publisher's own catalogue), shape + (about 7,600 wines, categorical, numeric and short text), risk - (only archived snapshots remain).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `wine_world_cost`.
- as published: about 11,900 products (all drinks; wines the largest group, their count not opened), one row per product, ~30 columns: name, producer, bottle size, price (EUR), price per litre, new, type, subtype, ...; target: shelf price of a bottle in EUR, rows filtered to wines; access: open (public Excel file, no licence stated; alko.fi answered our automated fetch with 403, the URL is used by public code from 2025-2026).
- Why: same target (a shop's bottle price) and use case, features of the same kind known at listing (country, region, grapes, vintage, alcohol, bottle size, style, a short description)
- Adds: several times the 1,279 wines of one scraped UK shop, a named publisher's own file instead of a scrape, maintained daily. Notes: the monopoly price is supplier price plus a set margin and excise by alcohol content; price per litre is a function of the target and must go

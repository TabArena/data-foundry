---
unique_name: visuelle_new_fashion_product_sales
name: 'VISUELLE: new fashion product sales of Nunalie (from ''Well Googled is Half Done: Multimodal Forecasting of New Fashion Product Sales with ...'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2021'
domain: business & marketing
source_links:
- https://arxiv.org/abs/2109.09824
- https://doi.org/10.1002/for.3104
- https://github.com/HumaticsLAB/GTM-Transformer
- https://openaccess.thecvf.com/content/CVPR2022W/CVFAD/supplemental/Skenderi_The_Multi-Modal_Universe_CVPRW_2022_supplemental.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 5,577 new products of an Italian fast-fashion retailer with 12 weeks of sales after release and a stated pre-launch ordering protocol; but the tabular inputs are three tags and a date, the source's models lean on the product image and Google Trends, and the target is a weekly curve to collapse into one number.
- Source: Skenderi, Joppi, Denitto, Cristani, "Well Googled is Half Done: Multimodal Forecasting of New Fashion Product Sales with Image-based Google Trends", arXiv 2109.09824 (v1 2021-09-20; Journal of Forecasting 2024, doi 10.1002/for.3104); VISUELLE through the GTM-Transformer repository ("publicly available to download here", a Google Form). As published (Sec. 3): "the sales between October 2016 and December 2019 of 5577 products in 100 shops of Nunalie, an Italian fast-fashion company"; per product an RGB image, a category (27 values), a colour (10; "extracted from the images with a proprietary pixel clustering algorithm" and validated by two operators), a fabric (58; "from the technical sheets"), season and release date, a weekly sales series of 12 observations, and three Google Trends series (52 weeks before release). VISUELLE 2.0 (CVPRW 2022, the supplemental link) adds prices, discounts and per-shop sales (the run's note, not read).
- Use case: Sec. 5.2, "an experimental protocol that simulates how a fast fashion company deals with new products": the first order, "when the company orders the first stock of products ... usually two months before the starting season", and the release setup; horizon 6 weeks, "the period where no interventions are made by the company"; fit direct for the first-order quantity of a product with no sales history. Regime temporal: the paper tests on "the 497 most recent products".
- Siblings and duplicates: `dresses_sales` (Lennart, `TBD -> 2nd Tier`, `Missing source information`, `Outdated`): another source, not a duplicate (PROV-4); `hm_article_buyer_age`, `khaadi_clothes_price` and `flipkart_fashion_discount` are other fashion tasks; no other VISUELLE record (`grep -il "visuelle\|nunalie"`). External collections: none of our vocabulary.
- Better data: found as better data for `dresses_sales`; no further search this round.
- Papers and pages: the arXiv paper (Sec. 3, Sec. 5.2 and Table 1 read); the GTM-Transformer README (download form; MIT licence for the code, none stated for the data); the VISUELLE 2.0 supplemental not read.
- Metric: WAPE, "the primary error measure" (Sec. 5.2), with MAE, tracking signal and ERP reported beside it: a deliberate primary choice (MET-5) on the 6-week curve; for one summed target WAPE is the fold's MAE over its mean sales, so `mae` or a WAPE scorer, to decide. Inputs: none.
- Risks for /add-dataset: the target is a 12-week series (SEL-10 against SEL-11): ship one pre-launch number (such as the first 6 weeks' sales) with no lagged sales (TP-10); the tabular inputs are category, colour, fabric and release date only, and the colour is image-derived (SEL-13 to weigh); in Table 1 the attribute kNN [T] (WAPE 59.8) beats the image kNN [I] (62.2), so the image does not clearly dominate (SEL-12); the Google Trends are 3 x 52 weekly values per product, known before release (flatten or drop); sales may be normalised (not checked); a form for access, no data licence stated (EV-4: no criterion).
- Priority: gap 0 (business, regression, temporal not thin), use case + (the paper's protocol names a fast-fashion company's first order), source + (a paper with a named company), shape 0 (5,577 products but four tabular inputs), risk - (a series target to collapse, image-led source models).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `dresses_sales`.
- as published: 5,577 new products sold in about 100 stores, 2016-2019; per product an image, category, colour, fabric, release date and 12 weeks of sales (plus Google Trends series); VISUELLE 2.0 (CVPRW 2022): ...; target: sales of a new product over its first 12 weeks (a total, or a sold-well flag like dresses' Recommendation); access: registration.
- Why: dresses_sales predicts whether a dress sells from design attributes (style, season, material, pattern, price); VISUELLE measures the same quantity directly (unit sales) for new products from the same kind of design attributes known before launch
- Adds: 11x the rows, a named company and a paper (dresses_sales has no source information), real sales instead of an unexplained 0/1 flag, release dates for a temporal split. Caveats: the authors frame it as forecasting the 12-week curve with Google Trends, so the record must fix a single pre-launch target with no lagged ...

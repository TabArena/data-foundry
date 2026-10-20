---
unique_name: criteo_sponsored_search_conversion_log
name: Criteo Sponsored Search Conversion Log / Criteo-SSC (Criteo AI Lab)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Company
year: '2018'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://ailab.criteo.com/criteo-sponsored-search-conversion-log-dataset/
- http://go.criteo.net/criteo-research-search-conversion.tar.gz
- https://arxiv.org/abs/1806.08211
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

Criteo AI Lab's sample of 90 days of Criteo Predictive Search traffic: one row per click on a product ad, with `Sale`,
`SalesAmountInEuro`, `time_delay_for_conversion`, the click timestamp, product price, age group, gender, brand, seven
undisclosed categories, country, product, partner and user ids, a hashed title, device and an undisclosed audience id.
OptDist (Weng et al. 2024, Table 1, p. 7) counts 15,995,633 clicks with 1,150,996 conversions (7.20%), so 92.8% zero
revenue, and splits them randomly 7:1:2 (Sec. 4.1.1, p. 6). Not measured: the download link redirects to an Azure
storage account that no longer resolves (2026-10-20), and no mirror turned up on Hugging Face or Kaggle.

No: the source task is post-click conversion prediction for ad bidding, the CTR family that criterion 3 excludes.
Tallis & Yadav (2018), Sec. 1, p. 1: "an effective advertisement bidding strategy requires determining the probability
that an advertisement click will originate a conversion"; Sec. 4.3, p. 4: "we label each event with the event
outcome. That is whether that event originated in a conversion or not". The revenue target OptDist uses is the value
side of the same per-click bid, and most features are ids and hashes (user, product, partner, title), as in `albert`
(Criteo display clicks, No). Kept anyway, it would need a temporal split by click time, not OptDist's random one.
Licence: CC BY-NC-SA 4.0 (dataset page).

## Reference

Tallis M., Yadav P. (2018). Reacting to Variations in Product Demand: An Application for Conversion Rate (CR)
Prediction in Sponsored Search. arXiv:1806.08211.

Weng Y., Tang X., Xu Z., Lyu F., Liu D., Sun Z., He X. (2024). OptDist: Learning Optimal Distribution for Customer Lifetime Value Prediction. CIKM '24.
arXiv:2408.08585.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).

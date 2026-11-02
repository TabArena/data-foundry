---
unique_name: indabax_guinea_2022
name: indabax-guinea-2022/
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/indabax-guinea-2022/data
- https://zindi.africa/competitions/ai-bootcamp-2021/data
source_row: 992
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4, PROV-5): the Sapa "customer response" data of the DSN 2021 AI Bootcamp hackathon, which is the Kaggle `marketing_campaign` table (2,240 customers) with renamed columns; `marketing_campaign` ships as `Yes`.
- Source: Zindi, IndabaX Guinea 2022 Hackathon (2022-08-19, 4 hours, private); the Zindi API gives `ai-bootcamp-2021` (Data Science Nigeria 2021 AI Bootcamp Qualification Hackathon, 773 participants) as its parent, with the same files (Train.csv 160,318 B, Test.csv 67,526 B, SampleSubmission.csv 8,748 B). The "sapa.com" company and its CEO "Mr Echoke" are the hackathon's fictional framing. As published: "split into train and test with a volume of 1568 and 672"; 26 variables from `Year_of_Birth` to `User_Response`.
- Use case: respond / not respond to a marketing campaign; regime IID.
- Siblings and duplicates: the variables map one to one onto `marketing_campaign` (Kaggle rodsaldanha/arketing-campaign, Parr-Rud 2014; `Yes`, v2 folder `datasets/_dev/tabarena-v0pt2/marketing_campaign/`, 2,240 rows): Year_Birth, Education, Marital_Status, Income, Kidhome, Teenhome, Dt_Customer, Recency, NumDealsPurchases, NumWeb/Catalog/StorePurchases, Mnt* (wines, fruits, meat, fish, sweets, gold), NumWebVisitsMonth, AcceptedCmp1-5, Complain, Response; 1,568 + 672 = 2,240. The same table is under `customer_personality_analysis` and `customer_personality_analysis_2`. Precedent: `indabax_drc_2022` and `indabax_eswatini_2022` (Lennart, 2026-10-12, `Duplicate` on the parent competition and identical file sizes).
- Papers and pages: the two Zindi pages (via the API).
- Metric: F1 (Zindi Evaluation page).
- Reject check (AI, 2026-10-22): stands. Zindi API: parent 'ai-bootcamp-2021', and the files are byte-identical (Train.csv 160,318, Test.csv 67,526, SampleSubmission.csv 8,748). The data page's 1,568 + 672 = 2,240 rows and a one-to-one column mapping point to the shipped `marketing_campaign` (Yes). The Zindi re-run alone already makes it a PROV-4 duplicate (precedent indabax_drc_2022, Lennart 2026-10-12). https://zindi.africa/competitions/indabax-guinea-2022

IndabaX Guinea 2022 provides a structured dataset (described as pulled from a CRM-style database) to predict customer response to marketing campaigns, a marketing-response binary classification on tabular features. This is a legitimate real-world predictive tabular task aligned with the IID criterion. Plausible Yes, though the record has no size/feature specifics and 'sapa.com database' provenance is vague. A human must verify final table size, the response target, feature provenance, and uniqueness.

---

a structured dataset pulled from the sapa.com database with a few important features that can be used to predict customer response to marketing campaigns

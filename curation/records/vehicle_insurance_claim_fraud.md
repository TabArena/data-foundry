---
unique_name: vehicle_insurance_claim_fraud
name: Vehicle insurance claim fraud (fraud_oracle.csv)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
domain: insurance
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/shivamb/vehicle-claim-fraud-detection
- https://doi.org/10.1145/1007730.1007738
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the classic automobile-claims sample (15,420 claims of 1994-1996, 33 columns, `FraudFound_P`) used by Phua et al. 2004 for claim-fraud detection, a task insurers still do, in a thin domain; the trail from the Kaggle upload ends at a software vendor's sample of an unnamed insurer, and the paper that describes it is closed access.
- Source: Kaggle `shivamb/vehicle-claim-fraud-detection` (2021-12-20, CC0, `fraud_oracle.csv`, 3.6 MB; its metadata names "Oracle Databases" as the source) re-uploads the sample known in the literature as `carclaims.txt`, which later papers describe as claims of an anonymous insurer provided with the Angoss KnowledgeSeeker software (search snippets, not read). First paper found: Phua, Alahakoon and Lee 2004, "Minority report in fraud detection: classification of skewed data", SIGKDD Explorations 6(1):50-59 (closed; abstract: "a publicly available automobile insurance fraud detection data set"). A course report (C. Bright, Waterloo, 2013, read): "data from 6142 automobile owners in 1994 was used to identify the fradulent "risk" of 9278 automobile owners in 1995 and 1996", with "33 variables, which included Policy number and Year (not used for prediction purposes) as well as Fraud found". As published: 15,420 claims x 33 columns: accident and claim month, week and weekday, make, area, sex, marital status, age, fault, policy type, vehicle category, binned vehicle price, deductible, driver rating, binned days from policy start to accident and to claim, past claims, binned vehicle and holder age, police report, witness, agent type, supplements, address change, number of cars, year, base policy, `PolicyNumber`, `RepNumber`; target `FraudFound_P`.
- Use case: an insurer's claims unit, when a claim is filed, decides whether to refer it for a fraud investigation; Phua et al. compare methods "in terms of cost savings" (abstract), which implies that decision. Fit direct if the paper's text confirms it. Regime temporal by `Year` (1994 against 1995-1996 in the course report; the paper's split not read).
- Siblings and duplicates: no other record of this sample (searched by `fraud_oracle`, `carclaims`, Angoss, Phua and vehicle claim; `fraud_detection`, `is_fraud` and `fraud_detection_update` are other data, checked on OpenML); `autoinland_vehicle_insurance_claim_challenge`, `axa_vehicle_insurance_claim_challenge` and `monthly_insurance_claim_prediction_challenge` predict claim occurrence, not fraud. External collections: none found (no OpenML copy by name).
- Better data: found by the gap scout for insurance; no further search this round.
- Papers and pages: Phua et al. 2004 (stacking-bagging against bagged C4.5); the Waterloo course report; the file is widely reused in later fraud papers (not read). The Kaggle discussions and notebooks were not read (PROV-18).
- Metric: Phua et al. 2004 rank by cost savings under their cost model (abstract); its costs could not be read (closed access, PROV-17). If the paper fixes a cost per investigation and per missed fraud, `cost_matrix` (MET-7); otherwise the fallback `roc_auc` (MET-8). Inputs none beyond the label.
- Risks for /add-dataset: provenance: the trail ends at a vendor's sample of an unnamed insurer; ask the curator for the paper's PDF (PROV-2, PROV-17) and read the Kaggle threads (PROV-18); `FraudFound_P` is known only where a claim was investigated, so unreferred frauds sit among the negatives; `PolicyNumber` is a row id (check its order against the label and the year, LEAK-16) and `RepNumber` the claims representative (check when it is assigned); `Age` next to the binned `AgeOfPolicyHolder` (check zeros and agreement, CLEAN); most numbers ship as bins (ordinal categories); the data is 30 years old (`Outdated` is the curator's call).
- Priority: gap + (insurance has 3 accepted), use case + (the paper's cost savings of an investigation decision, from the abstract), source 0 (the first publisher, Angoss, documents nothing found and the paper is closed), shape + (15,420 claims, 30 mixed features, three years), risk - (provenance gap; labels only from investigated claims).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for insurance.
- as published: about 15,420 claims x 33 columns (fraud_oracle.csv, 3.6 MB): accident and claim month, week and weekday, make, area, sex, marital status, age, fault, policy type, vehicle category and price, ...; target: FraudFound_P (the claim was found fraudulent); access: open.
- Why: insurance fraud is named in the area and absent from the benchmark; mixed categorical and numeric features with a year column (temporal split possible); the standard public auto-claim fraud set in the fraud-detection literature
- Adds: a claims-fraud classification task. Risks: provenance must be traced from the Kaggle upload to the Angoss sample and Phua et al. (PROV-1, PROV-8) before it counts as a known source; the old age of the data (Outdated?); PolicyNumber and RepNumber ids

---
unique_name: allstate_claim_prediction_challenge
name: Allstate Claim Prediction Challenge (Kaggle 2011, ClaimPredictionChallenge)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Kaggle
year: '2011'
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/ClaimPredictionChallenge
- https://digital.wpi.edu/downloads/zs25x859f
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

Allstate's Kaggle competition: one row per insured vehicle and calendar year, 13,184,290 rows for 2005-2007 with
`Household_ID`, `Vehicle`, model year, blinded make, model and submodel and anonymised vehicle and policy variables;
the 2008 and 2009 test rows were never labelled publicly. The target, bodily-injury liability payments, "has been
adjusted to control for known non-vehicle effects" (data page), so it "isn't actually in units of any major currency"
(Allstate, thread 928). Not `allstate_claims_severity` (2016, positive losses only). Measured on the downloaded
`train_set` (2026-10-20): 99.27% exact zeros, 95,605 positives, no negatives, matching Huangfu (2015, Sec. 2.0, p. 6:
"only 95,605 non-zero values (about 0.73%) among the 13,184,290 records"); 4,309,042 households, 71% of the 2007
households already present in 2005-2006.

Split temporal by `Calendar_Year`, as the competition did (trained on 2005-2007, scored on 2008 and 2009). Drop
`Row_ID`; `Household_ID` is a group id (a household's own claim history is fair under the temporal split). Missing
values (37-54% of `Cat2`, `Cat4`, `Cat5`, `Cat7`) occur only in the training file, and Allstate asked that models not
use missingness (thread 826). Untuned LightGBM, 3M sampled rows of 2005-2006 -> 2007: AUC 0.59 for a claim, normalized
Gini 0.093, R^2 -0.03 on log1p among positives; Huangfu's best model reached 0.080 on 2007 (Sec. 5.0 d, p. 30), the
Kaggle winner 0.20 on 2009. A small real signal behind an undisclosed adjustment, at a size that needs subsampling (a
1M-row cut holds about 7,300 positives): 2nd tier. Terms: Kaggle competition rules (a 2022 licence question in the
forum is unanswered). To check: whether a target adjusted for non-vehicle effects and a vehicle-only feature set count
as a representative pricing task.

## Reference

Kaggle (2011). Allstate Claim Prediction Challenge. https://www.kaggle.com/competitions/ClaimPredictionChallenge

Huangfu D. (2015). Data Mining for Car Insurance Claims Prediction. MSc project report, Worcester Polytechnic
Institute. https://digital.wpi.edu/downloads/zs25x859f

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).

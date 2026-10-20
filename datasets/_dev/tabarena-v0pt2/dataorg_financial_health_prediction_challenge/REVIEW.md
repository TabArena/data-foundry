# dataorg_financial_health_prediction_challenge

**Outcome:** added. Zindi's FinScope MSME survey file as an IID three-class task on the business's Financial Health
Index (Low, Medium, High), scored with log loss, without Lesotho's 1,944 rows. The AI recommends shipping it; dropping
Lesotho and keeping the product columns are the curator's calls (issues 1 and 2).

**Main points:** Lesotho dropped: its label runs against the index. The label is the 11 product columns plus a residual.

**Record fields that disagree with the definition:**

- `domain`: record `business & marketing`, definition `finance`.

**Record judgment:** valid with concerns: Lesotho's label runs against the index (issue 1), and the label is a rule on
the product columns plus a residual (issue 2).

**Issues for Lennart:**

1. **Lesotho's label runs against the index. Implemented: drop the 1,944 Lesotho rows.**
   - The comparison is among Lesotho businesses asked the same question: share of Medium or High with the answer vs
     without it.

     | Answer | Lesotho, with vs without |
     |---|---|
     | Loan account | 0.17 vs 0.21 |
     | Debit card | 0.12 vs 0.34 |
     | Internet banking | 0.17 vs 0.21 |
     | Motor insurance | 0.19 vs 0.40 |
     | Income-tax compliance | 0.25 vs 0.40 |

   - In Eswatini, Malawi and Zimbabwe each of these answers goes with a higher class.
   - In Lesotho the class also falls with income (Spearman −0.12, −0.11 and −0.11 for income, expenses and turnover;
     +0.14 to +0.24 elsewhere).
   - Models trained on any two of the other countries score the third at AUC 0.63-0.68 and Lesotho at 0.46.
   - The FinScope Lesotho report says "formal MSMEs exhibit greater financial health" (p. 53), the opposite of what the
     released labels show.
   - The label is learnable within Lesotho (log loss 0.520 against 0.671 for the class shares). So it was built
     differently, not at random.
   - **Alternative A:** keep Lesotho as released. That needs an `Anomaly:` bullet saying the label looks inverted
     against formal finance and income. It also needs the Lesotho sentinel fixes from the first round restored: amounts
     of 97 and owner age 99 → missing. With Lesotho, LightGBM log loss is 0.317; without it, 0.260.
   - **Alternative B:** remap the labels. Not possible: I found no exact inversion.
     - Swapping Low and Medium leaves Lesotho at AUC 0.54 for a model trained on the other three countries.
     - Reversing the order would make 60% of Lesotho's businesses High.
   - The "Never had" ↔ "Used to have" swap I flagged in round 1 is harmless. The verifier's LightGBM log loss is 0.3167
     either way; mine is 0.3177 vs 0.3176.
   - data.org or FinMark Trust could say how Lesotho's FHI was computed.

2. **The product columns are inputs of the index. Implemented: keep them.**
   - Results on the shipped splits after the drop:

     | Model | Log loss | Accuracy | vs LightGBM on all columns |
     |---|---|---|---|
     | Depth-3 tree, country + 11 product columns | 0.373 | 0.888 | worse on 9 of 9 splits |
     | Depth-5 tree, same columns | 0.301 | 0.910 | worse on 9 of 9 splits |
     | Depth-6 tree, same columns | 0.285 | 0.916 | worse on 9 of 9 splits |
     | LightGBM, all columns | 0.260 | 0.917 | — |
     | LightGBM, country + 11 product columns | 0.255 | — | better on 7 of 9 splits |
     | LightGBM, the 26 other columns | 0.695 (macro AUC 0.752) | — | — |
     | Class shares | 0.796 | — | — |

   - Within identical (country + 11 product) profiles, the majority class covers 0.938 of the rows. It was 0.899 with
     Lesotho.
   - The label is therefore a rule on the products plus a residual, not a deterministic function. It is not Trivial
     under rule 4: the depth-6 tree is worse on 9 of 9 splits.
   - **Alternative:** drop the 11 product columns (0.695 against 0.796 for the class shares), or answer No.

4. **Year.**
   - `year = "2025"`, the competition and release year. The surveys are from 2019-2023.
   - This is the open year-convention question.

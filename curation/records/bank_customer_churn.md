---
unique_name: bank_customer_churn
name: Bank_Customer_Churn_Dataset / bank_customer_churn
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: No (Retired)
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Missing source information
original_source: Kaggle
year: '2022'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/gauravtopre/bank-customer-churn-dataset
notebook_path: datasets/beyond_iid/old_iid/bank_customer_churn/bank_customer_churn.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Source for the Kaggle dataset likely from a data science course from (https://www.superdatascience.com/deep-learning), and the data/code is from here https://drive.google.com/drive/folders/1hGpnrfAVzcuHpNVQeHz46c_4tWmu1Y23

However, this does not seem to be the original dataset either.
Given the heavy usage of this data from this course, we keep the data source as is.

Looks like a recent and good dataset for churn applications over an international company with time invariant fetatures

Duplicate with shrutime (which however is older and has fake names?)

Potential issue: -

Lennart: No objection

Andrej: Licence & data source unclear

CC (2026-10-14, Lennart): No licence is known (Kaggle: 'Other (specified in description)', and the description names none), so the definition's licence is None.

CC (2026-10-21, Lennart): option (a) of the consistency check on one-snapshot churn sets: tagged `ForcedIIDFromTemporal`; SPLIT-8 now covers a release with one stock month or one undated snapshot.

**Assessment (AI, 2026-10-21):** tag and one note line added; a dated window would test the model on a later period's customers; not measurable on one undated snapshot.

CC (2026-10-21, Lennart): an upload whose first platform cannot be traced is kept for now, case by case, when the data looks sound and there is a source to point to ("if the data looks good enough even without a good source but there is a source, we want to keep it for now and risk it"); PROV-1/PROV-2 amended, the gap written as an approximate fit with a note.

**Assessment (AI, 2026-10-21):** listed as a case of the amended PROV-2; no change to the definition.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Kaggle dataset (likely a course dataset) with no stated task metric; no first publication.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Retire as generated: seven of ten columns carry next to nothing beyond the class (within-class shuffle AUC 0.48-0.53 against 0.54-0.76 on the real bank_marketing), tenure is flat over age, and a hand-written class-first Bayes net beats all 41 benchmark methods. Priority 1: gap 0, use case 0, source 0, shape 1, risk -1.

CC (2026-11-04, Andrej): retired as generated data (`No (Retired)`, `AHDS`, `Missing source information`). The table comes from a data-science course (SuperDataScience, Deep Learning A-Z) and names no bank, period or generation method.
- **How it was generated:** a class-rooted Bayes net (a sampler that draws the label first, then each column given the label and at most two other columns), written down by hand: churn first; country, gender, activity and number of products given churn; a zero balance given churn, country and products; a positive balance around one shared centre (about 120,000), its spread given churn and country; age given churn and activity; credit score given churn (capped at 850); tenure, salary and the card flag independent noise.
- **The generator beats every method:** used as a classifier on the 9 shipped splits it scores 1 - ROC AUC 0.1213, ahead of all 40 benchmark methods (best 0.1233, TabPFN-3.5 0.1240), so the task ranks methods by how well they recover a sampler's densities, not how customers leave.
- **Checks calibrated on a real bank table agree:** seven of the ten columns cannot be told from a copy shuffled within each class (ROC AUC 0.48-0.53; every client column of bank_marketing 0.54-0.76), tenure does not rise with age, salary is uniform from 12 to 200,000.
- **Why the keep of 2026-10-21 no longer holds:** it rested on a named course counting as a source when the data shows no marks of generation; the data shows them, as for credit_card_customers.

## Review

**Outcome:** added; retired as generated data on 2026-11-04 (`No (Retired)`, `AHDS`, issue 1). The "Churn_Modelling"
table of the SuperDataScience course Deep Learning A-Z, re-uploaded on Kaggle (2022): 10,000 customers of an unnamed
bank in France, Germany and Spain, 20.4% left, one undated snapshot, random split forced from temporal. Reviewed on
2026-11-04 without a panel, from the gathered evidence (the record, model runs on the shipped data and on the
TabArena v0.1 task of the same table) and two checks. Validity: the table's generator was written down, a
class-rooted Bayes net (churn drawn first, every other column drawn given churn and at most two other columns, tenure,
salary and the card flag pure noise), and that hand-written net beats all 40 benchmark methods. Two checks calibrated on
the real bank_marketing table agree: seven of the ten columns carry next to nothing about the rest of the row beyond
the label (a model cannot tell real rows from rows with one of them shuffled within each class, ROC AUC 0.48 to 0.53,
where every client column of bank_marketing is detected, 0.54 to 0.76); tenure does not rise with age, salary is
uniform and tied to nothing, and positive balances centre on the same 120,000 in every country and class. The source
names no bank and no generation method. Value: the methods separate (1-AUC 0.123 for the best, 0.130 for boosted
trees, 0.228 for logistic regression), but they separate on how well they recover the sampler's densities. Quality: no
issue beyond the origin. Weighed: a widely used teaching table with real-looking marginals +, the generator written
down and beating every method -, marks of generation in three calibrated tests -, no traceable bank -.

**Main points:** Retire as generated data (issue 1)? Retired.

**Record judgment:** not valid as real data: a course table drawn by a class-rooted Bayes net, which, written down,
beats every method; the earlier keep rested on a course counting as a source while the data
showed no such marks.

**Issues for Andrej:**

1. **Retire as generated data?**

   * **Problem:**
     - The table was drawn class first: churn is drawn, then each column given churn and at most two other columns, with tenure, salary and the card flag as pure noise, and this class-rooted Bayes net, written down by hand, beats all 40 benchmark methods (1-AUC 0.1213 against 0.1233 for the best).
     - Tests calibrated on the real bank_marketing table find the same: seven of the ten columns carry nothing about the rest of the row beyond churn (ROC AUC 0.48 to 0.53 against a within-class shuffle, 0.54 to 0.76 for bank_marketing), tenure does not rise with age, and salary is uniform.
     - Retire the dataset as generated, or keep it?
   * **Background:** the file comes from the course's material and was re-uploaded on Kaggle (the original has
     surnames, which this copy drops); no bank, period or generation method is named. It was kept on 2026-10-21
     because a named course counts as a source when the data shows no marks of generated data[^d1-1a]. The automated
     generated-data probe did not flag it (11.1% of within-class column pairs dependent, 2 of 8 columns uniform,
     below its thresholds)[^d1-1b]. Writing the generator down settles the question[^d1-1c]; the tests below look at the
     columns one by one and are calibrated on a real bank table.
   * **Experiments:**
     - The generator, written down by hand: churn first; country, gender, activity and the number
       of products given churn; a zero balance given churn, country (Germany never zero, France and Spain one rate)
       and products; a positive balance normal around one shared centre, its spread given churn and country; age
       given churn and activity (churners one normal around 45, the others a two-part mixture weighted by activity);
       credit score given churn (a normal capped at 850); tenure, salary and the card flag drawn independently of
       everything. Scored as a classifier on the 9 shipped splits it reaches 1-AUC 0.1213 (SD 0.0018), ahead of all
       40 benchmark methods (best 0.1233, TabPFN-3.5 0.1240, logistic regression 0.228).
     - Shuffle test (one column permuted within each class, LightGBM telling real from shuffled rows, 3-fold CV
       with each row and its shuffled copy in one fold, 2 shuffles): credit score 0.488, gender 0.498, age 0.514,
       tenure 0.500, card 0.499, activity 0.526, salary 0.484; only country 0.618, balance 0.655 and products 0.613
       are tied to the rest. The same test on bank_marketing: age 0.687, job 0.756, education 0.720, marital status
       0.643, housing loan 0.626, balance 0.578, personal loan 0.543.
     - Correlations (check of 2026-11-04 on the shipped table, the v0.2 rows and columns): Spearman age-tenure -0.010
       (-0.002 and -0.026 within the classes), age-salary -0.002, balance-salary 0.012, credit score-salary 0.001; 1
       and 2 of the 15 pairs of numeric columns within each class pass p < 0.05, about what chance gives. Mean tenure
       is 5.2 years at ages 18 to 25 and 5.1 above 65, and 72 of the 142 customers aged 21 or less have held their
       account for 5 years or more. Salary passes a test for a uniform distribution (p 0.84), 59 salaries are below
       1,000. In bank_marketing age and balance correlate (Spearman 0.10; 0.09 and 0.14 within the classes).
     - Positive balances by country and class: means 119,400 to 121,900 in all six cells, standard deviations 30,000
       for the customers who stayed, 19,500 for German leavers and 38,400 and 41,500 for French and Spanish leavers.
   * **Effect on the task:** the benchmark would score methods on how well they recover the densities of a sampler,
     not on how a bank's customers leave; the hand-written sampler is the best model.
   * **Consistency:** follows credit_card_customers, another teaching table retired as generated on calibrated marks
     without a known generator (2026-10-26, Lennart)[^d1-1d]; here the generator is known as well. A `Duplicate` of this
     table (superdatascience_churn_modelling) and a self-declared synthetic upload under a similar name
     (bank_customer_churn_duplicate) were rejected before; neither is a precedent for this copy.
   * **Unknown:** the course's own words about where the table came from; the surnames of the original file (dropped
     here) could show whether names fit the countries.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep | 10,000 customers, random split, `ForcedIIDFromTemporal` | a widely used churn table; the methods separate | rows drawn by a written-down generator that beats every method |
     | B | Retire (implemented) | record `No (Retired)` with `AHDS` and `Missing source information`; the folder leaves the working copy | follows the rule on generated data and the credit_card_customers case | one churn task fewer |

   * **Recommendation:** B: the generator is written down and beats every model, and three calibrated tests find its
     marks, one of them tied to the label. **Decision:** retire (B), or keep (A)?

   **Notes for the AI:** done on 2026-11-04: record `suggestion: No (Retired)`, markers `AHDS (Artifical/Handmade/
   Deterministic/Simulated)` and `Missing source information`, CC and Assessment lines; a CC line on the earlier copy's
   record (superdatascience_churn_modelling); a PROV-3 case row and example in provenance.md; CHANGELOG entry. Left:
   remove the folder and clear `v2_path` once this file is committed, so it stays in git history (as for the other
   retirements of this branch).

   **Andrej (2026-11-04, discuss):** I generally would say the following: Yes, retire as generated and add a comment
   on how it was generated wherever this is appropriate. However, I find it weird how you stated the problem. We
   already uncovered the data generation as a class rooted bayes net, yet you still don't mention this in the problem
   bullets. Something like this should be a priority.

   **Resolved (2026-11-04, Andrej):** retired as generated data (B). The problem and the outcome now lead with the
   written-down generator, as PROV-3's detection asks (the decisive test first). How the table was generated is in the
   record's CC line, in a CC line on the earlier copy's record (superdatascience_churn_modelling) and in PROV-3 (a case
   row and an example of a written-down generator). The folder leaves the working copy once this file is committed.

   [^d1-1a]: **PROV-2** (Should): a source that is plausible but unclear in a detail stays, with a note; case row: a
     named first platform (a named data-science course) counts as a known source when the data shows no PROV-3 marks
     (2026-10-21, Lennart).
   [^d1-1b]: Generated-data probe calibration (task_probes.md, 2026-10-12): `uniform_within_class` lowest in the working
     copy santander (4.9%), biogeographical_ancestry_prediction (5.6%), bank_customer_churn (11.1%, 2 of 8).
   [^d1-1c]: provenance.md, "Is the data generated?": "When you can, write the generator down: that settles it", and
     report the decisive test first.
   [^d1-1d]: **PROV-3** (Must): the data is real, not generated and not a real table someone reworked; without a source
     statement or a generator, calibrated marks from at least two of the tests, or marks linked to the label, can be
     strong enough. **SEL-16** (Must): data that does not come from a real random distribution is out. Case:
     credit_card_customers, calibrated marks without a label link and an offline source, retired as `AHDS`
     (2026-10-26, Lennart).

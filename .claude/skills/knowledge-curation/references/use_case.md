# The use case and the prediction point

A dataset in the benchmark simulates a decision someone makes with a prediction. Write that decision down before
anything else: every column, filter, target and split choice is checked against it. In the 2026 leak audit the
written prediction point found columns no probe flagged (kickstarter's `staff_pick`, awarded mid-campaign, once the
task was "predict at launch").

## The use case

An actor, a moment and a decision: "a lender, when an application arrives, decides whether to approve it". Take it
from the source (the paper, the competition, the data card) when it states one; otherwise write the most plausible
one and say "for example". Then:

* what one row is, with its population, place and period;
* what is predicted, by when after the prediction point, in what classes or unit;
* what is known at the prediction point, and nothing recorded later;
* what the test data stands for (new customers, the next two weeks, configurations never measured, unseen patients).

A task no decision fits is out (criterion 3 in [selection.md](selection.md)): a label counted over one calendar
window shared by all rows, a label from clustering, a label the subject already knows when the features are
recorded, or data that serves only a study looking back.

## How closely the data mirrors it

* Direct: the rows, the features, the label's timing and the split mirror the use case (airfoil_self_noise,
  superconductivity, 2_month_survival_rate_prediction).
* Approximate: a stand-in with a known gap, named as such. One snapshot standing in for a forecast
  (account_debt_south_africa), a potential leak kept on purpose (kick), a reconstructed time axis or a label without a
  stated horizon (alfa_battle_2_0_task_2), one judge or rating service standing for the rating a buyer meets
  (coffee_rating_prediction; Lennart, 2026-10-14).
* None: no decision fits. The dataset goes back to triage as `No Good Target / Scientific Discovery`.

Before settling on approximate, ask whether the data as shipped mirrors another well-defined use case that
practitioners have, where the features are known and the label is not. If it does, that is the use case and the fit
is direct (5g_energy_consumption: a split by station within one week fills the gap for stations without
measurements, rather than standing in weakly for a forecast; Lennart, 2026-10-14). Do not rephrase a use case only
to excuse a gap: a credit model scores future applicants, so a random split of undated applications stays
approximate.

## The prediction point

When the model is used and what is known then: at launch (kickstarter), at admission (mic), at quote time
(homesite), at checkout (brazilian_ecommerce), before the stay ends, photometric classification (sdss_17), cold start
for a new respondent (in_vehicle_coupon_recommendation). A value that did not exist at that point is a leak
([leak_checks.md](leak_checks.md)), including a field that is blank because the outcome already happened and a
feature computed over a window that ends at the outcome.

When the features include measurements from a stage after the decision the task models (a biopsy after the clinical
examination, a lab result after triage), offer the task at the stage the source describes (eryhemato_squamous_disease:
the 12 clinical features, before the skin biopsy).

## The real-world target

Predict what the actor would act on, at the resolution they act on it. An agency rates the company and each of its
debt instruments separately; the decision a lender or an investor takes rests on the issuer rating (S&P issuer credit
rating, Moody's corporate family rating, Fitch issuer default rating), not on whichever instrument rating a file
happened to keep (corporate_credit_rating: 17% of the checkable labels were not the issuer rating; retired 2026-10-16
for a rebuild from the agencies' own histories). Check how the source built its label before accepting it.

A leak in the features is no reason to reject a task whose use case is real: fix the leak and keep the task. A target
the source defined badly can often be redefined into the real one (cirrhosis_patient_survival_prediction: time to
death over the patients who died became death or transplant within five years, over the patients followed that long).

## Inputs known at prediction time

Anything known at the prediction point is a legitimate input, including a number the company itself computed:

* A company's own estimate made before the outcome is an input, and the model refines it. brazilian_ecommerce keeps
  the delivery date Olist promised at checkout (it cannot leak, it is fixed before the delivery); dropping it would make
  the task "predict without the company's estimate" (R^2 0.366 with it, 0.332 without; 2026-10-15).
* A forecast the task corrects is the task's input. bias_correction_r_bias_correction_r_2 corrects the LDAPS weather
  model's forecast.

A row that lacks the input the prediction acts on is no task row. Drop it rather than keep it as missing:
bias_correction drops the three days without an LDAPS run, because nobody corrects a forecast that does not exist
(Lennart, 2026-10-15). Missing values of the other inputs stay missing.

## Recurring entities and the cold start

Decide from the use case whether the entity the model predicts for is new or known, before choosing the split
([splits.md](splits.md)).

* Most real predictions are for entities seen before: an agency reviews every rating at least once a year, a bank
  scores its existing customers. Then the entity's history is legitimate and the split is temporal; the previous
  outcome is a feature (corporate_credit_rating: 72% of the ratings with an earlier one repeat its class, and the
  previous rating lifts a random forest's skill from 0.285 to 0.460).
* A cold start predicts for an entity without history: a shadow rating of a new borrower, a recommender before it has
  data on a person (in_vehicle_coupon_recommendation). A grouped split tests that.
* When the use case is the first event of each entity, one row per entity makes it an IID task without grouping:
  breast_cancer_prediction keeps each woman's earliest exam, since screening assesses her at the first exam (Lennart,
  2026-10-15). One row per entity loses rows and signal, so take it only when the use case is that row
  (corporate_credit_rating: the latest rating per company scored 0.112 skill, all ratings grouped by company 0.158).

## In Data Foundry

The use case is written in a definition's `task_summary` with its `fit`, and the prediction point opens its
`curation_comments`: [definitions.md](../../knowledge-data-foundry/references/definitions.md).

# Deciding a split from the data collection type

This is the decision tree SPLIT-37 in [splits.md](splits.md) asks you to walk for every definition's split. Its root
is the record's data collection type (SPLIT-35); under each type the use case is asked first, then what the data and
its documentation allow, then a measurement where one decides. A leaf names the split and what justifies it: the time
basis of SPLIT-32, a forced tag of SPLIT-8, `ForcedIIDFromGrouped` of SPLIT-36, or for a temporal split the date the
windows are cut on and the gap.

## How to walk it

* Start at the record's collection type, and answer each question from what it says it reads. The kinds of question
  are marked: _use case_ (the source's stated application and the definition's use case), _data and documentation_
  (the raw rows, the source's account of how the data was collected), _measurement_ (a number you compute and write
  into the `Time basis:` line). A collection fact (`Samples:`, `Time:`, `Target:`, `Entities:`) appears only as
  "orientation": it points to where to look, it never answers a question by itself.
* Answer as if no split had been decided. The leaf you reach is the split to implement, with the tag in its title.
  `Random · ...` is an IID split, `Grouped · ...` a `grouping`, `Temporal · ...` a `temporal` declaration. A
  `ForcedIIDFromGrouped` leaf sits beside a time basis (SPLIT-36): the questions of the type's other branches give it.
* Ask a reviewer, with the split you suggest and the facts behind it, when:
  - you reach a forced leaf (`ForcedIIDFromTemporal`, `ForcedGroupedFromTemporal`, `ForcedIIDFromGrouped`): a forced
    split is a compromise the use case does not ask for;
  - you reach a leaf no v0.2 definition reaches yet: the reviewer decides the split and how the tree changes;
  - no answer fits a question: the tree needs a new branch, which only a reviewer adds.
* A use case the source states (a paper, a competition, a data card) answers the use-case questions (USE-1). A split
  the source prescribes is evidence, not an answer: it answers a question only where the source chose it for that use
  case. Where it matches the leaf, its official periods, gap and training history fill in the leaf (SPLIT-19); where
  it differs, the leaf decides, and the `splits_comment` says what the source prescribed and why it does not fit the
  use case (SPLIT-5), as a departure for a reviewer.
* `AssumedStationaryRelation` is only ever reached through a person's answer (SPLIT-32): offer it with the facts for
  and against and recommend it if you like, but answer "no" yourself unless a person has given the reason.
* Where a definition ships another split than its leaf, its `splits_comment` says which leaf the tree gives and why
  the definition departs; the departure goes to a reviewer like a forced leaf. The departures known when the tree was
  adopted are at the end.
* The examples under each leaf are v0.2 definitions that reach it; read one before writing yours.

## Shared answers

* **Catalogue block (①).** Under the expanding science catalogue, the question "Does the use case hold out a group: a
  family, a site or an instrument?" is reached three ways: from the items it was built from or from elsewhere, and
  from the next-items branch when there is no usable entry date or arrival changes nothing.
* **The gap.** Under every temporal leaf the gap follows SPLIT-10: late labels (a gap of about the delay, or training
  only on cases whose outcome is known before the window), a planning lead the use case states (a forecast issued
  ahead), an outcome window still open at the next scoring date, or claims still open when the next price is set. No
  gap where the delay is within the time step or a written exception holds.

## Expanding science catalogue

**Which items will the model meet?** _(use case; reads the source's stated aim and scope (abstract, methods, caveats;
its own split counts only where chosen for the use). In every leaf an item's copies stay on one side)_
- items like those it was built from, or from elsewhere (other sites or instruments) (the shared block (①)) →
  **(①) Does the use case hold out a group: a family, a site or an instrument?** _(use case; reads the use case and the
  source's scope: new members of a family (a scaffold, an element set, a protein target), or items from another site,
  survey or instrument → yes; more items of the kinds the data holds, with no group to hold out → no. Also reached from
  the next-items branch, through the link boxes: no usable entry date, or arrival changes nothing)_
  - no → **Random · `Timeless` (grouping not the objective)**. The use case holds out no group, only more items of the
    kinds the data holds: random, each item's copies together. A catalogue's family key is the usual split, so a case
    here goes to a reviewer. No v0.2 definition reaches it yet.
  - yes →
    **Can the data compute that group key?** _(data and documentation; reads a scaffold, an element set, a protein
    target, a well, a strain, a survey project or a site column, with several groups to hold out; not the label)_
    - yes → **Grouped · `UnseenGroup` (family, site or instrument)**. The entry date does not decide the split, and the
      use case holds out a family, site or instrument the data can key: whole groups held out, each item's copies with
      it; how the catalogue grew goes in the notes. Examples: drug_induced_autoimmunity_prediction,
      force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition, nci_aids_antiviral_screen.
    - no → **Random · `ForcedIIDFromGrouped` (no group key)**. The family, site or instrument the use case holds out
      cannot be computed apart from the label: random, the overlap it leaves named in the `Group basis:` line. No v0.2
      definition reaches it yet.
- the items the catalogue adds next, or no scope stated →
  **Does each item carry a final date of entry into this catalogue?** _(data and documentation; reads a date of entry
  into this catalogue in the release or a parent source, not a registration that predates it; items still to come, not
  an inventory already collected, a closed study or a designed experiment; labels final (orientation: the Time tag,
  Target: Revised Later))_
  - no → the shared block (①)
  - yes →
    **Does arrival change what is recorded or selected, or does the date carry waves?** _(measurement; reads a recording
    convention or an intake that moves with the entry date; or a forward split leaves clearly fewer close training
    neighbours than a random draw)_
    - yes: recording or selection moves → **Temporal · entry date (recording or selection moves)**. Items not held yet,
      a final entry date, and arrival changes how items are recorded or which are taken in: each era tested on the
      earlier ones; an item keys on its first date, which orders the split and is no input. Examples: ecoli_proteins.
    - yes: the date carries waves → **Temporal · entry date (the date carries waves)**. Items not held yet, a final
      entry date, and a forward split leaves clearly fewer close training neighbours than a random draw: each era tested
      on the earlier ones. Examples: apistox, qsar_tid_11.
    - no → the shared block (①)

## Experimental results

**Is there an order to how samples arrive in the use case?** _(use case; reads the use case: samples sent to a
certification body one after another, visitors at a screening point → yes; a property of an item, the outcome of a
designed run, with no sample before or after another → no)_
- yes →
  **Is the order available in the data?** _(data and documentation; reads the raw rows: a recorded date, or an order
  rebuilt from the data (a file position, an id) and checked against something dated (orientation: the Time tag))_
  - yes →
    **Is the relation measured flat along that order?** _(measurement; reads a measurement along the order in the `Time
    basis:` line: windows scoring like random folds of the same sizes)_
    - yes → **Random · `StationaryRelation`**. Later samples in an order the data holds, and the relation measured flat
      along it: random. Examples: infrared_thermography_temperature.
    - no or not measured → **Temporal · sample order**. Later samples in an order the data holds (a recorded date, or an
      order rebuilt from the data and checked against something dated), the relation not shown flat along it: each
      window tested on the earlier samples; a rebuilt order orders the split and is no input. Examples: wine_quality.
  - no →
    **Has a person given a domain or use-case reason to treat earlier and later samples as interchangeable?** _(use
    case; reads a person's call, written as `AssumedStationaryRelation (<person>, <date>): <reason>` (SPLIT-32);
    orientation only: what drives the label (adversaries, markets, the credit climate, a judge's call or outcomes that
    treatment changes count against; a diagnosis or a measured property may support it) and the collection span)_
    - yes → **Random · `AssumedStationaryRelation`**. Later samples, no date or order, and a person gave a reason from
      the domain or the use case to treat earlier and later samples as interchangeable, written in the definition's
      `Time basis:` line: random. No v0.2 definition reaches it yet.
    - no → **Random · `ForcedIIDFromTemporal`**. Later samples, no date or order, and no person has given a domain or
      use-case reason to treat earlier and later samples as interchangeable: random; the drift a later test would show
      stays untested. No v0.2 definition reaches it yet.
- no →
  **Was the experiment repeated, producing several rows for the same measurement?** _(data and documentation; reads the
  raw file and the source's design: replicates, test ages of one mix, frequency bands of one setup, conformations of one
  molecule, runs of one instance (orientation: Entities: Recur))_
  - yes →
    **Does the model meet new items, or further measurements of items it has measured?** _(use case; reads the use case:
    a new mix, setup, strain, instance or molecule → new items; another replicate of a known sample, as in a robustness
    or repeatability study → further measurements)_
    - new items → **Grouped · `Timeless` (the measurement)**. The experiment was repeated (replicates, test ages of one
      mix, frequency bands of one setup, conformations, runs of several solvers on one instance): whole measurements
      held out with all their rows, or a wider group where the use case holds one out. Examples: airfoil_self_noise,
      asp_potassco_classification, concrete_compressive_strength.
    - further measurements of measured items → **Random · `Timeless` (further measurements of measured items)**. The
      experiment was repeated, and the use case predicts further measurements of items already measured (a robustness or
      repeatability study): random, the other repeats of an item in training are the use case, not a leak. No v0.2
      definition reaches it yet.
  - no →
    **What does the model meet that the data does not hold?** _(use case; reads the use case: a new item of the kinds
    held, or a kind or family the data does not hold)_
    - a kind or family the data does not hold →
      **Can the data compute that kind?** _(data and documentation; reads a problem class, a target gene, a chemical
      series (a scaffold, SPLIT-31) computed from the data, with several kinds to hold out; not the label)_
      - yes → **Grouped · `UnseenGroup` (the kind)**. The model meets a kind the data does not hold (a problem class, a
        target gene): whole kinds held out. Examples: huesken_sirna_efficacy.
      - no → **Random · `ForcedIIDFromGrouped` (no kind key)**. The model meets a kind or family the data does not hold
        (a new chemical series), but the data cannot compute it (no structure): random, the overlap it leaves named in
        the `Group basis:` line. Examples: bioresponse.
    - a new item of the kinds held → **Random · `Timeless`**. One row per measurement, and the model meets a new item of
      the kinds held: random. Examples: biogeographical_ancestry_prediction, body_density_prediction,
      forensic_glass_identification.

## Clinical study

**Where will the model be used?** _(use case; reads the use case)_
- at another hospital or site →
  **Does the data hold several sites?** _(data and documentation; reads a hospital or site column)_
  - yes → **Grouped · `UnseenGroup` (sites)**. Another hospital, and the data holds several: whole sites held out.
    Examples: gossis_icu_hospital_mortality.
  - no → **Random · `ForcedIIDFromGrouped` (one site, the transfer untested)**. Another hospital is the use, but the
    data holds one: random; the step to another site stays untested, as the `Group basis:` line says. No v0.2 definition
    reaches it yet.
- at the same clinic, for later patients →
  **Is an arrival order available in the data?** _(data and documentation; reads the raw rows and the source: an order
  rebuilt from case numbers, encounter numbers or deposit batches and checked against something dated (a date the raw
  rows record would make the set a dated event log); or the order is lost; or all patients share one prediction point, a
  cohort scored at one baseline exam (orientation: Time: Inferred, Samples: One Moment))_
  - yes →
    **Are earlier and later patients interchangeable along that order?** _(measurement; reads a measurement along the
    order in the `Time basis:` line: the outcome and its relation to the features flat across periods, windows scoring
    like random folds (StationaryRelation, SPLIT-32))_
    - yes, measured flat → **Random · `StationaryRelation`**. Earlier and later patients measured interchangeable along
      the arrival order the data holds (case numbers): random, a patient's rows together. Examples:
      horse_colic_survival.
    - no, or not measured →
      **Does the order give enough periods for three windows?** _(data and documentation; reads the span and density of
      the order (SPLIT-14); a forced definition's `Time basis:` line names too few periods)_
      - yes → **Temporal · rebuilt order**. The data holds the arrival order (encounter numbers), not measured flat,
        with enough periods: each window tested on the earlier patients. Examples: diabetes_130_us.
      - no → **Random · `ForcedIIDFromTemporal` (too few periods)**. The data holds the arrival order (deposit batches),
        not measured flat, but with too few periods for three windows: random, a patient's rows together. Examples:
        lung_cancer_epithelial_genexp.
  - no, the order is lost →
    **Is there sufficient evidence to treat future patients as interchangeable with the study's patients?** _(use case;
    reads a person's domain or use-case reason in the `Time basis:` line (AssumedStationaryRelation, set only by a
    person, SPLIT-32): a mechanism the time between collection and use does not change, read by a fixed reference test)_
    - yes → **Random · `AssumedStationaryRelation`**. The arrival order is lost, and a person gave a domain or use-case
      reason to treat later patients as interchangeable with the study's: random, a patient's rows together. No v0.2
      definition reaches it yet.
    - no → **Random · `ForcedIIDFromTemporal`**. Patients arrived one by one, the order is lost, and no person gave a
      reason to treat later patients as interchangeable: random, a patient's rows together; the drift stays untested.
      Examples: breast_cancer_prediction, diabetes_3, differentiated_thyroid_cancer_recurrence.
  - no, all patients share one prediction point → **Random · `ForcedIIDFromTemporal` (one scored cohort)**. The whole
    cohort shares one prediction point (a baseline exam), and the target arrives after it: one date is one period, too
    few for three windows, so random patients of that point; a cohort scored at a later point stays untested. Examples:
    framingham_heart_study_fhs.

## Survey

**Whom, and when, does the model predict for?** _(use case; reads the use case)_
- the surveyed population at a later round →
  **How are the rounds known?** _(data and documentation; reads a round, wave or date column in the raw rows (an
  election year, an observation date), rounds rebuilt from the data and checked, or neither (orientation: the Time
  tag))_
  - recorded → **Temporal · round**. The next round is the use, and the rounds are recorded: each round tested on the
    earlier ones. Examples: anes_voting_2026, sdss_17.
  - rebuilt from the data → **Temporal · rebuilt round**. The next round is the use; the rounds are rebuilt from the
    data, not recorded: each rebuilt round tested on the earlier ones. Examples:
    ai4d_lab_tanzania_tourism_classification_challenge.
  - neither → **Random · `ForcedIIDFromTemporal` (no rounds)**. The next round is the use, but no round can be told
    apart: random; the step to the next round stays untested. No v0.2 definition reaches it yet.
- people or places the survey did not sample, at the rounds held →
  **Inside the population and area the survey covered, or outside them?** _(use case; reads the use case: gaps between
  sampled sites, respondents like these → inside; groups or places the survey never reached → outside)_
  - inside →
    **Did the survey sample in clusters, or ask each respondent several items?** _(data and documentation; reads the
    source's sampling design and a cluster or respondent id in the raw file: plots in a burn area, a respondent's
    several scenarios (orientation: Entities: Recur))_
    - yes → **Grouped · `Retrospective` (sampling cluster)**. People or places the survey did not sample, inside what it
      covered, where it sampled in clusters (sites, burn areas) or a respondent answered several items: whole clusters
      or respondents held out. Examples: boreal_postfire_lichen_biomass, in_vehicle_coupon_recommendation.
    - no → **Random · `Retrospective`**. People the survey did not sample, inside what it covered, one row each and no
      clusters: random, a fair draw of the same design. Examples: caracas_cervical_cancer.
  - outside →
    **Does the data hold several of those groups or places?** _(data and documentation; reads a facility, region or site
    column)_
    - yes → **Grouped · `UnseenGroup` (groups)**. Groups or places outside what the survey covered, and the data holds
      several: whole groups held out. Examples: early_learning_predictors.
    - no → **Random · `ForcedIIDFromGrouped` (one group, the transfer untested)**. Groups outside what the survey
      covered, but the data holds one: random; the transfer stays untested, as the `Group basis:` line says. No v0.2
      definition reaches it yet.

## Database snapshot

**What does a model trained on data from the snapshot meet in production?** _(use case; reads the use case)_
- rows of this same snapshot that lack the label →
  **Are those rows scattered among labelled ones, or whole areas or groups with none?** _(use case; reads the use case:
  a listing among listings, a module not yet inspected → scattered; unmapped land, a producer new to the shop → whole
  areas or groups)_
  - scattered →
    **Does a unit have several rows?** _(data and documentation; reads a unit id that repeats in the snapshot: a stone,
    a car (orientation: Entities: Recur))_
    - yes → **Grouped · `Retrospective` (the unit)**. Rows of this snapshot that lack the label, scattered among
      labelled ones, and a unit (a stone, a car) has several rows: whole units held out. Examples: diamonds, fiat_500,
      immoscout_german_house_prices.
    - no → **Random · `Retrospective`**. Rows of this snapshot that lack the label, scattered among labelled ones, one
      row per unit: random is the use. Examples: houses, jm1, otto_group_product_classification_challenge.
  - whole areas or groups →
    **Does the snapshot hold a key for them?** _(data and documentation; reads a group column (a producer) or a location
    fine enough to cut blocks)_
    - yes → **Grouped · `Retrospective` (area or group)**. Whole areas or groups of the snapshot lack the label (a
      producer new to the shop), and the snapshot holds their key: whole areas or groups held out. Examples:
      wine_world_cost.
    - no → **Random · `ForcedIIDFromGrouped` (no area key)**. Whole areas lack the label (unmapped land), but the
      snapshot holds no key fine enough to hold them out: random beside the Retrospective time basis, the share of test
      rows whose neighbours sit in training named in the `Group basis:` line. Examples: covertype.
- a whole population scored at a date, for what happens after it →
  **Can different snapshots be reconstructed from the data to create at least three train and test windows?** _(data and
  documentation; reads the source's reference dates: a second labelled file of the same population, scoring dates kept
  per row; four or more snapshots with their outcomes give three test windows and one to train on; one reference date,
  two or three, or several mixed with their dates lost do not)_
  - yes → **Temporal · scoring date**. A whole population scored at a date, and four or more snapshots with their
    outcomes can be reconstructed: three test windows, each trained on the earlier snapshots. No v0.2 definition reaches
    it yet.
  - no →
    **Does a model trained on an earlier snapshot score a later one as well as random folds?** _(measurement; reads a
    measurement across the snapshots held, in the `Time basis:` line (StationaryRelation, SPLIT-32): trained on one,
    tested on the next, against random folds of the same sizes; not possible with one snapshot or with dates lost)_
    - yes, measured → **Random · `StationaryRelation` (measured across the snapshots)**. Too few snapshots for three
      test windows, but trained on an earlier snapshot the model scores a later one as well as random folds do: random,
      a unit's rows together, the measurement in the `Time basis:` line; a later snapshot stays untested. Examples:
      distribution_transformers_at_cauca_department.
    - no, or not measurable → **Random · `ForcedIIDFromTemporal` (too few snapshots)**. A whole population scored for
      what happens after a date, but too few snapshots for three test windows (one scoring date, two or three, or
      several with their dates lost) and no flat comparison across them: random, a unit's rows together; a later
      snapshot stays untested. Examples: account_debt_south_africa, allstate_claim_prediction_challenge_1m,
      blood_transfusion.
- units of a place or group the snapshot does not hold →
  **Does the snapshot hold several of them?** _(data and documentation; reads a municipality, branch, region or site
  column with several groups to hold out)_
  - yes → **Grouped · `UnseenGroup` (groups)**. The model meets units of a place or group the snapshot does not hold (a
    new municipality, branch or region), and the snapshot holds several: whole groups held out. No v0.2 definition
    reaches it yet.
  - no → **Random · `ForcedIIDFromGrouped` (one group, the transfer untested)**. Another place or group is the use, but
    the snapshot holds one: random; the transfer stays untested, as the `Group basis:` line says. No v0.2 definition
    reaches it yet.
- new cases that arrive one by one →
  **Can the arrival order be rebuilt from the data and checked against time?** _(measurement; reads an id issued in
  sequence or the export's row order, checked against something dated (orientation: Time: Inferred))_
  - yes → **Temporal · rebuilt order**. New cases arrive one by one; the raw rows hold no date, but an order rebuilt
    from an id or the file's row order tracks time: windows on it, the order no input when it comes with the target.
    Examples: fremtpl2, labour_inspection_compliance, loan_default_prediction_imperial_college.
  - no →
    **Is there sufficient evidence to treat future samples as interchangeable with snapshot samples?** _(use case; reads
    a person's call, written as `AssumedStationaryRelation (<person>, <date>): <reason>` (SPLIT-32); orientation only:
    what drives the label (adversaries, markets, the credit climate, a judge's call or outcomes that treatment changes
    count against; a diagnosis or a measured property may support it) and the collection span)_
    - yes → **Random · `AssumedStationaryRelation`**. New cases arrive one by one, no date or order, and a person gave a
      reason from the domain or the use case to treat earlier and later samples as interchangeable, written in the
      definition's `Time basis:` line: random, a unit's rows together. No v0.2 definition reaches it yet.
    - no → **Random · `ForcedIIDFromTemporal`**. New cases arrive one by one, no date or order, and no person has given
      a domain or use-case reason to treat earlier and later samples as interchangeable: random, a unit's rows together;
      the drift a later test would show stays untested. Examples: allstate_claims_severity, amazon_employee_access,
      aps_failure.

## Dated event log

**Will the model be used at a place or group the data does not hold?** _(use case; reads the use case: a new hospital, a
new region)_
- yes →
  **Does the data hold several of them?** _(data and documentation; reads a hospital, region or site column)_
  - yes → **Grouped · `UnseenGroup` (groups)**. The use is at a place or group the data does not hold, and the data
    holds several: whole groups held out, the dates not weighed. Examples: heart_disease.
  - no → **Random · `ForcedIIDFromGrouped` (one site, the transfer untested)**. Another place is the use, but the data
    holds one: random beside the time basis; the step to another place stays untested, as the `Group basis:` line says.
    No v0.2 definition reaches it yet.
- no →
  **Does the model fill in the period the data covers, or predict forward?** _(use case; reads the use case: the gaps of
  the covered period (a record not taken, a value not read) → fill in; an order, a trip, a loan, a booking, a tariff
  after the data → forward)_
  - fill in → **Random · `Retrospective`**. The use fills in the period the data covers: random, or by time unit where
    rows of one time share the target. No v0.2 definition reaches it yet.
  - forward →
    **Can the dates hold three windows above the test floor?** _(data and documentation; reads the span and density of
    the dates (SPLIT-14); a forced definition's `Time basis:` line names too few periods)_
    - no → **Random · `ForcedIIDFromTemporal` (too few periods)**. A forward use, the relation not shown flat, and too
      few periods for three windows (cases, scoring dates or pricing periods): random, a unit's rows together; a later
      period stays untested. Examples: 2_month_survival_rate_prediction, frempl_french_motor_personal_line,
      online_shoppers_purchasing_intention_dataset.
    - yes →
      **What sets off a prediction?** _(use case; reads the use case: a case that arrives (an order, a trip, a loan); a
      date at which the open cases are scored (bookings not yet arrived, accounts at a month-end); a price set for the
      next period (a tariff year))_
      - a case arrives →
        **Is the target known only after a delay longer than the time step, or does the use case predict ahead?** _(data
        and documentation; reads SPLIT-10: the source's account of when the target is known (a delivery, a chargeback, a
        recorded sale), checked on the newest window (fewer or selected labels); or a planning lead the use case states
        (a forecast made a day ahead); no gap where the delay is shorter than the time step or a written exception holds
        (orientation: the Target tag))_
        - yes, late labels → **Temporal · arrival date, label-delay gap**. Each case scored when it arrives, its target
          known only after a delay longer than the time step (a delivery, a chargeback, a recorded sale): windows on the
          arrival date, a gap of about the delay, or training only on cases whose outcome is known before the window
          (SPLIT-10). Examples: 2024_lusaka_mobility_prediction_hackathon, aeolus_rebuilt_1m,
          african_credit_scoring_challenge.
        - yes, a planning lead → **Temporal · arrival date, planning gap**. Each case scored some time before it happens
          (a forecast made a day ahead): windows on the arrival date, the planning lead as the gap. No v0.2 definition
          reaches it yet.
        - no → **Temporal · arrival date**. Each case scored when it arrives, its target known with it or within the
          time step, or no gap by a written SPLIT-10 exception: windows on the arrival date, no gap. Examples:
          acquire_valued_shoppers_challenge, alfa_battle_2_0_task_2, ames_housing.
      - a date at which open cases are scored →
        **Is the outcome window still open at the next scoring date?** _(data and documentation; reads the source's
        definition of the outcome window (a 20-day return, three months after the period, the arrival of a booking)
        against the spacing of the scoring dates)_
        - yes → **Temporal · scoring date, outcome window as gap**. The open cases are scored at a date (bookings not
          yet arrived, accounts at a month-end, the stocks of a week), and their outcome window is still open at the
          next scoring date: windows cut on the scoring date, the outcome window as the gap. Examples:
          hotel_booking_demand, numerai_v5_2_1m, predict_students_dropout_and_academic_success.
        - no → **Temporal · scoring date**. The open cases are scored at a date, and their outcome is known by the next
          one (a campaign whose last call settles it): windows cut on the scoring date, no gap. Examples:
          bank_marketing.
      - a pricing period →
        **Are a period's claims still open when the next price is set?** _(data and documentation; reads the source's
        claim reporting: claims of a policy year known only when it ends, or settled within it)_
        - yes → **Temporal · period start, closed periods only**. A price set for the next period (a tariff year), and a
          period's claims still open when the next price is set: windows cut on the period start, training only on
          periods closed by then. Examples: pricing_game_2016_french_fleet, spanish_motor_insurance_2015_2018.
        - no → **Temporal · period start**. A price set for the next period, and a period's claims known by the time the
          next price is set: windows cut on the period start, no gap. No v0.2 definition reaches it yet.

## Panel data

**Does the model go forward in time with the units it holds, or across to units it does not hold?** _(use case; reads
the use case. A panel follows the same identified units over repeated occasions, so a test can step forward along the
occasions, across to other units, or both: the next month of the same stores, the next visit of the same patients →
forward; other stations, clients or sessions → across)_
- forward: later occasions of the units it holds →
  **Do the units share a calendar, or does each have only its own sequence?** _(data and documentation; reads the raw
  rows: a date, month or year that all units share → shared; only a visit number or hours since admission → each unit's
  own sequence; nothing → no order (orientation: Time: Dated, Within Entity, Lost))_
  - a shared calendar →
    **Do the shared dates give enough whole periods for three windows?** _(data and documentation; reads the span and
    density of the dates (SPLIT-14))_
    - no → **Grouped · `ForcedGroupedFromTemporal` (the unit, too few periods)**. Later occasions of the units held, on
      a shared calendar, but too few whole periods for three windows: whole units held out. Examples:
      spanish_motor_insurance_coverage_level_2022_2024.
    - yes →
      **Is the target known only after a delay longer than the time step, or does the use case predict ahead?** _(data
      and documentation; reads SPLIT-10: the source's account of when the target is known (the next day's reading, a
      rate published years later), checked on the newest periods; or a planning lead the use case states (a forecast
      issued days ahead, sales planned weeks ahead); no gap where the delay is within the time step or a written
      exception holds (orientation: the Target tag))_
      - yes, late labels → **Temporal · whole periods, label-delay gap**. Later occasions of the units held, on a
        calendar they share, the target known only after a delay longer than the time step (the next day's minimum, a
        completion rate published years later): windows of whole periods across all units, a gap of about the delay
        (SPLIT-10). Examples: bias_correction_r_bias_correction_r_2, college_scorecard,
        g_research_crypto_forecasting_1m.
      - yes, a planning lead → **Temporal · whole periods, planning gap**. Later occasions of the units held, on a
        calendar they share, and the use case predicts ahead (a forecast issued days before, sales planned weeks ahead):
        windows of whole periods across all units, the planning lead as the gap. Examples:
        climate_model_weather_forecasting_1m, rossmann_store_sales.
      - no → **Temporal · whole periods**. Later occasions of the units held, on a calendar they share, the target known
        with the occasion or within the time step, or no gap by a written SPLIT-10 exception: windows of whole periods
        across all units, no gap. Examples: airqo_low_cost_air_quality_monitor_calibration_challenge,
        ashrae_great_energy_predictor_iii_1m, garments_worker_productivity.
  - each unit's own sequence → **Temporal · each unit's last occasions**. Later occasions of the units held, but each
    unit has only its own sequence (a visit number, hours since admission): each unit's last occasions tested, its
    earlier ones in training. Examples: dementia_prediction, sepsis_prediction_1m.
  - no order → **Grouped · `ForcedGroupedFromTemporal` (the unit, no order)**. Later occasions of the units held, but no
    order at all: whole units held out; the step forward stays untested. No v0.2 definition reaches it yet.
- across: units it does not hold →
  **At the occasions the panel covers, or at later ones?** _(use case; reads the use case: other units over the same
  months, or with no calendar at all → covered; new units observed after the data → later)_
  - the occasions covered, or no calendar → **Grouped · `Retrospective` (whole units)**. Units the panel does not hold,
    over the occasions it covers or with no calendar: whole units held out with all their occasions. Examples:
    5g_energy_consumption, amex_non_iid_1m, electric_motor_temperature_prediction.
  - later occasions → **Temporal · later periods, units unseen**. New units at later occasions: windows of whole
    periods, the test units unseen in training. No v0.2 definition reaches it yet.

## Definitions that ship another split

When the tree was adopted (2026-11-17), these v0.2 definitions shipped a split other than their leaf's. Each is
open for a reviewer: change the split, or keep it and write the reason in the `splits_comment`.

| Definition | Leaf | Ships |
|---|---|---|
| ecoli_proteins | Temporal · entry date (recording or selection moves) | random, `Timeless` |
| ai4d_lab_tanzania_tourism_classification_challenge | Temporal · rebuilt round | random, `ForcedIIDFromTemporal` |
| fiat_500 | Grouped · `Retrospective` (the unit) | random, `Retrospective` |
| immoscout_german_house_prices | Grouped · `Retrospective` (the unit) | random, `Retrospective` |
| fremtpl2 | Temporal · rebuilt order | random, `ForcedIIDFromTemporal` |
| bad_customer_detection | Temporal · arrival date | random, `StationaryRelation` (measured) |
| cirrhosis_patient_survival_prediction | Temporal · arrival date | random, `StationaryRelation` (measured) |
| dementia_prediction | Temporal · each unit's last occasions | grouped, `ForcedGroupedFromTemporal` |
| sepsis_prediction_1m | Temporal · each unit's last occasions | grouped, `ForcedGroupedFromTemporal` |
| tunisian_fraud_detection_challenge | Grouped · `Retrospective` (whole units) | temporal |

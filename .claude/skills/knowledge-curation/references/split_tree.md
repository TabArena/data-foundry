# Deciding a split from the data collection type

This is the decision tree SPLIT-36 in [splits.md](splits.md) asks you to walk for every definition's split. Its root
is the record's data collection type (SPLIT-34); under each type the use case is asked first, then what the data and
its documentation allow, then a measurement where one decides. A leaf names the split and what justifies it: the time
basis of SPLIT-32, a forced tag of SPLIT-8, `ForcedIIDFromGrouped` of SPLIT-35, or for a temporal split the date the
windows are cut on and the gap.

## How to walk it

* Start at the record's collection type, and answer each question from what it says it reads. The kinds of question
  are marked: _use case_ (the source's stated application and the definition's use case), _data and documentation_
  (the raw rows, the source's account of how the data was collected), _measurement_ (a number you compute and write
  into the `Time basis:` line). A collection fact (`Samples:`, `Time:`, `Target:`, `Entities:`) appears only as
  "orientation": it points to where to look, it never answers a question by itself.
* Answer as if no split had been decided. The leaf you reach is the split to implement, with the tag in its title.
  `Random · ...` is an IID split, `Grouped · ...` a `grouping`, `Temporal · ...` a `temporal` declaration. A
  `ForcedIIDFromGrouped` leaf sits beside a time basis (SPLIT-35): the questions of the type's other branches give it.
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
* A temporal leaf gives the date the windows are cut on and the gap; the windows and the horizon are signed off by
  the curator (SPLIT-12, SPLIT-14), as is every window that trains on less than half of the rows.

## Shared answers

* **Family-key step (①).** Under the expanding science catalogue, every answer that does not split by entry date
  continues at "Can the data compute a family key?", written once below: the family key is a catalogue's default split;
  without one the split is `Timeless`, grouped by the item where items repeat, else random, and a catalogue does not
  carry `ForcedIIDFromGrouped` (SPLIT-37 step 2).
* **ForcedFromTemporal step.** Every forced point of the tree (too few periods or snapshots, an order lost, one
  prediction point) continues at the same step, written once below. It first asks whether the arrival order can be
  reconstructed from the data (SPLIT-22): if so, rebuild it, record it as recovered time (`Time: Inferred`) and walk
  the tree again from the root. If the windows failed only for too few positives in a sequence that is not stationary,
  the task is `Too Small` and never falls back to random (SPLIT-16). Otherwise it is the only place for a reason to keep
  a split random: a relation
  measured flat over the periods held (`StationaryRelation`), or, where nothing can be measured, a person's domain or
  use-case reason (`AssumedStationaryRelation`); a unit with several rows makes either grouped by the unit. Without a
  reason, whole periods are held out where the data has at least two, then the unit where it has several rows and the
  use case meets new units, then random (SPLIT-8, SPLIT-32).
* **The gap.** Under every temporal leaf the gap follows SPLIT-10: late labels (a gap of about the delay, or training
  only on cases whose outcome is known before the window), a planning lead the use case states (a forecast issued
  ahead), an outcome window still open at the next scoring date (a policy year's claims when the next tariff is set). No
  gap where the delay is within the time step or a written exception holds.
## Expanding science catalogue

**Does the use case predict for the items the catalogue adds next?** _(use case; reads SPLIT-37 step 3: the source's
stated aim and scope (abstract, methods, caveats); its own split counts only where chosen for the use. Items like those
it was built from, or items from elsewhere (other sites or instruments) → no; compounds not yet made, materials not yet
reported, or no scope stated → yes. In every leaf an item's copies stay on one side (step 1))_
- no: items like those it holds, or from elsewhere → **① family-key step** (here: open_soil_spectral_library,
  qsar_biodeg, superconductivity)
- yes, or no scope stated →
  **Does each item carry a final date of entry into this catalogue?** _(data and documentation; reads SPLIT-37 step 4: a
  date of entry into this catalogue in the release or a parent source, not a registration that predates it; items still
  to come, not an inventory already collected, a closed study or a designed experiment; labels final (orientation: the
  Time tag, Target: Revised Later))_
  - no → **① family-key step** (here: drug_induced_autoimmunity_prediction, nci_aids_antiviral_screen,
    qsar_oral_toxicity)
  - yes →
    **Does arrival change what is recorded or selected, or does the date carry waves?** _(measurement; reads step 4a: a
    recording convention or an intake that moves with the entry date; step 4b: a forward split leaves clearly fewer
    close training neighbours than a random draw)_
    - yes →
      **Does the order give the windows SPLIT-14 and SPLIT-15 ask for?** _(data and documentation; reads the span and
      density of the order (the dates, rounds, entry dates or rebuilt order): at least three windows; the newest and one
      other train on at least half of the rows, the others on at least 30% (SPLIT-14); about 50 test rows or more per
      window (SPLIT-17), with enough positives in each for a classification task (TP-9; too few in a drifting sequence
      makes the task Too Small, SPLIT-16); as many windows as an IID or grouped task of that size gets folds (SPLIT-15,
      SPLIT-33), as long as they stay meaningful; counted after the gap a label delay needs: if the gap breaks the
      floor, no (a curator may still accept an exception, SPLIT-10))_
      - yes → **Temporal · entry date**. Items the catalogue adds next, each with a final entry date, and arrival
        changes how items are recorded or which are taken in, or a forward split leaves clearly fewer close training
        neighbours than a random draw (SPLIT-37 step 4): each era tested on the earlier ones; an item keys on its first
        date, which orders the split and is no input; the gap as SPLIT-10 sets it (a label delay or a planning lead).
        Examples: apistox, ecoli_proteins, qsar_tid_11.
      - no → **① family-key step**
    - no → **① family-key step** (here:
      force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition, protein_model_quality_rf_pcp,
      qsar_aquatic_toxicity, …)

## Experimental results

**Is there an order to how samples arrive in the use case?** _(use case; reads the use case: samples sent to a
certification body one after another, visitors at a screening point → yes; a property of an item, the outcome of a
designed run, with no sample before or after another → no)_
- yes →
  **Is the order available in the data?** _(data and documentation; reads the raw rows: a recorded date, or an order
  rebuilt from the data (a file position, an id) and checked against something dated (orientation: the Time tag))_
  - yes →
    **Does the order give the windows SPLIT-14 and SPLIT-15 ask for?** _(data and documentation; reads the span and
    density of the order (the dates, rounds, entry dates or rebuilt order): at least three windows; the newest and one
    other train on at least half of the rows, the others on at least 30% (SPLIT-14); about 50 test rows or more per
    window (SPLIT-17), with enough positives in each for a classification task (TP-9; too few in a drifting sequence
    makes the task Too Small, SPLIT-16); as many windows as an IID or grouped task of that size gets folds (SPLIT-15,
    SPLIT-33), as long as they stay meaningful; counted after the gap a label delay needs: if the gap breaks the floor,
    no (a curator may still accept an exception, SPLIT-10))_
    - yes → **Temporal · sample order**. Later samples in an order the data holds (a recorded date, or an order rebuilt
      from the data and checked against something dated): each window tested on the earlier samples; a rebuilt order
      orders the split and is no input; the gap as SPLIT-10 sets it (a label delay or a planning lead). Examples:
      infrared_thermography_temperature, wine_quality.
    - no → **ForcedFromTemporal step**
  - no → **ForcedFromTemporal step**
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
      held out with all their rows. Where the use case holds out a wider group (a problem class, a target gene), group
      on it and tag UnseenGroup, as the kind question does. Examples: airfoil_self_noise, asp_potassco_classification,
      concrete_compressive_strength.
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
      the kinds held: random. Molecules with exact structures group on the scaffold instead (SPLIT-31). Examples:
      biogeographical_ancestry_prediction, body_density_prediction, forensic_glass_identification.

## Clinical study

**Where will the model be used?** _(use case; reads the use case)_
- at another hospital or site →
  **Does the data hold several sites?** _(data and documentation; reads a hospital or site column; several means enough
  to hold out: whole groups per test fold with every class present, else they count as one (covertype's four areas; the
  weighed factor 'Only a few groups'))_
  - yes → **Grouped · `UnseenGroup` (sites)**. Another hospital, and the data holds several: whole sites held out.
    Examples: gossis_icu_hospital_mortality.
  - no → **Random · `ForcedIIDFromGrouped` (one site, the transfer untested)**. Another hospital is the use, but the
    data holds one: random; the step to another site stays untested, as the `Group basis:` line says. No v0.2 definition
    reaches it yet.
- at the same clinic, for later patients →
  **Is an arrival order available in the data, or can it be recovered?** _(data and documentation; reads the raw rows
  and the source: an order rebuilt from case numbers, encounter numbers or deposit batches and checked against something
  dated (a date the raw rows record would make the set a dated event log); or the order is lost; or all patients share
  one prediction point, a cohort scored at one baseline exam (orientation: Time: Inferred, Samples: One Moment))_
  - yes →
    **Does the order give the windows SPLIT-14 and SPLIT-15 ask for?** _(data and documentation; reads the span and
    density of the order (the dates, rounds, entry dates or rebuilt order): at least three windows; the newest and one
    other train on at least half of the rows, the others on at least 30% (SPLIT-14); about 50 test rows or more per
    window (SPLIT-17), with enough positives in each for a classification task (TP-9; too few in a drifting sequence
    makes the task Too Small, SPLIT-16); as many windows as an IID or grouped task of that size gets folds (SPLIT-15,
    SPLIT-33), as long as they stay meaningful; counted after the gap a label delay needs: if the gap breaks the floor,
    no (a curator may still accept an exception, SPLIT-10))_
    - yes → **Temporal · rebuilt order**. The data holds the arrival order (encounter numbers) with enough periods: each
      window tested on the earlier patients; the gap as SPLIT-10 sets it (a label delay or a planning lead). Examples:
      diabetes_130_us, horse_colic_survival.
    - no → **ForcedFromTemporal step** (here: regensburg_pediatric_appendicitis, lung_cancer_epithelial_genexp)
  - no, the order is lost → **ForcedFromTemporal step** (here: breast_cancer_prediction, diabetes_3,
    differentiated_thyroid_cancer_recurrence, …)
  - no, all patients share one prediction point → **ForcedFromTemporal step** (here: framingham_heart_study_fhs)

## Survey

**Whom, and when, does the model predict for?** _(use case; reads the use case)_
- later respondents, arriving one by one without rounds →
  **Does the interview order give the windows SPLIT-14 and SPLIT-15 ask for?** _(data and documentation; reads a
  recorded interview date, or an order rebuilt from the data and checked against something dated (SPLIT-22): at least
  three windows; the newest and one other train on at least half of the rows, the others on at least 30% (SPLIT-14);
  about 50 test rows or more per window (SPLIT-17), with enough positives in each for a classification task (TP-9; too
  few in a drifting sequence makes the task Too Small, SPLIT-16); as many windows as an IID or grouped task of that size
  gets folds (SPLIT-15, SPLIT-33), as long as they stay meaningful; counted after the gap a label delay needs: if the
  gap breaks the floor, no (a curator may still accept an exception, SPLIT-10); no date or order → no)_
  - yes → **Temporal · interview order**. Later respondents arrive one by one, and a recorded interview date or a
    rebuilt order gives the windows SPLIT-14 and SPLIT-15 ask for: each window tested on the earlier respondents, the
    gap as SPLIT-10 sets it; a rebuilt order orders the split and is no input. No v0.2 definition reaches it yet.
  - no → **ForcedFromTemporal step** (here: caracas_cervical_cancer)
- the surveyed population at a later round →
  **Do the rounds give the windows SPLIT-14 and SPLIT-15 ask for?** _(data and documentation; reads the rounds a round,
  wave or date column records (an election year, an observation date), or rounds rebuilt from the data and checked: at
  least three windows; the newest and one other train on at least half of the rows, the others on at least 30%
  (SPLIT-14); about 50 test rows or more per window (SPLIT-17), with enough positives in each for a classification task
  (TP-9; too few in a drifting sequence makes the task Too Small, SPLIT-16); as many windows as an IID or grouped task
  of that size gets folds (SPLIT-15, SPLIT-33), as long as they stay meaningful; counted after the gap a label delay
  needs: if the gap breaks the floor, no (a curator may still accept an exception, SPLIT-10); no rounds at all → no)_
  - yes → **Temporal · round**. The next round is the use, and the rounds, recorded or rebuilt from the data, give the
    windows SPLIT-14 and SPLIT-15 ask for: each round tested on the earlier ones; a rebuilt round orders the split and
    is no input; the gap as SPLIT-10 sets it (a label delay or a planning lead). Examples:
    ai4d_lab_tanzania_tourism_classification_challenge, anes_voting_2026, sdss_17.
  - no → **ForcedFromTemporal step**
- people or places the survey did not sample, at the rounds held →
  **Inside the population and area the survey covered, or outside them?** _(use case; reads the use case: gaps between
  sampled sites, respondents like these → inside; groups or places the survey never reached → outside)_
  - inside →
    **Did the survey sample in clusters, or ask each respondent several items?** _(data and documentation; reads the
    source's sampling design and a cluster or respondent id in the raw file: plots in a burn area, a respondent's
    several scenarios (orientation: Entities: Recur))_
    - yes → **Grouped · `Retrospective` (sampling cluster)**. People or places the survey did not sample, inside what it
      covered, where it sampled in clusters (sites, burn areas) or a respondent answered several items: whole clusters
      or respondents held out. Check that no row of a test row's time carries its target (one day's weather across
      stations); if one does, group by that time unit (SPLIT-32, question 2). Examples: boreal_postfire_lichen_biomass,
      in_vehicle_coupon_recommendation.
    - no → **Random · `Retrospective`**. People the survey did not sample, inside what it covered, one row each and no
      clusters: random, a fair draw of the same design. Check that no row of a test row's time carries its target (one
      day's weather across stations); if one does, group by that time unit (SPLIT-32, question 2). No v0.2 definition
      reaches it yet.
  - outside →
    **Does the data hold several of those groups or places?** _(data and documentation; reads a facility, region or site
    column; several means enough to hold out: whole groups per test fold with every class present, else they count as
    one (covertype's four areas; the weighed factor 'Only a few groups'))_
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
    **Does a unit have several rows, and does the use case meet new units?** _(data and documentation; reads USE-10: a
    unit id that repeats in the snapshot, recorded or rebuilt exactly from the data (SPLIT-24: a stone, a car), and the
    use case: units the snapshot does not hold → grouped; more rows of units it holds (another listing of a known car),
    or one row per unit → random. Exact copies are dropped, not grouped (LEAK-19); repeats that matter but cannot be
    identified retire the dataset (SPLIT-25), for a reviewer (orientation: Entities: Recur))_
    - yes: several rows, new units in use → **Grouped · `Retrospective` (the unit)**. Rows of this snapshot that lack
      the label, scattered among labelled ones, and a unit (a stone, a car) has several rows: whole units held out.
      Check that no row of a test row's time carries its target (one day's weather across stations); if one does, group
      by that time unit (SPLIT-32, question 2). Examples: diamonds.
    - no: one row per unit, or known units in use → **Random · `Retrospective`**. Rows of this snapshot that lack the
      label, scattered among labelled ones, one row per unit: random is the use. Check that no row of a test row's time
      carries its target (one day's weather across stations); if one does, group by that time unit (SPLIT-32, question
      2). Examples: fiat_500, houses, immoscout_german_house_prices.
  - whole areas or groups →
    **Does the snapshot hold a key for them?** _(data and documentation; reads a group column (a producer) or a location
    fine enough to cut blocks)_
    - yes → **Grouped · `Retrospective` (area or group)**. Whole areas or groups of the snapshot lack the label (a
      producer new to the shop), and the snapshot holds their key: whole areas or groups held out. Check that no row of
      a test row's time carries its target (one day's weather across stations); if one does, group by that time unit
      (SPLIT-32, question 2). Examples: wine_world_cost.
    - no → **Random · `ForcedIIDFromGrouped` (no area key)**. Whole areas lack the label (unmapped land), but the
      snapshot holds no key fine enough to hold them out: random beside the Retrospective time basis, the share of test
      rows whose neighbours sit in training named in the `Group basis:` line. Examples: covertype.
- a whole population scored at a date, for what happens after it →
  **Can different snapshots be reconstructed from the data to give the windows SPLIT-14 and SPLIT-15 ask for?** _(data
  and documentation; reads the source's reference dates: a second labelled file of the same population, scoring dates
  kept per row; one reference date, or several mixed with their dates lost, give none. at least three windows; the
  newest and one other train on at least half of the rows, the others on at least 30% (SPLIT-14); about 50 test rows or
  more per window (SPLIT-17), with enough positives in each for a classification task (TP-9; too few in a drifting
  sequence makes the task Too Small, SPLIT-16); as many windows as an IID or grouped task of that size gets folds
  (SPLIT-15, SPLIT-33), as long as they stay meaningful; counted after the gap a label delay needs: if the gap breaks
  the floor, no (a curator may still accept an exception, SPLIT-10))_
  - yes → **Temporal · scoring date**. A whole population scored at a date, and enough snapshots with their outcomes can
    be reconstructed for three test windows, each trained on the earlier snapshots; the gap as SPLIT-10 sets it (a label
    delay or a planning lead). No v0.2 definition reaches it yet.
  - no → **ForcedFromTemporal step** (here: account_debt_south_africa, allstate_claim_prediction_challenge_1m,
    blood_transfusion, …)
- units of a place or group the snapshot does not hold →
  **Does the snapshot hold several of them?** _(data and documentation; reads a municipality, branch, region or site
  column with several groups to hold out; several means enough to hold out: whole groups per test fold with every class
  present, else they count as one (covertype's four areas; the weighed factor 'Only a few groups'))_
  - yes → **Grouped · `UnseenGroup` (groups)**. The model meets units of a place or group the snapshot does not hold (a
    new municipality, branch or region), and the snapshot holds several: whole groups held out. No v0.2 definition
    reaches it yet.
  - no → **Random · `ForcedIIDFromGrouped` (one group, the transfer untested)**. Another place or group is the use, but
    the snapshot holds one: random; the transfer stays untested, as the `Group basis:` line says. No v0.2 definition
    reaches it yet.
- new cases that arrive one by one →
  **Can the arrival order be rebuilt from the data and checked against time?** _(measurement; reads an id issued in
  sequence or the export's row order, checked against something dated (orientation: Time: Inferred))_
  - yes →
    **Does the order give the windows SPLIT-14 and SPLIT-15 ask for?** _(data and documentation; reads the span and
    density of the order (the dates, rounds, entry dates or rebuilt order): at least three windows; the newest and one
    other train on at least half of the rows, the others on at least 30% (SPLIT-14); about 50 test rows or more per
    window (SPLIT-17), with enough positives in each for a classification task (TP-9; too few in a drifting sequence
    makes the task Too Small, SPLIT-16); as many windows as an IID or grouped task of that size gets folds (SPLIT-15,
    SPLIT-33), as long as they stay meaningful; counted after the gap a label delay needs: if the gap breaks the floor,
    no (a curator may still accept an exception, SPLIT-10))_
    - yes → **Temporal · rebuilt order**. New cases arrive one by one; the raw rows hold no date, but an order rebuilt
      from an id or the file's row order tracks time: windows on it, the order no input when it comes with the target;
      the gap as SPLIT-10 sets it (a label delay or a planning lead). Examples: fremtpl2, labour_inspection_compliance,
      loan_default_prediction_imperial_college.
    - no → **ForcedFromTemporal step**
  - no → **ForcedFromTemporal step** (here: allstate_claims_severity, amazon_employee_access, aps_failure, …)

## Dated event log

**Will the model be used at a place or group the data does not hold?** _(use case; reads the use case: a new hospital, a
new region)_
- yes →
  **Does the data hold several of them?** _(data and documentation; reads a hospital, region or site column; several
  means enough to hold out: whole groups per test fold with every class present, else they count as one (covertype's
  four areas; the weighed factor 'Only a few groups'))_
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
    **Do the dates give the windows SPLIT-14 and SPLIT-15 ask for?** _(data and documentation; reads the span and
    density of the dates: at least three windows; the newest and one other train on at least half of the rows, the
    others on at least 30% (SPLIT-14); about 50 test rows or more per window (SPLIT-17), with enough positives in each
    for a classification task (TP-9; too few in a drifting sequence makes the task Too Small, SPLIT-16); as many windows
    as an IID or grouped task of that size gets folds (SPLIT-15, SPLIT-33), as long as they stay meaningful; counted
    after the gap a label delay needs: if the gap breaks the floor, no (a curator may still accept an exception,
    SPLIT-10))_
    - no → **ForcedFromTemporal step** (here: 2_month_survival_rate_prediction, bad_customer_detection,
      frempl_french_motor_personal_line, …)
    - yes →
      **What sets off a prediction?** _(use case; reads the use case: a case that arrives (an order, a trip, a loan); a
      date at which the open cases are scored (bookings not yet arrived, accounts at a month-end, policies priced at the
      start of a tariff year))_
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
          (a forecast made a day ahead): windows on the arrival date, the planning lead as the gap. A planning lead that
          makes the task look like forecasting is first checked for tabular scope (SEL-11, TP-10). No v0.2 definition
          reaches it yet.
        - no → **Temporal · arrival date**. Each case scored when it arrives, its target known with it or within the
          time step, or no gap by a written SPLIT-10 exception: windows on the arrival date, no gap. Examples:
          acquire_valued_shoppers_challenge, alfa_battle_2_0_task_2, ames_housing.
      - a date at which open cases are scored (a month-end, a tariff year's start) →
        **Is the outcome window still open at the next scoring date?** _(data and documentation; reads the source's
        definition of the outcome window (a 20-day return, three months after the period, the arrival of a booking, a
        policy year's claims known only when it ends) against the spacing of the scoring dates)_
        - yes → **Temporal · scoring date, outcome window as gap**. The open cases are scored at a date (bookings not
          yet arrived, accounts at a month-end, the stocks of a week, policies priced at a tariff year's start), and
          their outcome window is still open at the next scoring date: windows cut on the scoring date, training only on
          cases whose outcome window has closed by then (the outcome window as the gap, a policy year's claims closed).
          Examples: hotel_booking_demand, numerai_v5_2_1m, predict_students_dropout_and_academic_success.
        - no → **Temporal · scoring date**. The open cases are scored at a date, and their outcome is known by the next
          one (a campaign whose last call settles it): windows cut on the scoring date, no gap. Examples:
          bank_marketing.

## Panel data

**Does the model fill in the period the panel covers, or predict after it?** _(use case; reads the use case: occasions
the panel covers but did not record, or units it did not observe then (a reading not taken, a station not in the
network) → fill in; the next month of the same stores, the next visit of the same patients, new patients or stations
after the data → predict after it)_
- fill in the covered period →
  **Are the occasions to fill in scattered among a unit's recorded ones, or are whole units missing?** _(use case; reads
  the use case: a reading not taken at a station that reports, a month a firm did not file → scattered; a station not in
  the network, a firm not surveyed → whole units (also when some recorded units have gaps too: holding units out is the
  stricter test))_
  - scattered among recorded occasions → **Random · `Retrospective` (scattered occasions)**. Fill in occasions the panel
    covers but did not record, scattered among a unit's recorded ones: random over the occasions; a unit's other
    occasions in training are the use, not a leak. Check that no row of a test row's time carries its target (one day's
    weather across stations); if one does, group by that time unit (SPLIT-32, question 2). No v0.2 definition reaches it
    yet.
  - whole units missing → **Grouped · `Retrospective` (whole units)**. Fill in the covered period where whole units are
    missing (a station not in the network, a firm not surveyed): whole units held out with all their occasions. Check
    that no row of a test row's time carries its target (one day's weather across stations); if one does, group by that
    time unit (SPLIT-32, question 2). Examples: 5g_energy_consumption, electric_motor_temperature_prediction,
    fraud_detection_in_electricity_and_gas_consumption_1m.
- predict after it →
  **Which units does the model predict for?** _(use case; reads the use case: later occasions of units the panel holds,
  also when new units join them → the same units, or both; patients, stations, clients or stays not in the data, and no
  known unit's later occasions → only new units)_
  - the same units, or both same and new units (their later occasions) →
    **Do the units share a calendar, or does each have only its own sequence?** _(data and documentation; reads the raw
    rows: a date, month or year that all units share → shared; only a visit number or hours since admission → each
    unit's own sequence (orientation: Time: Dated, Within Entity))_
    - a shared calendar →
      **Do the shared dates give the windows SPLIT-14 and SPLIT-15 ask for, in whole periods?** _(data and
      documentation; reads the span and density of the shared dates, in whole periods across all units: at least three
      windows; the newest and one other train on at least half of the rows, the others on at least 30% (SPLIT-14); about
      50 test rows or more per window (SPLIT-17), with enough positives in each for a classification task (TP-9; too few
      in a drifting sequence makes the task Too Small, SPLIT-16); as many windows as an IID or grouped task of that size
      gets folds (SPLIT-15, SPLIT-33), as long as they stay meaningful; counted after the gap a label delay needs: if
      the gap breaks the floor, no (a curator may still accept an exception, SPLIT-10))_
      - no → **ForcedFromTemporal step** (here: spanish_motor_insurance_coverage_level_2022_2024)
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
          calendar they share, and the use case predicts ahead (a forecast issued days before, sales planned weeks
          ahead): windows of whole periods across all units, the planning lead as the gap. A panel that looks like
          forecasting is first checked for tabular scope (SEL-11, TP-10). Examples:
          climate_model_weather_forecasting_1m, rossmann_store_sales.
        - no → **Temporal · whole periods**. Later occasions of the units held, on a calendar they share, the target
          known with the occasion or within the time step, or no gap by a written SPLIT-10 exception: windows of whole
          periods across all units, no gap. Examples: airqo_low_cost_air_quality_monitor_calibration_challenge,
          ashrae_great_energy_predictor_iii_1m, garments_worker_productivity.
    - each unit's own sequence → **Temporal · each unit's last occasions (not declarable yet)**. Later occasions of the
      units held, each unit with only its own sequence (a visit number, hours since admission): each unit's last
      occasions tested, its earlier ones in training. Data Foundry cannot declare a split inside each unit yet (a
      grouped split holds whole units out), so a case here goes to a reviewer. No v0.2 definition reaches it yet.
  - only new units → **Grouped · `UnseenGroup` (new units)**. Only new units, met after the data (new patients, new
    customers): the use case aims at units the panel does not hold, so whole units are held out (SPLIT-32); the unit's
    earlier occasions serve as context only where the use case reads them (Grouping with time_on and context past_rows,
    otherwise none); the later calendar stays untested, as the `Time basis:` line says. Examples: amex_non_iid_1m,
    dementia_prediction, sepsis_prediction_1m.
  - units of a place or group the panel does not hold (a new hospital, a new station network) →
    **Does the data hold several of them?** _(data and documentation; reads a hospital, region, network or site column;
    several means enough to hold out: whole groups per test fold with every class present, else they count as one
    (covertype's four areas; the weighed factor 'Only a few groups'))_
    - yes → **Grouped · `UnseenGroup` (groups)**. Units of a place or group the panel does not hold, and the data holds
      several: whole groups held out with all their units and occasions (SPLIT-32). No v0.2 definition reaches it yet.
    - no → **Grouped · `UnseenGroup` (units; the other place untested)**. Units of a place or group the panel does not
      hold, but the data holds one: whole units held out, the closest split; the step to another place stays untested,
      as the `Time basis:` line says. No v0.2 definition reaches it yet.

## The family-key step (①)

The catalogue's family-key questions, reached from its scope answer and from the next-items branch.

**① Can the data compute a family key: a scaffold, an element set, a protein target, a site, a survey or an
instrument?** _(data and documentation; reads SPLIT-37 step 2: a key computed from the data, with several groups to hold
out, not the label; the scaffold for molecules (SPLIT-31), the survey or site that stands for elsewhere (step 3).
Reached when the entry date does not decide: a use case that stays with items like those held or aims elsewhere, no
final entry date, arrival that changes nothing, or too few windows on the entry date)_
- yes → **Grouped · `UnseenGroup` (the family key)**. The entry date does not decide, and the data computes a family key
  (a scaffold, an element set, a protein target, a site, a survey or an instrument), a catalogue's default split
  (SPLIT-37): whole families held out, each item's copies with them; how the catalogue grew goes in the notes with its
  measurement. Examples: drug_induced_autoimmunity_prediction, nci_aids_antiviral_screen, qsar_oral_toxicity.
- no →
  **Does an item have several rows (re-measurements)?** _(data and documentation; reads SPLIT-37 step 1: an item id or a
  structure that repeats in the raw file (a compound tested twice, a composition reported in several papers); exact
  copies are dropped, not grouped (LEAK-19) (orientation: Entities: Recur))_
  - yes → **Grouped · `Timeless` (the item)**. The entry date does not decide, no family key can be computed, and an
    item has several rows: whole items held out with their re-measurements (SPLIT-37 step 1); the family the use case
    would hold out goes in the notes. No v0.2 definition reaches it yet.
  - no → **Random · `Timeless` (no family key)**. The entry date does not decide, no family key can be computed apart
    from the label, and one row per item: random; the target is a property of the item. The family the use case would
    hold out goes in the notes with the overlap the split leaves (SPLIT-37 step 2). No v0.2 definition reaches it yet.

## The ForcedFromTemporal step

Every forced point of the tree continues here: too few periods or snapshots, an order lost, one prediction point.

**ForcedFromTemporal: can the sample arrival order be reconstructed from the data?** _(data and documentation; reads
SPLIT-22: an order the release does not record but the data allows (an id issued in sequence, the export's row order,
case or encounter numbers, a recovered survey wave), checked against something dated; not an order the branch above
already used and found too short. Yes → rebuild it and walk the tree again from the root, with the order as recovered
time (Time: Inferred); no → the forced split below)_
- yes → **Restart · rebuild the order, then walk the tree again**. The arrival order can be reconstructed from the data:
  rebuild it (SPLIT-22), record it as recovered time (Time: Inferred), and answer the tree again from the root with that
  order; the leaf it reaches decides the split. No v0.2 definition reaches it yet.
- no →
  **Did the windows fail only because they hold too few positives, in a sequence that is not stationary?** _(data and
  documentation; reads SPLIT-16 and TP-9: count the positives per candidate window; a time series or a drifting sequence
  whose windows would have enough rows but too few positives must not fall back to a random split. No when the windows
  failed for too few periods, rows or a lost order)_
  - yes → **Retire · Too Small**. The windows hold too few positives in a sequence that is not stationary: no random
    fallback; the task is Too Small (SPLIT-16, TP-9), retired or kept only on the curator's call. No v0.2 definition
    reaches it yet.
  - no →
    **Is there a reason to treat later samples as interchangeable with the data's?** _(measurement; reads SPLIT-32:
    measured: the target and its relation to the features flat across the periods the data holds (dated or a rebuilt
    order), over the longest span the source or a parent covers, in the `Time basis:` line; assumed: a person's domain
    or use-case reason, only where no two periods can be measured (the time lost), written as AssumedStationaryRelation
    (<person>, <date>): <reason>; neither: measured not flat, or nothing to measure and no person has given a reason)_
    - yes, measured flat across the periods held →
      **Does a unit have several rows, and does the use case meet new units?** _(data and documentation; reads USE-10: a
      unit id that repeats, recorded or rebuilt exactly from the data (SPLIT-24: a household, a client, a policy, a
      patient), and the use case: new units → grouped; more rows of units it holds, or one row per unit → random. Exact
      copies are dropped, not grouped (LEAK-19); repeats that matter but cannot be identified retire the dataset
      (SPLIT-25), for a reviewer (orientation: Entities: Recur))_
      - yes: several rows, new units in use → **Grouped · `StationaryRelation` (the unit)**. No usable windows, but the
        relation is measured flat across the periods held: whole units held out, as a unit has several rows; the
        measurement in the `Time basis:` line, a later period untested. No v0.2 definition reaches it yet.
      - no: one row per unit, or known units in use → **Random · `StationaryRelation`**. No usable windows, but the
        relation is measured flat across the periods held: random, the measurement in the `Time basis:` line; a later
        period untested. Examples: bad_customer_detection, distribution_transformers_at_cauca_department.
    - yes, assumed by a person (nothing to measure) →
      **Does a unit have several rows, and does the use case meet new units?** _(data and documentation; reads USE-10: a
      unit id that repeats, recorded or rebuilt exactly from the data (SPLIT-24: a household, a client, a policy, a
      patient), and the use case: new units → grouped; more rows of units it holds, or one row per unit → random. Exact
      copies are dropped, not grouped (LEAK-19); repeats that matter but cannot be identified retire the dataset
      (SPLIT-25), for a reviewer (orientation: Entities: Recur))_
      - yes: several rows, new units in use → **Grouped · `AssumedStationaryRelation` (the unit)**. No usable windows
        and nothing to measure, and a person gave a domain or use-case reason to treat later samples as interchangeable:
        whole units held out, as a unit has several rows. No v0.2 definition reaches it yet.
      - no: one row per unit, or known units in use → **Random · `AssumedStationaryRelation`**. No usable windows and
        nothing to measure, and a person gave a domain or use-case reason to treat later samples as interchangeable:
        random. No v0.2 definition reaches it yet.
    - neither: measured not flat, or nothing measurable and no person's reason →
      **Is there an order with at least two periods to hold out?** _(data and documentation; reads the raw rows: a date,
      a phase, a round, a presentation or a rebuilt order that cuts the rows into two or more periods of usable size
      (orientation: the Time tag). Opened at every forced point of the tree: too few periods or snapshots, an order
      lost, one prediction point)_
      - yes → **Grouped · `ForcedGroupedFromTemporal` (periods)**. Forced: the use is later in time, but no usable
        windows; the data holds an order with at least two periods (scan periods, study phases, visit months,
        presentations, policy years): whole periods held out, training also on later ones; closer to the shift a
        temporal split tests than random folds, the step forward still untested. Where units recur across periods and
        the use case meets new units, a unit's rows must stay in one period, or the unit is held out with its period
        (USE-10, LEAK-17); check it before shipping. Examples: 2_month_survival_rate_prediction,
        online_shoppers_purchasing_intention_dataset, open_university_learning_analytics_dataset.
      - no →
        **Does a unit have several rows, and does the use case meet new units?** _(data and documentation; reads USE-10:
        a unit id that repeats, recorded or rebuilt exactly from the data (SPLIT-24: a household, a client, a policy, a
        patient), and the use case: new units → grouped; more rows of units it holds, or one row per unit → random.
        Exact copies are dropped, not grouped (LEAK-19); repeats that matter but cannot be identified retire the dataset
        (SPLIT-25), for a reviewer (orientation: Entities: Recur))_
        - yes: several rows, new units in use → **Grouped · `ForcedGroupedFromTemporal` (the unit)**. Forced, no periods
          to hold out, and a unit has several rows (a household, a client, a policy, a patient): whole units held out,
          so no unit's outcome sits on both sides; the step forward stays untested. Examples:
          allstate_claim_prediction_challenge_1m, pricing_game_2017_french_mtpl, aps_failure.
        - no: one row per unit, or known units in use → **Random · `ForcedIIDFromTemporal`**. Forced, no periods to hold
          out and one row per unit: random; the step forward stays untested. Examples: account_debt_south_africa,
          blood_transfusion, churn_telco_south_asia.

## Definitions that ship another split

When the tree was last regenerated (2026-11-17), these v0.2 definitions shipped a split other than their leaf's. Each
is open for a reviewer: change the split, or keep it and write the reason in the `splits_comment`.

| Definition | Leaf | Ships |
|---|---|---|
| 2_month_survival_rate_prediction | Grouped · `ForcedGroupedFromTemporal` (periods) | random, `ForcedIIDFromTemporal` |
| ai4d_lab_tanzania_tourism_classification_challenge | Temporal · round | random, `ForcedIIDFromTemporal` |
| cirrhosis_patient_survival_prediction | Temporal · arrival date | random, `StationaryRelation` |
| ecoli_proteins | Temporal · entry date | random, `Timeless` |
| fremtpl2 | Temporal · rebuilt order | random, `ForcedIIDFromTemporal` |
| horse_colic_survival | Temporal · rebuilt order | grouped, `StationaryRelation` |
| infrared_thermography_temperature | Temporal · sample order | random, `StationaryRelation` |
| online_shoppers_purchasing_intention_dataset | Grouped · `ForcedGroupedFromTemporal` (periods) | random, `ForcedIIDFromTemporal` |
| regensburg_pediatric_appendicitis | Grouped · `ForcedGroupedFromTemporal` (periods) | random, `ForcedIIDFromTemporal` |
| tunisian_fraud_detection_challenge | Grouped · `Retrospective` (whole units) | temporal |

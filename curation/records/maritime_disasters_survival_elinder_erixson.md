---
unique_name: maritime_disasters_survival_elinder_erixson
name: 'Elinder and Erixson (2012), Gender, social norms, and survival in maritime disasters: individual-level database of 18 maritime disasters (Dataset S1)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- No Good Target (yet)
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
original_source: Other
year: '2012'
domain: social science
problem_type: Binary Classification
source_links:
- https://doi.org/10.1073/pnas.1207156109
- https://pmc.ncbi.nlm.nih.gov/articles/PMC3421183/
- http://www.pnas.org/lookup/suppl/doi:10.1073/pnas.1207156109/-/DCSupplemental/sd01.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: an individual-level database of about 15,000 passengers and crew on 18 passenger-ship disasters of 1852-2011, built by two economists to test whether "women and children first" holds. The people and the outcome are real, but no decision rests on a survival prediction for a ship that has already sunk. The closest precedents disagree: `passenger_list_for_the_estonia_ferry_disaster` is at 2nd Tier and `titanic` is `No`. The curator has the call (Consistency check below).
- Proposed reject (refuted): `No` (`No Good Target / Scientific Discovery`, SEL-3, USE-2): a hypothesis study. Its abstract says "We analyze a database of 18 maritime disasters spanning three centuries ... Taken together, our findings show that human behavior in life-and-death situations is best captured by the expression 'every man for himself'" (PNAS abstract), and the paper tests with linear probability models and no classifier, as for `titanic`. Reject check (AI, 2026-10-31): refuted. SEL-3 fails on the source's words, but the selection pattern for survey and discovery tables gives `No` or `TBD -> 2nd Tier`. The curator put the closest case at `TBD -> 2nd Tier`: `passenger_list_for_the_estonia_ferry_disaster`, whose ship is one of these 18, with the same unit, target and kind of features ("Like Titanic, a scientific discovery task", Lennart). `titanic`'s `No` also carries `Trivial` and `Not Representative`, for a toy table with thousands of copies. A precedent with the same facts is followed, so `No` is the curator's call, not a fast reject.
- Open doubt: SEL-3 and USE-2 fail as the source states its purpose. The record stays only if the curator keeps the Estonia record's reading or a use case is found (USE-1). Marker `No Good Target (yet)`, as on the Estonia record.
- Source: Elinder and Erixson, "Gender, social norms, and survival in maritime disasters", PNAS 109(33):13220-13224, 2012 (doi 10.1073/pnas.1207156109; PMC3421183; PMID 22847426). It first appeared as "Every Man for Himself! Gender, Norms and Survival in Maritime Disasters", IFN Working Paper No. 913, 2012. The working paper's Appendix A describes the data: "The database is available as Supporting Online Material in a separate excel file: Maritime Disasters.xlsx". That file is PNAS Dataset S1 (sd01.xlsx); both PNAS links answered 403 to a scripted request on 2026-10-31.
- As published (working paper, Table 1 and Appendix A):
  - 18 ships, from HMS Birkenhead (1852) to MV Bulgaria (2011), among them RMS Titanic 1912 (1,496 casualties, 712 survivors), RMS Lusitania 1915 (1,190 and 768) and MS Estonia 1994 (852 and 137: the 989 people of the Estonia record). Table 1 sums to 15,166 people, 5,667 of whom survived.
  - One row per person: `Survival` (dead and missing grouped as 0); `Female` ("For most ships we have used the individual's name to determine gender"); age (on 9 lists, grouped <16, 16-50, >50, with a child flag on 2 more); crew; passenger class; nationality; companionship. Each person variable is present for some ships only (Table A1).
  - Ship-level variables from Table 1: year, cause, water, nationality, duration (quick or slow, cut at 30 minutes) and whether the captain gave the WCF order.
  - The main sample leaves out the Titanic and the Lusitania ("we focus on the 16 previously uninvestigated shipwrecks"): 11,000 people by Table 1, and 10,976 to 10,978 observations in the pooled regressions (Table 2).
- Use case: none in the source. The paper tests its hypotheses (H1-H6 in the working paper; the PNAS abstract lists eight findings) with linear probability models with shipwreck fixed effects ("The dependent variable (Survival) is binary", Method) and probit checks. It reports coefficients and R², with no prediction and no out-of-sample test. Its one practical point is that "it seems as if it is the policy of the captain, rather than the moral sentiments of men, that determines if women are given preferential treatment" (Discussion). That is a finding for evacuation policy, not a decision taken on a person's predicted survival. A use case would have to be ours (USE-1), and none was found. Regime if kept: grouped by ship (a new disaster is a new group), 18 groups, 16 in the main sample.
- Siblings and duplicates:
  - `passenger_list_for_the_estonia_ferry_disaster` (Lennart, `TBD -> 2nd Tier`, `No Good Target (yet)`; Kaggle and OpenML 43389, 989 people): the record this was found for. Its rows are one of the 18 ships here (PROV-6 overlap).
  - `titanic` (AI `No`, `Trivial`, `Not Representative`; the curator's CC: "Not a real predictive task"): this database holds its own Titanic list with the crew, 2,208 people against titanic3's 1,309 passengers, so the two overlap too.
  - The Lusitania Kaggle manifest that the run put into `source_links` (https://www.kaggle.com/datasets/rkkaggle2/rms-lusitania-complete-passenger-manifest) is one ship's list from another source, not this database. It is related work (PROV-12), so it moves here from `source_links`.

  External collections: none found. A search on 2026-10-31 found no Kaggle, GitHub or OpenML copy of the database. A Mendeley dataset of 30 maritime disasters (doi 10.17632/fygdybctyt.1) holds fault trees in PDFs, another thing.
- Better data: found as better data for `passenger_list_for_the_estonia_ferry_disaster` in the data-scouting run of 2026-10-30/31; no further search.
- Papers and pages:
  - the PNAS paper; its abstract was read through Europe PMC, while the PMC page and pnas.org refused scripted reads on 2026-10-31;
  - the IFN working paper No. 913 (https://www.ifn.se/media/3eoh2e0u/wp913.pdf, 79 pages), read for Table 1, Method, Table 2, Discussion, Appendix A and Table A1; Appendix B describes each disaster and its lists, and Appendix C has the regressions with the Titanic and the Lusitania;
  - the earlier studies of the Titanic and the Lusitania it builds on (Frey, Savage and Torgler 2010, 2011).
- Metric: none found. The working paper and the PNAS abstract report linear probability and probit models (coefficients, p-values, R²) and score no prediction. So the fallback for a binary target on probabilities, roc_auc or log_loss (MET-8). Inputs: the ship as the split group, not a feature.
- Risks for /add-dataset:
  1. A use case (USE-1), or the record goes (SEL-3, USE-2).
  2. Dataset S1: PNAS answers scripts with 403, so a manual download (ask the curator); then check the rows and columns against Table 1 and Table A1.
  3. The Admiral Nakhimov's 1,243 rows were built from counts: "For the Admiral Nakhimov there are aggregate data on the number of male and female passengers and crew. Accordingly, we use the aggregate statistics to construct individual level data" (Appendix A). These are constructed rows: drop them (PROV-3, SEL-16).
  4. The person variables exist per ship only (Table A1), so most columns are empty for most ships and missingness marks the ship. That is harmless under a split grouped by ship, but it thins the features (CLEAN).
  5. `Female` is inferred from names, and "observations, which remained inconclusive ... were left out" (Appendix A).
  6. A split grouped by ship has 18 groups, 16 without the Titanic and the Lusitania (TP-5 per fold). The ship-level variables are constant within a ship, 18 values in all. The WCF order is given during the disaster, so it is known only once the sinking is under way (LEAK).
  7. The Estonia and Titanic rows overlap `passenger_list_for_the_estonia_ferry_disaster` and `titanic` (PROV-6).
  8. The source says its last two selection criteria render "the sample somewhat unrepresentative" and that "British and American ships are likely to be overrepresented" (Appendix A): `Selection Bias` to weigh.
- Priority: gap + (social science has 1 accepted dataset, thin), use case 0 (none), source + (a peer-reviewed paper and a working paper that document each ship's lists and the coding), shape + (about 15,000 people on 18 ships for a grouped split, binary, categorical and ship-level features), risk - (no decision fits, SEL-3; constructed rows for one ship).

**Consistency check (AI, 2026-10-31):** this record is screened `TBD -> 2nd Tier` with `No Good Target (yet)`, like `passenger_list_for_the_estonia_ferry_disaster` (Lennart: "Like Titanic, a scientific discovery task"). `titanic` is `No` ("Not a real predictive task") with the same unit, target and kind of features, and both the Estonia and the Titanic are among these 18 ships. What sets them apart?
(a) The AI's best guess: this is a peer-reviewed database of 18 ships with documented sources and coding, not a toy re-upload with thousands of copies, so `titanic`'s `Trivial` and `Not Representative` do not carry over; recorded as the fact that keeps it at 2nd Tier.
(b) Treat it like `titanic`: `No` with `No Good Target / Scientific Discovery` (SEL-3, USE-2), and reopen the Estonia record to match.
(c) Reopen `titanic` to 2nd Tier, to match the Estonia record and this one.
(d) Amend SEL-3's pattern for survey and discovery tables, to say when such a table waits at 2nd Tier and when it is `No`.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `passenger_list_for_the_estonia_ferry_disaster`.
- as published: over 15,000 individuals of more than 30 nationalities on 18 ships (wrecks spanning three centuries), including MS Estonia (1994) and RMS Lusitania (1915); one row per person; Dataset S1 is an xlsx ...; target: survived (binary); access: open (PNAS supplementary Dataset S1).
- Why: Same target and unit (a person aboard a sinking ship) with the same kind of features as the Estonia passenger list (sex, age, crew/passenger, nationality), from a peer-reviewed study that contains the Estonia itself.
- Adds: About 15x the people (15,000+ against 989) and 18 disasters instead of one, so the ship can be a group for a grouped split, plus ship-level covariates (cause, speed of sinking, captain's WCF order). The verdict question stays: titanic was judged 'No' (no decision is taken on the prediction), and the Estonia record is ...

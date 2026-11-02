---
unique_name: pricing_game_2015_french_mtpl
name: pg15training / pg15pricing (CASdatasets, 2015 French pricing game)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- Two-Regime Zeros
year: '2015'
domain: insurance
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/dutangc/CASdatasets/blob/master/man/pricingame.Rd
- https://github.com/dutangc/CASdatasets/tree/master/data
- https://freakonometrics.hypotheses.org/20034
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 3: the first actuaries' pricing game (2015), 100,000 motor
TPL policies over two years with the game's own pricing task. The earlier `No` for generated covariates rests on
measured marks, not on the source's words, so it is no fast reject; the doubt stays open.
- Source: the pricing game of Arthur Charpentier, Romuald Elie and Jérémie Jakubowicz at the French Institute of
  Actuaries, 5 November 2015 (freakonometrics.hypotheses.org/20034; the English post on r-bloggers, August 2015: "We
  provide two datasets, (motor insurance, third party claims), with 2 years of experience, and 100,000 policies"). Kept
  in CASdatasets as `pg15training` (100,021 x 20) and `pg15pricing` (36,311 x 15): "Datasets from unknown private
  insurers"; "For confidentiality reasons, most categorical levels have unknown meaning." Target: `Indtppd` + `Indtpbi`,
  the third-party material and bodily-injury cost.
- What the source says about real data: neither organiser post nor `pricingame.Rd` says anything about simulation or
  noise; their words describe insurers' policies with recoded levels.
- Doubt (the earlier reject): earlier AI triage, 2026-10-20, measured `Poldur` independent of `Age` (r = 0.05; 168
  fifteen-year policies of drivers aged 20 or less), the same mean car `Value` across `Category` and `Type`, and 12,651
  male "Housewife" rows. Each has a benign reading the source allows: a policy can be older than its present driver
  (pg17's documentation: the same policy "could have evolved in the past (e.g. by changing coverage, or vehicle, or
  drivers"), and levels were recoded for confidentiality. The marks were not calibrated against pg16 or pg17, so PROV-3
  is not settled; `AHDS` stays as the concern to test.
- Use case: the game's: "Each 'team' has to submit premium proposal for 36,000 potential insured for the third year";
  fit direct. Regime temporal on `CalYear`, but two years give one window (SPLIT-14 not met, so SPLIT-8).
- Siblings and duplicates: `pricing_game_2016_french_fleet` (TBD -> Yes, a fleet portfolio of 2011-2013) and
  `pricing_game_2017_french_mtpl` are other portfolios of the same series ("unknown private insurers", plural; schemas,
  years and ids differ): several datasets, not cuts of one (PROV-7). Whether the benchmark takes more than one game is a
  weighing call. OpenML: none by name.
- Papers and pages: the organisers' two posts; the rules PDF they link was not read.
- Metric: the game scored a market ("the cheapest is chosen, or more complex rules, based on random selection among
  cheap insurers"), which needs the other teams' prices and cannot be computed here; no accuracy metric found, so the
  fallback (`rmse`) (MET-1, MET-11).
- Risks for /add-dataset: the PROV-3 tests first (4 and 6, calibrated on pg16 and pg17); `Numtppd` and `Numtpbi` copy
  the occurrence (drop); exposure in days (`Expdays`) as a feature or weight, the family's insurance-conventions
  question; only two years.
- Priority: gap 0, use case + (the game's pricing task), source + (the organisers' posts and the column documentation),
  shape + (100,000 policies, 15 mixed features, two years), risk - (the generated-covariate doubt, one temporal window).

**Assessment (AI, 2026-10-30):** suggested call for policy question 3 of the zero-inflated review, where Andrej asked
for a call per dataset from its references and the domain's practice instead of one convention for the family (the
shared reasoning is in `curation/inputs/two_regime_zero_triage_summary.md`, "Policy calls of 2026-10-30"); the curator
has the call.
- Target: `Indtppd` + `Indtpbi`, the third-party cost of the policy-year, the cost the game's premium had to cover; drop
  `Numtppd` and `Numtpbi`.
- Exposure: `Expdays` / 365 as a feature.
- Negative amounts: none.
- Metric: the game's market (the cheapest offer wins the policy) needs the other teams' prices; the normalized Gini is
  the stand-in (MET-11), since it scores how well prices rank the risks, which decides who wins which policies in such a
  market.
- First the PROV-3 tests (`AHDS` stays the open concern); one window, 2009 -> 2010 (SPLIT-8).

**Assessment (AI, 2026-10-30):** the PROV-3 tests the curator asked for ("Do the tests needed to decide"), each mark
calibrated against `pricing_game_2016_french_fleet`, `pricing_game_2017_french_mtpl` and `fremtpl2`, which pass every
one. Verdict: the covariates are generated or block-resampled and the claims simulated from them; strong circumstantial
evidence, not proof (EV-6: no generator written down, and no organiser source says either way). Test 6 (the structure
the world shows): driver age and policy age correlate at Spearman 0.05 (pg17 0.36), 10.5% of policies are older than the
driver's years past 18 (pg17 0.04%), 22% of drivers aged 18-20 hold a policy of 10 years or more (pg17 0%); log car
value is unrelated to `Category` and `Type` (eta^2 0.0000 and 0.0001; pg17 value against power rho 0.88); `Type` is
independent of all 12 other covariates (smallest p 0.16) yet the claim rate rises steadily from A to F (14.5% to 18.4%,
p 1e-20), which relabelling or permuting for anonymity cannot produce; 37% of covariate pairs are dependent at p < 1e-6
against 97-100% in the others (median Cramer's V 0.010 against 0.065-0.083); employed and unemployed drivers have the
same age, bonus and car group and differ only in claim rate; 63% of "Housewife" rows are male, the overall share; 13% of
retired drivers are under 50 (pg17 0.1%); policies per subregion follow density almost exactly (rho 0.93). Test 4
(marginals): 27.9% of policies in malus (pg17 0.4%, freMTPL2 1.1%), car values with no catalogue heaping (top 100 values
cover 4% of rows, pg17 30%), smooth lognormal-like and rounded to 5. On the label: the covariates explain 20-21% of the
claim-count Poisson deviance from 2009 to 2010, against 2.5-5% in pg16, pg17 and freMTPL2. Nothing found by test 2 (no
row-counter effect over 1,794 tests) or the house `check_frame` probe. The two-year panel test cannot run: 2009, 2010
and 2011 are disjoint blocks of 50,000 policy numbers. Under PROV-3 the record would go back to `No` with `AHDS`; the
marks sit on the columns that would ship, so no subset fixes it. Word from the organisers that the rows are a real
insurer's would reopen it.

CC (2026-10-30, Andrej): `TBD -> Yes`, priority 3 (the AI screening had `TBD -> 2nd Tier`, priority 3; zero-inflated
screening review page). "Do the tests needed to decide"

CC (2026-10-30, Andrej): `No`, after the AI's PROV-3 tests (Assessment above): "Generated. Type is independent of every
other covariate yet predicts claims, and 27.9% of policies are in malus against 0.4%. Under PROV-3 that means No with
AHDS"

`pg15training` (100,021 rows, 2009-2010) and `pg15pricing` (36,311 policies of 2011, no claims) from the first
pricing game of the French Institute of Actuaries (5 November 2015), listed in CASdatasets as "Datasets from unknown
private insurers". Measured 2026-10-20: 100,000 policies (21 split over two rows), each seen once, exposure in days;
the third-party cost `Indtppd` + `Indtpbi` is exactly 0 for 84.1% (no claim, never negative), and `Numtppd` and
`Numtpbi` copy the occurrence. Schema, years and id format differ from pg17 (`pricing_game_2017_french_mtpl`), so a
separate portfolio.

The covariates fail the generated-data checks. `Poldur` (policy age) is independent of `Age` (r = 0.05): 10,480
policies are older than the driver's years past 18, among them 168 fifteen-year policies of drivers aged 20 or less.
Mean car `Value` is the same for `Category` Small, Medium and Large (16,381-16,542) and for every `Type`, and 12,651 of
the 20,010 "Housewife" rows are male (the levels may be recoded: "most categorical levels have unknown meaning"). Only a
few dependencies exist (Age-Bonus r = -0.22, Age-Adind 0.20, Group1-Value 0.23). That points to simulated or resampled
covariates, against the documentation; the evidence is circumstantial. Untuned LightGBM, 2009 -> 2010: AUC 0.72 for a
claim, R^2 -0.04 on log1p among positives. Word from the organisers (Arthur Charpentier) that the covariates are real
would reopen it. Licence: GPL (>= 2) (CASdatasets). The 2016 game (`pg16trainpol`, `pg16trainclaim`, a fleet
portfolio) is not in the log.

## Reference

CASdatasets (Dutang C., Charpentier A.), `pg15training`, `pg15pricing`, first pricing game of the French Institute of
Actuaries (5 November 2015). https://github.com/dutangc/CASdatasets/blob/master/man/pricingame.Rd

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).

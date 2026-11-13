---
unique_name: bemtpl97
name: beMTPL97
checked_by:
- Myunghwan
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 4
tags:
- Two-Regime Zeros
- 'Samples: One Moment'
- 'Target: Later'
original_source: Github
year: '2019'
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/katrienantonio/PE-pricing-analytics/tree/0b279c433de7c8ef46ebf0a33cd70ebd76d2af9e
- https://github.com/henckr/treeML/tree/2ee8accc6df49168bd865cdf49efa1b7a5c8f4de
- https://dutangc.github.io/CASdatasets/reference/beMTPL97.html
- https://ideas.repec.org/a/taf/sactxx/v2018y2018i8p681-705.html
v2_path: datasets/_dev/tabarena-v0pt2/bemtpl97/dataset.py
source_row: 1045
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: a documented Belgian MTPL portfolio for claim frequency or severity, the insurer's pricing task, and insurance is thin.
- Source: CASdatasets R package (Dutang and Charpentier), `beMTPL97` page: "Unknown insurer", 163,212 unique policyholders, 18 columns (`id`, `expo`, `claim`, `nclaims`, `amount`, `average`, `coverage`, `ageph`, `sex`, `bm`, `power`, `agec`, `fuel`, `use`, `fleet`, `postcode`, `long`, `lat`); the page cites Henckaerts, Antonio, Clijsters and Verbelen (2018), "A data driven binning strategy for the construction of insurance tariff classes", Scandinavian Actuarial Journal 2018(8), as the reference for the data. One table. The `year` 1997 is the portfolio year the name suggests; the page does not state it (first publication of the data is about 2018).
- Use case: an insurer sets the premium of a policy at underwriting from the rating factors (Henckaerts et al.: GAMs on the number of claims and on severity, then GLM tariff classes); fit direct for the frequency target (`nclaims` with `expo` as exposure); regime IID, one row per policyholder, no date column.
- Siblings and duplicates: `fremtpl2` (French MTPL, CASdatasets, a different portfolio, so no duplicate, PROV-7); no other Belgian MTPL record. External collections: CASdatasets; used in Deprez, Verbeke and Verdonck (arXiv 2605.22892, 2026, TabPFN for insurance pricing on two public MTPL sets, which ones not confirmed from the abstract).
- Papers and pages: https://dutangc.github.io/CASdatasets/reference/beMTPL97.html; Henckaerts et al. 2018 (https://ideas.repec.org/a/taf/sactxx/v2018y2018i8p681-705.html, open working paper KU Leuven AFI 583471); CASdatasets manual https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf.
- Metric: none found as one ranked criterion (the abstract of Henckaerts et al. reports model fit of GAMs and GLMs; the full text was not read; the CASdatasets page states none), so the fallback (rmse on the claim count) unless the full text fixes Poisson deviance; a deviance would need `expo` as an input, which ships (MET-1, MET-5).
- Risks for /add-dataset: choose one target (`nclaims` per exposure, or `amount` / `average` for severity on claimants); `claim`, `amount`, `average` are framings of the outcome and must be dropped as features (LEAK, USE-3); `postcode` with `long`/`lat` is spatial and may call for a grouped check; `expo` as weight or offset needs a decision.
- Priority: gap + (insurance thin), use case + (pricing named by the paper), source + (CASdatasets page and a paper), shape + (163k rows, mixed types, spatial), risk - (target and exposure handling to settle).

beMTPL97 from the CASdatasets actuarial collection: a Belgian motor third-party liability portfolio used for claim-frequency (and severity) modelling, a classic real-world tabular insurance task with policyholder/vehicle features and a count/exposure target. It is a genuine, well-known actuarial dataset, representative of tabular ML, typically modelled with an IID split. Considerations: the natural target is claim COUNT with exposure offset (Poisson), which a human should map to a supported problem type (regression, or binary has-claim), and confirm it is not a duplicate of other CASdatasets MTPL tables already in the benchmark.

---

Also see https://arxiv.org/abs/2605.22892 and https://cas.uqam.ca/pub/web/CASdatasets-manual.pdf

**Assessment (AI, 2026-10-23), prior-decision carry-over, not new screening:** The curator confirmed regression on original `nclaims` values 0–5, with RMSE and a random split. `expo` is the recorded time insured: longer coverage gives more opportunity for claims, so retain it as a predictor. Keep the original count target unchanged. Exclude `id` as an identifier and `claim`, `amount` and `average` as same-period outcome information; `nclaims` is the target, never a predictor. Realized exposure can reflect later cancellation; its availability at a new-policy quotation remains a noted limitation of the accepted scenario. The old annualized-frequency/severity alternatives in the main screening do not replace these choices. This carries forward the previous definition and confirmed decisions; it adds no source inspection, model result or fresh verification mark.

CC (2026-10-23, Myunghwan): Accepted for adding: original nclaims 0–5 regression, RMSE and random held-out policyholders from the represented portfolio. Retain expo, the recorded time insured: longer coverage permits more claims. Exclude id and same-period outcome columns claim, amount and average; nclaims is the target. Do not annualize, bin, clip, weight or add row filters. Realized exposure may reflect cancellation and is not verified as quotation-time information; retain the accepted approximate-fit and source-release selection notes. Screening and curator review are complete; current-API qualification remains add-stage work.

**Assessment (AI, 2026-10-23), current add-stage builder evidence:** The pinned CASdatasets and author releases decode to exactly equal 163,212-row tables. All original counts and rows survive; 13 predictors include exposure, nominal postcode and municipality coordinates. Nine IID folds each train on 108,808 and test on 54,404 rows. Current dataset check has no errors or unaccepted warnings; the two retained target warnings follow the existing count-task decision. Leak probes (three capped folds) and the IID hidden-group probe establish no new remedy; neither can verify quotation-time exposure. Current task probes (five full folds) have no flags: LightGBM RMSE 0.364180 versus dummy 0.368248. Bounded train-only local LightGBM/Ridge tuning on all nine full folds scores 0.363999/0.364032 versus dummy 0.367470, each winning 9/9; this is small signal, not the full tuned benchmark suite. Zero-heavy diagnostics are retained separately. The author data commit is verified as 2020-04-30, so year/source now name that release; 1997 remains the observation year and earliest public distribution is unverified. Source-selected high-severity exclusions and exposure/cancellation timing remain qualified limits. Full evidence, draft follow-ups and the claims list are in this delivery; independent panel and curator add review remain pending. Priority 4: gap + (insurance is thin among 133 accepted definitions), use case + (actuarial pricing research), source + (pinned author/CASdatasets agreement), shape + (163,212 rows, 13 mixed predictors), risk - (approximate exposure timing and selected release).

**Assessment (AI, 2026-10-23), builder self-review correction:** Fresh rdata frames use NumPy string column labels. sklearn 1.7.2 ColumnTransformer did not recognize these as feature names when replaying the saved Ridge model; normalizing only the label scalar type to Python str fixes that failure. Field text, source values, original counts, rows and the accepted scientific task remain unchanged. The initial qualification used normal string headers from its verified Parquet input, so its scores are not invalidated by this input-compatibility fix. Model replay and the affected checks are retained in the self-review evidence; this is not the independent panel or final add acceptance.

CC (2026-10-26, Myunghwan): "yes, expected claim count should matter, so poisson deviance (with focusing on small number error) migt be better." Supersede only the earlier RMSE choice with source mean_poisson_deviance for original observed-period nclaims (observed 0-5), predicting expected claim count. Retain all released rows, expo as a predictor, the random policyholder split and id/claim/amount/average exclusions; no annualization, target transformation, weighting, clipping or binning. This favors the source loss's penalty for near-zero expected counts when claims occur, not every small absolute error. This is not a final ship or build decision.

**Assessment (AI, 2026-10-26), correction application pending:** Exact accepted definition/record recovered in a fresh child checkout from pin 1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b; historical checkout identity is retained, not treated as this execution location. Public raw RDA matches the accepted SHA-256. Source mean Poisson deviance has no registry entry at the pin, and Metric.local is explicitly prohibited in the working copy by the pinned add instructions. The intended Metric.source definition and minimal shared-registry candidate are retained in the owned warehouse for direct scorer-domain checks. Shared code is not edited in this dataset leaf. The executable fallback and generated README remain explicitly historical RMSE, not an applied substitute for the curator's decision. Application and affected qualification remain incomplete until the bounded library registration/helper follow-up is resolved. Historical builder/auditor reports and scores are unchanged; negative old predictions are not rescored. No independent role, final review, build or publication is claimed.

**Assessment (AI, 2026-10-26), bounded affected qualification:** Original all-row count target, 13 predictors and nine folds remain unchanged. Fixed Poisson diagnostics use training-only numeric scaling/categorical encoding, strictly positive finite expected-count predictions, no clipping, weighting, offsets, target transforms or HPO. Mean Poisson deviance: train-mean dummy 0.551734632; poisson_linear 0.547592694 (9/9 wins), poisson_lightgbm 0.528534431 (9/9 wins), poisson_forest 0.529093723 (9/9 wins), bm_only_poisson 0.549323188 (9/9 wins), expo_only_poisson 0.551113166 (9/9 wins). Every full-fold candidate score agrees with the source log-likelihood formula. These are fresh bounded diagnostics through an isolated supported scorer override, not old tuned scores, a full tuned benchmark, commercial pricing validation or completed registry integration. Official task probes hardcode RMSE and clip regression outputs; their flags were not relabelled. Neutral full-row blind inputs now include exact dtype/category restoration and the current scoring contract; no blind role ran. Shared-registry absence and zero-mean pseudo-prediction helper failure remain precise implementation blockers; application is pending, and executable RMSE/generated README are explicitly historical. Remaining independent synthesis and final human review stay separate.

**Assessment (AI, 2026-10-26), final same-worker critical corrections:** Clarify expected count as prediction and original nclaims as labels. Attribute the strictly positive finite mean contract to the AI/scikit scorer implementation protocol, not an extra verbatim curator choice; the human selected source deviance and expected observed-period counts. Replace the stale no-current-qualification sentence with completed bounded candidate diagnostics and still-blocked official integration/application. Narrow source-selection wording: large-claim preprocessing is documented, but excluded identities and removal of complete policies are unverified. This corrects an overstatement already identified in accepted domain evidence; it changes no source row, predictor, split, fit label or result. Saved-artifact checks of all45 fixed models confirm declared settings, train-only scaler/encoder contracts and solver iteration bounds without refitting. C028/source-default and domain/precedent metric interpretations require scoped independent reconciliation during the independent review; changed neutral scoring text needs independent blind handling there. Preserve remaining panel/mediator/editor and curator review gates. The historical named-versus-executed checkout equivalence remains unproven and requires controller provenance reconciliation before final integration; this recovery binds only exact admitted bytes to the fresh owned checkout. (superseded 2026-11-04: the release's 19 removed policies are counted in Review issue 2)

**Assessment (AI, 2026-10-26), direct remaining-test follow-up:** Applied the already approved source mean_poisson_deviance. Registered the sklearn scorer and corrected only its synthetic computability inputs; actual invalid model means still raise. Official dataset check now has zero errors/zero open warnings, with the two previously accepted count-shape warnings retained. Every source row, original nclaims value and all 13 predictors (including expo) are unchanged; id/claim/amount/average remain excluded. The current typed frame equals the prior executable and all nine original fold arrays match exactly. All 54 saved fixed-model scores reproduce through the integrated source scorer and independent Poisson likelihood; no refits or prediction clipping. LightGBM deviance0.528534 versus dummy0.551735 (4.20% same-fold skill, wins9/9); forest0.529094, linear0.547593. Independent focused claim/domain/precedent review found no new contradiction; existing approximate-fit, source-selection, identity and licence limitations remain disclosed. No final ship/build/commit approval inferred. Priority 4: gap + (insurance), use case + (risk differentiation), source + (pinned author code and public table), shape + (163k mixed-type records), risk - (no demonstrated new defect; retained timing/selection limits).

**CC (2026-10-28, Myunghwan):** "ship all". Approved this dataset for shipping in the five-dataset final added-dataset review (beMTPL97, Eucalyptus, Tanzania tourism, CPS88 wages and OSSL), on the exact presented definition with previously settled task choices and disclosed limitations retained. This is scientific acceptance for a separately requested build; it does not authorize build, commit or publication.

**Assessment (AI, 2026-10-28):** The independent consistency check supports applying this overall verdict without another task choice. Existing local curator dispositions remain distinct from source verification or shared-rule amendments. No definition, scorer, data, fold or warning acceptance was changed by this final verdict.

**Maintenance (AI, 2026-10-29):** Publication-privacy cleanup removes acquisition/process details from descriptive metadata. Native format-2 rebuild `01a18ad7-0bb6-7938-bc7e-98a4b50a8804` verifies on reload and reproduces from its single traced raw input. Every data row, target, scoring semantics and all nine folds exactly match the previous build; only descriptive metadata changes the checksum. Prior containers and scientific decisions are preserved.

CC (2026-11-04, Lennart): `coverage` is ordered TPL < TPL+ < TPL++ (CLEAN-14); the notes are cut to the decisions; beMTPL97 and freMTPL2 are treated alike, shipped IID with the `ForcedIIDFromTemporal` tag (SPLIT-8): "do (a) and ship both". The Poisson scorer floors predicted means at machine epsilon ("I also argue for a floor in the scorer"). The fit stays approximate while the consistency check is open (Review issue 1). (superseded 2026-11-04: the floor is `min_prediction=1e-6`, the CC below)

**Assessment (AI, 2026-11-04):** the metric is the source's: Henckaerts et al. (arXiv:1904.10890v3, Sec. 3.2 Eq. 5, Algorithm 3) tune and test by the mean Poisson deviance of the claim count against exposure times frequency, unweighted; their treeML code and the freMTPL2 case study compute the same. Exposure is an offset, not a weight. (superseded 2026-11-04: the second-pass panel's issue 1 asks whether realised exposure is an offset or a leak; open)

CC (2026-11-04, Lennart): the fit stays approximate under the `ForcedIIDFromTemporal` tag, as freMTPL2 and the 20 other forced-IID definitions ("(b)"). The Poisson scorer clips predicted means at a stated floor, `min_prediction=1e-6`, two orders below the smallest plausible mean ("I think being worse than the dummy only due to clipping is misguided, in pratice we would also clip to a reasonable number"); MET-13 says so. (superseded 2026-11-04: 18 other definitions carry `ForcedIIDFromTemporal` on 2026-11-04, ai4d included, not 20)

**Assessment (AI, 2026-11-04):** review panel (none): no panel ran for this dataset; its issues came from the light static review of the PR #33 page and the research behind each mark, and all are settled. (superseded 2026-11-04: the full review panel ran in a second pass)

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes; disputed: EV-7 (the rebuild as a separate gate); on LEAK-10 the advocate withdrew the amendment, so all sides recommend making `expo` a scoring column, as the source uses it, and keeping it as a feature under a LEAK-10 amendment stays open to the curator (for fremtpl2 too); for the curator: issues 1-3. Priority 3: gap +, use case -, source +, shape +, risk - (gap: insurance is thin among the accepted definitions; use case: the source names the insurer's pricing, but the fit is approximate, forced IID and realized exposure; risk: issue 1, a likely LEAK-10 leak through `expo`, 16-18% of the model's skill).

**Assessment (AI, 2026-11-04):** text corrections of the second-pass panel applied (Lennart's go-ahead on the review page): the stale lines above carry correction notes. No data, split, feature or metric change.

CC (2026-11-05, Lennart): issue 2, (b): ship all 163,231 policies of the first public copy (PROV-8), data/P&Cdata.txt of katrienantonio/PE-pricing-analytics commit 0b279c433de7c8ef46ebf0a33cd70ebd76d2af9e (26 September 2019), instead of the 2020 release's 163,212, which leaves out the 19 policies whose average claim cost exceeds EUR 81,000. Re-verified on 2026-11-05: the 2019 copy minus exactly those 19 rows equals the release row by row in the same order, every value equal to the text file's 15 digits; the 19 hold 21 claims (17 with one claim, 2 with two). The restored rows remove the selection by claim cost, so no `Selection Bias` marker is needed for it. The 2019 repository states no licence; CASdatasets declares GPL (>= 2) for the release. LightGBM-Poisson mean deviance (untuned, 9 folds, `expo` free): 0.5274 against the training mean's 0.5517 before, 0.5279 against 0.5520 after both of today's changes; the gain of a free `expo` over an offset is 0.0039 (was 0.0040), 16% of the skill either way.

CC (2026-11-05, Lennart): issue 3, (a): `sex` leaves the features. The actor is an EU insurer pricing today, and the Test-Achats ruling (CJEU C-236/09, 1 March 2011, in force for new contracts from 21 December 2012) bars sex as a rating factor: "We make this special case here as we would try to understand how good such models would be in the current world, and they would not be able to use sex". The 1997 portfolio stays the data, priced as an insurer would today; the fit stays approximate. Sex carried 0.0004 mean Poisson deviance (0.0002 to 0.0007 per fold, better in 9 of 9 folds, 1.6% of the skill). The tension (a factor known at the prediction point that the actor may no longer use) is a row in principles.md; home_credit_default_risk (`CODE_GENDER`) and credit_card_clients_default (`SEX`) keep sex, not reviewed yet. This supersedes the note "sex stays by curator choice, for research on a 1997 tariff".

CC (2026-11-05, Lennart): issue 1 (exposure) is parked, with fremtpl2's issue 6 and both declared metrics, until the zero-inflated stack (PRs #44-#47) is merged.

**Assessment (AI, 2026-11-05):** the parked exposure question is GitHub issue #51 (https://github.com/TabArena/data-foundry/issues/51).

CC (2026-11-06, Lennart): issue 1 resolved as the rate with a sample weight (option A of #51): the target is nclaims_per_year = nclaims / expo; expo is the weight scoring column, the metric's `weight` input and the task's `sample_weight`, never a feature (LEAK-41, MET-14, MET-15, adopted 2026-11-06); the floor is 1e-4 claims per year on the predicted rate (MET-13). The weighted rate deviance equals the source's count deviance of the expected count expo x rate (Henckaerts et al., Eq. 5) times n/sum(expo) of the scored rows (1.123 to 1.125 on the shipped folds). Supersedes Myunghwan's calls of 2026-10-23 ("Retain expo ... Do not annualize, bin, clip, weight") and 2026-10-26 (expo as a predictor), and the floor of 2026-11-04 (1e-6 on the expected count): the conditional measurement came later (+0.0043, 17% of the skill; never better at quotation), and the source itself scores with an offset. The built container 01a18ad7 is superseded (not deleted).

**Assessment (AI, 2026-11-06):** review panel (full, re-review under LEAK-41, MET-14 to MET-16): ship after changes, to the notes only (data, target, weight, metric, floor and split stay as defined); disputed: whether this definition says that test-row `expo` belongs to the scorer alone (the critic) or one house remedy covers every weighted table (the advocate), moved by the mediator to cross-dataset item X1; for the curator: no issue on this dataset (cross-dataset items X1 and X2, working copy REVIEW.md, "From PR #47"). On the declared metric the honest model scores 0.5979 against the training mean's 0.6193 (3.46%, better on 9 of 9 folds); the task probe's `no_signal` reads the RMSE skill (R^2 0.015). The priority's factor "risk -: issue 1" of 2026-11-04 is resolved: `expo` is the weight, never a feature.

**Assessment (AI, 2026-11-06):** the panel's text changes are in the definition's notes, with no data, split, feature or metric change: LEAK-41's report on the declared metric (`expo` as a feature gains +0.0047 under the weighted Poisson fit and +0.0051 under weighted L2, 9 folds; a fit on `expo` alone scores 0.6122, between the training mean and the honest model, and a scaled 1/`expo` scores at the training mean), the copy counts with `expo` out (397 extra exact rows, 88 conflicting profiles), the part-year pairs that may be one re-issued policy (57 to 176; both rows claim in at most 1.1%) and postcode's distinguishing fact (long and lat give each municipality's place). The +0.0043 (17%) of the CC of 2026-11-06 above is a gain on the count deviance of the old task (the exposure study's +0.00425 with early stopping, 9 folds), the scale of the 0.0039 of 2026-11-05, not the rate scale; on the weighted rate deviance the same comparison gains +0.0048. The AI line of 2026-11-04 "Exposure is an offset, not a weight" is superseded: `expo` is the weight, and the weighted rate deviance ranks models as the source's offset model does.

**Assessment (AI, 2026-11-06):** priority 4, up from 3 (selection.md, Priority): the risk factor behind 3 (issue 1, the exposure) is resolved; a gap in the benchmark (insurance) +, a good shape (163,231 units, 11 features) +, a strong source (Henckaerts et al., the treeML code) +; the fit stays approximate.

CC (2026-11-08, Lennart): the declared metric (`mean_poisson_deviance`) is checked, as declared; the record ships, with no open issue on the PR #47 review board.

CC (2026-11-08, Lennart): tagged `Two-Regime Zeros`, as fremtpl2 (its issue 10, reply (c)): the tag describes the target's distribution, not the task's model, and 88.8% of the policies have no claim (144,936 of 163,212) ("Tag bemtpl97 too; the tag should when the target has the kind of distribution indepdet of just the task as far as I understand").

## Review

**Outcome:** added. The AI recommends shipping it. The re-review of 2026-11-06 under the exposure rules (LEAK-41,
MET-14 to MET-16), held after issue 1 was resolved, asked only for text in the notes (mediator: ship after changes),
and that text is in. The first public copy (2019) of a Belgian motor-insurance portfolio of 1997: the claims per year
insured of 163,231 policyholders, predicted at the quote from 11 rating factors, each policyholder weighted by its share
of 1997 insured (`expo`). Validity: USE-1, USE-3 and USE-5 hold (settled on 2026-11-05); LEAK-41 was triggered by
`expo` and is fixed (the weight scoring column and `sample_weight`, never a feature), and the notes now give its report:
as a feature `expo` would gain +0.0047 under the weighted Poisson fit and +0.0051 under weighted L2 (9 folds), and a fit
on `expo` alone scores 0.6122, between the training mean's 0.6193 and the honest model's 0.5979; probe 22 finds that
the features predict `expo` at R² 0.032 under its 50,000-row cap (0.055 on full folds, claim audit), through factors
known at the start; LEAK-10 holds (`bm` is the level at the start); LEAK-16 holds (copies give no shortcut); SPLIT-8
holds, its cost disclosed (`ForcedIIDFromTemporal`, fit approximate); SPLIT-29 and SPLIT-30 find nothing (grouping by
postcode lowers the skill by 0.04 to 0.15 percentage points, and the ranking holds). Value: TP-2, a small real signal:
on the declared metric the honest model scores 0.5979 against the training mean's 0.6193, a skill of 3.46%
(3.27-3.68%), better on 9 of 9 folds; the task probe's `no_signal` flag reads the RMSE skill (R² 0.015), not this
metric (EV-3); MET-11 holds (the source's Eq. 5 score times n/sum(expo), 1.1229-1.1254 per fold, so models rank as by
the source's metric); MET-13, MET-14 and MET-15 hold (the floor of 1e-4 claims per year never binds); MET-16 does not
apply (`expo` is an exposure, not a survey weight). Quality: CLEAN-14 holds (`postcode` stays nominal, since `long` and
`lat` give each municipality's location) and CLEAN-16 holds. Weighed: nothing decides the verdict. Left for Lennart: no
issue here; the panel's two open questions concern weighted tables in general and are the cross-dataset items X1 and X2
(working copy REVIEW.md, 'From PR #47'). Like every container with a `sample_weight`, it enters no run before the
collection's training-weight gate (`BENCHMARK_CHANGES_TODO.md`, "Training weights", "The gate").

**Main points:** No open issue, so it ships by default: issues 1-3 are resolved, and the re-review of 2026-11-06 adds
none on this dataset (its two questions are the cross-dataset items X1 and X2).

**Record judgment:** valid; a documented Belgian motor-insurance portfolio and the source's own frequency task, now the
claims per year insured weighted by `expo`. The CC of 2026-11-06 names the calls it supersedes (Myunghwan's of
2026-10-23 and 2026-10-26, the floor of 2026-11-04). Three AI lines of 2026-11-06 follow it: the panel's assessment;
the text changes, which mark the 2026-11-04 line "Exposure is an offset, not a weight" as superseded; and the priority,
raised from 3 to 4 because its risk factor (issue 1) is resolved. The scores in the CCs of 2026-11-05 and 2026-11-06
are on the count target shipped until then. The CC's +0.0043 is the exposure study's gain on the count deviance
(+0.00425, fitted with early stopping), not on the rate scale as the mediator and the claim auditor read it. On the
weighted rate deviance the same comparison gives +0.0048. A dated AI line next to the CC in the notes says so.

**Issues for Lennart:**

1. **Make `expo` a scoring column instead of a feature?**

   * **Problem:**
     - `expo` is the share of 1997 a policy was insured, and the source gives two reasons for less than a full year:
       the policyholder "started the policy in the course of the year" (known when the premium is quoted) or
       "surrendered the policy before the end of the year" (often after a claim, so known only later)
       ([arXiv:1904.10890v3](https://arxiv.org/pdf/1904.10890v3), Sec. 4.1).
     - The source uses exposure only in proportion, the expected count being `expo` times the annual frequency with
       the slope fixed at 1 (an offset; Eq. 5 and
       [treeML.Rmd L641-657](https://github.com/henckr/treeML/blob/2ee8accc6df49168bd865cdf49efa1b7a5c8f4de/treeML.Rmd#L641-L657)),
       but here `expo` is a plain feature, so a model can learn that short policies claim more per insured day.
     - An actuary cannot use that, because at quotation the exposure is set to a full year, and without dates the two
       reasons cannot be told apart.
   * **Background:** A value from the outcome's period stays only when the data shows it does not move with the
     outcome given the covariates[^leak10]; the narrower rule for anonymised fields does not apply here[^leak38].
     Because that rule is a Must, keeping `expo` as a feature needs an amendment of it for exposure as the denominator
     of a count target; an exception is not enough. A scoring column is a column the scorer reads and the model never
     sees. Under it a model does not see `expo` while it trains unless the harness passes it; trained on `nclaims`
     alone, it learns the count per observed period, not the annual frequency the scorer multiplies by `expo`. There
     are two ways to pass it, and they rank every model the same (mediator): (i) the count target with `expo` as an
     offset at fit time, for models that take one; (ii) the target `nclaims / expo` with `expo` as the sample weight,
     for any model that takes weights. Form (ii) changes the shipped target.
   * **Experiments:** Four agents, independently: per insured year, policies insured up to a quarter of the year claim
     0.292 times, full-year ones 0.126. Given all other features and a proportional offset, part-year policies claim
     about 1.4 times what is expected, and the fitted coefficient on log(`expo`), when it is not fixed, is 0.45-0.54; 1
     would mean claims scale exactly with insured time. New business does not explain it: part-year rows at the entry
     bonus-malus level (bm = 11) show 1.39 times, the rest 1.41; existing policyholders (bm other than 11) reach 2.13
     at `expo` up to 0.1.

     | LightGBM-Poisson, 9 folds (claim auditor) | mean deviance | skill over the training mean |
     |---|---|---|
     | `expo` as a free feature (shipped) | 0.5274 | 4.4% |
     | `expo` as an offset only | 0.5314 | 3.7% |
     | no `expo` | 0.5369 | 2.7% |
     | training mean | 0.5517 | 0 |

     The free use gains 0.0036-0.0041 over the offset, 16-18% of the skill; a random column moves the score by
     0.0001-0.0004.
   * **Consistency:** The keep of 2026-10-23 and 2026-10-26 (Myunghwan) and 2026-11-04 (Lennart) rested on the fit on
     log(`expo`) alone (0.5470 against 0.5517), which measures only the proportional part; the conditional test is the
     new fact. fremtpl2 shows the same mechanism (slope 0.62; deviance 0.2428 with the offset, 0.2407 free) and keeps
     Exposure "as in bemtpl97".
   * **Panel:** The mediator and the critic recommend the scoring column, and so does the advocate after its rebuttal.
   * **Unknown:** Policy start and end dates would settle the mechanism; no copy has them.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as a feature (implemented) | `expo` is one of the 13 features; the note says "kept on purpose" and now gives both causes and the measured gain; the leak rule is amended for exposure as the denominator of a count target | no change to the features or the metric | a model can use that short policies claim more per insured day, 16-18% of the skill; needs an amendment of a Must, an exception is not enough |
     | B | Scoring column | `expo` leaves the features; the model predicts the annual frequency, and the scorer computes the mean Poisson deviance of `nclaims` against `expo` times the prediction | under form (i) target, rows and metric stay the source's; the proportional part of `expo` stays | it also removes the part from mid-year starts (bm = 11 at `expo` up to 0.1: 3.36 times expected); the scorer needs an exposure input with tests; form (ii) changes the shipped target |

   * **Recommendation:** B, the scoring column (mediator, critic, and the advocate after its rebuttal).
     **Decision:** B (scoring column) or A (keep as a feature under an amendment of the leak rule), for bemtpl97 and
     fremtpl2 together?

   **Notes for the AI:** the decision goes into a CC line that names LEAK-10, for bemtpl97 and fremtpl2 together. On
   B, `_poisson_deviance` in `src/data_foundry/v2/metrics.py` needs an exposure input with tests, and Claude picks the
   form ((i) offset at fit time, or (ii) target `nclaims / expo` with `expo` as sample weight) together with the metric
   change. On A, write the LEAK-10 amendment for exposure as the denominator of a count target.

   [^leak10]: **LEAK-10** (Must): a value from the outcome's period stays only when the data shows it does not move
     with the outcome given the covariates (account_debt_south_africa, 2026-10-26); late values that cannot be located
     row by row go when they may carry a gain (distribution_transformers_at_cauca_department).
   [^leak38]: **LEAK-38** does not apply: `expo` is a named field, and comparing part-year claims with what the other
     features and proportional exposure predict measured the mechanism.

   **Lennart (2026-11-05, discuss):** This is related to the discussion for fremtpl2, compare it and check

   **Answer (AI, 2026-11-05):** It is the same question, with the same facts, so the two should be decided together; see
   fremtpl2 issue 6's answer of today. Here part-year policies claim about 1.4 times what a proportional offset expects,
   and a free `expo` gains 0.0036-0.0041 mean deviance over the offset (16-18% of the skill); in fremtpl2 the free
   `Exposure` gains 0.0033-0.0047 (21-30% of the gain after today's blanking). Neither has dates that tell a mid-year
   start from a cancellation. The open PRs #44 to #47 do not settle it: they add no exposure weight to the Poisson
   deviance and no training-weight declaration, and #44 keeps an unlocated cut with a measured note. So the choice is
   the same in both:
   - (a) A for both: `expo` / `Exposure` becomes a weight scoring column, the target the annual frequency, the metric a
     weighted Poisson deviance, and the benchmark passes the exposure as `sample_weight` (new code in the API, the
     container and the benchmark);
   - (b) B for both: the feature stays, with an amendment of LEAK-10 for exposure as a denominator and the measured size in
     the note.

   Your answer here also answers fremtpl2 issue 6.

   **Lennart (2026-11-05, discuss):** see my comment for fremtpl on this

   **Deferred (2026-11-05):** parked with fremtpl2 issue 6 until the zero-inflated stack (PRs #44-#47) is merged; [#51](https://github.com/TabArena/data-foundry/issues/51)
   holds the context. The declared metric waits with it.

   **Resolved (2026-11-06, Lennart):** B, as the rate with a sample weight (option A of
   [#51](https://github.com/TabArena/data-foundry/issues/51), the exposure study of 2026-11-05). The target is
   `nclaims_per_year` = `nclaims` / `expo`; `expo` is the weight scoring column, the `weight` input of
   `mean_poisson_deviance` and the task's `sample_weight`, and never a feature (LEAK-41, MET-14, MET-15, adopted the same
   day); the floor is 1e-4 claims per year (MET-13). This is the source's offset model (Henckaerts et al., Eq. 5): on
   every shipped fold the weighted rate deviance equals the count deviance of the same predictions times n/sum(expo) of
   the scored rows (1.123 to 1.125). Supersedes Myunghwan's calls of 2026-10-23 and 2026-10-26 (keep `expo` as a
   predictor; do not weight) and the floor of 2026-11-04 (1e-6 on the expected count): the conditional measurement came
   later (+0.0043, 17% of the skill; never better at quotation), and the source itself scores with an offset. The
   low-cardinality acceptance goes (the rate has 559 values); the built container `01a18ad7` is superseded.
   `dataset check`: 0 errors, 0 warnings.

2. **Ship the 163,212 released rows or all 163,231?**

   * **Problem:**
     - The release leaves out the 19 policies whose average claim cost exceeds EUR 81,000, now verified row by row
       against the first public copy of 2019 (all 19 are claimants, 21 claims, 0.1% of all claims; every other row is
       identical and in the same order).
     - A cut by claim cost depends on the outcome, so the test folds miss 19 heavy claimants, too few to matter for a
       frequency task (the domain practitioner: negligible).
     - Whether to keep the cut or undo it is a weighing call[^use5].
   * **Panel:** The mediator, the advocate and the critic agree on keeping 163,212.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep 163,212 rows (implemented) | the release's rows; the note now states the selection as a fact | these are the rows the boosting paper evaluates on (Sec. 4.1); the cut is the source's own preprocessing ("exclusion of very large claims") | the test folds miss 19 heavy claimants |
     | B | Restore all 163,231 | download the 2019 file and ship 163,231 rows | the unselected 2019 copy exists, so the cut can be undone | a new download; rows that differ from the ones the metric's paper used |

   * **Recommendation:** A, keep 163,212 (mediator, advocate and critic agree). **Decision:** A (keep) or B (restore)?

   [^use5]: **USE-5** (Weigh, as the panel weighs it) and **USE-8** (a selection alone does not change the fit).

   **Lennart (2026-11-05, ok):** If this is the official verison, we can stay with it for now instead of moving on

   **Answer (AI, 2026-11-05):** Partly, and I corrected my first reply. The 163,212 rows are what the source's GitHub
   release ships and what its boosting paper evaluates on (Sec. 4.1), with "exclusion of very large claims" as its own
   preprocessing; but the first publication (PROV-8) is the 2019 copy with all 163,231 rows, so the official version
   by our rule is the unselected one. Keeping the release's rows (A) is still a weighing call, and since the cut is by
   claim cost, the fit rule as amended on 2026-10-27 asks `fit_reason` to name it and the record to carry `Selection
   Bias`, as lt and tunisian do.
   - (a) A, with the selection named in `fit_reason` and the `Selection Bias` marker;
   - (b) B, restore the 2019 rows.

   **Lennart (2026-11-05, ok):** Reply (b): B, restore the 2019 rows

   **Resolved (2026-11-05, Lennart):** (b). The 2019 copy (katrienantonio/PE-pricing-analytics, commit of 2019-09-26,
   SHA-256 pinned) ships all 163,231 rows; minus its 19 rows with an average claim above EUR 81,000 it equals the
   release row by row, so the selection by claim cost is gone and no `Selection Bias` marker is needed. The 2019
   repository states no licence (a note). LightGBM-Poisson mean deviance 0.5274 to 0.5279; the free `expo` still gains
   0.0039 over the offset.

3. **Confirm that `sex` stays?**

   * **Problem:**
     - The notes say "sex stays by curator choice, for research on a 1997 tariff", but no curator line in the record
       states that choice; the 2026-10-23 line accepts the 13 predictors without naming it.
     - Gender-based insurance pricing is banned in the EU since 21 December 2012 (CJEU C-236/09, Test-Achats), so a
       tariff today would not use it.
     - The ethics rule is not triggered: no subject or creator objects to this use[^sel1].
   * **Effect on the task:** A model may use a rating factor that a tariff written today cannot.
   * **Consistency:** No other rule covers protected attributes, and no precedent was found.
   * **Unknown:** Its share of the score was not measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `sex` (implemented) | `sex` stays a nominal feature, disclosed as a 1997 rating factor | a rating factor of the 1997 tariff the data describes; the domain practitioner: fine if disclosed | a tariff written today cannot use it |
     | B | Drop it | `sex` leaves the features | no factor a tariff written today cannot use | one fewer rating factor of the 1997 tariff the data describes |

   * **Recommendation:** A, keep it, disclosed as a 1997 rating factor (the domain practitioner: fine if disclosed).
     **Decision:** A (keep) or B (drop)?

   **Notes for the AI:** on A, write Lennart's reason as a CC line.

   [^sel1]: **SEL-1** (ethics, Must): a task with ethical concerns is out, including data whose subjects or creators
     ask that it not be used for ML.

   **Lennart (2026-11-05, change):** Option B: Drop it. I think it is valid to remove it from the data to have models
   that more acucratly track what would be used today

   **Consistency check (AI, 2026-11-05):** dropping `sex` departs from USE-6 (Must: what is known at the prediction
   point is a legitimate input) while the actor prices the 1997 tariff the notes describe, from the kept `CODE_GENDER`
   (home_credit_default_risk) and `SEX` (credit_card_clients_default), and from SEL-18 of today, where "today one would
   use other features" is a note. No rule covers protected attributes. What sets it apart?
   - (a) the actor is an EU insurer pricing today, and the Test-Achats ruling (2012) bars sex as a rating factor:
     `use_case` and `known` move to today's tariff, with a Tensions row;
   - (b) keep it, as the panel said;
   - (c) (a), and review the credit datasets that keep sex too;
   - (d) a new rule on protected attributes.

   Give the letter in the note; nothing is applied until then.

   **Lennart (2026-11-05, change):** Reply (a): the actor is an EU insurer pricing today, and the Test-Achats ruling
   (2012) bars sex as a rating factor: use_… Option B: Drop it. We make this special case here as we would try to
   understand how good such models would be in the current world, and they would not be able to use sex

   **Resolved (2026-11-05, Lennart):** (a). The actor is an EU insurer pricing today; since 21 December 2012 EU law bars
   sex as a rating factor (CJEU C-236/09, Test-Achats), so `sex` leaves the features (it carried 0.00038 deviance, 1.6%
   of the skill). `use_case`, `known` and `fit_reason` are rewritten; a Tensions row in principles.md (the actor's legal
   constraint today wins when the use case is today's pricing; home_credit_default_risk and credit_card_clients_default
   keep sex, not reviewed yet).

**Review panel:** ship after changes (mediator). Tier full, re-review of 2026-11-06 under LEAK-41, MET-14 to MET-16,
after issue 1 was resolved as the rate weighted by `expo`. Claim audit: 31 claims, 20 hold (2 with a caveat), 2 refuted
(LEAK-41's report and the copy counts, both now in the notes), 4 stale or on mixed scales (now named or superseded),
the `no_signal` flag a reading of the wrong scale, 4 untested (the shuffle seed, the sex ruling settled on 2026-11-05,
the licence and the paper's text; its Sec. 4.1 quote on exposure was checked after the audit). Blind review: include
with changes; its main concern, the metric, asks for the exposure-weighted Poisson deviance that ships (its task sheet
does not name the metric). Task gamer: only test-row `expo`, which a participant can read from the scoring columns, beats the noise
(+0.0052 used as a feature, against 0.00005 of noise; cross-dataset item X1). Agreed: the target, the weight, the
metric and its floor, the split, the signal and every text change (made). Disputed: whether this definition should say
that test-row `expo` is the scorer's alone (the critic) or one house remedy should cover every weighted table (the
advocate), moved to cross-dataset item X1; the mediator settled the rest (`postcode` stays nominal with the fact that
sets it apart written down; the clause on possibly re-issued pairs goes in).

<details><summary>Mediator</summary>

**Mediator report: bemtpl97 (exposure re-review, 2026-11-06, full tier)**

I ran no new experiment because no fact is in dispute. Both sides accept every measurement. The two places where the reports differ (which fit is "the worse"; the critic's "15% of the skill") are settled from the reports' own numbers below.

**1. Judgment record**

Verdict: ship after changes. The changes are to the notes only: the data, target, weight, metric, floor and split stay as defined. The rebuild happens when the curator asks for it.

Validity:
- USE-1, USE-3 and USE-5 hold (settled on 2026-11-05, not reopened).
- LEAK-41 was triggered by `expo` and is fixed: `expo` is the weight scoring column and `sample_weight`, and it is never a feature. Its reporting clause is missing from the text, which is an unmet Must. It is fixed now with a sentence of numbers that are already measured (change 1).
- LEAK-10 holds: bm is the level at the start (5,215 claimants at bm 0).
- LEAK-16 holds: copies give no shortcut, and the possibly re-issued pairs share no outcomes.
- SPLIT-8 holds, and its cost is disclosed. SPLIT-29 and SPLIT-30 have no hit (grouping by postcode costs 0.0004-0.0015, and the ranking holds).

Value:
- TP-2: a small real signal. The deviance skill is 3.46% (3.27-3.68%), better than the constant on 9 of 9 folds. The probe's no_signal flag reads the RMSE skill (R² 0.015); read that way under EV-3, the flag is not a finding.
- MET-11 (origin source): the metric is exactly the source's Eq. 5 times n/sum(expo), a factor of 1.1229-1.1254.
- MET-13: the floor never binds.
- MET-14 and MET-15 hold.

Quality:
- CLEAN-14: postcode stays a nominal category. The fact that sets it apart is written down: long and lat give each postcode's location, as in the three nominal precedents (all of which have coordinates).
- CLEAN-16 holds.

Weighed: nothing decides the verdict.

For the curator:
- X1, cross-dataset (P4, LEAK-41): participants can read the test-row weight from the scoring columns.
- X2, cross-dataset (P4, LEAK-41): what "1/weight alone" means under a deviance.
- Issue 3, low: the record's priority now that the risk factor is resolved.

**2. Agreed facts**

Target, weight and metric:
- The target is `nclaims_per_year` = nclaims / expo. It rebuilds the integer counts 0-5 exactly and has 559 distinct values.
- `expo` is not in `feature_columns`. `sample_weight` is `expo`, and the metric input is {weight: expo}.
- The weighted rate deviance equals the source's count deviance (treeML.Rmd L641-657) times n/sum(expo). The factor is 1.1229-1.1254 and the identity is exact on all 9 folds, so models rank exactly as under the source's metric.
- Floor 1e-4:
  - The smallest honest predicted rate is 0.008-0.045.
  - 0 of 489,693 test predictions fall below 1e-3, and 0.0% sit at the floor in every probe family.
  - NaN and inf raise an error.
- Weighting:
  - Unweighted, the mean rate is 1.13 times the portfolio rate (0.157 against 0.139).
  - Ignoring the weight costs 0.0066-0.0114 of deviance.
  - Actual/expected is 0.89-0.94 without the weight and 0.98-1.01 with it.

Exposure as a leak, on the declared metric over 9 folds:
- `expo` as a feature gains +0.0047 (SD 0.0006) under the weighted Poisson fit and +0.0051 (SD 0.0007) under weighted L2.
- Probe 22, with its 50k cap, gives +0.0040 (SD 0.0008) under Poisson and +0.0035 (SD 0.0027) under L2.
- Which fit gains more flips between the two runs, and the difference is within one SD. Both gains are positive, so "decide on the worse" excludes `expo` either way.
- The weight alone, fitted (a tree on expo, which is the same as on 1/expo): 0.6122 against the training mean's 0.6193 and the honest model's 0.5979. Per fold it beats the constant by 0.0051-0.0079.
- A scaled k/expo used directly as the prediction scores no better than the constant (0.6223 against 0.6233).
- The features predict expo at R² 0.032 under the 50k cap and 0.055 on full folds (Spearman 0.24). No feature's gain runs through expo above noise under either fit.

Part-year rows:
- Part-year policies claim at actual/expected 1.42 (1.31-1.48) against 0.93 for full years.
- Excess starts claim 0.094 a year, full years 0.126.
- At the quote, a model with expo as a feature is worse than the honest model on 9 of 9 folds, and its claims come in at 1.08 times its price.

Signal:
- The honest model scores 0.5979 against 0.6193 (3.46%, 9/9 folds). The probe's own numbers give 3.1% (0.6004 against 0.6199).
- The top predicted decile claims 3.4-3.8 times the bottom one, and the ordered Lorenz Gini is 0.207-0.212.

Split:
- Train and test match on expo on every fold: mean 0.889-0.891, KS p-values 0.67-1.00.
- On full-year test rows only, the ranking is the same as on all rows.
- Copies:
  - On the shipped basis there are 397 extra exact rows and 88 conflicting profiles (177 rows). The notes' "50 rows" were 50 profiles (100 rows).
  - 0.4% of test rows have a copy in train.
  - Between 57 (strict) and 176 (loose) pairs of part-year rows have exposures that sum to one year. That is 15.1% of two-row profile copies against 2.8% for random same-postcode pairs. Both rows of a pair claim in 0.0% (strict) to 1.1% (loose) of pairs.

Postcode:
- 583 levels, with long and lat as its centroid, one pair per postcode.
- Untuned LightGBM with the native category overfits it: skill 0.0342 without postcode against 0.0063 with it.
- This is context only. Types are decided from meaning, not from model runs (EV-4).

Two corrections of fact:
- The critic's "about 15% of the honest skill" for the gamer's 0.0052 does not reproduce. Against the honest gain over the constant (about 0.020-0.021) it is about a quarter (24-26%).
- The blind reviewer's "19 policies with two rows" is a misreading. 163,231 − 163,212 = 19 are the restored policies with an average claim cost above EUR 81,000, not duplicate policies.

**3. Changes to make now (no decision needed)**

In `datasets/_dev/tabarena-v0pt2/bemtpl97/`:

1. LEAK-41 reporting clause (P4, Must; both sides agree). Add one sentence to the Exposure bullet of `curation_comments`, giving the declared-metric numbers:
   - the Poisson gain +0.0047 (SD 0.0006) and the L2 gain +0.0051 (SD 0.0007) on 9 folds;
   - probe 22 at its 50k cap: +0.0040 and +0.0035;
   - both fits gain, so expo stays out;
   - the weight alone, fitted: 0.6122 against 0.6193 (constant) and 0.5979 (honest);
   - a scaled 1/expo as the prediction: at the constant.
   Giving both readings of the ceiling meets the clause however X2 is settled.

2. Name the scale of the old numbers (EV-2, writing):
   - In the Exposure bullet, "0.0036 to 0.0041" and "0.0039" are count-target fits with expo as a free feature, from the old task.
   - The +0.0043 in the 2026-11-06 CC and in the leak_checks.md LEAK-10/LEAK-41 Cases row looks rate-scale (0.0039 × 1.124). The CC is the curator's line: annotate it, do not rewrite it.

3. Copies kept bullet (LEAK-16, Should; writing):
   - Give the shipped counts: 397 extra exact rows and 88 conflicting profiles (177 rows).
   - In the superseded part, "50 rows" becomes "50 profiles (100 rows)".
   - Add the clause on possible re-issued policies: 57-176 pairs whose exposures sum to a year, sharing no claims. The bullet's "each row is a distinct source policyholder" is a claim the data makes less than certain. The clause costs one line; the critic asked for it and the advocate called it optional, so I settle it as: add it.

4. Postcode (CLEAN-14, Should; both sides agree after the rebuttals):
   - In the Dtypes bullet: "postcode nominal although its leading digit is the province, since long/lat give each municipality's location (as in house_sales, melbourne_housing_market and perth_house_prices; unlike lt_vehicle_loan_default_prediction, which has no coordinates)".
   - Add a note that a 583-level code needs encoding or smoothing, as the source smooths location in space (Sec. 4.1).

5. REVIEW.md:
   - The new panel block supersedes the old outcome block, which still says floor 1e-6, LEAK-10 triggered and 4.2-4.4% skill.
   - Add the no_signal reading: "no_signal reads the RMSE skill (R² 0.015); declared-metric skill 3.46% (0.5979 vs 0.6193), 9/9: TP-2 small real signal, keep (EV-3)".
   - Give the probe 22 R² with its cap: 0.032 at 50k, 0.055 on full folds.

6. Record `curation/records/bemtpl97.md`:
   - An Assessment line for this panel: ship after changes, notes only, and the current skill of 3.46%.
   - It states that the priority's "risk -: issue 1" factor is resolved. Re-weighing the priority is issue 3.
   - Inline "(superseded 2026-11-06)" notes on Myunghwan's lines 50 and 56 and the floor line 76 are optional. No rule asks for them, and fremtpl2 and australian do not have them either.

Not a definition change: the clean-room task.md does not name the metric. That is a gap in the panel kit, and it is why the blind reviewer asked for the weighted Poisson deviance that already ships.

**4. Issues for the curator (ranked)**

X1 (P4, LEAK-41 Must; cross-dataset: fremtpl2, australian_vehicle_insurance_2004_2005, frempl_french_motor_personal_line, pricing_game_2016_french_fleet, spanish_motor_insurance_coverage_level_2022_2024). The test-row weight is readable next to the features.

- Problem: a scoring column stays in the frame. The participant kit ships test-row expo in scoring.parquet, so one line of code makes the realized exposure, which the outcome partly sets, a model input.
- Effect, measured by the task gamer on 9 splits against an honest 0.59913 (noise moves the score by 0.00005):

  | Exploit | Score | Gain |
  |---|---|---|
  | expo or 1/expo as a feature | 0.59396 | 0.0052 (0.0039-0.0061) |
  | expo<1 flag | 0.59467 | 0.0045 |
  | per-expo-bin factor learned on train | 0.59503 | 0.0041 |

  No deployed model has this input at the quote.
- What this definition needs now: nothing more than changes 1-2.
  - The definition meets LEAK-41: `feature_columns` drops expo, and the scoring column's description already says "never a feature".
  - A clause for this dataset alone would treat it unlike its five siblings.
  - The critic's disputed clause ("test-row values are for the scorer only") is a placement question, not a conflict between rules, so it moves here.
- Advocate's best evidence: the API (definitions.md) says a scoring column is never a feature and the harness passes the weight only as `sample_weight` and to the scorer, so misuse breaks the protocol, not the dataset.
- Critic's best evidence: the generated README is what a user reads. It does not say that test-row weights belong to the scorer, and the misuse gains about a quarter of the honest skill.
- Rejected under LEAK-41's own Must: the gamer's alternative of scoring only full-year test rows. It is also unnecessary, since the ranking is unchanged on those rows.
- Options:
  - (a) withhold test-row scoring columns from participant bundles, with the scorer joining them on its side;
  - (b) generated README and describe() text, for every role=weight scoring column, saying that test-row values are for the scorer only and never a model input;
  - (c) a clause in each definition's scoring-column description;
  - (d) leave as is.
- Recommendation: (b) now, as one house change that covers every weighted table, and (a) for any kit given to outside participants.

X2 (P4, LEAK-41 Must, wording; cross-dataset: fremtpl2 has the same gap). What "the score of 1/weight alone" means for a deviance.

- Problem: for a deviance, 1/weight used as a prediction is no ceiling (k/expo scores at the constant). Probe 22 computes it only for a Gini.
- Effect: none on the decision. bemtpl97 and fremtpl2 still have to state the numbers, and the three siblings that report them may read the clause differently.
- Best evidence:
  - Precedent checker, for an amendment: a scaled 1/expo scores 0.6223 against 0.6233; fitted on expo, it beats the constant by 0.0051-0.0079.
  - Both sides: it does not block bemtpl97.
- Options:
  - (a) Amend LEAK-41: the ceiling is the weight alone fitted to the target (1/weight for a rank metric). This is the precedent checker's recommendation.
  - (b) Read the clause as it stands and report the fitted weight alone, with no amendment.
  - (c) Leave it. A Must has no exceptions, so this is not open.
- Recommendation: (a). Under (a) or (b), add fremtpl2's equivalent of change 1.

Issue 3 (Weigh). The record's priority, 3, rests on "risk -: issue 1", which is resolved today. This is a re-weighing for the next assessment, not a block.

**5. Disputed points and how they settle**

D1. Clause in this definition against a harness-level policy (critic point 2, advocate point 6).
- No rule demands a clause in the definition: LEAK-41 governs model inputs, and the definition meets it.
- The remedy belongs at the house level, so like cases stay alike (principles, Conflicts).
- Moved to X1.

D2. Postcode: "settled precedent" against lt_vehicle_loan_default_prediction (P7, CLEAN-14, Should).
- Settled by a fact I checked. house_sales, melbourne_housing_market and perth_house_prices, which went nominal, all ship coordinates.
- lt_vehicle_loan has no coordinates, and its geographic order was measured.
- The distinguishing fact holds and is written down (change 4). No change of type.
- If the curator wants it explicit, CLEAN-14's code clause could say "unless coordinates already carry the place". That would be an amendment, with four cases behind it.

D3. Which fit is "the worse" (advocate's rebuttal).
- Not a real dispute. The order flips between the full-fold and capped runs, by less than one SD, and both gains are positive. The note gives both runs (change 1).

D4. Re-issued pairs clause, "optional" against "ask": add it (change 3; writing, LEAK-16).

**6. The task gamer's exploits, mapped to rules**

The definition has no "Potential leak, kept on purpose:" note. Its only accepted warning, task_target_value_dominant (the 144,936 zero rates), is unrelated.

| Exploit | Rule | Status | Gain compared with the notes |
|---|---|---|---|
| 1. expo or 1/expo as a feature (+0.0052) | LEAK-41 (Must), LEAK-10 | The mechanism is known (Exposure bullet; scoring column "never a feature"). The channel, readable test-row weights, is new and not documented. | Differs from the notes' 0.0036-0.0041 / 0.0039 / +0.0043, which are count-scale fits from the old setup. Matches the declared-metric 0.0047 / 0.0051 within noise. Change 1 removes the difference. |
| 2. expo<1 flag (+0.0045) | LEAK-41, "a column that encodes it" | Known mechanism; same channel | Same as 1 |
| 3. per-expo-bin post-hoc factor (+0.0041) | LEAK-41: the test weight used as an input after the model | Known mechanism; same channel | Same as 1 |

Attacks that found nothing:
- postcode frequency over all rows (LEAK-30): +0.0003, within noise, and a statistic a deployed model has;
- copies (LEAK-16): a twin's claim gives 0.103 against 0.099, no entity leak;
- row order: the claim rate by row decile is flat;
- value formats: no class-dependent precision or rounding;
- the training target revealing expo: no help at test time beyond exploit 1;
- lookup in the public source: works for any public dataset, not ranked.

Dropping short rows from training makes an honest model worse (0.60106 against 0.59913).

**7. Consistency with precedent**

The precedent checker found the definition consistent, and the register raises no flag on bemtpl97.
- It is treated exactly like fremtpl2: rate target, exposure as the weight, mean_poisson_deviance, floor 1e-4, ForcedIIDFromTemporal, fit approximate.
- It fits the pattern of the four sibling tables reversed the same day.
- The three reversals each name the fact that sets them apart, so none needs a prompt:
  - Myunghwan's call of 2026-10-23 (keep expo as a predictor);
  - Myunghwan's call of 2026-10-26 (count target, no weighting; his Poisson deviance is kept up to a constant per fold);
  - the 1e-6 floor of 2026-11-04 (MET-13 amended on purpose).
- The per-contract exception (spanish_motor_insurance_2015_2018) does not apply: bemtpl97's term within 1997 varies and cannot be told apart from surrenders.

Reflection prompts:
- **Consistency check (AI, 2026-11-06):** australian_vehicle_insurance_2004_2005, frempl_french_motor_personal_line and pricing_game_2016_french_fleet report LEAK-41's L2 gain and weight-alone score, while bemtpl97 and fremtpl2 do not. A Must has no exceptions. (a) Add the numbers to both (change 1 here, and the same for fremtpl2); (b) amend LEAK-41's ceiling for deviances (X2) and then add them; (c) none, since a Must cannot be left unmet.
- **Consistency check (AI, 2026-11-06):** bemtpl97's postcode stays nominal while lt_vehicle_loan_default_prediction's geographically ordered code went numeric (2026-11-05). The distinguishing fact: long/lat give each postcode's location, as in house_sales, melbourne and perth, which also went nominal. (a) Record the fact in the Dtypes bullet (change 4); (b) ship postcode as a number like lt_vehicle_loan; (c) amend CLEAN-14's code clause to name coordinates.
- Optional naming point: fremtpl2's `claim_frequency` is the one outlier against the family's `*_per_year` target names. No rule covers it.

</details>

<details><summary>Claim audit</summary>

**Claim audit: bemtpl97 (exposure re-review, 2026-11-06, full tier)**

Read-only. Tests: the target, weight, splits, metric identity and edges; 9-fold LightGBM fits, weighted Poisson and
weighted L2, with and without expo, 1/expo alone, at-quote and A/E tests; the raw file and the start-excess claim;
copies; unweighted fits and expo predictability.
Model used throughout: untuned LightGBM (400 trees, lr 0.03, 31 leaves, min_child_samples 200), shipped types, every fit
weighted by expo unless stated, scored by an independent formula of the declared metric that equals the scorer on every
fold (dummy 0.623246 both ways on fold 0/0).

**Verdict**

Today's change holds: the target, the weight, the metric identity with the source's Eq. 5 count deviance, the floor and
the removal of expo from the features all survive tests that could have refuted them. One Must clause is not met in the
text: LEAK-41's reporting clause (gain of the suspect column on the declared metric under an L2 fit and under the
weighted actuarial fit, and the score of 1/weight alone) is not in the definition; the numbers it gives are on the old
count scale with expo as a free feature. The decision itself does not change: both fits show expo gains, so it stays
out. The other findings are about stale numbers and wording.

**Claims table (today's changes first)**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Target nclaims_per_year = nclaims/expo, 559 distinct values; _clean checks the count rebuilds; nclaims 0 to 5 | dataset.py _clean, curation_comments "Target", CHANGES.md | rebuild nclaims = y*expo on the container | holds | integers exactly, 0..5 = {144936, 16556, 1558, 162, 17, 2}; 559 distinct; max rate 182.5 (2 claims in 4 days) | MET-14 |
| 2 | expo is no feature; it is the weight scoring column, the metric's weight input and sample_weight | dataset.py scoring_columns/sample_weight; CC 2026-11-06 | feature_columns(c), sample_weight(c), task_metadata | holds | features = 11 rating factors, expo absent; sample_weight 'expo'; MetricSpec inputs {'weight':'expo'} | LEAK-41, MET-15 |
| 3 | Weighted rate deviance = source count deviance of expo x rate times n/sum(expo) of the scored rows, 1.123 to 1.125; so models rank as by the source's metric on every fold | metric.definition; curation_comments "Metric"; REVIEW issue 1 Resolved | compute both on all 9 test folds | holds | ratio = n/sum(expo) exactly on every fold, 1.12290 to 1.12542 (rounds to 1.123-1.125); algebraically exact, floor included (floor applies to the rate) | MET-11 (source, identity) |
| 4 | The original is the mean Poisson deviance of observed claims against expected observed-period counts (treeML.Rmd L641-657) | metric.original/reference | read treeML.Rmd at the pinned commit | holds | dev_poiss(ytrue,yhat) = -2*mean(dpois(y,yhat,log)-dpois(y,y,log)), called as dev_poiss(mtpl_tst$nclaims, .x * mtpl_tst$expo), unweighted; the fit uses offset(log(expo)) (L148) | MET-1, MET-3 |
| 5 | Floor 1e-4 claims per year, two orders below the smallest plausible rate; NaN or infinite raises | metric.params; curation_comments "Metric"; MET-13 | min prediction of the weighted Poisson fit on 9 folds; scorer with NaN/inf/-1/0 | holds | min predicted rate 0.022-0.045, 0.1% quantile 0.034-0.056: 1e-4 is 2.3-2.7 orders below; 0 of 489,693 test predictions below 1e-3; NaN and inf raise ValueError; 0 and -1 floor; score row-order invariant | MET-13 |
| 6 | Library implementation tested (weighted equals sklearn sample_weight, hand case, equals count deviance) | MET-13 | read src/data_foundry/v2/metrics.py and tests/test_v2_metrics.py | holds | _poisson_deviance -> sklearn mean_poisson_deviance(sample_weight=w) on floored preds; tests at L531-559 cover weighted vs sklearn, by hand, rate-vs-count identity, floor | MET-13 |
| 7 | "Each policyholder counts in proportion to that share, in training and scoring"; README: a model fitted without the weight targets another quantity | task_summary.predicted; README "Training weight" | fit the rate unweighted (repeat 0-2, fold 0) | holds | unweighted training mean 0.157 vs weighted 0.139 (1.13x); unweighted Poisson LGBM 0.6052 vs weighted 0.5973 on the same folds; unweighted L2 0.6161, worse than the weighted dummy on 1 of 3 folds (0.6221 vs 0.6171) | MET-15 |
| 8 | The weighting is right for the decision (premium earned pro rata, not a per-contract decision) | task_summary.use_case; MET-15 | reading of MET-15 against the use case | holds | the actuary prices a yearly premium earned pro rata over insured time; the book's claims are a sum over exposure | MET-15 |
| 9 | Probe 22: features predict expo at R2 0.03; expo as a feature gains +0.0040 (SD 0.0008); no feature's gain goes through expo above noise | CHANGES.md; probes/probe22*.txt | refit expo on the 11 features on full train folds; 9-fold gain of expo on the declared metric | holds in substance, numbers cap-dependent | expo R2 0.055, Spearman 0.24 on full folds (probe, 50k cap: 0.032 / 0.20); gain of expo +0.0047 (SD 0.0006, 9/9 folds) weighted Poisson, +0.0051 (SD 0.0007) weighted L2; probe: +0.0040 / +0.0035 (SD 0.0027); mediated gains all within noise in both probe runs | LEAK-41, USE-6 |
| 10 | LEAK-41 reporting: "for each suspect column the definition reports its gain on the declared metric with an L2 fit on the shipped scale and with the weighted actuarial fit, and decides on the worse; it states the score of 1/weight alone" | leak_checks.md LEAK-41 (applies to the definition) | read curation_comments Exposure bullet and CC | REFUTED (not reported) | the bullet gives "0.0036 to 0.0041 ... over a proportional offset" and "0.0039", the CC "+0.0043": all Poisson count-target fits with expo free (old scale, old task); no L2 number, no 1/expo-alone score. On the declared metric: L2 +0.0051 (SD 0.0007), weighted Poisson +0.0047 (SD 0.0006): the worse is L2; 1/expo alone scores 0.6122 (Poisson) / 0.6126 (L2) against the training mean's 0.6193 and the honest model's 0.5979 (it recovers 0.0071 of the honest 0.0214) | LEAK-41 (Must) |
| 11 | Part-year policies claim about 1.4 times the offset model's expected count | curation_comments Exposure | A/E of expo<1 rows under the shipped weighted Poisson fit, 9 folds | holds | A/E part-year 1.42 (1.31-1.48), full-year 0.93; expo<=0.25: 1.82 | LEAK-41 |
| 12 | At the quote the free model was 0.0002 to 0.0011 worse than the offset model, never better; its claims 1.08 times its price | curation_comments Exposure; CC "never better at quotation" | free model (expo as feature) predicted at expo=1, scored on the declared metric, vs the honest model | holds in direction; range not reproduced | worse on 9/9 folds by 0.0003-0.0018 on the rate scale (0.00026-0.0016 on the count scale); claims/price 1.080 (1.058-1.102); honest model 1.000 | LEAK-41 |
| 13 | Without the month-end and first-of-month background, excess starts claim 0.094 a year and full years 0.126, so true starts show no excess claims | curation_comments Exposure | day counts expo*365 on the raw file; spikes at first-of-month starts and month-end ends against the mean of the 6 neighbouring days; 31 and 334 (start and end alike) left out | holds | 885 excess start rows, 43.8 excess claims, 0.0939 claims/yr; full years 0.1260; month-end ends 4,413 excess rows at 0.166/yr (the surrender side) | LEAK-41, LEAK-7 |
| 14 | No model trained or scored on rows selected by the realized weight | LEAK-41 (implied) | read _clean | holds | no row filter; all 163,231 rows in every split | LEAK-41 |
| 15 | Floor change from 1e-6 on the count; low-cardinality acceptance went; container 01a18ad7 superseded | CHANGES.md, CC | README frontmatter, accepted_check_warnings | holds | only task_target_value_dominant accepted; README build_stale true | MET-13 |
| 16 | Accepted warning: 144,936 zero rates are nonclaimants | accepted_check_warnings | count | holds | 144,936 rows with nclaims 0 | TP |
| 17 | Row: one of 163,231 policyholders; distinct IDs; one TOWN per postcode | task_summary.row; _clean; notes | raw file | holds | 163,231 rows, ID unique, 583 postcodes, 1 TOWN each | PROV-8 |
| 18 | The 19 policies with AVG above 81,000 hold 21 claims, all claimants (0.1% of claims) | notes "Selection by the release", CC 2026-11-05 | raw file | holds | 19 rows, 21 claims, all claimants, 0.104% of claims | USE-5, PROV-8 |
| 19 | Raw order sorted by postcode, so no row-order window | notes "Split forced IID" | raw PC monotone | holds | PC monotone increasing over all 163,231 rows | SPLIT-8 |
| 20 | Split: random 3x3 IID, train 108,820-108,821, test 54,410-54,411; test customers unseen | splits_comment | splits | holds | sizes as stated, no train/test overlap, each repeat covers all rows | SPLIT-1, SPLIT-8 |
| 21 | "after the base class's content ordering and shuffle with seed 42" | splits_comment | not run | untested | house mechanism; not refutable from the container without re-implementing the base class | - |
| 22 | Copies kept: "176 extra exact rows and 50 rows with a conflicting profile" (no sex) | curation_comments "Copies kept" | recount on the old basis (expo a feature) and the shipped basis | REFUTED (stale and miscounted) | old basis: 176 extra exact rows holds; 50 is the number of conflicting PROFILES (100 rows). Shipped basis (expo no feature): 397 extra exact rows, 88 conflicting profiles (177 rows), 485 extra feature-profile copies; bundle info shows 397 and 88; probe 5: 0.4% of test rows have a train copy, 0.1% with another label | LEAK-16, LEAK-18, writing |
| 23 | Exposure gain "+0.0043, 17% of the skill" (CC 2026-11-06, leak_checks case row) vs "0.0036 to 0.0041 ... 0.0039 on the 163,231 rows" (bullet) | CC vs bullet | compare scales | inconsistent | 0.0039 x 1.124 = 0.0044: the CC number appears to be on the rate scale and the bullet's on the count scale, neither says so; mine on the declared metric: 0.0047 (18% of the free model's gain over the dummy) | writing, EV-2 |
| 24 | Skill: "the model scores 0.5279 against the training mean's 0.5520 (4.4%)" | CC 2026-11-05 | honest weighted Poisson fit on the shipped task | superseded, not restated | today 0.5979 vs 0.6193 on the declared metric: 3.46% (3.27-3.68%), 9/9 folds; without postcode 0.5982. The 4.4% was count scale with expo free; no current skill number is in the definition | TP-2, writing |
| 25 | Task probe flag no_signal (TP-1, TP-2) | probes/task.txt | read the probe JSON | flag is a reading artifact; signal real | the probe's "skill" is the RMSE skill (= R2 0.015); on the declared metric probe LightGBM scores 0.6004 vs dummy 0.6199 (3.1%), and the weighted Poisson fit 3.5%, 9/9. task.txt also prints "best family lightgbm" and "best family linear" (declared-metric best vs RMSE best). Under EV-3 the benign reading holds; it needs one line in REVIEW.md | TP-2, EV-3 |
| 26 | Use case: EU insurer today; sex barred since 21 December 2012 (C-236/09) | task_summary | settled on 2026-11-05; not re-run | untested today | not reopened by today's change | USE-1 |
| 27 | Prediction point: rating factors registered at policy start (binning manuscript Sec. 2) | notes | settled; every remaining feature is a rating factor | holds (settled) | expo, the only period value, is gone; probe 22 finds no feature that carries it above noise | LEAK-10, LEAK-41 |
| 28 | The source's paper (arXiv:1904.10890v3 Eq. 5, Sec. 4.1 quote) | notes | fetch the PDF | untested here | the PDF did not render to text in this sandbox (no pdftotext/pypdf); the code check (claim 4) and the 2026-11-04 panel's reading support it | MET-1, EV-2 |
| 29 | Licence: no licence in the 2019 repo, GPL (>= 2) in CASdatasets | license | not run | untested | unchanged today | PROV |
| 30 | REVIEW.md outcome block (floor 1e-6, LEAK-10 triggered, 4.2-4.4% skill) | REVIEW.md top | compare with today | stale | describes the pre-2026-11-06 state; the new panel block replaces it | writing |
| 31 | Record priority 3 rests on "risk: issue 1, a likely LEAK-10 leak through expo" | record Assessment 2026-11-04 | compare | stale | the risk is resolved today; the priority factors may be revisited | Weigh |

**Refuted and untested, ranked (validity first, Must first)**

R1. LEAK-41 reporting clause not met (claim 10; P4, Must). Validity of the decision is NOT affected: under both fits
    expo as a feature gains (L2 +0.0051, weighted Poisson +0.0047 on the declared metric, 9/9 folds), so "decide on the
    worse" also keeps it out. What is missing is the stated evidence, on the declared metric's scale: the L2 gain, the
    actuarial gain, and the 1/weight-alone score.
    What it changes: the notes, not the data. Mildest remedy: one sentence in the Exposure bullet, e.g. "On the declared
    metric (9 shipped folds, untuned LightGBM, weighted by expo): expo as a feature gains +0.0047 (SD 0.0006) under the
    weighted Poisson fit and +0.0051 (SD 0.0007) under a weighted L2 fit (probe 22, 50,000-row cap: +0.0040 and
    +0.0035); 1/expo alone scores 0.6122 against the training mean's 0.6193 and the honest model's 0.5979." Also mark
    the 0.0036-0.0041 / 0.0039 numbers as count-scale fits with expo free.

R2. Stale copy counts (claim 22; P4/P7, LEAK-16/18, Should/quality). The "Copies kept" bullet gives counts for the old
    feature set (expo a feature), and "50 rows" are 50 profiles (100 rows). With expo out: 397 extra exact rows,
    88 conflicting profiles (177 rows); probe 5: 0.4% of test rows have a train copy. The keep stays right (coarse
    profiles, distinct IDs). Remedy: update the numbers and say "profiles".

R3. Mixed scales for the exposure gain (claim 23; writing, EV-2). The CC and the leak_checks case row say +0.0043,
    the bullet 0.0036-0.0041 and 0.0039, without a scale. Remedy: name the scale on each number, or replace them with
    the declared-metric numbers of R1.

R4. No current skill number (claim 24) and the unread no_signal flag (claim 25; P6, TP-2, EV-3). The signal is real on
    the declared metric: 3.46% deviance skill (3.27-3.68%), 9/9 folds; the probe's flag reads RMSE skill (R2 0.015).
    Remedy: one REVIEW.md line with the reading; optionally replace the stale 0.5279/0.5520 in the notes with
    0.5979/0.6193.

R5. Probe 22 numbers depend on the cap (claim 9; minor). Full-fold expo R2 is 0.055 (Spearman 0.24), not 0.03. It does
    not change the call (rating factors known at the quote stay, USE-6). Remedy: quote the full-fold value or name
    the cap.

R6. Stale review text (claims 30, 31; writing, Weigh). The REVIEW.md outcome block and the record's priority line
    describe the pre-change state. Remedy: the new panel block supersedes the outcome; the next assessment may revisit
    the priority (the "risk -" factor is resolved).

Untested: claim 21 (seed/shuffle mechanism, house code), claim 26 (sex ruling, settled 2026-11-05, not reopened),
claim 28 (the arXiv PDF text did not render here; the treeML code confirms the metric), claim 29 (licence), the
rebuild (curator only; README build is stale by design).

**Metric summary (MET-1, MET-11, MET-13, MET-15):** holds. The source scores the unweighted mean Poisson deviance of
nclaims against frequency x expo (treeML.Rmd L641-657, fit with offset(log(expo)) at L148). The shipped weighted rate
deviance is that score times n/sum(expo) of each fold (1.1229-1.1254), an exact identity, so models rank the same on
every fold (origin source). Computable on every fold: 54,410-54,411 test rows, 5,986-6,169 claimants and
6,647-6,822 claims per fold; dummy scores 0.6142-0.6256. Floor 1e-4 is never reached by honest fits (min 0.022). NaN
and inf raise. sample_weight equals the metric's weight input (MET-15).

</details>

<details><summary>Column audit</summary>

**Column audit: bemtpl97 (exposure re-review, 2026-11-06, tier full)**

Verdict: no leak and no cleaning problem in any column. The change of 2026-11-06 is right column by column. expo has
left the features and is only the weight. The target is the rate and is not transformed (CLEAN-16). nclaims is out of
the frame. Every feature that predicts expo is known at the quote, so it stays (LEAK-41, USE-6). There is one open
question for the curator, low rank (P7, CLEAN-14): the 583-level nominal postcode, whose digits carry geography.

Read: the dataset's dataset.py and REVIEW.md; principles.md, leak_checks.md (LEAK-10, LEAK-41, probe 22),
cleaning_features.md (CLEAN-14, CLEAN-16) and use_case.md (USE-6, USE-7); the CASdatasets codebook
man/beMTPL97.Rd; the probe outputs task.txt, leak.txt, probe22.txt and probe22_l2.txt.

Frame: loaded with dataset_io.from_definition (rebuilt from the definition), 163,231 rows, 11 features, the target,
and expo as the weight scoring column (it is not in df; it is ProbeInput.weights). No missing values in any column.

Prediction point: the quote at policy start. Source: "The risk factors are registered at the start of the policy
period and remain constant during this period" (binning manuscript, Sec. 2).

**Column table**

| Column | Meaning (codebook) | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| nclaims_per_year (target) | claims of 1997 divided by expo (counts 0-5: 144,936 / 16,556 / 1,558 / 162 / 17 / 2) | the outcome | float64, 559 values, 0 to 182.5. The weighted mean 0.139 matches the portfolio frequency. 79 rows above 10 a year carry 87 claims but only 5.6 of the total weight, so the weight keeps them in proportion. Not transformed, as CLEAN-16 asks for a deviance-scored target. _clean checks that rate x expo gives back the count | fine | MET-14, CLEAN-16 |
| expo (weight scoring column) | share of the year at risk; values are whole days from 1/365 to 1 (expo*365 is an integer on every row). 22.7% of rows are part-year, with spikes at month ends (31, 90, 120, 151, 181, 273, 334 days) | no: realized, cut short by a surrender | the weight of the metric and of training. Not a feature: absent from the probe frame | fine as the weight; never an input | LEAK-41, MET-15 |
| coverage | TPL / TPL+ (plus limited material damage) / TPL++ (plus comprehensive) | yes, contract at the start | ordered category TPL < TPL+ < TPL++, the codebook's nesting. The raw PO/FO codes are decoded correctly (raw row 2: PO -> TPL+) | fine | CLEAN-14, CLEAN-12 |
| ageph | policyholder age | yes | int64, 18-95, numeric | fine | CLEAN-14 |
| bm | level 0-22 on the former Belgian bonus-malus scale; higher means a worse claim history | yes. Checked on the data: bm 0 has 5,215 claimants (frequency 0.101 a year), which a level updated after the year's claims would not allow. So it is the level at the start | int64, numeric. No words per level, so it stays a number (CLEAN-14 scale rule). 2 rows have age 18-19 at bm 0 or 1 (a new driver enters at 11): implausible but not impossible (a transferred level), so left alone | fine | LEAK-10, CLEAN-14 |
| power | vehicle power in kW | yes | int64, 10-243 | fine | CLEAN-14 |
| agec | vehicle age in years | yes | int64, 0-48. agec 0 has only 195 rows (mostly full year), while agec 1 has 7,557 rows, 34% of them part-year. This looks like age counted from the registration year (the source does not say). It is a vehicle attribute at the start either way. A car older than the driver's years since 18 occurs on 9,126 rows (used cars), which is not impossible | fine | CLEAN-14 |
| fuel | gasoline / diesel | yes | nominal category | fine | CLEAN-14 |
| use | private / work | yes | nominal category | fine | CLEAN-14 |
| fleet | vehicle is part of a fleet (1 yes, 0 no) | yes | category "0"/"1", decoded from the 2019 copy's N/Y to the release's codes. A 0/1 flag is a category (CLEAN-14). N/Y would read better, but the release's codes are a documented choice | fine | CLEAN-14 |
| postcode | policyholder's postcode (municipality) | yes | nominal category, 583 levels, 1000-9990. The dtype probe flags it numeric_levels (answered below). TOWN, the name with one value per postcode, is dropped as redundant | question for the curator (low) | CLEAN-14 |
| long | longitude of the municipality centre | yes | float64. One value per postcode in both directions (583 values), real coordinates | fine (redundant with postcode, not a leak) | CLEAN-14 |
| lat | latitude of the municipality centre | yes | float64, as long | fine | CLEAN-14 |
| Dropped: ID | policy number, equal to the raw row position; the file is sorted by postcode | - | dropped | right | CLEAN-3 |
| Dropped: AMOUNT, AVG | claim amount and average claim, from the same period | no (outcome) | dropped | right | LEAK-10 |
| Dropped: NCLAIMS -> nclaims | the count, part of the target | no | leaves the frame after the division | right | LEAK-10, MET-14 |
| Dropped: SEX | policyholder sex | yes, but barred for an EU insurer today | dropped by the CC of 2026-11-05 (Tensions row) | settled, not reopened | USE-6 tension |
| Dropped: TOWN | municipality name | yes | dropped, one value per postcode | right | CLEAN-3 |

**Weight proxy (LEAK-41, probe 22): each feature that predicts expo, judged by its timing**

- From the features, expo is predicted at R^2 0.032 and Spearman 0.20. Gain shares: postcode 57%, bm 12%, ageph 10%,
  agec 8%, power 6%. Under the Poisson fit no feature's gain goes through expo above noise: bm 15% and power 22% of
  their gains, each inside one SD. Under the L2 fit every weight-mediated gain is within its SD, and some are
  negative. The leak reference: expo as a feature gains +0.0040 (SD 0.0008) on the Poisson fit and +0.0035 (SD 0.0027)
  on L2.
- My own tables show where the link comes from: risk selection on attributes fixed at the start.
  - bm 11, the entry level, is 10.8% of part-year rows against 3.4% of full-year rows (new business that starts
    mid-year). Higher bm levels have more part-year rows.
  - agec 1 is 34% part-year (newly bought vehicles).
  - Young drivers are more often part-year: 33.7% at 18-20 against 12.7% over 70.
  - fleet 1 is 9.6% part-year against 23.1%.
  - Brussels (1xxx postcodes) has a mean expo of 0.845 against 0.89-0.91 elsewhere. Postcode alone predicts expo at a
    cross-fitted R^2 of 0.014 (shrunk means). Its 57% gain share is mostly a high-cardinality effect.
- Timing: all five are registered at the start of the policy period (the source), and bm is shown above to be the
  level at the start. None is set or cut after the quote, and none encodes expo (no length, earned amount, group sum
  of exposures, or precision that marks a cut). Under LEAK-41 and USE-6 they all stay. No feature goes.

**Dtype probe: one column of 11 flagged**

- postcode (category, 583 values, 1000-9990): numeric_levels.
  - Answer: postcode is a code, so a category is the default (CLEAN-14, last bullet). This follows the settled
    precedents (house_sales zipcode, melbourne_housing_market Postcode, perth_house_prices POSTCODE; the earlier panel
    settled it nominal).
  - The clause "unless its digits carry meaning a model can use (zip code prefixes, whose nearby values are nearby
    places)" applies in part. Belgian postcodes are hierarchical by province (1xxx Brussels and Brabant, 2xxx Antwerp,
    ... 9xxx East Flanders), and lt_vehicle_loan_default_prediction (2026-11-05) shipped a geography-ordered code as a
    number.
  - What sets this case apart: long and lat already give each municipality's exact location (one value per postcode),
    so a number adds no place information that is not already there. I would keep the category and leave the call to
    the curator.
  - For context only (types are decided from meaning, not from model runs; EV-4): with untuned LightGBM-Poisson,
    weighted, on the first 6 shipped splits x 2 seeds:
    - postcode as a category: 0.60851;
    - as a number: 0.59770 (-0.0108, better 12/12);
    - postcode dropped: 0.59791;
    - all geography dropped: 0.60174;
    - dummy: 0.61933.
    The 583-level category overfits an untuned model and is worse than no geography at all. Probe 22 shows the same
    (postcode gain -0.017 on the Poisson fit, -0.037 on L2) and so does the leak probe (all features -0.021, below a
    depth-2 tree at +0.012). This is a model-handling matter, not a cleaning error.
- No column of unknown meaning, no proxy missing codes, no reversed scale. coverage is the only ordinal, and its order
  matches the codebook.

**Problems ranked (principles.md: P1-P5 validity, then P6 value, then P7 quality)**

P4 (LEAK-41, LEAK-10, Must):
- None open. The only column set after the quote, expo, is now the weight and nothing else. Its leak was +0.0040 (SD
  0.0008), 16-18% of the skill earlier. No feature encodes it: R^2 0.03, and no gain through the weight above noise.
- bm was checked to be the level at the start (5,215 claimants at bm 0).
- No missingness caused by the outcome (no missing values), no window that ends at the outcome, no identifier left.
P6: none from the columns. The target is the rate, weighted, and the deviance on it equals the source's count deviance
times n/sum(expo).
P7 (CLEAN-14, Should; question for the curator, low):
- postcode stays a nominal category of 583 levels, although its digits are hierarchical by province.
- Mildest remedy: keep it as it is (precedent; long and lat carry the location). If you want the CLEAN-14 digit clause
  applied as for lt_vehicle_loan_default_prediction, ship it as a number. Do not decide it from the model numbers
  above.
- This is not reopened by today's change. It is listed only because probe 22 ranks postcode first as a predictor of
  expo, and that ranking comes from its cardinality, not from a timing problem.
Notes, no action:
- fleet ships as "0"/"1" rather than N/Y. It is a release convention and lossless.
- 2 rows have age 18-19 at bm 0 or 1, and agec 0 is rare (195 rows). These are plausible source facts and not
  impossible values (CLEAN-10 does not apply).

</details>

<details><summary>Split audit</summary>

**Split audit: bemtpl97 (exposure re-review, 2026-11-06, tier full)**

Verdict: RIGHT WITH NOTES. The IID split (ForcedIIDFromTemporal, 3 x 3 folds) still mirrors the application under the
rate target with expo as the weight. No re-split, gap or filter is needed. The notes below are disclosures or cross-references.

Inputs: definition rebuilt from the raw 2019 copy through dataset_io.from_definition (163,231 rows, 11 features, expo
as the weight, regime iid). The splits are the shipped ones: 9 folds, 108,820-108,821 train / 54,410-54,411 test.
Every model is fitted with sample_weight=expo on nclaims_per_year. Every score is the declared metric: weighted mean Poisson
deviance, floor 1e-4. My dummy, 0.61933, matches the task probe's 0.6199 on 5 of 9 splits.

**What today's change reopens, and what it does not**

- Regime (P3/P4, SPLIT-1, SPLIT-8): unchanged. The data is one undated policy year and the raw order is sorted by
  postcode, so no window can be built and the cost cannot be measured. The splits.md SPLIT-8 row for bemtpl97 still holds. The new target
  and weight do not create a time index.
- Time on risk cut at the year's edges (brief: SPLIT-9, LEAK-41):
  * Every row's expo is cut at 1 Jan and 31 Dec 1997. expo x 365 is a whole number on every row. 77.3% of rows are full
    years (126,222 at 365 days). The part-year rows hold 13.1% of the exposure and claim at 0.228 a year against 0.126.
  * The split has no window cutoff, so neither side admits rows by the length of their exposure, unlike
    pricing_game_2016_french_fleet. The two sides match on every fold:
    - mean expo: train 0.8893-0.8903, test 0.8886-0.8906;
    - full-year share: train 0.772-0.774, test 0.772-0.775;
    - KS p on the expo distribution: 0.67 to 1.00;
    - weighted claim rate: train 0.1385-0.1403, test 0.1374-0.1411.
    Nothing to fix.
  * The application quotes a full year. I scored each model on only the full-year test rows: the ranking is the same as on
    all rows, and the skills are close. LGBM without postcode beats the GLM: all rows 0.0342 against 0.0319 skill,
    full-year rows 0.0270 against 0.0254, 9 of 9 folds. The part-year rows (surrender after a claim) carry about 21% of the
    test claims at their expo weight, but they do not change which model wins. A note for the metric auditor, not a
    split defect.

**Problems, ranked by principles.md**

1. P4, SPLIT-8 (Must, satisfied): the forced-IID cost still cannot be measured. Disclosed already
   (curation_comments SPLIT-8 bullet, task_summary.split, fit approximate). No remedy. The year-to-year drift of
   frequency and the bonus-malus transitions are not tested, as before.

2. P4, SPLIT-29/SPLIT-30 (Must, no hit): the hidden group, postcode, rerun under the new target and weight.
   * All 583 postcodes recur in every training side. 0 or 1 test postcode per fold is new to its training side, and each
     such postcode has 2 rows. 31 postcodes have fewer than 30 rows. A new quote always has a known municipality, so the
     municipality is a feature, not an entity new data would lack (SPLIT-4, unchanged).
   * The alternative splits, same models, 9 folds each, skill = 1 - deviance / dummy:

     | Split | LGBM no postcode | GLM no postcode | LGBM with postcode (nominal) |
     |---|---|---|---|
     | shipped IID 3x3 | 0.0342 | 0.0319 | 0.0063 |
     | grouped by postcode 3x3 | 0.0327 | 0.0315 | 0.0270 |
     | leave one region out (1st digit) | 0.0277 | 0.0284 | 0.0274 |

   * Grouping by municipality costs the honest models 0.0004 to 0.0015 of skill. The ranking holds:
     - LGBM against the GLM, mean paired difference: -0.00143 (SD 0.00032) under IID, -0.00080 (SD 0.00064) grouped;
     - LGBM wins 9 of 9 folds under IID and 7 of 9 grouped.
     Only leaving out a whole region (a cold start that the use case does not have) makes the two tie: 4 of 9, +0.00047, SD 0.00164.
   * No hidden-group optimism. No re-split (SPLIT-30: the gap never decides; the context says municipalities recur).

3. P4, LEAK-16 / SPLIT-29 (Should, negligible): copies of rating profiles across the split.
   * Exact 11-feature profile copies: 963 rows in 478 repeated profiles. The leak probe finds an exact copy in train for
     0.4% of test rows. They carry the same label on 0.3% of test rows, mostly both zero claims, so a copy gives no
     shortcut.
   * New today: some copies look like one policyholder in two part-year records. Take same-profile pairs of part-year rows:
     - 57 of 144 have expo summing to one full year (365 +- 1 days). Strict: same postcode, coverage, power, fuel, use,
       fleet, ageph, agec and bm.
     - With ages within 1 year and bm within 2, 176 pairs (352 rows) do.
     - Base rate: 2.8% of random same-postcode pairs sum to at most one year; 15.1% of the 2-row profile copies do.
     The most likely cause is a policy re-issued during 1997, such as a vehicle or contract change that the rating
     factors do not show.
   * Size and effect: 114 to 352 rows (0.07% to 0.22%). About 45-47% of the pairs fall across train and test on each
     fold. Their outcomes are not shared: both records claim in 0.0% of the strict pairs and 1.1% of the loose ones.
     Mildest remedy: none. If you want it on record, one clause in the copies bullet: "some part-year copies may be one
     policyholder re-issued in 1997 (57 to 176 pairs whose exposures sum to a year; no shared claims)". The definition's
     "each row is a distinct source policyholder" rests on the unique source ID, which a re-issued policy would also
     get.

4. Cross-reference, not a split defect (column auditor; CLEAN-14, model behaviour): under the new weighted rate target,
   LightGBM with postcode as a native 583-level category loses much more than before.
   * Skill falls from 0.0342 without postcode to 0.0063 with it under the shipped IID split (+0.0173 deviance, 0 of 9
     folds better). Before, under the count target, it fell from 0.0452 to 0.0308.
   * Under the postcode-grouped split the loss is 0.0035. The overfitting is to seen categories: it penalises the
     model, it gives no optimism.
   * This likely explains the task probe's weak LightGBM (skill 0.015) and its no_signal flag, and the leak probe's
     "all features -0.021" (no postcode in its single-feature list).
   * Typing stays from context (dtypes-from-context). The README could warn that a 583-level nominal postcode needs an
     encoding or smoothing, as the source does with lat/long.

What I did not check: the IBNR or reporting delay of late-1997 claims; the source does not say when the extract was
taken. This is moot for an IID split, where no training label is newer than a test row's quote.

</details>

<details><summary>Domain practitioner</summary>

**bemtpl97: domain practitioner, re-review of 2026-11-06 (full tier)**

Actor: the pricing actuary of an EU motor third-party liability (MTPL) insurer. I build the claim-frequency model of
today's tariff and learn it from the 1997 Belgian portfolio.

**Verdict**

Fit: approximate. I agree with fit="approximate" (USE-8). The target, the weight and the metric are now the source's
own offset frequency model, the quantity I price. The data is still one undated 1997 year: random 1997
policyholders stand in for next year's book, and the rating factors are thinner than a tariff of today.
Metric: yes, it scores my decision. I would pick a model by the expo-weighted mean Poisson deviance with the
1e-4 floor myself (MET-1, MET-5, MET-8, MET-11, MET-14, MET-15, MET-13).
Today's change closes gap 1 of my earlier block, the one I ranked largest (expo as a free feature), in the form I
asked for. Nothing new blocks the dataset from my side.

**The five questions, as the actuary**

1. Inputs at the quote (USE-3, USE-6).
   - The 11 features are coverage, ageph, bm, power, agec, fuel, use, fleet, postcode, long and lat. All are
     registered at the start of the policy period (binning manuscript Sec. 2 p. 4, cited in the notes), so I have
     each of them at the quote. long and lat are the postcode's centroid.
   - expo is no longer an input (LEAK-41). That matches the quote: I price a full year (the contract term), and I
     cannot know the realized share of the year.
   - sex is gone. Correct for an EU tariff since 21 Dec 2012 (CJEU C-236/09, Test-Achats).
   - Inputs I would always have that are missing, all limits of the release and not curation errors:
     - vehicle make, model and value;
     - new business or renewal, and tenure with the insurer;
     - the claims-history certificate beyond the bm level;
     - the policy start date and planned term;
     - in many books today, telematics or mileage.
   - bm is the 1997 bonus-malus level, which was then on Belgium's uniform legal scale. Today each insurer runs its
     own system. This is my own knowledge (the scale was liberalised in the early 2000s) and I did not fetch a
     source. It adds to the age of the data (gap 1 below).

2. Target (USE-5). The claims per year insured, nclaims / expo, is the annual frequency f(x).
   - It enters the pure premium as E[N] x E[S] (Henckaerts et al., arXiv:1904.10890v3 Sec. 2). It is the quantity I
     act on, not a proxy.
   - I want a number: the expected rate, scored by a proper rule. A class or a threshold would be of no use to me.
   - Frequency is only half of the premium. A separate frequency model is standard practice, so USE-5 holds.

3. Rows, weights and test data.
   - One row is one policyholder-year, which is one premium I set.
   - Weighting by the share of the year insured: yes, that is how I would do it. Premium is earned pro rata and
     unearned premium is refunded on cancellation, so a book breaks even per earned year. The break-even rate is
     sum(N) / sum(e), not the mean of N/e (MET-15). On the kit:

     | Quantity | Value |
     |---|---|
     | portfolio rate sum(N)/sum(e) | 0.1393 claims per year |
     | unweighted mean of the target | 0.1575 (1.13 times the portfolio rate) |

     A model that ignores the weight overprices the book. In my checks (LightGBM
     Poisson, lr 0.05, 400 trees, min_child_samples 200, splits r0f0 to r0f2), actual/expected was 0.89 to 0.94
     without the weight and 0.977 to 1.015 with it.

     | Split | Weighted LGBM | Unweighted LGBM | Weighted constant | Unweighted constant |
     |---|---|---|---|---|
     | r0f0 | 0.60380 | 0.61044 | 0.62325 | 0.62454 |
     | r0f1 | 0.59906 | 0.61045 | 0.62050 | 0.62266 |
     | r0f2 | 0.59433 | 0.60319 | 0.61424 | 0.61746 |

     Ignoring the weight costs 0.0066 to 0.0114, more than the free-expo leak of 0.0040 that probe 22 measured. The
     metric punishes it, which is right. The harness has to pass sample_weight to every method. A method that cannot
     take weights is mispriced, and the benchmark should say so rather than hide it.
   - Test data: random policyholders of the same year, while I face next year's book (SPLIT-8, ForcedIIDFromTemporal,
     disclosed). The source itself cross-validates within the year (Sec. 3.3), so the benchmark matches the source's
     protocol, not my production setting.

4. Would I use this model? Yes, as a frequency-model benchmark and as a first segmentation. It separates risks:
   - the lowest predicted decile claims 0.073 to 0.081 a year, the highest 0.274 to 0.284 (3.4 to 3.8 times);
   - the expo-weighted ordered Lorenz Gini is 0.207 to 0.212.
   What would make me trust a winner:
   - actual/expected near 1 overall and by segment (bm, age, region). The weighted fit is at 0.98 to 1.01 overall.
   - a top decile that is not overfit. Mine came in at actual/expected 0.91 to 0.97, so it overprices the riskiest
     tenth a little.
   - postcode smoothed in space rather than memorised over 583 levels, as the source does (Sec. 4.1).
   What would make me distrust one:
   - a gain that rests on the 583 postcode levels;
   - a model that ignores the sample weight.
   The free-expo channel is now closed, so the worry I named in my earlier block is gone.

5. Metric: yes.
   - It is the source's metric. sum(w*d)/sum(w) on the rate equals Henckaerts et al.'s count deviance of e x f(x)
     (Eq. 5, Sec. 4.5) times n/sum(expo), 1.123 to 1.125 per fold, so models rank as by the source's metric
     (MET-5, MET-11).
   - It is scored at the unit I act on: the policyholder, weighted by the earned year, which is the premium I collect
     (MET-1, MET-15).
   - It is a strictly proper rule for the mean rate. It rewards both segmentation and level, and a tariff needs both
     (MET-8).
   - It weighs segmentation more than level. A uniform 10% overprice of the weighted model costs only 0.0009 to
     0.0019, against its 0.019 to 0.020 gain over the constant rate. That suits a frequency benchmark: in practice the
     level is rebalanced to the target premium volume at the end anyway.
   - Floor of 1e-4 claims per year (MET-13 as amended): the lowest decile's observed rate is about 0.07, and a
     plausible best cell is about 0.03, so the floor sits 2.5 to 3 orders below. The task probe puts 0.0% of
     predictions at the floor in every family. The floor never binds on honest predictions, which is how I would
     clip.
   - MET-6 and MET-7 do not apply: I make no threshold decision per policy and the source fixes no cost matrix. MET-9
     does not apply: this is not classification.
   - The alternatives I would not pick for a frequency benchmark:
     - the paper's loss-ratio lift, double lift and the ordered Lorenz Gini (Sec. 5) work on the pure premium and
       need a severity model;
     - the Gini ranks only and ignores the level.
   - The metric I would choose is the declared one, unchanged.

**Gaps between the dataset and my decision, ranked by how much they change the task**

1. One undated 1997 year with a random split. Today's book differs in claim frequency, in the bonus-malus system (a
   legal scale then) and in rating factors, and no later year exists to test drift (SPLIT-8). This is the reason the
   fit is approximate. It is disclosed.
2. Rating factors thinner than a modern tariff (vehicle, tenure, claims history, telematics). These are the release's
   limits. A benchmark only needs consistent inputs.
3. Without dates, the legitimate part of a mid-year start cannot be used. The notes measure little legitimate signal
   in it: excess starts claim 0.094 a year against 0.126 for full years. An offset GLM loses the same. Small.
4. Frequency only, no severity. This is the standard split of the premium, so USE-5 holds.
5. The 19 restored heavy-cost policyholders (21 claims, 0.1% of claims). Negligible for frequency, and restoring them
   removes a selection by the outcome. Agree.
Settled and not reopened: sex dropped (agree), coverage ordered, postcode nominal.

**What an expert would change**

- Nothing in the definition. Target, weight, metric and floor are what I would ship (MET-14, MET-15, LEAK-41,
  MET-13).
- Point for the mediator: the task probe flags no_signal (TP-1, TP-2) with "skill +0.015", which matches the probe's
  R^2. The relative deviance reduction of its own numbers is 3.1% (0.6199 to 0.60043). I measured 3.1% to 3.5%,
  with a 3.4 to 3.8 times decile spread. For MTPL frequency this is a normal, real signal: individual counts are
  mostly Poisson noise. It is TP-2's "small real signal: keep" (evidence.md row no_signal, case 3). If the probe's
  skill is the R^2 and not the declared metric's skill, the flag reads the wrong scale. The column or task auditor
  should check that.
- Optional wording: fit_reason could also name the 1997 legal bonus-malus scale as part of "rating factors may
  differ". Not required.

**Sources**

- Henckaerts, Cote, Antonio, Verbelen, arXiv:1904.10890v3: Sec. 2 (pure premium, offset), Sec. 3.2 Eq. 5, Sec. 3.3
  (folds), Sec. 4.1 (exposure causes, 583 postcodes, spatial smoothing), Sec. 4.5, Sec. 5 (lift, Gini). I read these
  in my earlier block and did not re-fetch them today.
- The definition, README, REVIEW.md (issue 1 resolved, my earlier block) and record; the change summary; the task
  probe and probe 22 (Poisson and L2 fits).
- My own checks on the participant kit (3 splits; my deviance equals the kit's score() to the last digit).
- Web, on offset against weighted-rate equivalence in Poisson GLMs and exposure as a covariate:
  https://metricgate.com/blogs/offset-vs-weight-in-glm/
  https://www.r-bloggers.com/2013/08/exposure-as-a-possible-explanatory-variable/
- From my own knowledge, not fetched: CJEU C-236/09 (Test-Achats); the pro-rata earning and refund of MTPL premium;
  the liberalisation of Belgium's legal bonus-malus scale.
- Rules: use_case.md USE-3, USE-5, USE-6, USE-8; metrics.md MET-1, MET-5, MET-6 to MET-9, MET-11, MET-13 to MET-15;
  leak_checks.md LEAK-41; evidence.md (no_signal row).

</details>

<details><summary>Blind review</summary>

**Blind review: beMTPL97 claim frequency (target nclaims_per_year, weight expo)**

**Verdict:** Include with changes. A real, widely used actuarial task with correct exposure handling and no leaks; the one real issue is the scoring metric: an exposure-weighted squared error on a claims-per-year rate is driven by a few short-exposure rows. Use Poisson deviance.

**Task**

Belgian MTPL portfolio, 1997 (CASdatasets beMTPL97; Henckaerts et al. 2018, Scand. Actuarial J.). An insurer predicts each policy's expected claim frequency at underwriting or renewal, to set the price (the frequency half of a frequency-severity tariff). This is a real, standard use.
- Features: coverage, ageph, bm, power, agec, fuel, use, fleet, postcode, long, lat. All are known at the start of the policy.
- Dropped source columns: id, claim, amount, average (all leaky or outcome columns, so dropping them is right) and sex. Dropping sex is defensible: the EU gender directive has banned gender in pricing since 2012. It does depart from the source paper.

**Training weight (expo): correct**

- The target is exactly nclaims/expo: max |target*expo - round| = 4e-16, and the implied counts are 0..5 (144,936 zeros, 16,556 ones, ...).
- Fitting the rate with weight expo is the textbook equivalent of a Poisson GLM/GBM on counts with a log(expo) offset: same likelihood up to a constant.
- Weighting test rows by expo is also right: Var(N/e) = lambda/e, so expo is the inverse-variance weight.
- Exposure-weighted mean rate = 0.139, which matches the published portfolio frequency of about 0.139. Unweighted mean = 0.158.
- Exposure: median 1.0 and 77% of rows equal 1.0, but 2% of rows have expo < 0.1 (minimum 0.00274, i.e. 1 day).

**Concerns (most to least serious)**

1. The metric must be Poisson deviance, not weighted MSE/RMSE.
   - The rate is heavy-tailed: max 182.5, which is 1 claim with expo 0.0055. 79 rows have a rate above 10.
   - Even after expo weighting, each row adds n^2/e to the squared error. The top 20 rows (0.01%) carry 4.6% of the total weighted SSE, and the top 1% carry 36%.
   - Signal is modest. In my 3-fold LightGBM check, model vs constant:
     - Poisson deviance: 0.600 vs 0.622, 0.592 vs 0.617, 0.600 vs 0.620 (about 3.5-4% reduction).
     - Weighted MSE: 0.187 vs 0.191 (about 2% reduction).
   - With a 2% margin, whichever fold holds the few extreme rows will dominate the ranking under MSE.
   - Change: score with exposure-weighted Poisson deviance, and declare it in task.md. If the framework only offers MSE-type metrics, at least report a deviance-based metric too.
   - Could not check: task.md says the score is weighted by expo but does not name the metric.
2. postcode is int64.
   - It has 583 levels, and long/lat are a deterministic function of it (each postcode maps to exactly one long/lat pair).
   - The numeric code is partly meaningful: the leading digit is the Belgian province, so treating it as ordinal is tolerable. With long/lat present it is redundant.
   - Change: keep as is, or declare it as a high-cardinality categorical. Either way, note that it is a geographic code. This is minor.
3. Duplicates and multiple rows per policy.
   - CASdatasets reports 163,212 unique policyholders, but there are 163,231 rows. So about 19 policies have two rows, and the id was dropped, so a random split can put the same policy in both train and test. The effect is negligible (0.01%).
   - 176 fully duplicated rows and 485 rows with duplicate features: these are natural coincidences of common profiles (mostly zero-claim, expo=1). Not a leak.
4. IID split.
   - The data is a single-year cross-section, so a random split is the only option. A real tariff would be applied to the next year's portfolio, so scores are mildly optimistic. Acceptable.
5. Signal and size.
   - Low signal by design: a claim-frequency task where the best possible model is close to the constant. Feature importance is spread (ageph, power, long, bm, postcode).
   - This is realistic and still separates methods: GLM vs GAM vs GBM differences in the literature are of this size.
   - 163k rows is plenty.

**Data plausibility**

- No missing values. Category levels match the source docs: coverage TPL/TPL+/TPL++, fuel, use, fleet as '0'/'1'.
- Ranges are plausible: ageph 18-95, bm 0-22, power 10-243 kW, agec 0-48, coordinates inside Belgium.
- The data is real (well-documented public portfolio), not synthetic.

**Could not check**

- The exact metric used.
- Whether the source's few multi-row policies are split across folds (id was removed).
- Whether the GitHub repos' versions differ from CASdatasets (I only read the CASdatasets reference page).

</details>

<details><summary>Task gamer</summary>

**beMTPL97 (nclaims_per_year, weighted Poisson deviance, IID 3x3): task gamer report**

Verdict: the task can be gamed only through the exposure (expo). It is shipped in scoring.parquet for the test rows as well, and using it as a feature cuts the deviance by about 0.9% (0.0052). Nothing else beats the noise.

All scores are mean_poisson_deviance (lower is better), averaged over the 9 shipped splits. The model is LightGBM with the poisson objective, 400 trees, lr 0.05, 31 leaves, min_child_samples 50, sample_weight = expo, all 11 features, no tuning.

Honest baseline: 0.59913 (per split 0.5945-0.6051).

Noise check (baseline plus a uniform random column): 0.59918. The mean moves by +0.00005, and the per-split moves range from -0.0009 to +0.0004.

| # | Exploit | Honest | Exploited | Gain per split (range) | Deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | expo (or 1/expo) as a feature | 0.59913 | 0.59396 / 0.59400 | 0.0052 mean (0.0039-0.0061) | No: actual exposure is known only at the end of the period; at the quote the term is 1 year | Keep expo out of reach at test time (do not ship test-row expo to participants), or state that expo is a weight/offset only and check that it is not used as a feature |
| 2 | flag expo < 1 as a feature | 0.59913 | 0.59467 | 0.0045 mean | No (same reason) | same |
| 3 | post-hoc rule: baseline x per-expo-bin factor learned on train | 0.59913 | 0.59503 | 0.0041 mean | No | same |

Finding 1 (the weight). Under a constant-rate Poisson model the claim rate would not depend on the exposure. Here it does, strongly. Claims per year insured by expo bin:
  (0,0.1] 0.388 (3,323 rows); (0.1,0.25] 0.273; (0.25,0.5] 0.240; (0.5,0.75] 0.198; (0.75,0.99] 0.235; full year 0.126 (126,516 rows).
Partial-year policies are either new mid-year business or policies surrendered or cancelled during the year. A claim can trigger a cancellation, as can a vehicle written off, so a short exposure is partly a consequence of the outcome. That is why a short-expo rate three times the full-year rate gives the label away. At the quote, a deployed model knows the planned term (a 1-year contract). At most it knows a mid-year start date, and the data has no start date. It does not know the realised exposure. The fact that would settle the size of the leak is the split of short exposures into late starts and early ends; the published data does not have it. A model that knew only the start date would get part of this gain legitimately. Because scoring.parquet ships expo for every row, test rows included, the exploit takes one line. The source analysis (Henckaerts et al. 2018, treeML) uses expo only as an offset or weight, never as a feature.

Mildest fix: keep using expo as the weight, but do not give participants the test rows' expo, which the benchmark's scorer can join on its own side. Alternatively, keep only full-year rows in the test set (expo == 1, 77% of rows), where the feature carries no information.

Flaws that hurt an honest model: none found.
- Training only on full-year policies (drop the expo < 1 rows): 0.60106, worse than the baseline's 0.59913. The short-exposure rows help, and the IID split makes no training row unavailable at the prediction point.

Attacks that found nothing:
- Postcode frequency computed over train and test rows together: 0.59880, a gain of 0.0003, inside the noise spread. It is also a portfolio statistic that a deployed model has: signal, not an exploit.
- Row order: the claim rate by row decile is flat at 0.135-0.144. The rows are shuffled, and no id column exists.
- Copies across the split: 963 rows share all 11 features with another row. Their claim rate given that a twin claimed is 0.103, against 0.099 when the twin did not, so there is no entity leak.
- Formats: long/lat are postcode centroids, one per postcode, with 11-14 decimals depending on the value, not by class. The share of round values (multiples of 5) in ageph, power and agec is the same for claimants and non-claimants. The difference in bm is the bm signal itself.
- Target format: y = nclaims/expo, so a non-zero training y reveals its exposure. That is no help at test time beyond expo itself (exploit 1).
- Train-vs-test differences and transforms over all rows: the split is IID random with equal fold sizes, and no feature is standardised or ranked (raw ages, postcodes, coordinates).
- Lookup in the published source (CASdatasets beMTPL97): it would work, since the public file holds nclaims and expo per row. Not ranked.

Not checked: a tuned honest model, to see whether the expo gain survives tuning (it is a large, monotone effect, so it likely does), and the split of short exposures into late starts and early ends (no date in the data).

Sources: https://arxiv.org/pdf/1904.10890 (Henckaerts et al., expo as offset; notes policyholders who start mid-year or surrender early); https://arxiv.org/pdf/2604.02400 (mid-term cancellations partly tied to severe claims); https://www.r-bloggers.com/2013/08/exposure-as-a-possible-explanatory-variable/

</details>

<details><summary>Precedent check</summary>

**Precedent check: bemtpl97, full tier, exposure re-review of 2026-11-06**

Verdict: consistent. The definition decides bemtpl97 exactly as fremtpl2 and fits the pattern of the other four insurance tables changed the same day. All three reversed calls (Myunghwan's of 2026-10-23 and 2026-10-26, Lennart's floor of 2026-11-04) name the fact that sets the new decision apart, so none needs a reflection prompt. The register raises no flag on bemtpl97 or on any exposure case: its flags concern LEAK-38, TP-10, USE-5, USE-8, SPLIT-9/10/14 and others, on unrelated datasets. There is one real gap: a reporting clause of LEAK-41 (a Must) that bemtpl97 and fremtpl2 both leave out and that australian_vehicle_insurance_2004_2005, frempl_french_motor_personal_line and pricing_game_2016_french_fleet fill. An issue draft for it is at the end.

Files read: the definition and REVIEW.md; the record (lines 50, 56, 72, 76, 92); fremtpl2's dataset.py;
principles.md, leak_checks.md, metrics.md and cleaning_features.md; the decision register; the probe outputs
(probe 22 with Poisson and L2 fits, the task probe).

My own measurements (read-only, with the shipped container and splits):
- The weighted rate deviance equals the count deviance of expo x rate times n/sum(expo) on the scored rows, exactly (0.62019 = 0.62019 on fold 0/0; 0.62350 on fold 1/1).
- Honest LightGBM-Poisson fitted with the expo weight: the smallest predicted rate is 0.0082 / 0.0096, the 0.1% quantile 0.020 / 0.023. The portfolio rate is 0.139 a year.
- expo alone (LightGBM on expo only) scores 0.61538 / 0.61303 / 0.60917 against the training-rate constant's 0.62325 / 0.62050 / 0.61424 (repeat 0, folds 0-2). That is a gain of 0.0051 to 0.0079.
- A scaled 1/expo (k/expo, with the counts summing right) scores no better than the constant: 0.62233 / 0.62152 / 0.61740.

**Decision 1: claims per year insured, expo as the weight scoring column and sample_weight, never a feature (Lennart, 2026-11-06; record line 92; REVIEW.md issue 1 option B in form (ii), option A of #51)**

Status: consistent.

Precedents and how bemtpl97 compares:
- fremtpl2, CC 2026-11-06 (Lennart): fremtpl2's dataset.py, line 171; metrics.md Cases line 313.
  - Same facts: realized time on risk, no dates that tell a mid-year start from a cancellation, a free-feature gain (fremtpl2 +0.0040, 25% of the skill; bemtpl97 +0.0043, 17%; probe 22 today +0.0040, SD 0.0008), and no better at quotation.
  - Same treatment: the rate as the target, the exposure as the weight scoring column, the metric's weight input and sample_weight, mean_poisson_deviance with origin source, min_prediction=1e-4, ForcedIIDFromTemporal, fit approximate.
  - Lennart's 2026-11-04 "beMTPL97 and freMTPL2 are treated alike" (record line 72) is honoured.
- leak_checks.md Cases line 441 (LEAK-10, LEAK-7, LEAK-41; Andrej 2026-11-02, amended Lennart 2026-11-06): where the cut cannot be located and the amount is the denominator of a count target, the rate ships with the amount as weight, never as a feature. bemtpl97 is listed there as a denominator case, and the definition matches the row.
- Same-day siblings that reverse earlier keeps of realized exposure for the same reason:
  - australian_vehicle_insurance_2004_2005 (Andrej's keep of 2026-11-02 reversed; metrics.md line 315)
  - spanish_motor_insurance_coverage_level_2022_2024 (Andrej's keep of 2026-11-02 reversed; line 318)
  - frempl_french_motor_personal_line and pricing_game_2016_french_fleet (lines 316-317)
  
  All four tables that had kept a realized exposure as a feature are now decided alike, so no opposite-outcome pair remains in the exposure family.
- Why the per-contract precedent does not apply (spanish_motor_insurance_2015_2018, MET-14 per-contract clause, Lennart, 2026-11-06, metrics.md line 319). That table keeps a per-contract target because every first year has a planned term of exactly one calendar year. In bemtpl97 the term inside 1997 varies (mid-year starts as well as surrenders), and the two cannot be told apart (curation_comments, Exposure bullet). Same for pricing_game_2017_french_mtpl (whole policy-years, no exposure column).
- LEAK-41's "a part known at the start ships as its own column": the start part cannot be located without dates. That matches fremtpl2 and differs from frempl and pricing_game_2016, whose dates locate it. The definition says so.
- CLEAN-16 as amended: a deviance-scored rate ships untransformed, and nclaims_per_year is on the identity scale. Consistent.
- MET-11: origin source holds, because models rank the same as under Henckaerts et al.'s Eq. 5 count deviance on every fold (verified above).

Minor, not a departure: the target name. bemtpl97 uses `nclaims_per_year`, as do australian (`claim_cost_per_year`), pricing_game_2016 (`claim_charge_per_vehicle_year`), frempl (`log1p_claim_amount_per_year`) and spanish_coverage_level (`log1p_incurred_per_exposure_year`). fremtpl2's `claim_frequency` is the one outlier in the family. No rule covers this, so it is not a consistency issue. If Lennart wants one spelling, fremtpl2 is the one to rename.

**Decision 2: reversal of Myunghwan's CC of 2026-10-23 ("Retain expo, the recorded time insured ... Do not annualize, bin, clip, weight or add row filters"; record line 50)**

Status: departs, with a stated reason.

- What sets it apart, as written in the record (line 92) and in curation_comments:
  - The conditional measurement came after his call: part-year policies claim about 1.4 times what a proportional offset expects, and a free expo gains +0.0043 (17% of the skill) and is 0.0002-0.0011 worse at quotation.
  - The source itself scores with an offset.
  - With the weight, dividing by expo no longer inflates short records.
- His call rested on the proportional part ("longer coverage permits more claims"), which the rate form keeps.
- His own line already said "Realized exposure may reflect cancellation and is not verified as quotation-time information". The new fact settles a doubt he recorded; it does not contradict a fact he relied on.
- It is not drift: a newer curator decision beats an older one (principles.md, "Precedence in the process", Who decides), and the change comes with new Musts (LEAK-41, MET-15) adopted on purpose the same day.
- Myunghwan's "no clipping" had already been overruled by Lennart's floor of 2026-11-04, which is unchanged in substance.

**Decision 3: reversal of Myunghwan's CC of 2026-10-26 (mean_poisson_deviance on the original nclaims, "expo as a predictor; no annualization, target transformation, weighting"; record line 56)**

Status: departs, with a stated reason; the part he decided on purpose is kept.

- His quoted reason, "expected claim count should matter, so poisson deviance ... might be better", is kept.
  - The shipped metric is still the source's Poisson deviance on expected counts, up to a per-fold constant (1.123-1.125), so every model ranks as it would under his metric. My check above shows this exactly.
- Only the form (count against rate) and expo's role change, for the reasons given under Decision 2.
- "No weighting" in that line is the AI's paraphrase of what he left unchanged, not his own words. The reversal therefore overrules no argument he gave.

**Decision 4: reversal of the floor of 2026-11-04 (Lennart: min_prediction=1e-6 on the expected count; record line 76), now 1e-4 claims per year on the rate**

Status: consistent; a deliberate amendment, not drift.

- It is the same curator two days apart, but the rule was changed on purpose: MET-13 was amended on 2026-11-06 with this case named ("two orders below the smallest plausible mean, on the scale the metric scores ... 1e-4 claims per year on fremtpl2 and bemtpl97").
- The principle of 2026-11-04 is unchanged; only the scale moved from count to rate.
- On the count scale, 1e-6 had meant a different floor for each row on the rate scale (1e-6 to 3.65e-4 a year, depending on expo). The new floor is the same for every row.
- Measured:
  - The smallest honest predicted rate is 0.008-0.010 a year (0.1% quantile 0.020-0.023), so 1e-4 is about two orders below it, as MET-13 asks.
  - The task probe reports 0.0% of predictions at the floor for every model family.
- The same floor is used for fremtpl2 (portfolio rate 0.074), so like cases are decided alike.

Bookkeeping (no finding): the 2026-11-06 CC lines name what they supersede, but Myunghwan's lines 50 and 56 and the floor line 76 carry no inline "(superseded 2026-11-06: ...)" note. Some 2026-11-04 lines do carry such notes. fremtpl2 and australian are handled the same way as bemtpl97 (0 inline notes of 2026-11-06 in any of the three), and records.md sets no rule on it. So the three are consistent with each other; add the inline notes only if Lennart wants that habit kept.

**Departure without a stated reason: the reporting clause of LEAK-41 (Must)**

LEAK-41 says: "For each suspect column the definition reports its gain on the declared metric with an L2 fit on the shipped scale and with the weighted actuarial fit, and decides on the worse; it states the score of 1/weight alone as the ceiling a leak would reach."

- These siblings report both numbers:
  - australian_vehicle_insurance_2004_2005 (an L2 LightGBM and "1/exposure alone")
  - pricing_game_2016_french_fleet (L2 fit)
  - frempl_french_motor_personal_line (1/Exposure alone 0.184)
- bemtpl97 reports only the Poisson-fit gain (0.0036-0.0041; +0.0043 in the CC) and states neither number. fremtpl2 has the same gap.
- The outcome stands either way, since expo is out of the features. What is missing is the record of the check.

Draft in the review-file shape:

**Report the L2 gain and the weight-alone score of `expo`, as LEAK-41 asks, in bemtpl97 and fremtpl2?**

* **Problem:**
  - LEAK-41 asks every definition to report the suspect weight's gain under an L2 fit and under the weighted actuarial fit, and the score of the weight alone as the ceiling a leak would reach. australian_vehicle_insurance_2004_2005, frempl_french_motor_personal_line and pricing_game_2016_french_fleet do; bemtpl97 and fremtpl2 give only the Poisson-fit gain.
  - The numbers exist for bemtpl97:
    - probe 22: expo as a feature gains +0.0040 (SD 0.0008) under the weighted Poisson fit and +0.0035 (SD 0.0027) under L2, so the actuarial fit is the worse and decides.
    - expo alone (a fit on expo only) beats the training-rate constant by 0.0051 to 0.0079 mean deviance (3 folds).
    - a scaled 1/expo is no better than the constant (0.6223 against 0.6233).
  - Probe 22 computes "1/weight alone" only for a Gini, so for a deviance the rule's ceiling has no defined form yet.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Distinguishing fact: under a deviance a "1/weight alone" ceiling is not defined (a scaled 1/expo scores at the constant), so add only the L2 gain to both notes and amend LEAK-41 to say the ceiling is the weight alone fitted to the target (or 1/weight for a rank metric) | makes the rule computable for every metric; two sentences per definition | an amendment of a Must for a wording point |
  | b | Treat bemtpl97 and fremtpl2 like the three siblings: add the L2 gain and the score of expo (Exposure) alone to both notes, as the rule reads today | follows the rule as written; no rule change | "1/weight alone" has to be read as "the weight alone" for a deviance without the rule saying so |
  | c | Leave as is: expo is out of the features, so the decision does not depend on the numbers | no work | a Must's reporting clause stays unmet on two of six definitions, with no exception possible under a Must |

* **Recommendation:** (a). The numbers are already measured, and stating the ceiling per metric type keeps the six insurance definitions reporting the same thing.

Footnotes of the draft:

- **LEAK-41** (Must; 2026-11-06, Lennart, on fremtpl2 and bemtpl97): the reporting clause on the L2 and actuarial gains and the 1/weight ceiling; probe 22 (leak_checks.md, the probes table) computes 1/weight only for a Gini.
- **MET-13** (Must; amended 2026-11-06): the floor two orders below the smallest plausible mean on the scored scale; measured above as met.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief: bemtpl97 (exposure re-review, 2026-11-06, full tier)**

Position: ship as defined. The data, target, weight, metric, floor and split stay as they are. Before the build, the notes need a few added or corrected sentences. One of them is a Must (the LEAK-41 reporting clause). It is a documentation gap and the numbers it needs are already measured. Expected verdict: "ship after changes", with no change to the data.

1. The only validity problem the dataset had is fixed, and no feature brings it back (P4; LEAK-41 Must, LEAK-10 Must).
   - Evidence that expo is gone from the inputs:
     - It is no longer among the features. feature_columns gives the 11 rating factors, sample_weight is 'expo' and the metric input is {'weight':'expo'} (claim auditor, claims 2 and 14).
     - No model is trained or scored on rows chosen by expo; all 163,231 rows are in every split.
   - Evidence that no feature stands in for it:
     - The 11 features predict expo only weakly: R² 0.03 under the probe's 50k cap and 0.055 on full folds.
     - The gain that runs through the weight is within noise for every feature, under both the Poisson fit and the L2 fit (column auditor; claim auditor claim 9).
   - All features are registered at policy start (binning manuscript Sec. 2). The column auditor checked bm on the data: bm 0 has 5,215 claimants, so it is the start-of-year level.
   - Where postcode, bm, age and agec predict expo, they do so through risk selection on attributes fixed at the start. LEAK-41 and USE-6 keep such features explicitly.
   - Why this outranks any objection: this was the P4 Must that had kept the dataset parked (REVIEW issue 1). Every evidence agent says it is now resolved: the claim auditor, the column auditor, the split auditor, the domain practitioner, the precedent checker, and the blind reviewer ("no leaks").

2. The metric is the source's own metric, scored on the unit the decision acts on (P6; MET-1, MET-11, MET-13, MET-14, MET-15).
   - Identity with the source: the weighted rate deviance equals Henckaerts et al.'s Eq. 5 count deviance (treeML.Rmd L641-657) times n/sum(expo). That factor is 1.1229 to 1.1254 per fold. The identity is exact on all 9 folds, so models rank exactly as under the source's metric (claim auditor claim 3; precedent checker).
   - The floor never binds:
     - The floor is 1e-4. The lowest honest predicted rate is 0.008 to 0.045, which puts the floor 2.3 to 2.7 orders below.
     - 0 of 489,693 test predictions fall below 1e-3, and 0.0% of predictions sit at the floor for every probe family.
     - NaN and inf raise an error.
   - The weighting is right for pricing:
     - Without the weight the mean rate is 1.13 times the portfolio rate, and an unweighted fit is 0.0066 to 0.0114 worse.
     - Actual/expected is 0.89 to 0.94 without the weight and 0.98 to 1.01 with it (domain practitioner).
   - The practitioner says: "The metric I would choose is the declared one, unchanged."
   - Answer to the blind reviewer's concern 1: they asked for exposure-weighted Poisson deviance, which is exactly what ships. They could not see it because the clean-room task.md does not name the metric. That is a gap in the clean room's wording, not in the definition.

3. The split mirrors the application, and its one limit is disclosed (P4; SPLIT-1, SPLIT-8 Must satisfied, SPLIT-29/30).
   - The data is one undated year with raw rows sorted by postcode, so no time window can be built. The forced-IID cost is disclosed in curation_comments, task_summary.split and fit=approximate.
   - Train and test match on expo for every fold:
     - mean expo: 0.889 to 0.890 in train, 0.889 to 0.891 in test;
     - KS p-values: 0.67 to 1.00;
     - weighted claim rate: 0.1385 to 0.1403 in train, 0.1374 to 0.1411 in test.
   - Postcode as a hidden group:
     - Grouping the split by postcode costs honest models only 0.0004 to 0.0015 of skill.
     - The LightGBM-over-GLM ranking holds: 9/9 folds under IID, 7/9 grouped.
     - Scored on full-year rows only, the ranking is the same as on all rows.
   - Copies give no shortcut: 0.4% of test rows have a train copy, and same-label copies are mostly both zero claims.
   - Possible re-issued policies (57 to 176 pairs whose exposures sum to one year) share no claims (0.0% to 1.1%).
   - Mildest remedy for the re-issued pairs: an optional clause in the copies bullet. No re-split.

4. The signal is real; the no_signal flag reads the wrong scale (P6; TP-2 Should "small real signal: keep"; EV-3).
   - The probe's "skill +0.015" is its RMSE skill (equal to R² 0.015). On the declared metric:
     - probe LightGBM: 0.6004 against the dummy's 0.6199 (3.1%);
     - claim auditor's weighted Poisson fit: 3.46% (3.27% to 3.68%), better than the constant on 9/9 folds.
   - The decile spread is 3.4 to 3.8 times and the ordered Lorenz Gini 0.207 to 0.212 (domain practitioner).
   - For MTPL frequency this is the normal size of the signal, since individual claim counts are mostly Poisson noise. The blind reviewer independently judged that it "still separates methods".
   - Remedy: one line in REVIEW.md that reads the flag. No change to the task.

5. Like cases are decided alike, and every reversal names the fact that sets it apart (Principles, Conflicts: "treat like cases alike"; Who decides).
   - fremtpl2 has the same facts and gets the same treatment: rate target, exposure as the weight, mean_poisson_deviance, floor 1e-4, ForcedIIDFromTemporal, fit approximate.
   - The four sibling tables that had kept realized exposure as a feature were reversed the same day for the same reason, so no pair with opposite outcomes remains.
   - The per-contract exception (spanish_motor_insurance_2015_2018) does not apply. Its planned term is one calendar year; bemtpl97's term varies and cannot be told apart from surrenders.
   - The reversals of Myunghwan's calls of 2026-10-23 and 2026-10-26 rest on a later measurement. Part-year rows claim at an actual/expected of 1.42 against the offset model's expectation; the claim auditor reproduced this. His own line had already flagged expo as unverified at quotation, and his choice of Poisson deviance is kept.
   - The register raises no flag on bemtpl97 (precedent checker).

6. The task gamer's only exploit is not a defect of the definition (P4 LEAK-41; house API in definitions.md).
   - The gamer's finding: test-row expo in scoring.parquet, used as a feature, gains 0.0052.
   - Why it is not a definition defect:
     - The definition already declares expo a scoring column of role weight. feature_columns drops it, and the API says a scoring column is "never a feature". Every dataset with a weight or a group-scored metric works this way.
     - The gamer's own table says a deployed model does not have this input.
     - Using it breaks the declared protocol; it is not a gap in the dataset. Whether participants see the test-row weight is a question for the harness and the kit, across all such datasets.
   - The gamer's alternative fix ("keep only full-year test rows") is forbidden by LEAK-41's own Must: "No model is trained or scored on rows selected by the realized weight". The gamer also showed that dropping short rows from training makes an honest model worse (0.60106 against 0.59913).
   - Mildest remedy: none in the definition. If wanted, a harness-level note that scoring columns are withheld or must not be used as inputs. That is a house matter, outside this dataset.

7. What I concede, and the mildest fix for each. None of these touches the data.
   - (a) LEAK-41 reporting clause (Must, P4): not met in the text. The claim auditor and the precedent checker both flag it.
     - The decision does not depend on it. Expo gains under both fits on the declared metric: +0.0051 (SD 0.0007) under L2 and +0.0047 (SD 0.0006) under weighted Poisson, 9/9 folds. Probe 22 at its cap gives +0.0035 and +0.0040.
     - 1/expo alone scores 0.6122, against the training mean's 0.6193 and the honest model's 0.5979.
     - Remedy (fix the definition's notes, the second rung of the remedy ladder): one sentence with these numbers, and a label on the old 0.0036-0.0041 / 0.0039 / +0.0043 figures saying they are count-scale fits with expo free.
     - The precedent checker found the same gap in fremtpl2. Whether "1/weight alone" needs amending for a deviance metric (their option a) is a call for the curator, not grounds to hold this dataset.
   - (b) Stale numbers (writing, EV-2):
     - The copies bullet should read 397 extra exact rows and 88 conflicting profiles (177 rows); "50" counts profiles, not rows.
     - The skill should read 0.5979 against 0.6193 (3.46%), replacing 0.5279 against 0.5520.
     - The probe 22 R² should name its cap (full folds give 0.055).
     - The REVIEW.md outcome block and the record's priority "risk" factor describe the state before the change.
     - Remedy: text edits.
   - (c) Postcode as a 583-level nominal category (P7, CLEAN-14 Should; low): the column auditor and the split auditor note that untuned LightGBM overfits it.
     - Keeping it nominal follows settled precedent (house_sales, melbourne_housing_market, perth_house_prices) and the earlier panel's call.
     - long and lat already carry the location.
     - Types are decided from meaning, not from model runs (EV-4, dtypes-from-context).
     - At P7, a cheap note is the right remedy: a README line that a 583-level code needs encoding or smoothing, as the source smooths it in space.
     - It does not outrank anything above, and it was not reopened by today's change.

Judgment record as I would write it:
- Verdict: ship after changes (notes only).
- Validity: LEAK-41 triggered and fixed (expo is the weight, never a feature); its reporting clause is to be added to the notes. LEAK-10 holds. SPLIT-8 holds, cost disclosed. SPLIT-29/30 no hit.
- Value: TP-2, a small real signal (3.46% deviance skill, 9/9 folds); MET-11, the source's metric (exact identity); MET-13, the floor never binds; MET-15, the weighting is right.
- Quality: CLEAN-14, postcode nominal kept with a note.
- For the curator: (1) LEAK-41's "1/weight alone" wording for deviance metrics (shared with fremtpl2); (2) the harness policy on scoring columns in participant kits.

Sources: the panel's reports (claim auditor, column auditor, split auditor, domain practitioner, precedent checker, blind reviewer, task gamer) and the task probe; the rules in principles.md, leak_checks.md (LEAK-41) and task_probes.md (TP-2).

</details>

<details><summary>Critic</summary>

**Critic, opening brief: bemtpl97 (exposure re-review, 2026-11-06, full tier)**

Position: ship only after changes. None of my points is a reason to exclude. Today's change to the target, the weight and the metric holds up under every audit: the target rebuilds the integer counts exactly, expo is out of feature_columns, and the weighted rate deviance equals the source's Eq. 5 count deviance times n/sum(expo) (1.1229-1.1254 on every fold). What I ask for is mostly notes the definition owes under a Must, plus one quality call. Points are in rank order.

1. LEAK-41's reporting clause is not met (P4, Must).
- Problem: LEAK-41 says the definition "reports its gain on the declared metric with an L2 fit on the shipped scale and with the weighted actuarial fit, and decides on the worse; it states the score of 1/weight alone". The Exposure bullet and the CC give only Poisson count-scale gains with expo as a free feature (0.0036-0.0041, 0.0039, +0.0043). Those come from the old task. There is no L2 number and no weight-alone score.
- Effect: the decision stands, because both fits show a gain. But the evidence the Must asks for is missing, and the reader cannot check "decide on the worse".
- Evidence: claim auditor claim 10 (REFUTED). On the declared metric over 9 folds, expo gains +0.0051 (SD 0.0007) under weighted L2 and +0.0047 (SD 0.0006) under weighted Poisson, so L2 is the worse fit. 1/expo alone scores 0.6122 against the training mean's 0.6193 and the honest model's 0.5979. Probe 22 (50k cap) gives +0.0040 / +0.0035. The precedent checker finds that australian_vehicle_insurance_2004_2005, frempl_french_motor_personal_line and pricing_game_2016_french_fleet report these numbers, and that bemtpl97 and fremtpl2 do not. A Must has no exceptions.
- Remedy (note): add one sentence with these numbers to the Exposure bullet, and mark the old figures as count-scale fits with expo free. Precedent checker issue draft, option (a) or (b). If the curator takes (a), "1/weight alone" for a deviance should be read as "the weight alone fitted to the target", which scores 0.0051-0.0079 better than the constant.

2. Test-row expo sits next to the features (P4, LEAK-41 Must, "never a model input"; the definition meets it, the shipped bundle invites breaking it).
- Problem: expo is a scoring column, so it stays in the frame for test rows too. The participant kit ships it in scoring.parquet.
- Effect: one line of code puts the realized exposure, partly set by the outcome, into a model. That gains 0.0052 (0.0039-0.0061 per split), about 15% of the honest skill, and no deployed model at the quote has this value.
- Evidence: task gamer exploits 1-3: expo or 1/expo as a feature 0.59396 against 0.59913; an expo<1 flag 0.59467; a train-learned per-expo-bin factor 0.59503. The noise check moves the score by 0.00005.
- Remedy (note; this is protocol-wide, not a definition change): one line in the README's Training weight section. The harness passes expo only as sample_weight on training rows and to the scorer, never as a model input, and test-row expo is the scorer's alone. Also raise it for the curator as a cross-cutting issue for every weighted dataset (fremtpl2 and the four other insurance tables): either withhold test-row weights from what participants see, or document it.

3. The task probe's no_signal flag is not explained (P6, TP-1/TP-2, EV-3).
- Problem: probes/task.txt flags no_signal. Its "skill" is the RMSE-based R² (0.015). It also prints two "best family" lines (linear by RMSE, lightgbm by the declared metric). No REVIEW.md line reads the flag, and the definition states no current skill. The 4.4% skill in the notes is on the count scale with expo free (claim 24).
- Effect: a curator reading the probe sees "no signal" on a task whose real signal is small but real. random_forest scores worse than the dummy (-0.013).
- Evidence: on the declared metric the deviance skill is 3.46% (3.27-3.68%), 9/9 folds (claim auditor), and 3.1% from the probe's own numbers (0.6199 to 0.60043). The domain practitioner finds a 3.4-3.8x spread between the top and bottom deciles and a Gini of 0.207-0.212.
- Remedy (note): a REVIEW.md line, "no_signal reads RMSE skill; declared-metric skill 3.46%, 9/9: TP-2 small real signal, keep". Replace the stale 0.5279/0.5520 in the notes with 0.5979/0.6193.

4. postcode as a 583-level nominal category, digits geographic (P7, CLEAN-14, Should; quality only).
- Problem: Belgian postcodes are hierarchical by province (1xxx Brussels, 2xxx Antwerp, ... 9xxx East Flanders). CLEAN-14's last clause keeps a code numeric "when its digits carry meaning a model can use (zip code prefixes...)". lt_vehicle_loan_default_prediction (2026-11-05) shipped a code ordered by geography as a number. house_sales zipcode and the earlier panel's call went nominal. The source does not use the 583 levels as such: it smooths location in space (Sec. 4.1).
- Effect on the benchmark (stated as effect, not as the reason for the type; EV-4): an untuned LightGBM with the native category falls from 0.0342 to 0.0063 skill, 0 of 9 folds better (split auditor). As a number it scores 0.59770 against 0.60851 as a category (column auditor, 12/12). The ranking then partly measures how well a method handles high-cardinality categories, which is the gain the domain practitioner says he would distrust.
- Remedy (mildest): the curator decides CLEAN-14's digit clause against the lt_vehicle_loan precedent, from context. If postcode stays nominal, add a README note that it is a geographic code with long/lat as its centroid and needs encoding or smoothing, as the source does.

5. Stale and mixed-scale numbers in the notes (writing, EV-2).
- Copies kept: the bullet says "176 extra exact rows and 50 rows with a conflicting profile". Those counts are on the old basis (expo a feature), and the 50 are profiles (100 rows). With expo out it is 397 extra exact rows and 88 conflicting profiles (177 rows) (claim 22, REFUTED).
- Exposure gain: +0.0043 (CC, leak_checks Cases row) and 0.0039 (bullet) are on different scales, and neither says which (claim 23).
- Probe 22: expo R² 0.03 is the 50k-cap figure. On full folds it is 0.055 (Spearman 0.24) (claim 9).
- The REVIEW.md outcome block (floor 1e-6, LEAK-10 triggered, 4.2-4.4% skill) and the record's priority, which rests on the now-resolved "risk: issue 1", describe the old state (claims 30-31).
- Remedy: update the numbers, name the scale on each, and let the new panel block supersede the old outcome. The next assessment can revisit the priority (Weigh).

6. "Each row is a distinct policyholder" is not quite shown (P4, LEAK-16/SPLIT-29, Should; negligible effect).
- Problem: among same-profile pairs of part-year rows, 57 strict pairs (176 loose pairs, 114-352 rows) have exposures that sum to one year. That is 15.1% of 2-row profile copies against 2.8% of random same-postcode pairs, which points to a policy re-issued during 1997 under a new ID.
- Effect: 45-47% of the pairs straddle train and test, but their outcomes are not shared (0.0% / 1.1% both claim). No optimism.
- Remedy (note): one clause in the Copies kept bullet, as the split auditor words it. The task_summary "row" may keep its wording.

Not raised, because the evidence does not back it:
- The blind reviewer's MSE worry: the metric is already the weighted Poisson deviance.
- The outcome-cut part-year rows: the LEAK-41 case row settles this, and on full-year test rows only the ranking is unchanged (split auditor).
- The forced IID split: SPLIT-8 is disclosed.

Requested verdict: ship after changes.
- Validity: LEAK-41 holds in substance, but its reporting clause is unmet (Must, fix with a note: point 1); a test-weight note goes to the harness (point 2).
- Value: TP-2 small real signal, with the flag's reading recorded (point 3).
- Quality: CLEAN-14 postcode is a curator call or a note (point 4); points 5-6 are notes.

Sources: the panel's reports (claim auditor, column auditor, split auditor, domain practitioner, precedent checker, blind reviewer, task gamer) and the task probe; the definition's dataset.py; the rule text in leak_checks.md (LEAK-41) and principles.md.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate rebuttal: bemtpl97 (exposure re-review, 2026-11-06)**

The critic and I want the same verdict: ship after changes, with notes only and no change to the data. I concede five of the six points with the critic's remedies, and part of point 4. On point 4 I dispute only one thing: that the curator should consider shipping postcode as a number.

1. LEAK-41 reporting clause (P4, Must). I concede this in full, as in my opening point 7a.
   - What follows: the definition is not ready to build until the Exposure bullet carries the declared-metric numbers. These are the L2 gain of +0.0051 (SD 0.0007), the weighted Poisson gain of +0.0047 (SD 0.0006), and 1/expo alone at 0.6122 against the training mean's 0.6193 and the honest model's 0.5979. The old figures need their scale named.
   - One precision for the note: which fit is "the worse" depends on the run.
     - On full folds (claim auditor), L2 is worse.
     - Under probe 22's 50k cap, Poisson is worse (+0.0040 against +0.0035, the precedent checker's reading).
     - The note should give both runs and state that both fits show a gain. "Decide on the worse" then excludes expo either way, so the order between them does not matter.
   - The wording of "1/weight alone" for a deviance (precedent checker, option a or b) is the curator's call and shared with fremtpl2. It does not block bemtpl97.

2. Test-row expo next to the features. I concede the README line and the cross-cutting issue for the curator.
   - What follows: one sentence in the Training weight section. Expo is passed as sample_weight on training rows and to the scorer, never as a model input.
   - I dispute only the placement, and I believe the critic agrees. The definition meets LEAK-41: expo is a scoring column, and feature_columns drops it (definitions.md: a scoring column is never a feature). Withholding test-row weights from the kit is a harness decision that covers every weighted dataset. It is not a defect of this definition, and it is not a reason to hold bemtpl97.

3. Reading of the no_signal flag (P6, TP-2, EV-3). I concede this. It is the same as my opening point 4.
   - What follows: the REVIEW.md line the critic drafted, and 0.5979/0.6193 (3.46%, 9/9 folds) in place of 0.5279/0.5520.
   - random_forest scoring -0.013 is an untuned forest overfitting noise. TP-2's own row on no_signal says so ("Untuned models overfit noise"). It does not count against the signal.

4. Postcode as a nominal category (P7, CLEAN-14 Should). I concede the README note and dispute the alternative of shipping it as a number.
   - Concede: add a README note that postcode is a geographic code, that long/lat are its centroid, and that it needs encoding or smoothing, as the source smooths location (Sec. 4.1).
   - Dispute: CLEAN-14's digit clause asks whether the digits carry meaning "a model can use". Here they add none.
     - long and lat give each of the 583 municipalities its exact location, one value per postcode in both directions (column auditor).
     - The province that the leading digit encodes is a coarse function of those coordinates, so a numeric postcode adds no place information the frame lacks.
     - That fact sets bemtpl97 apart from lt_vehicle_loan_default_prediction. The precedents with a coordinate pair or comparable settings went nominal: house_sales zipcode, melbourne_housing_market, perth_house_prices, and this dataset's own earlier panel. Under "treat like cases alike" (principles, Conflicts), the nominal type stands.
   - The critic's effect numbers (0.0342 to 0.0063 skill; 0.59770 against 0.60851) are untuned-model behaviour. EV-4 and dtypes-from-context forbid deciding a type from them, and the critic says so.
   - The domain practitioner's distrust of "a gain that rests on the 583 postcode levels" is an argument for the note. A method that memorises 583 levels is penalised by the metric, as the split auditor shows: it costs skill and gives no optimism. Measuring that is legitimate.
   - What follows: keep nominal and add the note. The curator may still revisit the clause, but it is a P7 Should and outranks nothing above.

5. Stale and mixed-scale numbers (writing, EV-2). I concede all of these. They are the same as my opening point 7b.
   - What follows:
     - Copies kept: 397 extra exact rows and 88 conflicting profiles (177 rows), counted as profiles.
     - Each exposure gain is labelled with its scale.
     - The probe 22 R² names its cap (0.055 on full folds).
     - The new panel block supersedes the old outcome, and the priority is revisited at the next assessment.

6. "Each row is a distinct policyholder" (LEAK-16, SPLIT-29, Should). I concede the optional clause.
   - What follows: one clause in the Copies kept bullet, worded as the split auditor has it.
   - No re-split is needed. The pairs share no outcomes (0.0% of strict pairs and 1.1% of loose pairs both claim), and the effect is nil (SPLIT-30).

Net: the critic raises no point that touches the data, target, weight, metric, floor or split. Every remedy is on the notes rung of the remedy ladder or with the harness. The judgment record stays as in my opening brief, with three additions: the README note on test-row weights, the README note on postcode, and the clause on copies.

Sources: the critic's brief and the panel's reports; the rules in principles.md, leak_checks.md (LEAK-41) and task_probes.md (TP-2).

</details>

<details><summary>Critic rebuttal</summary>

**Critic rebuttal: bemtpl97 (exposure re-review, 2026-11-06)**

Overall: the advocate and I mostly agree. We both want "ship after changes", with notes only and no change to the data, and we both treat the LEAK-41 reporting clause as an unmet Must that a note fixes. Below I go through the advocate's seven points: what I concede, and the two places where we differ (points 6 and 7c).

1. Validity fixed, no feature brings expo back: concede.
- The audits support it. expo is not in feature_columns. Every feature's gain through the weight is within noise under both fits. The features predict expo at R² 0.03 (capped) to 0.055 (full folds), through risk selection on factors known at the start (LEAK-41, USE-6).
- One correction to "this outranks any objection": LEAK-41 is one Must, and its reporting clause is part of it. "Every Must has to hold" (principles, How to decide, step 4). The advocate's own 7(a) accepts this, so it only affects how the record is worded, not the verdict.

2. Metric: concede.
- The identity with Eq. 5 is exact (factor 1.1229-1.1254). The floor never binds. The weighting is right (MET-11, MET-13, MET-14, MET-15).
- I raised nothing here; I set aside the blind reviewer's MSE worry for the same reason the advocate gives.

3. Split: concede.
- SPLIT-8 is disclosed, and SPLIT-29/30 have no hit.
- On the re-issued pairs: the advocate calls the clause "optional", I asked for a note. Both are fine. I still ask for the clause, because the Decision text "Each row is a distinct policyholder" is a claim, and 57-176 pairs whose exposures sum to one year make it less than certain (LEAK-16, Should). It costs one clause.

4. Signal real, no_signal flag on the wrong scale: concede.
- The remedy is the same as my point 3: one REVIEW.md line, and the 3.46% skill (0.5979 against 0.6193) replacing the stale 4.4%.

5. Like cases alike: concede.
- The precedent checker finds every reversal grounded and no register flag. The siblings agree, except for the reporting clause shared with fremtpl2 (point 7a).

6. The gamer's exploit is not a defect of the definition: concede in part.
- Conceded:
  - The definition meets LEAK-41: expo is a scoring column, and feature_columns drops it.
  - The gamer's "full-year test rows only" fix is forbidden by LEAK-41's own clause. I did not ask for it.
  - The advocate already lists the harness policy for the curator. That covers the cross-cutting issue I asked for.
- Disputed: "Mildest remedy: none in the definition".
  - The README's Training weight section is generated from the definition (the scoring column's description), and it is what a user of the container reads. It already says expo is "never a feature".
  - What it does not say is that test-row expo belongs to the scorer alone, not the model.
  - The gain from misusing it is 0.0052, about 15% of the honest skill (task gamer, 9 splits). That is larger than any other exploit and well above the noise (0.00005).
  - One clause in the scoring column's description ("test-row values are for the scorer only") is the mildest remedy that works.
  - The rule that backs it is LEAK-41 (Must, "never a model input"), applied to the shipped bundle as well as to the feature list. If the curator prefers to settle this once at harness level, I accept that in place of the clause.

7. Concessions:
- (a) LEAK-41 reporting: agreed in full, including the numbers and labelling the old figures as count scale with expo free.
- (b) Stale numbers: agreed in full. Add the mixed scales of +0.0043 against 0.0039 (claim 23), which should name their scale.
- (c) postcode: agree on rank (P7, Should, not a reason to hold the dataset) and on the README note as the remedy. I dispute only "settled precedent".
  - The closest precedent with the same fact went the other way: lt_vehicle_loan_default_prediction (2026-11-05) shipped a code ordered by geography as a number under CLEAN-14's digit clause.
  - The house_sales, melbourne and perth precedents predate it.
  - Under "treat like cases alike" (principles, Conflicts), keeping postcode nominal needs the fact that sets it apart to be written down.
  - The advocate names that fact: long and lat carry the location, one pair per postcode. That is a sound distinguishing fact, and it comes from the data's meaning, not from model runs (EV-4).
  - My ask therefore narrows: a CLEAN-14 line in the Dtypes bullet, "postcode nominal despite its province digits, since long/lat give each municipality's location (unlike lt_vehicle_loan_default_prediction)", plus the README encoding note. No change of type unless the curator wants it.

Agreed judgment record:
- Verdict: ship after changes (notes only).
- Validity: LEAK-41 triggered and fixed; its reporting clause is added to the notes (Must). LEAK-10 holds. SPLIT-8 holds, cost disclosed. SPLIT-29/30 no hit.
- Value: TP-2 small real signal (3.46%, 9/9), with a REVIEW.md line that reads the no_signal flag. MET-11, MET-13 and MET-15 hold.
- Quality: CLEAN-14 postcode kept nominal, with the distinguishing fact and an encoding note. The stale counts, scales and skill are updated. The re-issued-pairs clause goes in.
- Still disputed:
  - The test-row expo clause in the scoring column's description (my ask) against a harness-level policy only (the advocate's).
- For the curator:
  - (1) LEAK-41's "1/weight alone" wording for deviance metrics (shared with fremtpl2).
  - (2) The harness policy on scoring columns in participant kits; if adopted, it replaces the disputed clause.

Sources: the advocate's brief and the panel's reports; principles.md and leak_checks.md.

</details>

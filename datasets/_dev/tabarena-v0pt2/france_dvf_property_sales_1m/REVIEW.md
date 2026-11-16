# france_dvf_property_sales

**Outcome:** added as `france_dvf_property_sales_1m`. The task: France's register of property sales (DGFiP's DVF, in Etalab's geolocated copy): one sale of one existing house or apartment, January 2023 to October 2025, the declared price on a log scale scored by RMSLE; 2,185,254 sales (1,653,624 shipped after sampling the train sides), 20 features; three 3-month test windows (194,513 to 217,561 sales), each training on a random 1M of the sales up to one month earlier. The AI recommends shipping it: the review panel's changes are made, and three calls are left to you, with the AI's recommendation implemented in each: issue 1 names a tax-office valuer who checks the declared price as the deed is published, the actor the one-month gap fits; issue 2 keeps the April 2026 data now and re-sources to the October 2026 release as a later version; issue 3 keeps the cadastral section. Changes made, needing no decision: off-plan sales (VEFA) are dropped, since their dwelling enters the land register only once the building is finished, after the sale (33,807 sales); declared prices of 1,000 EUR or less are dropped as amounts that are not the price of a dwelling (3,213 sales; the filter and the count read the price before the log); the year is 2026, the release we pin (the register grows; 2019 was its first publication); the download text names Etalab's release of 2026-10-20, says that the folder we read is deleted on 30 November 2026, and gives the archived raw files with their sha256 values; the licence adds the terms' clause that a reuse must serve the transparency of property markets, and the notes say a row is as identifying as the published record, no more; impossible coordinates (62), room counts (294) and Carrez (private floor) areas that contradict the floor area (390) are set missing by fixed rules; the notes' counts and wording are corrected (low prices on the raw price, the dwelling lines a sale can hold, twin units against resales, how fast deeds are recorded), and the split's comment says why the shipped file holds about two thirds of 2023-2024 and all of February to October 2025 (the 1M sample of each train side), and that a model which counts same-day sales over the test rows (worth 0.003 to 0.005 RMSLE) is called out.
Verdict: ship after changes (made).
Validity: SEL-1 holds (the terms' (CGU) bar is met with or without the coordinates: a row links back to its published record at 99.9% either way; the purpose clause and the privacy wording are added); USE-1 and USE-3 triggered (a lender or notary prices at the compromis (the preliminary contract), about 3 months before the deed, which gap 1 does not cover), fixed by the tax-office actor (issue 1, A, implemented; B, gap 3, also fixes it); USE-5 triggered, fixed (declared prices of 1,000 EUR or less dropped: the 100-1,000 EUR band sits at a median 0.3% of the local price level, as the band below 100 EUR does); LEAK-10 triggered, fixed (VEFA dropped); LEAK-16 holds (143 kept sales hold more than one dwelling line, under 0.01%); LEAK-5 and LEAK-9: counts of same-day sales over the test rows are worth 0.003-0.005, a protocol line, no data change; SPLIT-1, SPLIT-6 and USE-10 hold (temporal, known places); SPLIT-10 holds for the publication delay (cut and gap 1, measured); SPLIT-14 holds (train pools 69.0-86.3% before sampling); PROV-9 triggered, fixed (2026); PROV-8 holds (download text corrected, archive with sha256).
Value: TP-1 to TP-10 no flag (random forest RMSLE 0.454 against the dummy's 0.774, better on 3 of 3 windows, R^2 0.655; 194,513 to 217,561 test rows a window); MET-11 `rmsle` from context on a log target, as the house-price family.
Quality: CLEAN-11 masks by fixed rules within the row (CLEAN-7): 62 coordinates outside their territory's box, 294 room counts under 4 m2 per room, 390 Carrez areas that contradict the floor area; CLEAN-14 `code_section` kept with a verified fact (issue 3).
Weighed (priority 2): gap 0 (no thin domain, problem type or regime), use case 0 (ours: DGFiP names no prediction), source + (DGFiP's register with its notice and terms), shape + (2.2M sales, mixed types, temporal), risk - (a newer release of the same data exists, issue 2; partial-rights and family transfers stay unmarked in the target, 1.1% of the sales). Features are thin (no year built, condition, floor or energy rating): the fit is approximate.
For the curator: issue 1 (which actor and gap, a weighing: A implemented and recommended); issue 2 (re-source now or as a later version, a weighing: A implemented and recommended); issue 3 (`code_section` against zillow_prize, consistency: keep implemented and recommended).

**Main points:** Confirm the tax-office valuer at the deed's publication with the one-month gap, or switch to a valuer pricing before the sale with a three-month gap (issue 1, A implemented); confirm keeping the April 2026 data with the October 2026 release as a later version (issue 2, A implemented); confirm keeping the cadastral section, the finest unit of Etalab's own price statistics (issue 3, A implemented).

**Record fields that disagree with the definition:**

- `year`: record `2019`, definition `2026`.

**Record judgment:** valid. France's register of property sales from DGFiP (decree 2018-1350, open since 2019), read in Etalab's geolocated copy; the build met each risk the screening named (one row per sale, single dwellings, identifiers and address dropped with the coordinates kept at the published precision, which the terms allow, one release pinned and archived). Two readings of the screening are corrected: the use case's actor is narrowed to the one that fits the deed date and the one-month gap (a lender or notary prices about 3 months earlier), and the off-plan sales the screening left to a rule are dropped, because the register describes them only after the sale.

**Issues for Lennart:**

1. **Which actor: a tax-office valuer checking the declared price as the deed is published (one-month gap), or a valuer pricing before the sale (three-month gap)?**

   * **Problem:**
     - The first draft had "a lender, a notary or a valuer" price a home before it sells, but the time column is the date the deed is signed, and the price is agreed at the preliminary contract (the compromis) about 3 months earlier, so with a one-month gap a training side held deeds signed up to about 2 months after the first test sales of its window were priced[^use].
     - The definition now names a tax-office (DGFiP) valuer who checks the price a deed declares as the deed is published, for whom the one-month gap is the publication delay (implemented); a notary does not fit this framing, since the price is fixed at the compromis.
     - The alternative keeps a valuer who prices before the sale, at the compromis, and widens the gap to three months[^s10]; a lender stays out, since it sees public DVF 4 to 10 months late.
   * **Background:**
     - The tax office's price database is fed as each deed is published (notice, section 1), and most deeds are recorded within days; a lender working from public DVF sees sales 4 to 10 months late, at the April and October releases.
     - In France the final deed follows the compromis by about 3 months (PAP: https://www.pap.fr/vendeur/vendre-sans-agence/les-delais-a-connaitre-lors-de-la-vente/a3283), against a US escrow of 30 to 45 days.
   * **Effect on the task:** under A the question is whether a declared price is in line with the market, checked at publication, and no training sale is newer than the moment of the check; under B the question stays "what will it sell for", and each training side ends two months earlier.
   * **Experiments:**
     - Split auditor, on the first draft's rows, untuned LightGBM, equal training sizes, the date left out as an input: gap 1, gap 3 and training only on what the April and October public releases hold (4 to 9 months old) score within 0.001 RMSE of the log price on each window (gap 1: 0.496 / 0.520 / 0.531; gap 3: 0.495 / 0.520 / 0.530), so neither gap costs measurable information.
     - With the date as a number, a model carries the seasonal level of the last training month into the window (up to 0.03 a window) under every gap; a comparison over a few windows cannot decide the gap anyway[^s21].
     - Under B the train sides before sampling hold 80.5 / 71.6 / 63.2% of the sales (the floor is 50%), against 86.3 / 77.4 / 69.0% under A.
   * **Consistency:**
     - The house-price family gaps only the recording delay: house_sales one week, zillow_prize one month; A follows them.
     - B would depart from them on the fact that sets DVF apart, the 3-month delay from compromis to deed; it applies the rule that a delay built into the use case counts as a gap too[^s10], so it needs no exception.
   * **Panel:**
     - Tax-office valuer, gap 1 (domain practitioner, advocate): the price database is fed at publication, and the model is "a usable screen for a tax office flagging under-declared values".
     - Pre-sale valuer, gap 3 (split auditor): it keeps the task the record, the first draft and the blind reviewer describe, at no measurable cost.
     - The critic accepts either, but not a notary under gap 1; the mediator leaves the choice to you.
   * **Unknown:** whether DGFiP's control services value declared prices from comparables at publication; a DGFiP source saying so would tip it toward A.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Tax-office valuer, one-month gap (implemented) | question, use case and prediction point name a DGFiP valuer checking the declared price at the deed's publication; windows and train sides unchanged | the gap is the measured publication delay; follows the family's recording-delay gaps; the freshest training data | a narrower actor; the question is no longer "what will it sell for" |
     | B | Pre-sale valuer, three-month gap | `gap=3`, a valuer pricing at the compromis; training ends move to April 2025, January 2025 and October 2024 | keeps the task the record, the first draft and the blind reviewer describe; the gap covers the time from the agreed price to the deed | training ends two months earlier (no score cost measured); smaller train pools (80.5 / 71.6 / 63.2%, still above the 50% floor) |

   * **Recommendation:** A: the register fills as deeds are published, most within days of signing, so the valuer who checks a price at publication needs only the one-month publication gap; the scores cannot decide between the two. **Decision:** A or B?

   **Notes for the AI:**
   - A: nothing to change.
   - B: set `TemporalSplits(window=3, unit="months", n_windows=3, gap=3)`; rewrite `task_summary.question` ("What price will a house or an apartment in France sell for, from its land-registry description?"), `use_case` (a valuer prices a home at the compromis, with a model refit every quarter on the sales published until three months earlier; no lender), `split`, the "Prediction point" bullet and `splits_comment` (the gap is the publication delay plus the compromis-to-deed delay; train pools 1,380,117 to 1,759,310 before sampling, 63% to 81%); re-run `dataset check`, the leak and task probes, and a focused panel (split auditor, mediator, editor).

   [^use]: **USE-3** (Must): name the prediction point, when the model is used and what is known then; **USE-1** (Must): a use case is an actor, a moment and a decision, and every split choice is checked against it.
   [^s10]: **SPLIT-10** (Should): a model refit at a window's start knows only the rows whose label had arrived, so train with a gap of about the label's delay; "A planning gap the use case has (a forecast made a day ahead) is a gap too."
   [^s21]: **SPLIT-21** (Must): decide neither the training history nor the windows from a comparison over a few test windows.

2. **Keep the April 2026 data now and re-source to Etalab's October 2026 release as a later version, or re-source now?**

   * **Problem:**
     - The definition reads Etalab's geolocated release built from DGFiP's April 2026 delivery, but Etalab published the next one (DGFiP's October 2026 delivery: November and December 2025 complete, the first half of 2026 (2026-S1) added) on 2026-10-20, and deletes the folder we read on 30 November 2026.
     - Implemented: keep the April data now, with the raw files archived in the warehouse and their sha256 values in the download text as the reference copy, and re-source as a later version[^prov8].
     - The alternative re-sources now.
   * **Background:**
     - The checks behind this definition's cut and drops pair this release with DGFiP's October 2026 file: the cut of November and December 2025, the stability of the registry's attributes and the off-plan finding.
     - The October release re-geocodes on a newer cadastre ("Les coordonnées et certaines valeurs peuvent donc différer légèrement"), and its own newest months cannot be checked against a later release before April 2027.
     - Etalab deletes a release after the next one and DGFiP replaces its files at each delivery, so after 30 November no public copy of the April data is known to remain, and within a year the warehouse archive would be the reference under either option.
   * **Effect on the task:** B adds November and December 2025 and 2026-S1 (the windows could move into 2026), with the end-of-release cut measured again on per-day completeness; A keeps the windows of February to October 2025.
   * **Consistency:**
     - Newer data of the same task with the same target and features enters (tls_os over cesnet_os)[^newer]; A defers that to a later version rather than declining it.
   * **Panel:**
     - Re-source now (precedent checker, first recommendation): newer, more complete data of the same task with the same target and features enters, as tls_os did over cesnet_os.
     - Keep now, re-source later (advocate, critic in its rebuttal, mediator; the precedent checker's fallback when the rebuild is deferred): a re-source re-geocodes and ships an end of release no one has measured, so it makes a new version.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | April data now, re-source later (implemented) | the definition stays on the 2025-12 folder; the archived raw files and their sha256 values are the reference; the October 2026 release becomes a later version | every check pairs this release with a later one; no rebuild now; the archive is in place | this version misses November-December 2025 and 2026-S1; the public download links die on 30 November |
     | B | Re-source now | read Etalab's 2026-10-20 files; redo the end-of-release cut, the attribute and off-plan checks, and a focused panel | newer and more complete data; a public download that lasts until the next release | a rebuild and a new panel; the newest months cannot be checked against a later release before April 2027; coordinates re-geocoded |

   * **Recommendation:** A: the cut and the off-plan drop were measured against a later release, which only the April data has now; 2026-S1 can enter in the next version. **Decision:** A or B?

   **Notes for the AI:**
   - A: add a CC line to the record with the revisit condition (re-source to Etalab's October 2026 release once DGFiP's April 2027 delivery allows its newest months to be checked); the archive is in place and its sha256 values are in `download_description`.
   - B: download Etalab's resources of 2026-10-20 (static.data.gouv.fr/resources/demandes-de-valeurs-foncieres-geolocalisees/20261020-*, full-2023 to full-2026-s1) into a new folder, point `GEO_DIR` and `YEARS` at them (the prepared files rebuild), replace `_completeness` with a per-day completeness check of the release end, set the cut and windows from it, rewrite `download_description`, re-run `dataset check`, all probes and a focused panel (claim and split auditors, task gamer, mediator, editor).

   [^prov8]: **PROV-8** (Must): where we download the files can differ from the source; the download instructions name the copy and say which original it copies.
   [^newer]: principles.md, Tensions, "Same task, another source" (Lennart, 2026-11-08): when one source is better data for the task (larger or newer with the same target and features), it enters and the other stays for later; tls_os over cesnet_os.

3. **Keep the cadastral section (`code_section`), which zillow_prize's precedent would drop?**

   * **Problem:**
     - `code_section` names the dwelling's cadastral section (217,672 sections, about 10 sales each), and zillow_prize dropped its census block group of the same grain (8,334 levels, about 11 sales each) as a near-identifier whose place the coordinates already hold[^zillow].
     - The definition keeps the section (implemented) on a fact that sets it apart: Etalab, the publisher of the copy we read, publishes DVF's sales counts and mean and median prices per m2 at five scales, the finest being the cadastral section, so the section is the domain's own price unit.
     - The alternative drops it as zillow_prize did and keeps the commune, the postcode and the coordinates.
   * **Background:**
     - A cadastral section is "un ou plusieurs lieux-dits ... quartiers" (notice, lexicon), a named neighbourhood; DVF has no level between the commune (about 68 sales each) and the section.
     - Statistiques DVF (https://www.data.gouv.fr/datasets/statistiques-dvf, updated 2026-10-21, shown on explore.data.gouv.fr/immobilier) reports by nation, department, EPCI (a grouping of communes), commune and cadastral section; a census block group has no such role in Zillow's data.
     - How many levels the column has is no reason to keep or drop it[^width].
   * **Experiments:** the score cannot decide: the blind reviewer's LightGBM (a 200,000-row sample of the first draft) scores RMSE 0.548 with the section, commune and postcode codes and 0.547 without all three, and a probe of how closely each column locates a sale rates the section and the longitude about equal (0.400 and 0.391 on the final definition).
   * **Consistency:** keeping departs from zillow_prize with the fact above; dropping follows it.
   * **Panel:** the blind reviewer, who saw only the data, would drop it as a near-identifier with no gain over the coordinates; the column auditor and the precedent checker asked for the fact that sets it apart, now verified; the advocate and the critic leave keep-with-the-fact or drop to you.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, with the fact (implemented) | `code_section` stays; the notes give the Statistiques DVF fact | the unit valuers and Etalab's own price statistics use; no score cost | about 10 sales a level, a near-identifier whose place the coordinates hold; departs from zillow_prize unless you accept the fact |
     | B | Drop, as zillow_prize | `code_section` leaves; commune, postcode and coordinates stay | the same treatment as zillow_prize; no near-identifier | drops the domain's own price unit; no score gain |

   * **Recommendation:** A: the section is the finest unit in which the source's own publisher reports prices, which a census block group is not for Zillow. **Decision:** A or B?

   **Notes for the AI:**
   - A: add a Cases row to CLEAN-14 in `cleaning_features.md` ("france_dvf_property_sales: `code_section`, 217,672 levels, kept unlike zillow_prize's block group: Etalab's Statistiques DVF publishes prices per cadastral section", with your name and the date) and a CC line in the record.
   - B: drop `code_section` in `_clean` (step 7) and from `_feature_types`, delete its notes bullet, re-run `dataset check`, the leak probes and the hidden-group probe.

   [^zillow]: zillow_prize (CC 2026-10-26, Lennart): the census block group (8,334 levels) dropped as a near-identifier, the tract kept; **CLEAN-3** (Should): drop uninformative identifiers, keep one that carries meaning and process it into that meaning.
   [^width]: **CLEAN-22** (Must): columns leave for what they are, never for how many there are; **CLEAN-14** (Should): categorical for a fixed, finite set of values inferred from the context.

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain practitioner, blind reviewer, task gamer, precedent checker, advocate and critic with one rebuttal each, mediator. The panel worked on the first draft, before the off-plan sales and the prices of 1,000 EUR or less were dropped (2,222,274 sales, 1,658,250 rows shipped); the final definition keeps 2,185,254 sales and ships 1,653,624 rows, so every count in the reports below is the draft's: 3,214 low prices (3,213 in the definition), 476 room counts and 417 Carrez areas masked (294 and 390: 178 of the room counts and 5 of the Carrez areas were off-plan sales, 4 and 22 low prices), train pools of 86.5 / 77.6 / 69.3% under gap 1 and 80.7 / 71.9 / 63.4% under gap 3 (86.3 / 77.4 / 69.0% and 80.5 / 71.6 / 63.2%), test windows of 196,336 to 219,486 rows (194,513 to 217,561) and 217,872 sections (217,672). The reports before the mediator's number the builder's draft issues: 1 the low prices, 2 the coordinates, 3 the gap, 4 the release; the mediator's issues are this file's. Claim audit: 35 claims; refuted and fixed: the stability of the registry's attributes for off-plan sales (VEFA dropped), the year (2026), "the only dated release online" (Etalab's October 2026 release is out, issue 2), the low-price counts (taken after a log and back, which put the 625 sales at exactly 1,000 EUR below it; now counted on the price itself), the privacy wording (a row is as identifying as the published record), "by 31 December" (most deeds are recorded within days). Column audit: VEFA rows are selected after the sale; 62 impossible coordinates, impossible room counts and Carrez areas (now masked); `code_section` against zillow_prize (issue 3). Split audit: right with notes; leans to a three-month gap for a valuer pricing before the sale (issue 1, B), at no measurable cost. Domain practitioner: fit approximate; drop the prices of 1,000 EUR or less; name a tax office as the actor (issue 1, A); would rather score a mean absolute error on the log price, and accepts RMSLE once the low prices are dropped. Blind review: include with changes; its concerns were the symbolic prices (dropped), the 2025 jump in rows (the shipped file's shape under the 1M cap, now in the splits comment), farm and estate sales priced as a whole (kept: every parcel's land is summed into the row, the fact that sets DVF apart from house_sales, which dropped its multi-parcel sales) and `code_section`, which it would drop (issue 3). Task gamer: barely gameable; counts of same-day sales over the test rows are worth 0.003-0.005 (a protocol line now). Precedent check: consistent on the target, the metric, the gap and the coordinates; departures on VEFA, the year and the masks (fixed) and on `code_section` (issue 3). Debate: agreed on VEFA, the year, the licence, the coordinate and room masks and release option A; disputed the 100-1,000 EUR band (both sides left it to you; the mediator settled it by measurement: dropped), a notary under gap 1 (settled: out) and a mask of every Carrez area below 8 m2 (settled: only where it contradicts the floor area); the actor and the release are weighing calls (issues 1 and 2).

<details><summary>Mediator</summary>

MEDIATOR: france_dvf_property_sales (folder france_dvf_property_sales_1m), 2026-11-09

Read: principles.md; the builder's report and claims.md; the claim, column, split, domain, blind, task-gamer and
precedent reports; the advocate's and critic's briefs and rebuttals; dataset.py, README.md and the record; the rules
USE-1/3/5/7, CLEAN-3/7/11/14/15/22, LEAK-5/6/9/10/30, SPLIT-10/12/14/21, PROV-8/9/13 and definitions.md (row budget,
download_description). My experiments: the run's work files m1_band, m2_bands, m3_carrez (.py and .log), on the claim
auditor's curated frame and the column auditor's clean frame (raw prices, 4 threads); the notice (lexicon, p. 10); the
data.gouv.fr API entry of "Statistiques DVF" (read 2026-11-09).

**1. RECOMMENDATION**
Verdict: ship after changes.
Validity: SEL-1 holds (the CGU bar is met under every option: a row links back to its published record at 99.9% with
or without coordinates; the purpose clause and the privacy wording are owed). USE-1/USE-3 triggered (a lender or notary
prices before the compromis, which gap 1 does not cover), fixed by issue 1 (a) or (b). USE-5 triggered, fixed
(declared prices of 1,000 EUR or less dropped, 3,214 sales, measured as non-prices: S1). LEAK-10 triggered, fixed (VEFA
dropped, 33,807 sales). LEAK-16 holds (143 kept sales, 0.006%, hold two dwelling lines). LEAK-5/LEAK-9: counts over the
test block worth 0.003-0.005, a protocol point, no data change. SPLIT-1/SPLIT-6/USE-10 hold (temporal, known places);
SPLIT-14 holds (69.3-86.5%); SPLIT-10 holds for the publication delay. PROV-9 triggered, fixed (2026). PROV-8 holds
(download text corrected).
Value: no TP flags (dummy RMSLE 0.81-0.84, LightGBM 0.50-0.55, 196k-219k test rows a window); MET-11 rmsle on a log
target, as the house-price family.
Quality: CLEAN-11 masks for 62 coordinates, 476 room counts and 417 Carrez totals that contradict the floor area;
code_section kept with a verified fact (issue 3).
Weighed: size +, source +, use case 0 (ours), features - (no year built, condition or energy rating).
For the curator: issue 1, which actor (two framings that both meet USE-3: a weighing); issue 2, re-source now or as a
later version (a weighing); issue 3, code_section against zillow_prize (consistency).

**2. AGREED FACTS**
- 2,222,274 sales of one dwelling, 2 Jan 2023 to 31 Oct 2025; three windows (Aug-Oct, May-Jul, Feb-Apr 2025) of
  209,615 / 219,486 / 196,336 test rows; train pools 86.5 / 77.6 / 69.3% of the rows before the 1M sample.
- The 1M sample is uniform per quarter against the source (0.518-0.522, 0.577-0.582, 0.647-0.651) and label-free
  (mean 12.0748 in, 12.0755 out). The gamer's "52% of 2025 against 80% of 2023-24" divides by the shipped frame, which
  holds 2023-24 at about 65% (the union of the train samples) and Feb-Oct 2025 in full. The blind reviewer's "2025 jump"
  is the same frame shape (2025/2024 per month 1.00-1.36 in the source).
- Same-date, same-parcel rows are separate deeds (prices differ in 34,038 of 35,730; no consecutive ids in the 828
  one-price groups); the collapse by id_mutation holds.
- Nov / Dec 2025 hold 95.2 / 89.0% of DGFiP's October 2026 lines (ceiling 97.6-98.4%), and December's present lines
  are dearer: the cut and the 1-month gap hold. "By 31 December" is wrong: 73% of deeds signed on 31 December are
  present; most deeds arrive within days, about 10% months later and cheaper.
- VEFA: 2,544 of 7,972 VEFA keys of 2025 gain a dwelling between the April and October 2026 data (Vente: 44 of
  874,021); VEFA is 0.49-0.78% of the test windows against 1.68-1.89% of the train sides. LEAK-10, fixed by the drop.
- Low prices, on the raw price: 2,589 below 1,000 EUR, 3,214 at or below (625 at exactly 1,000); 1,268 below 100;
  1,946 from 100 to 1,000; 1,073 at 1 EUR; 189 at 10M EUR or more. Below 1,000: 0.09-0.12% of test rows, 22-25% of
  the squared log error; 10M+: at most 0.2%. exp(ln 1000) < 1000 is why the notes count 3,214 "below".
- The 6-decimal coordinates map 1:1 onto 1,481,249 parcels; (date, price, commune, floor area, type) alone is unique
  for 99.91% of rows. The CGU p. 2 purpose clause is missing from `license`.
- year should be 2026 (PROV-9: a growing register takes the year of the pinned snapshot).
- Etalab published the October 2026 data on 2026-10-20 with the mutation id and coordinates; the 2025-12 folder is
  labelled for deletion "au 31/11/2026".
- Without the date as an input, gap 1, gap 3 and the public-release cut score within 0.001 on every window.
- 62 coordinates in four communes of department 92 lie at latitude 40.88-83.52; 476 dwellings have under 4 m2 of floor
  area per main room.
- code_section: 217,872 levels, about 10 sales each; no gain over the coordinates (RMSE 0.547 against 0.548).

**3. CHANGES**
3a. Make now (no decision needed)
1. Drop `Vente en l'état futur d'achèvement` in `_clean` (33,807 rows); scope the 906,747-line note to existing
   dwellings. LEAK-10 (Must).
2. Drop raw `valeur_fonciere` <= 1,000 EUR in `_clean`, before the log (3,214 rows). Record it as an application of
   USE-5 with the measurement of S1, not as an exception to CLEAN-11. Delete the house_sales citation. Rebuild the
   "Extreme declared prices kept" decision on the raw price. Keep the 10M+ sales. Name the remaining unmarked
   partial-rights and family transfers in fit_reason (1.23% of sales below a fifth of their commune's level). Update
   the metric reason ("from under 100 EUR"). USE-5 (Must), CLEAN-15.
3. year = "2026"; the BibTeX can keep "open since 2019". PROV-9 (Must).
4. download_description: name Etalab's release of 2026-10-20 and the deletion of the 2025-12 folder on 30 November
   2026, delete "the only dated geo-dvf release online", and give the warehouse copy with its sha256 values as the
   reference. PROV-8 (Must); writing.md for the false sentence.
5. license: add the CGU p. 2 purpose clause ("concourir à la transparence des marchés fonciers et immobiliers").
   Reword the privacy bullet: a row is as identifying as the published record, no more (dropping the parcel id hides
   nothing while the coordinates stay). Coordinates stay at 6 decimals (builder issue 2 settled as (a) by both sides).
   SEL-1 (Must); selection.md, "Ethics, licence".
6. Masks by fixed rules within the row (CLEAN-11, CLEAN-7): coordinates missing outside a fixed box per territory
   (62); rooms missing where floor area / rooms < 4 m2 (476); surface_carrez missing where it contradicts the floor
   area: below 8 m2 beside a floor area of 20 m2 or more (141), or above 3 times the floor area and above 200 m2 (276,
   including all 43 above 1,000 m2), 417 rows (S4).
7. Notes (writing.md), the five corrections: (i) counts on the raw price (2,589 below, 3,214 at or below 1,000 EUR;
   1,268 below 100); (ii) the n x p bullet: 143 kept sales hold more than one distinct dwelling line (68 of different
   area), and about 1,000 one-dwelling sales leave on non-integer counts; (iii) "67,836 dwellings sold more than once":
   35,102 of the 43,169 apartment groups are twin units, 21,110 apartments resold by (parcel, first lot); (iv) "by 31
   December": most deeds are recorded within days, about 10% months later; (v) one sentence on the frame's shape
   (2023-24 at about 65% of the source, Feb-Oct 2025 in full). Also: 27,415 counts every kind of single-dwelling
   mutation (25,477 in the curated frame); coordinate missingness falls from 1.20% (2023) to 0.30% (2025), Etalab's
   later cadastre; the windows never test November to January (SPLIT-20).
8. One sentence in splits_comment: counts of same-day sales at a place over the test rows are worth 0.003-0.005
   RMSLE; a model that reads the test block is called out (LEAK-9). No data change.
9. After issue 1: task_summary (question, use_case), the prediction-point bullet and splits_comment follow the chosen
   actor and gap.

3b. Need the curator (ranked)

Issue 1. The stated actor does not fit the gap (P3/P4; USE-1 and USE-3 Must; SPLIT-10 Should; SPLIT-21 Must).
  Problem: the use case has "a lender, a notary or a valuer" price a home "before it sells". The time column is the
  deed date; the price is agreed at the compromis about 3 months earlier (split auditor: PAP, Square Habitat), and a
  lender working from public DVF sees sales 4-10 months late (domain practitioner). With gap 1 a train side holds deeds
  signed up to about 2 months after the window's first test sales were priced. As written, USE-3 fails.
  Effect: no measured cost in information (gaps of 1 to 9 months within 0.001 without the date). With the date as a
  number, a window's level follows the season of the last training month (up to 0.03 a window); SPLIT-21 bars that as
  a reason.
  (a) A tax-office (DGFiP) valuer checking the declared value as the deed is published; gap 1 (the publication delay);
      the question, use_case and prediction point reworded; no notary (S2). Best evidence: the BNDP is fed as deeds are
      published (notice §1); "a usable screen for a tax office flagging under-declared values" (domain practitioner);
      the family gaps only the recording delay (house_sales one week, zillow_prize one month). Cost: a narrower actor;
      the question is no longer "what will it sell for".
  (b) A pre-sale valuer (no lender); gap=3, one number; floor 80.7 / 71.9 / 63.4%; training ends move to April 2025 /
      January 2025 / October 2024. Best evidence: the compromis-to-deed delay of about 3 months against a US escrow of
      30-45 days, the fact that sets DVF apart from the family; it keeps the task the question, the record and the
      blind reviewer describe. Cost: two months less recency, unmeasurable without the date. An application of
      SPLIT-10's planning-gap sentence, not an exception.
  Decision: (a) or (b). No rule decides: it is which framing to ship (Weigh). Leans: split auditor (b); domain
  practitioner and advocate (a); critic either. What would tip it: a DGFiP source that its control services value
  declared prices from comparables at publication (for a).

Issue 2. Which release (P5; PROV-8 holds under both; tension "Same task, another source").
  Problem: the definition reads Etalab's April-2026-based release; the October 2026 release is out (Nov-Dec 2025
  complete, 2026-S1 added) and the 2025-12 folder goes on 30 November.
  (a) Keep the April data now, the fact and the archived raw files (sha256) recorded; re-source as a later version.
      Best evidence: every check that makes this definition honest pairs this release with DGFiP's October 2026 file
      (the cut, attribute stability, VEFA); the October release re-geocodes on a newer cadastre, and its newest months
      cannot be checked against a later release before April 2027; Etalab archives and deletes a release after the next
      (the 2025-12 files of May 2026 go in November; inference for the next one), so the warehouse archive is the
      reference under (b) too within a year.
  (b) Re-source now: rebuild, redo the cut and the checks, a focused panel. Best evidence: newer, more complete data
      with the same target and features enters (tension row; tls_os over cesnet_os); after 30 November no public copy
      of the April data is known to remain (DGFiP replaces its files at each release).
  Decision: (a) or (b). The advocate, the critic (rebuttal A7) and the precedent checker's fallback converge on (a)
  with the rebuild deferred; I recommend (a). What settles it: whether the curator wants 2026-S1 in this version.

Issue 3. code_section, 217,872 levels (P7; CLEAN-22 Must, CLEAN-3 and CLEAN-14 Should; precedent zillow_prize).
  Problem: zillow_prize dropped its census block group (8,334 levels, about 11 sales each) as a near-identifier whose
  place the coordinates hold (CC 2026-10-26). The section has about 10 sales a level and the coordinates hold its
  place too. The builder's reason (CLEAN-22, width) does not answer that.
  The distinguishing fact, now verified: Etalab, the publisher of the copy we read, publishes DVF's price statistics
  (count, mean and median price per m2 of houses and apartments) at five scales, the finest the cadastral section
  ("Statistiques DVF", data.gouv.fr, updated 2026-10-21; explore.data.gouv.fr/immobilier). The section is the domain's
  own price unit (notice: "un ou plusieurs lieux-dits ... quartiers"); a census block group has no such role in
  Zillow's data. The score (0.547 / 0.548) is no reason either way.
  (a) Keep, the fact in the notes and as a CLEAN-14 Cases row. (b) Drop, as zillow; keep the commune.
  Decision: (a) or (b). Recommendation: (a).

**4. DISPUTED POINTS**
S1. Non-market prices: a Must through 1,000 EUR, or the source's words to 100 EUR and the curator's reading above?
  Advocate (CLEAN-11, Should, P7): the source-words clause covers up to 100 EUR (Cerema); the 100-1,000 band (1,946
  rows) rests on a judgement no source states, so it is the curator's reading (precedent checker D1: "an application
  or a narrow exception"). Critic (USE-5, Must, P3): a symbolic amount is not the quantity the actor acts on; keeping
  the band departs from a Must; only the band's edge is the curator's.
  Decisive experiment (m2_bands.log). Local level: the commune-and-type median price per m2 of the sales above
  30,000 EUR; the lowest such median in France (cells of 20+ sales) is 550 EUR/m2 (m1_band.log).
    band            rows    median EUR/m2   median share of local   reach 5% of local   reach a fifth
    below 100       1,268   0.015           0.000                   0.0%                0.0%
    100-1,000       1,946   8.6             0.003                   1.6%                0.1%
    1,000-2,000     1,199   32              0.013                   10%                 0.4%
    2,000-3,000     1,173   52              0.023                   25%                 1.6%
    3,000-5,000     2,639   83              0.044                   46%                 4.4%
    5,000-10,000    6,080   154             0.101                   74%                 19%
  Settled for the critic, on the fact and by rank. The 100-1,000 band measures as the band below 100 does: a median
  0.3% of the local price, 0.1% of its rows reach a fifth of it, one row (0.05%) reaches 550 EUR/m2. That is "a label
  checked and found to be another quantity than the one the actor acts on" (USE-5), and a measurement outranks the
  absence of a page (EV-2). USE-5 (P3, Must) outranks CLEAN-11 (P7, Should): the band leaves as an application of
  USE-5, needs neither the source's words nor an exception, and keeping it is not an option. The tension row "a cleaning
  gap that changes what the target means is a validity question" points the same way (a quarter of the score).
  Where it stops: the data draw no hard line above 1,000. From 1,000 to 3,000 EUR (2,372 rows) most amounts are still
  far below any local level, but a tenth to a quarter reach 5% of it (1.6% below 1,000): real cheap sales begin there,
  and a floor on the declared price alone removes only what is certainly not a price (domain practitioner). 1,000 EUR
  is where that share first jumps by an order of magnitude, and no agent argued for more. No decision needed; the
  rest is named in fit_reason. Etalab's own statistics apply no floor but report medians, which these rows do not move;
  a squared error is moved by them.

S2. A notary in actor (a)? Settled for the critic. A notary prices at the compromis or earlier (avis de valeur), about
  3 months before the deed, so under gap 1 the train side holds deeds signed after that prediction point (USE-3;
  SPLIT-10, "a planning gap the use case has is a gap too"). The advocate's rebuttal names only the DGFiP valuer.

S3. The +0.084 residual on Feb-Apr 2025. Settled for the advocate. It comes from models that read the date as a number
  and carry the last training month's seasonal level; it appears under every cutoff (+0.106 to +0.119 under the
  public-release cut), and the date-free model is better under every cutoff (by 0.005 to 0.031). It says nothing about
  the gap, and SPLIT-21 bars it. The critic's USE-3 argument stands without it (issue 1).

S4. Carrez below 8 m2: a blanket mask (443) or only where Carrez and floor area disagree? Both rest on CLEAN-11
  (Should, P7): impossible values become missing, unusual ones stay. The notice's lexicon (p. 10) leaves lots under
  8 m2 out of the Carrez area, so the values sit outside the field's definition (critic). But 142 of the 443 have a
  floor area below 9 m2 too, so the small Carrez is the room's real size, and the definition keeps 1,180 floor areas
  below 9 m2 as unusual; masking their matching Carrez treats one room two ways (advocate). Settled for the advocate's
  rule within the row: mask where the two measurements of one dwelling contradict (141 below 8 m2 beside 20 m2 or more;
  276 above 3 times the floor area and above 200 m2: 417 rows, m3_carrez.log), keep the 302 consistent small ones, and
  say in the notes that they lie below the Carrez definition's 8 m2. (The advocate's "276 rows" counts only the second
  half of its rule.) The critic accepted a note as its alternative; P7 either way.

S5. Release, actor and gap, code_section: weighing calls (issues 1-3).

Task gamer's exploits, mapped (the definition has no `Potential leak, kept on purpose:` note and no accepted warning):
  0  Later windows' labels in data.parquet. Gain 0.005 / 0.010 / 0.023. LEAK-9: an evaluation-level matter; the
     harness fits on the split's train rows ("never re-split"). Known protocol point of every multi-window container.
     No change.
  2  Gap-month rows as training data. Gain 0.004 / 0.001 / 0.005 over every pre-cutoff row. LEAK-9; SPLIT-10 (the gap
     is part of the task). As 0.
  1  Gap month plus same-day counts. 0.007 / 0.007 / 0.010. As 2 and 3.
  3  Same-day sales at a place counted over the test rows. Strong model 0.004 / 0.005 / -0.001; baseline 0.003 /
     0.004 / 0.004 (mean under 0.004, under 1% of the score). LEAK-5: no stored value depends on the test rows (separate
     deeds, c2_sameday); LEAK-9: a model reading the test block is called out. LEAK-30 does not apply (no stored
     transform). New to the notes; one sentence (change 8). Under issue 1 (a), part of it is information a valuer has
     at publication.
  4  All-time counts per place, future rows included. 0.003 / 0.004 / 0.005. As 3.
  Flaw, the 1M cap. 0.0037 / 0.0034 / 0.0000, from 36% and 16% more rows. The v0.2 row budget (definitions.md,
     Lennart 2026-10-21); SPLIT-11 and SPLIT-20 hold (uniform sample). Known (version_comment). No change but the
     frame-shape sentence.

**5. CONSISTENCY**
Followed:
- VEFA dropped: perth_house_prices' off-the-plan sales (USE-7, shipped 2026-10-26). ames keeps its Partial sales, which
  are not selected after the sale.
- Coordinates at published precision, ids and address dropped: zillow_prize, house_sales, miami_housing.
- Masks by fixed rules within the row: perth and melbourne (2026-10-20/26); the Carrez rule is of the same kind.
- rmsle from context on a log target: house_sales, perth, melbourne, miami, immoscout.
- Gap and cut: house_sales (one week), zillow_prize (one month); house_sales and ames cut their short last months.
- year 2026: chicago_traffic_crashes, sf_permit_time, noaa_storm_events_damage.
- Kinds kept and dropped, multi-parcel single-dwelling sales kept, resales kept, 0 rooms to missing: ames and
  house_sales (precedent checker D8).
Departures, each with its fact:
- Low prices dropped where perth kept its 52 sales below $120,000: perth's lowest price ($51k) is plausible; DVF's
  100-1,000 EUR band is measured at a median 0.3% of its local level (S1). An application of USE-5, no exception;
  perth does not reopen.
- code_section kept where zillow_prize dropped its block group: the source's publisher reports prices per section
  (issue 3, for the curator to confirm).
- Under issue 1 (b), gap 3 where the family gaps only the recording delay: the 3-month compromis delay against a
  30-45-day escrow. SPLIT-14 holds, so no exception and nothing added to SPLIT-10's amendment_due flag.
- Issue 2 (a), the older release kept: the precedent checker's own fallback, with the fact recorded.
No drift, no third exception.

</details>

<details><summary>Claim audit</summary>

CLAIM AUDITOR REPORT: france_dvf_property_sales (folder france_dvf_property_sales_1m), 2026-11-09

Verdict: ship after changes. One Must is refuted (LEAK-10 on the off-plan sales), one Must is a metadata fix
(PROV-9, year), and the release premise behind issue 4 is wrong (Etalab's October 2026 release is already online, and
the folder we read gets deleted on 30 Nov 2026). The unit, the kinds of sale, the completeness numbers, the split, the
metric, the copies across the split and the extreme-price shares hold.

Scripts and logs: the run's work files (t1_counts, t2_lines, t3_release, t3b_release, t4_metric, t5_extreme,
t6_cutoff, t7_lost; .py and .log). Sources read: the notice (20221017), the CGU (20201016) and the FAQ (20221017) in
the warehouse docs folder; the data.gouv.fr API for both datasets (DGFiP and Etalab geo-dvf), files.data.gouv.fr/geo-dvf/.

Judgment record
Verdict: ship after changes.
Validity: SEL-1 holds on identifiability (every option of issue 2 leaves rows re-linkable to the published file, which is
the CGU's bar), but the claims leave out the CGU's purpose clause: for the curator. LEAK-16 holds (143 kept sales,
0.006%, have more than one distinct dwelling line). LEAK-10 is refuted for VEFA: off-plan sales get their dwelling
added to the record after the sale (2,544 of 7,972 VEFA keys of 2025). Fix: drop VEFA, 33,807 rows, 1.5%. LEAK-24 and
SPLIT-10 hold for the cut. SPLIT-10's premise ("by 31 December") does not match the data (73% of deeds signed on
31 December are present); low impact.
PROV-9 is refuted: year 2019 should be 2026, the snapshot we pin of a growing register. Issue 4's premise is refuted
(Etalab released the October 2026 delivery on 2026-10-20).
Value: MET-1, MET-2 and MET-3 hold (dummy RMSLE 0.81-0.84, perfect 0, scorer = manual). Claim 18 holds on a re-run.
Quality: numbers to correct in claims 9, 17, 24, 28 and 29.

Table (claim | source | test | result | evidence | rule)
1  DVF on data.gouv.fr since April 2019, semiannual, 5-year window | claims.md 1, download_description | read notice
   section 3, FAQ, API | HOLDS | notice section 3 (April / October, 10 / 11 semesters); Etalab history "24/04/2019 :
   première livraison"; API frequency semiannual | PROV-8
2  Licence Ouverte 2.0; CGU forbid re-identification and indexing | claims.md 2, license field | read CGU pp. 1-3, API |
   HOLDS, INCOMPLETE | API license lov2 for both datasets; CGU p. 2 also says "La réutilisation des présentes données
   n'est autorisée que pour répondre à l'objectif poursuivi par le législateur (à savoir concourir à la transparence des
   marchés fonciers et immobiliers)". This purpose limitation is in neither the claims nor the license field. CGU p. 3
   also asks reusers to block search-engine indexing of identifying data | SEL-1 (P1)
3  Etalab release folder 2025-12, files of 2026-05-18 | claims.md 3 | folder listing, API | UNTESTED (the date) | the
   folder index shows no dates; the API lists the folder as "[ARCHIVE] Données au format CSV - livraison avril -
   suppression au 31/11/2026", last modified 2026-05-25 | PROV-8
4  The release is built from DGFiP's April 2026 delivery (inferred) | claims.md 4 | API | HOLDS, now READ | Etalab
   history "20/04/2026 : nouvelles données DVF d'avril 2026"; the folder is labelled "livraison avril" | PROV-8
5  The 2025-12 folder is the only dated geo-dvf release online | claims.md 5, download_description, builder issue 4 |
   API, curl of the static files | REFUTED in substance | Etalab published the October 2026 delivery on 2026-10-20 as
   data.gouv.fr resources: full-2023, 2024, 2025 and 2026-s1 .csv.gz (static.data.gouv.fr/resources/demandes-de-valeurs-
   foncieres-geolocalisees/20261020-*). Its full-2025 is 116,267,867 bytes against the archive's 98,313,852, and it
   keeps the mutation id and the coordinates. The 2025-12 folder (= latest/, the same size) is to be deleted
   "au 31/11/2026", so the wget lines of download_description will break in about three weeks. The new release
   changes the geocoding (successive cadastre vintages) and adds ancien_* columns ("Les coordonnées et certaines valeurs
   peuvent donc différer légèrement") | PROV-8, reproducibility (P5)
6  sha256 of the downloads | download_description | sha256sum | HOLDS | all 4 match
7  year 2019, GOV Website, DGFiP source_url | claims.md 7, dataset.py | PROV-9 text | REFUTED (year) | PROV-9: "A source
   that grows over time (a public register, ...) takes the year of the snapshot we pin". DVF is a rolling register; the
   pinned snapshot is the April 2026 delivery (Etalab 2026-04-20). The 2023-2025 rows did not exist in 2019 | PROV-9
   (Must)
8  11,032,186 lines, 3,904,877 mutations | claims.md 8, curation notes | count on raw | HOLDS | 11,032,186 / 3,904,877
9  n x p rule; 1,508 non-integer counts, "none of them single-dwelling" | claims.md 9 | distinct dwelling signatures
   (type, area, rooms, lot1, lot2, volume, parcel, address) per mutation | HOLDS for 1,508; REFUTED for "none
   single-dwelling" | 463 (n=0.5), 380 (1.5), 137 (1.333), 60 (0.333) sales with one distinct dwelling line are dropped
   (DVF did not write all n x p combinations). In the other direction, 143 kept sales have more than one distinct
   dwelling signature: 68 differ in floor area, so two dwellings counted as one (e.g. 2023-1025141: 74 m2 and 57 m2
   apartments, 320,000 EUR). Also 7,846 one-signature sales with exact duplicate dwelling lines are dropped as
   "several" (ambiguous: twin units or a doubled line). All under 0.4% | LEAK-16, CLEAN-19
10 One price per mutation | claims.md 10 | n_prices | HOLDS | n_prices > 1: 0 (12,262 mutations have a null price)
11 2,360,591 single-dwelling mutations | claims.md 11 | recompute | HOLDS | 2,360,591
12 Kinds kept / dropped and counts | claims.md 12 | recompute | HOLDS | curated VEFA 33,807, Adjudication 5,899;
   dropped Echange 3,017, Expropriation 47, VTB 403. See claim 20 for VEFA
13 1,251 without a price | claims.md 13 | recompute | HOLDS | 1,251
14 Nov / Dec completeness 95.2% / 89.0%; ceiling 97.6-98.4%; Dec present median 3,153 | claims.md 14, decision table 2
   | CSV, and a per-day recount against DGFiP October 2026 | HOLDS | per day 15-31 Dec: 0.73-0.94 present; the key match
   on (date, price, parcel) covers 2,272,112 of 2,316,601 / 2,366,849 keys (about 2% unmatched in general)
15 2,222,274 sales, 2023-01-02 to 2025-10-31 | claims.md 15 | recompute | HOLDS
16 Target = ln(declared price), what it includes | claims.md 16 | notice column 11, FAQ | HOLDS
17 3,214 sales below 1,000 EUR, 1,268 below 100, 189 at 10M+ | claims.md 17, curation notes | recompute on the price |
   REFUTED (number) | 2,589 strictly below 1,000 EUR. 3,214 counts the 625 sales at exactly 1,000 EUR, which
   exp(log(1000)) rounds below 1,000. The decision table's "100 to 1,000" band and the extreme_share probe's "below
   1,000" carry the same float artefact. 1,268 and 189 hold | writing (numbers)
18 0.11-0.15% of test rows carry 22-28% of the squared log error; RMSLE 0.535-0.580 vs 0.465-0.505 | claims.md 18,
   builder issue 1 | re-run: LightGBM 400 trees, 300k train, windows 0 and 2, the container's scorer | HOLDS | strict <1,000
   or >=10M: 0.094% / 0.124% of rows carry 22.1% / 25.1%; RMSLE 0.524 / 0.554, without them 0.462 / 0.480. By band (w0 /
   w2): <100 16.6% / 18.1%; 100-<1,000 5.3% / 7.0%; exactly 1,000 1.2% / 1.9%; 10M+ 0.2% / 0.1%. The 1,000-<10,000 band
   (0.30% / 0.40% of rows) carries another 9.5% / 10.7%. So option (c) of issue 1 adds nothing over (b), and a 1,000
   floor leaves about 10% of the error in the 1k-10k band | USE-5, CLEAN-11, MET-1
19 rmsle from context, log transform; no source metric | dataset.py metric, README Metric block | looked once more:
   notice, CGU, FAQ, both data.gouv.fr pages; scored dummies per fold | HOLDS | no metric anywhere. Scorer: dummy
   median 0.809 / 0.830 / 0.844 (rep 0/1/2), equal to a manual log1p RMSLE on exp(y); perfect prediction 0.000.
   Prediction on the price scale fails loudly (overflow), so the scale cannot be mixed up by accident. No scoring
   columns needed; every fold has 196k-219k rows | MET-1, MET-2, MET-3
20 The registry attributes are those at publication and are not refreshed (906,747 lines agree) | claims.md 20, curation
   notes, builder LEAK-10 holds | the builder matched on a key that includes type_local, so a dwelling that appears
   later is invisible to it. Re-test: per (date, price, parcel) key, a dwelling present in the April 2026 data vs the
   October 2026 data; the VEFA share holding a dwelling by sale month | REFUTED for VEFA, HOLDS otherwise |
   2025 keys with no dwelling in this release but a dwelling in DGFiP October 2026: VEFA 2,544 (against 5,428 with a
   dwelling in both, so 32% of the later state is added after the release); ordinary Vente 44 of 874,021 (holds). Among
   dwelling keys present in both, area / rooms differ on 7 / 8 of 882,435 (holds). The FAQ supports this: "la dernière
   surface déclarée ... connue à la date de vente". VEFA mutations holding a dwelling by sale month fall from 0.25-0.30
   (2023) to 0.19-0.24 (2024), 0.09-0.16 (2025) and 0.045 (Dec 2025): the dwelling is added to the cadastre at
   completion. VEFA share of kept sales: 2.2% (2023), 1.5% (2024), 0.78% / 0.75% / 0.49% in the three test windows,
   1.68% in the largest train side. So a VEFA row's presence and its description are looked up after the sale, and
   the test-window VEFA rows are the quickly completed ones | LEAK-10 (Must: "attributes looked up after the outcome
   ... unless the data shows they did not change")
21 surface_carrez = the sum of lots 1-5 | claims.md 21 | code read | HOLDS (as coded)
22 n_dependances, n_parcelles, land groups | claims.md 22 | code read | HOLDS (as coded)
23 217,872 sections | claims.md 23 | recompute | HOLDS
24 Coordinates are Etalab's parcel centroid at 6 decimals; 0.76% missing | claims.md 24 | decimals of raw values;
   bounding boxes | HOLDS with a defect | 9,780,046 of 10,864,555 raw values have 6 decimals (trailing zeros drop the
   rest); missing 0.76%. 62 metropolitan sales lie outside metropolitan France (e.g. dept 92 at lat 40.88, 78.12,
   83.52), so they are not parcel centroids (the README's latitude max 83.5177 is one of them). The 878 outside the
   overseas boxes are Saint-Martin / Saint-Barthélemy under 971 (legitimate) | CLEAN (P7)
25 Ids and address dropped; the coordinates locate a sale no more closely than the published file | claims.md 25,
   curation notes, builder issue 2 | coordinate pair vs parcel, uniqueness of linkage keys | the CGU reading HOLDS; the
   implied protection of dropping the ids is REFUTED | the coordinates are a 1:1 code of id_parcelle: 1,481,249 pairs
   map to 1,481,249 parcels and back, every one 1:1. (date, price, lon, lat) is unique for 99.9% of rows, and without
   any coordinates (date, price, commune, floor area, type) is unique for 99.91% (99.93% with the section). Every row
   links back to its published record (address included) under options (a), (b) and (c) of issue 2. The CGU bar ("pas
   ... plus important que celui caractérisant le jeu de données mis à disposition") is met by all three, and none
   lowers identifiability | SEL-1 (P1)
26 0 rooms set to missing (2,258); 1,180 below 9 m2 | claims.md 26 | recompute | HOLDS (1,020 apartments, 160 houses)
27 1,270 sales share date, price, parcel, type, area, rooms | claims.md 27 | recompute | HOLDS | 1,270 rows in 613
   groups, same date, so on one side of the split. 365 same-key same-price pairs have gap 0
28 67,836 dwellings sold more than once (159,272 sales) | claims.md 28, curation notes | lot numbers of the apartments |
   numbers HOLD, meaning REFUTED | 35,102 of the 43,169 apartment groups hold more than one distinct first-lot number, so
   they are distinct units with the same layout (5,437 groups contain a VEFA sale). By (parcel, first lot) 21,110
   apartments were resold (42,517 sales). Resale gap: 5% within 3 days, 10% within 15 days. No validity impact under the
   temporal split: 4.7-5.5% of test rows have an earlier same-key sale in train, 0.12% at the same price | SPLIT-13,
   LEAK-34
29 Coverage; 971-974 hold 27,415 single-dwelling mutations | claims.md 29 | recompute | HOLDS (loosely) | 27,415 counts
   single-dwelling mutations of any kind, with or without commercial premises; 26,788 with the kinds kept, 25,477 in the
   curated frame. 57, 67, 68 and 976 are absent (0 rows)
30 No year built, condition, floor or energy rating | claims.md 30 | notice column list | HOLDS
31 Windows, gap, test and train counts | claims.md 31, README splits | the container's splits | HOLDS | test 209,615 /
   219,486 / 196,336; pre-sampling train 1,921,854 / 1,724,409 / 1,539,890 (0.865 / 0.776 / 0.693); train 1M each;
   windows as stated
32 The gap stands for the publication delay; the release holds 89.0% / 95.2% "by 31 December" | claims.md 32, splits
   comment | per-day completeness at the release end, for this release and for DGFiP October 2026's 2026-S1 | PREMISE
   UNTESTED / CONTRADICTED | deeds signed 29 / 30 / 31 Dec 2025 are 0.87 / 0.85 / 0.73 present. In DGFiP's October
   2026 file, 30 June 2026 holds 8,819 dwelling lines against 7,852 on 30 June 2025. A release that held only deeds
   published before its cut-off date would hold almost none of the deeds signed on that day. So the deed date to
   recording delay is not a simple lag of a month: most deeds are in within days, and about 10% arrive months later and
   are cheaper (December's missing median 2,586 against 3,153 present). The cut and the 1-month gap still guard against
   that, but "by 31 December" is not what the data show. Low impact | SPLIT-10 (Should)
33 Use case ours; DGFiP's aim quoted | claims.md 33 | CGU p. 1 | HOLDS | "concourir à la transparence ...", "nouveaux
   services d'initiative privée ou par la recherche publique"
34 Fit approximate | claims.md 34 | notice | HOLDS
35 Probe results | claims.md 35 | read the probe outputs, recomputed copies | HOLDS | my exact-copy recount: 2.85% /
   2.87% / 2.94% without the date, 0.0% with it

Implied claims
* Every feature is known at the prediction point: holds except the VEFA rows (claim 20). nombre_lots, n_parcelles and
  the land areas describe the deed's bundle, which is known at listing. code_commune and id_parcelle are remapped to
  the current cadastre by Etalab (location only, no target signal).
* The split mirrors the use case: holds (claims 31, 32). The October 2026 release would allow windows into 2026-S1.
* The target is the real-world target: holds, except that the declared price includes non-market transfers (claim 18,
  issue 1).
* No copy across the split: holds (0.0% exact copies with the date; same-sale groups share a date).

Refuted and untested claims, ranked (validity first, Must first)
1. Claim 20 / LEAK-10 (P4, Must): the off-plan (VEFA) dwelling's registry record is added after the sale.
   2,544 of the 7,972 VEFA keys of 2025 that have a dwelling in the October 2026 data had none in this release. The
   VEFA share with a dwelling falls with recency (0.27, then 0.22, then 0.09-0.16, then 0.045), and the kept VEFA rows
   are 2.2% of 2023 against 0.49% of the newest test window.
   What it changes: the VEFA rows' presence and description come from after the sale, and are selected by how fast the
   building was completed. Builder LEAK-10 "holds" becomes "triggered".
   Mildest remedy: drop nature_mutation == VEFA in _clean (33,807 rows, 1.5%; nature_mutation keeps Vente and
   Adjudication), and give the 906,747-line note its scope ("ordinary sales; a VEFA dwelling enters the record at
   completion"). Alternative for the curator: keep with a note, arguing that the off-plan buyer knows the planned type,
   area and rooms, so the late record stands in for the plan. The selection by completion remains.
2. Claim 25 (implied) / SEL-1 (P1): dropping id_parcelle and the address does not lower identifiability.
   The coordinates encode the parcel 1:1, and the rows stay linkable to the published file at 99.9% under every option
   of issue 2, with or without coordinates.
   What it changes: issue 2's options (b) and (c) buy no protection, so issue 2 can be settled as (a) on the CGU's own
   bar. The curation note should say that a row is as identifying as the published record (no more), not that the drop
   prevents pointing to one property.
   Mildest remedy: reword the note; no data change.
3. Claim 2 (omission) / SEL-1 (P1): the CGU limit reuse to the legislator's purpose (market transparency) and require
   steps against search-engine indexing of identifying data. The license field and the P1 row name neither.
   What it changes: the curator's P1 weighing should state why a benchmark of price models fits "concourir à la
   transparence" ("recherche publique", CGU p. 1). The FAQ shows people ask to have their sale removed and cannot,
   because publication is a legal duty: weigh, not a block.
   Mildest remedy: add the purpose clause to the license string and a sentence to the notes; curator call.
4. Claim 7 / PROV-9 (P5, Must): year 2019 is the first DVF publication, but PROV-9 gives a growing register the year of
   the pinned snapshot: 2026 (the April 2026 delivery).
   Mildest remedy: year = "2026". The bibtex note can keep "open since 2019".
5. Claim 5 and builder issue 4 (P5, reproducibility): Etalab's October 2026 release exists (2026-10-20, with ids and
   coordinates, complete Nov-Dec 2025 and 2026-S1). The 2025-12 archive is to be deleted on 30 Nov 2026.
   What it changes: issue 4's "revisit when Etalab publishes" is moot now, and download_description's URLs die within
   weeks.
   Mildest remedy: (a) keep the April data, archive the raw files (already in the warehouse), and correct the note: name
   the October release and the deletion date, and give the archive as the only copy. Or (b) re-source to the
   2026-10-20 files: this removes the Nov-Dec cut, can move the windows to 2026-S1, and redoes the completeness check
   against nothing newer, so the newest months need the same cut logic.
6. Claim 32 / SPLIT-10 (P4, Should): "the release holds 89% of December by 31 December" is not what the data show. 73%
   of deeds signed on 31 December are present, and 30 June 2026 is complete in the October 2026 file. Recording is fast
   for most deeds and slow (months) for about 10%, and those are cheaper.
   What it changes: the wording of the gap's justification. Keep the 1-month gap (it removes the month that is
   partial).
   Mildest remedy: reword ("most deeds are recorded within days, about 10% months later").
7. Claims 9, 17, 24, 28, 29 (P7, numbers and wording):
   * claim 17: 2,589 strictly below 1,000 EUR, plus 625 at exactly 1,000; the same float artefact affects the
     decision-table band edges.
   * claim 9: about 1,000 one-dwelling sales are dropped by non-integer counts, and 143 kept sales hold more than one
     dwelling line, 68 of them two dwellings.
   * claim 24: 62 coordinates far outside France.
   * claim 28: most "resold dwellings" among apartments are twin units.
   * claim 29: 27,415 includes commercial and dropped kinds.
   Mildest remedy: correct the numbers and wording. Optionally blank the 62 metropolitan coordinates outside the
   metropolitan box.
8. Claim 3 untested: the folder index shows no file dates; the API's archive entry is dated 2026-05-25.

For issue 1 (numbers the curator can use): strictly below 1,000 EUR, 0.09-0.12% of test rows carry 22-25% of the
squared log error; the 1,000-10,000 band carries another 9.5-10.7%; 10M+ carries at most 0.2%. So option (c) adds
nothing to (b), and (b) at 1,000 leaves about 10% of the error in prices that are equally implausible for a dwelling.

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR: france_dvf_property_sales_1m (record france_dvf_property_sales), 2026-11-09

Verdict: ship after changes. One P4 finding no probe flagged: the VEFA (off-plan) rows are in the frame only once
the building is finished and in the cadastre, which happens after the sale. The rest are a P1 weighing call that is
already open (coordinates), a consistency check on the target (non-market prices), and small P7 cleaning gaps.

Read: dataset.py (prediction point: "before a sale ... only the property, the place, the kind of sale and its date
are inputs"), the DVF notice (2022-10-17), the FAQ
(2022-10-17), the CGU (2020-10-16), the builder's report,
claims.md, the probes, principles.md, use_case.md, leak_checks.md and cleaning_features.md.
How the frame was rebuilt: `_clean` was run on the prepared dvf_mutations_2023_2025.parquet, giving 2,222,274 rows and
21 columns, the builder's counts. Scripts and the frame are in the run's work files (a1.py to a8.py,
clean.parquet).

Judgment record (column view):
  Validity: SEL-1 holds with a weighing call (coordinates, issue 2). LEAK-10 is triggered for VEFA rows: the dwelling
  is attached after the sale, and the measurement shows it, so it is a new issue. The other attributes hold LEAK-10:
  the FAQ says "dernière surface déclarée ... connue à la date de vente", and 906,747 lines agree. LEAK-16 holds.
  Value: not my role. Target: the non-market prices (issue 1) need a consistency check against ames_housing and
  house_sales.
  Quality: CLEAN-11 has gaps. 62 coordinates are impossible, the room counts go up to 198, and some Carrez totals are
  below 8 m2 or above 1,000 m2. CLEAN-14: the dtype probe's 3 flags are answered (codes, categorical by meaning).
  code_section's 217,872 levels conflict with a precedent (zillow_prize).

COLUMN TABLE
(column | meaning (notice column / origin) | known at prediction? | dtype and cleaning | verdict | rule)

date_mutation | The date the deed was signed (col 9, "Document (acte)"). | Yes: the planned signing date. It is the time
  column too. | Datetime %Y-%m-%d, 984 days from 2023-01-02 to 2025-10-31, none missing. Sundays 0.01%. |
  Fine | USE-3, CLEAN-14

nature_mutation | Kind of sale (col 10): Vente 2,182,568, Vente en l'état futur d'achèvement (VEFA) 33,807,
  Adjudication 5,899. | Yes: the kind is fixed before the deed (an auction is announced, an off-plan contract is
  signed). | Category of the source's words, 3 levels. | The column is fine. The VEFA rows are selected after the
  sale (problem 2). | LEAK-10

type_local | Maison or Appartement (col 37, cadastral data). | Yes for existing dwellings: the FAQ gives the record
  "connue à la date de vente". No for VEFA: the local is attached after completion (problem 2). | Category, 2 levels
  (Maison 1,233,429, Appartement 988,845). | Fine, except VEFA | LEAK-10

surface_reelle_bati | Floor area in m2, measured between the walls, rounded down, outbuildings excluded (col 39,
  cadastral). | Yes for existing dwellings: the FAQ says it is the last declared area known at the sale date; 906,747
  lines of 2025 agree across two releases. VEFA as above. | Float, 0.01% missing, 1 to 1,915. No zeros. 1,180 below
  9 m2 are kept, and 284 of those have a Carrez area of 9 m2 or more (an outdated cadastral area). Unusual, not
  impossible. | Fine | LEAK-10, CLEAN-11

nombre_pieces_principales | Main rooms; kitchens, bathrooms and outbuildings not counted (col 40, cadastral). |
  As surface_reelle_bati. | Float. 0 set to missing (2,258); 0.11% missing. 223 values above 15, 115 above 20, up to
  198 (a 92 m2 house with 95 rooms, a 47 m2 house with 49). 476 rows have less than 4 m2 per room. | Cleaning gap,
  minor (problem 6) | CLEAN-11

nombre_lots | Total number of condominium lots in the disposition (col 35, "Document (acte)"). | Yes: what is being
  sold, including cellar and parking lots. | Numeric 0 to 23. 0 means no condominium (96% of houses). | Fine |
  CLEAN-14

surface_carrez | Sum of the Carrez private areas listed for lots 1 to 5 on the dwelling's line (cols 26-34,
  "Document (acte)"). It is the only part of the deed's description the file keeps (notice §1). | Yes. The deed
  supplies it, but the Carrez law requires the area in the promise of sale, measured before signature, so a valuer or
  lender has it. Its gaps come from the property type and the lot count, not from the outcome. | Float, 69.2% missing
  (houses 97%, more than 5 lots, VEFA). 443 values below 8 m2, which the Carrez definition excludes. 43 above
  1,000 m2 (max 7,749). 276 are more than 3 times the floor area and above 200 m2. | Minor gap (problem 7) |
  CLEAN-11

n_dependances | Built: outbuilding locals in the sale (garages, cellars, parking spaces), using the notice's 1/p rule.
  | Yes: part of what is sold. | Numeric, all integers, 0 to 142. | Fine | CLEAN-19

n_parcelles | Built: number of distinct parcels in the sale. | Yes. | uint32, 1 to 312. | Fine | CLEAN-19

surface_terrain, surface_terrain_sols (S), surface_terrain_jardins (J, AG), surface_terrain_a_batir (AB),
surface_terrain_autres | Built: land area in m2, in total and by cadastral land-use group (cols 41, 43). | Yes:
  cadastral area. | Float. All five are missing for a sale without land (46.1%: apartments 98%, houses 4%); a group
  the sale lacks is 0. 38 sales have a total land area of exactly 0. | Fine (the 38 zeros are trivial) | CLEAN-11,
  CLEAN-19

code_departement | Department code (col 19). | Yes. | Category, 97 levels including 2A/2B and 971-974. The probe
  flags numeric_levels: it is a code, so categorical is right. | Fine | CLEAN-14

code_commune | INSEE commune code, 5 characters (col 20). | Yes. | Category, 32,783 levels. The numeric_levels flag is
  answered the same way. | Fine | CLEAN-14

code_postal | Postcode (col 17). | Yes. | Category, 5,862 levels, 0.01% missing. The numeric_levels flag: the
  zip-prefix clause of CLEAN-14 does not apply because the coordinates carry the place (bemtpl97, house_sales). |
  Fine | CLEAN-14

code_section | Built: commune + section prefix + section, the first 10 characters of id_parcelle. A section is "un ou
  plusieurs lieux-dits ... quartiers" (notice, lexicon). | Yes. | Category, 217,872 levels (8 to 10 sales each).
  Every value is 10 characters, and 99.997% start with code_commune. | Question for the curator (problem 8) |
  CLEAN-14, precedent zillow_prize

longitude, latitude | Etalab's centroid of the dwelling's parcel, 6 decimals. | The place is known before the sale.
  The geocode was looked up on the 2025-26 cadastre: missing for 1.20% of 2023 sales, 0.71% of 2024 and 0.30% of
  2025 (parcels split or renumbered after the sale). That missingness depends on time, not on the outcome. | Float,
  0.76% missing. 62 values are impossible (problem 5). | Cleaning gap; a P1 question (problem 1); note the missingness
  | CLEAN-11, SEL-1

log_valeur_fonciere (target) | ln of the declared price (col 11): seller-paid agency fees and VAT included; notary
  fees, buyer-paid fees and furniture excluded. "montant ou évaluation déclaré(e)" | The outcome. | Float, -1.90 to
  19.37. 1,073 sales at exactly 1 EUR (log 0). | Consistency check (problem 3); counts to correct (problem 4) |
  CLEAN-16, CLEAN-11, USE-5

Dropped, and right to drop: id_mutation (Etalab's row-grouping id) and id_parcelle (parcel id) under CLEAN-3; the
street number, name and code, the lot numbers, numero_disposition and numero_volume. Also n_lines and n_prices
(bookkeeping), and n_dwellings and n_commercial (constant after the filter, CLEAN-5). One caveat on id_parcelle: the
6-decimal parcel centroid maps one to one onto the parcel through the public cadastre, so dropping the parcel id
gives no privacy gain while the coordinates stay (problem 1). code_nature_culture_speciale only feeds the
de-duplication of land pieces. Dropping it loses only fine land-use detail, which is acceptable.

**PROBLEMS, RANKED (principles.md: rank, then strength, then effect)**

1. P1, SEL-1 and the CGU: the coordinates (builder's issue 2, a weighing call). The CGU (p. 2) allow reuse only
   "pour répondre à l'objectif poursuivi par le législateur (... transparence des marchés)", with no
   re-identification and "pas ... un degré d'identification ... plus important que celui ... du jeu de données mis à
   disposition". Page 3 forbids search-engine indexing and asks reusers to block indexing "des données identifiantes
   publiées" (robots.txt, captcha).
   Facts:
   - The 6-decimal coordinates are the parcel centroid. They identify the parcel as precisely as the dropped
     id_parcelle does (the cadastre's geometries are public). Dropping id_parcelle therefore hides nothing from a
     reader while the coordinates stay.
   - The published geo-dvf file carries both, so the "no more identifying than the published file" test holds with
     or without them.
   - What the definition does not address is the indexing clause. Hosting the container with a crawlable row viewer
     would put date + price + parcel centroid in front of search engines.
   Mildest remedy: (a) keep the coordinates, and add a line under the licence or the notes that a hosted copy must
   not be indexable. Rounding to 3 decimals (option b) lowers the identification below the source's level, at some
   cost: longitude alone R^2 0.081, and 39% of test rows' longitude is seen in train, which is resale history
   (USE-10).

2. P4, LEAK-10 (Must): VEFA rows enter only after the building is finished, which is after the sale. No probe flagged
   it.
   Mechanism: the frame keeps a mutation only when the cadastre attaches exactly one Maison or Appartement local. An
   off-plan dwelling has no local until it is completed and declared. In this release the local, its floor area and
   its rooms appear long after the deed.
   Evidence (a3.py, a4.py):
   - Share of VEFA mutations that carry a dwelling local, by quarter of sale: 26.5%, 28.3%, 28.0% and 23.8% in 2023;
     22.3% to 14.1% in 2024; 14.3%, 14.6%, 10.1% and 6.1% in 2025. The number of VEFA mutations per quarter stays
     between 9.6k and 26k with no downward trend.
   - Between this release (built on the April 2026 DGFiP data) and DGFiP's October 2026 file, 2025 VEFA lines
     carrying a dwelling rise by +28% to +61% in January to October (Jan 503 -> 703, Sep 434 -> 697). The total VEFA
     lines stay the same (Jan 8,728 -> 8,714).
   - For ordinary sales the dwelling lines grow only as much as all lines do (+0.2% to +1.0%, late publications).
     The effect is specific to VEFA.
   - In the shipped frame, VEFA is 0.78%, 0.75% and 0.49% of the three test windows (Feb-Apr, May-Jul, Aug-Oct 2025)
     against 1.89%, 1.77% and 1.68% of their train sides.
   - Claim 20 and the bullet "They are not refreshed at later releases ... (LEAK-10)" are wrong for VEFA. The
     builder's stability check matched lines on type_local, so a dwelling that appears between releases could not
     show up in it.
   Strength: weak in effect. VEFA is 1.5% of rows, and the kept VEFA price per m2 is flat across years (median 4,682 /
   4,619 / 4,685 EUR). The planned floor area and rooms are in the off-plan contract, so the values were knowable in
   another form (USE-6). What the frame cannot undo is the selection: which VEFA sales are rows depends on a
   completion date after the prediction point, and the train and test sides are selected differently.
   Mildest remedy:
   (a) Drop the VEFA sales (33,807 rows), one more filter beside the dropped building-land sales. Lean (a): only it
       removes the post-sale selection.
   (b) Keep them, and state the selection with the numbers above in the notes and in fit_reason.
   Either way, correct the bullet and claim 20 to "for existing dwellings".

3. P3/P4, consistency check on the target: non-market prices (the builder's issue 1). The definition says it keeps
   sub-1,000 EUR prices "as house_sales and perth_house_prices keep their low prices". The family precedent is the
   other way:
   - ames_housing dropped all 82 non-market sales (CC 2026-10-26, Lennart, issue 7 "do (c)").
   - house_sales dropped its related-party sales (warning 51) "so that they are treated as the family sales of
     ames_housing", and the appraiser-flagged non-representative ones.
   What sets DVF apart: no source column marks the non-market sales, so only the price itself can. A floor is
   therefore a filter on the target, which is the builder's concern.
   Facts for the call:
   - 1,073 sales at exactly 1 EUR, then round amounts (500 EUR 354, 100 EUR 188, 200 EUR 90).
   - Nearly all are Vente (2,587 of 2,589). None is marked as anything else.
   - They carry 22% to 28% of the squared log error.
   Options: (a) keep, recorded as an exception that departs from the family precedent; (b) drop prices below 1,000
   EUR with the source's words ("montant ou évaluation déclaré(e)": a valuation, not a price) and the family stance.
   Lean (b), as the builder does, but the curator decides. The definition's sentence citing house_sales should
   change either way.

4. P4/P6, counts to correct (claims 17 and 18, the "Anomaly" bullet). The counts were taken on exp(log price), and
   exp(ln 1000) = 999.99999 < 1000, so sales at exactly 1,000 EUR (625) and 100 EUR (188) count as below.
   Re-measured on the frame:
   - 2,589 sales below 1,000 EUR (3,214 at 1,000 EUR or below).
   - 1,080 below 100 EUR (1,268 at 100 EUR or below).
   - 189 at 10M EUR or more.
   The error shares of the extreme-price probe include the 1,000-EUR sales. If option (b) is chosen, filter on
   the raw valeur_fonciere before the log, not on exp(target).

5. P7, CLEAN-11 (Should): 62 impossible coordinates. They are 62 sales in four communes of Hauts-de-Seine: Vanves
   92076 (27), Malakoff 92046 (20), Issy-les-Moulineaux 92040 (11) and Châtenay-Malabry 92019 (4). Their latitudes
   are 40.88, 78.12 and 83.52, i.e. Etalab geocoding errors, all more than 500 km from the commune's other sales. No
   other sale is between 50 and 500 km away.
   Remedy, cheap and safe: set longitude and latitude missing outside a fixed box per territory (metropolitan France
   lat 41.3-51.2, lon -5.3-9.7; each overseas department its own box). Use a fixed box, not a median over rows
   (CLEAN-7).

6. P7, CLEAN-11: impossible room counts. 115 dwellings have more than 20 main rooms, up to 198 (examples: 92 m2 with
   95 rooms, 47 m2 with 49, 99 m2 apartment with 68). 476 have less than 4 m2 of floor area per main room. Setting 0
   rooms to missing was right; these are the same kind of fault.
   Remedy: set rooms missing where floor area / rooms < 4 m2 (a fixed rule within the row), or keep with a note.

7. P7, CLEAN-11: surface_carrez outliers.
   - 443 totals below 8 m2: the Carrez definition excludes lots under 8 m2 (notice, lexicon).
   - 43 above 1,000 m2, max 7,749, for one dwelling.
   - 276 more than 3 times the floor area and above 200 m2.
   They look like unit or typing errors in the deed. Remedy: keep with a note, or set missing above a fixed ratio to
   the floor area. Also trivial: the 38 sales with land whose surface_terrain is exactly 0 could be missing.

8. P7, CLEAN-14, a precedent question for the curator: code_section has 217,872 levels with about 8 to 10 sales each.
   zillow_prize dropped its block-group code (8,334 levels, about 11 sales each) "as near-identifiers" and kept the
   tract (CC 2026-10-26).
   Facts that could set DVF apart:
   - A cadastral section is a named neighbourhood or lieu-dit that valuers use.
   - DVF has no level between the commune (32,783 levels, about 68 sales each) and the section.
   - The coordinates carry the same place anyway (hidden-groups s_id 0.336 for the section, 0.332 for longitude).
   The builder cites CLEAN-22 (width), which does not answer the near-identifier precedent. Lean: keep, with the
   distinguishing fact written into the notes, or treat it like zillow_prize.

Not problems (checked):
- surface_carrez comes from the deed, but it is a pre-sale measurement required in the promise of sale.
  nombre_lots is from the deed and describes what is sold.
- Neither is the floor area declared in the sale. The notice says the deed's description is not taken over except
  the Carrez area, and the floor area, rooms and type come from the cadastre (MAJIC) as declared before the sale (FAQ).
- 0 rooms set to missing and floor areas under 9 m2 kept: both agree with CLEAN-11.
- No feature is computed from statistics over all rows (CLEAN-7).
- The dtype probe's three numeric_levels flags (code_commune, code_departement, code_postal) are codes, so
  categorical is right (CLEAN-14).
- The coordinate missingness that grows with the age of the sale (1.20% to 0.30%) comes from Etalab's later
  cadastre, not from the price. Worth a sentence in the notes.

</details>

<details><summary>Split audit</summary>

SPLIT AUDITOR - france_dvf_property_sales (folder france_dvf_property_sales_1m), 2026-11-09

VERDICT: right with notes.
The regime (temporal by deed date, known places, expanding train side) is the use case's. The windows, the train
sides, the gap against the publication delay and the November-December cut check out with numbers. Nothing must
change. Two notes for the curator: issue 3 (the gap) is a weighing call, and VEFA rows enter the data late. Every
alternative split I fit differs from the shipped one by at most 0.001 RMSE once the date is not a model input.

Scripts and logs: (the run's work files) (s1_container, s2_vefa, s3_prep, s4_alternatives, s5_sampling,
s6_resales, s7_nodate; *.log). Model: untuned LightGBM, 400 trees, 255 leaves, 800k training rows drawn in one random
order for every scheme (equal size), codes as integer codes, 4 threads. Score: RMSE of the log price (the declared
rmsle up to its +1).

**WHAT I CHECKED (all hold unless named under PROBLEMS)**
Regime (SPLIT-1, SPLIT-6, USE-10). The task is a sale price predicted before the sale, so it is temporal (SPLIT-6).
The entity is a known place. Over the full pool, the cadastral section of 96.2%-96.8% of test rows is in train (93.9%
in the hidden-group probe on the sampled train sides), and the department or commune of almost every test row is. A
valuer prices a home in a place whose past sales they know, so a section or commune is a feature, not a group
(SPLIT-4, SPLIT-13). Unseen sections are the cold-start part: 3.2%-3.8% of test rows, RMSE 0.64-0.72 against
0.50-0.55 for seen ones. Grouping by section would test a use case nobody has.

Container as built (s1). Three repeats, one fold each:
  test 2025-08-01..10-31  209,615 rows | train 1,000,000, 2023-01-02..2025-06-30
  test 2025-05-01..07-31  219,486 rows | train 1,000,000, 2023-01-02..2025-03-31
  test 2025-02-01..04-30  196,336 rows | train 1,000,000, 2023-01-02..2024-12-31
No train and test overlap. Every training date is before window start - 1 month. Pools before sampling: 1,921,854 /
1,724,409 / 1,539,890 = 86.5% / 77.6% / 69.3% of 2,222,274, so SPLIT-14's floor holds. Sampling is uniform over time
(s5): each quarter keeps 0.518-0.522, 0.577-0.582 and 0.647-0.651 of its rows in the three train sides, so all of
2023 onward is in every train side (SPLIT-11, SPLIT-20).

Time column. `date_mutation` is the date the deed was signed (notice, column 2), not the date it was published or
entered DVF. The release holds the deeds published by 31 Dec 2025. The cut at 1 Nov 2025 is right (LEAK-24,
SPLIT-10). Against DGFiP's October 2026 release, December is at 89.0% and its present lines are dearer (median 3,153
EUR/m2 against 2,579-2,846), and November is at 95.2%. January to October sit at 97.6%-98.4%, the ceiling of the
match. October 2025 (0.976) is the lowest of these, but its missing lines are dearer, as in every month (3,235
against 2,720), so it shows no end-of-release selection.

Gap against the publication delay (SPLIT-10). A refit on 1 August knows June at about 95% (the November-at-31-December
analogue) and July at about 89% with a price selection. The 1-month gap removes the selected month. The train side
holds month T-2 at about 98% instead of about 95%: roughly 3% of one month, about 0.1% of a train side. That is not a
shortcut. These rows are linked to no test row's own label, and the gap rules out pairs under a month apart.

Training rows whose label was not known at the prediction point (SPLIT-9): no shortcut found.
* Late-published deeds: about 2-3% of month T-2, see above.
* VEFA rows described late: see note 2.
* Resales across the split (s4, s6): 5.1%-5.9% of test rows have an earlier sale of the same dwelling key (parcel,
  type, floor area, rooms, Carrez) in train. Cutting those earlier sales from training (18,032 / 17,576 / 14,587
  rows) moves the window RMSE by +0.0012 / 0.0000 / -0.0026. On the resold rows themselves it moves +0.007 to
  +0.010. The model barely uses a past sale it cannot see as a price, and a valuer knows a dwelling's earlier DVF
  sale anyway (SPLIT-13, USE-10, as in house_sales).
* The key overcounts: 10% of "resale" pairs are 15 days apart or less and 5% are 3 days apart or less. Those are twin
  units in one building, or one deed recorded twice. The 67,836 resold dwellings are an upper bound.
* Pairs at the same price across the split: 0.12% of test rows.
* Exact feature copies without the date: 2.9% of test rows, 2.8% of them with another price. With the date: 0.0%.

Window sizes and horizon (SPLIT-12, SPLIT-15, SPLIT-17). Windows of 196k-219k rows, 3 x 3 months, newest first. A
quarterly refit is "ours", which SPLIT-12 allows when stated. It matches the family's practice of one horizon per
source (SPLIT-12 cases).

**PROBLEMS AND NOTES, ranked (all P4; none is a Must violation)**
1. Issue 3: the gap counts from the deed, but the prediction point is the valuation, which comes 2-3 months before
   the deed. (P4; SPLIT-10 "a planning gap the use case has is a gap too", SPLIT-12; Should; weighing call.)
   Evidence:
   * The use case (task_summary) prices a home "before it sells, for a loan, an offer or a listing". The time column
     is the deed date. In France the authentic deed follows the compromis by about 3 months (2-3 months with a loan;
     notaries and PAP: pap.fr a3283, squarehabitat, Credit Agricole). The listing and offer valuations come before
     the compromis.
   * So when the price of a test deed signed in a window's first month was set, the shipped train side already held
     deeds signed up to 1 month before the window, which did not exist yet. Measured from the valuation, the
     use case's own gap is about 3-4 months (publication delay of about 1 month plus the compromis-to-deed delay).
   * That is also the shortest lag of a public-DVF user: the April release holds data to 31 December, the October
     one data to 30 June (data.gouv.fr; immovrai.com on the October 2025 update). So gap = 3 covers both readings of
     issue 3.
   Measured, on the same test rows at equal training size (s4, s7), RMSE per window (Aug-Oct / May-Jul / Feb-Apr):
     A0  no gap                        0.5022 / 0.5246 / 0.5353   (with the date as input)
     A   shipped, gap 1                0.5010 / 0.5257 / 0.5529
     B   gap 3                         0.5000 / 0.5283 / 0.5386
     C   public release cut (4-9 mo.)  0.5274 / 0.5476 / 0.5351
   Without the date as input:
     A 0.4958 / 0.5201 / 0.5307 | B 0.4954 / 0.5198 / 0.5297 | C 0.4962 / 0.5195 / 0.5303
   * Without the date the gap costs nothing: any cutoff from 1 to 9 months is within 0.001. Prices and their drivers
     are stable enough over 2023-2025 that the newest months add no information.
   * With the date as a number, a tree puts the test window at the level of the last training month. That level is
     seasonal: winter months are low and June-July high. Median log price is 12.07-12.09 in Nov-Jan against
     12.14-12.21 in June-July (s3_prep.log).
   * So the window scores move with the month that ends training. With the shipped gap the third window ends on
     December 2024 and gets a mean residual of +0.084 (0.5529 against 0.5307 without the date). The public cut ends
     on December 2024 for May-October and gets +0.106 to +0.119.
   * Neither cadence changes the information. The date-as-number model scores worse than the date-free one on every
     window and under every cutoff, by +0.005 to +0.031.
   Decision (SPLIT-21: not from these scores):
   * Precedent: zillow_prize (1 month), house_sales (1 week), perth, ames and melbourne (none) all gap the recording
     delay only, never the time from offer to deed. A US escrow is 30-45 days; a French compromis-to-deed delay of
     about 3 months is the fact that could set DVF apart.
   Options:
   (a) keep gap 1, adding to splits_comment and task_summary that the gap counts from the deed date and that the
       valuation comes about 3 months earlier;
   (b) gap = 3 (`TemporalSplits(..., gap=3)`), a one-number change. The floor holds: pools 80.7% / 71.9% / 63.4%.
       The training ends move to April / January / October.
   My lean is (b), mildly. It is the gap the use case's own prediction point implies, it also covers the public user,
   and it costs no window. (a) is defensible on the family precedent and on the measured zero cost.
   Do not adopt the six-monthly design (S: 6-month windows after each release, 3-month lag):
   * it changes nothing measurable once the date is not an input;
   * its third window trains on 36.4% of the rows (809,763; scores 0.5378 / 0.5430 / 0.5627), below SPLIT-14's floor,
     so it would need 2022 (DGFiP's October 2026 release still holds 2021-S2 on; Etalab's coordinates do not);
   * it doubles the test window for no gain.

2. VEFA (off-plan) sales enter the data only once their dwelling is described, and that comes late. This selects rows
   by how long ago they were sold. (P4; SPLIT-10, LEAK-24 by analogy; note, no change to the split.)
   Evidence (s2):
   * The share of VEFA mutations with no dwelling line rises with recency: 0.72-0.76 in 2023, 0.77-0.86 in 2024,
     0.85-0.94 in 2025.
   * VEFA's share of the kept rows falls from 1.85%-2.83% (2023) to 1.37%-1.81% (2024) and to 0.77%, 0.86%, 0.51%
     and 0.50% in 2025 Q1-Q4.
   * The claim auditor's cross-release match (t3_release.log): 2,544 VEFA sales of 2025 had no
     dwelling in the April 2026 data and have one in the October 2026 data, against 5,428 that had one in both.
   * The VEFA market fell over these years too, but the rising no-dwelling share is a recording lag.
   * So the train sides hold 2023-2024 VEFA sales a refit at the window start would not yet have had as one-dwelling
     sales: about 1% of the newest quarter's rows. The test windows hold the VEFA sales described fast.
   * Effect on the score: none measurable. VEFA is 0.5%-0.8% of test rows, scores 0.28-0.33, and `nature_mutation`
     marks it.
   * It qualifies the LEAK-10 sentence in curation_comments ("not refreshed between releases: 906,747 lines agree").
     That holds for lines present in both releases. It does not hold for lines added later.
   Mildest remedy: one note bullet in curation_comments (no filter). Dropping VEFA (33,807 rows) would remove a real
   kind of sale to fix nothing measurable.

3. Season shape of the test windows. (P4; SPLIT-20; note.)
   * The windows cover February to October 2025. November to January is never tested: the release cut takes November
     and December, and January 2025 is window 3's gap month. Those months hold 21%-25% of a year's sales and the low
     season's prices.
   * Within the windows, July (the yearly peak: 13.3% of 2025's sales to October) sits in the May-July window.
   * This is forced by the release, not chosen, and 9 of 12 months are covered.
   * Interaction with point 1: the month that ends training sets a date-using model's level, which reaches up to 0.03
     RMSE in a window.
   Remedy: a sentence in splits_comment that the windows leave out November to January and why.

**JUDGMENT LINE**
Validity:
  SPLIT-1 / SPLIT-6 / USE-10 hold (temporal, known places);
  SPLIT-14 holds (69.3%-86.5% before sampling, uniform sample);
  SPLIT-10 holds for the publication delay, measured; the planning gap of the valuation is the curator's issue 3,
    lean gap = 3, cost 0 measured;
  SPLIT-9 holds (resales: -0.003 to +0.001 RMSE when cut);
  SPLIT-13 holds;
  SPLIT-20 noted (Nov-Jan untested; VEFA recording lag).
Alternatives fit:
  gap 3: equal to gap 1 within 0.001 without the date;
  public release cadence: the same;
  six-monthly windows: need 2022 for the floor.

Sources:
* data.gouv.fr DVF page (two releases a year, April and October): https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/
* immovrai.com, the DVF update of October 2025 (the April release holds data to 31 December, the October release adds
  the first half-year): https://www.immovrai.com/magazine/mise-a-jour-dvf-octobre-2025
* PAP, the delays of a sale (about 3 months from compromis to deed): https://www.pap.fr/vendeur/vendre-sans-agence/les-delais-a-connaitre-lors-de-la-vente/a3283
* Square Habitat, the delay from promise to final deed: https://www.squarehabitat.fr/info/conseils/vendeur/quel-est-le-delai-entre-la-promesse-de-vente-et-l-acte-definitif-de-vente_3479.aspx

</details>

<details><summary>Domain practitioner</summary>

DOMAIN PRACTITIONER REPORT: france_dvf_property_sales (folder france_dvf_property_sales_1m), 2026-11-09
Actor played: a DGFiP valuer (contrôle of a declared value, a succession or IFI valuation), a notary or a bank's
valuation desk, pricing one dwelling before it sells from the cadastral description and the place.

VERDICT
Fit: APPROXIMATE (agree with the builder). One-sentence reason: one row is one valuation I make and every input is
known before the deed, but the inputs are only the registry's description (no year built, condition, floor, lift or
energy rating, all of which I always have), and the label mixes market prices with symbolic and partial-rights
transfers that no input marks.
Metric scores the decision: PARTLY. RMSLE scores relative error per sale, which is the right family (MET-1, MET-3),
but as shipped about a quarter of the score comes from 0.10-0.15% of rows that are not market prices. With
issue 1 (b) applied I would accept RMSLE. My first choice would be a mean absolute error on the log price: it scores
the same relative error, it is closer to the MdAPE that the AVM industry reports, and the unmarked tail does not
dominate it. Not in the library (MET-13 cost), so it is not a blocker.
Issue 1: (b), drop declared prices of 1,000 EUR or less, and keep the 10M+ sales. Issue 3: keep the quarterly refit
with a 1-month gap, but name the actor who has data that fresh (DGFiP or a notary), not a lender working from public
DVF.

SOURCES
- DGFiP, notice descriptive DVF (2022-10-17): §1 BNDP
  fed after publication of the deed by the SPF; §3 April/October releases (deeds published before 31 Dec / 30 Jun);
  col. 11 "montant ou évaluation déclaré(e)", furniture and buyer-paid agency fees excluded; p.3 a lot carries
  "propriété, usufruit, etc.", and the rights sold are not given.
- DGFiP FAQ (2022-10-17): the floor area is the "dernière surface déclarée ... connue à la date
  de vente" (stale areas exist); furniture is not in the price.
- Cerema, Documentation des Données foncières, "Calculer un prix de marché" (doc-datafoncier.cerema.fr/doc/export/174,
  generated 2026-11-09): "La variable filtre permet d'évincer les prix à 0 ou 1 euros ... on peut évincer les
  mutations de moins de 100 euros"; abnormally high prices may be excluded after a check; it recommends medians over
  means so that outliers need no removal; furniture is worth "a minima 5 à 10 000 euros" and is excluded from the price.
- data.gouv.fr "Statistiques DVF" (Etalab's aggregates): medians per m2; only sales above 100k EUR/m2 or without a
  computable price per m2 are dropped (from the search summary, not read in full).
- AVM accuracy practice: European AVM Alliance / vendor glossaries (valuations.andrewgadsden.com/knowledge/accuracy-
  metrics, clearcapital.com AVM glossary, ICE "Automated Valuation Models"): MdAPE and PPE10/PPE20 (the share within
  10%/20%) are the headline numbers, and the hit rate (coverage) is reported beside them.
- Rules: use_case.md USE-1, -3, -5, -7, -8, -10; metrics.md MET-1, -3, -6, -8, -10, -11, -13.
- Measurements (scripts and logs in the run's work files): d1_prices.py, d2_relative.py on the column
  auditor's _clean frame and the claim auditor's curated frame (same rows, same order).

Q1. DO I HAVE THESE INPUTS AT THE MOMENT I PRICE? (USE-3, USE-6)
Yes, for every shipped feature:
- type, floor area (surface réelle), main rooms: from MAJIC, which I consult before any valuation. The FAQ warns
  that the area is the last one declared and can be stale. That is the same noise I face, and LEAK-10 holds (the
  906,747-line check).
- Carrez area, lots: the Carrez area is mandatory in the promesse de vente of a condominium lot, so it is known
  before the deed.
- outbuildings, land by use, parcels: the cadastral extract of what is being sold. Known.
- department, commune, postcode, section, parcel centroid: known. As a valuer I also have the exact address. The
  section plus the coordinates cover the location for comparables, so dropping the address for the CGU costs me little.
- nature_mutation: I know before the sale whether it is a VEFA (developer's price list) or a judicial auction (I set
  the mise à prix). Known.
- date: the expected signing date. Known.
Missing inputs that I would always have:
- the year or period of construction, the condition and works needed, the floor and lift for an apartment, a view,
  the exposure, parking (partly covered by n_dependances), and the energy rating (DPE class). The DPE is mandatory in
  every listing and, since the climate law, a G or F class weighs on the price (the rental ban on G from 2025). An
  expert would join ADEME's open DPE file by address; that is a rebuild of our own and out of scope for v1.
- the dwelling's own previous sale price and date (USE-10, a known entity). The claim auditor's count: 4.7%-5.5% of
  test rows have an earlier sale of the same dwelling in the training window. I always pull that history first. It
  can be built from the dropped parcel id over strictly earlier sales (the LEAK-34 / tunisian_fraud precedent), and
  shipping the previous price does not reveal the parcel. Optional and lower priority.
No input is one I would lack at the prediction point.

Q2. IS THE TARGET WHAT I ACT ON? (USE-5)
I act on the market value of the dwelling (valeur vénale): a number in EUR, read as a relative error. The declared
price is the best available proxy, and for about 98-99% of rows it is that market price (seller-paid agency fees and
VAT in, furniture out, which adds a few percent of noise I cannot remove). The rest is a different quantity:
- symbolic prices: 1,073 sales at exactly 1 EUR. Every price below 1,000 EUR is a symbolic or non-market transfer;
  no dwelling, garage or attic room in France sells for 100-900 EUR. Cerema's own guidance drops 0 and 1 EUR (its
  `filtre`) and suggests dropping below 100 EUR.
- partial rights and family transfers, unmarked: DVF does not give the right sold (full ownership, bare ownership,
  usufruct, an undivided share bought out by a co-heir; notice p.3). 27,229 sales (1.23%) have a price per m2 below
  a fifth of their commune's median for that type, and only 3,180 of them are below 1,000 EUR. These rows hold 56% of
  the squared log deviation from the local level (d2_relative.log). Some are real (a ruin in the Creuse), many are a
  share or a bare ownership. I cannot tell them apart from the inputs, and neither can a model.
So the target is a proxy with a contaminated low tail. A cut on the declared price alone can remove only the part
that is certainly not a price.

ISSUE 1, the extreme prices (the builder's options):
- Choose (b). A price of 1,000 EUR or less is not the price of a dwelling (DGFiP: "montant ou évaluation déclaré(e)";
  Cerema evicts 0-1 EUR as standard practice), so those rows are not task rows (USE-5; USE-7 by analogy: a row whose
  label is another quantity than the one I act on). Per the builder's numbers they decide 22-28% of the squared log
  error. The fact that sets this apart from perth_house_prices and house_sales, which keep low prices, is that their
  low prices are plausible market prices of a property.
- Do not take (c). The 189 sales at 10M EUR or more carry 0.09%-0.21% of the squared error (extreme_price_share.json).
  They are rare, and a château or an estate with a dwelling is a real valuation, so cutting them changes nothing in the
  score and filters a real market.
- Do not cut on the price relative to the local median. That filters on the target by a rule of our own (CLEAN-11).
  Name the remaining unmarked partial-rights transfers in fit_reason as the gap instead.
- PRECISION BUG TO FIX WITH (b): "below 1,000 EUR" counts 2,589 sales on the raw price but 3,214 on
  np.exp(log_valeur_fonciere). The 625 sales at exactly 1,000 EUR fall to 999.999... after the round trip (checked:
  the two frames have identical prices row by row). The decision table's bands (pd.cut on np.exp of the log, right=False)
  and the notes' "3,214 below 1,000 EUR" therefore mean "1,000 EUR or less". Whichever threshold the curator picks, cut
  on the raw `valeur_fonciere` in `_clean` before the log, and write the count to match (2,589 strictly below,
  3,214 at or below). I would cut at 1,000 EUR or less: 1,000 EUR is a round symbolic amount too.

Q3. DOES ONE ROW MATCH ONE DECISION? IS THE TEST WHAT I FACE?
- Unit: one sale of one dwelling with its outbuildings and land is exactly one valuation file. Dropping the
  multi-dwelling and shop sales is right, because I value those as an investment block by another method.
- Test: next quarter's sales across France (without Alsace-Moselle and Mayotte), including resales and known places
  (94% of test rows in a section seen in training). That is what I face: almost every valuation is in a known
  commune and section (USE-10).
- VEFA selection (a release artefact, small): off-plan sales enter only when the cadastre already lists a dwelling
  local. 73% of VEFA mutations lacked one in 2023Q1 and 94% in 2025Q4, so the kept VEFA share falls from 1.4%-2.8% of
  rows in 2023-2024 to 0.5% in 2025Q3-Q4 (split auditor, s2_vefa.log). The test windows hold fewer new builds than
  training because the registry is filled late, not because the market changed. LEAK-10's check matched on
  type_local, so it cannot see a VEFA line that gains its local later. The notes should name this. It is a small
  shift, not a leak of the price.
- Refit cadence (issue 3): the 1-month gap is right for me as DGFiP (the BNDP is fed as each deed is published,
  notice §1) or as a notary (the notarial price databases are fed from the deeds). It is not right for a bank or an
  AVM working from public DVF. That user sees the April release (deeds published by 31 December) and the October
  release (by 30 June), so their lag is about 4 to 10 months. The split auditor's alternative C (training cut at
  1 January 2025 for the August-October window) scores rmse_log 0.527 against 0.501, with a median residual of +0.15
  against +0.03. The cadence does change the task. National median prices per m2 moved within about ±4% over
  2023-2025, so most of that gap is seasonality and composition, not a market trend.
  My call: keep the 1-month gap and quarterly windows (zillow_prize precedent; more test windows), and narrow the
  task_summary's actor from "a lender, a notary or a valuer" to "a notary or a tax-office valuer, who sees deeds as
  they are published". Today the use case names a lender, who would not have that data (USE-1, USE-3).

Q4. WOULD I USE THIS MODEL?
As a first-pass comparable estimate, the "fourchette" I check against my comparables, yes. As the valuation, no.
- Trust: the inputs are the ones I start from, the location is fine-grained (section and coordinates), and the
  evaluation is out of time on the next quarter. An untuned model's median absolute log error is about 0.20-0.22
  (extreme_price_share.json), about 20% typical error. That is weak next to a valuer (10% or better) because of the
  missing condition and DPE. It is still a usable screen for a tax office flagging under-declared values.
- Distrust: a model trained with the symbolic and partial-rights rows learns to hedge low on dwellings that look
  like candidates for a family transfer. I would also want a coverage rate and a bias reported, as AVM practice does.
  For the bench it ships as a regression, which is fine.

Q5. DOES RMSLE SCORE MY DECISION? (MET-1, MET-3, MET-6, MET-8, MET-10, MET-11)
- Scale and unit: right. RMSLE on the price in EUR (target_transform="log", MET-3), per sale, the unit I act on.
  The error I care about is relative (10% on 80k EUR and 10% on 800k EUR weigh the same), which a log error gives.
  No source metric exists (notice, CGU, data.gouv pages), so `context` is the right origin (MET-11).
- Problem: squaring makes the score depend on the unmarked non-market tail. Below-1,000 EUR rows are 0.10%-0.15% of
  each window and 22%-28% of the squared error. The rows far below the local level (1.2%) hold most of the remaining
  squared deviation. So models are partly ranked by how they hedge on rows I would never value.
- What I would choose: the AVM industry selects by MdAPE and PPE10/PPE20 (European AVM Alliance practice). PPE10 is a
  threshold metric no source of ours fixes, so it is out (MET-6), and MdAPE is a median that the library lacks. The
  closest mean-based, threshold-free metric is the mean absolute log error (MAE on the log price, which estimates the
  conditional median, the "valeur vénale" a valuer gives). It is robust to the tail and adds diversity next to the
  RMSLE house-price family (MET-10, the diversity factor). It would be a new custom metric (MET-13).
- What I accept: RMSLE with issue 1 (b) applied. After the cut the squared tail is the partial-rights rows only, and
  RMSLE keeps the collection's house-price convention. Hence "partly", and "yes" once (b) is in.

GAPS BETWEEN THE DATASET AND THE REAL DECISION, ranked by how much they change the task
1. The label mixes market prices with unmarked non-market transfers: 2,589 below 1,000 EUR (3,214 at 1,000 or less)
   decide 22-28% of the RMSLE, and about 24k more rows are priced below a fifth of the local level (partial rights,
   family sales). Fix (b) for the first part and name the second in fit_reason. USE-5, CLEAN-11.
2. No year built, condition, floor or lift, or DPE: the model is a comparable screen, not a valuation. This is why the
   fit is approximate (USE-8); a DPE join is a later version.
3. The actor and cadence: the task_summary names a lender, whose public-DVF lag is 4-10 months, not 1. Narrow the
   actor (issue 3; USE-1, USE-3).
4. No previous-sale history for the 5% of test sales of a dwelling sold before (USE-10). This is an optional feature
   built over strictly earlier sales.
5. VEFA rows are selected by late cadastral entry (0.5% of test against 1.4-2.8% of train). Name it in the notes.
6. Price noise: furniture is excluded, agency fees are included only when the seller pays, and floor areas can be
   stale. These are unmarked and cannot be fixed. Known to any DVF user.

WHAT AN EXPERT WOULD CHANGE
- Drop declared prices of 1,000 EUR or less on the raw price (fixing the float round trip, and the count in the
  notes and decision table). Keep the 10M+ sales.
- Rewrite the use case's actor as DGFiP or a notary, keeping the quarterly refit and the 1-month gap. Alternatively
  keep the lender and move to semi-annual windows with a 3-4 month gap, which needs 2021-2022 for SPLIT-14.
- In fit_reason: "the declared price includes partial-rights and family transfers that DVF does not mark".
- Later version: the dwelling's previous price from earlier sales, and the DPE class from ADEME.
- Metric: RMSLE once (b) is applied; a mean absolute log error if the collection takes a robust relative metric.

NOT CHECKED
- Whether DGFiP's internal tools (BNDP, Patrim) see a deed within the month, or notaries' databases within two to
  three months. This comes from domain knowledge, not a source read here.
- The share of the far-below-local rows that are partial rights against real cheap dwellings. DVF has no field to
  tell them apart.

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: france_dvf_property_sales (target log_valeur_fonciere, regression, temporal split on date_mutation)
Inputs used: the clean-room data (a 200,000-row sample of 1,658,250), its task description and public pages
(data.gouv.fr DVF and geolocated DVF, a web search). No other local file was opened.

VERDICT: Include with changes. It is a real and useful valuation task with plenty of signal and an honest temporal
split. But about 0.5% of rows have symbolic or non-market prices, and they dominate the log-RMSE. There is also an
unexplained jump in row volume in 2025, where the test windows sit, and it should be explained before release.

WHAT THE TASK IS
Each row is one notarised property sale (a "mutation") in France, 2023-01-02 to 2025-10-31, with exactly one dwelling:
type_local is Maison 55.5% or Appartement 44.5%. The target is log(sale price of the whole mutation, in EUR). The
features describe the dwelling: built area, Carrez area, rooms, number of outbuildings (dependances), lots and parcels,
land area by use, and location (department, commune, postcode, cadastral section, parcel lat/lon), plus the date and the
kind of sale (Vente 98.3%, VEFA 1.4%, Adjudication 0.25%).
Real use: an automated valuation model (AVM) for banks, notaires, the tax administration, estate agents, or buyers. It
predicts a price from a property's description and location before or at the time of sale. Every feature is known
before the deed is signed, so I see no leakage in the columns. Data come from DGFiP deeds and are real, not generated.
Licence Ouverte 2.0. Alsace, Moselle and Mayotte are absent, as the source says ("a l'exception de l'Alsace, de la
Moselle et de Mayotte"): departments 57, 67 and 68 are missing from the data.

SIGNAL (LightGBM, sample; train before 2025-03, test 2025-06..10, n_train=131,351, n_test=45,134)
  predict-the-mean RMSE 0.822 | all features RMSE 0.548, MAE 0.313, R2 0.553
  without code_section/commune/postal: RMSE 0.547 (the high-cardinality codes add nothing beyond lat/lon + department)
  7 core features (area, type, lat, lon, rooms, land, time): RMSE 0.568
  random 80/20 split: RMSE 0.583, R2 0.556 (temporal and random are about equally hard; time feature gain 4.7%)
  Not trivial, not saturated, large. Good benchmark material.

CONCERNS, MOST TO LEAST SERIOUS

1. Symbolic and non-market prices dominate the metric (serious).
   exp(target) quantiles: min 1 EUR, 0.1% = 500 EUR, 0.5% = 9,000 EUR, median 185,000 EUR, max 23.8 MEUR.
   100 rows (0.05%) have price = 1 EUR (target = 0.0), e.g. a 127 m2 house in dept 01 and a 71 m2 flat in dept 56.
   295 rows are below 1,000 EUR and 1,060 rows (0.53%) are below 10,000 EUR. Price per m2 at the 1% quantile is 265 EUR
   and at the 0.1% quantile 8 EUR.
   Impact: in the temporal test above, the 0.5% of rows under 10k EUR contribute 37% of the squared error (45% on the
   random split). RMSE goes from 0.548 to 0.435 when they are excluded. Model rankings would largely reward guessing
   which sales are family transfers or symbolic, and the features cannot know that.
   Cerema (the official DVF documentation) says such mutations are kept for counting "mais il est conseille de les
   exclure pour de l'analyse de prix".
   Change: drop rows with a price below a floor (e.g. under 1,000-5,000 EUR, or under about 100 EUR/m2 of built area),
   and document the rule. Otherwise use a robust metric.

2. Unexplained jump in row volume in 2025, the test period (serious until explained).
   Rows per year in the sample: 2023: 63,519; 2024: 57,075; 2025 (Jan-Oct only): 79,406.
   Ratio of 2025 to 2024, month by month: Jan 1.02, Feb 1.72, Mar 2.15, Apr 1.95, May 1.53, Jun 1.77, Jul 1.78,
   Aug 1.63, Sep 1.68, Oct 1.69. The increase is uniform across departments (Paris 2,891 vs 2,037; Nord 3,002 vs 2,070).
   The real French resale market grew far less than about 70% in 2025. Price distribution, type mix, rooms and
   missingness look similar across years, and I found no duplicate surge (exact duplicates: 1; duplicates ignoring the
   date: 25). So it is probably a sourcing or filtering difference: a different delivery or file for 2025, or a changed
   rule for keeping single-dwelling mutations. It is not a market effect.
   Change: rebuild all years from one DVF delivery with one filter, and check yearly counts against published DVF
   statistics. If the change is real, document it. Because the test windows are all late, the test population may
   differ from training by construction.

3. The target is the price of the whole mutation, not of the dwelling (moderate).
   valeur_fonciere covers everything in the deed. Rows with many parcels show it: n_parcelles up to 312, and 1.7% of rows
   have more than 5 parcels. Examples: a 63 m2 flat on 312 parcels / 10.8 ha sold for 12,000 EUR, and a 36 m2 house on
   176 parcels / 455 ha sold for 4.56 MEUR. These are farm, forest or land deals with a house attached, so they are not
   housing prices. The land columns (surface_terrain_*) partly let a model see this, so this is not fatal.
   Change: either restrict to ordinary residential sales (e.g. n_parcelles <= 5 and surface_terrain below some cap), or
   state clearly that the target is the mutation price. I could not see whether mutations that also contained
   commercial premises were dropped. Only two type_local values remain, so they probably were, but please confirm.

4. Geocoding and area errors (minor).
   8 rows have impossible coordinates: dept 92 (Hauts-de-Seine) at latitude 78.1 to 83.5. 0.68% of rows have no lat/lon,
   which the source explains ("Certaines lignes restent sans coordonnees..."). surface_carrez is more than 1.2 times the
   built area in 2,545 rows (1.3%), with max 6,092 m2; these look like Carrez areas summed over several lots.
   Change: set out-of-France coordinates to NaN (check them against the department), and possibly cap or flag
   implausible Carrez/built ratios.

5. Very-high-cardinality location codes (minor, preparation).
   code_section has 82,939 levels in 200k rows (a near-identifier), code_commune 22,647, code_postal 5,794; all are
   stored as category. They gave no gain over lat/lon in LightGBM, but they will blow up one-hot or embedding baselines
   and make memory use uneven across methods. code_commune and code_section are nested (they share the prefix in 99.996%
   of rows).
   Change: keep department and commune as categoricals and drop code_section, or declare it a high-cardinality ID-like
   feature. code_postal has 8 NA. Other dtypes look sensible: counts are numeric, and missing Carrez (69%) and missing
   land (46%, mostly flats) are structural and correctly left as NaN.

6. Distribution and privacy terms (minor, legal).
   data.gouv says the files contain personal data and that reuse must not allow indirect re-identification or indexing
   by external search engines. Parcel-level lat/lon + date + price is exactly the re-identifiable combination, although
   the geolocated DVF publishes it too. Check that redistributing the data in a benchmark respects these terms.

7. Near-duplicates (negligible). 1 exact duplicate row and 25 rows identical apart from the date. Same-date,
   same-commune, same-price pairs (49 groups in 2025) look like coincidental round prices, not copies.

WHAT I COULD NOT CHECK
- The full 1.66M rows and the actual three test-window boundaries. I only had the 200k sample and built my own split.
- The preparation code: how lines were aggregated to one row per mutation, which mutations were dropped
  (multi-dwelling, commercial), and which DVF delivery each year came from. So the cause of concern 2 is open.
- The DVF notice PDF: it is CID-font-encoded and I could not extract its text with the tools available. The
  statement that valeur_fonciere is the mutation total (including VAT, excluding notary fees) is from my own knowledge
  of DVF, not a quote.
- Repeat sales of the same property across train and test. There is no stable property ID (id_mutation is "non stable
  d'une livraison a l'autre"). These would be legitimate in a temporal AVM setting anyway.

Sources: https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/ ;
https://www.data.gouv.fr/datasets/demandes-de-valeurs-foncieres-geolocalisees ; Cerema DVF docs via
https://doc-datafoncier.cerema.fr/ (low-value mutation advice) ; data.gouv DVF discussions (user reports of extreme values).

</details>

<details><summary>Task gamer</summary>

TASK GAMER REPORT: france_dvf_property_sales (log_valeur_fonciere, RMSLE after exp = RMSE on log price, 3 temporal windows)

Verdict: barely gameable. The best mix of exploits that a model fed only the shipped train rows plus the test features could use (counts of same-day sales at the same place over the test rows) gains about 0.003 RMSLE. Training on the gap month, which the kit ships with labels, adds about 0.004 more. Together they give 0.0079 over the best honest model (1.6%).

Honest scores (scripts and all numbers in the run's work files)
  baseline        LightGBM 600 trees, 255 leaves, raw features, shipped train rows (baseline.py)
                  r0 0.49433 | r1 0.51821 | r2 0.54363 | mean 0.51872
  noise           different seed: mean 0.51866; plus a random column: mean 0.51892. Per-split spread up to 0.003.
                  The same 1M rows in another order moved r2 by 0.0029 (single-seed models).
  strong honest   baseline + log price per m2 of earlier training sales at the same coordinates, section and
                  commune (type-specific, strictly before each row's date), 2 seeds averaged (strong.py a)
                  r0 0.47740 | r1 0.50323 | r2 0.52266 | mean 0.50110
                  This is deterministic: with identical training rows r2 gives exactly 0.52266 again.
  strong honest + all rows up to the train end (see the flaw below; strong.py c)
                  r0 0.47367 | r1 0.49982 | r2 0.52266 | mean 0.49872

EXPLOITS, ranked by gain
| # | Exploit | Script | Honest score | Exploited score | Gain (r0, r1, r2) | A deployed model has it? | Fix |
| 0 | (Not a flaw of the model inputs) Train on later windows' labels, which data.parquet ships for every row | extra_rows.py (cheat_plus_future_windows) | 0.51872 (baseline) | 0.50586 | 0.0053, 0.0099, 0.0233 | No (the future) | The harness must give the model only train rows. Already so if the kit is not the model's input. |
| 1 | Gap month + same-day place counts | strong.py e | 0.49872 (strong, all pre-cutoff rows) | 0.49082 | 0.0066, 0.0070, 0.0100 | No | As for 2 and 3 |
| 2 | Gap-month rows (the month between train end and test start) as training rows and comparables pool | strong.py d | 0.49872 / 0.50110 | 0.49541 | 0.0039, 0.0010, 0.0051 vs all pre-cutoff rows (0.0076, 0.0044, 0.0051 vs shipped train) | No: the gap stands for DVF's publication delay | Do not ship gap-month labels to the model (only the shipped train rows). |
| 3 | Count of sales in the whole table (test included) on the same day at the same coordinates / section / commune | exploit_counts.py, strong.py b,f | 0.50110 (strong) ; 0.51872 (baseline) | 0.49823 ; 0.51515 | strong: 0.0042, 0.0051, -0.0007 ; baseline: 0.0029, 0.0041, 0.0038 | Mostly no: other deeds signed the same day are not known when one property is valued | Small. Accept it, or score rows one at a time. Dropping the date to month granularity would weaken it. |
| 4 | All-time counts of sales per coordinates / section, future rows included | exploit_counts.py | 0.51872 | 0.51487 | 0.0027, 0.0036, 0.0053 | Partly: past counts are honest (the comparables features already use them) | Same as 3 |

FLAW THAT HURTS AN HONEST MODEL
| Training set capped at 1,000,000 rows by a subsample that drops 20-48% of the sales before the cutoff, the most recent months hardest | explore2.py, strong.py c | 0.50110 (shipped train) | 0.49872 (every row up to the shipped train end) | 0.0037, 0.0034, 0.0000 (r2 already has every row) | Yes: a deployed model has every sale published before the cutoff | Ship all rows up to the cutoff, or subsample uniformly in time. |

Findings
1. The kit ships labels for the gap month and for later windows. For r0 the train end is 2025-06-30 and the test starts 2025-08-01. July 2025 (90,805 rows) is in data.parquet with labels. Using it as training rows and as the pool for local-price features gains 0.001-0.005 over a model with every pre-cutoff row. That is recency information: the most recent local prices. A deployed model valuing in August would not have July sales, because DVF is published with a delay of months. Using later windows' labels on the earlier folds gains up to 0.023 (r2); that is plain cheating. Fix: hand the model only the train rows; no change to the data is needed.
2. Same-day place counts. 1.9% of rows share a date and parcel coordinates with another row; 7.4% share a date and section. These rows are cheaper (mean log price 11.8 vs 12.09 for groups of 2 at the same coordinates) and much noisier (SD 1.3-1.9 vs 0.84). Some are VEFA programmes (10-17% VEFA vs 1.3%), some are multi-unit sales split into rows. Counting them over the test rows gains about 0.004 on r0 and r1 and nothing on r2. That is above the 2-seed deterministic model's noise but small. A deployed model valuing one property does not know which other deeds are signed that day at the same parcel. If the preparation split one mutation into several rows, the count of units in the same deed would be known. The fact that decides it is whether these rows share an id_mutation in the source. Mildest fix: keep the date at month resolution, or accept a gain under 1%.
3. Training-set cap (honest flaw). The 1M-row cap keeps 80% of the 2023-24 rows but only 52% of the 2025-02..06 rows for r0, and 58% of 2025-02..03 for r1. The subsample does not depend on the label (in/out label means 12.0748 vs 12.0755 overall; per month within 0.005), so it is not a leak. It still throws away the most recent and most useful sales. Using every pre-cutoff row gains 0.0034-0.0037 on r0/r1. On the baseline model the same change was inside noise (mean 0.51666 vs 0.51872), so it matters once the model uses local comparables.
4. Honest signal, not exploits: the previous sale of the same property (same coordinates, type, surface, rooms; 12-13% of test rows have one in train) gives mean 0.51524 vs 0.51872. Local price per m2 from earlier sales gives 0.50110 vs about 0.5187. A deployed model has both, since DVF history is public.

Attacks that found nothing
- Row order: rows are sorted by date and shuffled within a day. Within-day position vs target r = 0.0002; next-row target correlation 0.008.
- Formats: decimals of surface_carrez (2 decimals 80-83% in every target quintile), lon/lat precision (6 decimals 90% in every quintile), whole-number shares, and NaN rates of terrain/carrez all follow property type, not price. code_* strings have fixed lengths. The section prefix (000 vs other) is flat (3.6-5.2%).
- Train-vs-test classifier without date features (r0, 150k+150k rows): AUC 0.534.
- Exact feature twins across the split: 4.7% of rows have a twin, but date gaps are mostly months to years (resales or identical units). Their previous price is honest signal (finding 4). No duplicated records across the split: same-day twins with the same price number only about 900 pairs, all inside one window.
- Label-dependent training membership: none found (see 3).
- Transforms over all rows: none, raw values throughout.
- Lookups/formulas: none; the price is not a function of the columns.
- Web: no Kaggle competition, leak or magic-feature thread for DVF found. Looking rows up in the published DVF géolocalisée files (date + commune + section + surface) would recover the exact price; every public dataset allows that, so it is not ranked.
- Composition shift between the 2023-24 part and 2025: the VEFA share is 1.85% before Feb 2025 vs 0.67% after, and adjudications fall from 0.31% to 0.16%. The 2023-24 months hold about 45k rows each vs 55-90k in 2025, so the earlier years look subsampled at preparation. This is a time shift; I found no way to exploit it.

Could not check
- Whether same-day same-parcel rows are one DVF mutation split into several rows (needs id_mutation from the source). This decides whether exploit 3 is honest deal composition or future knowledge.
- Whether the benchmark harness exposes gap-month and later-window rows to the model. If it gives only the train rows, exploits 0-2 are not available inside the benchmark.
- Hyperparameter tuning: all comparisons use one fixed LightGBM; larger models may shrink or grow the small gains.

</details>

<details><summary>Precedent check</summary>

PRECEDENT CHECKER: france_dvf_property_sales (folder france_dvf_property_sales_1m), 2026-11-09

Read: principles.md (Consistent judgement, Exceptions and amendments, Tensions), the rules CLEAN-3/11/14/15/22, LEAK-10/11,
USE-5/7/10, SPLIT-10/12/14, MET-3/11, PROV-8/9/13, SEL-1 and their Cases tables; the definitions and records of
ames_housing, house_sales, perth_house_prices, zillow_prize, melbourne_housing_market, miami_housing,
immoscout_german_house_prices; the record of cook_county_residential_sales (in the queue, not built); perth's REVIEW.md
history (git, 2026-10-19 to 2026-10-26); the builder's report, claims.md, and the column, claim, domain and blind reports;
register.json (34 flags; none names this dataset's calls; SPLIT-10 carries an amendment_due flag that this dataset does
not add to, since it sets a gap).

SUMMARY
- Consistent: the log target with rmsle from context; the gap and the Nov-Dec cut; coordinates at published precision
  with the address and parcel id dropped; the kinds of sale kept and dropped; the 10M+ sales kept.
- Departs, with a stated fact: dropping prices under 1,000 EUR (issue 1 (b)) departs from perth_house_prices, but the
  fact that sets it apart holds, and the part up to 100 EUR is an application of CLEAN-11 as amended, not an exception.
  The quarterly cadence departs from the source's semi-annual release, for a reason that holds only for an insider
  actor.
- Departs, without a fact: keeping VEFA (LEAK-10, a Must: perth dropped its off-plan sales); keeping code_section
  (zillow_prize dropped the same kind of code); keeping the older Etalab release (the stated reason is refuted); year
  2019 (PROV-9, a Must); the impossible coordinates and room counts kept (the perth/melbourne pair of 2026-10-20).
- Wrong citation in the definition: "as house_sales and perth_house_prices keep their low prices". house_sales has no
  low prices (its target runs from $75,000), and it dropped its non-market sales on the county's warnings. Only perth
  is a precedent for keeping. The column auditor's reading ("the family precedent is the other way") is not right either.
  The family drops non-market sales on a source marker and has never dropped them without one.

**D1. Non-market declared prices (builder issue 1; USE-5, CLEAN-11, CLEAN-15)**
Precedents:
- ames_housing: the 82 Family, Alloca and AdjLand sales were dropped on the file's `Sale Condition`, a source marker
  (CC 2026-10-26, Lennart, issue 7 "do (c)", USE-5). The CLEAN-11 amendment of 2026-10-21 came from De Cock's three
  partial sales, dropped with his words ("likely don't represent actual market values").
- house_sales: dropped the county's warnings 46 and 8, and 45, 5 and 1 (CC 2026-10-22), then related party 51 "as the
  family sales of ames_housing" (CC 2026-10-26). All of these are markers. The same notes refuse warning 32 ("$1,000 or
  less") as a filter because it is "defined by the price". That is moot there: its one sale is at $385,000, and the
  target starts at $75,000.
- perth_house_prices: keeps the 52 sales since 2012 below $120,000. "The file has no sale type to mark them, and a price
  floor of our own would filter on the target". This was the AI's call (REVIEW issue 9, 2026-10-19), found consistent by
  the check of 2026-10-20 and shipped with the dataset (CC 2026-10-26). The file's lowest price is $51k.
- Target floors kept within CLEAN-11 as amended:
  - sendy_logistics_challenge: 740 legs of 60 s or less, dropped under "a row whose target the source names as not the
    task's quantity", with the winners' page as the words, guarded at 740 (2026-11-05, Lennart, issue 4).
  - nyc_taxi_trip_duration_1m and pkdd_15: trips under 30 s. delivery_eta_1m and cooking_time_1m: under 1 min.
  - 2024_lusaka_mobility_prediction_hackathon: impossible targets set missing, so the rows leave by CLEAN-15, in the test
    windows too (2026-11-05). qsar_tid_11 (2026-10-21) is the same.
- cook_county_residential_sales (queue, not built): the assessor's own filter keeps sales above $10k. That filter is the
  source's, not ours.

Comparison:
- The rule the family follows: drop on a source marker, never add a floor of our own. DVF has no marker:
  `nature_mutation` is Vente for 2,587 of the 2,589 sales below 1,000 EUR. On the marker fact, DVF is perth's case, and
  keeping (option a) follows perth.
- What sets DVF apart from perth: its low values are not prices of a dwelling at all. There are 1,073 sales at exactly
  1 EUR, then round amounts (500 EUR 354, 100 EUR 188, 200 EUR 90, 1,000 EUR 625). Perth's lowest price is a plausible
  price. They also decide 22-28% of the squared log error, against nothing comparable in perth.
- The source's words exist:
  - DGFiP's notice, column 11: "montant ou évaluation déclaré(e)".
  - Cerema's DVF documentation (domain practitioner): the `filtre` "permet d'évincer les prix à 0 ou 1 euros ... on peut
    évincer les mutations de moins de 100 euros".
- Does (b) need an exception to CLEAN-11? For the sales at 100 EUR or less (1,268), no. They leave under the clause the
  ames amendment wrote, with the source's and the field's words, as sendy's legs did. That is an application.
- The band from 100 to 1,000 EUR (1,946 sales) has no source words. It rests on the practitioner's judgement that no
  dwelling in France sells for that. Two readings:
  - an application of CLEAN-11's first sentence (an impossible value of the target becomes missing and leaves by
    CLEAN-15, as lusaka);
  - a narrow exception (a floor of our own above the source's words), with that fact recorded.
  Either is defensible. The curator's acceptance of 1,000 EUR as impossible for a dwelling decides which. Perth stays as
  it is: its prices are plausible, so nothing reopens.
- (c), dropping the 10M+ sales, has no precedent. CLEAN-11's extreme-target clause covers a single value in the training
  period only (mercedes_benz), and these are 189 sales spread across the test windows with no source words. They carry
  0.09-0.21% of the error. Keeping them is consistent.
- Drift: none. Lennart moved from "keep with an indicator" (house_sales, 2026-10-22) to "drop on the marker" (2026-10-26)
  on purpose: house_sales was reopened to match ames. No third exception: the clause is already an amendment.
- Mechanics, for whichever cut: filter the raw `valeur_fonciere` before the log. exp(ln 1000) < 1000 counts the 625
  sales at 1,000 EUR as below (column and domain reports). Guard the count as sendy and lusaka do.

Verdict: (a) keep = consistent with perth. (b) drop below 1,000 EUR = departs from perth with a stated fact. Up to
100 EUR it is an application of CLEAN-11; from 100 to 1,000 EUR it is an application or a narrow exception, the
curator's reading. (c) = departs without a fact. Either way the house_sales citation in the definition goes.

Consistency check (AI, 2026-11-09), for the curator if (b) is chosen:

  Is "a declared amount of 1,000 EUR or less is not the price of a dwelling" the fact that sets DVF apart from
  perth_house_prices, which kept its low prices?

  **Problem:**
  - perth kept its 52 sales below $120,000 because no column marks them and a floor of our own filters on the target[1].
  - DVF has no marker either, but its 1 EUR to 1,000 EUR amounts are no price of a dwelling, and the source calls the
    field an amount "or valuation"[2].
  - Up to 100 EUR the source's documentation drops them itself. From 100 to 1,000 EUR the bound is ours.

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Drop at or below 1,000 EUR, fact recorded | the source's words up to 100 EUR, the impossible-price reading above | removes 22-28% of the error from non-prices | the 100-1,000 EUR band rests on judgement |
  | b | Drop at or below 100 EUR only | Cerema's own bound | fully within the source's words | leaves 1,946 symbolic amounts (500 EUR, 1,000 EUR) |
  | c | Keep all, as perth | no change but the citation | same handling as perth | a quarter of the score from non-prices |
  | d | Amend CLEAN-11 | a written rule for target values that are no price of the unit | settles the family for good | one case so far |

  **Recommendation:** a. **Decision:** a, b, c or d?

  [1]: CLEAN-11 (Should; amended 2026-10-21, on ames_housing); perth_house_prices note on the 52 sales (2026-10-20/26).
  [2]: USE-5 (Must); CLEAN-15 (Must); Cases sendy_logistics_challenge, 2024_lusaka (2026-11-05).

**D2. Off-plan (VEFA) sales whose dwelling enters the cadastre after the sale (LEAK-10, Must; USE-7)**
Precedents:
- perth_house_prices: dropped the 563 sales dated before the build year as "land or off-the-plan sales". "A land or
  off-the-plan sale is not the sale of the house the valuation prices, and the row's attributes describe a house built
  1-23 years later" (USE-7, panel change 6, shipped 2026-10-26).
- ames_housing: keeps its `Partial` sales ("Home was not completed when last assessed (associated with New Homes)"), with
  `Sale Condition` as an input. Only De Cock's three large partial sales were dropped.
- house_sales: keeps 6 houses under construction at the sale, with their placeholder areas set missing.

Comparison:
- Keeping VEFA as a kind with `nature_mutation` as an input matches ames's `Partial`. VEFA's price is the dwelling's
  price (VAT included), unlike perth's land sales.
- What sets DVF apart from ames and house_sales: a VEFA row's presence, not only its description, depends on an event
  after the sale (the dwelling entering the cadastre on completion).
  - The share of VEFA mutations that carry a dwelling falls from 26-28% (2023) to 6.1% (2025Q4).
  - 2,544 of 7,972 VEFA keys of 2025 gain a dwelling between the two releases.
  - VEFA is 0.49-0.78% of the test windows against 1.68-1.89% of the train sides (column and claim auditors).
- This is LEAK-10's "attributes looked up after the outcome", a Must, with no exceptions. LEAK-11 (keep a value that
  weakens the signal) covers a value, not which rows exist. Dropping follows perth, the closest mechanism: attributes of a
  dwelling that did not exist at the sale.
- The definition's reason ("a price paid for the property and known as a kind before the sale") answers the kind, not
  the selection. The 906,747-line check matched on `type_local`, so it could not see the VEFA lines that gain a dwelling
  later.

Verdict: keep, as defined = departs from a Must without a fact; not reasonable under the ranking unless the curator reads
the selection as one of LEAK-10's case-by-case clauses. That needs a measurement that the selection does not move with
the price given the inputs. The flat VEFA price per m2 (4,682 / 4,619 / 4,685 EUR) is a start, not that test. Drop =
consistent with perth.

Consistency check (AI, 2026-11-09):

  Should the off-plan sales leave, as perth_house_prices' off-the-plan sales did, now that they are known to enter the
  frame only after completion?

  **Problem:**
  - An off-plan sale is in the frame only once its dwelling is in the cadastre, after the sale[3].
  - So the test windows hold 0.5-0.8% off-plan sales against 1.7-1.9% in training, chosen by completion speed.
  - perth dropped its off-the-plan sales; ames keeps its new-home sales, which are not selected that way[4].

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Drop VEFA (33,807 rows, 1.5%) | one more filter beside building-land sales | removes the post-sale selection, as perth | loses new-build pricing |
  | b | Keep with a note, as a LEAK-10 clause reading | measure first that the kept VEFA rows' residuals do not move with the share kept | keeps new builds | a Must, decided on one measurement |
  | c | Amend LEAK-10 | allow a row selection after the prediction point that the data shows is price-neutral | general | no second case |

  **Recommendation:** a. **Decision:** a, b or c? Either way, scope the 906,747-line note to existing dwellings.

  [3]: LEAK-10 (Must; amended 2026-11-08): "attributes looked up after the outcome ... unless the data shows they did
        not change"; LEAK-11 (Should) covers values, not rows.
  [4]: USE-7 (Must); perth_house_prices (563 pre-build sales, shipped 2026-10-26); ames_housing `Partial` kept.

**D3. Coordinates at 6 decimals, address and parcel id dropped (SEL-1; CLEAN-3)**
Precedents:
- zillow_prize ships latitude and longitude in microdegrees (6 decimals, as Zillow published) and drops `parcelid`.
- house_sales and miami_housing ship lat/long.
- melbourne_housing_market ships the street address as a string.
- perth_house_prices keeps ADDRESS and builds a UNIT flag from it (CC 2026-10-26, Lennart, issue 5).
- No dataset was ever coarsened for privacy, and SEL-1's Cases hold only Pima (subjects object to ML use).
- selection.md, "Ethics, licence": a licence or redistribution restriction is no reason; note it.

Comparison:
- DVF is more conservative than the family: it drops the address, the parcel id and the lots.
- The CGU bar ("pas ... plus important que celui ... du jeu de données mis à disposition") is met at the published
  precision, as the claim auditor confirms. The indexing clause is a hosting matter and is already in `license`.
- The column auditor is right that dropping the parcel id adds no privacy while the parcel centroid stays. That is no
  inconsistency: CLEAN-3 drops it as an identifier, as zillow did.
- What is new: the source's terms count the file as personal data. Nothing in the family had such terms, so whatever the
  curator decides here becomes the first row of the "Ethics against anything" tension, which has no case yet.

Verdict: (a) keep = consistent with the family. (b) rounding and (c) dropping would depart with a stated fact (the CGU),
in the stricter direction, which needs no exception. No prompt.

**D4. `code_section`, 217,872 levels (CLEAN-14, CLEAN-22, CLEAN-3)**
Precedent: zillow_prize (CC 2026-10-26, Lennart, issue 9).
- Zillow keeps the tract (3,030 levels, about 40 sales each).
- It drops the block group (8,334 levels, about 11 sales each) and the block (55,601) as "near-identifiers whose
  location the coordinates hold".
- The county is already in `fips`.

Comparison: the facts match point for point.
- The section has about 10 sales per level (2,222,274 / 217,872).
- The coordinates hold the place: hidden-groups s_id 0.336 for the section, 0.332 for longitude. The blind reviewer
  measured no gain from the codes over the coordinates (RMSE 0.547 against 0.548). A score is no reason either way.
- The commune (32,783 levels, about 68 sales each) plays the tract's role.
- The builder's reason, CLEAN-22, answers width. CLEAN-22 itself lets a column leave "for what it is ... an identifier",
  which is the zillow reading, so it does not distinguish the case.
- Possible distinguishing fact: the section is the cadastre's named unit ("un ou plusieurs lieux-dits ... quartiers",
  notice), which valuers use. The census block group is a statistical unit. Unverified: whether Etalab's "Statistiques
  DVF" aggregate at section level; if they do, the source's own publisher treats it as a price unit.
- Side question, not checked against precedent: CLEAN-14 types "high-cardinality values" as string, not as a category.

Verdict: departs from zillow_prize without a recorded fact.

Consistency check (AI, 2026-11-09):

  Does the cadastral section stay although zillow_prize dropped its census block group, a code of the same grain whose
  place the coordinates also hold?

  **Problem:**
  - The section has about 10 sales per level, zillow's block group about 11, and both datasets ship the coordinates[5].
  - zillow kept the next level up (the tract), and DVF has the commune at a similar grain.
  - The builder's reason is width, which does not answer the near-identifier reading.

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Keep, recording the fact: the section is the cadastre's named neighbourhood that valuers use, unlike a census block group | notes and Cases row | keeps a unit of the domain | weaker if DVF's own statistics do not use it |
  | b | Drop, as zillow; keep the commune | one column less | same handling as zillow | loses a named unit |
  | c | Reopen zillow to keep its block group | zillow changes | one rule for both | reverses a decision of 2026-10-26 |

  **Recommendation:** a, if the fact is confirmed; otherwise b. **Decision:** a, b or c?

  [5]: CLEAN-14 (Should), CLEAN-22 (Must), CLEAN-3 (Should); zillow_prize Cases row of CLEAN-14 (2026-10-26).

**D5. Log target, `rmsle` from context (MET-3, MET-11, CLEAN-16)**
Precedents:
- house_sales and perth_house_prices: `Metric.from_context("rmsle", target_transform="log")` (2026-10-21, CC Lennart:
  "ship the target on the modelling scale, score on the original scale").
- melbourne_housing_market, miami_housing and immoscout_german_house_prices declare the same.
- ames_housing and zillow_prize keep their source's metrics; they have one. cook_county's source names RMSE, so it will
  differ by origin, not by rule.

Comparison: DVF has no source metric, found after a search of the notice, the CGU and the data.gouv.fr pages. It ships
the natural log and declares the transform.

Verdict: consistent. The domain practitioner's mean absolute error on the log price would depart from the family. It is
a MET-10 diversity call for the curator, not a precedent conflict.

**D6. Quarterly refit, one-month gap, Nov-Dec 2025 cut (SPLIT-10, SPLIT-12, SPLIT-14)**
Precedents:
- SPLIT-10 Cases:
  - house_sales: a one-week gap, the measured recording delay (review 2026-10-20).
  - zillow_prize: a one-month gap, since Zillow receives sales late.
  - ames_housing and perth_house_prices: no gap. Sales are dated by month, and the newest month shows no selection by
    price (an application since the amendment of 2026-11-04).
  - house_sales drops its cut-short May 2015, and ames its July 2010.
- SPLIT-12 Cases (2026-10-21, Lennart): no family window; "each keeps the horizon of its own source or refit cadence".
  ames and perth refit monthly by the curator's judgement, where the source gave no cadence.

Comparison:
- The gap and the cut: DVF has daily dates, and its newest months show selection by price (December's present lines
  dearer, 89% complete). SPLIT-10 as amended asks for a gap and a cut exactly here. Consistent with house_sales and
  zillow; ames and perth differ by their measured facts.
- The cadence: unlike ames and perth, DVF's source has a cadence, the semi-annual public release. The split does not
  follow it. The stated reason is the actor's own refit, the zillow pattern (an insider with its own feed). That holds
  for DGFiP or a notary. It does not hold for "a lender", who sees public DVF 4-10 months late (domain practitioner).
  The claim auditor finds the recording fast (73% of 31 December deeds present), which supports the one-month delay
  for an insider.

Verdict: the gap and the cut are consistent. The cadence departs from the source's release with a stated reason that
holds only if the actor is narrowed to an insider (one line in the use case). Otherwise move to semi-annual windows with
a gap of 3-4 months, which needs 2021-2022 for SPLIT-14. No exception to SPLIT-10 is created.

**D7. Etalab's release over DGFiP's own (PROV-8) and the year (PROV-9)**
PROV-8, attribution: `source_url` is DGFiP, `download_description` names Etalab's copy and what it copies, and both are
cited. That is PROV-8's "Where we download the files can differ from the source". Consistent.

Which release:
- The builder's reason for the 2025-12 folder was "revisit when Etalab publishes a release of the October 2026 data".
- The claim auditor refutes it: Etalab published the October 2026 delivery on 2026-10-20, with the mutation id and the
  coordinates. The 2025-12 folder will be deleted on 30 Nov 2026.
- The standing nearest to two versions of one source is the tension row "Same task, another source" (Lennart,
  2026-11-08). When one is better data (newer, same target and features), it enters (tls_os over cesnet_os,
  mh_1m over kronodroid, uji_long_term over ujiindoorloc). The row is written for records; for two releases of one source
  it applies at least as strongly.
- Possible distinguishing fact: every measurement of the definition (completeness, attribute stability, VEFA) is made
  between this release and DGFiP's October 2026 one, and the new Etalab release re-geocodes on a newer cadastre.
  That is a cost of the rebuild, not a reason the older data is the better data.

PROV-9, the year: 2019 is DVF's first publication. PROV-9 gives "a source that grows over time (a public register ...)
the year of the snapshot we pin". Precedents:
- chicago_traffic_crashes and sf_permit_time: "2026  # the snapshot we pin; the source grows over time (PROV-9)".
- noaa_storm_events_damage: 2026.
- This batch: fpa_fod_wildfire_cause_1m and ny_wcb_assembled_claims_1m (2026). nyc_motor_vehicle_collisions in this
  batch carries 2012, the same departure: a pair for its own panel.
A Must, so no exception: the year is 2026, and the BibTeX note can keep "open since 2019".

Consistency check (AI, 2026-11-09), on the release:

  Does the definition stay on Etalab's April-based release now that Etalab has published the October 2026 data with the
  same columns?

  **Problem:**
  - The reason given for the older release, that no newer Etalab release existed, no longer holds[6].
  - The newer release completes November-December 2025, adds 2026-S1, and keeps the mutation id and coordinates.
  - The older folder will be deleted on 30 November 2026, so the download lines break.

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Keep the April data, recording the fact: the definition's checks are measured on this pair of releases; archive the raw files | notes and download text | no rebuild | older data, a dead download link |
  | b | Re-source to the release of 2026-10-20 | rebuild; redo the cut and the completeness check | newer and complete, as the "better data" row says | a rebuild; the geocoding changes |

  **Recommendation:** b, unless the rebuild is deferred to a later version, then a with the fact recorded.
  **Decision:** a or b?

  [6]: PROV-8 (Must), PROV-9 (Must); principles.md Tensions, "Same task, another source" (Lennart, 2026-11-08).

**D8. Smaller calls checked**
- Echange, Expropriation and building-land sales dropped, and sales of several dwellings dropped: consistent with ames's
  AdjLand and Alloca, and with house_sales's 45, 5 and 1 ("the recorded price is not this house's alone", CC 2026-10-22).
- Auctions kept, with `nature_mutation` as an input: consistent with house_sales's "bankruptcy or forced sale" level
  (CC 2026-10-22) and ames's `Abnorml`.
- Single-dwelling sales over several parcels kept: house_sales dropped multi-parcel sales (warning 45). The fact that
  sets DVF apart is in the definition: every parcel's land is summed into the row (`n_parcelles`, `surface_terrain_*`),
  so the price matches what the row describes. Consistent, with a stated fact.
- Resales kept (SPLIT-13, USE-10): consistent with house_sales.
- 0 main rooms to missing: consistent with house_sales (0 bedrooms or bathrooms to missing).
- The impossible values kept: the 62 coordinates outside France, room counts up to 198 (476 rows under 4 m2 per room),
  and Carrez totals below 8 m2 (column auditor problems 5-7). The same pair was checked on 2026-10-20: perth kept
  impossible floor areas while melbourne set 86 `BuildingArea` values missing with no marker, which was called "departs,
  without a distinguishing fact". Perth then set 19 floor areas and 2 bathroom counts missing by within-row rules.
  DVF gives no reason.

  Consistency check (AI, 2026-11-09):

    Are the impossible coordinates and room counts set to missing, as perth and melbourne did?

    **Problem:**
    - 62 coordinates lie 500 km or more outside their commune, and 476 dwellings have under 4 m2 per main room[7].
    - perth (2026-10-20/26) and melbourne set such values missing by fixed rules within the row; DVF keeps them with no
      note.

    | | Option | What it does | Pro | Con |
    |---|---|---|---|---|
    | a | Set missing by fixed rules (a box per territory; floor area / rooms < 4 m2) | two masks in `_clean` | same as perth and melbourne | none to speak of |
    | b | Keep with a note naming them | notes only | no code change | departs from the pair |

    **Recommendation:** a. **Decision:** a or b?

    [7]: CLEAN-11 (Should), CLEAN-7 (fixed bounds, not row statistics); perth_house_prices REVIEW (2026-10-20).

DRIFT AND AMENDMENTS
- No drift found. Lennart's non-market line changed once, on purpose (2026-10-22 to 2026-10-26, house_sales reopened to
  match ames).
- No third exception is pending. The CLEAN-11 target clause is already an amendment. SPLIT-10's amendment_due flag
  (10 exceptions) gets no new member from this dataset.
- If the curator takes D1 (b) at 1,000 EUR as an exception, it is the first exception of its kind ("a target value that
  is no price of the unit, without the source's words").

Sources: .claude/skills/knowledge-curation/references/{principles,cleaning_features,leak_checks,splits,
metrics,provenance,selection,use_case}.md; curation/records/{ames_housing,house_sales,perth_house_prices,
zillow_prize,cook_county_residential_sales,france_dvf_property_sales}.md; datasets/_dev/tabarena-v0pt2/
{ames_housing,house_sales,perth_house_prices,zillow_prize,melbourne_housing_market,france_dvf_property_sales_1m}/
dataset.py; git history of perth_house_prices/REVIEW.md (5b2dc855 .. 031d3d39).

</details>

<details><summary>Advocate</summary>

ADVOCATE, OPENING BRIEF: france_dvf_property_sales (folder france_dvf_property_sales_1m), 2026-11-09

Position: ship after changes. The task is a real valuation evaluated honestly on 2.2M sales. The panel found two Must
problems. The VEFA rows break LEAK-10, and the year breaks PROV-9. A filter fixes the first and one field fixes the
second. Everything else is a weighing call, a cheap P7 mask or a wording fix. No option the evidence agents put on the
table excludes the dataset. The remedy ladder keeps exclusion for a Must that cannot be fixed, and none of these is one.

Changes that need no decision (part of shipping):
- year = "2026" (PROV-9).
- Notes. Count on the raw price: 2,589 strictly below 1,000 EUR and 3,214 at or below. Drop the house_sales citation.
  Limit the 906,747-line check to existing dwellings. Reword "by 31 December" to say most deeds are in within days
  and about 10% arrive months later. Say that the apartment "resales" are mostly twin units. Fix the 27,415 count.
  Say that a row is "as identifying as the published record, no more".
- license: add the CGU purpose clause ("concourir à la transparence des marchés") and say that a hosted copy must
  block indexing.
- download_description: name Etalab's release of 2026-10-20 and the deletion of the 2025-12 folder on 30 Nov 2026,
  and give the warehouse copy (sha256 recorded) as the reference.
- splits_comment: one sentence saying that the frame holds 2023-24 at about 65% and the test months in full (point 2).

1. The task is real and the evaluation is honest, on every Must the base needs.
   Claim: one row is one valuation file, predicted before the deed and tested on the next quarter. The split, the
   unit and the metric hold.
   Evidence:
   - Domain practitioner (Q1): "No input is one I would lack at the prediction point" (VEFA aside, point 5).
   - LEAK-16 holds. 143 of 2,222,274 kept sales (0.006%) hold two dwelling lines. Exact copies with the date: 0.0% of
     test rows. The 1,270 same-sale rows share a date.
   - The regime is temporal with known places: 96.2-96.8% of test rows fall in a cadastral section seen in training.
     SPLIT-14 holds: the train pools are 69.3-86.5% of the rows. The split auditor: "Nothing must change."
   - Value: the dummy scores RMSLE 0.81-0.84 and LightGBM 0.50-0.55. RF R^2 is 0.57, the task probes raise no flag,
     and every window holds 196k-219k test rows.
   - The blind reviewer, from the data alone: "a real and useful valuation task with plenty of signal and an honest
     temporal split."
   - rmsle with a log target is consistent with the house-price family (precedent checker D5).
   Rules: SEL-2, USE-1 (approximate), USE-10 (Must), LEAK-16 (Must), SPLIT-6 and SPLIT-14 (Must), TP, MET-11.
   Why it outranks: each objection below concerns a subset of rows, a field or wording, and the ladder fixes it in
   the definition. None touches the unit, the regime or the metric.

2. The 1M training cap (task gamer's flaw) needs no fix, and it also explains the blind reviewer's "2025 jump".
   Claim: the sample is label-free and uniform in time against the source. The "52-58% of the newest months" is an
   artefact of measuring against the shipped frame, not against the sales.
   Evidence:
   - Against the source, r0 keeps 0.518-0.522 of every quarter from 2023Q1 to 2025Q2. r1 keeps 0.577-0.582 and r2
     keeps 0.647-0.651 (split auditor, s5_sampling.log). The gamer's own test finds no dependence on the label: mean
     12.0748 in the sample against 12.0755 out, and within 0.005 per month.
   - The frame (data.parquet) holds 2024 at 0.644-0.654, the union of the train samples. It holds Feb-Oct 2025 at
     1.0, because those months are other repeats' test windows (v1_frame_vs_source.log). Measured
     against that frame, r0 seems to keep 80% of 2023-24 and 52% of 2025. Against the source it keeps 52% of both.
   - The same artefact is the blind reviewer's concern 2. The 2025/2024 ratio per month is 1.00-1.36 in the source
     and 1.54-2.11 in the frame. The data is one delivery under one filter (claim auditor recount: 2,222,274).
   - The gamer's "every pre-cutoff row" model trained on 1,357,830 rows for r0 and 1,160,385 for r1, against
     1,000,000. Its gain of 0.0037 and 0.0034 mostly comes from 36% and 16% more rows. r2, with no extra rows, gains
     0.0000. Size and recency cannot be separated in that design.
   - Even taken whole, the gain is 0.7% of the score. On the baseline it is inside noise (0.51666 against 0.51872),
     and the gamer's per-split spread is up to 0.003.
   Rules:
   - The v0.2 row budget is a curator's decision (Lennart, 2026-10-21; definitions.md, "Larger than the row budget":
     "a random train of all earlier rows for each train side, drawn in one random order").
   - SPLIT-11 and SPLIT-20 (Should): train on the whole history.
   - SPLIT-21 (Must).
   Why it outranks:
   - "Ship all rows" would break the curator's budget, and a curator's decision ranks above an AI proposal.
   - "Subsample uniformly in time" is already true.
   - A newest-first sample chosen for a 0.0035 gain on two windows is the comparison SPLIT-21 forbids as a reason.
   - It is not a P4 problem: every model gets the same label-free rows, as in every temporal _1m version
     (delivery_eta_1m, nyc_taxi_trip_duration_1m).

3. The split mirrors the use case, and issue 3 is fixed by one line of wording.
   Claim: the Nov-Dec cut and the 1-month gap remove the incomplete, price-selected months. The cadence question is
   settled by naming the actor, not by moving windows.
   Evidence:
   - December is 89.0% complete and November 95.2%, against 97.6-98.4% for January to October. December's present
     lines are dearer (3,153 EUR/m2 against 2,579-2,846).
   - Gap 1, gap 3 and the public-release cadence score within 0.001 RMSE of each other without the date (split
     auditor, s7).
   - Cutting resales from training moves the score by -0.0026 to +0.0012.
   - The gamer's exploits 0-2 (labels of the gap month and of later windows) exist only if a harness trains on
     data.parquet instead of the declared splits, which the protocol forbids ("never re-split"). That is not a
     dataset defect.
   - Exploit 3 (same-day counts over the test rows) gains at most 0.005 and 0 on r2. The gamer: "Accept it."
   Rules: SPLIT-10 (Should, applied as amended), SPLIT-12 (Should), SPLIT-21 (Must). Precedents: house_sales (one
   week) and zillow_prize (one month) (precedent checker D6: consistent).
   Remedy: narrow the actor in task_summary to "a notary or a tax-office valuer, who sees deeds as they are published"
   (domain practitioner). Then the 1-month gap's stated reason holds (D6). gap=3 is a one-number alternative with the
   floor kept (pools 63.4-80.7%). Both ship, and SPLIT-21 says to choose from the use case, not from these scores.

4. P1: SEL-1 holds and the coordinates stay.
   Claim: the dataset is no more identifying than DGFiP's and Etalab's own publication, and no option of issue 2
   lowers identifiability.
   Evidence:
   - The published geo-DVF file carries the same coordinates, with the address.
   - Without any coordinates, (date, price, commune, floor area, type) is unique for 99.91% of rows. Every option
     leaves the rows linkable to the published file, so rounding or dropping buys no protection. Rounding still
     costs signal: longitude alone has R^2 0.081 (claim auditor, claim 25; column auditor).
   - The CGU bar ("pas ... plus important que celui ... du jeu de données mis à disposition") is met. The publisher
     publishes for transparency and for "recherche publique" (CGU p. 1).
   - No subject or creator objects to ML use. Removal requests are refused because publication is a legal duty
     (FAQ).
   Rules: SEL-1 (Must, P1). Precedents: zillow_prize (6 decimals), house_sales and miami_housing (D3: consistent).
   Remedy: the license string and the notes' wording (listed above), with no data change.
   Why it outranks: P1 ranks first, so it is answered first, and the measurement says it holds.

5. VEFA (LEAK-10, Must): conceded, and fixed by one filter.
   Evidence:
   - 2,544 of 7,972 VEFA keys of 2025 gain a dwelling between the two releases.
   - VEFA is 0.49-0.78% of the test windows against 1.68-1.89% of the train sides, so the rows are selected by
     completion after the sale.
   - The effect on the score is not measurable. VEFA is 0.5-0.8% of test rows and `nature_mutation` marks it. The
     price per m2 is flat (4,682 / 4,619 / 4,685 EUR).
   Remedy, the mildest that resolves it: drop VEFA in `_clean` (33,807 rows, 1.5%), as perth_house_prices dropped its
   off-the-plan sales. `nature_mutation` keeps Vente and Adjudication.
   - Keeping VEFA with a note would need the curator to read a LEAK-10 clause into it, plus a measurement that the
     selection is price-neutral given the inputs. That measurement has not been made, so I do not argue for keeping.
   Why: independent failures are not conflicts. This Must has to hold, and it holds after the filter. The ladder puts
   "fix the definition" above exclusion.

6. Non-market prices (issue 1): the dataset ships under every option, and I support (b).
   Evidence:
   - Prices strictly below 1,000 EUR are 0.09-0.12% of test rows and carry 22-25% of the squared log error (claim
     auditor re-run). 1,073 sales are at exactly 1 EUR.
   - The source calls the field a "montant ou évaluation déclaré(e)", and Cerema's own filter drops 0 and 1 EUR and
     sales under 100 EUR.
   - The 10M+ sales carry at most 0.21% of the error, and the multi-parcel estates are real valuations whose land the
     row describes (D8). Option (c) adds nothing.
   Rules: USE-5 (Must), CLEAN-11 (Should, amended 2026-10-21: a row whose target the source names as not the task's
   quantity may leave, with the source's words), CLEAN-15.
   Why it does not exclude:
   - Keeping, as defined, follows perth_house_prices (D1: consistent), so the definition breaks no rule.
   - (b) cuts at 1,000 EUR or less on the raw `valeur_fonciere` before the log (3,214 rows, 0.14%). Up to 100 EUR it
     applies CLEAN-11 with the source's words. From 100 to 1,000 EUR it rests on a stated fact, the curator's reading.
   - The remaining partial-rights rows (1.2% of rows priced below a fifth of their commune's median) cannot be told
     apart by any input. Filtering them would be a floor of our own on the target, so they stay, named in fit_reason
     under USE-5's approximate clause.
   - The domain practitioner accepts RMSLE once (b) is applied.

7. Provenance and cleaning: fixes, not grounds to exclude.
   PROV-9 (Must): the year goes to 2026, the pinned snapshot of a growing register. Precedents: chicago_traffic_crashes,
   sf_permit_time, noaa_storm_events_damage.
   PROV-8 holds: DGFiP is the source, and Etalab's copy is named and cited.
   Release, my lean is (a): keep the April-based data now and record the fact.
   - Every check that makes this definition honest pairs this release with DGFiP's October 2026 one: the Nov-Dec cut,
     the attribute stability and the VEFA finding.
   - Re-sourcing to Etalab's 2026-10-20 release changes the geocoding and adds two months of 2025. Its own newest
     months (2026-S1) cannot be checked against a later release before April 2027 ("against nothing newer", claim
     auditor).
   - That makes the re-source a new version, not a repair of this one. The precedent checker allows (a) "with the fact
     recorded" when the rebuild is deferred.
   P7, under CLEAN-11 (Should) and CLEAN-7, following the perth and melbourne pair:
   - Set missing the 62 impossible coordinates (lat 40.88-83.52 in department 92), using a fixed box per territory.
   - Set missing the room counts below 4 m2 of floor area per room (476 rows), a fixed rule within the row.
   - These are two masks, cheap and safe.
   code_section (CLEAN-14, Should; the zillow_prize precedent):
   - Keep it, recording the fact that sets it apart. The notice describes a section as "un ou plusieurs lieux-dits ...
     quartiers", the cadastre's named unit that valuers use, unlike a census block group.
   - Otherwise drop it.
   - The score cannot decide (0.547 against 0.548), and it is a quality call (P7) either way.
   Why: the principles' step 3 says a P7 problem is fixed when the fix is cheap and safe, otherwise kept with a note,
   and never excludes.

Judgment record (advocate's):
Verdict: ship after changes.
Validity:
- SEL-1 holds (the CGU bar is met; wording only).
- USE-1 holds (approximate).
- USE-5 holds under issue 1 (a) or (b), with (b) preferred.
- LEAK-10 triggered for VEFA; fixed by dropping 33,807 rows.
- LEAK-16 holds.
- SPLIT-10 holds (cut and gap 1, measured).
- SPLIT-14 holds (69.3-86.5%).
- PROV-9 triggered; fixed (2026).
- PROV-8 holds.
Value: no TP flags. MET-11 rmsle is consistent with the family.
Quality: CLEAN-11 masks for the coordinates and the room counts. code_section kept with its fact, or dropped.
Weighed:
- size +, source +
- features - (no year built, no DPE)
- the 1M cap 0 (label-free and uniform; at most 0.7% of the score)
For the curator:
- issue 1, (a) or (b)
- VEFA: drop, or a note with a measurement
- issue 3: the actor's wording, or gap=3
- the release: (a) now, or (b) rebuild
- code_section: keep with its fact, or drop

</details>

<details><summary>Advocate rebuttal</summary>

ADVOCATE, REBUTTAL: france_dvf_property_sales (folder france_dvf_property_sales_1m), 2026-11-09

The critic and I agree on the verdict ("ship after changes"), on exclusion (none) and on most remedies. Here I
concede where the evidence is with the critic and dispute only three framings, each with evidence.

A. The 1M cap. Agreed (c1_sampling.log matches the split auditor's s5 and my v1 log). Whether the budget is called a
   house rule or a curator's decision, the result is the same: it is not weighed against this dataset.

B. Same-day, same-parcel rows. Agreed: they are separate deeds (c2_sameday.log). The rows are already collapsed by
   id_mutation (LEAK-16), and the count exploit gains at most 0.004 and nothing on r2.

1. P1, SEL-1. Conceded. My remedy was the same:
   - put the purpose clause, citing CGU p. 2, in `license`;
   - reword the privacy bullet to "as identifying as the published record, no more";
   - settle issue 2 as (a).

2. USE-5, the non-market prices. I concede the remedy: drop raw `valeur_fonciere` <= 1,000 EUR before the log
   (3,214 rows), keep the 10M+ sales, delete the house_sales citation, and name the partial-rights rows (1.23%) in
   fit_reason. I dispute one framing. "As defined it breaks USE-5" holds only up to 100 EUR, where CLEAN-11's
   source-words clause applies: the notice's "montant ou évaluation" and Cerema's filter. The 100-1,000 EUR band
   (1,946 rows) rests on a judgement no source states. The precedent checker (D1) calls keeping "consistent with
   perth" and calls the band "an application or a narrow exception, the curator's reading". So the cut is right, but
   from 100 to 1,000 EUR it is the curator's call with the fact recorded, not a Must the definition breaks.

3. USE-1 and USE-3, the actor and the gap.
   - Conceded: "a lender" does not match the gap. A lender works from public DVF with a 4-10 month lag (domain
     practitioner; D6). Either text fix (a) or gap=3 (b) settles it, and both keep the floor.
   - Disputed: the critic uses the split auditor's +0.084 mean residual on the Feb-Apr window as evidence that the
     test does not mirror the application. That residual comes from models that read the date as a number and carry
     the level of the last training month into the window. It appears under every cutoff: the public-release cut
     gets +0.106 to +0.119. Without the date, gap 1, gap 3 and the public cadence score within 0.001 (s7). So the
     residual measures the date encoding, not the gap.
   - Under SPLIT-21 (Must) this measurement cannot decide the gap anyway. The choice comes from the actor.
   - I keep my lean for (a): a DGFiP valuer checking a declared value prices at the deed and sees deeds as they are
     published, so gap 1 is that actor's gap (SPLIT-10). The question and use_case lines must then be reworded to
     match. (b) is as good if the curator wants a pre-sale valuer.

4. LEAK-10, VEFA. Conceded, with the same remedy: drop VEFA (33,807 rows, 1.5%) and limit the 906,747-line note to
   existing dwellings. The critic's citation of LEAK-6 settles my one hesitation (no measured score effect).

5. PROV-9 and PROV-8.
   - Conceded: year 2026, and the download text rewritten to name the 2026-10-20 release, the deletion date and the
     archived raw files with their sha256 values.
   - Disputed: the label. PROV-8, which names the source, holds: DGFiP is the source and Etalab's copy is named and
     cited (D7: consistent). The false sentence ("the only dated release online") is a notes error under writing.md,
     with the same fix.
   - Disputed: re-sourcing as the default.
     - The tension row "Same task, another source" lets better data enter.
     - The October release adds two months of 2025 and 2026-S1. Its newest months cannot be checked against a later
       release before April 2027.
     - The cut and gap this definition ships were set from a measured comparison of two releases (SPLIT-10, LEAK-24).
       A re-source would ship an end of release that has not been measured, and it would change the geocoding.
     - The precedent checker accepts (a) "with the fact recorded" when the rebuild is deferred.
     - So (a) now and (b) as a later version is the milder remedy on the ladder. This stays the curator's weighing,
       as the critic says.

6. P7, impossible values.
   - Conceded: the coordinates outside a fixed box per territory, and rooms where floor area / rooms < 4 m2.
   - Disputed: masking every Carrez total below 8 m2. Of the 443 rows (437 of them apartments):
     - the median floor area is 10 m2;
     - 142 have a floor area below 9 m2, and their tiny Carrez area agrees with it;
     - 141 have a floor area of 20 m2 or more (v2_carrez_small.log).
   - The definition keeps 1,180 floor areas below 9 m2 as attic rooms (CLEAN-11: "values that are only unusual
     stay"). Masking their matching Carrez areas would treat one room two ways.
   - Milder rule: a fixed ratio within the row. Set Carrez missing where it disagrees with the floor area (below 8 m2
     with a floor area of 20 m2 or more, or more than 3 times the floor area and above 200 m2: 276 rows, column
     auditor). Keep the consistent small rooms.

7. code_section and the notes.
   (a) Conceded: record the distinguishing fact or drop the column as in zillow_prize. Curator's call, P7.
   (b) Conceded, all five corrections. They match my no-decision list. The sentence on the frame's shape can go in
       version_comment or splits_comment.

Net effect on my opening: no point withdrawn. Point 6 now leans firmly to the cut, at 100 EUR as an application and
from 100 to 1,000 EUR as the curator's reading. Point 3 concedes the actor. Point 7 adds a ratio rule for Carrez in
place of a blanket floor.

</details>

<details><summary>Critic</summary>

CRITIC, OPENING BRIEF: france_dvf_property_sales (folder france_dvf_property_sales_1m), 2026-11-09

Position: ship only after changes. Nothing here calls for exclusion. The task is real (a home's price from the
land-registry description, temporal, 196k-219k test rows per window), and every problem below has a fix in the
definition or the notes. As defined, it breaks four Musts (USE-5, USE-1/USE-3, LEAK-10, PROV-9), and its download
text is false (PROV-8).

My scripts and logs are in the run's work files (c1_sampling.py/.log, c2_sameday.py/.log), run on the claim auditor's
curated frame (2,222,274 rows, with id_mutation and id_parcelle) and the participant kit.

**THE TASK GAMER'S TWO OPEN QUESTIONS, SETTLED FIRST (EV-1)**
A. Does the 1M cap thin the newest training months? No. The split auditor is right.
   * Measured against the full curated pool, each train side keeps the same share of every quarter: r0 0.518-0.522,
     r1 0.577-0.582, r2 0.647-0.651, from 2023Q1 to its last training quarter (c1_sampling.log).
   * The task gamer divided by the shipped frame instead (explore2.py reads data.parquet). The frame holds only the rows
     some split uses: 2023-24 at 65% of the source (the union of the train samples, which equals r2's 1,000,000 rows),
     2025Q1 at 87%, and February 2025 onward in full (test windows). So "80% of 2023-24 against 52% of 2025" is an
     artefact of the denominator. Against the source, both are 52%.
   * The kit's "every pre-cutoff row" is 1,357,830 rows for r0 and 1,160,385 for r1 (r2: exactly its 1M), with 2025
     over-represented. The 0.0034-0.0037 gain therefore comes from more rows and more recent rows. That is the cost of
     the 1M budget, a house rule of TabArena v0.2 (definitions.md, "Larger than the row budget"; Lennart, 2026-10-21),
     which is never weighed. It is not a flaw of the definition. Dropped as a point.
   * The same frame shape explains the blind reviewer's "unexplained 2025 jump". Frame 2025Q2 against 2024Q2 is 1.74x;
     in the source it is 1.13x. A notes fix (point 7).

B. Are same-day, same-parcel rows one DVF mutation split into several rows? No evidence of that (c2_sameday.log).
   * 35,730 rows (1.61%) sit in 16,864 groups that share a date and a parcel. In 34,038 of them the prices differ. Those
     are separate deeds (12.6% VEFA: programme sales), priced at the local level: the median log of price per m2 against
     the commune and type median is -0.04, against 0.00 for single rows.
   * 1,692 rows (828 groups) share one price. If one deed's total price were repeated on split rows, each row's price
     per own m2 would sit about +0.7 log above the local level. It sits 0.26 below (and 0.98 below if divided by the
     group's summed area). None of the 828 groups has consecutive Etalab ids, which the lines of one deed would carry.
   * The definition already collapses by id_mutation. So the count exploit counts other deeds in the test batch. No
     stored value depends on the test rows (LEAK-5). The gain is at most 0.004 (<1%), and nil on r2. Dropped as a
     point; at most one sentence in the notes.
   * Also not a point: gap-month and later-window labels in the kit. The harness hands a model only the train rows.

**POINTS, IN RANK ORDER**
1. P1, SEL-1 (Must) and selection.md "Ethics, licence" (note the terms): the purpose clause is missing, and a
   protection is claimed that does not exist.
   Problem:
   * The CGU (p. 2) allow reuse only "pour répondre à l'objectif poursuivi par le législateur (à savoir concourir à la
     transparence des marchés fonciers et immobiliers)", and they count the file as personal data. Neither the
     `license` field nor the notes say so.
   * The notes say the dropped address, parcel id and lots stop a row from pointing to one property. In fact the
     6-decimal coordinates map 1:1 onto 1,481,249 parcels. (date, price, commune, floor area, type) alone is unique for
     99.91% of rows, so every row links back to its published record, address included.
   Effect: the curator weighs SEL-1 on a false premise, and a user does not see the purpose limit. This is no reason
   to exclude: the CGU's bar ("pas ... plus important que celui ... du jeu de données mis à disposition") is met under
   every option of issue 2.
   Evidence: claim auditor claims 2 and 25; column auditor problem 1; precedent checker D3.
   Remedy, a note:
   * add the purpose clause, with "CGU p. 2", to `license`;
   * reword the bullet to "a row is as identifying as the published record, no more".
   Issue 2 can then settle as (a), keep the coordinates.

2. P3, USE-5 (Must), fixed through CLEAN-11's source-words clause: the target keeps declared amounts that are not the
   price of a dwelling.
   Problem:
   * 2,589 sales are below 1,000 EUR. 1,073 of them are at exactly 1 EUR, and the rest are round amounts (500 EUR 354,
     100 EUR 188, 200 EUR 90). Another 625 sit at exactly 1,000 EUR.
   * 2,587 of the 2,589 are `Vente`, and no input marks them.
   Effect: in the claim auditor's re-run with the container's scorer, the rows below 1,000 EUR carry 21.9% (window 0)
   and 25.1% (window 2) of the squared log error, while they are 0.085% and 0.12% of the rows. So about a quarter of
   the ranking rewards hedging on rows a valuer never prices. The domain practitioner calls RMSLE acceptable only once
   these rows are gone.
   Rules and words:
   * The source names the field "montant ou évaluation déclaré(e)" (notice, column 11).
   * Cerema's DVF documentation evicts 0-1 EUR prices and suggests evicting those below 100 EUR.
   * CLEAN-11: "a row whose target the source names as not the task's quantity may leave, with the source's words".
   * The definition says it keeps low prices "as house_sales and perth_house_prices" do. house_sales has no low prices
     (its target starts at $75,000) and dropped its non-market sales on the county's markers (precedent checker D1).
   Remedy, fix the definition:
   * in `_clean`, drop raw `valeur_fonciere` <= 1,000 EUR before the log (3,214 rows). Record the 100-1,000 EUR band
     with its fact, as the precedent checker's option (a).
   * Keep the 10M+ sales: they carry 0.1-0.2% of the error.
   * Count on the raw price. exp(ln 1000) < 1000 is why the notes and the decision table count 3,214 "below 1,000".
   * Delete the house_sales citation.
   * Name the remaining unmarked partial-rights transfers in fit_reason: 1.23% of sales below a fifth of their
     commune's median (domain practitioner).

3. P3/P4, USE-1 and USE-3 (Must), SPLIT-10 (Should, "a planning gap the use case has is a gap too"): the stated
   actor and prediction point do not match the one-month gap.
   Problem:
   * The use case is "a lender, a notary or a valuer" who prices a home "before it sells, for a loan, an offer or a
     listing", refit on "sales recorded until a month earlier".
   * But date_mutation is the deed's date, and the price is set at the compromis about 3 months earlier (split
     auditor, sources PAP and Square Habitat). With gap 1, a train side holds deeds signed up to about 2 months after
     the earliest test sales of its window were priced.
   * A lender works from public DVF, released twice a year with a 4-10 month lag (domain practitioner). The precedent
     checker (D6) finds the quarterly cadence justified only for an insider.
   Effect: with the date as an input, a model sets a window's level from the last training month, which is seasonal
   (+0.084 mean residual on the Feb-Apr window; split auditor). The test does not mirror the stated application.
   Remedy, the curator's choice between two mild fixes (SPLIT-21: not from scores):
   (a) text only: name an actor whose prediction point is the deed's publication and who sees deeds as they are
       published (a DGFiP valuer checking a declared value; domain practitioner), and keep gap 1;
   (b) keep a pre-sale valuer, drop "a lender", and set `gap=3`. That is one number. SPLIT-14's floor holds at
       80.7/71.9/63.4%, and without the date it costs at most 0.001 (split auditor's lean).
   As defined, neither holds.

4. P4, LEAK-10 (Must): off-plan (VEFA) sales enter the frame only after the sale, when the cadastre attaches the
   finished dwelling.
   Evidence:
   * The share of VEFA mutations that carry a dwelling falls from 26-28% (2023 quarters) to 6.1% (2025Q4), with no
     fall in VEFA volume (column auditor a3/a4).
   * 2,544 of the 7,972 VEFA keys of 2025 that have a dwelling in DGFiP's October 2026 file had none in this release.
     For ordinary sales the same count is 44 of 874,021 (claim auditor t3).
   * VEFA is 0.49-0.78% of the test windows against 1.68-1.89% of their train sides.
   * The 906,747-line stability check matched on type_local, so it could not see a dwelling added later.
   Rule:
   * LEAK-10 puts out "attributes looked up after the outcome ... unless the data shows they did not change". Here
     they went from absent to present.
   * LEAK-5: "models predict the same" is no defence.
   * LEAK-37 (planned type and area known to the buyer) covers values, not which rows exist (precedent checker D2).
   * Precedent: perth_house_prices dropped its off-the-plan sales (USE-7, shipped 2026-10-26).
   Effect: the presence and the description of a VEFA row come from after the sale. Train and test VEFA rows are
   selected differently: the test holds the ones completed fast. The split auditor measured no score effect, but
   LEAK-6 says a confirmed leak goes even when small.
   Remedy, fix the definition:
   * drop `Vente en l'état futur d'achèvement` in `_clean` (33,807 rows, 1.5%);
   * scope the 906,747-line note to existing dwellings.

5. P5, PROV-9 and PROV-8 (Must): wrong year, and download text that is false and about to break.
   * PROV-9: "a source that grows over time (a public register ...) takes the year of the snapshot we pin". year is
     "2019"; it should be "2026", as for chicago_traffic_crashes, sf_permit_time and noaa_storm_events_damage. The
     BibTeX note can keep "open since 2019".
   * PROV-8 (the instructions name the copy we download):
     - download_description says the 2025-12 folder is "the only dated geo-dvf release online".
     - Etalab published the October 2026 delivery on 2026-10-20, with the mutation id and the coordinates.
     - The data.gouv.fr API labels the 2025-12 folder "suppression au 31/11/2026", so the wget lines break this month.
     - Builder issue 4's premise ("revisit when Etalab publishes") is refuted (claim auditor claim 5).
   Remedy:
   * set year = "2026";
   * rewrite download_description: name the October 2026 release and the deletion date, and point to the archived raw
     files (the sha256 values are already recorded).
   * Re-sourcing to the 2026-10-20 release (Nov-Dec 2025 complete, 2026-S1 added) is the curator's weighing under the
     tension "Same task, another source" (newer, better data enters). The precedent checker recommends it.

6. P7, CLEAN-11 (Should): impossible values kept, with no note. Quality only, not a reason to hold the task.
   * 62 coordinates in four Hauts-de-Seine communes lie at latitude 40.88-83.52, more than 500 km from their commune.
   * 115 dwellings have more than 20 main rooms (up to 198); 476 have under 4 m2 per room.
   * 443 Carrez totals are below 8 m2, which the Carrez definition excludes; 43 are above 1,000 m2.
   Precedent: perth and melbourne set such values missing by fixed within-row rules (2026-10-20/26); DVF gives no
   reason to differ (precedent checker D8).
   Remedy, cheap and safe:
   * set longitude and latitude missing outside a fixed box per territory;
   * set rooms missing where floor area / rooms < 4 m2;
   * set Carrez missing below 8 m2.

7. P7, CLEAN-14 and CLEAN-3 (Should), and the notes (writing.md).
   (a) code_section:
       * 217,872 levels, about 10 sales each, and the coordinates hold the same place (hidden-groups s_id 0.336 for
         the section, 0.332 for longitude).
       * zillow_prize dropped its census block group of the same grain as a near-identifier (CC 2026-10-26).
       * The builder's reason, CLEAN-22 (width), does not answer that.
       Remedy: record the distinguishing fact (the cadastre's named neighbourhood, which valuers use) or drop the
       column as zillow did.
   (b) Wrong or misleading statements in the notes:
       * "3,214 below 1,000 EUR" (point 2).
       * The n x p bullet: 143 kept sales hold more than one distinct dwelling line, 68 of them two dwellings of
         different area.
       * "67,836 dwellings sold more than once": 35,102 of 43,169 apartment groups are distinct twin units.
       * "89.0% by 31 December": 73% of the deeds signed on 31 December are present; most deeds are recorded within
         days and about 10% months later.
       * Nothing says that the frame holds 2023-24 at 65% and 2025 from February in full. Both the blind reviewer and
         the task gamer read that shape as the data's.
       Remedy: correct the text; add one sentence to version_comment.

**JUDGMENT RECORD (critic's draft)**
Verdict: ship after changes.
Validity: SEL-1 holds, note owed (CGU purpose clause; privacy wording). USE-5 triggered, fix: drop declared amounts
<= 1,000 EUR on the raw price. USE-1/USE-3 triggered, fix: an actor at the deed's publication, or gap 3. LEAK-10
triggered, fix: drop VEFA. PROV-9 triggered, fix: year 2026. PROV-8: download text corrected and raw files archived.
SPLIT-11/SPLIT-14 hold (uniform 1M sample, c1). LEAK-16 holds for same-day groups (c2).
Value: TP holds; MET-1 rmsle holds once USE-5 is fixed.
Quality: CLEAN-11 masks for coordinates, rooms and Carrez; CLEAN-14 code_section consistency check against
zillow_prize; notes corrected.
Weighed: re-source to Etalab's October 2026 release (newer and complete) against a rebuild (curator).
For the curator: point 3 (a) or (b); point 5 re-source or not; point 7 (a) keep or drop the section.

</details>

<details><summary>Critic rebuttal</summary>

CRITIC, REBUTTAL: france_dvf_property_sales (folder france_dvf_property_sales_1m), 2026-11-09

The advocate and I agree on the verdict (ship after changes) and on most remedies. Two disputes remain: point 3 (who
the actor is) and point 6 (whether keeping the sub-1,000 EUR prices is an option at all). The rest I concede.

A1. The task is real and the evaluation honest: CONCEDED. I never argued exclusion. The unit, the regime, SPLIT-14,
    LEAK-16 and the value probes hold. One qualification: USE-1 holds only once the actor is fixed (A3 below), so
    "every Must the base needs" holds after the changes, not as defined. The 143 sales with two dwelling lines (68 of
    different area, 0.006%) are negligible; a note suffices.

A2. The 1M cap: CONCEDED. My own count agrees (c1_sampling.log: 0.518-0.522, 0.577-0.582 and
    0.647-0.651 of every source quarter). The cap is the v0.2 house budget, and the frame-shape sentence settles the
    blind reviewer's 2025 jump. It makes no difference whether that sentence goes in splits_comment or
    version_comment.

A3. The split, issue 3: PARTLY DISPUTED. I agree that the cut and gap 1 hold for the publication delay, and that the
    fix is the actor's wording or gap=3, not the scores (SPLIT-21). I dispute the advocate's wording, "a notary or a
    tax-office valuer":
    * A notary does not price the deed. The price is fixed at the compromis about 3 months before date_mutation
      (split auditor: PAP, Square Habitat), and a notary's avis de valeur for a listing comes earlier still. So with a
      notary in the use case, the train side still holds deeds signed after the test sale was priced. That is the
      planning gap SPLIT-10 names ("a planning gap the use case has is a gap too"), and USE-3 (Must) asks for the
      prediction point to be named as it is.
    * Only an actor whose prediction point is the deed's publication fits gap 1: a tax-office valuer checking the
      declared value as the deed comes in.
    * Under that actor, the question and use_case texts ("before it sells, for a loan, an offer or a listing") change
      too.
    * The family precedents (house_sales one week, zillow one month) gap only the recording delay. The compromis delay
      of about 3 months against a US escrow of 30-45 days is the fact that sets DVF apart (split auditor).
    Remedy, unchanged: either (a) the tax-office actor alone, with gap 1 and the question reworded, or (b) a pre-sale
    valuer with gap=3. Their judgment line "SPLIT-10 holds (gap 1)" is true only under (a).

A4. P1, SEL-1 holds and the coordinates stay: CONCEDED. This was my point 1, with the same remedy (license purpose
    clause, reworded note, no data change). The license string already says "no indexing by search engines".

A5. VEFA, LEAK-10: CONCEDED. We agree: drop VEFA (33,807 rows), and scope the 906,747-line note to existing
    dwellings.

A6. Non-market prices: DISPUTED on one claim, "keeping, as defined, follows perth_house_prices, so the definition
    breaks no rule".
    * Perth is not a like case. Its lowest price is a plausible price of a property ($51k), and the precedent checker
      says so ("Perth's lowest price is a plausible price"). DVF holds 1,073 sales at 1 EUR, and the source calls the
      field "montant ou évaluation déclaré(e)".
    * principles.md: a precedent is followed only when no fact sets the case apart. Here the fact does, and the
      definition's own reason for keeping (the house_sales citation) is wrong.
    * USE-5 (Must) asks for the quantity the actor acts on. A 1 EUR transfer is not a market price, and these rows
      decide 22-25% of the squared error. The tension row "a cleaning gap that changes what the target means is a
      validity question (P3)" applies.
    * So option (a) would be a departure from a Must, which can have no exception (principles.md, "Strengths"). It is
      not a free choice.
    I agree on the rest: cut at <= 1,000 EUR on the raw price, keep the 10M+ sales, name the partial-rights rows in
    fit_reason. Remedy: the curator's choice is the band 100-1,000 EUR (recorded with its fact), not whether to cut.

A7. Provenance and cleaning: CONCEDED, with two notes.
    * PROV-9: we agree, 2026.
    * PROV-8: the advocate already lists the download_description fix among its changes, which settles my point.
    * Release: I concede (a) for this version. Every check of the definition pairs this release with DGFiP's October
      2026 file, and a re-source re-geocodes and leaves the newest months unchecked: that makes it a new version, not
      a repair. Condition: the fact and the archived raw files go into download_description (the precedent checker's
      fallback).
    * Masks: agreed on coordinates and rooms. The advocate drops my third mask: Carrez totals below 8 m2 (443) are
      impossible by the Carrez definition (column auditor problem 7), the same kind under CLEAN-11 (Should). I hold it
      as a cheap third mask, or a note; it is no reason to hold the dataset.
    * code_section: we agree, keep it with its fact or drop it, a P7 curator call.

Rebuttal judgment line: ship after changes. Agreed: VEFA dropped, year 2026, license and notes reworded, download text
corrected, the release kept with the fact recorded, masks, code_section's fact. Disputed: USE-5 needs the cut (not
"(a) or (b)"); USE-1/USE-3 need the tax-office actor with gap 1, or gap 3 (not "a notary").

</details>

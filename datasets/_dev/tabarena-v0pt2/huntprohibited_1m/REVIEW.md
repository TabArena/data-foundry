# huntprohibited

**Outcome:** added as `huntprohibited_1m`. Avito's moderation decisions on 1.5M classified ads (binary: blocked for
illicit content or not), from the Russian title, description and form text plus category, price and the counts of
masked contacts; a random split, tagged `ForcedIIDFromTemporal` (a task that is temporal by nature, split at random
because the file has no dates). The AI recommends shipping; the review panel's changes were all to text and are in
dataset.py.

```text
Verdict: ship (the panel's changes were text only and are made; the data, cleaning, target and split are as built).
Validity: SEL-1 holds (content and licence noted, EV-4); SEL-12 holds (LightGBM on the structured columns plus
  TF-IDF reaches ROC AUC 0.987 against 0.994 for a TF-IDF logistic regression); USE-5 holds (is_blocked);
  USE-3 triggered, fixed in text (the row is the ad's last version, the price is final); USE-8 triggered, fixed in
  text (second gap: content only; the cohort in `row`); LEAK-10 triggered, fixed (close_hours, is_proved dropped);
  LEAK-19/20/21 hold; SPLIT-8 applied (forced IID), its note on what a date would change now written;
  SPLIT-29/25 not triggered in the AI's reading (per-ad label, source wording only; grouping by description moves
  ROC AUC by at most 0.0006); the curator's call, issue 4.
Value: task probe clean; LightGBM minus linear +0.050 ROC AUC (paired SE 0.001); average precision spreads 0.51-0.95 across
  pipelines.
Quality: CLEAN-10 price codes kept with a note; CLEAN-19 over CLEAN-12 for `attrs` (kept as text, as the winners).
Weighed: real task +, size +, source (Avito's own competition data) +, text-heavy -, near the ceiling in ROC AUC -.
For the curator: issue 4 (sellers against the emscad precedent), issue 9 (the Spatial tag).
```

**Main points:** Does the per-ad label set this dataset apart from emscad, which was grouped by poster (issue 4)? Add
the `Spatial` tag (issue 9)?

**Record judgment:** valid with concerns. A real content screen for Avito's moderation queue on the source's own data;
the time axis is lost (the cost cannot be measured, because the April labels were never published), and the Russian
text carries most of the signal, though tabular models on vectorised text come close to the best text model.

**Issues for Lennart:**

4. **Sellers: keep the split by ad, unlike emscad's split by poster?** The file has no seller id, and the phones,
   e-mails and links are masked without a hash, so ads cannot be grouped by seller. The curator's comment on the
   record (CC line) names the problem:
   "malicious users, who one should detect instead of the ads itself". You grouped emscad, the same kind of
   moderation task, by poster (2026-09-30), and its ROC AUC fell from 0.99 on a random split to 0.94; under SPLIT-25,
   maternal_health_risk was retired because its real groups could not be recovered.
   - Effect: if a seller's ads share one label, a model learns the seller from ads in train and scores the seller's
     other ads in test; the random split then overstates how well it screens a new seller. Without a seller id, by
     how much cannot be measured.
   - Evidence that sellers do not carry the label here: the data page speaks of ads "blocked for illicit content", so
     the label is set per ad; emscad's was set per client (the EMSCAD paper by Vidros et al., Sec. 5; 4,439 of 4,441 posters have one label).
     The key closest to emscad's identical company profile is the ad's description text. The split audit tried four
     exact keys: the raw description (30+ characters), the description reduced to letters (30+), its first 100
     letters (descriptions of 60+) and the title with the normalised description. By these keys, 1.4-4.9% of the test
     ads have a near copy in train, 99.5% of them with the same label. A split that keeps all ads with one key on the
     same side (GroupKFold, fold 0, a word n-gram logistic regression) gives ROC AUC 0.99384 on the first-100-letters
     key and 0.99386 on the letters-only key, against 0.99390 for the random split, and average precision within
     0.002.
   - Against: "per ad" is the page's wording, not a measurement (EV-2), and a seller who rewrites every ad escapes
     every test.
   - Implemented: (a) a random split by ad, exact copies dropped; the notes give the per-ad label and the grouped run
     as the fact that sets the case apart. The mediator, the advocate and the critic recommend it.
   - Alternatives: (b) group on the exact description key (changes nothing measurable); (c) retire under SPLIT-25 (the collection loses its only large
     text-moderation task, on no measured evidence that sellers matter); (d) reopen emscad to match (its grouped run
     did move ROC AUC, 0.99 to 0.94).
   - Rule: SPLIT-29 and SPLIT-25 (Must); precedents emscad and maternal_health_risk.
   - Decision: (a), (b), (c) or (d).

9. **Add the `Spatial` tag?** The tag marks data that hold geographic information ("ZIP, latitude and longitude,
   region, store location", definitions.md). Here 901,011 ads (22.5% of the file, all real estate) hold a street
   address inside the `attrs` form text. emscad carries the tag for a free-text location string without coordinates.
   The definition gives no reason for leaving the tag off; the earlier reason ("no region or coordinates") applied to
   emscad too.
   - Effect: metadata only; no score changes.
   - Implemented: no tag.
   - For leaving it off (the advocate's lean): the address sits inside one category's form string, and the dataset
     has no geographic column. For adding it: the tag's definition, and the emscad and perth_house_prices precedents.
   - Alternatives: (a) no tag, with the nested-address reason written into the notes; (b) add `Spatial`; (c) remove
     emscad's tag; (d) amend the tag to require a geographic column.
   - Rule: the `data_tags` house rule of definitions.md (a tag, not validity).
   - Recommendation: none from the mediator; the advocate leans to (a), and the critic accepts either (a) or (b).
   - Decision: (a), (b), (c) or (d).

**Review panel:** ship after changes (mediator), 2026-10-20. Claim audit: most claims hold; refuted or
overstated were "every new ad has both" subcategory and attrs (attrs is missing on 2.8%), the mask counts in part,
"loses most of the task" (true for the error and average precision, not ROC AUC) and an undocumented price code, all
fixed in dataset.py; untested: whether the row is the ad's last version beyond the price, the April copy share, two
use-case inferences and the sellers. Blind review: include with changes; main concern a text task near the ceiling.
Debate: agreed on the data, the split and every remedy; disputed how severe the SPLIT-8 and USE-3 gaps are (settled:
text fixes, in dataset.py); the sellers (issue 4) and the tag (issue 9) go to the curator. The reports cite this file's
earlier issue list as "REVIEW_before" (issues 1-9, of which 4 and 9 remain), and the mediator numbers those two 1 and
2. The reports quote the definition as it stood before the text changes.

<details><summary>Mediator</summary>

**Summary**

I recommend shipping huntprohibited_1m after changes. Every change is to text: `task_summary` and `curation_comments`. The data, `_clean`, the features, the target and the split stay as they are, so only the checksum changes. On the two disputed points the critic's label wins and the advocate's remedy wins. SPLIT-8 and USE-3 are Musts that the current text does not meet. Each is met by rewriting the text, which is the mildest remedy. Neither is a reason against shipping. Two calls go to the curator:

1. Answer the emscad consistency check. I recommend option (a): the label is per ad, and the analogous exact key changes the score by 0.0006.
2. Decide the `Spatial` tag.

I ran no experiment. No fact is in dispute, and the one open fact (whether a blocked ad can be edited later) cannot be measured without version history. The full report follows.

---

**Recommendation (judgment record)**

```text
Verdict: ship after changes (text only: task_summary and curation_comments; data, cleaning, target and split unchanged).
Validity: SEL-1 holds (content and licence noted, EV-4); SEL-12 holds (LightGBM on structured columns + TF-IDF SVD
reaches 0.987 against 0.994 for TF-IDF LR); USE-5 holds (is_blocked); USE-3 triggered, fixed in text (the prediction
point is the ad's last submitted version, and the price is final); USE-8 triggered, fixed in text (second gap: content
only; cohort in `row`); LEAK-10 triggered, fixed (close_hours, is_proved dropped); LEAK-10 not triggered by `price` on
the evidence; LEAK-19/20/21 hold; SPLIT-8 applied (ForcedIIDFromTemporal), its documentation clause added;
SPLIT-29/25 not triggered: exact-key GroupKFold changes ROC AUC by <= 0.0006 and the label is per ad (source wording,
not measured).
Value: TP probes clean; LightGBM - linear +0.050 (SE 0.001); smallest class per test fold 3,399; AP spreads 0.51-0.95.
Quality: CLEAN-10 code kept with a note (price 999,999,999 and 1); CLEAN-19 over CLEAN-12 for attrs (stated reason).
Weighed: real task +, size +, source (first publication) +, text-heavy -, near ceiling in ROC AUC -.
For the curator: issue 1, the emscad consistency check (SPLIT-29/25); issue 2, the Spatial tag (house rule, a tag).
```

**Changes to make now (no decision needed)**

All files are in `datasets/_dev/tabarena-v0pt2/huntprohibited_1m/`.

1. **SPLIT-8 (Must, P4).** Add one sentence to the IID bullet in `dataset.py`. It says what a date would change: drift in how sellers word ads to avoid blocks, seasonal items (New Year, 8 March) and the category mix. It says the cost cannot be measured because the April labels were never published. It says the time axis should be recovered if Avito or Kaggle releases dates.
2. **USE-8 (Must, P3).**
   - Add the second gap to `fit_reason`: the model sees only the ad's content, not the seller, region, posting time, photos or raw contacts the site has.
   - Add the cohort to `row`: closed ads, blocked for illicit content or never blocked.
   - Fit stays `approximate`.
3. **USE-3 (Must, P3).** Replace "Everything the model sees is known when the ad is submitted" in `fit_reason`. New meaning: known when the ad is submitted, as of its last version; the price is the final price. Make prediction-point bullet 1 say the same.
4. **SPLIT-29 reason (Must, P4).** Rewrite the edited-reposts bullet with:
   - the fact that sets the case apart: the label is per ad, which is the data page's wording and was not checked against a seller key, because none exists (EV-2);
   - the split audit's numbers in place of the earlier "at most 0.002":
     - 1.4-4.9% of test ads have a near copy in train, with 99.5% label agreement;
     - grouping by description (GroupKFold): ROC AUC 0.99384 / 0.99386 against 0.99390 random; AP within 0.002.

   The bullet should also say that a seller who rewrites every ad is not covered by any measurement.
5. **Writing and EV-2: four rewordings, one per claim.**
   - Claim 41: "every ad has a subcategory, and attrs is its category's form (missing for the 2.8% of ads in categories without one)".
   - Claim 40: "loses most of the remaining error and most of the average precision". Support: structured columns alone ROC AUC 0.932, AP 0.51 against 0.95.
   - The "0.50% of the April test ads" figure: mark it as from the 2026-10-07 run. It cannot be re-measured, because avito_test.zip is not in the warehouse.
   - "AP@32500" becomes "AP@k (k = 32,500 per the participants)".
6. **Mask counts (writing).** Say the counts are Avito's own, mostly from the masks in the description: `phones_cnt` exceeds the masks in the description on 0.92% of ads, with no label signal.
7. **CLEAN-10 (Should, P7).** Add one Anomaly line on the price placeholders, kept because sellers typed them at submission and they carry signal:
   - `price` = 999,999,999 is the form maximum: 29 raw ads (14 shipped), 65.5% blocked;
   - `price` = 1: 3,962 ads, 19.0% blocked.
8. **REVIEW.md (procedure).**
   - Remove the stale "Record fields that disagree" block. The record says `Random (IID)` since the curator's 2026-10-19 sync.
   - Close REVIEW_before issue 1 (drop because the source is temporal): SPLIT-8 is a Must that narrows SPLIT-7, so dropping the dataset would break it.
9. **Rebuild the checksum** after the text change (`dataset check`), and add a dated CHANGELOG entry.

**Disputed points, settled**

**D1. How severe is the SPLIT-8 documentation gap?**

- **Advocate (SPLIT-8, the operative clause):** the split is IID and tagged, and the ids are random:
  - itemid AUC 0.4998;
  - block share 0.0681-0.0693 over id deciles;
  - holiday words flat over 20 position bins;
  - next-row label match 0.871837 against 0.871830 by chance;
  - eight shipped definitions carry the same tag.

  On this view only a note is missing.
- **Critic (SPLIT-8, the documentation clause):** the rule says "Say what the timestamp would change and that it should be recovered". The definition says only "cannot be repeated".
- **Settled:** not a conflict. Both sides cite one Must, and its documentation clause is part of it. The clause fails on its own, so the Must is unmet as written. That makes the verdict "ship after changes", not "ship". The fix is to write the sentence, the "fix the definition" rung of the remedy ladder. The advocate is right that the data and the split need no change. The cost cannot be measured because the April labels were never published, so the "measured where the data allows" part is met by saying so.

**D2. Is the USE-3 final-price caveat a Must or a weak leak?**

- **Advocate:** at most a weak leak, so a Should, and note 11 is the remedy. Evidence:
  - price alone ROC AUC 0.740;
  - the counts 0.502-0.512;
  - no outcome-tied missingness;
  - an edit re-enters moderation.
- **Critic:** USE-3 (Must) requires the prediction point to be written accurately. `fit_reason` contradicts note 11 and the data page ("final price of ad").
- **Settled:** these are two separate questions.
  1. **USE-3 (Must, P3): the critic wins.** The headline sentence is inaccurate as worded. The fix is the rewording in change 3.
  2. **LEAK-10 (Must, P4): not triggered on the evidence.** The advocate's "LEAK-10 is a Should here" cites a grading the rule does not have. Only LEAK-30 is graded by strength, and LEAK-11 covers post-outcome values that weaken the signal. The right test is whether the final price exists after the decision the label records. Every edit re-enters moderation. Blocking closes the ad: the cohort is closed ads, and the blocked median of `close_hours` is 0.53 h. So the last version is, as far as the source shows, the version the last decision was made on. That fits a prediction point of "each submission, new or edited".
- **What remains unknown:** whether a blocked ad can still be edited. That needs version history, which the release lacks, so no cheap decisive experiment exists. If it ever turned out true, the bound is price alone 0.740, which is not strong.
- **Remedy:** text only. No `Potential leak, kept on purpose:` marker is required. Adding one would be harmless if the curator prefers caution.

**Issues for the curator (ranked)**

**1. Sellers against the emscad precedent (P4, SPLIT-29 and SPLIT-25, Must; consistency check)**

- **Problem:** emscad was grouped by poster after the same kind of curator concern. Its ROC AUC fell from 0.99 IID to 0.94 grouped (Lennart, 2026-09-30). Here there is no seller id, and under SPLIT-25 maternal_health_risk was retired because its groups could not be recovered.
- **Effect:** if sellers carry the label, the IID score is optimistic by an amount nobody can measure.
- **For option (a):**
  - The label is per ad (data page: ads "blocked for illicit content"). emscad's label was per client (Vidros Sec. 5; 4,439 of 4,441 posters have one label).
  - The key analogous to emscad's identical profile text is an exact description key. It moves ROC AUC by 0.0006 and AP by 0.002 here (split audit), against 0.05 for emscad.
  - SPLIT-25 retires a dataset only "when the real groups matter", and no evidence says they do.
- **Against:**
  - "Per ad" is page wording, not a measurement (EV-2).
  - A seller who rewrites every ad is invisible to every test.
  - The CC itself says to "detect malicious users".
- **What would settle it:** a seller key from Avito; it is not available.
- **Decision needed:** choose one of:
  - (a) record the per-ad label and the exact-key run as the fact that sets the case apart (my recommendation);
  - (b) group on the exact description key, which changes nothing measurable;
  - (c) retire under SPLIT-25;
  - (d) reopen emscad.

**2. The `Spatial` tag (house rule, `data_tags` in definitions.md; not validity)**

- **Problem:** 901,011 ads (22.5%, all real estate) hold a street address inside `attrs`. emscad carries `Spatial` for a free-text location with no coordinates. The definition's stated reason ("no region or coordinates") applies to emscad too, so it does not set this case apart.
- **Effect:** metadata only; no score changes.
- **For leaving it off (advocate's lean):** the address sits inside one category's form string, and the dataset has no geographic column.
- **For adding it:** the tag's definition ("geographic information") and the emscad and perth_house_prices precedents.
- **Decision needed:** choose one of:
  - (a) no tag, with the nested-address reason written down;
  - (b) add `Spatial`;
  - (c) remove emscad's tag;
  - (d) amend the tag to require a geographic column.

**Agreed facts**

- **Raw file:** the zip is 772,619,211 bytes and its sha256 matches. It has 3,995,803 rows, and `itemid` is unique.
- **Rows dropped and kept:**
  - 32,103 exact copies and 212 ads whose features occur with both labels are dropped (0.005% of rows), leaving 3,963,488.
  - 1.5M are sub-sampled, stratified, with 6.865% blocked in every fold; folds are 1M/500k with no overlap.
- **Dropped columns:**
  - `close_hours` is post-decision (host: "not available at scoring phase").
  - `is_proved` is set on 274,996 of 274,996 blocked ads and 0 of 3,720,807 unblocked.
  - `itemid` is random (AUC 0.4998; flat over deciles and position bins).
- **No time index survives:** no date column, and the April labels were never published. The cost of the forced IID split cannot be measured.
- **Leak probe:** the best structured feature is subcategory at 0.908; no missing indicator; NN-distance AUC 0.512; exact copies across the split 0.0%.
- **Text against structured, fold 0:**

  | Model | ROC AUC | AP |
  |---|---|---|
  | Structured columns alone | 0.932 | 0.51 |
  | LightGBM + TF-IDF SVD | 0.987 | 0.89 |
  | TF-IDF LR | 0.994 | 0.95 |

  Task probe: LightGBM 0.970, RF 0.970, linear 0.945; no flags.
- **Near copies:** 1.4-4.9% of test ads have a near copy by exact key, with 99.5% label agreement. Exact-key grouping changes ROC AUC by <= 0.0006.
- **`attrs` and price:**
  - `attrs` is missing for 2.76% of ads, structurally (9 subcategories have no form).
  - Price: 0 on 12.4% of ads, 1 on 3,962, 999,999,999 on 29 raw ads; the data page calls it the final price.
- **Real estate:** 1,149,136 ads, 0.12% blocked; moderation covers every ad.
- **Fit:** approximate (the practitioner agrees). It would be used as a queue ranker.
- **Blind reviewer:**
  - Its size concern is answered by `version_comment`, which it did not see.
  - Its "keep `itemid`" is refuted by the id tests.
  - Its "price 0 as missing" would merge "free" into missing; the notes cover this.
- **Text scope:** not grounds to exclude (SEL-12 not triggered). Neither side asks for exclusion, a re-split or a column change.

**Consistency with precedent**

- **Followed:**
  - forced IID: account_debt_south_africa, aps_failure, food_delivery_time, labour_inspection_compliance and others;
  - text kept: mercari_price_suggestion, emscad, consumer_complaints;
  - `is_proved` dropped and the target kept: kickstarter, corporate_credit_rating (USE-5);
  - real estate kept: LEAK-22, consumer_complaints_1m;
  - deduplication: wine_quality, jm1, emscad (LEAK-19/20/21);
  - licence noted: lucas_topsoil (EV-4).
- **Departures with a distinguishing fact:**
  - `attrs` kept as text, against kickstarter's decoding. The fact: a sparse 79-key form, which the winners treated as text (CLEAN-19, discussion 10178).
  - Price codes kept, against sdss_17's -9999 made missing. The fact: the seller typed them, and they carry signal (CLEAN-10, "keep a code and say why"). This departure is resolved once change 7 is written.
- **Departures that go to the curator:**
  - emscad sellers (issue 1). The distinguishing fact is offered, but it rests partly on page wording.
  - emscad `Spatial` (issue 2).
- **Drift and exceptions:** no drift and no third exception. SPLIT-8's parenthetical example ("one extract") is narrower than how it is applied to event logs with dates removed. A wording example could be added on the next pass; no amendment is due.

**Notes outside the decision**

- **`attrs` and pandas:** the column name shadows `pandas.DataFrame.attrs` (column auditor). Renaming it would be cosmetic, and it is not part of the agreed changes.
- **Probe gap:** the near-copy check in `hidden_groups.py` skips long text, so its "0.0%" here is a probe gap, not evidence (EV-3). This is a tooling note.

**Files**

- Definition: datasets/_dev/tabarena-v0pt2/huntprohibited_1m/dataset.py
- Record: curation/records/huntprohibited.md
- Rules: .claude/skills/knowledge-curation/references/splits.md (SPLIT-8, -25, -29), use_case.md (USE-3, USE-8), leak_checks.md (LEAK-10, -11, -30)

</details>

<details><summary>Claim audit</summary>

Claim numbers are those of the panel's claim list. Frame and splits loaded through `dataset_io.from_definition`,
fold 0 = 1M train / 500k test. Source quotes checked against the Kaggle pages and discussions saved in the 2026-10-07
run. Licence
(15, 43) is not evidence (EV-4) and is not tested.

| # | Claim (short) | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1, 5, 19, 25 | target = moderator blocked the ad for illicit content | D task_summary, notes | data page text | holds | "is_blocked - Boolean target variable"; ads "blocked for illicit content or ... never been blocked" | USE-5 |
| 2 | Avito scores ads at submission to route moderation | D use_case | none possible from the files | untested | inference; no source page says how Avito uses the score | USE-1 |
| 3, 22, 37 | closed ads, Dec 2013 to Mar 2014 | D row, notes, bullet 11 | data page | holds | "sampled from Dec 2013 - Mar 2014"; "All ads ... have already been closed" | PROV-1 |
| 4, 13, 62 | 1.5M of 3,963,488 after 32,315 dropped; stratified; 3 folds 1M/500k | D row, version_comment, R | rebuild frame and splits | holds | 1,500,000 rows; blocked 6.865% overall and 6.865% in each test fold; folds 1M/500k, no index overlap; 32,103 + 212 = 32,315 | SPLIT-1 |
| 6, 32, 58 | counts are the phones / e-mails / URLs masked in the description | D known, bullet 8, R CC | count `@@PHONE@@` etc. per description vs the count columns | holds with a gap | e-mails 99.9998% and URLs 99.998% match; phones only 99.08%: 36,807 ads (0.92%) have `phones_cnt` above the masks in the description (always above; title masks explain 0.05 pp); their block rate 5.1% (below base), so no label signal | LEAK-1 |
| 7, 12, 29 | file has no date; competition tested on the next month | D split, fit_reason, bullet 5 | data page; columns | holds | no date column; "Ads for testing has been sampled from Apr 2014" | SPLIT-4 |
| 8, 26, 50, 57, 63 | close_hours post-outcome, modulo 24 h | D changes, bullet 2, decision 1, R | distribution, AUC; host quote | holds | max 24.0 (0.06% at 24.0, rounding), median 3.9 h; AUC of -close_hours 0.641; host: "not available at scoring phase", `.seconds` "24 hour cap" (9729) | LEAK-10 |
| 9, 30, 53 | exact copies and both-label vectors dropped | D changes, bullet 6, decision 3 | code + rebuilt frame | holds | fold-0 test rows with an exact feature copy in train: 0.0% | LEAK-16 |
| 10, 11 | fit approximate; everything the model sees is known at submission | D fit, fit_reason | data page | untested (partly against) | the row is the ad at close: "price - final price of ad", so an edited ad shows its last version, not the version scored; whether title/description/attrs are also final cannot be measured from the file | USE-3, LEAK-1 |
| 14, 18 | year, domain, source, URL, bibtex | D | page | holds | competition page of Avito, 2014 | PROV-1 |
| 16 | ForcedIIDFromTemporal | D | see 7, 52 | holds | | SPLIT-4 |
| 17 | zip size and sha256 | D download_description | raw-file measurements (this run) | holds | 772,619,211 bytes, sha256 aa5472aa...a23b | PROV-13 |
| 20 | 3,995,803 rows | D comment | read zip | holds | 3,995,803 | PROV-13 |
| 21 | feature types | D `_feature_types` | rebuilt frame dtypes | holds | category/subcategory categorical, 3 string, 4 int | CLEAN |
| 23 | April test file not used | D notes | code | holds | `_load_raw` reads only avito_train.zip | |
| 24 | prediction point: ad submitted (new or edited) | D bullet 1 | none possible | untested | no source states it; see 10-11 for the final-version caveat | USE-3 |
| 27, 51, 56 | is_proved set only for blocked ads; data page "not to be used as a direct modeling attribute" | D bullet 3, decision 1, R CC | counts by label; page | holds | set on 274,996 of 274,996 blocked, 0 of 3,720,807 not blocked; quote verbatim on the data page | LEAK-10 |
| 28, 52, 61 | itemid random; flat over deciles | D bullet 4, decision 2, R | AUC of itemid; decile table | holds | itemid AUC 0.4998; block share 0.0681-0.0693 over deciles | SPLIT-4 |
| 31, 64 | 1.39% of fold-0 test ads share a 30+ char description with train; dropping them changes ROC AUC by at most 0.002 | D bullet 7, R | measure on fold 0; AUC with and without those ads | holds | 1.389% (6,943 ads, 10.1% blocked, 99.4% agree with the train label); TF-IDF LR 0.99474 -> 0.99465, structured LightGBM 0.93242 -> 0.93208 | LEAK-16, SPLIT-29 |
| 31, 64 (April) | 0.50% of April test ads share such a description | D bullet 7, R | needs avito_test.zip (not in the warehouse) | untested | earlier run's number, not re-measured | SPLIT-29 |
| 33 | unpacking gives 72 mostly empty columns; winners treated attrs as text | D bullet 9 | parse JSON keys; discussion 10178 | holds | 79 keys, 72 on >= 1,000 ads; 10178: "for the attributes feature, anything more fancy than running it through a tfidf added nothing" | CLEAN |
| 34 | 6,004 attrs not valid JSON | D bullet 10 | json.loads | holds | 6,004 | CLEAN |
| 35 | "^p" line breaks | D bullet 10 | raw-file measurements | holds | 36.5% of descriptions | CLEAN |
| 36 | price 0 for 12.4% | D bullet 10 | count | holds | 12.41%; undocumented: 1,411 ads at price >= 1e8 (10.1% blocked), 29 at 999,999,999 (65.5% blocked) | CLEAN |
| 38 | price is the final price | D bullet 11 | data page | holds | "final price of ad in Russian rubles" | LEAK-1 |
| 39, 65 | fold 0: structured LightGBM 0.932, TF-IDF LR 0.994 | D bullet 12, R | refit on fold 0 | holds | 0.9324 and 0.9947 (without real estate 0.9929) | TP-10 |
| 40 | a poor Russian-text pipeline "loses most of the task" | D bullet 12 | from 39 | holds on error, overstated on the metric | 1 - AUC grows from 0.005 to 0.068 (x13), but structured columns alone keep ROC AUC 0.932; AP 0.95 vs 0.51 (REVIEW_before) | TP-10 |
| 41 | hidden-group hits subcategory and attrs; "every new ad has both" | D bullet 13 | probe stdout; attrs missingness | refuted (wording) | hits confirmed (gaps 0.816, 0.250); but attrs is missing for 2.76% of ads (10.1% of blocked, 2.2% of unblocked; missing-indicator AUC 0.540). The conclusion (an attribute, not an entity) still holds | SPLIT-9, writing |
| 42 | competition scored AP@32500 | D bullet 14 | evaluation page; discussions | holds (third-party K) | the evaluation page gives AP@K without K; 32500 appears only in a participant's thread title (9600) | EV-2 |
| 44 | content warning | D bullet 14 | rules page | holds | "illicit, illegal, immoral, ... offensive, or obscene material" | SEL-1 |
| 45 | no splits_comment; IID; subsample_to_budget | D | code, README | holds | | SPLIT-1 |
| 46, 47 | real estate and children's clothes almost never blocked; 0.12% of 1,149,136 | D accepted warning | counts | holds | 0.124% of 1,149,136; children's clothes 0.053% of 144,076 | EV-5 |
| 48 | seller picks the category at posting | D accepted warning | none possible | untested | plausible; not documented by the source | LEAK-1 |
| 49 | winners left real estate out of training (10178) | D accepted warning | discussion 10178 | holds | "built on the entire data minus real estate" | |
| 54, 55 | text-to-features script; JSON attrs | R CC | earlier run folder | holds | `avito_ProhibitedContent_SampleCode.py`; attrs JSON | |
| 59 | malicious users should be detected instead of ads | R CC | no seller id in the file | untested | cannot group by seller; description copies bound the effect (31) | SPLIT-3 |
| 60 | needs basic preprocessing; non-English language | R comment | | holds | Russian text, masks, "^p" | |
| 66 | priority 3, "no known risk" | R assessment | | untested (judgment) | the same assessment names the lost temporal split and text dominance | |
| 67 | record front matter | R | compare with D | holds | required_split Random (IID) now matches the definition | |

**Implied claims**

| Implied claim | Test | Result | Evidence | Rule |
|---|---|---|---|---|
| No row is a copy across the split | exact features; title+description; 30+ char description on fold 0 | holds (bounded) | 0.0%; 0.26%; 1.39%, worth <= 0.0003 ROC AUC | LEAK-16 |
| Every feature is known at the prediction point | page; missingness by label | untested | the row is the ad at close (final price, possibly final text); description missing AUC 0.504, attrs missing 0.540 (form-dependent, known at posting) | LEAK-1, USE-3 |
| The split is the one the use case needs | | refuted by the definition itself (stated) | the use case scores next ads; split is random over four months; no date exists, so no remedy beyond the tag | SPLIT-4 |
| The target is the real-world target | page | holds | moderator's block decision; is_proved alternative noted in REVIEW | USE-5 |
| The cleaning uses no label across rows | code | holds with a trace | the 212 both-label ads are dropped using labels of all rows (transductive, 0.005% of rows; negligible) | LEAK-30 |

**Ranked**

Refuted:
1. Claim 41 (writing, P4 context): "every new ad has both" subcategory and attrs; attrs is missing on 2.76% of ads (10.1% of blocked). Changes nothing in the split decision. Remedy: reword to "every ad has a subcategory, and attrs is the form of its category (missing for 2.8%)".
2. Claims 6/32/58 partly (P7): phones_cnt exceeds the masks in the description on 0.92% of ads; no label signal. Remedy: say "counted by Avito, mostly the masks in the description".
3. Claim 40 (P6 wording): overstated in ROC AUC (structured alone 0.932). Remedy: say "loses most of the remaining error / most of the AP".
4. Undocumented (P7): price >= 1e8 on 1,411 ads, 999,999,999 on 29 (65.5% blocked). Remedy: one note line.

Untested (ranked): 10/11/24 final-version features vs the scoring point (P4, cannot be measured; the source says price is final); April 0.50% copy share (needs avito_test.zip); 2 and 48 (use-case inferences); 59 sellers; 66 judgment.

</details>

<details><summary>Column audit</summary>

Frame: the definition rebuilt through `dataset_io.load(..., built=True)` (origin `rebuilt`), 1,500,000 rows x 10
columns; masked-token and missingness breakdowns on the clean-room sample (200,000 rows). Meanings from the Kaggle data page as quoted in the
definition and REVIEW.md (not re-fetched). Prediction point (bullet 1): the ad as submitted (new or edited) when it
enters moderation.

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `category` | top-level category the seller picked (10 levels) | yes, chosen at posting | categorical, 0 missing | fine | CLEAN-14 |
| `subcategory` | subcategory the seller picked (53 levels, nested in category) | yes | categorical, 0 missing; alone ROC AUC 0.908 (leak probe), a category effect (accepted `dataset_pure_feature_value`) | fine | CLEAN-14, LEAK-10 (not met) |
| `title` | ad title, Russian free text | yes | string; 739,086 distinct; a handful missing (kept as missing) | fine | CLEAN-14 |
| `description` | ad body, Russian free text; contacts replaced by `@@PHONE@@`, `@@EMAIL@@`, `@@URL@@`; line breaks written `^p` (36.7%) | yes (as posted; for an edited ad the last version) | string; 1.41% missing (blocked 10.9% vs 6.8%), spread over all categories, no category where missing means blocked; `^p` kept and documented | fine (note: `^p` could become `\n`, optional) | CLEAN-14, CLEAN-12 (optional) |
| `attrs` | the category's form fields as JSON text (79 keys) | yes | string; 2.77% missing, blocked 25.1% vs 6.3%. Missingness is structural, not outcome-caused: it is missing for every ad of 9 subcategories without a form (Охота и рыбалка 79.6% blocked, Продукты питания 48.6%, Ноутбуки 0.8%, ...) and set for every ad of the others (3 exceptions in 200k). Alone 0.945 as text: the subcategory signal plus form values. 6,004 malformed JSON kept (documented). The name shadows `pandas.DataFrame.attrs` (`df.attrs` returns the metadata dict, not the column) | fine; question kept (unpack or text, REVIEW_before 3) | LEAK-10 (missingness, not met), CLEAN-14 |
| `price` | price the seller entered, in rubles; the final value of an edited ad | yes at submission; the final-price caveat (note 11) cannot be checked | int64; 0 for 12.43% (blocked 17.9% vs 5.3%), meaning "no price" or "free", mostly in services/jobs/animals; `1` on 3,962 ads (19.0% blocked) and 999,999,999 (the 9-digit form maximum) on 14 shipped ads (29 raw), 64.3% blocked (titles offer people, organs, guns): seller-entered placeholders, not measurement errors; >= 1e8 on 500 ads, 89% real estate (plausible) | cleaning: document the placeholders; keep the values (they are what the moderator saw) | CLEAN-10, CLEAN-11, writing |
| `phones_cnt` | number of phone numbers Avito masked in the ad | yes, if masking runs at submission (not documented) | int64, 0-215; equals the `@@PHONE@@` count in the description for 99.08%, larger for 0.92% (counts also from the title or before truncation; mismatches 5.6% blocked, below the base rate) | fine | CLEAN-14 |
| `emails_cnt` | number of e-mails masked | as above | int64, 0-5; equals the token count for 99.9995% | fine | CLEAN-14 |
| `urls_cnt` | number of URLs masked | as above | int64, 0-31; equals the token count for 99.996% | fine | CLEAN-14 |
| `is_blocked` (target) | moderator blocked the ad for illicit content | the outcome | categorical Yes/No, 6.86% Yes, no missing | fine | CLEAN-15 |
| dropped `close_hours` | hours the ad stayed live | no, after the decision | dropped | correct | LEAK-10 |
| dropped `is_proved` | blocked by an experienced moderator; set only for blocked ads | no, part of the target | dropped | correct | LEAK-10 |
| dropped `itemid` | random id (discussion 9554); flat over deciles (decision 2) | n/a | dropped | correct | CLEAN-3 |

No column is built from labels or all-row statistics (CLEAN-6, CLEAN-7, LEAK-27 to LEAK-31 not met). No untyped
object column (CLEAN-9). No constant or copied column (CLEAN-5); `category` is a function of `subcategory` but a coarser
level, not a copy.

**Problems, ranked**

1. **P4, LEAK-10 (question, weak): `price` and the masked counts may hold the last version of an edited ad.** Note 11
   already says the price is the final price. Whether a blocked ad could be edited afterwards, or whether Avito masked
   contacts before moderation, is not in the source. Evidence that it is not a leak: price alone 0.740 and the counts
   0.502-0.512 (leak probe); no missingness tied to the outcome. Mildest remedy: none beyond the existing note.
2. **P7, CLEAN-10 / CLEAN-11 and writing (cleaning, minor): undocumented price placeholders.** 999,999,999 on 29 raw
   ads (65.5% blocked; 14 shipped, 64.3%) and `1` on 3,962 shipped ads (19.0%) are entered values, not impossible
   measurements: the moderator saw them, and they carry the signal of the illicit offer, so turning them into missing
   would remove information known at submission. `0` (12.4%) mixes "no price" and "free" and cannot be split
   (documented). Remedy: add to the anomaly bullet that 999,999,999 is the form's maximum, typed by 29 sellers (65.5%
   blocked), and that 0 and 1 are placeholders; keep the values.
3. **P7, CLEAN-12 (optional): `^p` line breaks.** Documented and kept; replacing `^p` with `\n` is a cheap, safe
   restoration but changes nothing for a TF-IDF or embedding pipeline. Remedy: none required.
4. **Note (no rule): the column name `attrs` shadows `pandas.DataFrame.attrs`.** `df.attrs` returns the metadata dict;
   only `df["attrs"]` reaches the column (it broke two of my scripts). Remedy, optional: rename to `form_fields` and
   say so in the notes.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** The use case (Avito scores each ad when it is submitted) is a stream over time, so the
regime the application implies is temporal (SPLIT-1, SPLIT-7). The release has no time index left, so IID tagged
`ForcedIIDFromTemporal` is the rule's own answer (SPLIT-8; precedent account_debt_south_africa). Hidden groups and
near copies do not move the score: a split grouped by normalised description scores the same as the shipped random
split (ROC AUC 0.9939 against 0.9939).

Data: loaded through `dataset_io.load(..., built=True)`; origin `rebuilt` (the README has no build path), 1,500,000
rows, 3 folds of 1,000,000 / 500,000, blocked 102,974 (6.86%). Threads capped at 2.

**Regime (SPLIT-1, SPLIT-3, SPLIT-7, SPLIT-8, USE-10)**

- What one prediction is: one new or edited ad at submission, scored from its content as posted (prediction point,
  bullet 1). The entity is the ad, and every ad is new, so this is not a cold-start grouped task (USE-10). Sellers
  recur, but the file has no seller id (see below).
- Time: the training ads date from Dec 2013 to Mar 2014 and the competition tested on April 2014. No column carries a
  date. Measured in this run: the raw file is sorted by `itemid` (monotonic, so file order = id order and gives no
  separate time proxy, SPLIT-22). Over 20 position bins the block share is 0.0679-0.0697, the real-estate share
  0.286-0.289, "новый год/новогод" 0.0065-0.0072, "8 марта" 0.00097-0.00122 and "2014" 0.0153-0.0164. All flat: the
  Jan-to-March holiday words would rise or fall if the order were time. Next-row label match is 0.871837 against
  0.871830 by chance. The ids are random, as the host says (discussion 9554). The temporal split cannot be rebuilt.
- So SPLIT-8 applies and is applied: IID, tag `ForcedIIDFromTemporal`, fit `approximate` with the gap named. SPLIT-8
  also asks that the cost be measured "where the data allows". The April labels were never published, so the only
  out-of-time evidence is the copy rate: 1.39% of the shipped test ads share a raw 30+ character description with
  train, against 0.50% of the April ads (definition note, earlier run). Drift in the block rate or in the categories
  cannot be measured.
- Gap and late labels (SPLIT-9, SPLIT-10): do not apply to an IID split. The label comes from moderation within hours
  (the blocked median of `close_hours` is 0.53 h), and `close_hours` is dropped. The cohort is closed ads only, which
  is a target-population note (record issue), not a split one.
- Season (SPLIT-20): the four months include New Year and 8 March. With no dates, the test window cannot be checked
  for an atypical season. This is a cost of the forced IID split and is covered by the tag.

**Grouping and hidden groups (SPLIT-4, SPLIT-24, SPLIT-29, SPLIT-30)**

- Probe hits on `subcategory` (gap +0.816) and `attrs` (gap +0.250): both are features every new ad has (SPLIT-4,
  reading 4 of the hidden-group table in evidence.md). No re-split. `title` gap +0.011; composite key (all but
  description) gap +0.004. Agree with the definition.
- The near-copy part of the probe did not run: "1500000 rows with fewer than 10 tokens left single". The probe tokenises
  only short columns, so the long descriptions never entered it. I measured near copies with exact constructed keys
  instead (SPLIT-24 allows exact keys, not similarity clusters):

  | key | rows sharing a key | test ads with a copy in train (folds 0/1/2) | blocked share of those | label agrees with train |
  |---|---|---|---|---|
  | raw description, 30+ chars | 1.82% | 1.39 / 1.41 / 1.40% | 10.1-10.4% | 0.994-0.995 |
  | description, letters only, 30+ chars | 3.71% | 2.94 / 3.01 / 2.96% | 6.7-7.0% | 0.995 |
  | first 100 letters of description (60+ chars) | 5.83% | 4.76 / 4.88 / 4.80% | 6.7-7.2% | 0.995-0.996 |
  | title + normalised description | 2.41% | 1.94 / 1.98 / 1.96% | 2.1-2.2% | 0.999-1.000 |

- Alternative split, run because sellers and edited reposts are the record's concern (CC: "malicious users"): a
  hashed 1-2-gram logistic regression over category, subcategory, title, description and attrs (2^21 features,
  liblinear, C=4):

  | split | ROC AUC | AP |
  |---|---|---|
  | shipped random, fold 0 | 0.99390 | 0.9443 |
  | same, without the 4.76% of test ads with a near copy in train | 0.99356 | 0.9424 |
  | grouped by first-100-letters key (GroupKFold, fold 0) | 0.99384 | 0.9422 |
  | grouped by letters-only description key (GroupKFold, fold 0) | 0.99386 | 0.9446 |

  The differences are at most 0.0006 ROC AUC and 0.002 AP. Reposts are rare and are labelled like the original, but
  even a model built on text n-grams gains nothing from them. A real seller id could matter more (a seller who rewrites
  each ad), but it is not in the file and cannot be recovered. SPLIT-25 retires a dataset only "when the real groups
  matter", and the evidence says they do not matter here. The definition's 0.002 bound is now re-measured and holds.

**Problems, ranked (all P4, none blocking)**

1. **SPLIT-8 (Must), applied; a note on its second half.** The forced IID split is right, but it carries the
   unmeasured cost of time drift: the competition's April test is lost and its labels were never published. The
   definition says the monthly split "cannot be repeated". It should also say what a date would change (the
   holiday-season ads, drift in the categories and in how spammers write) and that the time axis should be recovered if
   Avito or Kaggle ever releases the dates. Mildest remedy: a sentence in `curation_comments` / `splits_comment`. No
   re-split possible.
2. **SPLIT-29/30 and LEAK-16 to LEAK-21 (copies), closed with a measurement.** The near-copy probe's "0.0%" is a probe
   gap, not evidence (EV-3). By exact keys, 1.4-4.9% of the test ads have a near copy in train, with 99.5% label
   agreement. Grouping by description changes ROC AUC by under 0.001. Remedy: none. Optionally, replace the note's
   "earlier run" bound with these numbers. A tooling note for the curator: `hidden_groups.py` leaves long-text rows out
   of the near-copy check.
3. **Record consistency (procedure).** REVIEW.md's "Record fields that disagree" still says the record holds
   `Temporal (NON-IID), ?`, but the record now says `required_split: Random (IID)`. That list is stale. Remedy: the
   editor updates REVIEW.md. This is not a split problem.

Judgment record: Validity: SPLIT-1 holds (as far as the release allows); SPLIT-7 triggered, settled by SPLIT-8 (forced
IID, tagged); SPLIT-4 settles the `subcategory`/`attrs` hits; SPLIT-24/25 no group id, and the grouped alternative
changes nothing (0.0006 AUC); SPLIT-9/10 n/a.

</details>

<details><summary>Domain practitioner</summary>

Actor: I run the trust-and-safety (moderation) team at Avito in 2014. Every new or edited ad enters a pre-moderation
queue; my moderators can check only so many ads a day, so an automatic score orders the queue (and, at the top,
could auto-block). The competition's metric, AP@32500, is exactly that: precision over the top of a daily queue.

**Fit: approximate (agree with the definition)**

Every input is known when the ad is submitted and the label is the moderator decision my score automates, but the
test ads are random ads of the same four months rather than next month's ads, and the model sees only the ad's content,
not the seller, place, time or photos that my system always has (USE-8; USE-9 gives no direct rephrasing, since a
content-only screen of a random sample of the same months is not a decision anyone makes, see the weighed factor
"a use case rephrased only to excuse a gap").

**1. Inputs at the prediction point (USE-3, USE-6)**

Have, and in the data: title, description, attrs (the category form), category, subcategory, price, counts of masked
phones/e-mails/URLs. All exist at submission. `close_hours` (post-decision, hosts: "not available at scoring phase")
and `is_proved` (set only for blocked ads) are rightly dropped (USE-3, LEAK-10). `itemid` is random, rightly dropped.

Small caveat: `price` is the final price, so an edited ad may carry a later version than the one scored (curation
bullet 11). The edit itself re-enters moderation, so this is a row-version blur, not a leak worth acting on.

Missing that I would always have (cannot be added; the source withheld them):
- the seller: account id, account age, earlier blocks, other live ads (the CC comment: "detect malicious users");
- where and when: region/city, posting time and day;
- the photos;
- the raw phone/e-mail/URL (masked to counts; in production a phone seen on blocked ads is a strong signal).
These make the task a content-only screen. It is a real component of the moderation stack (a text classifier on the
ad), but it is weaker than the decision I make and the task summary's `known` and `fit_reason` do not say so.

**2. Target (USE-5)**

`is_blocked` = a moderator blocked the ad for illicit content. That is what I act on: the score replaces or orders a
moderator's decision. It is a proxy for "the ad truly violates the rules": 191,186 of 274,996 blocks were not
confirmed by an experienced moderator (`is_proved`), so positives carry some moderator noise; keeping the source's
target is right, since that is the decision I automate. Output I want: a ranking score (probability), cut at queue
capacity. ROC AUC is acceptable as a ranking metric; at my operating point top-k precision matters more, and AUC
here is lifted by 1.15M real-estate ads that are almost never blocked (0.12%). Those easy negatives are real ads my
queue also sees (moderation covers every ad), so keeping them is correct for the use case.

Cohort: the source keeps closed ads that were blocked for illicit content or never blocked (curation bullet 11). Ads
blocked for other reasons (duplicates, wrong category, other rule breaks) and ads still live are not in the file. My
live queue holds those too, so the population is a filtered version of what I face; this is a small gap, likely
inherited from the hosts, and worth one clause in `row`.

**3. Row and test data (USE-1, USE-10, SPLIT)**

One row = one ad = one moderation decision: matches. Test data: random ads from Dec 2013 to Mar 2014; I would face
next month's ads. Prohibited content is adversarial: sellers learn which words get them blocked and obfuscate
(misspellings, Latin look-alikes, numbers in words), and seasonal items move (New Year fireworks, 8 March). A random
split overstates how well a model trained in March works in April. The split cannot be built (no date, random ids,
checked flat), so ForcedIIDFromTemporal is the honest label. The seller is often a known entity (USE-10), but without
a seller id the model can only be a cold-start-per-ad model; the edited reposts across the split are bounded at 0.002
ROC AUC, so this does not change the task much.

**4. Would I use it?**

Yes, as one component: a text-based queue ranker. I would trust it if it holds precision at the queue cut-off on the
next month and per category (services, hobby, business, where 19-39% are blocked). I would distrust a 0.99 ROC AUC that
comes partly from real estate and from a random split of the same months, and a model that never saw who posted.

**Gaps, ranked by how much they change the task**

1. Random split over the same four months instead of next month (adversarial drift); cannot be fixed, tagged
   ForcedIIDFromTemporal (USE-8, SPLIT-3).
2. Content only: no seller identity or history, region, time, photos or raw contacts, which the actor always has; the
   task is a content screen, not the full moderation decision (USE-1, USE-6). Not stated in `known` / `fit_reason`.
3. Cohort filtered by the source: closed ads, blocked for illicit content or never blocked (USE-5, row population).
4. Metric: ROC AUC over a population with many trivially negative ads, where the decision is top-k precision; not a
   use-case rule breach, a note for interpreting scores.
5. Label noise from unconfirmed blocks (USE-5); keep `is_blocked`.
6. `price` as the final version of an edited ad (USE-3); negligible.

**What an expert would change**

- In `task_summary.fit_reason` (or `known`), name the second gap: "the model sees only the ad's content, not the
  seller, region, time or photos that the site has". The fit stays approximate.
- In `row`, say the cohort: closed ads blocked for illicit content or never blocked.
- Keep `is_blocked`, keep real estate, keep the IID split with ForcedIIDFromTemporal; no other edit.
- If the benchmark allows a secondary metric, average precision is closer to the queue decision than ROC AUC.

**Sources**

- dataset.py, README.md, REVIEW.md of datasets/_dev/tabarena-v0pt2/huntprohibited_1m/; curation/records/huntprohibited.md
- the panel's claim list, the raw-file measurements (block rate by category), REVIEW_before (is_proved counts)
- Kaggle competition page https://www.kaggle.com/competitions/avito-prohibited-content (did not render via fetch;
  quotes taken from the definition: discussions 9554, 9729, 10178, data page, AP@32500)
- .claude/skills/knowledge-curation/references/use_case.md (USE-1, 3, 5, 6, 8, 9, 10)
- Web searches on Avito moderation returned nothing usable; the domain view (pre-moderation queue, adversarial text
  drift, seller signals) is practitioner knowledge of classifieds trust-and-safety, not a cited source.

</details>

<details><summary>Blind review</summary>

**Verdict**
Include with changes. It is a real moderation task: Avito decides at posting time whether to block a classified ad. But it is mostly a text-classification task, it sits close to the ceiling, and the stated 1.5M size cannot be reconciled with the source.

**Task and use**
Avito, a Russian classifieds site, runs a moderation queue. When an ad is posted, a model scores it, and blocked-looking ads are routed to human moderators or blocked outright. This is a real use. The prediction is made at posting time, and every remaining column (category, subcategory, title, description, attrs, price, and the phone/email/url counts) exists at that moment. The original competition file also had `is_proved` (a moderator verified the decision) and `close_hours` (how long the ad stayed open). Both are post-hoc and would leak. Both are absent here, which is good.

**Concerns, most serious first**
1. **Mostly a text task, and near the ceiling.** I ran 3-fold CV on a 200k-row sample.
   - Subcategory alone: AUC 0.909.
   - Categoricals, price, the counts and text lengths with LightGBM: AUC 0.960.
   - TF-IDF on title+description with logistic regression: AUC 0.987.

   Blocking rates by category range from 0.2% (Real estate) to 38.7% (Services). Most of the remaining signal is in Russian free text. A tabular method with no text handling is mainly tested on how it drops or encodes strings.

   *Change:* include only in a track that supports text. Otherwise exclude, or fix the text featurization for all methods. Score with AUC or AP; accuracy is not useful at a 6.9% positive rate.
2. **The split does not match deployment.** The data are ads drawn from a period of time, and moderation rules and spam tactics drift. The competition test set was a different set of ads, and I recall it covered a later period. A random IID split is optimistic. No time or item-id column is kept, so a temporal split cannot be rebuilt. *Change:* keep `itemid` or a date if one is available and split on it. Otherwise document the IID optimism.
3. **The size claim cannot be explained.** task.md gives 1.5M rows. From memory, the Kaggle avito_train.tsv has about 3.9M rows, and I could not open the page to confirm. If the 1.5M rows are a subsample, say how they were drawn (random or stratified, and from which period). Otherwise the base rate may be distorted.
4. **Preparation details.**
   - `attrs` is a pseudo-JSON string with duplicated keys, for example "Этаж" (floor) twice, once as a number and once as a range. As stored it is an unusable high-cardinality string (70,940 unique values in the 200k sample). Either parse it into features or drop it.
   - Price is 0 for 12.5% of rows (a placeholder for "not given") and reaches 1e9. Encode 0 as missing.
   - The target is stored as a Yes/No category. That is fine.
   - Duplicates: 69 rows share an identical title and description, and none of them have conflicting labels. This is negligible.
5. **Labels are imperfect.** `is_blocked` is a moderator decision, not ground truth. The competition shipped `is_proved` to mark which decisions were verified. Dropping it is correct, but some labels are noisy.

**What I could not check**
- The Kaggle data page did not render.
- From memory only, not confirmed: the column definitions, the train/test time periods, the original row count, and the evaluation metric (AP@k).
- Whether the 1.5M rows are random.
- I did not tune any model; all scores are from the 200k sample.

</details>

<details><summary>Precedent check</summary>

Inputs: REVIEW_before (issues 1-9), the verification checklist, `dataset.py`, `curation/records/huntprohibited.md`, the
register of decisions (huntprohibited appears only as AI open issues and AI assessments, no `CC` line of
the curator on any of them), the Cases tables of `selection.md`, `splits.md`, `leak_checks.md`,
`cleaning_features.md`, `definitions.md`, and the sibling records and definitions named below. None of the register's
four flags (few_minority, one_feature, scaling over all rows, trivial) touches this dataset.

Summary: the definition follows its precedents on 8 of 11 points. One precedent pair needs a reflection prompt
(issue 4 against emscad), one small departure has no reason written down (the `price` value 999,999,999). One part of
the open issues is already out of date: the record no longer disagrees with the definition. No drift and no third
exception found.

**Stale part of REVIEW_before.md**

The "Record fields that disagree" block and issue 1 ("The record says `required_split: Temporal (NON-IID), ?`")
describe the record before commit 58ee235. The record now reads `required_split: Random (IID)`, and the
`Non-IID (Temporal)` tag is gone. The change came from the curator's bulk alignment of 2026-10-19: "Records
(Lennart, 2026-10-19): `required_split` set to the definition's regime in the 34 records that disagreed"
(`datasets/_dev/tabarena-v0pt2/CHANGELOG.md`, line 111). The field rows should be removed from REVIEW.md. That
bulk alignment synced fields and did not decide whether forced IID should ship, so the question in issue 1 itself
stays open (see 1 below).

**Per decision**

| # | Decision (definition / open issue) | Rule | Verdict | Closest precedents |
|---|---|---|---|---|
| 1 | IID, tagged `ForcedIIDFromTemporal`, because no date survives | SPLIT-7, SPLIT-8 (Must) | consistent | account_debt_south_africa (SPLIT-8 case, Lennart 2026-10-12); food_delivery_time, aps_failure, labour_inspection_compliance, taiwanese_bankruptcy_prediction, home_credit_default_risk, phiusil_phishing (all the same tag for a release without dates); emscad (Lennart 2026-10-14: no tag only because its split is grouped) |
| 2 | Text kept as string columns; SEL-12 not triggered | SEL-12 (Must) | consistent | mercari_price_suggestion (kept, Lennart 2026-10-06: R^2 0.06 without its text, 0.670 with it); emscad (fraud moderation of job ads, text, kept, grouped 2026-09-30); consumer_complaints (narrative kept, 2026-10-01/06) |
| 3 | `attrs` kept as one JSON string | CLEAN-12, CLEAN-14, CLEAN-19 (Should) | departs from kickstarter's decoding, with a stated reason | kickstarter (decodes `category` and `location` JSON into columns) |
| 4 | Sellers not grouped; edited reposts kept | LEAK-17, SPLIT-24, SPLIT-25, SPLIT-29 (Must) | **departs from emscad; one reason written down (no seller key), the reason that sets it apart is not** | emscad (Lennart 2026-09-30: grouped by poster, ROC AUC 0.99 IID -> 0.94 grouped); maternal_health_risk (SPLIT-25: retired when the real groups cannot be recovered) |
| 5 | Hidden-group hits on `subcategory`, `attrs` dismissed | SPLIT-4, SPLIT-30 | consistent | superconductivity / SPLIT-4 text ("a soil type or a fund category is known for every new row"); kick (SPLIT-5) |
| 6 | Target `is_blocked`, `is_proved` dropped | USE-5, LEAK-10 | consistent | kickstarter (`staff_pick` dropped as post-launch); corporate_credit_rating (USE-5: the target the actor acts on) |
| 7 | Real estate kept (0.12% blocked) | LEAK-22, USE-1 | consistent | LEAK-22 "follow the paper's cohort" (diabetes_130_us); consumer_complaints_1m and emscad accept `dataset_pure_feature_value` warnings for values known at the prediction point |
| 8 | Licence and content noted, not a verdict reason | SEL-1, EV-4 | consistent | lucas_topsoil (EV-4: the licence is noted, not a reason); churn_telco_europa (No, 2026-10-12) and okcupid (Ethical Issue) differ on the facts |
| 9 | No `Spatial` tag | definitions.md `data_tags` | departs from emscad and the tag's definition; a reason is given but it is weak | emscad (`Spatial` for its `location` string, country/state/city); perth_house_prices (`ADDRESS` string plus geography, `Spatial`) |
| 10 | Exact copies and conflicting feature vectors dropped | LEAK-19, LEAK-20, LEAK-21 (Should) | consistent | wine_quality, audiology_diagnosis (LEAK-19); jm1, consumer_complaints (LEAK-20); emscad (LEAK-21) |
| 11 | `price` = 999,999,999 on 29 ads (65.5% blocked), kept and not mentioned in the notes (checklist, new finding) | CLEAN-10 (Should) | **departs without a stated reason** (minor, P7) | CLEAN-10 lists `999999` as a proxy value to convert, "keep a code and say why when it means something"; sdss_17 `-9999` and heart_disease_va_long_beach `chol == 0` made missing (CLEAN-11) |
| 12 | ROC AUC rather than the competition's AP@32500 | definitions.md, `metric` | consistent | house rule: "A competition with its own metric keeps our default, and the notes name the original metric" (the notes do) |

**1. Forced IID**

The definition does what SPLIT-8 says: the task is temporal in nature (the competition tested on the following
month), and the release has no dates at all, because the ids are random (discussion 9554, flat id deciles). Removing
the dataset "because the source task is temporal", which REVIEW_before issue 1 offers as an alternative, would depart
from a Must and from at least eight shipped definitions with the same tag. Its only support is SPLIT-7, and SPLIT-7's
case (combined_cycle_power_plant) is a stream of readings, which is forecasting. An ad is a separate unit, not a
reading in a stream. One small gap against the text of SPLIT-8: the notes do not say that the timestamp should be
recovered if a later release has it. Unlike account_debt_south_africa (file blocks), the cost cannot be measured here,
and the notes say so.

Not a third exception. SPLIT-8's parenthetical example ("one extract, the status at that moment standing in for a
forecast") is narrower than how the rule is applied: food_delivery_time, aps_failure, labour_inspection_compliance and
huntprohibited are event logs with their dates removed, not snapshots. The rule's main clause covers them, so no
amendment is due. A wording example for this kind of release could be added on the next pass.

**2. Text**

The precedents agree with the definition. Mercari is the stronger case of text dominance (almost all its signal is
in the text), and Lennart kept it. Here the structured columns alone reach ROC AUC 0.924-0.932, and LightGBM on the
structured columns plus SVD of TF-IDF reaches 0.987, against 0.994 for TF-IDF logistic regression. SEL-12 asks
whether "modality-specific models are clearly better", and a tabular model on vectorised text comes close to the best
text model, so SEL-12 is not triggered.

Pairs that look similar but differ on the facts:

* stackoverflow (`No`, `NLP (Text)`): its record is AI-filled and unverified, and its CC reasons are "no purpose" and
  feature engineering from ids. It is no curator precedent on SEL-12.
* jigsaw_unintended_bias100k and the other comment-moderation sets: they have no structured columns.
* avito_context_ad_clicks: `No` for CTR scope (`Out-of-scope Task`), not for Russian text.

One point in issue 2 should not weigh: the cost of the TabArena text cache (2.67M strings to embed). The Tensions
table settles this ("a model's input cap is never an argument", coad, Lennart 2026-10-15), and a pipeline's cost is
the same kind of argument.

**3. `attrs` as text**

Kickstarter decodes JSON fields that carry one value each (a category name, a location name). `attrs` is a form with
79 keys, 72 of them sparse, and a repeated key, `Этаж`, in 735,772 ads. CLEAN-19 asks what a data scientist on this
task would build and says to "take the features the top solutions share". The winners treated `attrs` as text
(discussion 10178). This is a stated reason, and it serves CLEAN-19 over CLEAN-12. If the curator keeps the string,
it is a departure with a fact behind it. A Cases row is optional, since CLEAN-12 does not literally cover JSON.

**4. Sellers and edited reposts (the precedent pair to raise)**

The facts that matter for the rule:

| | emscad (2026-09-30, Lennart) | huntprohibited |
|---|---|---|
| Moderation of posted ads, text heavy | yes | yes |
| The curator's concern | "fraudsters ... repeatedly try to post the same job ad" | CC: "malicious users, who one should detect instead of the ads itself" |
| Exact poster key | identical `company_profile`, or a poster-specific masked contact hash | none: no seller id, and contacts are masked without a hash |
| Who carries the label | per client (Vidros Sec. 5; 4,439 of 4,441 posters have one label) | per ad as far as the page says (a moderator blocks an ad); not checked |
| Exact reposts | dropped (LEAK-21) | dropped (LEAK-19/21) |
| Near-identical text | kept: dropping cosine >= 0.95 copies did not change the grouped AUC | kept: 1.39% of test ads share a 30+ character description with a train ad, ROC AUC changes by at most 0.002 |
| Split | grouped by poster; ROC AUC 0.99 IID -> 0.94 grouped | IID |

Keeping the near-copies matches emscad, so that part is consistent. The difference lies in the poster. The
curator's CC raises the same concern that led to emscad's poster grouping, and the poster carries the label in
emscad. SPLIT-29 and SPLIT-25 say that when the real groups matter and cannot be recovered, the dataset retires
(maternal_health_risk, hazelnut_spread_contaminant_detection). The definition says that sellers "cannot be grouped
exactly", which explains why there is no grouping. It does not say why the groups do not matter. The 0.002 bound
covers description-sharing reposts only, not sellers who write new text, and SPLIT-4/SPLIT-30 say the size of the gap
never decides. Two facts could set this case apart: the label is per ad (an ad blocked for its content, not an
account banned), and an exact description is an allowed SPLIT-24 key (like emscad's identical profile text). Neither
is written down.

**Consistency check (AI, 2026-10-20):** your call on huntprohibited (IID, sellers not grouped) differs from emscad
(grouped by poster, 2026-09-30: the same mechanism, ad moderation where the CC says posters should be detected, IID
0.99 against 0.94 grouped). Under SPLIT-25, maternal_health_risk was retired because its real groups could not be
recovered. What sets huntprohibited apart?
(a) Avito's label is set per ad (a moderator blocks an ad for its content), while emscad's label was assigned per
client (Vidros Sec. 5). So the seller does not carry the label (SPLIT-29), and the near-copies that do recur cost at
most 0.002. Record as an exception note in the definition. (b) Treat it like emscad: group on the one exact key the
data has (identical description text, SPLIT-24), and drop the fact that the poster cannot be recovered. (c) Treat it
like maternal_health_risk: the sellers matter and cannot be recovered, so `No` (SPLIT-25). (d) Reopen emscad to
match.

**5. Hidden-group hits**

Consistent. SPLIT-4: "If new rows keep having the value, the column is a feature and the split stays". Every new ad
has a subcategory and a form. The notes give the reason, so SPLIT-30 is satisfied.

**6. `is_proved`**

Consistent. It is set only for blocked ads (a component of the target). `is_blocked` is the decision Avito acts on
and the source's target (USE-5).

**7. Real estate**

Consistent. The winners left real estate out of training only. The source's cohort includes it, and real-estate ads
can have the outcome (0.12%), so LEAK-22 does not apply. The accepted `dataset_pure_feature_value` warning follows
consumer_complaints_1m (Block's response policy, known at filing).

**8. Licence and content**

Consistent with EV-4 and lucas_topsoil. The ethics pairs differ on the facts. churn_telco_europa (No, 2026-10-12) held
national ids and mobile numbers under a false name. Avito masked phones, e-mails and URLs, and first names and ages
are not direct identifiers. okcupid's target (sexual orientation) is itself the problem, and blocking an ad is not a
target about a person's protected traits.

**9. `Spatial` tag**

definitions.md: `"Spatial"` "when the data holds geographic information (ZIP, latitude and longitude, region, store
location)". emscad carries the tag for a free-text `location` (country, state, city). Here, 22.5% of the ads (all
real estate) hold a street address inside `attrs`. The stated reason ("no region or coordinates") does not match the
emscad precedent, which has none either. One fact could set it apart: the address is nested inside a form string
and covers only one category, so a model cannot use it as a geographic column. This is a tag question, not a
validity question.

**Consistency check (AI, 2026-10-20):** your call on huntprohibited (no `Spatial` tag) differs from emscad (tagged
`Spatial` for a free-text location string, no coordinates). What sets huntprohibited apart?
(a) The address sits inside the `attrs` form string, only for real estate (22.5% of ads, 0.12% blocked), so the
dataset has no geographic column. Record it as the reason in the notes. (b) Treat it like emscad and add `Spatial`.
(c) Remove emscad's tag to match. (d) Narrow the tag's definition (an amendment of definitions.md): a geographic
column, not a value inside a text field.

**10. Deduplication**

Consistent with LEAK-19/20/21. The 212 ads whose features occur with both labels are dropped as in jm1. Nothing
suggests they are genuine label ambiguity that the task has.

**11. `price` 999,999,999**

The checklist found 29 ads at 999,999,999 (65.5% blocked) and 1,411 at 1e8 or more (10.1% blocked). They are kept
and not mentioned in the notes. CLEAN-10 names `999999`-style values as proxy values. The rule converts them, or keeps
them as a code when the code means something, and says why. The precedents (sdss_17, heart_disease_va_long_beach)
converted. The high blocked share suggests the value means something (a fake price), which would justify keeping it,
but no reason is written down.

**Consistency check (AI, 2026-10-20):** keeping `price` = 999,999,999 unmentioned departs from CLEAN-10, where
sdss_17's `-9999` was made missing. What sets it apart?
(a) The value is what the seller typed into the form, and 65.5% of these ads are blocked, so it is a signal known
when the ad is posted (CLEAN-10: "keep a code and say why when it means something"). Add one Anomaly line to the
notes. (b) Treat it like sdss_17: make it missing. (c) Reopen sdss_17 (no: its -9999 is a pipeline fill value, not
an input). (d) Amend CLEAN-10 to say that a value a user enters stays.

**Drift and the third exception**

* Drift: none. The curator's decisions on SPLIT-8 (2026-10-12 account_debt_south_africa, 2026-10-14 emscad's tag,
  2026-10-19 the bulk field sync) and on text-heavy datasets (2026-10-06 mercari, 2026-10-01/06
  consumer_complaints, 2026-09-30 emscad) all point the same way.
* Third exception: none due. The forced-IID cases apply SPLIT-8; they are not exceptions to it.

**Files**

* Definition: `datasets/_dev/tabarena-v0pt2/huntprohibited_1m/dataset.py`
* Record: `curation/records/huntprohibited.md`
* emscad: `curation/records/emscad.md`, `datasets/_dev/tabarena-v0pt2/emscad/dataset.py`
* mercari: `curation/records/mercari_price_suggestion.md`
* kickstarter: `datasets/_dev/tabarena-v0pt2/kickstarter/dataset.py`
* The bulk field sync: `datasets/_dev/tabarena-v0pt2/CHANGELOG.md`, line 111
* Rules: `.claude/skills/knowledge-curation/references/splits.md` (SPLIT-4, -8, -24, -25, -29, -30, Cases),
  `selection.md` (SEL-12, Ethics), `leak_checks.md` (LEAK-17 to LEAK-22), `cleaning_features.md` (CLEAN-10, -19),
  `.claude/skills/knowledge-data-foundry/references/definitions.md` (`data_tags`, `metric`)

</details>

<details><summary>Advocate</summary>

**Advocate: ship huntprohibited_1m as defined (opening brief, 2026-10-20)**

Position: ship the code as it is (columns, cleaning, target, split). Every real problem the evidence agents found is
fixed by a note or a reworded sentence, the mildest rung of the remedy ladder. No change to `_clean`, the features or
the splits is needed.

**1. The split is the one SPLIT-8 prescribes, and the grouped alternative was run (P4, SPLIT-8 Must, SPLIT-25/29 Must)**

- Evidence: no date column; `itemid` AUC 0.4998, block share 0.0681-0.0693 over id deciles, holiday words flat over 20
  position bins, next-row label match 0.871837 against 0.871830 by chance (split audit, claim audit 28/52/61). The ids
  are random (host, discussion 9554). Eight shipped definitions carry the same tag for the same reason
  (account_debt_south_africa, aps_failure, food_delivery_time, labour_inspection_compliance, ...; precedents 1).
- Sellers/reposts: the split auditor grouped by exact description keys (SPLIT-24 allows exact keys): GroupKFold ROC AUC
  0.99384 / 0.99386 against 0.99390 random, AP within 0.002. Near-copies agree with the train label 99.5%.
- Rule: SPLIT-8 narrows SPLIT-7, so "drop because the source is temporal" (REVIEW_before 1) would break a Must, not
  apply one. SPLIT-29 needs an entity that carries the label; SPLIT-25 retires only "when the real groups matter". The
  label is set per ad (data page: ads "blocked for illicit content"), and the one exact key the data has moves the
  score by under 0.001. This is what sets the case apart from emscad, whose label was per client (Vidros Sec. 5) and
  whose grouped AUC fell 0.99 to 0.94.
- Conceded, with the fix: (a) SPLIT-8's second half is missing: add one sentence on what a date would change (season,
  drift in spam wording) and that it should be recovered if Avito releases it. (b) A seller who rewrites every ad is
  not covered by any measurement and cannot be (no seller id); write precedent option (a) as an exception note citing
  the per-ad label and the grouped run. Notes, not a re-split.

**2. Text does not take it out of scope: tabular models are competitive (P2, SEL-12 Must)**

- Evidence (fold 0): TF-IDF logistic regression 0.9947; LightGBM on structured columns plus 32 SVD dims per text
  column 0.9870; structured columns alone 0.9324 (claim audit 39; REVIEW_before 2). Task probe with strings as text:
  LightGBM 0.970, RF 0.970.
- Rule: SEL-12 removes text data only "where modality-specific models are clearly better"; here the winning 2014 model
  is a bag-of-words linear model, which is itself a tabular model on vectorised text, and no language model is needed.
  Precedents keep text-heavier sets: mercari (R^2 0.06 without text, kept), emscad, consumer_complaints. The cost of
  embedding 2.67M strings is not an argument (Tensions: a model's input cap is never an argument, coad).
- Conceded: claim 40 overstates ("loses most of the task"); reword to "loses most of the remaining error and most of
  the average precision" (AP 0.51 structured vs 0.95 text). Wording only.

**3. Every leak the source carried is removed, and the probes find none left (P4, LEAK-10 Must, LEAK-16 to LEAK-21)**

- Evidence: `close_hours` (post-decision, host "not available at scoring phase") and `is_proved` (set on 274,996 of
  274,996 blocked, 0 of 3,720,807 not blocked) dropped. Leak probe: best single structured feature subcategory 0.908 (a
  category the seller picks), no missing indicator, NN-distance AUC 0.512; exact copies across the split 0.0%; the 212
  both-label ads dropped (0.005%, LEAK-30 trace negligible).
- Open caveat, `price` is the final price of a possibly edited ad: price alone 0.740, the counts 0.502-0.512, and an
  edit re-enters moderation (practitioner). Weak at most, so LEAK-10 is a Should here and the existing note 11 is the
  remedy (column audit 1).

**4. A real use case with the target the actor acts on (P3, USE-1, USE-5, USE-8 Must)**

- Evidence: the practitioner (Avito trust-and-safety) agrees the fit is approximate and would use the model as a queue
  ranker; `is_blocked` is the moderator decision the score automates; claims 1/5/19/25 hold. Swapping to `is_proved`
  would trade the source's target for a convenient cleaner label (Tensions: the real-world target wins,
  corporate_credit_rating).
- Conceded, with the fix: `fit_reason` names only the split gap. Add the second: the model sees the ad's content only,
  not the seller, region, time or photos the site has. Add the cohort to `row`: closed ads, blocked for illicit
  content or never blocked. Fit stays approximate (USE-8 is met once both gaps are named).

**5. Worth benchmarking, with stable folds (P6, TP rules)**

- Evidence: task probe flags none; LightGBM minus linear +0.050 (paired SE 0.001); smallest class per test fold 3,399;
  generated-data probe flags none. Near the ceiling in ROC AUC, but AP spreads from 0.51 to 0.95 across pipelines, so
  the task separates methods. Real estate (0.12% blocked) is kept: it can have the outcome, so LEAK-22 does not apply,
  and moderation covers every ad (practitioner; precedents 7).
- Rule: Tensions "the right split against the score": a high score is no reason to retire.

**6. Faithful data, verified byte for byte (P5, PROV-13)**

- Evidence: zip 772,619,211 bytes, sha256 matches; 3,995,803 rows; 32,103 + 212 = 32,315 dropped; 1.5M stratified,
  6.865% blocked in every fold (claim audit 4, 17, 20). The blind reviewer's concern 3 (1.5M vs 3.9M) is answered by
  `version_comment`, which it did not see; its concern 2 ("keep `itemid`") is refuted by the id tests in point 1.

**7. The remaining findings are P7 notes, not reasons to change the data (P7, CLEAN-10/CLEAN-19 Should)**

- `price` 999,999,999 (29 raw ads, 65.5% blocked) and 1 (3,962 ads, 19.0% blocked) are what the seller typed and
  what the moderator saw: CLEAN-10 says "keep a code and say why when it means something". Fix: one Anomaly line.
  Making 0 missing (blind review) would merge "free" into missing; the notes already say 0 mixes both.
- `attrs` as text: CLEAN-19 (what the top solutions share; winners: "anything more fancy than ... tfidf added
  nothing", 10178) over kickstarter's decoding of single-value JSON. Keep.
- Claim 41 wording refuted (attrs missing on 2.76%, structural by subcategory): reword, the conclusion holds. Claim
  6/32/58: say the counts are Avito's, mostly the masks in the description. `Spatial` tag: a tag question for the
  curator, not validity. REVIEW.md's "Record fields that disagree" block is stale (record now Random (IID)): remove.

Judgment record (advocate):

```text
Verdict: ship (definition code unchanged; notes and task_summary wording updated).
Validity: SEL-12 holds (tabular models competitive); USE-8 holds once the content-only gap is named; LEAK-10 triggered,
fixed (close_hours, is_proved dropped); SPLIT-8 applied (ForcedIIDFromTemporal), note to complete; SPLIT-29/25 not met
(per-ad label; exact-key grouping changes ROC AUC < 0.001).
Value: TP probes clean; AP spread 0.51-0.95.
Quality: CLEAN-10 code kept with a note; CLEAN-19 over CLEAN-12 for attrs.
For the curator: the emscad consistency check (sellers), the Spatial tag.
```

**Advocate: rebuttal to the critic (2026-10-20)**

The critic and I agree on the facts and on every remedy. Neither of us asks to exclude the dataset, re-split it or
change a column. The only gap left is the label on the verdict. I concede it: "ship after changes", where every
change is to text (`task_summary` and `curation_comments`) and `_clean`, the features and the splits stay as they are.
Below I answer each point. Where I dispute something, it is the size of the problem, not the fix.

**1. SPLIT-8: concede the fix, dispute "breaks a Must"**

- Conceded: the second half of the rule (what a date would change, and that it should be recovered) is missing. I
  conceded this in my point 1(a). Add the critic's sentence, including that the cost cannot be measured because the
  April labels were never published.
- Disputed, on severity only: the Must's operative part (ship as IID, tagged) is applied, with the evidence the rule
  asks for. The ids are random (AUC 0.4998, flat over deciles and position bins, next-row label match at chance), and
  eight precedents carry the same tag. What is missing is documentation. Under the remedy ladder a missing note
  is fixed by writing it, so this point does not move the verdict.

**2. SPLIT-29 / SPLIT-25: concede**

- We agree on the fact that sets the case apart (the label is per ad), on the evidence (exact-key GroupKFold ROC AUC
  0.99384 / 0.99386 against 0.99390) and on the remedy: write it as the reason SPLIT-29 does not trigger, and replace
  the earlier-run "at most 0.002" with the split audit's numbers.
- One caveat for both of us: "the label is per ad" comes from the data page wording. Nobody measured it, and
  nobody can without a seller id. The note should say it is the source's wording (EV-2: page < measurement).

**3. USE-8: concede**

- This is the same fix as my point 4: add the content-only gap (no seller, region, time, photos or raw contacts) to
  `fit_reason`, and add the cohort (closed ads, blocked for illicit content or never blocked) to `row`. The fit stays
  approximate. My severity note from point 1 applies here too: the fit is already labelled approximate, and one gap
  is named. What is missing is the second gap, which is wording.

**4. USE-3: concede the wording, dispute the rank**

- Conceded: `fit_reason` says "everything ... is known when the ad is submitted", which contradicts note 11. Use
  the critic's wording ("as of its last version; the price is the final price").
- Disputed: this is not a USE-3/LEAK-1 problem of Must weight. Price alone scores ROC AUC 0.740, the counts score
  0.502-0.512, no missingness is tied to the outcome (column audit 1), and an edit re-enters moderation
  (practitioner). Under the rule's graded strength this is at most a weak leak (Should), and the existing note is
  the remedy. It is a writing fix, not a validity finding.

**5. Writing / EV-2: concede all four**

- Claim 41 reworded as the critic proposes. Claim 40 restated for the error and AP (I conceded this in my point 2).
  "0.50% of April ads" marked as coming from the 2026-10-07 run. "AP@32500" changed to "AP@k (k = 32,500 per the
  participants)": the evaluation page does not give K (claim audit 42). I missed this one, and it holds.

**6. CLEAN-10: concede (same as my point 7)**

- Add one Anomaly line: 999,999,999 (the form maximum, 29 raw ads, 65.5% blocked) and 1 (3,962 ads, 19.0% blocked)
  are placeholders the seller entered. They are kept because they are known at submission and carry signal.

**7. `Spatial` tag: concede that the reason as written fails; the choice goes to the curator**

- The stated reason ("no region or coordinates") applies to emscad as well, so it does not set this case apart. My
  lean is to keep the tag off and write the fact that does set it apart: the address is nested in one category's form
  string (real estate, 22.5% of ads, 0.12% blocked), and the dataset has no geographic column. Adding the tag is
  equally defensible. It changes no validity rule, so the curator decides.

**Net**

Agreed changes (all text): SPLIT-8 sentence; SPLIT-29 reason with the split audit's numbers; `fit_reason` (content-only
gap, last-version wording); `row` cohort clause; four rewordings (claims 40, 41, the April share, AP@k); the price
Anomaly line. For the curator: the `Spatial` tag, and the emscad consistency check, answered with option (a).

</details>

<details><summary>Critic</summary>

**Critic: huntprohibited_1m (opening brief, 2026-10-20)**

**Position: ship only after changes.** No point below is grounds to exclude: the task is real (practitioner: approximate
fit, would use it as a queue ranker), and every Must problem I found has a fix in the definition's text. But as
defined, the definition breaks two Musts in what it writes down (SPLIT-8, USE-8), leaves the emscad precedent
unanswered (SPLIT-29), and states claims the audit refuted. Points in rank order.

**1. SPLIT-8 (Must, P4): the forced IID split is tagged, but the rule's second half is not met**

- Problem: SPLIT-8 asks the definition to "say what the timestamp would change and that it should be recovered if a
  later release has it", and to measure the cost where the data allows. The notes say only that the monthly split
  "cannot be repeated".
- Effect: a reader of the score cannot tell how optimistic it is. The task is adversarial (sellers change wording to
  dodge blocks) and seasonal (New Year, 8 March in the window); a random split over the same four months overstates a
  model trained in March and used in April (practitioner, gap 1).
- Evidence: split_audit problem 1; precedents section 1 ("the notes do not say that the timestamp should be
  recovered"); April labels were never published, so the cost cannot be measured (claim audit, 7).
- Remedy (fix the definition, text): one sentence in `curation_comments`: what a date would change (adversarial drift
  in wording, seasonal items, category mix), that the cost cannot be measured because the April labels are not public,
  and that the time axis should be recovered if Avito or Kaggle releases dates.

**2. SPLIT-29 / SPLIT-25 (Must, P4): the seller question is answered with "cannot be grouped", not with "does not matter"**

- Problem: the record's CC asks to detect "malicious users, who one should detect instead of the ads itself". emscad,
  the same kind of task (ad moderation, text, the same CC concern), was grouped by poster and fell from 0.99 to 0.94
  ROC AUC (Lennart, 2026-09-30). Under SPLIT-25, when real groups matter and cannot be recovered, the dataset retires
  (maternal_health_risk). The definition says only why it cannot group, not why grouping is not needed.
- Effect: as written, the definition sits between emscad (grouped) and maternal_health_risk (retired) with no fact
  that sets it apart; the curator cannot tell it was a decision rather than an omission.
- Evidence: precedents section 4 and its consistency check; split_audit: grouping on exact description keys
  (SPLIT-24-allowed) changes ROC AUC by at most 0.0006 (0.99390 random vs 0.99384 / 0.99386 grouped), and 1.4-4.9% of
  test ads have a near copy in train with 99.5% label agreement. Not tested: sellers who rewrite their text (no id).
- Remedy (fix the definition, text): write the fact that sets this case apart: the label is per ad (a moderator blocks
  an ad for its content), and grouping on the exact keys the data allows changes nothing measurable (cite the split
  audit numbers, replacing the earlier-run "at most 0.002"). Record it as the reason SPLIT-29 does not trigger. I do
  not ask for exclusion: the evidence that the groups matter (SPLIT-25's condition) is absent.

**3. USE-8 (Must, P3): the fit names one gap; there are two, and the cohort is not in `row`**

- Problem: `fit_reason` names only the random split. The practitioner's second gap: the model sees only the ad's
  content, not the seller (account, history, earlier blocks), region, posting time, photos or the raw contacts that the
  site always has. `row` does not say the cohort is closed ads blocked for illicit content or never blocked (ads
  blocked for other reasons and live ads are not in the file).
- Effect: the task is a content-only screen, one component of moderation, not the moderation decision the use case
  describes; a reader takes the 0.99 ROC AUC as the decision's quality.
- Evidence: practitioner, gaps 2 and 3 and "What an expert would change"; claim audit 3 (data page: "All ads ... have
  already been closed").
- Remedy (fix the definition, task_summary): add the content-only gap to `fit_reason`; add the cohort clause to `row`.
  Fit stays approximate.

**4. USE-3 (Must, P4): "Everything the model sees is known when the ad is submitted" is not what the source says**

- Problem: `fit_reason` states it flatly, but the data page says `price` is the "final price of ad", so an edited ad
  carries its last version, not the version scored; whether the text and the masked counts are also final is not in
  the source. Bullet 11 notes the price caveat; the task summary contradicts it.
- Effect: small on the score (price alone ROC AUC 0.740; counts 0.502-0.512; no outcome-tied missingness, column
  audit problem 1), but the headline claim is untrue as worded.
- Evidence: claim audit 10/11/24 ("untested (partly against)"); column audit problem 1.
- Remedy (text): "known when the ad is submitted, as of its last version (the price is the final price)". No change to
  the data.

**5. Writing / EV-2: claims in the notes that the audit refuted or could not re-measure**

- "every new ad has both" (bullet 13): `attrs` is missing for 2.76% of ads (10.1% of blocked, 2.2% of unblocked),
  structurally, for 9 subcategories with no form (claim audit 41; column audit). Reword: "every ad has a subcategory,
  and attrs is its category's form (missing for the 2.8% of ads in categories without one)".
- "a pipeline that encodes Russian text poorly loses most of the task" (bullet 12): structured columns alone keep ROC
  AUC 0.932; the claim holds for the error (x13) and for AP (0.51 vs 0.95), not for AUC (claim audit 40). Reword to
  say so.
- "0.50% of the April test ads" (bullet 7): not re-measurable (avito_test.zip not in the warehouse); mark as from the
  2026-10-07 run.
- "AP@32500": K appears only in a participant's thread title (claim audit 42); say "AP@k (k = 32,500 per the
  participants)".
- Remedy: reword; no data change.

**6. CLEAN-10 (Should, P7): price placeholders kept without a word**

- Problem: 29 raw ads (14 shipped) have `price` = 999,999,999, the form maximum, 65.5% blocked; 3,962 shipped ads have
  `price` = 1 (19.0% blocked). CLEAN-10 keeps such a code only "and say why"; the notes say nothing (precedents 11;
  column audit problem 2; checklist).
- Effect: quality only; the values are what the moderator saw and carry signal, so keeping them is right.
- Remedy (a note): add to the Anomaly bullet that 999,999,999 and 1 are seller-entered placeholders, kept because they
  are known at submission. Not a reason against shipping.

**7. `data_tags` (house rule, definitions.md; precedent): no `Spatial` tag, with a reason the emscad precedent contradicts**

- Problem: 901,011 ads (22.5%, all real estate) carry a street address inside `attrs`; emscad carries `Spatial` for a
  free-text location string with no coordinates. The stated reason ("no region or coordinates") applies to emscad too.
- Remedy: either add `Spatial`, or write the fact that sets it apart (the address is nested in one category's form
  string, no geographic column). Curator's call; a tag, not validity.

**Not raised, and why**

- Text dominance (SEL-12): I cannot back exclusion. LightGBM on structured columns plus TF-IDF SVD reaches 0.987
  against 0.994 for TF-IDF LR, so tabular models are competitive; mercari and emscad are the precedents.
- Real estate as easy negatives: kept by the use case (moderation covers every ad); a weighing note, no rule broken.
- `is_proved` label, `attrs` as text: the definition's choices are backed (USE-5; CLEAN-19 via discussion 10178).
- REVIEW.md's stale "record fields that disagree" block: an editor fix, not a dataset point.

Judgment record (critic's ask): ship after changes. Validity: SPLIT-8 triggered, applied but its documentation half
missing (fix: note); SPLIT-29 open against emscad (fix: write the distinguishing fact); USE-8 gap incomplete (fix:
task_summary); USE-3 claim overstated (fix: wording). Quality: CLEAN-10 departure without a reason (fix: note). Tag:
`Spatial` for the curator.

**Critic: rebuttal to the advocate (huntprohibited_1m, 2026-10-20)**

We agree on the facts and on the remedies. The data, the cleaning, the target and the split stay as they are. What is
left is (a) what the verdict is called, and (b) two wording fixes the advocate's brief leaves out.

**On the advocate's points**

1. **Split, sellers (SPLIT-8, SPLIT-25/29).** Conceded on substance. The advocate concedes my points 1 and 2 and asks
   for the same notes: what a date would change, recover it if released, and the per-ad label plus the exact-key
   grouped run (0.99384 / 0.99386 against 0.99390) as the fact that sets this apart from emscad. One caveat stays: "the
   label is per ad" rests on the data page wording, and nobody checked it against a seller key, because none exists
   (precedents 4: "not checked"). The note should say so (EV-2: a page, not a measurement). That is wording, not a
   dispute.
2. **Text (SEL-12).** Conceded. I did not raise it: 0.987 for tabular plus SVD against 0.994 means tabular models are
   competitive. The claim 40 rewording is common ground.
3. **Leaks (LEAK-10, LEAK-16 to LEAK-21).** The dropped columns and the probes are conceded. On `price`, I agree the
   leak is weak (0.740 alone) and that note 11 covers the data side. **Disputed, narrowly:** my point 4 is not about
   the data. It is that `task_summary.fit_reason` says "Everything the model sees is known when the ad is submitted",
   which contradicts note 11 and the data page ("final price of ad"; claim audit 10/11, "untested (partly against)").
   USE-3 (Must) asks that the prediction point be written accurately, and the task summary is the first thing a user
   reads. Remedy: add "as of its last version". The advocate's brief does not address this sentence.
4. **Use case (USE-1, USE-5, USE-8).** Conceded. The advocate makes the same `fit_reason` and `row` fix I asked for
   (my point 3).
5. **Value (TP).** Conceded; I raised nothing on value.
6. **Provenance (PROV-13).** Conceded.
7. **P7 notes (CLEAN-10, CLEAN-19).** Conceded: keep the price codes with a note, keep `attrs` as text, reword
   claim 41, and leave `Spatial` to the curator. **Added, from my point 5, not in the advocate's list:** the "0.50% of
   April test ads" figure cannot be re-measured (the test zip is not in the warehouse), so mark it as from the
   2026-10-07 run. "AP@32500" should be "AP@k", since 32,500 comes only from a participant's thread title (claim audit
   42; EV-2).

**On the verdict**

- **Disputed: "ship" against "ship after changes".** The advocate's own judgment record says USE-8 "holds once the
  content-only gap is named" and SPLIT-8 has a "note to complete". So two Musts are not met by the definition as it
  stands. By principles.md ("a violation is fixed in the definition"), the verdict is **ship after changes**. The
  changes are text in `task_summary` and `curation_comments`, with no rebuild of the data beyond the checksum.
- Which rule wins: USE-8 and SPLIT-8 are Musts. "Ship as defined" cannot stand while both briefs agree the definition
  text must change first.

Settled between us: every remedy (notes and wording only, no data change); the emscad and `Spatial` questions go to
the curator. Open: the verdict label, and my wording points 4 and 5 (April figure, AP@k).

</details>

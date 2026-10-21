# house_prices_nominal

**Outcome:** added. De Cock's full Ames file (2,919 residential sales, January 2006 to June 2010) as a regression of
the log sale price, 13 two-month windows each trained on all earlier sales; the AI recommends shipping it after the
non-market sales are dropped. Validity: SEL-1 and SEL-2 hold; USE-1 holds with the city assessor as the actor (direct
fit); USE-5 triggered by 34 scored sales whose price is not a market value (issue 7); LEAK-10 holds (the record is the
house at the sale; one later remodel year set to missing); SPLIT-1, SPLIT-9 and SPLIT-14 hold; SPLIT-10 departed from
(no gap despite a short last month, issue 4). Value: no task-probe flag; the record's `Trivial` marker fails TP-4
(`Overall Qual` alone R² 0.682 against 0.911 for a linear model, worse in all 13 windows; issue 3). Quality: the drop
of De Cock's three outliers meets CLEAN-11 as amended (2026-10-21); CLEAN-12 open for the text codes (issue 9).
Weighed: original source +, twice the Kaggle rows +, an over-studied dataset - (no rule).

**Main points:** Drop the 82 family, allocation and adjoining-land sales (issue 7); a one-month gap or no gap as an
exception to SPLIT-10 (issue 4); remove the `Trivial` marker (issue 3); map the text codes to labels (issue 9); keep
the name (issue 10).

**Record judgment:** valid. The city assessor's record of each Ames sale with its price, published by De Cock (2011).

**Issues for Lennart:**

7. **Drop the sales whose price is not a market value?** The file's `Sale Condition` marks 82 sales as a sale
   between family members (`Family`, 46), an allocation of two linked properties with separate deeds, such as a
   condo and its garage unit (`Alloca`, 24), or a purchase of adjoining land (`AdjLand`, 12) (DataDocumentation.txt).
   34 of them are among the 1,450 test rows (17 Family, 15 Alloca, 2 AdjLand).
   - Effect on the task: the assessor values a house at its market value. Assessors' sales-ratio studies (the check
     of assessed values against sale prices) and the accuracy tests of valuation models leave such sales out (domain
     practitioner, from the standards of the IAAO, the International Association of Assessing Officers). Kept, they
     are scored as if the model should predict a family discount or a share of a joint price, and they carry large
     errors: RMSE by condition is 0.095 for normal sales, 0.291 for Family and 0.228 for Alloca (500-tree LightGBM,
     3 seeds, 13 windows). `Abnorml` sales (foreclosures and short sales) err about as much (0.250) and stay, as
     sales on the market, so the case rests on what the price means, not on the size of the error.
   - Evidence (same model and windows): dropping the 82 rows changes the mean scored RMSE from 0.1154 to 0.1103
     (-0.0051, SE 0.0029; lower in 8 of 13 windows); the RMSE on the remaining sales changes by -0.0008 (SE 0.0007)
     when the model trains without them, so nearly all of the change is from no longer scoring them. Dropping only
     `Alloca` gives -0.0007 (SE 0.0010) and keeps the two Family sales with the largest residuals (0.75 and 0.86).
   - Implemented: kept, with `Sale Condition` as a feature (dropping the feature costs +0.0045 RMSE, worse in 13 of
     13 windows). Alternative: drop the 82 rows.
   - Rule: USE-5 (P3, Must: the target is the quantity the actor acts on) against CLEAN-11 and CLEAN-1 (P7, Should:
     rows stay). The critic and the mediator: no one in the use case predicts these prices, and the definition
     already drops three training rows for not being market values. The advocate: De Cock does not call them
     outliers, and dropping hard rows makes the task easier. Closest curator precedent: california_house_prices_2020
     (CC 2026-10-14) drops prices that do not belong to the record; house_sales (AI draft, its issue 8) drops the
     county's non-market sale codes, family sales among them.
   - If the 82 rows are dropped, De Cock's three outliers rest on USE-5 as well as on CLEAN-11 as amended
     (2026-10-21).
   - Recommendation: drop the 82 rows (mediator, by rank). Decision: drop them, or rule that a flagged non-market
     price is a target the assessor acts on (then USE-5 is not triggered).

4. **A one-month gap, or no gap as an exception to SPLIT-10?** A price model is refit on all earlier sales, and each
   window trains up to the month before it. SPLIT-10 (P4, Should) asks for a gap when the newest rows are recorded
   late, as here: the extract's last full month, June 2010, holds 82 sales against 97-112 in the Junes of 2006-2009
   (about 78% of a usual June), and July 2010 (8 sales) is cut.
   - Effect on the task: if the late-recorded sales were a biased subset (cheap or expensive), the newest training
     month would mislead the model. The 73 normal sales of June 2010 show no such bias (mean residual -0.001, RMSE
     0.105); June 2010 is only ever a test month, never trained on.
   - Implemented: no gap. The cost of a gap is small either way: one month +0.0004 to +0.0010 RMSE, two months
     +0.0016 to +0.0026 (500-tree LightGBM, 3 seeds, 13 windows), within noise.
   - The small cost cannot be the reason: principles.md's table of tensions has a row "the right split against the
     score", which says the split follows the application, not the size of the effect (precedent forest_fires).
   - Alternatives: (a) a one-month gap, SPLIT-10's default and zillow_prize's choice (AI draft); (b) no gap as an
     exception on the mechanism: `**Exception to SPLIT-10 (2026-10-20, Lennart):** the only visible recording
     shortfall is the extract's last month (June 2010, 78% of a usual June), and its normal sales show no price
     selection (mean residual -0.001); serves P4: the windows train on every recorded sale before them, as the
     assessor's refit does.`
   - house_sales already has a one-week gap. The answer carries to perth_house_prices, which cites this dataset for
     its no-gap split, and to melbourne_housing_market (working copy REVIEW.md, "Rules from the house_prices_nominal
     review").
   - Recommendation: (b). Decision: (a) or (b).

3. **Remove the `Trivial` marker?** `Overall Qual` alone, chosen on each training side, reaches R² 0.682 (RMSE 0.228)
   against 0.911 (0.119) for the task probe's linear model and 0.900 (0.126) for its LightGBM, and is worse in all 13
   windows; De Cock's own two-variable model (neighbourhood and total area) reaches R² 0.766. The task probe raises no
   flag.
   - Effect on the task: none on the data; on the record the marker reads as a reason not to ship, which the numbers
     do not support.
   - Implemented: the notes say the marker does not hold; the record still carries it. Alternative: keep it.
   - Rule: TP-4 (Must: `Trivial` needs proof); precedents california_house_prices_2020 and aps_failure drop the
     marker on the same evidence. The curator removes markers.
   - Recommendation: remove it. Decision: remove or keep.

9. **Map the text codes of 43 columns to the documentation's labels?** Apart from `MS SubClass` and the absent-item
   levels, the categorical columns keep the source's short codes (`TA` for typical/average, `GLQ` for good living
   quarters, `Gtl` for gentle slope).
   - Effect on the task: none for a model that treats each code as a category; a model that reads text gets
     abbreviations instead of words.
   - Implemented: the codes. Alternative: map every code to its DataDocumentation.txt label in one lookup, as for
     `MS SubClass`. Mapping does not order the 21 graded columns: Ex to Po stay unordered categories (CLEAN-14), as
     the column audit recommends.
   - Rule: CLEAN-12 (P7, Should: undo destroyed meaning). Precedents: credit_g, college_scorecard and
     melbourne_housing_market (AI draft) map codes to labels. The fact that could set this case apart: the codes are
     readable abbreviations decoded by one documented lookup, unlike credit_g's `A11`. The advocate and the critic
     accept either.
   - Recommendation: map them. Decision: map, or record an exception to CLEAN-12 with that fact.

10. **Keep the name `house_prices_nominal`?** It is OpenML's name for the Kaggle half (OpenML 42165); the folder ships
    De Cock's full file. `ames_housing_dataset`, a Kaggle mirror of the same file, stays `Duplicate`.
    - Effect on the task: none; the name only tells a user which data ship.
    - Implemented: the record's name. Alternative: rename to `ames_housing` (no precedent), which describes the data.
    - Rule: none (a naming choice); the precedent is hr_analytics, which kept its record's name after a source swap.
    - Recommendation: keep it. Decision: keep or rename.

**Review panel:** ship after changes (mediator). The panel's numbers are on the definition before this review's
changes. The mediator's issues 1, 2, 3 and 4 are issues 7, 4, 9, and 3 with 10 here; "REVIEW_before" in the other
reports is an earlier draft of this file. Claim audit: 46 claims, 34 hold as stated, one refuted (the OpenML wording,
fixed), two with stale numbers (fixed), and the record's `Trivial` marker refuted (issue 3). Blind review: include
with changes; main concern where the rows come from (the definition cites De Cock). Debate: agreed on the source, the
assessor as the actor, the outlier drop and the cleaning fixes; disputed: the non-market sales (issue 7).

<details><summary>Mediator</summary>

Summary. Verdict: ship after changes. All validity Musts hold except one, settled by rank: Family, Alloca and AdjLand
sale prices are not the market value either agreed actor uses; USE-5 (Must, P3) outranks CLEAN-11 (Should, P7), so drop
all 82 such rows. Decisive run (13 windows, 500-tree LightGBM, 3 seeds): mean scored RMSE -0.0051 (SE 0.0029), lower in
8 of 13 windows; nearly all from no longer scoring those rows (training without them changes RMSE on the remaining rows
by -0.0008, SE 0.0007). Dropping Alloca only gives -0.0007 and leaves the worst rows (Family sales): not a real middle
option. Abnorml sales are just as noisy (RMSE 0.250), so the case rests on what the target means, not on error size.
The SPLIT-10 exception must rest on the mechanism, not on a small effect: June 2010's Normal sales show no price
selection.

**Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL-1, SEL-2 hold; USE-1 holds once use_case names the assessor (direct fit, USE-9); USE-5 triggered by
  34 scored non-market prices, fixed by dropping Sale Condition in {Family, Alloca, AdjLand} (82 rows; curator
  confirms, issue 1); USE-3/LEAK-10 hold (row 937 one post-sale value, set missing); SPLIT-1/9/14 hold; SPLIT-10
  departure kept as an exception on a mechanism fact (issue 2); PROV-8 holds (record links to fix).
Value: TP-4 refutes `Trivial` (Overall Qual R² 0.682 vs ~0.91, loses 13/13); models spread +0.026 (SE 0.005).
Quality: CLEAN-11 outlier drop as an exception via CLEAN-1 (third of its kind: propose an amendment); CLEAN-12
  Exterior 2nd mapped; CLEAN-3 PID reason replaced with the measurement; CLEAN-12 codes: curator's choice (issue 3).
Weighed: source +, size + (2,919 vs 1,460), signal +, over-studied - (no rule; note at most).
For the curator: issue 1 (drop the non-market sales; my recommendation by rank), issue 2 (SPLIT-10 exception text,
  set for the house-price family), issue 3 (map codes or a CLEAN-12 exception), issue 4 (record: Trivial marker, name).
```

**Changes to make now (no decision needed; both sides agree)**

1. Rewrite `use_case` around the source's actor: "a city assessor values residential properties from recent sales,
   refit as new sales arrive". Drop the lender and keep `fit = "direct"` (USE-1, USE-9).
2. `fit_reason` and the curation bullet say what was tested: "the assessor's file of about 2010; no remodel year
   postdates its sale except one new house (2008, sold 2007)". Add one plain sentence that the timing of the grades
   cannot be checked from the file. No `Potential leak` line (the critic withdrew it; USE-3; EV-6/7).
3. Row 937: set `Year Remod/Add` to missing. Row 2032 (remodelled 2001, built 2002): set to missing (CLEAN-11;
   LEAK-10 weak, one training row).
4. Replace "A price is known once the sale is recorded" in `splits_comment` (contradicted: July 2010 has 8 sales,
   June 2010 is at 78% of a usual June) with the exception text of issue 2 (SPLIT-10; writing.md).
5. Update stale numbers and name the run behind each (EV-8): outlier effect, linear model 0.125 -> 0.119; "0.912" is a
   500-tree LightGBM with 3 seeds, the probe's LightGBM gives 0.901; gap effect "under 0.003 RMSE, within noise".
6. Claim 23: remove "as in OpenML's house_prices_nominal" (refuted; EV-4 case of 2026-10-15).
7. `Exterior 2nd`: map `Brk Cmn`/`CmentBd`/`Wd Shng` to `BrkComm`/`CemntBd`/`WdShing`, 225 rows (CLEAN-12).
8. `PID`: replace "unique per row" with the measurement: the block prefix as a feature changes RMSE by -0.0005
   (SE 0.0005); the section by -0.0001 (SE 0.0007) (CLEAN-3; EV-2).
9. Write the drop of De Cock's 3 outliers in the exception form via CLEAN-1; flag it as the third target-outlier row
   drop (after mercedes_benz_greener_manufacturing and qsar_tid_11), so the next pass proposes an amendment to CLEAN-11.
10. Record: add the JSE file and DOI 10.1080/10691898.2011.11889627 to `source_links` (PROV-8; hr_analytics precedent).

**Issues for the curator, ranked**

**1. Non-market sales in the scored windows (P3, USE-5 Must against CLEAN-11/CLEAN-1 Should). Recommendation: drop
Family, Alloca and AdjLand; keep Abnorml.**

- Problem: 82 rows, 34 of them among the 1,450 test rows (17 Family, 15 Alloca, 2 AdjLand). Their prices are not the
  market value the assessor or a valuation service targets: DataDocumentation defines them as "Sale between family
  members" and "two linked properties with separate deeds"; assessors' ratio studies and AVM accuracy tests exclude such
  sales (practitioner; IAAO-based sources); the advocate concedes the assessor point.
- Rank: USE-5 is a P3 Must; CLEAN-11 and CLEAN-1 are P7 Shoulds. The tension row: "a cleaning gap that changes what
  the target means is a validity question".
- Decisive experiment (500-tree LightGBM, 3 seeds, 13 windows): mean scored RMSE 0.1154 with the rows, 0.1103 without,
  -0.0051 (SE 0.0029), lower in 8 of 13 windows. Biggest changes: window 7 0.123 -> 0.091, window 12 0.107 -> 0.088
  (Family sales); window 0 0.156 -> 0.145. Training effect on the same market rows -0.0008 (SE 0.0007). Alloca only:
  -0.0007 (SE 0.0010), 6 of 13 windows; misses the Family rows behind the largest errors (residuals 0.75 and 0.86).
  RMSE by condition: Normal 0.095, Partial 0.132, Abnorml 0.250, Alloca 0.228, Family 0.291, AdjLand 0.062.
- Advocate's best evidence: De Cock does not call these rows outliers; `Sale Condition` is a feature worth +0.0045
  RMSE in 13 of 13 windows; dropping hard rows makes the task easier; zillow_prize and house_sales keep linked units,
  sberbank keeps pre-completion sales.
- Critic's best evidence: under the agreed actor no one targets these prices; the definition drops 3 training-only rows
  for not being market values, yet scores 34 rows with the same defect.
- Reading: the advocate's precedents concern copies (zillow_prize, house_sales) or market sales (sberbank, CC
  2026-10-14). Closest curator precedent: california_house_prices_2020, which dropped prices that do not belong to the
  record. "The model can learn them" is CLEAN-1, a P7 Should, and cannot outrank USE-5.
- Decision needed: confirm the drop, or rule that a recorded, flagged non-market price is a target the actor acts on
  (a finding that USE-5 is not triggered, not an exception). De Cock's teaching advice (p. 9) is to keep only Normal
  sales; it supports neither side directly.

**2. The form of the SPLIT-10 exception (P4, Should). Both sides agree on an exception; its fact needs fixing.**

- Effect size alone cannot be the fact (tension row "the right split against the score", forest_fires).
- The fact: the mechanism SPLIT-10 guards against is bias from fast-recorded newest rows. The 73 Normal sales of June
  2010, the only month visibly short, have a mean residual of -0.001 (RMSE 0.105); June's lower price is explained by
  smaller houses; June 2010 is test-only, so it never trains.
- Proposed text: `**Exception to SPLIT-10 (2026-10-20, <curator>):** the only visible recording shortfall is the
  extract's last month (June 2010, 78% of a usual June), and its Normal sales show no price selection (mean residual
  -0.001); serves P4: the windows train on every recorded sale before them, as the assessor's refit does.`
- Other option (a): a one-month gap, matching zillow_prize (an AI draft) and SPLIT-10's default.
- Decision needed: (a) or (b). It carries to house_sales and perth_house_prices (which cites this dataset for its "no
  gap"). If issue 1 is accepted, June's 2 Alloca rows leave too.

**3. The 43 text-coded columns (P7, CLEAN-12 Should).** Map the codes to DataDocumentation's labels (credit_g,
college_scorecard, melbourne precedents) or an exception: "readable abbreviations decoded in one lookup, unlike `A11`".
Both sides accept either. The OpenML reason goes in any case (change 6).

**4. Record items (procedure).** Remove `Trivial` (TP-4 refutes it; the curator removes markers). Keep the name
`house_prices_nominal` (hr_analytics precedent) or rename to `ames_housing` (no precedent). The JSE licence stays a
note (lucas_topsoil).

**Agreed facts**

- De Cock's JSE file, sha256 matches; 2,930 raw rows, 2,919 after the July 2010 cut (8 sales) and the 3 outliers. The
  Kaggle train file is a random half: 1,460 of 1,460 rows match.
- 13 expanding two-month windows, 46-191 test rows (median 98); train share 50.3-94.5%; no overlap, no training row
  after its window. A random split is 0.005-0.010 RMSE more optimistic.
- LEAK-10: no remodel after the sale for houses built 2 or more years before it; refuting test (0.0% in 2006 vs 5.2% in
  2010) passes. One post-sale value (row 937, training only). Grade revision cannot be tested.
- Probes: no leak, task, hidden-group or generated-data flag. Overall Qual alone R² 0.682, below the models in 13 of 13.
- The 3 dropped outliers are training-only ($28-$40 per sq ft vs $150) and named by De Cock (p. 4).
- `Sale Condition` worth +0.0045 RMSE (13 of 13). Gap cost: 1 month +0.0004 to +0.0010, 2 months +0.0016 to +0.0026,
  within noise.
- June 2010: 82 sales vs 97-112 in earlier Junes; April 2010: 72 vs 48-61, its excess error in 9 non-Normal sales.
- Both sides recommend ship after changes; only issue 1 is disputed.

**Consistency with precedent**

- Followed: hr_analytics (source swap; name and links); california_house_prices_2020 and aps_failure/sepsis (`Trivial`
  dropped on TP-4); house_sales and zillow_prize (prediction point "a house sells"; July cut); the temporal-against-
  grouped tension row (Lennart, 2026-10-12); coffee_rating_prediction (two-month windows, SPLIT-17).
- Departure (issue 1): the precedent checker scored keeping these rows as consistent (its decision 10); the mediator
  departs on one fact: under the agreed actor their price is not a market value.
- Third exception: the outlier drop is the third CLEAN-11 row drop of its kind; propose the amendment. If issue 1 is
  accepted, its drop rests on USE-5, not CLEAN-11.
- Open across the family: SPLIT-10 for house_sales, perth_house_prices and zillow_prize (issue 2).

</details>

<details><summary>Claim audit</summary>

Data: the definition's container rebuilt through `dataset_io.load(..., built=True)` (no build record, so `rebuilt`;
2,919 x 79, 13 splits), the raw `AmesHousing.txt` (sha256 matches), De Cock (2011) PDF text, DataDocumentation.txt,
the JSE policy page, OpenML 42165 arff and 42563 metadata, all fetched today into (run folder). Scripts:
`t1.py` (counts, cleaning), `t2.py` (windows, outliers, blocks, snapshot test), `t3.py` (task probe with
and without the 3 outliers, `ds_keep_outliers.py` is a copy of the definition without the drop), `t4.py`
(500-tree LightGBM, 3 seeds: gaps, feature drops; De Cock's two-variable model), `t5.py` (types vs documentation,
Kaggle overlap). Threads capped at 2.

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | question: sale price of an Ames house | D task_summary | target column vs raw `SalePrice` | holds | `log_SalePrice` = log(SalePrice) | USE-5 |
| 2 | use case: lender / valuation service, refit every 2 months | D task_summary | split plan vs use case | holds (framing; "lender" is "for example") | 13 expanding 2-month windows, no gap | USE-1, USE-10 |
| 3 | 2,919 sales, Jan 2006 - Jun 2010, assessor's office | D task_summary | shape, month range; paper p.2-3 | holds | 2,919 rows; 2006-01 to 2010-06; paper: "data dump from their records system" of the Assessor's Office | USE-2 |
| 4 | predicted: sale price in USD, log scale | D | as 1 | holds | natural log | USE-5 |
| 5 | known: assessor's record + sale month, type, condition | D | column list; snapshot test (claim 26) | holds | 78 features are those groups | LEAK-1 |
| 6, 35 | 13 two-month windows May-Jun 2008 .. May-Jun 2010, newest first, train all earlier | D task_summary, splits_comment | enumerate shipped splits | holds | 13 windows; first 2010-05..06, last 2008-05..06; train = every earlier row in all 13 (set equality) | SPLIT-1, SPLIT-9 |
| 7 | Kaggle is a random half; split by month; 3 partial sales dropped | D | Kaggle 42165 arff vs raw; outlier mask | holds | 1,460/1,460 Kaggle rows match a raw row on (Lot Area, Year Built, Gr Liv Area, Yr Sold, Mo Sold, SalePrice); 3 rows dropped | PROV-1 |
| 8, 9 | fit direct; De Cock kept latest sale only, older months miss ~100 sales | D | paper p.4 text | holds (primary document, EV-2 rank 2; not measurable in the file) | "approximately 100 homes changed ownership multiple times ... I elected to keep only the most recent sales data on any property" | USE-8, USE-9 |
| 10 | source_url, Other, 2011, domain, `Spatial` | D | DOI; tag definition | holds | `Neighborhood` (28 areas) is regional information (definitions.md: "region") | PROV-2 |
| 11, 47 | licence: teaching free; publication needs author consent | D, R | JSE policy page | holds | "Data Sets may be freely used in teaching ... To use data sets in papers, books, or other published material you must obtain the consent of the contributing author." | EV-4 (note only) |
| 12 | 2,930 x 82, sha256 6cfe...cfcc; Kaggle/OpenML 42165 hold 1,460 | D | hash, shape, overlap | holds | sha256 equal; (2930, 82); 1,460 matched | PROV-1 |
| 13 | 2,930 sales Jan 2006 - Jul 2010, Ames City Assessor's Office | D | raw months; paper | holds | 2006-01 to 2010-07 | PROV-2 |
| 14 | prediction point: a house sells | D | snapshot test, feature drops | holds as stated; the moment is a judgment call (see U1) | | USE-3 |
| 15 | twice the labelled rows, values as published | D | counts | holds | 2,930 vs 1,460 | PROV-1 |
| 16 | ~100 sales missing (paper p.4) | D | paper | holds | quote under 8-9 | PROV-2 |
| 17, 31 | July 2010 cut: 8 vs 101-122 | D | counts | holds | July: 122/108/101/110/8 | LEAK-22..26 |
| 18 | PID unique per row | D | `is_unique` | holds | 2,930 unique | SPLIT-29 |
| 19 | Month Sold from Yr/Mo Sold, no day | D | columns | holds | | CLEAN |
| 20 | 14 NA-level columns; 2 detached garages with NA as missing | D | raw counts by anchor | holds | garage exists but Finish/Qual/Cond NA: 2 rows, both `Detchd`; no basement column non-NA where `Bsmt Qual`=NA; Fireplace/Pool/Misc NA consistent with counts (0 conflicts) | CLEAN-1..6 |
| 21 | MS SubClass labels; `Sale Type` "WD " stripped | D | values | holds | 16 labels; Sale Type values have no trailing blank | CLEAN |
| 22 | Garage Yr Blt 2207 typo, house built 2006, sold 2007 | D | raw | holds | one row 2207 (built 2006, sold 2007, New); one other row 2008 > sale 2007 is a new build (built 2008), kept correctly | PROV-13 |
| 23 | 23 nominal + 21 text ordinal categorical "with the source's codes, as in OpenML's house_prices_nominal" | D | doc types; OpenML 42563 feature list | partly refuted | counts hold (doc: 24 nominal incl. PID, 23 ordinal of which Overall Qual/Cond numeric; shipped 44 categorical). But OpenML 42563 `house_prices_nominal` has 43 nominal with `MSSubClass` numeric, and the shipped categories are not "the source's codes" for MS SubClass (relabelled) and the 14 NA levels (written out) | writing.md, CLEAN |
| 24 | log target; RMSE on it is the competition's metric | D | Kaggle evaluation text (via mirrors) | holds | "RMSE between the logarithm of the predicted value and the logarithm of the observed sales price" | USE-5 |
| 25 | 3 outliers dropped, 2 kept; linear RMSE 0.133 -> 0.124 | D | task probe with and without the 3 rows | refuted (numbers stale), direction holds | today: linear 0.1251 (with) -> 0.1188 (without), LightGBM 0.1260 -> 0.1250; drop list holds ($28.4/36.1/39.5 per sq ft, Partial, Edwards) | EV-8, writing.md |
| 26 | record at the sale: no house built >= 2 yrs before sale has remodel after it | D | count + snapshot test | holds (strong) | 0 rows; 3 rows remod > sale are all Partial new builds. Refuting test: houses built <= 2004 with remodel in 2007-2009: 0.0% of 2006 sales vs 5.2% of 2010 sales; a 2010 snapshot would show ~5% in 2006 too | LEAK-1, LEAK-10 |
| 27 | Year Remod/Add floor 1950: 337 of 629 pre-1950 | D | shipped counts | holds | 337/629 (raw 339/632); no pre-1950 house has remod = built year | CLEAN |
| 28 | Alloca / AdjLand mostly in blocks of one month | D | group by month x neighbourhood | holds | Alloca 16/24 in blocks (8 SawyerW 2009-06), AdjLand 9/12 | SPLIT-29 |
| 29 | no duplicate rows; two pairs share features, same month, different prices | D | duplicated() | holds | 0 full dups; 4 rows (Edwards 2006-05 $130,000/$134,000; Somerst 2006-07 $149,900/$147,400) | LEAK-16 |
| 30 | Trivial does not hold: Overall Qual R² 0.682, De Cock 0.766, LightGBM 0.912 | D | probe; De Cock OLS per window; 500-tree LGBM 3 seeds | holds, source mixed | single feature 0.6815 (probe); De Cock nbhd + (Total Bsmt SF + Gr Liv Area) mean window R² 0.7657 (in-sample all rows 0.802, matching paper "about 80%"); 500-tree LGBM 0.9117. But the probe's LightGBM is 0.901 and its linear 0.911: "0.912 for LightGBM" is from an unnamed 500-tree run | EV-8, TP-4 |
| 32, 34, 37 | monthly 19-112; two-month 46-191; quarterly 91-233 | D | TemporalSplits on shipped frame | holds | 1 mo: 26 windows 19-112; 2 mo: 13, 46-191 (median 98); 3 mo: 8, 91-233 | SPLIT-17 |
| 33 | $28-40 vs median ~$150; all five before oldest test window | D decision 3 | raw | holds | median partial $149.8; five sold 2007-01..2008-01 < 2008-05 | |
| 36 | Mar-Apr 2008 window would train on 47% | D | share of rows before 2008-03 | holds | 47.0% | SPLIT (min_train_fraction) |
| 38 | price known once recorded, no gap | D | split check | holds | train max month = test min - 1 in all windows | SPLIT-9 |
| 39 | gap 1 / 2 months: +0.0006 (SE 0.0010) / +0.0026 (SE 0.0013) | D | rerun 500-tree LGBM, 3 seeds, train trimmed by 1/2 months | numbers not reproduced; conclusion holds | +0.0010 (SE 0.0015, worse 9/13) / +0.0016 (SE 0.0012, 8/13): both within noise, below 0.003; LightGBM config of the original run not stated | EV-8 |
| (R4) | dropping Sale Condition +0.0047, Sale Type 0, Month Sold ~0 | REVIEW_before 4 | same rerun | holds | +0.0045 (SE 0.0009, 13/13); Sale Type -0.0004 (SE 0.0009); Month Sold +0.0008 (SE 0.0009) | USE-3 |
| 40 | 0 warnings | D | dataset_check.txt | holds | 0 errors, 0 warnings, 1 info | |
| 41, 42 | record: 1,460 samples, Kaggle split not temporal; `Trivial`; source_links Kaggle + OpenML 42165 only | R | overlap; probe | 41 holds for Kaggle; `Trivial` refuted (claim 30); source_links do not name the data shipped | the shipped data is De Cock's file, not in `source_links` | PROV-1, PROV-8, TP-4 |
| 43 | Kaggle train is a random half; all 1,460 rows match | R | arff vs raw | holds (6-column key; not every feature re-checked) | 1,460/1,460 | PROV-4 |
| 44 | `ames_housing_dataset` mirror equals the file | R | not run (no copy fetched) | untested | | PROV-4 |
| 45 | 2,919 rows, log price, 13 windows | R | as above | holds | | |
| 46 | per-grade mean worse than LightGBM in all 13 (0.228 vs 0.119) | R | probe | holds | single 0.2275, 500-tree LGBM 0.1183 | TP-4 |
| 48 | priority 3 | R | weighing | not a factual claim | | |

**Implied claims**

| Implied claim | Test | Result | Evidence | Rule |
|---|---|---|---|---|
| Every feature is known at the prediction point | snapshot test (claim 26); garage/remod years vs sale year | holds for resales; for Partial (new) sales the record describes the finished house after the sale | 3 remod > sale year, 1 built > sale year, 1 garage 2008 > sale 2007, all Partial new builds: the contracted house, known from the plans | LEAK-1, LEAK-10 |
| The split is the one the use case needs | windows vs "refit every two months" | holds | expanding, no gap, newest first | SPLIT-1, USE-10 |
| The target is the real-world target | target vs use case | holds, with the Alloca caveat | Alloca prices can be a share of a joint price (REVIEW_before 7); kept with `Sale Condition` | USE-5 |
| No row is a copy across the split | PID unique; full and feature duplicates; probe | holds | 0 exact copies across splits (leak probe); the 2 identical-feature pairs are same month, one side; near copies seen 0.9% | LEAK-16..21 |
| Every window is scorable at ~50 rows | window sizes | minor | one window of 46 rows (Jan-Feb 2009) | SPLIT-17 (Should, "about 50") |

**Refuted, ranked (principles.md)**

1. **Claim 23 (P7 / writing, quality).** "categorical with the source's codes, as in OpenML's house_prices_nominal":
   OpenML 42563 keeps `MSSubClass` numeric (43 nominal, not 44) and the definition relabels MS SubClass and the 14 NA
   levels. Changes nothing in the data. Mildest remedy: reword to "categorical, as the documentation types them
   (OpenML's house_prices_nominal keeps MS SubClass numeric)" and drop "with the source's codes".
2. **Claim 25 (procedure, EV-8).** "linear model from RMSE 0.133 to 0.124": today's probe gives 0.125 -> 0.119
   (LightGBM 0.126 -> 0.125). The decision stands. Remedy: update the two numbers and name the probe run.
3. **Claim 30 / 39 sources (procedure, EV-8, not refuted on substance).** "0.912 for LightGBM" is a 500-tree run, not
   the probe beside it (probe LightGBM 0.901, linear 0.911); the gap effects reproduce in conclusion but not in digits
   (+0.0010/+0.0016 vs +0.0006/+0.0026). Remedy: name the model ("a 500-tree LightGBM, 3 seeds") or quote the probe's
   numbers; give the gap effect as "under 0.003 RMSE, within noise".

**Untested, ranked**

1. **U1, prediction point (P3/P4, USE-3, LEAK-10; a judgment, not testable on the data).** `Sale Condition` is worth
   +0.0045 RMSE (13/13 windows). For a lender at origination it is known; for a valuation service estimating a house
   before it is listed, foreclosure/family/allocation status is often not. The definition's moment ("a house sells")
   makes it known; the curator decides the moment (REVIEW_before 4). Mildest remedy: keep, and state in
   `curation_comments` that the sale's type and condition are known at the moment.
2. **Claim 44 (P5, PROV-4).** The `ames_housing_dataset` mirror was not fetched; its Duplicate marker rests on the
   2026-10-07 assessment. Changes nothing here.
3. **Source links (P5, PROV-1/PROV-8, not a written claim).** The record's `source_links` still name only Kaggle and
   OpenML 42165; the shipped file (JSE) is in the definition only. Remedy: add the JSE file and DOI to the record.

</details>

<details><summary>Column audit</summary>

Definition `datasets/_dev/tabarena-v0pt2/house_prices_nominal/dataset.py`; frame rebuilt through `dataset_io.load(...,
built=False)` (2,919 rows, 77 features + target + `Month Sold`). Codebook: DataDocumentation.txt (JSE, fetched to
(run folder)). Scripts: (run folder), `checks.py`, `checks2.py`, `pid.py`, `pid_effect.py`.

Prediction point (bullet 1): a house sells; an AVM refit every two months predicts its price from the assessor's
record and the sale's type and condition. Every column is tested against that point.

**The key timing check (LEAK-10, the King County lesson)**

The codebook says the file holds the assessor's data "used in computing assessed values for individual residential
properties sold". If the attributes were the 2010 record looked up after the sale, houses sold early would show
remodels after their sale. Measured: among houses built two or more years before the sale, `Year Remod/Add` is never
after the sale year (0 of ~2,590). Older houses are remodelled in the year before their sale at 1.6-5.3% per sale year,
so a 2010 snapshot would have put dozens of post-sale remodels into the 2006-2008 sales. `Year Built` and `Garage Yr
Blt` are never after the sale year either. The record is as at the sale: the property attributes pass. One exception:
row 937 (built 2007, `Year Remod/Add` 2008, Partial sale 2007-06): a value from after the sale (the finished new
house). Residual, unknowable from the file: whether grades (`Overall Qual`, `Exter Cond` "present condition") were
revised at the assessor's sales verification; no evidence either way, no action.

**Column table**

Known = known at the prediction point. All categorical columns are unordered `category` with the source's codes.

| Column(s) | Meaning (codebook) | Known? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| MS SubClass | dwelling type in the sale | yes | category, codes mapped to documented labels (16) | fine | CLEAN-12 |
| MS Zoning | zoning class | yes | category; data codes `C (all)`, `A (agr)`, `I (all)` vs doc `C`, `A`, `I` (harmless) | fine | CLEAN-14 |
| Lot Frontage | feet of street connected | yes | float, 489 missing (16.8%; 49% of CulDSac lots): no-frontage or not recorded, codebook silent; left missing | fine (question, low) | CLEAN-2, CLEAN-10 |
| Lot Area | lot size sq ft | yes | int, 1,300-215,245 | fine | |
| Street, Alley | road / alley access | yes | category; Alley "NA" -> "No alley access" | fine | CLEAN-10 |
| Lot Shape, Land Contour, Lot Config, Land Slope | lot shape, flatness, configuration, slope | yes | category (Lot Shape, Land Slope ordinal as nominal) | fine | CLEAN-14 |
| Utilities | utilities available | yes | category, 2,916 AllPub, 3 others | fine (near constant, not constant) | CLEAN-5 |
| Neighborhood | location within Ames (28) | yes | category; Landmrk, GrnHill only in 2006-07 | fine | |
| Condition 1, Condition 2 | proximity to road/rail/park | yes | category | fine | |
| Bldg Type | dwelling type | yes | category; data `2fmCon`, `Duplex`, `Twnhs` vs doc `2FmCon`, `Duplx`, `TwnhsI` (harmless) | fine | |
| House Style | style of dwelling | yes | category | fine | |
| Overall Qual, Overall Cond | 1-10 grades of material/finish and condition | yes (as at sale; see above) | int; Overall Cond = 5 for 323 of 332 houses at most 1 year old (assessor default) | fine | CLEAN-14 |
| Year Built | original construction year | yes (never after sale) | int 1872-2010 | fine | |
| Year Remod/Add | remodel year (= Year Built if none) | yes, except row 937 (2008 > sale 2007) | int; floor 1950 for 337 of 629 pre-1950 houses (censored, documented); row 2032 remod 2001 < built 2002 (impossible) | leak (1 row, negligible) + cleaning (1 row) | LEAK-10, CLEAN-11, CLEAN-10 |
| Roof Style, Roof Matl | roof type, material | yes | category | fine | |
| Exterior 1st | exterior covering | yes | category, documented codes | fine | |
| Exterior 2nd | second covering | yes | category; 225 rows use `Brk Cmn` (21), `CmentBd` (124), `Wd Shng` (80) where the codebook and Exterior 1st use `BrkComm`, `CemntBd`, `WdShing` | cleaning problem (low) | CLEAN-1, CLEAN-12 |
| Mas Vnr Type, Mas Vnr Area | masonry veneer type, area | yes | category ("None" is a documented level) + float; 23 empty in both (missing); 7 rows "None" with area 1-344 (three at 1 sq ft), 3 rows a type with area 0 | fine, inconsistencies noted | CLEAN-11 |
| Exter Qual, Exter Cond | exterior material quality, present condition | yes | category, Ex/Gd/TA/Fa/Po as nominal | fine (ordinal question) | CLEAN-14 |
| Foundation | foundation type | yes | category | fine | |
| Bsmt Qual, Bsmt Cond, Bsmt Exposure, BsmtFin Type 1, BsmtFin Type 2 | basement grades and finish types | yes | category; "NA" -> "No basement" anchored on Bsmt Qual (78); 1 row all-empty (missing); Bsmt Exposure 3 empties with a basement, BsmtFin Type 2 1 empty with SF2 479 (missing, correct) | fine | CLEAN-10 |
| BsmtFin SF 1, BsmtFin SF 2, Bsmt Unf SF, Total Bsmt SF | basement areas | yes | float; Total = sum of parts in every non-missing row (kept as published); 1 BsmtFin Type 2 "Unf" with SF2 > 0 | fine | CLEAN-5 (a sum, not a copy) |
| Heating, Heating QC, Central Air, Electrical | heating type and grade, A/C, electrical | yes | category; Electrical 1 empty (missing) | fine | |
| 1st Flr SF, 2nd Flr SF, Low Qual Fin SF, Gr Liv Area | floor areas | yes | int; Gr Liv Area = 1st + 2nd + Low Qual in 100% of rows (kept as published) | fine | CLEAN-5 |
| Bsmt Full Bath, Bsmt Half Bath | basement baths | yes | float; 2 missing (row 1466 all-empty basement; row 1711 has no basement, structurally 0, left missing) | fine | CLEAN-2 |
| Full Bath, Half Bath, Bedroom AbvGr, TotRms AbvGrd | above-grade rooms | yes | int; 12 with 0 full baths above grade, 8 with 0 bedrooms (plausible) | fine | |
| Kitchen AbvGr, Kitchen Qual | kitchens above grade and their grade | yes | int + category; 3 rows with 0 kitchens and Kitchen Qual "TA" (contradiction) | cleaning note | CLEAN-11 |
| Functional | home functionality deductions | yes | category | fine | |
| Fireplaces, Fireplace Qu | count and grade | yes | int + category, "No fireplace" exactly where Fireplaces = 0 | fine | |
| Garage Type, Garage Finish, Garage Qual, Garage Cond | garage location, finish, grades | yes | category; "NA" -> "No garage" anchored on Garage Type (156); two Detchd garages with "NA"/empty details -> missing | fine | CLEAN-10 |
| Garage Yr Blt | garage build year | yes (never after sale) | float; 159 missing (156 no garage + 2 detached + the 2207 typo set missing); 18 garages older than the house (plausible) | fine | CLEAN-11 |
| Garage Cars, Garage Area | capacity, area | yes | float; 1 missing (row 692) | fine | |
| Paved Drive | paved driveway | yes | category | fine | |
| Wood Deck SF, Open Porch SF, Enclosed Porch, 3Ssn Porch, Screen Porch | deck and porch areas | yes | int | fine | |
| Pool Area, Pool QC | pool area and grade | yes | int + category, consistent ("No pool" iff area 0) | fine | |
| Fence | fence quality | yes | category, "No fence" | fine | |
| Misc Feature, Misc Val | other feature and its $ value | yes | category ("None") + int; consistent (3 features valued 0) | fine | |
| Sale Type | deed / sale type | yes, at the sale (closing terms are set before) | category, "WD " stripped | fine | LEAK-37 / USE-6 |
| Sale Condition | normal, abnormal, family, partial, allocation, adjoining land | yes, at the sale | category; New (236) nearly nests in Partial (242) | fine; dropping costs +0.0047 RMSE (REVIEW_before) | LEAK-37 / USE-6 |
| Month Sold | sale month (from Yr Sold, Mo Sold) | yes (the prediction point) | datetime `%Y%m`, time column | fine | CLEAN-12 |
| log_SalePrice | ln(SalePrice $) | target | float 9.46-13.53, no cap | fine | CLEAN-16, LEAK-26 |
| Order (dropped) | row number | - | encodes the sale year in reverse (corr -0.976; Order 1-341 = 2010) | drop correct | CLEAN-3, LEAK-10 |
| PID (dropped) | parcel number | - | township (05/09) + section (27) + block (679) + parcel: a location; adding section, or section and block, as categories: LightGBM RMSE -0.0001 (SE 0.0007) / -0.0005 (SE 0.0005), 13 windows x 3 seeds | drop fine; meaning not worth keeping | CLEAN-3 |

**Problems, ranked by principles.md**

1. **P4, LEAK-10 (weak, 1 row).** Row 937: `Year Remod/Add` 2008 for a Partial sale in June 2007 (built 2007), a
   value recorded after the sale. The rest of the file passes the as-at-sale test (above). Mildest remedy: a sentence in
   the notes; or set this one value to missing (or to `Year Built`). Curation comment bullet "no house built two or
   more years before its sale has a remodel year after it" is true, and could add "one new house has (2008, sold 2007)".
2. **P7, CLEAN-12 / CLEAN-1 (low).** `Exterior 2nd` spells three materials differently from the codebook and from
   `Exterior 1st` in 225 rows (`Brk Cmn`, `CmentBd`, `Wd Shng`). Remedy: map them to `BrkComm`, `CemntBd`, `WdShing`
   (the 1st/2nd match then rises from 85.0% to about 90.7%). The other code-vs-codebook differences (Bldg Type, MS
   Zoning) are harmless spellings; optional.
3. **P7, CLEAN-11 (low, tiny counts).** Contradictions kept as published: `Year Remod/Add` 2001 < `Year Built` 2002
   (row 2032; impossible by the codebook's definition), 3 rows with 0 kitchens and a kitchen grade, 7 "None" veneers
   with an area (three at 1 sq ft) and 3 veneers with area 0, 1 unfinished BsmtFin Type 2 with finished area. Remedy:
   keep with one note line; at most set row 2032's remodel year to missing.
4. **Question, CLEAN-14.** The 21 text ordinals (Ex/Gd/TA/Fa/Po and the like) are unordered categories while
   `Overall Qual`/`Overall Cond` are integers; the package has only unordered categories, and the dataset's name
   ("nominal") follows OpenML's choice. Keep; the curator may prefer integer grades for the Ex-Po scales.
5. **Notes, no action.** `Year Remod/Add` floor 1950 (CLEAN-10, documented censoring, kept). `Lot Frontage` 16.8%
   missing, not explained by the codebook (left missing, CLEAN-2). PID dropped although it encodes location; measured
   no gain (CLEAN-3). `Order` encodes the sale year and must stay dropped. Grades possibly revised at sales
   verification: unknowable, no evidence.

No column predicts from after the sale beyond row 937; no id encodes the label; no all-row statistics (LEAK-29) in the
cleaning.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** Temporal, 13 expanding two-month windows, no gap. SPLIT-1, SPLIT-2, SPLIT-3, SPLIT-6,
SPLIT-9, SPLIT-11, SPLIT-14, SPLIT-15, SPLIT-17 hold. No Must is broken; three notes (all Should/Weigh, P4), none needs
a change to the definition.

Data: container rebuilt from the definition (`dataset_io.load(..., built=False)`, origin `rebuilt`), 2,919 rows, 79
columns; raw `AmesHousing.txt` for the checks on dropped columns. Scripts and pickles: (run folder) (windows.py,
models.py). Thread caps on every run.

**Regime against the use case**

* Use case: an automated valuation (lender / valuation service) of a house at its sale, refit every two months. The
  stream of sales over time makes it temporal (SPLIT-6: "a sale price" is the rule's own example). Declared temporal on
  `Month Sold`: matches.
* Entity: the house (parcel). `PID` is unique in all 2,930 raw rows, because De Cock kept only the latest sale of a
  home sold more than once. No house recurs, so the cold-start / known-entity question (USE-10, SPLIT-13) does not arise:
  every test house is new to the model by construction. A real AVM would see the house's earlier sale; the data cannot
  offer that (note 3).
* Hidden-group probe: only `Neighborhood` is entity-like (28 values, 100% of test rows seen); it is a feature every new
  sale keeps (SPLIT-4), not a group. Composite keys: none (best 0.2%). Near copies at 0.85: 2.5% of rows, 0.9% of test
  rows with a copy in train (0.0-3.1%). Allocation / adjoining-land blocks sell in one month and so share a window. No
  grouping is called for.

**Temporal checks (measured)**

* Time column: `Month Sold` = `Yr Sold`*100 + `Mo Sold`, the month of the sale (no day in the file). Parsed as
  datetime `%Y%m`.
* Windows (newest first): 2010-05/06 161, 03/04 120, 01/02 52; 2009-11/12 58, 09/10 98, 07/08 172, 05/06 181, 03/04 93,
  01/02 46; 2008-11/12 61, 09/10 65, 07/08 152, 05/06 191. Train side 94.5% down to 50.3% (SPLIT-14 holds, 13 >= 3
  windows). Every split: no overlap, max train month < min test month, 0 training rows after the window. Expanding
  train from 2006-01 (SPLIT-11).
* Size: winter windows hold 46-61 rows, at the ~50 floor of SPLIT-17; monthly windows would go to 19. Two months is the
  right width; three months (8 windows of 91-233) is the alternative if the curator wants steadier windows.
* Season: the 13 windows tile the calendar (Jan-Feb, Mar-Apr, May-Jun x3; Jul-Aug, Sep-Oct, Nov-Dec x2). Mean log
  price by calendar month lies within 11.96-12.06, so no window is an atypical season (SPLIT-20 holds).
* Label delay and gap: the price is the sale's own price, known when the deed is recorded, so SPLIT-9 holds with no
  gap. Re-measured the alternative prediction point (purchase agreement, one or two months earlier): LightGBM (500
  trees, 3 seeds, paired per window) RMSE +0.0004 (SE 0.0006, worse in 8/13) for a 1-month gap and +0.0017 (SE 0.0009,
  8/13) for 2 months, against 0.1163 with no gap. The definition's +0.0006 / +0.0026 are of the same size: confirmed.
* Features after the prediction point (LEAK-10 as it touches the split): `Year Remod/Add` > `Yr Sold` in 3 raw rows, all
  new Partial sales of 2007 (house finished after the contract); `Year Built` > `Yr Sold` in 1 (same kind). Among houses
  built two or more years before the sale, a remodel in or after the sale year occurs in 1/512 (2006), 7/581 (2007),
  3/573, 2/604, 1/325: no rise for the oldest sales, so the record is the house at the sale, not a 2010 snapshot. All
  these rows are 2007 sales, training only.
* Training history (SPLIT-20): 2006-01 onward, all kept. Mean log price by year 12.023, 12.048, 12.013, 12.022, 11.980
  (2010 half year): no break. Partial (new-house) sales fall from 86-90 a year in 2006-07 to 27-29 in 2008-09 and 13 in
  the 2010 half year: the new-construction slump, a shift the expanding window carries; no reason to cut history.

**Alternative split (quick models, untuned)**

| split | LightGBM RMSE | ridge RMSE |
|---|---|---|
| shipped temporal, 13 windows | 0.1165 (SE 0.0064) | 0.1236 (SE 0.0092) |
| random 3x10 KFold | 0.1115 (SE 0.0027) | 0.1197 (SE 0.0032) |
| random, same train/test sizes as the 13 windows | 0.1097 | 0.1139 |

A random split is 0.005-0.010 RMSE more optimistic. Small, and the split follows the use case, not the gap
(SPLIT-4): temporal stays. Per-window LightGBM RMSE 0.090-0.158; the worst are 2010-05/06 (0.158), 2009-11/12 (0.153),
2010-01/02 (0.143).

**Problems, ranked (all P4)**

1. **Newest window: June 2010 is thin and its error comes from non-market sales (SPLIT-20, Should; LEAK-24 checked, not
   triggered).** June 2010 has 82 sales against 97-112 in June 2006-09 (May 2010: 79, within 69-89), and smaller houses
   (median `Gr Liv Area` 1,368 against 1,416-1,512). In the newest window (3 LightGBM seeds) June's RMSE is 0.201
   against May's 0.087, but for the 73 Normal June sales the mean residual is -0.001 and RMSE 0.105: the excess sits in
   9 non-Normal sales (2 Alloca, 3 Abnorml, 4 Partial). So it is not a price-censoring of late-recorded sales; the low
   count may be recording lag before the extract or the end of the first-time-buyer credit (closing deadline June
   2010). Remedy: none needed; keep the note in REVIEW item 6. Mildest change if the curator doubts June's completeness:
   end the data at May 2010 (windows shift by one month).
2. **Winter windows at the size floor (SPLIT-17, Should).** 46, 52, 58, 61 test rows; they also carry three of the four
   highest RMSEs. Within the rule; three-month windows (8 windows, 91-233 rows, already in the decision table) are the
   alternative. Curator's call on width (REVIEW item 2); not a defect.
3. **Repeat sales removed by the source (SPLIT-13, USE-10, Weigh; also P5).** De Cock kept only the latest sale of a
   resold home, so the training side (older months) under-represents frequently traded houses, and the model never sees
   a house's previous price, which a real AVM uses. Every test house is a cold start by construction; this matches the
   task as shipped but understates what a deployed model knows. The "about 100 missing sales" figure was not
   re-measured (yearly counts 625 / 692 / 621 / 648 show no visible deficit in 2006). Remedy: a note (already in
   `curation_comments` and `fit_reason`).
4. **Prediction point wording (USE, Weigh).** A lender values the house before closing (appraisal), slightly earlier
   than "a house sells". Measured cost of a 1-2 month gap is within noise (above), so no gap is needed; the
   `splits_comment` already states it.

Not problems: the IID Kaggle split the record links (SPLIT-5: correctly replaced); hidden groups (none beyond
`Neighborhood`, a feature); the outlier drop (all five >4,000 sq ft sales are before the oldest window, train only).

</details>

<details><summary>Domain practitioner</summary>

I read `dataset.py` (`task_summary`, `curation_comments`, `splits_comment`), the record, `claims.md`, the task probe
output, REVIEW_before.md, De Cock (2011), the AmesHousing R package's documentation and Iowa Code 428.4. Who I am in
this review: first a residential appraiser at the Ames City Assessor's Office (the actor whose data this is), then
the actor the definition names, a lender's or valuation service's AVM analyst. Scratch:
(run folder) (the paper's text extracted from the JSE PDF).

**Fit**

**Direct.** As the assessor's mass-appraisal model, the rows (arm's-length and other residential sales), the
inputs (the characteristics the assessor keeps on file to compute assessed values) and the forward-in-time windows
match how sales are used to value homes. As the lender's AVM the definition names, the fit is only approximate: the
analyst would always have exact location, the previous sale price and the assessed value, and none of them is here.
The data's own actor makes the fit direct (USE-1, take the use case from the source; USE-9). Because this actor is the
source's and not a rewording invented to excuse a gap, the factor against rewording does not apply.

**1. Inputs at the prediction point (USE-3, USE-6)**

As the assessor, valuing a home on 1 January of a reassessment year, or checking last month's sales:
- I have every column. The 80 variables are the assessor's own property record. De Cock removed the variables "that
  required special knowledge or previous calculations", i.e. the city's own weighting and adjustment factors and the
  assessed values (paper, section 1). For the assessor the assessed value is the output, not an input, so its absence
  is right for my use.
- `Sale Type` and `Sale Condition` exist at the sale. The assessor gets them from the transfer declaration and uses
  them to qualify sales. A lender knows them at the contract. Keeping them is correct (USE-6).
- `Month Sold` is known.
- **The open risk is when the record was taken.** De Cock received the file while the office was "updating the
  assessment" (about 2010). It is the record as of the extract, not a snapshot at each sale. Assessors review sold
  properties after a sale ("sales verification"). If a grade (`Overall Qual`, `Kitchen Qual`, conditions) was revised
  after the sale, the record of a sold house is better informed than the one a model would see before it. The
  definition's check, that no remodel year falls after the sale, covers one variable only. The quality grades cannot
  be checked from this file. So `fit_reason`'s "The record describes the house at the sale" claims more than the
  evidence shows. I would write "the record is the assessor's file of about 2010; no remodel year postdates its sale"
  (USE-3).

What the AVM analyst would always have and is missing here (ranked):
1. Exact location. `PID` can be geocoded (De Cock points to the Beacon GIS by PID). The AmesHousing R package ships
   approximate `Longitude`/`Latitude` per PID in `ames_geo`. The definition drops `PID` as "unique per row". An AVM
   values a home from comparable sales by distance, and `Neighborhood` (28 levels) is a coarse stand-in. An assessor's
   CAMA model also works by neighbourhood, so for the assessor this gap is small.
2. The previous sale price of the same home. About 100 homes sold more than once, and De Cock kept only the latest
   sale (p. 4). For a known entity this is a legitimate and strong input (USE-10), and the data cannot recover it.
   Assessors may not use a home's own sale price to set its value ("sales chasing", IAAO), so this gap is again the
   lender's, not the assessor's.
3. The current assessed value: a standard AVM input, removed by De Cock.
4. The list price, for a valuation service working on listed homes. It is not in an assessor file.

**2. Target (USE-5)**

The sale price is what both actors act on. The assessor targets market value, and qualified sales are the standard
proxy for it. The lender wants the collateral value, and for a purchase loan the contract price is that value. The
log price with RMSE comes close to the relative error both actors measure. In practice they report the median absolute
percentage error and the share within 10% (AVM), or the median ratio, COD and PRD (assessor). A point estimate is the
right output. A practitioner would also want a confidence band (the AVM's "forecast standard deviation"), which a
benchmark of point RMSE does not ask for. Acceptable.

One caveat for the lender framing: at purchase origination the lender already knows the contract price, so it does not
predict the price. It validates the price, or values homes with no sale (refinance, HELOC, portfolio monitoring), and
in those cases `Sale Type`/`Sale Condition` do not exist. "A valuation service estimates the sale price of a house
about to sell" or "the assessor values homes from recent sales" both avoid this.

**3. Row and test data (USE-8, USE-10)**

- One row is one sale, as one valuation in a ratio study or one AVM call is: matches.
- The test is the next two months of sales after all earlier ones. The assessor revalues every two years (Iowa Code
  428.4: as of 1 January of each odd year, with even-year corrections) and calibrates on the sales of the past one or
  two years. The AVM vendor refits monthly or more often. Two-month windows lie between the two. The windows are a
  benchmark choice (USE-8 needs the split to follow time, which it does), and the gap test in `splits_comment`
  (+0.0026 RMSE for two months) shows the cadence hardly matters. No change needed.
- Each property appears once, so every test home is new to the model. In reality about 3% of homes would carry an
  earlier sale (point 2 above). This is small, and De Cock's own choice.
- Population: of the 1,450 sales in the test windows (May 2008 to June 2010, computed from AmesHousing.txt), 1,264 are
  Normal, 58 Partial (new homes), 94 Abnorml (foreclosures, short sales: real market sales in 2008-2010, which AVMs
  must value), 17 Family, 15 Alloca and 2 AdjLand. An assessor's ratio study and an AVM accuracy test both exclude
  sales that are not arm's-length (family transfers, adjoining-land purchases, allocations of a joint price). These 34
  rows (2.3%) are scored here. REVIEW_before issue 7 shows two allocation sales alone move the newest window's RMSE from
  0.145 to 0.157.

**4. Would I use this model?**

As the Ames assessor: yes, as a cross-check of a CAMA model. These are my own variables and my own sales, and a
learned model reaching R² 0.90 (log RMSE 0.12, about 12% typical error) is close to what an assessor hopes for. IAAO's
target COD for single-family homes is about 5-15. What I would distrust:
- quality grades possibly updated after the sale, the unverifiable timing above;
- 2,900 sales in one college town, so thin cells (28 neighbourhoods, few sales per neighbourhood per window);
- the late-June 2010 drop (REVIEW_before issue 6), which looks like recording lag before the extract. A model scored
  on the newest window would look worse there for reasons unrelated to it.

As a lender's AVM analyst: no. Without coordinates, prior sales or the assessed value, the inputs are those of a
listing flyer, and one city with 50-190 sales a window is far below what a commercial AVM trains on.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. **The actor (USE-1, USE-9).** The lender/valuation-service framing makes the missing location, prior sale and
   assessed value real gaps (an approximate fit). The source's own actor, the assessor valuing homes from recent
   sales, has exactly these inputs and makes the fit direct. This changes the reading of the task, not the data.
2. **When the record was taken (USE-3).** The file is the assessor's record of about 2010, possibly revised after
   each sale. It cannot be checked beyond the remodel year. The fit_reason overstates it.
3. **Sales that are not arm's-length in test (USE-5).** 34 of 1,450 test rows (Family, Alloca, AdjLand) are prices no
   valuation decision targets. They are kept as a feature-flagged population and they move window scores.
4. **Missing location coordinates (USE-6).** The coordinates exist upstream (PID, `ames_geo`). This matters for the
   AVM actor and little for the assessor.
5. **Repeat sales removed by De Cock (USE-10).** About 100 earlier sales are missing, along with the prior-price
   input. The definition already names it as an anomaly. Small.

**What an expert would change**

- Write the use case as the source's actor: "For example, a city assessor values residential properties from recent
  sales, with a model refit as new sales arrive". Or keep the valuation service but drop the lender, because a
  purchase lender knows the price. Keep `fit = direct` under that actor (USE-1, USE-9).
- Soften `fit_reason` and the curation bullet "The records describe the house at the sale" to what was checked: the
  assessor's file of about 2010, in which no remodel postdates the sale (USE-3).
- Consider dropping the sales that are not arm's-length (`Sale Condition` in Family, Alloca, AdjLand: 82 rows in the
  whole file before the outlier drop, 34 in the test windows), as an assessor's ratio study or an AVM test
  would. Keep Abnorml: foreclosures are market sales the model must value. This is the curator's choice, and keeping
  them as a feature is defensible (REVIEW_before issue 7 already offers the Alloca part).
- Optional, not required: join approximate coordinates from AmesHousing's `ames_geo` on `PID` (GPL-2 R package,
  approximate geotags, some PIDs updated). This would bring the task closer to an AVM. It brings in a second source
  and a licence question, so I would only note it.
- No change to the target, the windows or the outlier rule: the three partial-sale outliers are non-market prices an
  assessor would also disqualify, and they only train.

**Sources**

- De Cock (2011), JSE 19(3), https://jse.amstat.org/v19n3/decock.pdf (data origin, removed variables, repeat sales,
  outliers; text extracted to (run folder)), doi:10.1080/10691898.2011.11889627
- DataDocumentation.txt, https://jse.amstat.org/v19n3/decock/DataDocumentation.txt
- AmesHousing R package manual (`ames_geo`: PID, approximate Longitude/Latitude),
  https://cran.r-project.org/web/packages/AmesHousing/refman/AmesHousing.html
- Iowa Code 428.4 (reassessment as of 1 January of odd years), https://www.legis.iowa.gov/docs/code/2023/428.4.pdf
- Sales chasing and ratio-study tests (IAAO 2013 standard, as applied by Washington DOR),
  https://propertytax.dor.wa.gov/node/2331; sale qualification (arm's length), Buncombe County Sales Disqualification
  Study, https://www.buncombecounty.org/common/tax/Sales%20Disqualification%20Study.pdf
- Measured here: Sale Condition counts in the test windows (May 2008 to June 2010) from
  (run folder); probe output (run folder).

</details>

<details><summary>Blind review</summary>

**Verdict**
Include with changes: this is real, well-understood residential appraisal data with strong but not trivial signal and no leaking columns. The changes are to document where the rows come from, and to state that the dataset is heavily over-studied.

**The task**
Predict the log sale price of a residential property in Ames, Iowa, from assessor records (sales from 2006-01 to 2010-06). The users are mass appraisal and tax assessment, automated valuation for lenders, and pricing at listing. This is a real and common use. Kaggle scores it as RMSE on log price, which matches this target.

**Concerns, most serious first**

1. **Where the rows come from is unclear, and the row count does not match the cited sources.**
   - OpenML 42165 is the Kaggle training file, with 1,460 rows. Kaggle's test labels are not public.
   - This table has 2,919 rows, all labelled. That equals Kaggle train + test (1460 + 1459), yet the column names ("Gr Liv Area", "Year Remod/Add") and the levels ("No alley access", "No pool", the long MS SubClass labels) follow De Cock's full Ames file (2,930 rows) as recoded by the R AmesHousing package.
   - So 11 rows were dropped. Among them are the three well-known partial-sale outliers above 4,000 sq ft (Gr Liv Area 4676, 5095 and 5642). Here the maximum is 4,476 and only 2 houses are above 4,000; De Cock lists 5.
   - Dropping the hardest rows makes the task slightly easier.
   - The known Garage Yr Blt typo (2207) is also absent: the maximum is 2010.
   - Change: cite De Cock (2011) / AmesHousing as the actual source, and document which rows were removed and why.
2. **The dataset is heavily over-studied.** It is among the most-used tabular regression sets (Kaggle, tidymodels, textbooks).
   - Tuned pipelines and pretrained or LLM-based models may have seen it.
   - Its value as a fresh benchmark task is limited. Keep it only if this exposure is acceptable.
3. **The temporal split adds little but is harmless.**
   - Year means of the target are flat: 12.02, 12.04, 12.02, 12.03, 11.98.
   - Sale volume is seasonal: 18 to 122 rows per month.
   - The task is really cross-sectional appraisal. A time-ordered split is defensible because it mimics valuing future sales.
   - I could not check the 13 window boundaries. The last windows cover only 2010 (333 rows in Jan to Jun), so check that each test window has enough rows, at least about 100.
4. **Leakage check: none found.**
   - Every feature is a property attribute known before the sale.
   - Sale Type and Sale Condition are known at contract time. "Partial" (a new build) and "Abnorml" (foreclosure or short sale) are legitimate pricing information.
   - Mo Sold and Yr Sold are merged into the datetime `Month Sold`. Remove it from the features or encode it ordinally, so that a model cannot memorise the window.
   - The PID and Order columns are absent, which is good.
5. **Copies across rows:** 2 pairs of rows have identical features but different prices (11.78/11.81 and 11.92/11.90). These are probably townhouse units in the same development. This is negligible and needs no action.
6. **Preparation is minor and acceptable.**
   - All the quality and condition ratings (Exter Qual, Bsmt Qual, Kitchen Qual and others) are nominal categories. The ordinal order Po<Fa<TA<Gd<Ex is lost, which is consistent with the name "nominal".
   - Missing values are mixed: structural absence is coded as a level ("No garage", "No basement"), while real gaps stay NaN (Lot Frontage 489, Garage Yr Blt 159, Mas Vnr Type/Area 23, a few single basement and garage cells). This is sensible.
   - Utilities is almost constant (2916 AllPub), and so is Pool QC (2907 "No pool"). These are harmless.

**Signal and difficulty**
- I trained LightGBM on 2006 to 2008 and tested on 2009 to 2010 (1,911 / 1,008 rows).
- RMSE was 0.127 against 0.415 for predicting the training mean, which gives R2 0.91.
- One feature alone does much worse: Overall Qual gives RMSE 0.233 and Gr Liv Area gives 0.305.
- So the signal is strong but not trivial, and models should still separate, mostly on the categorical and outlier handling.
- 2,919 rows is small but adequate to score.

**Plausibility**
- Prices run from 12,789 to 755,000 USD, with median 160,000.
- Living area runs from 334 to 4,476 sq ft. Years are coherent: Garage Yr Blt is at most 2010.
- This is real data, not generated.

**What I could not check**
- The OpenML API returned errors (HTTP 412 and a database connection error), so I could not read the metadata of 42165 or of any "house_prices_nominal" entry.
- I could not identify the 8 removed rows beyond the 3 outliers.
- I could not see the exact boundaries of the 13 test windows.

</details>

<details><summary>Precedent check</summary>

Scope: the choices of `datasets/_dev/tabarena-v0pt2/house_prices_nominal/dataset.py`, the record's CC line
(`curation/records/house_prices_nominal.md`) and issues 1-8 of `REVIEW_before.md`.

Register ((run folder), `register.json`): of its 4 flags, only `mechanism: probe flag one_feature` touches a
house-price dataset (california_house_prices_2020, kept 2026-10-06). No flag names house_prices_nominal. The record has
only one curator decision, an undated CC, so there is no drift on this record and no third exception from it (see
decision 7 for the third row drop of the same kind across the repository).

Status of the precedents: the curator decisions are CC lines. hr_analytics (CC 2026-10-14),
california_house_prices_2020 (CC 2026-09-30, 2026-10-06, 2026-10-14) and sberbank_housing_market_forecasting (CC
2026-10-14) are curator decisions. house_sales, zillow_prize, melbourne_housing_market, perth_house_prices and
stroke_prediction are AI drafts with open REVIEW.md issues. house_sales was checked today ((run folder))
and its gap and last-month questions are the same as here. perth_house_prices (issue 7) cites house_prices_nominal as
its precedent for "no gap", so the answer here carries over to the family.

Measured here (raw AmesHousing.txt): sales per month 2006-2010 (June: 97/106/108/112 then 82 in 2010; April 2010: 72
against 48-61; July 2010: 8). PID is 10 digits: its first 6 digits take 227 values, and 94.5% of the rows share their
6-digit prefix's most common neighbourhood (4 digits: 27 values, 64.9%).

**Summary**

| # | Decision | Rule | Result |
|---|---|---|---|
| 1 | De Cock's full file instead of the record's Kaggle half; record name kept (issue 1) | PROV-8, PROV-9, PROV-14, PROV-4 | consistent (hr_analytics) |
| 2 | Temporal split instead of Kaggle's random split (the CC) | SPLIT-19, SPLIT-5 | consistent: follows the CC |
| 3 | Two-month windows, 13 windows (issue 2) | SPLIT-12, SPLIT-14, SPLIT-15, SPLIT-17 | consistent; family call open |
| 4 | Proposal to drop the `Trivial` marker (issue 3) | TP-4 | consistent (california_house_prices_2020, aps_failure, sepsis) |
| 5 | Prediction point "a house sells", `Sale Type`/`Sale Condition`/`Month Sold` kept (issue 4) | USE-3, LEAK-10 | consistent (house_sales, zillow_prize) |
| 6 | No gap between train and test | SPLIT-10 | departs; the stated reason does not match the data |
| 7 | De Cock's 3 partial-sale outliers dropped (issue 5) | CLEAN-1, CLEAN-11 | departs from CLEAN-11 with a stated reason (reasonable); third drop of its kind |
| 8 | July 2010 dropped | (last-period cut; no numbered rule) | consistent (house_sales, zillow_prize) |
| 9 | June 2010 kept (issue 6) | (last-period cut), EV-2 | departs from both sibling reasons, no distinguishing fact |
| 10 | Allocation and adjoining-land sales kept (issue 7) | CLEAN-1, LEAK-20 | consistent, with a fact that sets them apart from decision 7 |
| 11 | Two feature-equal parcel pairs with different prices kept | LEAK-16, LEAK-20 | consistent (zillow_prize, house_sales) |
| 12 | "NA" levels written out, `Garage Yr Blt` 2207 to missing, `MS SubClass` labels, `Sale Type` stripped | CLEAN-10, CLEAN-11, CLEAN-12 | consistent |
| 13 | The other 43 text-coded columns keep the source's codes, "as in OpenML's house_prices_nominal" | CLEAN-12; EV-4/PROV-15 case | departs; the stated reason is one the rules call no evidence |
| 14 | `Year Remod/Add` 1950 floor kept as recorded | CLEAN-10, CLEAN-11 | consistent |
| 15 | `PID` dropped as "unique per row" | CLEAN-3 | departs without a reason: the parcel number encodes the block |
| 16 | `Order` dropped; log target, RMSE | CLEAN-3, CLEAN-16 | consistent |
| 17 | `fit = "direct"` with about 100 older sales missing (latest sale only) | USE-8 | consistent (melbourne_housing_market) |
| 18 | `source` Other, `year` 2011, bibtex De Cock (2011) | PROV-8, PROV-9, PROV-10 | consistent (hr_analytics, airfoil_self_noise) |
| 19 | JSE licence as a note only (issue 8) | selection.md licence rule; EV-4 | consistent (lucas_topsoil, Lennart 2026-09-23) |
| 20 | Temporal only, `Spatial` as a tag | SPLIT-3, USE-10 | consistent (tension row, Lennart 2026-10-12) |

**Per decision**

**1. De Cock's full file instead of the Kaggle half, record name kept: consistent**

PROV-8 (Must): the source is the first publication. The Kaggle competition (2016) is a random half of De Cock's JSE
file (2011), so De Cock is the source and the definition follows PROV-8 and PROV-9 (year 2011). PROV-14 (a rebuild that
does not match the release is a new record) does not apply: under PROV-8 the release is De Cock's file, and the
definition uses it as published.

Closest curator precedent: hr_analytics (CC 2026-10-14, Lennart): "Build from the hackathon's public train file ...
source Other, the contest page, year 2018". The record kept its name and its `source_links` gained the contest page.
stroke_prediction (AI draft, 2026-10-07) follows the same pattern ("the contest's whole training file instead of the
Kaggle cut", same record name). So:

* Adding the JSE file and the DOI to `source_links` (REVIEW issue 1) is what hr_analytics did. Follow it.
* Keeping the name `house_prices_nominal` is what hr_analytics did. A rename to `ames_housing` has no precedent in a
  source swap. It is a choice, not a consistency point.
* `ames_housing_dataset` (`Duplicate`, "Version of" the Kaggle competition) is the cell-for-cell mirror of the file used
  now. PROV-4 is met: the data enters once.

**2. Temporal split instead of Kaggle's random split (the CC): consistent**

The CC (undated) calls the Kaggle split "gap-filling ... of questional relevance". SPLIT-19 follows a split only when the
source defines it. De Cock defines none, and Kaggle's random half is a claim checked under SPLIT-5. The definition does
what the CC asks. The CC's "1460 samples" is superseded by the source change (decision 1).

**3. Two-month windows (issue 2): consistent; family call open**

SPLIT-15 would give 30 windows (10 x 3). SPLIT-14 (Must, train side >= 50%) stops the windows at 13 (oldest train side
50.3%). SPLIT-17 widens months of 19 sales to two months of at least 46. That follows coffee_rating_prediction.
SPLIT-12 wants the horizon from the source, and De Cock gives none. Among the siblings, only zillow_prize's window comes
from its source; the others are size-driven or conventions:

| Dataset | Window |
|---|---|
| house_sales | 3 weeks |
| perth_house_prices | 1 month |
| zillow_prize | 1 month + gap |
| melbourne_housing_market | 3 weekly sheets |
| house_prices_nominal | 2 months |

None of these is a curator decision yet. This is not a departure. As with house_sales, the curator may want to settle
the family together.

**4. Proposal to drop `Trivial` (issue 3): consistent**

TP-4 (Must): `Trivial` needs a single raw feature, chosen per training side, that matches or beats the methods fold by
fold. Here `Overall Qual` reaches R² 0.682-0.685 against 0.90-0.91 and loses in 13 of 13 windows. The curator
precedents are:

* california_house_prices_2020 (CC 2026-10-06, Lennart): kept. The listed price gives R² 0.89-0.91 against 0.93, a far
  narrower margin than here.
* aps_failure (CC 2026-10-06): kept.
* sepsis_survival (CC 2026-10-06): kept.
* fitness_club (CC 2026-10-05): retired. Its single feature beat all 37 configurations. That fact does not hold here.

The marker is undated and has no reason on the record. Lennart's early uses of `Trivial` were impressions (anneal,
haberman_survival, 2026-07-27: "very simplistic"). The October uses are measured (TP-4). This is the register's
`trivial` opposite-outcomes flag, and it reads as the rule hardening rather than drift. The AI only proposes; the
curator removes the marker.

**5. Prediction point "a house sells" (issue 4): consistent**

This is the same automated-valuation framing as house_sales and zillow_prize. `Sale Type` and `Sale Condition` are
facts of the transaction at the sale (USE-3). No post-outcome lookup was found: no remodel year after the sale for
houses built two or more years before it (LEAK-10).

**6. No gap: departs; the stated reason does not match the data**

SPLIT-10 (Should): when a label is known only some time after its row, train on what is known at the window's start,
with a gap of about the delay. The definition's reason is "A price is known once the sale is recorded". The data shows
that recording lags the sale:

* July 2010 holds 8 sales against 101-122.
* June 2010 holds 82 against 97-112, about 78% of a usual June. The REVIEW (issue 6) itself names "late recording before
  the July 2010 extract" as one explanation.
* April and May 2010 are complete.

So at a refit on 1 May 2010, about a fifth of April would still be missing. This is the mechanism of house_sales
(today's precedents report, decision 4: 24% of May by mid-May, no gap, flagged) and of zillow_prize (one-month gap,
"Zillow receives sales with a delay"; AI draft). perth_house_prices cites house_prices_nominal for "no gap". The cost
is negligible: a one-month gap changes LightGBM RMSE by +0.0006 (SE 0.0010). But the tension row "the right split
against the score" (forest_fires) says the split follows the application, not the size of the effect.

```text
**Consistency check (AI, 2026-10-20):** your call on house_prices_nominal (two-month windows with no gap, a departure
from SPLIT-10) differs from zillow_prize (a one-month gap for the county-recording delay; AI draft), and the file's own
counts show a recording lag (June 2010 at ~78% of a usual June, July 2010 at 8 sales). What sets Ames apart?
(a) the lag affects about a fifth of only the newest month, under half of one two-month window, so the refit loses
little; recorded as an exception with these counts; (b) treat it like zillow_prize: a one-month gap (+0.0006 RMSE,
measured), stated with the task; (c) reopen zillow_prize's gap; (d) amend SPLIT-10 for sale-price tasks (decide with
house_sales and perth_house_prices).
```

**7. De Cock's 3 partial-sale outliers dropped (issue 5): departs from CLEAN-11 with a stated reason**

CLEAN-11 (Should): values that are only unusual stay, and a row leaves only when it is no task row (USE-7) or a copy.
CLEAN-1 (Should, earlier in the file, so it wins at equal strength) adopts "removed anomalies" from the data owners, and
De Cock, the publisher, names these three (p. 4: "Partial Sales that likely don't represent actual market values").

The fact that sets the case apart is stated:

* $28-$40 per sq ft against a median of $150 for partial sales.
* All three are in the training rows only, so the scored task is unchanged.
* The other 242 partial sales stay.

The closest curator precedents point the same way:

* california_house_prices_2020 (CC 2026-10-14, Lennart): drops the 2,480 rows whose listing describes another sale (a
  price that does not belong to the record).
* sberbank_housing_market_forecasting (CC 2026-10-14, Lennart): keeps all 1,124 pre-completion sales. Ames does the same
  for its 242 ordinary partial sales, so there is no clash.
* zillow_prize (AI draft) keeps its extreme logerrors because the competition's test kept them, and they are scored
  rows. That fact does not hold for Ames.

The departure is reasonable, but it is written as a decision, not as an exception. If the curator accepts it, record
it in the exception form:

```text
**Exception to CLEAN-11 (date, curator):** the publisher names the three partial sales as not market values, at a
quarter of the partial-sale price per sq ft, and all sold before the oldest test window. Serves P7 via CLEAN-1.
```

Third of its kind: mercedes_benz_greener_manufacturing ("We remove the one outlier from y") and qsar_tid_11 ("Remove one
negative outlier row") also drop target-outlier rows against CLEAN-11's letter. Both are legacy steps with no recorded
exception; mercedes was kept by Lennart on 2026-10-06 without addressing the step. With Ames this is the third. Per
principles.md, propose an amendment of CLEAN-11 on the next pass: "a row whose target the source names as not the
task's quantity, or a single extreme target in the training period only, may leave, with the source's words". That
pass would also check whether the mercedes and qsar_tid_11 drops meet it.

**8. July 2010 dropped: consistent**

This is a cut by the extract (8 sales against 101-122). It matches house_sales (May 2015 dropped, 24% coverage) and
zillow_prize (August-September 2017 dropped).

**9. June 2010 kept (issue 6): departs from both sibling reasons**

The precedents for a short last month are:

* perth_house_prices (AI draft): December 2020 kept, because it has 0.71 of November's sales and "its prices are in
  line".
* house_sales (AI draft): May 2015 dropped, because it has 24% coverage and the recorded part is price-selected.

Ames June 2010 has the coverage of perth (about 78%) but not perth's reason: its prices are not in line (mean log price
11.931 against 11.985-12.077 in earlier Junes and 12.009 in May 2010). That is the direction of house_sales'
price-selection argument. The definition's reason, "the file cannot tell", names no fact that sets it apart. One
candidate fact is checkable outside the file: the first-time homebuyer credit required a contract by 30 April 2010 and
closing by 30 June 2010, which fits the April surge (72 sales against 48-61) and a cheaper June.

```text
**Consistency check (AI, 2026-10-20):** your call on house_prices_nominal (keep June 2010, ~78% of a usual June and
cheaper) differs from perth_house_prices (December 2020 kept because its prices are in line) and from house_sales (May
2015 dropped because the recorded part is price-selected). What sets June 2010 apart?
(a) the cheaper June is the market, not the recording: the homebuyer tax credit's 30 June 2010 closing deadline
(and its April contract surge) explains it; recorded as an exception with that source; (b) treat it like house_sales:
drop June 2010 (the newest window becomes April-May 2010 ... and the windows shift); (c) reopen perth or house_sales;
(d) write a rule for short last periods (none exists; decide the three together).
```

**10. Allocation and adjoining-land sales kept (issue 7): consistent**

CLEAN-1 says "Keep what a model can learn". The condition is a documented feature, and a block of neighbouring parcels
sold in one month stays in one window, so no copy crosses the split (LEAK-17 does not bite). This differs from
decision 7 by a stated fact: the publisher does not call these sales outliers, they are in the scored windows, and the
model sees `Sale Condition`. zillow_prize (units of one building kept) and house_sales (townhouse pairs) agree.

**11. Feature-equal parcel pairs kept: consistent**

LEAK-20's genuine-ambiguity clause applies: two neighbouring parcels sold in one month, on the same side of every split.
This is the same as zillow_prize (feature-equal units kept) and house_sales (decision 11 there).

**12. "NA" levels, garage-year typo, `MS SubClass` labels, `Sale Type` strip: consistent**

* "NA" levels: CLEAN-10 keeps a code that means something ("NA No Basement" written out). The two "NA" values of
  existing garages become missing, as CLEAN-10 asks.
* Garage year 2207: CLEAN-11, impossible value to missing, row stays (thyroid_discordant `age = 455`).
* `MS SubClass`: CLEAN-12 (codes to labels).

**13. The other 43 text-coded columns keep the source's codes: departs; the reason is no evidence**

CLEAN-12 (Should) reverses ordinal codes into categories with their labels. The definition does this for `MS SubClass`
but keeps the documentation's codes for the 21 ordinal grades (`Ex`, `Gd`, `TA`, `Fa`, `Po`) and the nominal columns
(`RL`, `Norm`, `NAmes`, ...). Its stated reason is "as in OpenML's house_prices_nominal". That is another collection's
version, which the PROV-15/EV-4 case (2026-10-15, Lennart, "another collection's columns or labels are no reference for
ours") rules out as a reason. Precedents that map codes to the source's words:

* credit_g and credit_approval (`A11` codes)
* college_scorecard ("Codes become the data dictionary's labels")
* melbourne_housing_market (Type codes to "house, unit, townhouse")

This is P7 and minor, since the codes are mnemonic and tree models are indifferent. Still, the stated reason has to
change either way.

```text
**Consistency check (AI, 2026-10-20):** your call on house_prices_nominal (43 text-coded columns keep the source's
codes, "as in OpenML's house_prices_nominal", a departure from CLEAN-12) differs from credit_g, college_scorecard and
melbourne_housing_market (codes mapped to the documentation's words) and from the EV-4 case of 2026-10-15 (another
collection's version is no reference). What sets Ames apart?
(a) the codes are readable abbreviations from DataDocumentation.txt that a reader decodes in one lookup, unlike `A11`;
recorded as an exception, with the OpenML reason removed; (b) treat it like the others: map the codes to
DataDocumentation.txt's labels as for `MS SubClass`; (c) reopen the others; (d) amend CLEAN-12 to cover only opaque
codes.
```

**14. `Year Remod/Add` 1950 floor kept: consistent**

The value is a recording floor, not impossible, and CLEAN-11 keeps values that are only unusual. house_sales (decision 8
there) is the one flagged, for turning a documented 0 into missing.

**15. `PID` dropped as "unique per row": departs without a reason**

CLEAN-3 (Should) drops uninformative identifiers but keeps an identifier that carries meaning and processes it into
that meaning. Ames' PID is a 10-digit parcel number. Its first 6 digits take 227 values, and 94.5% of rows share their
prefix's main neighbourhood (measured), so it is a block-level location finer than `Neighborhood` (28 values). The file
has no coordinates.

The siblings that drop parcel ids:

* zillow_prize drops `parcelid` and miami_housing drops `PARCELNO`, but both keep latitude and longitude.
* sberbank drops a row id.

That difference runs against Ames: there the parcel id is the only fine location. The rows are unique per PID, so a
prefix is no entity leak (LEAK-17), and the prefix is no target statistic.

```text
**Consistency check (AI, 2026-10-20):** your call on house_prices_nominal (drop PID as an identifier, CLEAN-3) drops
the only fine location in the file, while zillow_prize and miami_housing dropped their parcel ids only next to
latitude and longitude. What sets Ames apart?
(a) `Neighborhood` (28 values) is the location an Ames assessor's model uses, and the PID's block structure is not
documented in DataDocumentation.txt, so its meaning cannot be cited (PROV-16); recorded as an exception; (b) keep the
block prefix (the first 6 digits) as a categorical location feature, CLEAN-3's "process it into that meaning", with a
probe of its effect; (c) reopen zillow_prize/miami_housing (no: they keep coordinates); (d) amend CLEAN-3.
```

**16. `Order` dropped; log target, RMSE: consistent**

CLEAN-3 drops a row number. CLEAN-16 logs a skewed positive target and names it `log_SalePrice`. RMSE on the log is the
competition's metric and matches house_sales and perth_house_prices.

**17. `fit = "direct"` with about 100 older sales missing: consistent**

The gap affects only training months and is named in `fit_reason`. That matches melbourne_housing_market (before 27 May
2017 only the inner suburbs; all test windows later; `direct`). The family-level question from house_sales (decision
16 there: `direct` with post-outcome remnants) does not arise here, since nothing is post-outcome.

**18. `source` Other, `year` 2011, bibtex De Cock (2011): consistent**

PROV-8 to PROV-10. hr_analytics (CC 2026-10-14: source Other, the contest page) and airfoil_self_noise (2026-10-20,
Lennart: the original is cited, not the re-upload) agree. The record's `original_source: Other` and `year: '2011'`
already agree.

**19. JSE licence as a note only (issue 8): consistent**

selection.md: a licence or redistribution restriction is no reason and no marker, so it is noted (Lennart, 2026-09-23;
lucas_topsoil). This differs from house_sales: the raw file is pinned by sha256.

**20. Temporal only, `Spatial` as a tag: consistent**

This follows the tension row "Temporal against grouped" (Lennart, 2026-10-12) and house_sales (decision 12 there).

**Not precedent questions (for the claim auditor)**

* curation_comments says the linear model goes "from RMSE 0.133 to 0.124" without the outliers. Today's task probe
  gives 0.119.
* The `Trivial` bullet gives "0.912 for LightGBM", which is the earlier 500-tree run. Today's probe LightGBM is 0.901
  (checklist).

**Files**

* Definition: `datasets/_dev/tabarena-v0pt2/house_prices_nominal/dataset.py`
* Record: `curation/records/house_prices_nominal.md`
* Curator precedents: `curation/records/{hr_analytics,california_house_prices_2020,sberbank_housing_market_forecasting,mercedes_benz_greener_manufacturing}.md`
* AI-draft siblings: `datasets/_dev/tabarena-v0pt2/{house_sales,zillow_prize,perth_house_prices,melbourne_housing_market,stroke_prediction,miami_housing,qsar_tid_11}/dataset.py`
* house_sales report of today: (run folder)
* Rules: `.claude/skills/knowledge-curation/references/{provenance,splits,cleaning_features,task_probes,leak_checks,use_case,selection}.md`

</details>

<details><summary>Advocate</summary>

Read: `dataset.py`, the record, principles.md, and the phase A reports (claim_audit, column_audit, split_audit,
practitioner, precedents, clean_room/report, checklist, REVIEW_before). No Must is broken in any report. What the
reports found are wording, record edits and Should departures that need a written reason. Each one keeps the dataset.

**1. Honest evaluation holds: the record is the house at the sale (P4; LEAK-10 Must, USE-3 Must)**

- Evidence: among houses built two or more years before the sale, `Year Remod/Add` is never after the sale year (0 of
  ~2,590). A refuting test fails to refute it: houses built by 2004 with a 2007-2009 remodel make up 0.0% of 2006 sales
  and 5.2% of 2010 sales (claim audit 26). Split audit, by year: 1/512, 7/581, 3/573, 2/604, 1/325, with no rise for
  the oldest sales. Under a 2010 snapshot, dozens of 2006-2008 sales would show a later remodel. Leak probe: no flag,
  0.0% exact copies across the split. All three auditors and the blind reviewer found no leaking column.
- Objection answered: the practitioner says quality grades may have been revised at sales verification. No report
  tested this or found evidence for it (column audit: "no evidence either way"). EV-6/7: an untested claim is a
  question, not a finding. The one measurable proxy passes.
- Row 937 (a new Partial sale with remodel year 2008, sold 2007) is a training-only row and the house in its contract.
  This is the LEAK-10 "known from the plans" case, weak and one row.
- Mildest fix: wording only. In `fit_reason`, write "the assessor's file of about 2010, in which no remodel postdates
  its sale" (practitioner). Optionally, a note on row 937.

**2. The source is right: De Cock's first publication, pinned (P5; PROV-8 Must, PROV-4 Must)**

- Evidence: the Kaggle train file is a random half. All 1,460 of its rows match De Cock's file. The sha256 matches.
  The full file gives 2,930 labelled rows against 1,460.
- Precedent: hr_analytics (CC 2026-10-14) made the same swap and kept the record's name (precedents decision 1).
- This answers the clean room's first concern ("cite De Cock as the actual source"): the definition already does.
- Remaining gap: the record's `source_links` do not list the JSE file and the DOI. That is a record edit, not a defect
  in the definition.

**3. The use case is real and the fit is direct (P3; USE-1 Must, USE-5 Must, USE-9 Should)**

- Evidence: the data's own actor is the Ames assessor valuing homes from recent sales. That actor has exactly these
  inputs, so the fit is direct (practitioner, "Fit": direct). The target is the price both an assessor and an AVM act
  on. The log RMSE matches the competition's metric (claim 24).
- Objection answered: under the lender framing, location, prior sale and assessed value are missing. That objection
  is about the example sentence, not the data.
- Mildest fix: reword `use_case` to the assessor, or to a valuation service, and drop "lender". The data and the
  split stay as they are.

**4. The split mirrors the application (P4; SPLIT-1, SPLIT-9, SPLIT-14 Must; SPLIT-17 Should)**

- Evidence: 13 expanding two-month windows with 46-191 test rows (median 98). Train is every earlier row, and no row
  is after the window. The split audit's verdict is "right with notes". Two months follows coffee_rating_prediction
  (SPLIT-17). A random split is 0.005-0.010 RMSE more optimistic, so the temporal split matters.
- Objection answered: the precedents report says the no-gap choice departs from SPLIT-10 (Should), because June 2010
  is about 78% of a usual June. Three re-runs measured the gap's effect: +0.0004 to +0.0010 for one month and +0.0016
  to +0.0026 for two, all within noise. April and May 2010 are complete. The shortfall sits only at the extract edge.
- SPLIT-9 (Must) holds: no training label is unknown at the window start in the file as shipped.
- Mildest fix: record the no-gap choice as an exception to SPLIT-10 with these counts (option (a) of the consistency
  check). If the curator prefers the zillow_prize line, a one-month gap is a one-line change and also keeps the
  dataset.

**5. Worth benchmarking: `Trivial` is refuted (P6; TP-4 Must)**

- Evidence: `Overall Qual` alone reaches R² 0.682 against about 0.91 and loses in 13 of 13 windows. De Cock's own
  two-variable model reaches 0.766. The probes give no flag. Models spread: linear minus RF +0.026 (SE 0.005).
- Precedent: california_house_prices_2020 was kept with a far narrower margin (0.89-0.91 against 0.93).
- Objection answered: the blind reviewer calls the dataset "over-studied". No rule excludes for familiarity. The
  temporal split and the full file also differ from the Kaggle task people tuned on. A note at most.

**6. The outlier drop follows the publisher (P7; CLEAN-1 Should, which ranks above CLEAN-11 Should)**

- Evidence: De Cock (p. 4) names the 3 partial sales as "true outliers (Partial Sales that likely don't represent
  actual market values)". They sold at $28-$40 per sq ft against a median of $150. All three are training-only, so
  the scored task is unchanged. CLEAN-1 adopts the data owner's removed anomalies, and at equal strength the earlier
  rule wins.
- Precedent: california_house_prices_2020 dropped prices that do not belong to the record.
- Objection answered: the blind reviewer says the drop makes the task "slightly easier". The rows are never scored.
- Mildest fix: write the drop in the exception form (precedents decision 7), and flag it as the third of its kind for
  an amendment of CLEAN-11.

**7. The rest is quality and wording (P7 and procedure; the remedy ladder)**

None of these items touches validity. Each is a note or a cheap fix:

- **Stale numbers (EV-8 Should).** Linear 0.133 -> 0.124 is now 0.125 -> 0.119. "0.912 LightGBM" is a 500-tree run.
  Update the numbers and name the model. The decision stands either way.
- **Claim 23.** Drop "with the source's codes, as in OpenML": that is another collection's version and no reason
  (EV-4). Keep the documented codes as a CLEAN-12 exception (readable abbreviations from DataDocumentation.txt, unlike
  `A11`). Or map them, which is cheap.
- **`PID` dropped (CLEAN-3 Should).** A measurement outranks inference (EV-2). Adding the section or block as a
  feature changes RMSE by -0.0001 (SE 0.0007) and -0.0005 (SE 0.0005). Keep the drop and give the measured reason.
- **Small cleaning items.** `Exterior 2nd` uses three spellings in 225 rows: map them (CLEAN-12, cheap). Row 2032 has
  a remodel year before the build year: set it to missing (CLEAN-11).
- **June 2010 and the Alloca/AdjLand sales.** Both are kept with `Sale Condition` as a feature. CLEAN-11 keeps values
  that are only unusual. On June, I concede that no distinguishing fact is written yet. Mildest fix: an exception
  citing the first-time-buyer credit's 30 June 2010 closing deadline, which fits the April surge (72 against 48-61).
  Fallback: end the data at May 2010.

**Judgment:** ship after the wording and record edits above.

- Validity: PROV-8, LEAK-10, USE-1/3/5 and SPLIT-1/9/14 hold.
- Exceptions: SPLIT-10 and CLEAN-11 kept as exceptions with their facts.
- Value: TP-4 refutes `Trivial`.
- Quality: notes, plus two cheap fixes.

**Advocate: rebuttal to the critic (2026-10-20)**

The critic and I agree on the verdict: ship after changes, no exclusion. We disagree on one change, point 2. On
points 3 and 4 I differ only on the form of the fix. No new facts.

**1. Actor: conceded**

The lender framing does not fit: a purchase lender already knows the price. This is the same remedy as my point 3.
Rewrite `use_case` around the assessor, or a valuation service with the lender removed, and keep `fit = "direct"`
(USE-1, USE-9). Text only.

**2. Drop the Family, Alloca and AdjLand sales: disputed; at most drop Alloca, and the curator weighs it**

1. **The 3 dropped outliers are a different case.** Three facts set them apart from these 82 rows. The publisher
   names those 3 as not market values (De Cock p. 4; CLEAN-1). They sit at a quarter of the partial-sale price per sq
   ft. And they are training-only, so dropping them changes no score. De Cock does not call the Family, Alloca and
   AdjLand sales outliers, and 34 of them are in the scored windows. The definition already states this difference
   (precedents decision 10: "consistent, with a fact that sets them apart from decision 7"). So the critic's demand
   "say why it treats them differently" is already met.
2. **The model sees the condition.** `Sale Condition` is a documented feature present at the sale, and dropping it
   costs +0.0045 RMSE in 13 of 13 windows (claim audit R4), so models do learn the discount.
3. **The rule favours keeping them.** USE-5 asks for the price the actor acts on: a recorded sale price, with its
   type flagged. CLEAN-11 (Should) keeps rows that are only unusual. A row leaves only when it is no task row (USE-7).
   A family or adjoining-land sale is still a sale the assessor records and has to classify. Precedents agree:
   zillow_prize and house_sales keep linked units, and sberbank keeps its pre-completion sales.
4. **Dropping them makes the task easier.** The 0.145 -> 0.157 example is two rows of one window. Removing the hard
   rows is what the critic objects to in the opposite direction.

**Conceded part:**

- Under the assessor framing, ratio studies exclude these sales, so this is a fair weighing call.
- Alloca prices can be a share of a joint price. That is the strongest sub-case. If the curator wants a change, the
  mildest one is dropping the 24 Alloca rows (REVIEW_before issue 7).
- Weighed on the side of keeping them: the data as published, the feature flag, and score realism. On the side of
  dropping them: the assessor's practice.

**3. "At the sale" overclaims: mostly conceded**

- **Conceded:** reword `fit_reason` and the curation bullet to what was tested, naming the one new house with a
  post-sale remodel year (row 937).
- **Conceded:** set row 937's `Year Remod/Add` to missing. It is cheap and safe (CLEAN-11).
- **Disputed:** the form of the note on the grades. A `Potential leak, kept on purpose:` line is the LEAK-30 form for
  a suspected mechanism. Here no report has evidence either way, and an untested claim is a question, not a finding
  (EV-6, EV-7). Better: one plain sentence saying the grades' timing cannot be checked from the file.

**4. The no-gap reason: conceded that it must be replaced; option (b)**

- **Conceded:** "known once recorded" is not the right reason.
- **Disputed:** "at a refit on 1 May, part of April would still be missing" is inference. The file shows April 2010 at
  72 sales, above 48-61 in earlier Aprils. So the shortfall measured in this file is at the extract edge only.
- **Choice:** take (b), an exception to SPLIT-10 that names this fact. With June's excess error sitting in its 9
  non-Normal sales, the same fact also settles keeping June 2010.
- **Fallback:** (a), a one-month gap. It keeps the dataset too. I agree to settle it together with house_sales and
  perth_house_prices.

**5. `source_links`: conceded**

A record edit, as for hr_analytics.

**6. Stale numbers and claim 23: conceded**

This is my point 7. Update the numbers, name the run each comes from, and remove the OpenML reason. No data change.

**7. Cleaning: conceded**

- Record the outlier drop in the exception form and flag it for an amendment.
- Map the three `Exterior 2nd` spellings.
- Give the measured reason for dropping `PID`.

**Net**

Shared changes: points 1, 3, 4, 5, 6 and 7, all text, record edits or one-cell fixes. The only open call is point 2,
a weighing call for the curator. My position: keep the 82 rows. If the curator wants a change, drop Alloca only.

</details>

<details><summary>Critic</summary>

**Position: ship only after changes.** No point below calls for exclusion. The task is real and nothing leaks in a way
that cannot be fixed. Points 1-4 are validity points (P3, P4) that need changes to the text or the definition before
the folder ships. Points 5-7 are record, procedure and quality fixes.

**1. The named actor does not fit the inputs (P3, USE-1 Must, USE-5 Must)**

- **Problem.** The use case says "a lender or a valuation service estimates the sale price ... from the assessor's
  record". At a purchase, the lender already knows the contract price, so it does not predict it. For a refinance,
  HELOC or portfolio valuation, the lender predicts a price with no sale, and then `Sale Type` and `Sale Condition`
  (worth +0.0045 RMSE, 13/13 windows; claim audit R4) do not exist. As an AVM, the task also lacks what every AVM uses:
  coordinates, the previous sale and the assessed value.
- **Effect.** Under the stated actor the fit is approximate, not the `direct` the definition claims. Under the source's
  own actor, the assessor valuing homes from recent sales, the inputs match exactly and the fit is direct.
- **Evidence.** practitioner.md (Fit; point 2, "one caveat for the lender framing"; gap 1).
- **Remedy (fix the definition, text only).** Rewrite `use_case` around the source's actor: "a city assessor values
  residential properties from recent sales, refit as new sales arrive". The other option is "a valuation service
  estimates the price of a house about to sell", with the lender removed. Keep `fit = "direct"` (USE-9: the source's
  actor, not a rewording that excuses a gap).

**2. Non-market prices are scored while the same kind of price is dropped from training (P3, USE-5 Must)**

- **Problem.** The definition drops De Cock's 3 partial sales because their price is not a market value. It keeps the
  Family, Alloca and AdjLand sales: 82 rows in the file, 34 of the 1,450 test rows. Their prices are no actor's target.
  An Alloca price can be a share of a joint price, and assessors' ratio studies and AVM accuracy tests exclude all
  three kinds.
- **Effect.** They move the scores. Two IDOTRR Alloca sales (residuals -0.55 and -0.56) raise the newest window's
  LightGBM RMSE from 0.145 to 0.157. June 2010's excess error sits in its 9 non-Normal sales: for the 73 Normal June
  sales, RMSE is 0.105 against 0.201 for all of June.
- **Evidence.** practitioner.md (point 3; gap 3), REVIEW_before issue 7, split_audit.md problem 1.
- **Remedy (fix the definition).** Drop the rows with `Sale Condition` in {Family, Alloca, AdjLand}, on the same ground
  as the 3 outliers. Keep Abnorml: foreclosures are market sales the model must value. The mildest acceptable
  alternative is to drop Alloca only. If the curator keeps all of them, the definition must say why it treats their
  prices differently from the 3 dropped outliers.

**3. "The record describes the house at the sale" claims more than was tested (P4, USE-3 Must, LEAK-10 Must, weak)**

- **Problem.** The claim was tested on `Year Remod/Add` only, and the test holds strongly (claim 26). The file is the
  assessor's record of about 2010, so the grades (`Overall Qual`, `Kitchen Qual`, the condition grades) may have been
  revised at sales verification. The file cannot show this either way.
- **One measured post-sale value.** Row 937 (built 2007, sold 2007-06, Partial) has `Year Remod/Add` = 2008.
- **Effect.** Small: one training row, and no evidence about the grades. But `fit_reason` presents an unverified point
  as a fact.
- **Evidence.** column_audit.md problem 1; practitioner.md point 1; claim_audit.md implied claim 1.
- **Remedy (repair and a note).**
  - Set row 937's `Year Remod/Add` to missing, which is CLEAN-11's treatment of the 2207 typo.
  - Reword `fit_reason` and the curation bullet to what was checked: "the assessor's file of about 2010; no remodel
    year postdates its sale except one new house (2008, sold 2007)".
  - Add a `Potential leak, kept on purpose:` line on the grades.

**4. The reason given for no gap is contradicted by the data (P4, SPLIT-10 Should)**

- **Problem.** `splits_comment` says "A price is known once the sale is recorded", but recording lags the sale in this
  file:
  - July 2010 has 8 sales, against 101-122 in earlier Julys.
  - June 2010 has 82 sales, against 97-112 in earlier Junes.
  
  At a refit on 1 May, part of April would still be missing. zillow_prize takes a one-month gap for the same mechanism.
  perth_house_prices cites this dataset as its precedent for "no gap", so the call carries over to the whole family.
- **Effect on the score.** Small: a one-month gap costs +0.0004 to +0.0010 RMSE, within noise. That is no reason to
  skip the rule: the split follows the application, not the size of the effect (tension row "right split against the
  score", forest_fires).
- **Evidence.** precedents.md decisions 6 and 9; split_audit.md (gap rerun); claim_audit.md claim 39.
- **Remedy, one of two.**
  - (a) Add a one-month gap and state it with the task.
  - (b) Record an exception to SPLIT-10 that names the fact: the lag touches only the newest month, at about 78% of a
    usual June, and the split audit found June's excess error in non-Normal sales, not in censored prices. The same
    fact settles keeping June 2010.
  
  Either way, replace the current reason, which is untrue. Settle this together with house_sales and
  perth_house_prices.

**5. The record does not name the data shipped (P5, PROV-8 Must)**

- **Problem.** The record's `source_links` name only the Kaggle competition and OpenML 42165. The definition builds
  from De Cock's JSE file.
- **Effect.** The record does not lead to the first publication, which is the data actually used.
- **Evidence.** claim_audit.md claims 41-42 and untested item 3; precedents.md decision 1 (hr_analytics, CC
  2026-10-14).
- **Remedy (record edit).** Add the JSE file and the DOI to `source_links`, as was done for hr_analytics.

**6. Stale and unsourced numbers, and one refuted claim (procedure, EV-8; writing.md)**

- **Outlier effect, stale.** "Linear RMSE 0.133 -> 0.124": today's probe gives 0.125 -> 0.119.
- **LightGBM R², unsourced.** "0.912 for LightGBM" comes from an unnamed 500-tree run. The probe beside it gives 0.901.
- **Gap effects, not reproduced.** +0.0006 / +0.0026 reran as +0.0010 / +0.0016.
- **Claim 23, refuted.** "Categorical with the source's codes, as in OpenML's house_prices_nominal":
  - OpenML 42563 keeps MS SubClass numeric.
  - The definition relabels MS SubClass and the 14 "NA" levels, so these are not the source's codes.
  - Another collection's version is no reason (the EV-4 case of 2026-10-15).
- **Effect.** No data change. The evidence the curator reads is wrong in the places listed.
- **Evidence.** claim_audit.md refuted items 1-3; precedents.md decision 13.
- **Remedy (text).** Update the numbers and name the run each comes from. Give the gap effect as "under 0.003, within
  noise". Remove the OpenML reason.

**7. Cleaning fixes, cheap and safe (P7, CLEAN-11, CLEAN-12, CLEAN-3; Should)**

- **Outlier drop not recorded as an exception (CLEAN-11).** It departs from CLEAN-11 but is written as a decision, and
  it is the third target-outlier row drop in the repository, after mercedes_benz_greener_manufacturing and qsar_tid_11.
  Remedy: record it in the exception form (precedents.md decision 7), and flag the third exception for an amendment.
- **`Exterior 2nd` spellings (CLEAN-12).** 225 rows spell three codes differently from the codebook and from `Exterior
  1st`. Remedy: map `Brk Cmn`, `CmentBd`, `Wd Shng` to `BrkComm`, `CemntBd`, `WdShing` (column_audit.md problem 2).
- **Wrong reason for dropping `PID` (CLEAN-3).** The definition says it is "unique per row", but `PID` encodes a block
  location. The drop stands because its block prefix measured no gain (-0.0005, SE 0.0005). Remedy: give that as the
  reason (column_audit.md, PID row; precedents.md decision 15).

**Dropped**

- **The dataset is over-studied (blind reviewer).** No rule supports this and nothing measured it.
- **Winter windows of 46-61 rows.** Within SPLIT-17.
- **Mapping the remaining codes to labels.** P7 and minor. It is covered by removing the wrong reason in point 6.

**Critic: rebuttal to the advocate (house_prices_nominal, 2026-10-20)**

The advocate's own remedies are changes: a reworded `use_case` and `fit_reason`, a record edit, two exceptions, updated
numbers and two cheap fixes. Our two briefs therefore lead to the same verdict, "ship after changes", not "ship as
defined". One point is still in dispute: the non-market sales (advocate 7, critic 2).

**Point by point**

**Advocate 1 (as at the sale; LEAK-10, USE-3).** I concede most of it.
- The remodel test holds, and EV-6/EV-7 make the grade-revision risk a question rather than a finding, so I withdraw my
  request for a `Potential leak` line on the grades.
- I keep two cheap requests:
  - Reword `fit_reason`. The advocate agrees.
  - Set row 937's `Year Remod/Add` (2008, sold 2007) to missing. The definition already treats the 2207 garage year
    this way under CLEAN-11. "Known from the plans" covers the build year, not a remodel dated after the sale.

**Advocate 2 (source; PROV-8, PROV-4).** I concede. The only fix left is the `source_links` edit, which matches my
point 5.

**Advocate 3 (use case; USE-1, USE-9).** We agree: change the actor to the assessor or a valuation service, drop the
lender, and keep `fit = "direct"`. This is my point 1. It is a required text change, not an optional one.

**Advocate 4 (split; SPLIT-10).** I concede that an exception is enough. The SPLIT-10 exception must name a measured
fact. The split audit gives one: in June 2010 the 73 Normal sales have a mean residual of -0.001 (RMSE 0.105), and the
excess error sits in the 9 non-Normal sales. That points away from censored prices and fits the same exception for
keeping June. The current reason, "known once recorded", must go because it is untrue.

**Advocate 5 (Trivial; TP-4).** I concede. Remove the marker. I had already dropped the over-studied point.

**Advocate 6 (outlier drop; CLEAN-1 over CLEAN-11).** I concede the drop, written in the exception form. Its reason is
the publisher's "not actual market values", which matters for advocate 7.

**Advocate 7 (quality and wording).**
- Stale numbers, claim 23, `PID`, `Exterior 2nd`, row 2032: I concede. These are the same remedies as my points 6 and
  7. I accept either the CLEAN-12 exception or the mapping for the remaining codes.
- June 2010: I concede, with the exception described under advocate 4.
- **Alloca, AdjLand and Family sales: I dispute this.** The advocate keeps them under CLEAN-11 ("values that are only
  unusual"). That is the wrong rule, for two reasons:
  - The question is whether these prices are the target the actor acts on. That is USE-5 (Must, P3), which outranks
    CLEAN-11 (Should, P7).
  - An allocation price can be a share of a joint price (REVIEW_before issue 7). An assessor's ratio study excludes
    family and adjoining-land transfers (practitioner, point 3), so neither actor targets these prices.
- **The definition is also inconsistent with itself.** It drops 3 training-only rows because their price is not a
  market value, yet keeps 34 scored test rows with the same defect. Those rows move the window scores: two Alloca sales
  take the newest window from 0.145 to 0.157.
- **Remedy, unchanged.** Drop Family, Alloca and AdjLand; keep Abnorml. The mildest form is to drop Alloca only. If the
  curator keeps them, the definition must name the fact that sets them apart from the 3 dropped outliers.
- **What would settle it.** The window RMSEs with and without these rows, and an answer to whether a valuation task
  ever targets these prices.

</details>

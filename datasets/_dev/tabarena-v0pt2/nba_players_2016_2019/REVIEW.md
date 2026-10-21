# nba_players_2016_2019

**Outcome:** added. Verdict: ship; the changes the review panel asked for are in the definition. Validity: SEL holds;
USE-5 holds (the 2017-18 and 2018-19 scores recomputed to the NBA's official values, PROV-13 applied); USE-3
triggered and fixed in the text (the prediction point is the vote's close); LEAK-10 holds (votes, ranks, `Play`,
`Rk` and names dropped); LEAK-11 applied to the 25 whole-season statistics and `team`, both measured to weaken the
signal; USE-10 met in part (last season's score added as `prev_score`), its temporal part barred by SPLIT-14, so the
grouped split stays, tagged `ForcedGroupedFromTemporal` under SPLIT-8 as amended (Lennart, 2026-10-21); PROV-13 for the pageviews met in part by masking
185 stale copies (issue 7). Value: TP holds (linear skill 0.739, SE 0.004, rerun with `prev_score`; no probe flag; about 220 test players per
fold).
Quality: P7 clean. Weighed: against, a student upload on Kaggle and an approximate use case; for, the first sports dataset and clear
signal. Left for you: the target over the whole ballot (issue 4), and two second sources: box scores for the statistics (issue 3) and the Wikimedia API for the pageviews
(issue 7).

**Main points:** Keep the score over the whole ballot (issue 4), and keep the end-of-season statistics (issue 3) and the masked pageviews (issue 7)
instead of rebuilding them from a second source?

**Record fields that disagree with the definition:**

- `domain`: record `Other`, definition `social science`.

**Record judgment:** valid with an approximate fit: the prediction point and the split are stand-ins, both named in the
definition. The record's earlier "no known risk" is corrected in its new assessment.

**Issues for Lennart:**

4. **Target: keep the All-Star score over the whole ballot?**
   - Problem: a ballot is one season, one conference and one position group (guards or frontcourt), with 92-140
     players. Only its top 2 guards or top 3 frontcourt players start, and the actor (a team's staff deciding whom to
     campaign for) acts on the top few. The score ranks every player on the ballot, and the error measure (RMSE, the
     root of the mean squared error) weighs every row the same. 92% of the rows score above 10 and carry 77% of the
     score's variance.
   - Effect on the real task: the benchmark mostly measures how well a model orders bench players with a few thousand
     fan votes, which no decision uses. A model that is good at the top and poor at the bottom scores worse than its
     use warrants.
   - Implemented: the source's target, the NBA's own selection score (SEL-8), with a note in `predicted` and in the
     notes. A label is relative to its ballot, and the ballot (season, conference, position group) is in the
     features.
   - Alternatives: keep only the contenders (a cut of our own that shrinks a 1,408-row task); `Play`, whether the
     player played in the game (73 positives; points per game alone gives AUC 0.966, close to one feature); log fan
     votes (one value per row, but its scale changes by season: median 4.7k, 4.6k, 13.1k).
   - Rule: USE-5 (P3, Must: the target is what the actor acts on), weighed against SEL-8 (trace the source's task).
     The advocate and the critic both recommend keeping the target with the note.
   - Recommendation: keep.
   - Decision: keep the whole-ballot score, or restrict the rows or change the target?

3. **Statistics: keep the end-of-season values, or rebuild them as of the vote's close?**
   - Problem: the 25 statistics (games, games started, minutes and the per-game values) and the team are the values at
     the end of the regular season in April. The vote closes in mid-January, and by then a player had played a median
     54% of the season's games.
   - Implemented: the end-of-season values kept, with a LEAK-11 note in the definition naming the vote's close as
     the prediction point.
   - Effect on the real task: models see whole-season statistics that a staff member in January would not have yet.
     This makes the task harder, not easier: about 0.03 R² below what vote-close inputs give. No label information
     rides on them.
   - Rule: LEAK-11 (P4, Should: a value measured after the outcome that weakens the signal stays, with a note).
   - Evidence that they weaken the signal: the statistics as of the vote's close, rebuilt from box scores (one record
     per player and game), predict better, grouped LightGBM R² 0.772 against 0.741 (paired SE 0.004, an earlier run;
     this panel had no box scores). Blanking the end-of-season team on the 87 rows whose team is of the other
     conference raises R² from 0.744 to 0.751 (paired SE 0.0015). Trades within a conference are not measured.
   - Alternative: rebuild the statistics and the team as of the vote's close from a second raw input, the Kaggle
     dataset nathanlauga/nba-games (box scores scraped from stats.nba.com, licence "unknown"; 1,397 of 1,408 rows match
     by name, 43 have no game before the vote). The fit would come closer to direct. Cost: a source of unknown
     licence, and vote-close dates (16 Jan 2017, 15 Jan 2018, 21 Jan 2019) not confirmed on the NBA's pages.
   - Precedent: south_africa_coronary_heart_disease kept values measured after the outcome under LEAK-11.
   - Recommendation: keep; rebuild only once the dates and a box-score source are confirmed.
   - Decision: keep the end-of-season statistics, or rebuild them?

7. **Pageviews: re-pull them from the Wikimedia API, or keep the mask?**
   - Problem: `wikipedia_daily_views` is the mean daily views of the player's Wikipedia article over the calendar year
     the season starts in, before the vote. In 185 rows of the later seasons it was an exact copy of an earlier
     season's value of the same player (a stale merge in the upload). Also damaged:
     7 rows that hold a 2016 mean without being an exact copy, and rows that count a redirect title (another spelling
     of the article's name, which few readers land on) instead of the article.
   - Implemented: the 185 exact copies are blanked in `_clean`; the 7 rows and the redirect rows stay, with a note.
   - Effect on the real task: small. Masking changed grouped R² by -0.005 (SE 0.003); dropping the column costs
     0.038.
   - Rule: PROV-13 (P5, Must) asks for a repair from the origin when the origin has the clean data. The Wikimedia
     pageviews API reproduces the file's values to two decimals for the 4 player-years tested. SUPPORT2 and ashrae were repaired the same way, column by
     column from the origin.
   - Alternative: re-pull the column per calendar year from the API as a second raw input. Cost: the release has no
     article titles or redirect mapping, so we would build that mapping ourselves.
   - Keeping the mask alone departs from PROV-13 unless you record that the mapping is out of practical reach for
     this column.
   - Recommendation: keep the mask, and record as a fact under PROV-13 that the origin is out of practical reach for
     this column (the title and redirect mapping would be ours; effect -0.005).
   - Decision: keep the mask, or re-pull the column?

**Review panel:** ship after changes (mediator). Full tier: claim, column and split audits, domain practitioner, blind
review, precedent check, advocate and critic with one rebuttal each, mediator. Claim audit: most claims hold; refuted
the stated prediction point (end of season, after the outcome) and two record statements (`domain`, "no known risk"),
all fixed or listed above; untested the box-score measurement and a few low-stakes claims. Blind review: include with
changes; its main concerns are the season-long statistics and the whole-ballot target. Agreed by advocate and critic
and applied: the prediction point stated as the vote's close, `prev_score`, the split text and fallback note, masking
the 185 pageview copies, the target note, the use-case wording. Settled by the mediator: `team` stays under LEAK-11
(blanking the moved teams raises R² by 0.007), and PROV-14 does not block a column repair. To you: the mediator's issue
1 is issue 2 here (split), its issue 2 is issue 4 (target), its issue 3 is issue 3 (box scores), its issue 4 is issue 7
(pageviews).

<details><summary>Mediator</summary>

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1 holds (approximate fit, USE-8); USE-5 holds (target repaired to the NBA's official scores,
  PROV-13 applied); USE-3 triggered, fixed in text (prediction point = the vote's close); LEAK-10 holds (votes, ranks,
  `Play`, `Rk`, names dropped); LEAK-11 applied to the 25 whole-season statistics and `team` (both measured to weaken
  the signal); USE-10 partly fixed (`prev_score` added), its temporal part barred by SPLIT-14: grouped kept as a
  fallback with the cost measured, amendment due (issue 1); PROV-13 (pageviews) fixed in part by masking 185 copies,
  repair from the origin open (issue 4).
Value: TP holds (linear skill 0.710, SE 0.005; no flags; 220 test groups per fold).
Quality: P7 clean (missing values, `second_position`, salary placeholders: notes at most).
Weighed: source - (student project), use case approximate, gap + (no sports dataset yet), signal +.
For the curator: issue 1, the split amendment (third "too few periods" case); issue 2, target over the whole ballot;
  issue 3, vote-close statistics from box scores; issue 4, re-pull or mask the pageviews.
```

**Changes to make now (no decision needed)**

1. **Prediction point (USE-3 Must, LEAK-1; LEAK-11).** Name the vote's close as the prediction point in `known` and the
   first `curation_comments` bullet. Keep the 25 statistics, `games`, `games_started` and `team` under a LEAK-11
   note: "measured after the outcome; weakens the signal". Evidence for the statistics: vote-close statistics 0.772 vs
   0.741 (paired SE 0.004, earlier run). Evidence for `team`, new: masking the end-of-season team on the 87
   other-conference rows raises grouped R^2 0.744 -> 0.751 (paired +0.007, SE 0.0015); MSE on those test rows
   226 -> 188. Trades within a conference stay unmeasured; say so. In `fit_reason`, "predict as well" becomes
   "predict better".
2. **`prev_score` (USE-10 Must, USE-6; LEAK-34; CLEAN-19).** Add last season's score of the same player. It is
   missing for 2016-17 (436 rows) and for players without a row in the previous season. Note that the missing values
   come from the design and say nothing about the player. Measured: grouped 0.744 -> 0.760 (SE 0.004). It is known when
   the vote opens, so it stays valid under the grouped split. Both sides agree on this change.
3. **Split text (SPLIT-23, USE-8, EV-8).** In `split`, say that held-out players are mostly veterans whose other
   seasons are hidden, not new players. Tag the split as a fallback from temporal, with the measured cost: one valid
   window 0.745 vs grouped 0.744, same family order. Add the settings to `splits_comment` (untuned, 3 x 3 folds) and
   say that this panel's rerun puts the temporal window marginally above grouped.
4. **Pageviews (PROV-13 Must, ladder rung 2).** In `_clean`, mask the 185 exact copies of an earlier season's value
   (deterministic from the raw file; -0.005, SE 0.003). Note the 7 remaining 2016-mean rows and the redirect-title
   undercounts. "Kept as shipped" goes. The full repair is issue 4.
5. **Target note (USE-5, USE-8).** In `predicted` or `fit_reason`, say that the score ranks the whole ballot. 92% of
   rows score above 10 and carry 77% of the variance, so RMSE is driven by non-contenders. Also say that the label is
   relative to its cell (season x conference x ballot position), and that the cell is in the features.
6. **Use case and fit (USE-8; USE-9 factor).** Rephrase `use_case` to the actor before the first fan returns. In
   `fit_reason`, name the missing fan returns. Once change 2 is in, the prior vote is missing only for 2016-17.
7. **Record (house rule; writing.md).** `domain: Other` -> `social science`. In the 2026-10-20 assessment, change
   "no known risk" to "known gap: stand-in prediction point and split". Carry issues 1-4 into `REVIEW.md`.

**Issues for the curator (ranked)**

1. **Split: grouped instead of temporal (P3 USE-10 Must vs P4 SPLIT-14 Must). A rule question.**
   - Problem: the use case is a new season of mostly known players (81% of 2018-19 rows). A temporal split needs three
     windows with at least half the rows before each, and three seasons give one.
   - Effect: small. Grouped 0.744 vs the one valid window 0.745, with the same family order. After change 2, the gap
     to the real-use proxy (about 0.77) is mostly closed.
   - Advocate: exclusion is only for a Must that cannot be fixed. Ship the closest regime with the cost measured, as
     SPLIT-8 / account_debt_south_africa did.
   - Critic: USE-10 outranks SPLIT-14, so as written this is not a valid exception.
   - Rule: no Must can be met for the temporal part, so the ranking cannot settle it. This is the third case of the
     same reason (open_university, distribution_transformers), so principles.md calls for an amendment.
   - Decision: an amendment that says what a task with too few periods ships as. The options are the closest regime
     with a "forced from temporal" tag and the cost measured, a one-window temporal task, or `No`. Apply it to all
     three cases, including the distribution_transformers pair, which went the other way (see Consistency).
2. **Target over the whole ballot (P3 USE-5 Must). A weighing call.**
   - Problem: the actor acts on the top 2-3 of each cell. RMSE weighs the bench players' order most.
   - Advocate: the score is the NBA's own selection quantity and the source's target (SEL-8). Restricting the rows
     would be our own invention and would cut a 1,408-row task.
   - Critic: agrees to a note now, but asks whether to restrict the rows or use a target that does not depend on the
     other rows. The alternative `Play` is close to one feature (AUC 0.966), and log fan votes changes scale by season.
   - Both sides recommend keeping the target with the change 5 note.
   - What would settle it: whether the benchmark wants the source's target or a decision-resolution target.
3. **Vote-close statistics from box scores (P4 LEAK-11 Should, USE-3). A weighing call.**
   - Problem: change 1 keeps the whole-season values under LEAK-11.
   - The rebuild would make the fit closer to direct and score higher (0.772).
   - Against it: it needs a second raw input (Kaggle nathanlauga/nba-games, licence unknown), and the vote-close dates
     are unconfirmed. Neither side makes it a precondition.
   - What would settle it: confirmed vote-close dates and a usable box-score source.
4. **Pageviews: re-pull from the Wikimedia API or keep the mask (P5 PROV-13 Must).**
   - Problem: change 4 removes the exact copies. The 7 rows with a 2016 mean and the redirect undercounts stay.
   - The rule asks for repair when the origin has the clean data. The API reproduces the file to 2 decimals for the 4
     player-years tested.
   - PROV-14 does not block a column repair: SUPPORT2 and ashrae were repaired under PROV-13 without becoming new
     datasets. On this point the critic's correction holds.
   - Advocate: the release has no title or redirect mapping, so we would build that mapping ourselves.
   - Effect: small. Dropping the column costs 0.038.
   - Decision: re-pull as a second raw input. Or record that the title mapping is out of practical reach and keep the
     mask with a note. That second option is a departure from PROV-13 (consistency check D5).

**Agreed facts**

- The raw file is one Kaggle CSV, sha256 verified. It has 1,408 rows of 660 players over 3 seasons, with no duplicate
  player-seasons. OpenML 43653 holds the same data.
- The target recomputed for 2017-18 and 2018-19 equals the official NBA scores: 214/214 rows re-parsed here, 958
  overall. The shipped score matches 28.
- 2016-17 is on the same scale (unranked players get "voted in the cell + 1"). Season means are 42.4 / 45.8 / 44.7. A
  model trained on 2016-17 scores R^2 0.718 on 2017-18.
- The votes, ranks, `Play`, `Rk` and names are dropped correctly. The leak probe finds 0.0% exact copies across the
  split and no flags.
- The vote runs from 25 Dec to 21 Jan (2019), and the starters are public on 24 Jan. "The end of the regular season"
  is therefore after the outcome, and change 1 fixes the text.
- Post-vote values weaken the signal for the statistics (0.772 vs 0.741, earlier run) and for `team` on the moved rows
  (this report: +0.007 when masked).
- `wikipedia_daily_views` covers the calendar year the season starts in, before the vote. 185 rows are exact copies,
  192 rows are stale.
- Of the temporal windows, only 2018-19 has at least 50% of the rows before it (66%). Scores: grouped 0.744, temporal
  0.745, IID 0.759. `prev_score` adds +0.016 (grouped) and +0.017 to +0.021 (temporal).
- Task probe: linear skill 0.710, best single feature 0.426, no flags. Not `Too Small`.
- Fit is `approximate`, and the verdict is not exclusion.

**Consistency with precedent**

- **Target repair (D1):** follows SUPPORT2, ashrae, cirrhosis and the eryhemato tension (the formula is the NBA's own).
- **Prediction point and kept statistics (D3, D4):** after change 1 this follows south_africa_coronary_heart_disease
  (LEAK-11, point unchanged). Moving the point after the outcome had no precedent and goes.
  - `team` now has its own number, measured the way melbourne_housing_market was. The difference: its post-outcome
    value lowers the score rather than leaving it unchanged, which is LEAK-11 rather than "did not change".
- **Split (D2):** departs from distribution_transformers_at_cauca_department (2026-10-07, open). That case rejected
  stacking the periods and grouping by unit, and shipped one year IID.
  - Facts that may set NBA apart: no contaminated period to drop, and one season (436-498 rows) would be small.
  - These facts are not enough to settle it, so the question goes to the curator as issue 1. The amendment is due
    either way.
- **Pageviews (D5):** masking alone departs from PROV-13 as applied to SUPPORT2 and ashrae, unless the curator records
  that the origin is out of reach for this column (issue 4).
- **Drops, target choice, metadata, cleaning (D6-D9):** consistent. No register flag, and no prior curator decision on
  this dataset.

</details>

<details><summary>Claim audit</summary>

**Claims table**

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 3, 15, 28 | 1,408 rows, 660 players, 1-3 rows each | D task_summary, comments, grouping | count raw and rebuilt frame | holds | 1,408 rows; 660 ids, 660 names, id<->name 1:1; 207/158/295 players in 1/2/3 seasons | EV-1 |
| 12 | only file nba_final.csv, 45 cols, dated 2019-12-04, sha256 06455e5a... | D download_description | sha256sum; Kaggle API file list | holds | sha matches; one file, creationDate 2019-12-04T09:23Z, 321,038 bytes, version 1 | PROV-1 |
| 11 | licence CC0-1.0 | D | Kaggle API metadata | holds | `CC0-1.0` | EV-4 (note only) |
| 27 | social-power-nba is CC BY-NC-SA 4.0 | D comments | Kaggle API metadata | holds | `CC-BY-NC-SA-4.0` | EV-4 |
| 29 | data-card quote on independent observations | D grouping | Kaggle API description | holds (verbatim) | "for a problem of indipendent observations we took only the last seasons' observation for each player" | EV-2 (rank 3) |
| 13 | OpenML 43653 = same rows/cols, 51 names lost non-ASCII | D | download parquet, align on (Player_ID, Season) | holds | 1,408 x 45, same columns, all numeric equal; `Player.x` differs in 51 rows; `Pos2` NaN stored as string "None" (1,396; harmless) | PROV-4 |
| 14, 22 | names are make.names of bbref glossary; per-game stats | D RENAME, comments | read values | holds | MP values 7.4-~37 are per game though the card says "Minutes played" | CLEAN |
| 17, 4, 40 | score = 0.5 fan + 0.25 player + 0.25 media rank within conference x ballot position; NBA's own rule | D, R | data card text; pr.nba.com 2019 page | holds | card: "weighed, with weight 0.50 ... and 0.25 to the two remaining"; NBA: "(Fan Rank * 2 + Player Rank + Media Rank)/4" | EV-2 |
| 18, 41 | shipped 2017-18/2018-19 score adds ballot size + 1 (113-147) to the rank of no-vote players | D comments, R | 4 x (shipped - formula)/k per cell, k = number of missing components | holds | constant per cell 113-147; equals the cell's max fan rank + 1 in 7 of 8 cells (2017-18 West front: max + 2, as the earlier REVIEW.md says) | PROV-13 |
| 18, 34, 42 | recomputed equals official scores for all 958 matched rows; shipped matches 28 | D, R | parse 2 of 8 official 2019 PDFs (West guard, East frontcourt), match by name, compare unrounded formula to the official weighted score | holds (2 of 8 cells re-checked) | 214 of 214 matched rows equal, ranks and player votes agree in 214/214; shipped equals official in 4/214. The other 6 cells and 2018 not re-run | EV-1 |
| 18 | rounded to one decimal half-to-even, as source rounds 2016-17 | D | 2016-17 rows with all three ranks: formula vs shipped | holds | 32/32 equal after `.round(1)`; .x25 -> .x2, .x75 -> .x8 in the source (half-to-even); later-season quarters are exact binary, so pandas rounds the same way | CLEAN |
| 18 (2016-17 scale), checklist P3/P4 concern | 2016-17 "follows the formula and keeps its values": same scale as the recomputed seasons | D comments; checklist doubted it | infer the implied no-vote rank in 2016-17 per cell; compare with the official convention of 2017-18 | holds; checklist concern refuted | implied 2016-17 no-vote media rank = (file players with media votes) + 1 in all 4 cells (8, 12, 6, 10); implied player rank = voted + 1 plus 1-3 ballot players absent from the file, the same pattern as the official 2017-18 East front (71 voted in file, official no-vote rank 74). Target mean by season 42.4 / 45.8 / 44.7 (shipped 42.4 / 93.6 / 87.1). A model trained on 2016-17 scores R^2 0.718 on 2017-18 | USE-5, PROV-13 |
| 34 (table) | shipped = formula in 26 / 25 rows of 2017-18 / 2018-19; 2016-17 32 rows with all ranks | D decisions | recompute | holds | 26/498, 25/474, 32/436 | EV-1 |
| 35 | 295/158/207 players; Spearman 0.777 / 0.803 | D decisions | recompute | holds | 0.7766, 0.8034 | EV-1 |
| 36 | `Rk` is last-name order (0.9995-0.9996) | D decisions | recompute | holds | 0.9995 / 0.9996 / 0.9996 | PROV-15 |
| 19, 7 | votes, ranks, Play, Rk, name dropped | D | read frame columns | holds | none of the 10 columns in the 36-column frame | LEAK-10 |
| 23 | `team` of the other conference in 87 rows | D comments | team -> modal conference | holds (count); "mostly trades after the vote" untested | 87 rows, no TOT rows | LEAK-11 |
| 24 | `wikipedia_daily_views` = mean daily views over the calendar year the season starts; 185 later-season copies; drop -0.038 | D comments | Wikimedia API (agent=user) for 2 players; copy count; drop column on the shipped splits | holds | one player's 2016/2017/2018 means and a second player's 2016 mean equal the file to 2 decimals; 185 copies; drop -0.044 (0.736 -> 0.692). Masking -0.005 not re-run | LEAK-10, EV-1 |
| 25 | missing stays missing; no duplicate rows | D | count | holds | 0 duplicate (id, season); probe 0.0% exact copies across split | LEAK-16 |
| 31, 32 | grouped 3-fold; only the newest season has >= half the rows before it | D splits_comment | count | holds | train before 2017-18: 436/1,408 = 31%; before 2018-19: 934/1,408 = 66% | SPLIT-14 |
| 33 | grouped 0.751 vs newest season 0.747 vs random 0.769 | D splits_comment | rerun: shipped 10 x 3 grouped, 10 x 3 random KFold, train 2016-18 / test 2018-19 | holds (order and size; levels differ) | grouped 0.736, newest season 0.744-0.752, random 0.756 | SPLIT-4, EV-8 |
| 6, 9 (2nd half) | held-out players stand in for a new season of mostly known players | D task_summary | newest-season holdout: share of known players; add the previous season's score (USE-10 says it is a feature for a known entity) | holds as a stand-in, gap measured | 81% of 2018-19 rows are known players; prev score adds +0.017 R^2 (0.752 -> 0.770; known rows 0.757 -> 0.780, 5 seeds); grouped 0.736 vs the real-use proxy 0.770: the stand-in under-rates by ~0.03 | USE-10, SPLIT-1, SPLIT-14 |
| 16 (1st sentence), 5 | "Prediction point: the end of the regular season"; every feature known then | D comments, task_summary | compare with the use case's own moment and with when the outcome is published | refuted (as written) | the use case's moment is "while the All-Star vote is open" (claim 2); the vote result is published in late January, so at the end of the regular season (April) the label is already known and no decision is left. The point is chosen to make the features legal, not from the use case | USE-1, USE-3 (Must) |
| 16 (2nd half), 9 | later games carry no label information; vote-close statistics predict better (0.772 vs 0.741) | D | needs box scores (not available to this panel) | untested | rests on the earlier verifier's measurement (the earlier REVIEW.md issue 3, paired SE 0.004) | LEAK-11 |
| 9 vs 16 | fit_reason "predict as well" vs comments "predict the score better" | D | read | wording mismatch (not a fact) | 0.772 > 0.741 is "better", SE 0.004 | writing.md |
| 30 | context none, row-level prediction | D grouping | read | holds | each label is a rank against the other rows of the cell, but the cell (season x conference x ballot position) is in the features | SPLIT-23 |
| 37 | `dataset check` 0 warnings | D README | not re-run (rewrites README.md, a repository file) | untested | checklist reports 0/0/0 | EV-7 |
| 44 | record 2026-10-20: "no known risk" | R | compare with the definition | refuted | the definition itself documents a stand-in prediction point and a stand-in split (fit approximate) | USE-8, writing.md |
| 45 | record `domain: Other` | R | compare with D | refuted (consistency) | definition `social science` | house rule (record = definition) |
| 1, 2 | question; marketing-staff use case | D | no source states it; written "For example" | untested (plausibility) | the card's goal is "predict the All Star Game score"; actor is our inference | USE-1, EV-2 |
| implied | the regression target is what the actor acts on | - | variance share of the top of the ballot | concern, not refuted | 92% of rows score > 10; rows with score <= 10 (the starter race) carry 23% of the target variance, so RMSE is dominated by the long tail (fan-rank order of bench players) | USE-5 (Must) |
| implied | no row is a copy across the split | - | id/name maps, dup (id, season) | holds | 1:1 id<->name, 0 dup | LEAK-17 |
| implied | the rows are the ballot | - | official PDFs vs file cell | holds with a note | 2019 West guard: 107 ballot / 107 file but 9 names unmatched (suffix spellings), East front: 127 ballot / 124 file; players who did not play that season are on the ballot and not in the file: the population is ballot players who played | LEAK-22 (cohort) |

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. **Claim 16/5, the stated prediction point (P3, USE-1/USE-3, Must).** "The end of the regular season" is after the
   outcome is published (late January) and contradicts the use case's own moment, "while the All-Star vote is open".
   What it changes: nothing in the data; the honest statement is prediction point = the vote's close, with the 25
   whole-season statistics and `team` kept under LEAK-11 (Should: values measured after the outcome that weaken the
   signal), which is exactly what the 0.772 vs 0.741 measurement shows. Mildest remedy: rewrite the first
   curation_comments bullet and `known` to name the vote as the prediction point and cite LEAK-11 for the kept
   post-vote statistics; fix "predict as well" to "predict better" in fit_reason.
2. **Claim 16 (2nd half), the LEAK-11 premise (P4, Should): untested here.** The keep rests on one measurement by an
   earlier verifier with box scores from a Kaggle copy of unknown licence. What it changes: if the post-vote
   statistics did not weaken the signal the keep would fail LEAK-10 (Must). Remedy: keep the note; the number is
   already documented with its SE.
3. **Split (claims 6, 9, 31; P3/P4, USE-10 Must vs SPLIT-14 Must): holds as a stand-in, not as the use case's split.**
   81% of a new season's rows are known players, for whom USE-10 makes the previous score a feature; that adds +0.017
   R^2 and the grouped split scores ~0.03 below the real-use proxy. A single temporal window cannot meet SPLIT-14.
   Remedy: none in the data; state the measured cost (grouped 0.736 vs newest season with previous score 0.770) in
   splits_comment so the curator decides with the number (prior issue 2).
4. **Implied: the target over the whole ballot (USE-5, Must, concern).** The decision is about the top of each
   ballot; 77% of target variance lies in the long tail. Not refuted (the rank is the NBA's own score and the source's
   target); remedy: one sentence in `predicted` or a curator question; no change to data.
5. **Claim 44, record "no known risk" (writing / USE-8).** Remedy: "known gap: stand-in prediction point and split".
6. **Claim 45, record `domain: Other` vs `social science` (house rule).** Remedy: align the record field.
7. **Untested, low stakes:** claim 37 (`dataset check` would rewrite README), claim 23 "mostly trades after the vote"
   (needs trade dates), claim 34 for the 6 other official tables, claims 1-2 (actor is inference, written "For example").

The checklist's concern that 2016-17 sits on a different scale is refuted: the 2016-17 no-vote ranks follow the same
"voted in ballot + 1" convention as the official 2017-18 tables, and the season means are 42.4 / 45.8 / 44.7.

</details>

<details><summary>Column audit</summary>

Prediction point stated (first bullet): end of the regular season. The use case in `task_summary` says "while the
All-Star vote is open" (vote closes mid-January). Both are checked below: "season end / vote".

**Column table**

| column | meaning | known at prediction? (season end / vote) | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| all_star_score (target) | 0.5 fan + 0.25 player + 0.25 media rank within season x conference x ballot position; lower is better | outcome | float64, 1.0-93.2, no NaN; 2017-19 recomputed from file ranks | fine. Measured: unranked players get rank = (number with votes in the cell) + 1 in all three seasons (2016-17 implied media constants 8/12/6/10 = nM+1 in all four cells; 2017-19 file ranks = n voted + 1). The checklist's "max + 2" is ties in MRank, not a different convention: the seasons are on one scale | USE-5, PROV-13 |
| player_id | basketball-reference player id, hashed | yes / yes | category, 660 levels, stable hash | fine: group column, dropped by the harness before fitting | LEAK-33, CLEAN-4 |
| position | bbref primary position (`Pos1`) | yes / yes (season label, stable) | category, 5 levels | fine | CLEAN-14 |
| second_position | second position of a hybrid listing (`PF-C`) | yes / yes | category, 1,396 of 1,408 missing | fine (not constant; CLEAN-12 split of one field, lossless) | CLEAN-5 |
| age | bbref age (as of Feb 1 of the season) | yes / yes (from birth date) | int64, 19-42 | fine | |
| team | team at season end; traded players carry their last team with season-total (TOT) stats | yes / no for 82 of 87 other-conference rows | category, 30 levels, no `TOT` | fine at season end; mismatch at the vote (documented) | USE-3, LEAK-10 (weak) |
| games, games_started | games played / started, whole season | yes / no | int64, GS <= G in all rows | fine at season end; past the vote | USE-3 |
| minutes_per_game and the 22 other per-game and percentage stats | bbref season per-game stats | yes / no (median 54% of games played by the vote's close, prior run) | float64; PTS = 2FG + 3P + FT and TRB = ORB + DRB hold within rounding in all rows | fine at season end; past the vote, not label-carrying (vote-close stats predict better, 0.772 vs 0.741) | USE-3, LEAK-10 |
| field_goal_pct, three_point_pct, two_point_pct, free_throw_pct, effective_field_goal_pct | shooting percentages | as above | NaN exactly where the season's attempts are 0 (4/99/15/47/4); 59 3P% values with 0.0 attempts per game are rounding of the per-game value, not errors; eFG max 1.5 is possible (only threes made) | fine | CLEAN-10, CLEAN-11 |
| salary | season salary (source not named by the card; inferred bbref/hoopshype) | yes / mostly; 107 rows < $500k are two-way or 10-day contracts (77,250 repeated in 2017-18), some signed after the vote | float64, 62 NaN; target mean 46.9 missing vs 44.3 present (missingness not outcome-driven) | fine at season end; question at the vote | LEAK-10 (weak), CLEAN-10 |
| wikipedia_daily_views | mean daily pageviews over the calendar year the season starts in | yes / yes (no value after the vote) | float64, 138 NaN (no page; target mean 65.0 vs 42.1: obscurity, not the outcome). Measured: values that are k/366 (a 2016 leap-year mean) in 113 rows of 2017-18 and 54 of 2018-19, i.e. stale 2016 values in later seasons; plus redirect-title rows under 20 views | cleaning problem (damage repairable from origin) | PROV-13, CLEAN-1 |
| season | season label | yes / yes | category, 3 levels | fine (lets models absorb cell-size scale per season) | CLEAN-14 |
| conference | conference of the ballot (not of `team`; differs in 87 rows): fixed when the ballot is made, before the vote | yes / yes | category; `Est` -> `East` mapped without NaN (704/704) | fine | |
| ballot_position | ballot role, `Back`/`Front` -> guard/frontcourt | yes / yes | category, 629/779 | fine | |
| dropped: Fvot, FRank, Pvot, PRank, Mvot, MRank | votes and ranks | outcome components | dropped | correct | LEAK-10 |
| dropped: Play | played in the All-Star game | after the vote | dropped | correct | LEAK-10 |
| dropped: Rk, Player.x | alphabetical row number; name | - | dropped | correct | CLEAN-3, CLEAN-4 |

Selection: every row has a fan vote (min 3 votes); the rows are the inner join of bbref stats and the vote results. No
outcome-driven selection seen (2 rows with < 10 fan votes).

**Problems, ranked by principles.md**

1. **P3/P4, USE-1 and USE-3 (Must), LEAK-10 (weak): the use case's moment and the prediction point disagree.**
   `task_summary.use_case` places the decision "while the All-Star vote is open"; the first bullet sets the point at
   season end so that 25 statistics, `team` (82 rows moved after the vote) and some `salary` values are legal. Against
   the written use case they are post-point values. Evidence that no label information rides on them: vote-close
   statistics predict better (prior run, paired -0.031, SE 0.004), so it is a mismatch, not a strong leak. Mildest
   remedy: make the two statements agree. Either (a) keep season end and rewrite the use case to an actor who acts at
   season end (fit stays approximate; check it is not a SEL-3 look-back study), or (b) rebuild the 25 statistics and
   `team` as of the vote's close from box scores (then the use case is direct; the box-score source's licence is
   "unknown" and the vote-close dates are unconfirmed). Curator's call (open issue 3).
2. **P5, PROV-13 (repair from the origin before keeping): `wikipedia_daily_views` is damaged and the origin is
   reachable.** 167 later-season rows hold a 2016 (366-day) mean, 185 rows repeat an earlier season's value, and some
   rows count a redirect title. The Wikimedia pageviews API covers 2015-07 onwards and the prior run already pulled
   2017/2018 values from it (for one player 6,292 / 6,145 against the shipped 4,679). Current state: kept as shipped
   with a note, which is the third rung of the ladder while the first (rebuild per calendar year, following
   redirects) is available. Mildest acceptable: mask the 185 copies (deterministic, -0.005 R^2); preferred: rebuild.
   Effect on scores is small either way (dropping the column -0.038).
3. **P4, LEAK-10 (weak, only under the vote point): `salary` of late signings.** 107 rows under $500k are two-way or
   10-day contracts; some were signed after mid-January. Irrelevant at season end; if remedy 1(b) is chosen, take the
   salary as of the vote or note it.
4. **No problem, for the claim auditor: target scale across seasons.** The checklist's concern (2016-17 uses "max + 2"
   for the unranked) is resolved: in every cell of every season the unranked rank is the number of players with votes
   plus one (competition ranking; 2016-17 Est Back: 7 media-ranked players with tied ranks up to 6, implied constant 8).
   The recomputed 2017-19 target and the shipped 2016-17 target follow one convention.
5. **P7, fine with notes:** `second_position` 99% missing (kept, not constant); shooting percentages missing where no
   attempts (correct); `team` vs `conference` mismatch in 87 rows is the ballot conference against the end-of-season
   team (documented). Procedure note outside the column scope: the data card says CC0 while the merged pageviews come
   from a CC BY-NC-SA 4.0 source (already noted in the comments; licence field may need to say so).

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes**

The declared split (grouped 3-fold CV by `player_id`, 10 repeats) is not the regime the use case implies (known players
in a new season: temporal, USE-10), but the temporal split cannot be built under SPLIT-14, the grouped split scores
the same as the one temporal window that exists and ranks model families the same way, and the gap is written down
(`fit="approximate"`, `split`, `splits_comment`). No re-split needed. Notes below.

**Facts measured**

| | value |
|---|---|
| Rows / players per season | 2016-17: 436 / 436; 2017-18: 498 / 498; 2018-19: 474 / 474 (one row per player and season) |
| Rows of players seen in an earlier season | 2017-18: 364 / 498 (73%); 2018-19: 384 / 474 (81%) |
| Share of rows before each season (temporal train side) | before 2017-18: 31%; before 2018-19: 66% -> one window meets SPLIT-14's 50% floor |
| Shipped splits | 30; 0 players on both sides (checked 3 splits; grouping by construction); test 445-490 rows, ~220 players, every season in every test fold |
| Group id | `Player_ID`, basketball-reference's player id (`jamesle01`), anonymized; 1-3 rows per group (295/158/207 players in 3/2/1 seasons) |
| Mean target by season | 42.4 / 45.8 / 44.7 (sd 22-23): after the recompute the seasons are on a near scale |
| 2018-19 newcomers vs returning | 90 new (median age 22, 11.7 min, mean score 56.9, sd 17.3) vs 384 returning (26, 21.9 min, 41.9, sd 23.4) |

Scores (LightGBM unless named):

| split | all rows | rows with a previous season | rows without |
|---|---|---|---|
| shipped grouped (30 splits) | 0.744 (sd 0.023) | 0.738 | 0.740 |
| IID 10x3 | 0.759 (sd 0.019) | 0.758 | 0.750 |
| temporal: 16-17 + 17-18 -> 18-19 (one window, 66% train) | 0.745 | 0.749 | 0.558 (n=90) |
| temporal: 16-17 -> 17-18 (31% train, below SPLIT-14) | 0.731 | 0.713 | 0.653 |
| temporal 18-19 + `prev_score` (last season's score) | 0.766 | 0.773 | 0.563 |
| grouped (shipped) + `prev_score` | 0.760 (se 0.004) vs 0.744 (se 0.004) without | | |
| IID + `prev_score` | 0.769 | 0.780 | 0.746 |
| carry-forward of last season's score alone, 18-19 returning rows | 0.623 (n=379) | | |

Family ranking (ridge / RF / LightGBM): grouped 3x3 0.689 / 0.694 / 0.738; IID 3x3 0.699 / 0.709 / 0.751; temporal
18-19 0.693 / 0.735 / 0.756. Same order in all three; RF gains most under the temporal window.

Group probe (panel): IID 0.730 vs grouped 0.715, gap 0.015; across-group learnability 0.69-0.70 for three families
(SPLIT-27/28 not triggered). Leak probe: 0.0% exact feature copies across the split.

**Problems, ranked (principles.md order)**

**1. P3/P4: regime declared (cold start) differs from the use case's (known players over seasons). Note, not a re-split.**

- Rules: USE-10 (Must: decide new or known entity before the split; known entity -> temporal with the previous outcome
  as a feature), SPLIT-1, SPLIT-3, SPLIT-13; against SPLIT-14 (Must: >= 3 windows, train side >= 50%).
- Evidence: the use case is a team's staff estimating where *its* players will rank during the vote; 81% of 2018-19
  rows and 73% of 2017-18 rows are returning players. Only the 2018-19 window has >= 50% train (66%); 2017-18 has 31%.
  SPLIT-14 is a Must and cannot be met, so temporal is barred; the definition says so. The one valid window scores
  0.745 vs grouped 0.744, and family ranking agrees, so the stand-in does not distort the benchmark on these numbers.
- What the stand-in loses: the history a known-entity use case has. Last season's score adds +0.021 (temporal) and
  +0.016 (grouped) R^2; a grouped split by design hides a test player's other seasons.
- Mildest remedy: keep the grouped split with the existing note (approximate fit). Optional, curator's call
  (USE-6/USE-10): add the previous season's score as a feature (`prev_score`, missing for 2016-17 and for new
  players); it is known when the vote opens and keeps the grouped split valid (it is a label of the same player's
  earlier row, on the same side of every split). Cost: it is missing for 31% of rows by construction (2016-17), and
  the 2016-17 scale question (checklist, "unranked" constant) would then enter a feature.

**2. P4: the grouped test set stands for veterans without history, not for newcomers. Note.**

- Rules: SPLIT-23 (what one prediction is and what is known about a new group), USE-8 (name the gap).
- Evidence: held-out players under the grouped split are mostly multi-season veterans (rows without a previous season
  score 0.740 under grouped); the real newcomers of 2018-19 are young bench players (median 11.7 min) that the temporal
  window scores at 0.558 (n=90, narrower target sd 17.3 vs 23.4). The `split` text says "players never seen"; they are
  players whose other seasons are hidden, which is not the same population as real new players.
- Mildest remedy: one clause in `task_summary.split` / `splits_comment` (e.g. "held-out players are mostly veterans
  whose other seasons are hidden"). No code change.

**3. P4: IID alternative correctly rejected. Pass.**

- Rules: SPLIT-29/30, SPLIT-4.
- Evidence: under IID a test player's later seasons are in train (future information; 0.759 vs 0.744, probe gap 0.015).
  The gap is small and does not decide (SPLIT-4); the reason the definition gives (a random split trains on the
  future) is the right one. Grouping on a true id (SPLIT-24 pass), not a cluster or hash.

**4. Procedure (EV-8): split numbers in `splits_comment` lack their source. Minor.**

- Evidence: `splits_comment` gives LightGBM 0.751 grouped / 0.747 newest season / 0.769 random without saying the
  splits and settings (from the earlier REVIEW.md issue 2: untuned 3x3). This run: 0.744 / 0.745 / 0.759 (different settings,
  same conclusion). Note the comment says "close to"; here the temporal window is marginally higher, not lower.
- Mildest remedy: add "untuned, 3 x 3 folds" to the sentence.

**Checked, no problem**

- Temporal items (time column meaning, windows, gap vs label delay, rows with unknown labels, training history,
  season-shaped windows): not applicable, the split is not temporal. `season` is a categorical feature known at the
  prediction point. Within one season the label (the January vote) is known to all rows at once, so no SPLIT-9 issue
  under the grouped split. The fact that features run past the vote is a LEAK-10/USE-3 question for the leak auditor,
  not the split.
- Grouping declaration: `labels="per_sample"`, `prediction_unit="row"`, `context="none"` match the use case (one score
  per player-season, predicted from that row). No aggregation. `player_id` is excluded from the 34 features.
- The target is a rank within season x conference x ballot position (cells of 92-140 players), so a test row's label
  is relative to training players of the same cell; this holds under every split and is no leak.

</details>

<details><summary>Domain practitioner</summary>

Actor taken from `task_summary.use_case`: a team's marketing/PR staff during the All-Star vote, deciding which of its
players to campaign for. I also considered a sportsbook pricing "named a starter" props and a media analyst forecasting
the starters; their inputs and target are the same as the PR staff's.

**Fit: approximate (keep it; USE-8)**

The target is the real All-Star score (now on one scale), but the features describe the whole season, which ends three
months after the vote. They also leave out the published fan returns and the previous season's vote, which I would
always have. So the data stands in for the January decision with a named gap. It is not direct: no decision is made at
the stated prediction point (the end of the regular season), because by then the score has been public since late
January (USE-3, USE-9). It is not none: the January decision is real and the score is its outcome (USE-2).

**How the decision is made (2018-19, pr.nba.com)**

- Voting opens 25 Dec 2018 (about 30-35 games into the season) and closes 21 Jan 2019, 11:59 pm ET. Starters are
  revealed 24 Jan and reserves 31 Jan.
- The NBA publishes fan returns on 3, 10 and 17 Jan: the top 10 guards and top 10 frontcourt players per conference,
  with their vote counts.
- Score = average of the weighted ranks (fan x2, players, media). The top 2 guards and top 3 frontcourt players per
  conference start, and fan votes break ties. Reserves are picked by the coaches, not by the score.
- So the score matters only at the top of each of the 4 cells per season (10 starters a season). Ranks below about 10
  in a cell decide nothing.

**1. Inputs at the prediction point (the vote, Dec 25 to Jan 21)**

| Input | Have it then? |
|---|---|
| 25 per-game/total statistics, `games`, `games_started` | No, as shipped: whole-season values (USE-3). I would have the season up to the vote, about 40-55% of games. The earlier run's rebuild shows the vote-close statistics predict better (LightGBM 0.772 vs 0.741). This is a mismatch that lowers skill, not a leak. |
| `team` | Mostly yes. End-of-season team: 87 rows of the other conference, 82 of them traded after the vote. |
| `age`, `position`, `conference`, `ballot_position`, `season` | Yes. The ballot position is fixed when the ballot is published. |
| `salary` | Yes (contract set before the season). |
| `wikipedia_daily_views` | Yes. The calendar year the season starts, so before the vote. 185 rows are stale copies of an earlier season, a small cost (-0.005). |
| **Published fan returns (top-10 fan rank and votes per cell, 3 releases)** | **Missing. I would always have them.** The fan rank is half the score, and the returns cover exactly the contenders. |
| **Previous season's score / All-Star selection** for returning players | **Missing, and excluded by design by the grouped split** (USE-10, USE-6). 80% of 2018-19 rows have a 2017-18 row, Spearman 0.80. |
| Team record at the vote, prior All-Star count, injury status, market size, social following | Missing. A practitioner would use team record and All-Star history first. |

My probe (temporal: train 2016-17 + 2017-18, test 2018-19, LightGBM): adding the
previous season's score raises R^2 from 0.749 to 0.770 (+0.021). The model recovers 8 of the 10 actual starters with or
without it (one season, so this is noisy).

**2. Target: what I act on, or a proxy?**

- I act on "will he start (top 2/3 of his cell)?", or "is he close enough to the cut that a campaign could move him?".
  So I want a probability of starting, or a rank among the top ~10 of each cell (USE-5).
- The shipped target is a continuous weighted rank over the whole ballot, 92-140 players per cell, and RMSE weighs every
  row equally. About 80 of 1,408 rows (score <= 10, 34-40 a season) are in the zone anyone acts on. The RMSE is driven
  by the tail (ranks 30-90 among players with a few thousand fan votes), which no decision uses.
- The target is relative within the season x conference x ballot cell. A row's label depends on who else is on that
  ballot, while the grouping claims `context="none"` and treats each row as independent. This is acceptable for a
  benchmark but differs from my decision, which is a ranking within a cell.
- A cleaner per-row stand-in would be log fan votes (`Fvot`, the half of the score a campaign moves). It is
  season-dependent (median 4.7k / 4.6k / 13.1k across the three seasons), so it would need a season normalisation.
- The 2017-18/2018-19 recomputation is right from my side: the official pr.nba.com scores are what the NBA acted on.
  The checklist notes that 2016-17 keeps an "unranked" constant for players without player or media votes. That only
  affects the tail.

**3. Does a row match a decision? Does the test data match what I face?**

- One row = one player-season ≈ "where will this player land?", which is close to one decision. But the decision is
  made for 1-3 candidates per team against the whole cell, not for every player on the ballot.
- The test data is held-out players (cold start). What I face is a new season of players I mostly know (USE-10, the
  "entity seen before" factor). The earlier run measured grouped ≈ newest season held out (0.751 vs 0.747), and my
  probe gives +0.021 for the history the grouping excludes. The split costs little, and with three seasons a temporal
  split cannot meet the protocol (SPLIT-3). This is the smallest of the gaps.

**4. Would I use this model?**

- For the campaign decision: no. In January the three fan returns tell me the fan rank of every contender, and that is
  half the score. A model on whole-season box scores without the returns would not change whom I campaign for.
- As a benchmark it is an acceptable approximate stand-in: real data, a real target repaired to official values, and
  signal from features legitimately related to the outcome.
- What would make me trust it: statistics cut at the vote's close; evaluation focused on the top of each cell (did it
  find the starters, the 6th-10th "bubble"); the previous season's vote as an input.
- What makes me distrust it: features from after the outcome (even when harmless); a metric dominated by players
  nobody votes for.

**Gaps, ranked by how much they change the task**

1. **Time window of the features (USE-3, USE-4, USE-8).** Whole-season statistics and team for a vote that closes in
   mid-January. Under the stated end-of-season prediction point the label is already public, so the stated point serves
   no actor; the use case lives at the vote. Fix: issue 3 option (b), the statistics as of the vote's close (or its
   opening).
2. **Missing inputs the actor always has (USE-6, USE-10).** The published fan returns (dominant, but not in the source
   file) and the previous season's score (+0.021 R^2, excluded by the grouped split). Without the returns the task is
   "forecast the vote before any return is published", a narrower and earlier actor (a pre-vote preview) than the one
   `use_case` names. The `use_case` wording should say this.
3. **Target resolution (USE-5).** A full-ballot weighted rank scored by RMSE, against a decision about the top 2/3 (or
   ~10) of each cell. The labels also depend on the composition of the cell, which contradicts `context="none"`.
4. **Split (USE-10, USE-11).** Cold start by player against a known-player reality. Measured as small. Keep it and name
   it, as `fit_reason` already does.
5. **Feature hygiene.** 185 stale pageview copies and redirect-title undercounts. Small (-0.005 masked).

**What a domain expert would change**

- Rebuild the statistics, `games`, `games_started` and `team` as of the vote's close (25 Dec opening, 21 Jan close in
  2019; 2017-18 and 2016-17 analogous) from box scores. Then the prediction point is the vote and the fit could be
  argued closer to direct (USE-3, USE-4).
- Add the previous season's score / All-Star starter flag and the team's win percentage at the vote. This needs a
  temporal frame. With three seasons it is a feature only for 2017-18/2018-19, while the grouping keeps excluding
  history (USE-10).
- If the target stays the score, state that RMSE is dominated by the bottom of the ballot. Consider capping or
  restricting it to ballot players with meaningful votes, or offering "starter" (73 `Play` rows are a related but
  different label: All-Star including reserves, decided by coaches) as a secondary view. Log fan votes would be a
  row-independent alternative (USE-5).
- Rephrase `use_case` to the actor who has no returns: "before the first fan returns, a team's PR staff (or a preview
  writer) forecasts where its players will rank". Keep `fit="approximate"` and name in `fit_reason` both the window and
  the missing returns and prior-season vote. The current `fit_reason` names only the window and the split.

**Sources**

- pr.nba.com, "2019 NBA All-Star Voting first returns": https://pr.nba.com/2019-nba-all-star-voting-first-returns
  (vote 25 Dec to 21 Jan, returns 3/10/17 Jan, top 10 per position shown, scoring and tiebreak).
- NBA.com, first returns release: https://www.nba.com/news/all-star-voting-2019-first-returns-official-release
- Kaggle data card (via the definition): https://www.kaggle.com/datasets/davra98/nba-players-20162019

</details>

<details><summary>Blind review</summary>

**Verdict**
Include with changes. The data is real and has clear signal (LightGBM grouped 3-fold R2 0.74). But the features are full-season numbers, while the All-Star vote they are used to predict closes mid-season. The target is a within-group rank that is mostly noise for the roughly 80% of players who are never contenders. Both points need to be documented, and the timing problem should ideally be fixed.

**What the task is**
NBA All-Star starters are picked by a weighted vote: fans 50%, players 25%, media 25%. Each voter group ranks players within conference x ballot position (guard or frontcourt). `all_star_score` is that weighted rank: lower is better, 1 is the top vote-getter. The OpenML description says the source project wanted to "predict the All Star Game score for each player". The source is a university project from Milan, with data from basketball-reference and hoopshype. A team, an agent or a media/betting analyst could plausibly want to forecast vote standing, but this is a student project, not an operational use. Kaggle page content could not be fetched (JS-only). I read OpenML 43653 (description and feature list).

**Concerns (most to least serious)**

1. **Timing leak: the features come after the vote.** All-Star fan voting runs from about late December to mid/late January. The per-game stats (`games`, `games_started`, `points_per_game`, ...) are full-season numbers. `games` goes up to 82, and the 75th percentile is 74 games, so these are end-of-season totals and not stats as of the vote. `wikipedia_daily_views` is an average over an unknown window. If that window covers the whole season, it includes the attention spike from being picked as an All-Star, which is a reverse-causal signal. Effect in the model: dropping salary and views lowers R2 from 0.742 to 0.706. The direction of causality for views cannot be checked. *Change:* if possible, rebuild with stats as of the voting cutoff. Otherwise document the task as "explain season-level vote standing" and accept the soft leak. At minimum, state the window used for the views.

2. **The target is a within-group rank, and for most rows it is noise.** The score depends on who else is in the same season x conference x ballot-position group (12 groups of 92-140 rows). It is not a property of the player alone. Among players with fewer than 10 minutes per game (n=225), the score ranges from 16 to 93 (IQR 53-76). These are ranks among players with a handful of fan votes or none, and ties and how missing votes were imputed decide them. Missing values in the raw data: Pvot/PRank 159, Mvot/MRank 404. The source does not say how these missing ranks enter `Score`. So most of the loss in RMSE/R2 comes from ordering non-contenders, which is arbitrary, not from the decision-relevant top of the list. *Change:* document this. You could also limit rows to plausible contenders (for example minutes_per_game >= 15 or games_started > 0) or use a log/rank-stable transform. Check how missing player and media ranks were imputed.

3. **The split mostly fits the task.** One row per player-season (checked: 0 player-season duplicates). 660 players: 295 with 3 seasons, 158 with 2, 207 with 1. Holding out whole players stops a model from memorising a player's popularity, which is sensible. A forward-in-time split would be more natural for "predict next season's vote". My check: training on 2016-18 and testing on 2018-19 gives R2 0.744, the same as the grouped split, so the choice does not change the conclusions. Note that the OpenML description says only the most recent season was kept "to keep observations independent". This table instead has up to 3 seasons per player, which the grouped split handles correctly.

4. **Minor preparation and quality issues.**
   - `second_position` is 99% missing (1396 of 1408). Drop it, or keep it as a "dual position" flag.
   - Salary 77,250 appears 87 times. These are probably two-way or 10-day placeholders rather than real annual salaries. Document this or set to NaN.
   - `effective_field_goal_pct` max is 1.5 (2 rows), and for 10 rows points do not equal 2*2P + 3*3P + FT. These are small-sample rounding effects, harmless.
   - Shooting percentages are NaN when there were no attempts, which is correct.
   - For players traded mid-season there is one row with a single `team`. It is unclear which team was kept (TOT is not present). `team` carries real signal through market and fan base: dropping it lowers R2 from 0.742 to 0.702.
   - Leak columns from the source were removed correctly: Fvot/FRank/Pvot/PRank/Mvot/MRank, which define the target, and Play. Names and Rk were removed too.

5. **Size and difficulty are adequate but small.** 1,408 rows and 34 features. The target is not trivial: points_per_game plus minutes_per_game alone gives R2 0.43, and the full model 0.74. That leaves room to separate methods, but with only 12 rank groups the scores will vary from fold to fold.

**What I checked**
dtypes, missingness, value ranges, internal arithmetic consistency, player-season duplicates, position-to-ballot mapping, Spearman correlations with the target (strongest: points_per_game -0.69, views -0.56, salary -0.53), LightGBM GroupKFold baselines, ablations, and a temporal holdout.

**Could not check**
- The Kaggle page text (not rendered).
- The exact formula for `Score` when player or media votes are missing, and whether the 2016-17 media/player votes exist (media voting started in 2017).
- The averaging window for Wikipedia views.
- Which team traded players were assigned to.
- Whether the stats are season-end or as-of-vote. They look season-end: games up to 82.

</details>

<details><summary>Precedent check</summary>

Register: none of the four register flags involves this dataset. The record has no `CC` line and no curator mark on
any issue (the 2026-10-07 review page put it out of the task-summary scope; the REVIEW.md issues are all open), so there
is no curator decision on this dataset that could drift. The two undated screening comments ("Fake IID" by using only
the last season for each player; "Need to figure out which split / subset of the data to use") are the only curator
input, and the definition answers them in line with USE-11 (see D2).

**Summary**

| # | Decision | Verdict | Rules |
|---|---|---|---|
| D1 | 2017-18/2018-19 target recomputed with the NBA's formula | consistent | PROV-13, USE-5, TP-6 tension |
| D2 | Grouped by player instead of the temporal split the use case implies | departs with a stated reason that a lower-ranked Must gives; third case of the same reason: amendment due; a sibling went the other way | USE-10, SPLIT-3, SPLIT-14, (SPLIT-8, SPLIT-16) |
| D3 | Prediction point moved to the season's end so the whole-season statistics fit | outcome consistent (LEAK-11); framing departs without a reason | USE-3, LEAK-1, LEAK-11, USE weighed factor |
| D4 | `team` kept as the end-of-season team | departs with a stated reason that rests on D3; not measured | LEAK-10, LEAK-11 |
| D5 | Stale `wikipedia_daily_views` kept as shipped | departs without a reason | PROV-13 (Must), remedy ladder |
| D6 | Drops: votes and ranks, `Play`, `Rk`, names; id anonymized | consistent | LEAK-10, CLEAN-3, CLEAN-4 |
| D7 | Target choice (score over `Play` / salary) | consistent | USE-5, SEL-8, TP-4 |
| D8 | Metadata: year 2019, licence notes, domain `social science` | consistent | SEL licence line (Lennart, 2026-09-23); definitions.md field mapping |
| D9 | Missing values, `second_position`, dtypes; no accepted warnings | consistent | CLEAN-2, CLEAN-5, CLEAN-10, CLEAN-14 |
| D10 | fit `approximate` | consistent | USE-8 |

**D1. Target recomputed for 2017-18 and 2018-19 (REVIEW issue 1)**

* Follows PROV-13 (repair from the origin; Must): SUPPORT2 (phase II physiology restored from ICPSR 2957), ashrae
  (kWh from the owners' raw files, 2026-10-15), both `applied` in provenance.md Cases. Follows USE-5 (redefine a badly
  built target into the real one): cirrhosis_patient_survival_prediction (Lennart, 2026-10-14). Follows the tension
  "a better version against our own fix" (TP-6, USE-4; eryhemato_squamous_disease, Lennart, 2026-10-06): the formula is
  the source's and the NBA's own, confirmed against the official tables (958 matched rows), not a fix of our invention.
* Not a precedent question but a like-rows-alike one inside the dataset, for the claim auditor: 2016-17 keeps a small
  "unranked" constant per cell (checklist: max rank + 2 in a cell) while the recomputed seasons use the NBA's ranks for
  players without votes. If the two conventions put unvoted players on different scales, the repair is incomplete
  (USE-5); if they match, D1 is fully consistent.
* Verdict: consistent.

**D2. Split: grouped by player (REVIEW issue 2)**

* What the rules say. The definition's own use case is "a new season of mostly known players". USE-10 (Must, P3): for
  a known entity "the split is temporal and the previous outcome is a feature"; a grouped split tests a cold start.
  SPLIT-3 (Must) and the tension "temporal against grouped" (Lennart, 2026-10-12): "one regime, the one the use case
  implies". The definition picks the regime the use case does not imply, because SPLIT-14 (Must, P4) needs three
  windows with half the rows before each, and three seasons give one.
* Under the ranking this is not an exception: both rules are Musts, a Must has no exceptions, and USE-10 (part 2)
  outranks SPLIT-14 (part 4). The nearest curator-decided rules point away from a fallback regime: SPLIT-16 / seismic_bumps
  (Lennart, 2026-09-30: "no fallback to an IID split", retired `Too Small`). The only sanctioned fallback is SPLIT-8 /
  account_debt_south_africa (Lennart, 2026-10-12: ships as IID, tagged forced IID from temporal, cost measured), which
  is narrower (no dates at all). NBA has dates, only too few periods. The definition does measure the cost (newest
  season held out 0.747 against grouped 0.751, random 0.769), which is what SPLIT-8 asks for.
* Same reason, third time (principles, case 4). "Too few periods for SPLIT-14's three windows" now decides three
  open drafts, with two different fallbacks:
  - open_university_learning_analytics_dataset (AI, 2026-10-07; REVIEW issue 1 open): four start dates, grouped by
    module-presentation; deployment's unit (a new presentation) is a group, so grouping is close to the use case there.
  - distribution_transformers_at_cauca_department (AI, 2026-10-07; REVIEW issue 2 open): two years, shipped as IID on
    2020 only. It rejected the very option NBA implements, "both years stacked and grouped by transformer ... Every unit
    appears twice, and it is not the use case", and listed "a framework exception: allow a one-window temporal task".
  - nba_players_2016_2019: three seasons, all stacked, grouped by player (players recur 1-3 times; not the use case
    either).
  NBA and distribution_transformers are a real pair of similar facts (recurring entities across too few periods,
  known-entity use case) decided differently. A fact that may set them apart: the transformers' inventory postdates the
  2020 burns, so the 2019 rows are more contaminated (46% against 37% self-protected), a reason to drop a year that NBA
  lacks; and one NBA season (436-498 rows) would be small.
* Consistent parts: rejecting the source's one-row-per-player subset follows USE-11 (one row per entity only when the
  use case is that row; breast_cancer_prediction, Lennart, 2026-10-15; corporate_credit_rating, 2026-10-16: one row
  per entity cost 0.112 against 0.158 skill) and answers the curator's screening comment ("Fake IID"). Grouping on the
  source's `Player_ID` follows SPLIT-24 (a true group id).
* Verdict: departs with a stated reason, but the reason is a lower-ranked Must: not a reasonable exception under the
  ranking; an amendment is due (third case of the same reason).

**Consistency check (AI, 2026-10-20):** the grouped split of nba_players_2016_2019 (a departure from USE-10 and
SPLIT-3: the use case is a new season of known players) differs from distribution_transformers_at_cauca_department
(draft of 2026-10-07, open: stacking years and grouping by unit rejected as "not the use case", one year shipped IID),
and it is the third dataset where too few periods for SPLIT-14 decide the regime (with
open_university_learning_analytics_dataset). What sets NBA apart?
(a) one NBA season is too small to ship alone and no year is contaminated, so stacking is the only way to keep the
rows, and the grouped score sits closest to the newest-season hold-out (0.751 against 0.747), recorded as an
exception; (b) treat NBA like the transformers (one season, IID); (c) reopen distribution_transformers to stack and
group like NBA; (d) change the rule: an amendment to SPLIT-14 (or a new rule next to SPLIT-8) that says what a task
with too few periods ships as (the closest regime with the cost measured and a "forced from temporal" tag, or a
one-window temporal task as a framework change, or `No`), applied to all three.

**D3. Prediction point moved to the end of the regular season (REVIEW issue 3, option (a))**

* The outcome follows LEAK-11 (Should; narrows LEAK-10): "a value measured after the outcome that weakens the signal
  stays, with a note"; precedent south_africa_coronary_heart_disease (Lennart, 2026-10-01: measured after the MI, kept
  with a comment; dropping `sbp`, `obesity` moved AUC 0.774 to 0.778). NBA has the same fact pattern, measured more
  firmly: statistics as of the vote's close beat the whole-season ones for all three families (LightGBM 0.772 against
  0.741, paired SE 0.004; RF -0.010; ridge -0.019). The post-vote values weaken the signal.
* The framing departs. USE-3 (Must) names the prediction point as "when the model is used and what is known then"; the
  vote's result is fixed in mid-January, so at the season's end nobody predicts it. The definition is inconsistent with
  itself: `task_summary.use_case` says "while the All-Star vote is open", `curation_comments` says "Prediction point:
  the end of the regular season". Moving the point after the outcome is what use_case.md's weighed factor "a use case
  rephrased only to excuse a gap" warns against. The pattern of the curator's cases moves a point earlier, not later:
  mic (Lennart, 2026-09-30: predict at admission, ICU day-1..3 columns dropped); kickstarter (at launch, `staff_pick`
  dropped). The south_africa precedent kept the prediction point and called the values post-outcome.
* The remedy ladder puts "fix the definition" above "keep with a note": option (b) (vote-close statistics from box
  scores) is a fix that exists, which iranian_churn (retired: no common prediction point can be rebuilt) did not have.
  LEAK-11 as a Should allows keeping; choosing (a) over (b) is a weighing call, correctly left to the curator.
* Verdict: outcome consistent (LEAK-11, south_africa); the stated prediction point departs from USE-3 without a reason.

**Consistency check (AI, 2026-10-20):** your call on nba_players_2016_2019 (keep the whole-season statistics, framed
by moving the prediction point to the season's end, after the vote) differs from south_africa_coronary_heart_disease
(kept 2026-10-01, same mechanism: values measured after the outcome that weaken the signal, framed under LEAK-11 with
the prediction point unchanged) and from mic (2026-09-30: the point moved earlier, not later). What sets NBA apart?
(a) nothing: state the prediction point as the vote's close (as `task_summary.use_case` already does) and keep the 25
statistics under LEAK-11 with a "measured after the outcome, weakens the signal" note, fit approximate; (b) keep the
season-end framing as an exception to USE-3, naming the higher principle it serves; (c) take option (b) of issue 3,
rebuild the statistics as of the vote's close (the fix ranks above a note on the remedy ladder); (d) change the rule:
an amendment saying when a point may move after the outcome.

**D4. `team` is the end-of-season team**

* Mechanism: LEAK-10 "attributes looked up after the outcome ... unless the data shows they did not change". The
  Mechanisms table: house_sales (dropped) and melbourne_housing_market (kept: the looked-up `Bedroom2` equals `Rooms`
  in 98-100% of each window's rows). NBA: 82 of the 87 other-conference rows moved after the vote; trades within the
  conference are not counted, so the share that changed is unknown.
* Stated reason: "known at the prediction point, and a trade does not depend on the vote". The first half rests on D3's
  moved point; the second is a LEAK-11 argument (the value does not carry the label), plausible but not measured on its
  own (the 0.772 / 0.741 comparison swaps statistics and team together, per REVIEW issue 3 (b)).
* Verdict: departs with a stated reason, which stands or falls with D3. If D3 goes to (a), the note under LEAK-11
  should cover `team` too; a measured team-at-vote against end-of-season comparison would close it like melbourne.

**D5. Stale pageview values kept as shipped (REVIEW issue 7)**

* 192 of 856 later-season values (22%) repeat an earlier season's mean or a 2016 mean; some rows count a redirect
  title. This is damage to the release (the data is not what it claims to be: the season's pageviews), P5.
* PROV-13 (Must): check whether the origin has the clean data and repair from it when it has. The origin is reachable
  and already used by the drafter: the Wikimedia API gives 6,292 and 6,145 for one player's 2017 and 2018, where
  the file repeats 4,679. Precedents: SUPPORT2 and ashrae (repaired), coad_colon_adenocarcinoma (Lennart, 2026-10-16)
  and corporate_credit_rating (Lennart, 2026-10-16), retired for a rebuild; the tension "repair against cleaning around
  damage" (P5 over P7): "repair or rebuild from the origin first; when the origin cannot be reached, keep with a note".
* The reason given ("no value is later than the vote, so none leaks") answers a P4 question, not the P5 one. The
  remedy ladder also has a middle step the draft skipped: masking the 185 exact copies, deterministic from the raw
  file (-0.005 R², SE 0.003).
* Verdict: departs without a reason (from a Must; any departure needs an amendment or a fact that makes the origin
  unreachable).

**Consistency check (AI, 2026-10-20):** your call on nba_players_2016_2019 (keep 192 stale `wikipedia_daily_views`
values as shipped, a departure from PROV-13) differs from SUPPORT2 and ashrae (repaired from the origin) and from
coad_colon_adenocarcinoma and corporate_credit_rating (retired 2026-10-16 for a rebuild), all damage whose origin had
the clean data, as the Wikimedia pageviews API does here. What sets NBA apart?
(a) the damage sits in a column a third party merged in, the repair needs a new raw input with an article-title and
redirect mapping we would invent, and its effect is within noise (-0.005 R²), so the origin is practically out of reach
for this column; record it as kept with a note; (b) treat it like SUPPORT2: rebuild the column from the Wikimedia API
(as a second raw input) or at least mask the 185 exact copies (the fix in the definition); (c) reopen the precedents
(not suggested: they are larger damage to the target or all features); (d) change the rule: an amendment to PROV-13
that lets a small, measured, non-target damage stay with a note when the repair would need a new source.

**D6. Dropped columns and ids**

* Vote counts and ranks (`Fvot` ... `MRank`): parts of the target, LEAK-10 ("a part ... of the target"; UCI student
  performance G1/G2). `Play`: decided by the vote, a consequence of the target (LEAK-10; kickstarter `staff_pick`).
  `Rk`: an alphabetical row number (Spearman 0.9995-0.9996 with last-name order), CLEAN-3. Names: dropped, ids
  anonymized with a stable map, CLEAN-4.
* The TabSTAR note follows PROV-15 and its 2026-10-15 case (another collection's version named only for provenance or
  a duplicate: OpenML 43653 is the same file); the same kind of note is in one other definition.
* Verdict: consistent.

**D7. Target choice (REVIEW issue 4)**

* The source's own goal (SEL-8, trace the original task) and the quantity the actor acts on (USE-5). `Play` would be
  close to one feature (points per game alone AUC 0.966; TP-4 / the `one_feature` mechanism), salary is fixed before the
  season by contracts. Verdict: consistent.
* Not a departure, noted for completeness: SEL-9 puts ranking tasks out. The target is a within-cell rank, but one score
  per player-season predicted from that row, not an ordering of items for a query; the only SEL-9 case
  (yearprediction, a recommender) is unlike it. No precedent decides a rank-valued regression target either way.

**D8. Metadata (REVIEW issue 6, record fields)**

* Licence: CC0 plus the merged CC BY-NC-SA pageviews, noted; licence terms are no reason to exclude (selection.md,
  Lennart, 2026-09-23). Consistent.
* `domain`: `social science` in the definition is the closest match of the fixed list for the record's `Other`
  (definitions.md, field mapping); the only other `social science` definition is anes_voting_2026; no sports dataset
  was ever added, so there is no precedent to follow. Syncing the record is a field update for the curator, not a
  consistency question.
* `year = "2019"` (upload year) matches the source's first publication. Consistent.

**D9. Cleaning and dtypes; accepted warnings**

* Missing values left missing (CLEAN-2), no proxy codes found (CLEAN-10), `second_position` 12 of 1,408 set: not
  constant, kept (CLEAN-5 drops constant columns only), categories as listed (CLEAN-14). No accepted check warnings, 0
  warnings in `dataset check`. Consistent.

**D10. Fit `approximate`**

* USE-8: a stand-in with a known gap, named: like account_debt_south_africa (a snapshot for a forecast) and kick (a
  potential leak kept on purpose). Consistent. If D3 goes to (c) (vote-close statistics), the feature gap closes and
  only the split (D2) keeps it approximate.

**For the mediator**

* Departures without a reason: D3 (framing of the prediction point, USE-3) and D5 (PROV-13, a Must).
* Not reasonable under the ranking as written: D2 (USE-10 outranks SPLIT-14); with open_university and
  distribution_transformers it is the third case of the same reason, so an amendment is due, and the transformers pair
  is decided the other way.
* No drift (no curator decision on this dataset yet) and no register flag.

</details>

<details><summary>Advocate</summary>

Position: ship after changes. Every change below is text in `dataset.py` or one deterministic mask; none needs a
re-split, a new raw input or a retirement. Sources: the phase A reports in this folder.

**1. The target is repaired from the origin and verified (P5 PROV-13 Must, P3 USE-5 Must: hold)**

- Evidence: the shipped 2017-18/2018-19 `Score` adds the cell's ballot size + 1 (113-147) to no-vote ranks; recomputed
  with the NBA's own formula ("(Fan Rank * 2 + Player Rank + Media Rank)/4", pr.nba.com) it equals the official scores
  for all 958 matched rows (shipped: 28). The claim audit re-parsed two official 2019 PDFs: 214/214 equal. Season means
  go from 42.4 / 93.6 / 87.1 to 42.4 / 45.8 / 44.7; a model trained on 2016-17 scores R^2 0.718 on 2017-18 (shipped
  target: -0.95 to -1.07).
- The checklist's doubt that 2016-17 sits on another scale is refuted twice (claim audit, column audit): every cell of
  every season uses "voted in the cell + 1" for the unranked.
- Precedents: SUPPORT2, ashrae (PROV-13 applied); eryhemato tension (TP-6/USE-4): the formula is the source's and the
  NBA's, not our invention. This is the top rung of the remedy ladder (repair from origin) and answers the blind
  reviewer's "check how missing ranks were imputed".

**2. No leak survives; the post-vote statistics weaken the signal (P4 LEAK-10 Must holds; LEAK-11 Should applies)**

- Evidence: the six vote/rank columns, `Play`, `Rk` and names are dropped (column audit: "correct" for all). Leak probe:
  0.0% exact copies across the split; no task-probe flags. Statistics as of the vote's close beat the whole-season ones
  for three families (LightGBM 0.772 vs 0.741, paired SE 0.004; RF -0.010; ridge -0.019): later games carry no label.
  `wikipedia_daily_views` is the calendar year the season starts (claim audit: one player's 2016/17/18 means match the Wikimedia
  API to 2 decimals), so the blind reviewer's "All-Star attention spike" does not exist.
- Concede: the stated prediction point "the end of the regular season" breaks USE-3 (Must): the result is public in late
  January, and the definition contradicts its own `use_case` ("while the vote is open"). Mildest fix, text only: name
  the vote's close as the prediction point and keep the 25 statistics and `team` under LEAK-11 with a note, exactly as
  south_africa_coronary_heart_disease (Lennart, 2026-10-01). Fix "predict as well" to "predict better" in `fit_reason`.
- Why this outranks the "rebuild from box scores" alternative (issue 3 (b)): LEAK-11 is the rule written for this fact
  pattern and says keep; the rebuild needs a second raw input of unknown licence and vote-close dates not confirmed, and
  statistics re-derived from another source would not match the release, which PROV-14 (Must) makes a new dataset with
  its own record. It is an option for a sibling, not a precondition for this one. Concede: the 0.772/0.741 number was
  not re-run in phase A (no box scores on disk); it stands as documented with its SE.

**3. The split is the best the data allows and its cost is measured (P4: right with notes, split audit)**

- Evidence: the one temporal window that exists (train 2016-18, 66%; test 2018-19) scores 0.745 against grouped 0.744
  and ranks ridge / RF / LightGBM in the same order; IID 0.759 trains on test players' future seasons (correctly
  rejected, SPLIT-29/30). Only one window meets SPLIT-14's 50% floor (31% / 66%).
- Concede the rank point (precedents D2): USE-10 (part 2) outranks SPLIT-14 (part 4), so grouped is not a clean
  exception, and this is the third "too few periods" case (with open_university, distribution_transformers). What
  follows is an amendment for the curator (a SPLIT-8-style "forced from temporal, cost measured" rule), not exclusion:
  the remedy ladder ends in exclusion only for a Must that cannot be fixed, and the measured cost is ~0 on the one valid
  window (0.03 if `prev_score` is counted). SPLIT-8 / account_debt_south_africa is the nearest applied precedent: ship
  the closest regime, tag it, measure the cost. The tension "the right split against the score" (P4 over P6) is not at
  stake: no score argument is used.
- Mild fixes: add "untuned, 3 x 3 folds" to `splits_comment`; say held-out players are mostly veterans whose other
  seasons are hidden (SPLIT-23). Optional curator call: `prev_score` as a feature (USE-10), valid under the grouped split.

**4. Worth benchmarking (P6: TP rules hold)**

- Evidence (task probe, 30 splits): linear skill +0.710 (SE 0.005), beats the dummy on 100% of splits; best single
  feature +0.426; linear - RF +0.043 (paired SE 0.003); shallow tree 0.51-0.56 vs 0.74: not trivial, spreads families.
  660 groups, 220 test groups per fold, 445-490 test rows: not `Too Small` (TP-5). No flags.

**5. The use case is real and the target is what decides it (P3 USE-1/USE-5 Must: hold; USE-8 fit approximate)**

- Evidence: the score is the NBA's own selection quantity (top 2/3 per cell start); the practitioner keeps
  `fit=approximate` ("keep it; USE-8") and calls it "an acceptable approximate stand-in: real data, a real target
  repaired to official values". The alternatives are worse: `Play` is close to one feature (points per game alone AUC
  0.966; 19-28 positives per fold), log fan votes changes scale by season (4.7k / 4.6k / 13.1k medians).
- Answer to "RMSE is dominated by the tail" (claim audit: 77% of variance below the contenders; blind review): a concern,
  not a USE-5 violation; the ballot rank of every player is the official quantity and the source's goal (SEL-8). Restricting
  rows to contenders would be our own invention (eryhemato tension) and cut a 1,408-row task. Mildest fix: one sentence
  in `predicted`/`fit_reason`. Same for the missing fan returns: rephrase `use_case` to the actor before the first returns
  (practitioner's own wording); absent inputs lower fit, they do not make a leak.

**6. Stale pageviews: concede the departure, fix it in the definition (P5 PROV-13 Must)**

- Concede (precedents D5, column audit): 185 exact copies kept "as shipped" with a P4 reason for a P5 rule.
- Mildest fix that keeps the dataset: mask the 185 exact copies in `_clean` (deterministic from the raw file; -0.005 R^2,
  SE 0.003) and note the redirect undercounts that cannot be told apart. A full re-pull from the Wikimedia API is a
  curator call (a new raw input; PROV-14 if it would not match the release). The column is not the target and dropping
  it costs only -0.038, so the damage cannot change what the benchmark measures. Independent failures are not conflicts:
  this Must is met by the fix, it does not need to outweigh anything.

**7. Bookkeeping (writing.md, house rule): text only**

- Record `domain: Other` -> `social science`; record "no known risk" -> "known gap: stand-in prediction point and split".
  Optional: say in the licence the merged pageviews are CC BY-NC-SA 4.0 (already in comments; licence is never a reason
  to exclude, selection.md 2026-09-23).

Judgment record (advocate):
Verdict: ship after changes.
Validity: USE-5, PROV-13 (target) hold, repaired from origin; LEAK-10 holds (components and `Play` dropped); LEAK-11
applied to the whole-season statistics and `team`; USE-3 framing fixed in text; SPLIT-14 bars temporal, grouped kept
with cost measured (amendment due, third case); PROV-13 (pageviews) fixed by masking 185 copies.
Value: TP holds (skill 0.71, no flags).
Quality: P7 clean.
For the curator: the SPLIT amendment (three cases); masking vs re-pulling pageviews; `prev_score` as a feature.

**Rebuttal**

The critic and I agree on the verdict (ship after changes, no exclusion) and on the target repair. What is left is
which fixes are needed and in what order. Point by point:

**1. Prediction point after the outcome: concede**

- Same fix as my point 2: name the vote's close in `known` and the first comment bullet, keep the 25 statistics and
  `team` under LEAK-11 with a note, and change "predict as well" to "predict better".
- Also concede that `team` was never measured on its own (precedents D4). The LEAK-11 note should say the 0.772/0.741
  run swapped `team` together with the statistics, and that `team` has no separate number.
- The untested premise does not overturn the keep. The run is documented with a paired SE of 0.004 for three model
  families, and the column audit's checks are consistent with it: `team` is not label-driven, since a trade does not
  depend on the vote.
- Option (b), rebuilding the statistics from box scores, stays the curator's call. Nothing new here.

**2. Split and history: concede the `prev_score` fix, with one condition**

- USE-10 (Must, P3) names the previous outcome as a legitimate feature for a known entity. Adding it is a fix in the
  definition, which ranks above "keep with a note" on the remedy ladder, and it fits the grouped split.
- Evidence: +0.016 grouped (SE 0.004). It is the same player's earlier label, so it is always on the same side of the
  split.
- So I withdraw "optional" and support: `prev_score`, the corrected `split` text ("mostly veterans whose other seasons
  are hidden"), a "fallback from temporal" tag with the measured cost, and the amendment question in REVIEW.md.
- Condition: the feature is missing for all of 2016-17 (436 rows, 31%) by construction. The note has to say so, so that
  a model's missing-value handling is not read as a signal about a player.
- One correction to the critic's framing, not a dispute: the stand-in does not "measure cold start for veterans"
  at a different level from the real use. The one valid temporal window (0.745) and grouped (0.744) score the same and
  rank the model families the same way (split audit).

**3. Pageviews: concede the order of remedies; the choice between the two rungs is the curator's**

- PROV-13 puts repair from the origin first, and the claim audit shows the Wikimedia API reproduces the file for the
  players tested. I accept repair as the default.
- Why I proposed masking: the redirect undercounts cannot be told apart in the file. A full re-pull needs a title and
  redirect mapping that the release does not contain, and a rebuilt column that no longer matches the release raises
  PROV-14.
- The critic names the same fallback, masking the 185 copies. We differ only on which rung comes first, and that is a
  weighing call. Either rung meets PROV-13. Keeping the values "as shipped" is out.

**4. Target scored where no decision is made: concede the note, dispute one sub-claim**

- Concede: say in `predicted` or `fit_reason` that RMSE is dominated by non-contenders, and add the REVIEW.md question.
- Dispute that `context="none"` contradicts the cell-relative label. The cell is season x conference x ballot position,
  and all three are features in every row. The claim audit checked claim 30 on SPLIT-23 and found it holds: a model
  can see which ballot a row competes on. No change is needed beyond the note.

**5. Fit statement omits fan returns and prior vote: concede**

- Rephrase `use_case` to the actor before the first returns, and name both missing inputs in `fit_reason`.
- With the `prev_score` fix from point 2, the prior vote is no longer missing for 2017-18 and 2018-19. `fit_reason`
  should then name only the fan returns and the 2016-17 gap.

**6. Record and comment text: concede**

- Same as my point 7, plus the `splits_comment` settings. The comment should also say this panel's rerun put the
  temporal window marginally above grouped (0.745 vs 0.744), not below.

**Joint position for the mediator**

Ship after these changes:
- the USE-3 wording, with LEAK-11 notes covering the statistics and `team`;
- `prev_score` plus the corrected split text and the fallback tag;
- the pageviews repaired or the copies masked;
- the RMSE note and the use-case rephrasing;
- the record fixes.

For the curator:
- the SPLIT amendment (third "too few periods" case);
- re-pulling the pageviews or masking the copies;
- box-score statistics (issue 3 (b));
- whether to restrict the rows to contenders.

No disputed fact needs a new experiment.

</details>

<details><summary>Critic</summary>

Position: do not ship as defined; ship after the changes below. No point asks for exclusion: the task is real (the
NBA's own score, repaired and checked against the official tables), and the problems are in how the definition states
the moment, the split and one column. Sources: the phase A reports in this folder.

**1. The stated prediction point is after the outcome (P3, USE-3 Must; P4, LEAK-10 Must / LEAK-11 Should)**

- Problem: the first `curation_comments` bullet sets the prediction point at "the end of the regular season" so that
  25 whole-season statistics and the end-of-season `team` count as known. The vote closes mid-January and the score
  is public by late January (practitioner, pr.nba.com 2019: vote 25 Dec - 21 Jan, starters 24 Jan). At the stated
  point no one predicts anything; the definition's own `use_case` says "while the All-Star vote is open". The point
  was moved to make the features legal, which use_case.md's factor "a use case rephrased only to excuse a gap" names.
- Effect on the real task: the benchmark states a task that does not exist. Under the real point (the vote) the 25
  statistics, `games`, `games_started` and `team` (82 of 87 other-conference rows moved after the vote) are post-point
  values; whether they stay rests on LEAK-11 alone.
- Evidence: claim_audit claim 16/5 refuted; column_audit problem 1; precedents D3 (south_africa_coronary_heart_disease
  kept the point and called the values post-outcome; mic and kickstarter move points earlier, never later). The LEAK-11
  premise (vote-close statistics predict better, 0.772 vs 0.741, SE 0.004) is untested in this panel: it rests on one
  earlier run with box scores of unknown licence. `team` was never measured on its own (D4: swapped together with the
  statistics).
- Remedy (fix the definition): name the vote's close as the prediction point in `known` and the first comment bullet;
  keep the 25 statistics and `team` under LEAK-11 with a "measured after the outcome, weakens the signal" note citing
  the 0.772/0.741 run; fix `fit_reason` "predict as well" to "predict better". Option (b), vote-close statistics from
  box scores, stays the curator's call.

**2. The split tests a cold start the use case does not have, and drops the history it does (P3, USE-10 Must over P4, SPLIT-14 Must)**

- Problem: the use case is a new season of mostly known players (81% of 2018-19 rows, 73% of 2017-18 rows have an
  earlier season). USE-10 says a known entity gets a temporal split and its previous outcome as a feature. The
  definition ships a grouped split by player that hides every test player's other seasons, citing SPLIT-14. USE-10 is
  P3 and outranks SPLIT-14 (P4); a Must has no exceptions, so the departure is not a reasonable exception as written.
- Effect: the benchmark measures cold-start prediction for veterans whose history is hidden; the measured cost is
  small (grouped 0.736-0.744 vs newest-season holdout 0.745-0.752) but the stand-in drops the input USE-10 names:
  last season's score adds +0.016 (grouped) to +0.021 (temporal). The `split` text "players never seen" is wrong:
  held-out players are mostly multi-season veterans, not the young newcomers of a real season (0.740 vs 0.558).
- Evidence: split_audit problems 1-2; claim_audit row 6/9; practitioner gap 2; precedents D2: the third dataset
  decided by "too few periods for SPLIT-14" (with open_university and distribution_transformers, the latter rejecting
  exactly this stacked-and-grouped design), so an amendment is due.
- Remedy (fix the definition): add the previous season's score as a feature (`prev_score`, missing for 2016-17 and new
  players; known when the vote opens, same side of every grouped split), which brings the known-entity history USE-10
  asks for without a re-split; correct the `split` text; put the curator's amendment question (D2 options) in REVIEW.md
  and tag the split as a fallback from temporal with the measured cost, as SPLIT-8 asks of the one sanctioned fallback.

**3. A damaged column kept although its origin is reachable (P5, PROV-13 Must)**

- Problem: `wikipedia_daily_views` holds 192 of 856 later-season values that are copies of an earlier season or a 2016
  (366-day) mean, plus redirect-title undercounts. The definition keeps them "as shipped" with a P4 reason ("none
  leaks"), which answers no P5 question.
- Effect: the column is not what it claims (the season's pageviews) for 22% of later-season rows; small on the score
  (masking -0.005, dropping -0.038).
- Evidence: column_audit problem 2; claim_audit row 24 (the Wikimedia API reproduces the file to two decimals for
  two players' values, so the origin and its title mapping are reachable); the earlier REVIEW.md issue 7 (one player:
  6,292 / 6,145 at the API vs 4,679 shipped); precedents D5 (SUPPORT2, ashrae repaired; coad,
  corporate_credit_rating retired for a rebuild).
- Remedy: repair from the origin (the Wikimedia API per calendar year, as a second raw input). If the curator rules the
  title mapping out of reach, the next rung: mask the 185 exact copies in `_clean` (deterministic from the raw file)
  and note the redirect rows. Not "kept as shipped" without a reason.

**4. The target is scored where no decision is made (P3, USE-5 Must)**

- Problem: the actor acts on the top of each cell (2 guards, 3 frontcourt start; ranks below ~10 decide nothing). The
  target is a weighted rank over the whole ballot (92-140 players per cell) and RMSE weighs every row alike.
- Effect: 92% of rows score above 10 and carry 77% of the target variance; the benchmark mostly ranks the order of
  bench players by a few thousand fan votes. The label is also relative to the cell, while `context="none"`.
- Evidence: claim_audit implied row (23% of variance in rows <= 10); practitioner section 2; clean_room concern 2.
- Remedy (a note, not a re-target): say in `predicted` or `fit_reason` that the score covers the whole ballot and the
  error is dominated by non-contenders; a REVIEW.md question whether to restrict rows to contenders or offer a
  row-independent target (log fan votes, season-normalised). The rank is the NBA's and the source's own target, so
  no exclusion.

**5. The fit statement omits the inputs the named actor always has (P3, USE-8 Must, USE-6 Must)**

- Problem: a team's staff during the vote has the three published fan returns (top 10 per cell with votes, 3, 10 and
  17 Jan; the fan rank is half the score) and last season's vote. Neither is in the data; `fit_reason` names only the
  window and the split.
- Evidence: practitioner section 1 and gap 2.
- Remedy (fix the text): rephrase `use_case` to the actor without returns ("before the first fan returns ...") and name
  the missing returns and prior vote in `fit_reason`; fit stays `approximate`.

**6. Record and comment text disagree with the definition (writing.md, EV-8, house rule)**

- Record says "no known risk" while the definition documents a stand-in point and split; record `domain: Other` vs
  `social science`; `splits_comment` gives 0.751 / 0.747 / 0.769 without the settings (untuned, 3 x 3 folds), and this
  panel's rerun has the temporal window marginally above grouped, not below.
- Remedy: record "known gap: stand-in prediction point and split", align `domain`, add the settings to the sentence.

Not argued: the target recomputation (verified, 214/214 official rows in two re-parsed tables, the 2016-17 scale
concern refuted), the drops, missing values, `second_position`, the salary placeholders (P7 notes at most).

**Rebuttal**

We agree on the verdict (ship after changes) and on most changes. Two points are still disputed: `team` under LEAK-11,
and `prev_score`, which the advocate calls optional.

**Advocate 1 (target repaired and verified): concede**
The recomputation is the top rung of the remedy ladder. It was checked against the official tables, and the 2016-17
scale concern is refuted. My brief does not argue against it.

**Advocate 2 (no leak; LEAK-11 for the post-vote values): concede the statistics, dispute `team`**
- Concede: the prediction point is restated as the vote's close, the 25 statistics stay under LEAK-11 with a note, and
  "predict as well" becomes "predict better". I also accept that the rebuild from box scores is a curator option, not
  a precondition: its licence is unknown and the vote-close dates are unconfirmed.
- Dispute: `team` is put under the same note without its own evidence. LEAK-11 (Should) applies only to "a value
  measured after the outcome that weakens the signal". The 0.772/0.741 run swaps the statistics and `team` together
  (precedents D4). `team` carries real signal: dropping it costs 0.742 -> 0.702 (clean_room). 82 of the 87
  other-conference rows changed after the vote, and trades within a conference were not counted. So whether the
  end-of-season team weakens the signal is unmeasured. LEAK-10 (Must) holds unless the data shows it
  (melbourne_housing_market `Bedroom2`).
- Remedy: the mildest one. Either measure team at the vote against team at season end (the earlier run identified the
  82 moved rows), or have the note say plainly that this is unmeasured for `team`. The note must not claim the
  statistics' evidence for `team`.

**Advocate 3 (split best the data allows): concede the split, dispute "`prev_score` optional"**
- Concede: keep the grouped split, take the amendment question to the curator, add the settings and the "veterans
  whose other seasons are hidden" clause. Exclusion is not at stake.
- Dispute: the advocate concedes that USE-10 (P3, Must) outranks SPLIT-14 and is not met. The rule has two parts: a
  temporal split, and the previous outcome as a feature. The temporal part cannot be met, but the feature part can, and
  it works with the shipped grouped split. Both audits measure it: +0.016 R^2 grouped, +0.017 to +0.021 on the newest
  season. USE-6 (Must) makes it a legitimate input, since it is known when the vote opens. On the remedy ladder,
  "fix the definition" comes before "keep with a note". Leaving it optional keeps a Must unmet when part of it can be
  fixed.
- Remedy: add `prev_score` (missing for 2016-17 and for new players). Raise only the temporal part as the amendment.

**Advocate 4 (worth benchmarking): concede**
I raised no value point.

**Advocate 5 (use case real, tail of the target): concede**
I did not ask to restrict the rows or to re-target. A sentence in `predicted`/`fit_reason` is the remedy I asked for,
and so is the `use_case` rephrased to the actor before the first returns, with the missing returns and prior vote
named in `fit_reason`. One small addition: the note should also say that the label is relative to the cell, since
`context="none"`.

**Advocate 6 (stale pageviews): concede masking, correct one argument**
- Concede: masking the 185 copies plus a note is an acceptable fix now. The full re-pull goes to the curator.
- Correction: PROV-14 does not make a column repair "a new dataset". If it did, PROV-13 could never apply: the SUPPORT2
  and ashrae repairs did not match their releases either, and both are applied under PROV-13. The curator should
  decide the re-pull on whether the API's title mapping can be reached. The claim audit reproduced two players' values
  from the API to two decimals, so it can for those rows. The re-pull should not be decided on PROV-14.

**Advocate 7 (bookkeeping): concede**
Same items as my point 6. I add one: the `splits_comment` numbers need their settings.

</details>

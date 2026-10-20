# digicow_farmer_training_adoption_challenge

**Outcome:** added; recommended `No` (`Too Small`, `Data Quality Issue`). Zindi's DigiCow Train.csv as a temporal
binary task: does a farmer adopt within 7 days of a training (stored dates with day and month swapped back)? The AI
recommends retiring it; the folder stays for Lennart's decision.

**Main points:** Adoption was recorded in waves (a 0 often means "not recorded"); the newest windows hold 5-19 adopters.

**Record judgment:** do not ship: a 0 mixes "did not adopt" with "not recorded" (Data Quality Issue), and the temporal
windows hold 9, 5, 19 and 103 adopters from 1, 1, 2 and 7 trainers (Too Small); no split design fixes either.

**Issues for Lennart:**

1. **Retire as `No` with `Too Small` + `Data Quality Issue`.** Revisit if DigiCow documents when and for which
   trainers adoption was followed up.
   - Label recording, using Train.csv + Prior.csv in true dates:

     | Training month | 7-day adopters / 120-day adopters |
     |---|---|
     | Aug 2024 | 0 of 339 |
     | Sep 2024 | 0 of 237 |
     | Oct 2024 | 1 of 445 |
     | Nov 2024 | 147 of 326 (45%) |
     | Dec 2024 | 445 of 691 (64%) |
     | Feb 2025 | 112 of 118 (95%) |

   - 2024-12-12 lies inside the adoption interval of 1,028 of the 2,389 adopters. Three dates (2024-11-12,
     2024-12-12 and 2025-02-08) cover 1,972 of them (83%).
   - Mar-Oct 2024 has 21 7-day adopters in 36,664 rows (0.06%); Nov-Dec 2024 has 592 in 6,784 rows (8.7%).
   - TRA_gertumxc: 5-13% of its farmers adopted within 120 days for the Aug-Dec 2024 trainings. Then 0 of its 4,906
     rows from Mar-Jul 2025 adopted at any horizon, although those 120-day windows had closed before the release.
   - TRA_ubcgvofe: no 7-day adopter in 4,447 rows.
   - Too Small:
     - every adopter of the two newest windows is TRA_rkvyofbh's;
     - the 2024 window trains on 17 adopters, all of them TRA_hyodnntj's;
     - 1- to 3-month windows leave some windows without any adopter.
   - No other design fixes it:
     - IID: LightGBM 0.959 against a trainer x month lookup at 0.937;
     - grouped by `group_name`: 0.937 against 0.916;
     - leave one trainer out: one trainer with adopters per fold;
     - Prior.csv rebuild: the same waves (163 + 41 adopters in 2025, from TRA_rkvyofbh and TRA_kkzpfdtu).

2. **Date swap (confirmed by the verifier).** The stored `training_day` has day and month swapped, and the
   definition swaps them back.
   - Trainer-days:

     | | Mon-Thu | Fri | Sat | Sun |
     |---|---|---|---|---|
     | Swapped back | 16-20% each | 12.5% | 8.2% | 5.4% |
     | As stored | 13.3-15.8% on every weekday | | | |

   - Whole-week gaps between a group's sessions: 49.3% swapped back, against 14.7% as stored.
   - Swapped back, January holds almost no training (72 rows, none in Train.csv).
   - Timing-class coherence: 83% swapped back against 58% as stored.
   - Caveat: swapped back, 700 rows fall on Labour Day 2025 and 331 on Easter Monday 2024.
   - Only days 1-12 of each month survive. In true dates, the challenge's Train/Test cut splits 2025 by day of month,
     and 20.3% of the Train farmers' Prior rows come after their Train row.
   - Worth telling Zindi or DigiCow.

3. **Prior.csv is not used.**
   - As shipped, its history leaks later outcomes (the swap).
   - Rebuilt in true dates, history features add AUC -0.02 to +0.16 per window.
   - It carries the same recording waves.

4. **`has_topic_trained_on`: dropping it alone is incomplete. Drop both columns or keep both; Lennart's call, moot if
   retired.**
   - It goes with the adoption for two trainers: in mixed sessions, the 195 flagged farmers hold all 56 adopters.
   - It may simply mark the farmers whose adoption could be recorded at all (flag 0 never adopts, in 5,201 rows).
   - `topics_list` predicts the flag with AUC 0.870 in the two trainers' 4,195 rows (5-fold CV grouped by session),
     and 0.796 inside the 82 mixed sessions.
   - No code change: the definition drops the flag only.

5. **Target: 7 days.** Zindi's own scoring rubric (API field `benchmark_submission_private_scoring_rubric`) weights:
   - 7-day log loss 0.65;
   - 7-day AUC 0.15;
   - 90-day and 120-day log loss and AUC 0.05 each.

   The 90- and 120-day targets show the same waves.

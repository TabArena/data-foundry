# bank_marketing

**Outcome:** added. UCI's bank-full file (45,211 records of a Portuguese bank's term-deposit phone campaigns, May 2008 to November 2010, one per client and campaign), predicting a subscription before the campaign's first call, scored by ROC AUC on five time windows of the file's date order. A focused re-review of 2026-11-06 recommended shipping after changes; those that needed no decision are made in `dataset.py`, and the README is regenerated; the build stays stale until you ask. Settled on 2026-11-08: the split, by time on the file's date order, in place of the random split kept under your earlier call (issue 1); the prediction point, before the campaign, so `campaign` is dropped (issue 2); the duplicates, kept with a note (issue 3), now 811 exact copies on the twelve inputs since `campaign` left (274 before); and the record's `year`, set to 2012. Open: whether the month of the last call comes back as an input (issue 4). New on the windows: the newest one holds both records of 703 recurring clients, and the later record gives 419 subscribers away to a model that reads other test records; a protocol line covers it. Not checked on this tier: whether the authors' 2014 release of the same campaigns (with the month and weekday of each call, economic context and the true phone type of May-June 2008) is the better version; no provenance reviewer ran.

Validity: LEAK-17 and SPLIT-29 fixed by the split by time (issue 1): a client's later record never trains, and SPLIT-1, SPLIT-5, SPLIT-7, SPLIT-19 and SPLIT-22 hold on the file's date order. Inside the newest window recurring clients leave an evaluation leak, covered by a protocol line (LEAK-9). USE-3 holds: the prediction point is before the campaign's first call, and `campaign` is dropped (issue 2). LEAK-10 holds for `contact` and `pdays`. LEAK-41 and MET-15 do not apply (no weight).

Value: MET-1, MET-2 and MET-5 hold (ROC AUC is the source's selection criterion); 279 to 2,129 positives per test window. On the windows the signal is weak but there: LightGBM 0.522 to 0.679 (mean 0.586), logistic regression mean 0.614, against 0.76 on the random split; the task probes' best family (random forest, 0.631) beats the dummy on 5 of 5 windows, flagged `no_spread` (TP-3), which the tuned results cannot settle here, as they ran on the random split.

Quality: CLEAN-10 applied (`job`'s "unknown" missing; the reason for `pdays` = -1 written and its warning accepted); LEAK-16 decided: the exact copies kept with a note (issue 3, 2026-11-08), 811 on the twelve inputs since `campaign` left, 89% of them with a balance of 0; the wrong or one-sided sentences of the notes rewritten.

Weighed: source + (a paper with a stated metric), use case + (a real decision), split + (by time, as the source evaluates), signal - on the windows.

Left for you: issue 4. Settled on 2026-11-08: issues 1, 2 and 3 and the `year` field (the record now takes the definition's 2012, UCI's release, in place of 2011, the ESM paper, which only analysed the data).

**Main points:** Bring back the month of the last call as an input (issue 4)? Settled on 2026-11-08: split by time on the file's date order, reversing your call that kept the random split (issue 1); before the campaign, so `campaign` is dropped (issue 2); the exact copies kept with a note (issue 3); the record's `year` set to 2012.

**Record judgment:** valid, keep (`Yes`), after changes. The record's `year` (2011, the ESM paper, which only analysed the data) disagreed with the definition's 2012 (UCI's release, donated 2012-02-13); it was set to 2012 on 2026-11-08 (Lennart, `update`). Its `required_split` is `Temporal (NON-IID)`, with the tag `Non-IID (Temporal)`, since 2026-11-08 (issue 1). Its comment that the features "seem to be time-invariant" is superseded by an Assessment line of 2026-11-06 giving the measured shift by year; a second line of that date records this panel.

**Issues for Lennart:**

1. **Split by time on the file's date order instead of at random?**

   * **Problem:**
     - The same clients recur across campaigns, and the random split puts a client's later row in training next to its earlier row in test, where the later row's `poutcome` (the outcome of the previous campaign) is the earlier row's label.
     - The random split also lets a model learn each period's subscription rate (5% in 2008, 52% in 2010) from rows of the same period, which a bank choosing whom to call in its next campaign never has.
     - The file is in date order and the source evaluates on time-ordered windows, but your earlier call kept this dataset on a random split as optimistic yet true to how the task is framed[^split31].
   * **Background:** UCI ships the file "ordered by date", and the year and month rebuild exactly from where the months wrap (2008: 27,729 rows, 2009: 14,862, 2010: 2,620)[^order]. 995 pairs of rows in two different years share the profile and the balance to the euro; in 95% of them the later row counts more earlier contacts, and where the earlier row subscribed, the later row's `poutcome` says "success" in 562 of 581 pairs (97%). Moro et al. (2014, p. 5) find a random split does "not reflect the temporal dimension that a real prediction system would have to follow" and score their model on rolling windows in time. A split grouped by a client key rebuilt from the profile is no clean way out: the key is a near match (age within a year, balances near zero unmatched), not an exact id[^split24]. Under a split by time a client's earlier rows sit only on the training side, where they are legitimate history[^leak34].
   * **Effect on the task:** Under the random split, about 557 test rows per fold (3.7%) have the same client's later row in training, and in about 186 of them, 10.6% of the fold's positives, that row says "success". A model that matches clients (a nearest-neighbour or in-context learner can; the shipped LightGBM cannot without help) scores better than it would on a bank's next campaign, and every model profits from the period's base rate. The honest split costs a lot: most of the random split's 0.76 ROC AUC comes from telling the periods apart.
   * **Experiments:** On the 9 shipped splits LightGBM scores 0.7627 ROC AUC, and 0.7827 with a lookup of the client's later row built from training features only (+0.020, SD 0.0024, higher on 9 of 9 splits); the later row's `poutcome` alone ranks the matched test rows at ROC AUC 0.97 to 0.99. The period alone adds 0.026 (year) to 0.042 (year and month) under the random split. Five expanding windows on the file order (each test window 4,521 rows, training on 50% to 90% of the rows), LightGBM with 2 seeds: 0.438, 0.582, 0.603, 0.618, 0.569, mean 0.562; with a fixed 300 trees 0.49 to 0.66, logistic regression 0.47 to 0.69. The same test windows with an equal-size random training set drawn from all other rows: 0.54 to 0.70.
   * **Consistency:** Option A departs from your call that kept amazon_employee_access and bank_marketing on a random split[^split31], on facts that set this dataset apart: the source's own evaluation is in time, the date order is recoverable, a recurring client carries the label, and the base rate moves tenfold; amazon_employee_access is not affected. The datasets shipped on a forced random split (account_debt_south_africa, bemtpl97, fremtpl2, the churn snapshots) had no dates or too few periods; this file gives five windows, each training on at least half the rows[^split8]. A weak score under the right split is no reason to keep the wrong one, as decided on forest_fires[^p4].
   * **Panel:** The claim auditor found the leak and recommends the split by time; the column auditor did not test the split; the mediator recommends A by rank and leaves it to you, as it reverses your call and lowers the scores a great deal.
   * **Unknown:** Whether the task by time has enough signal: the first window is below chance, so the task probes would run on the windows under A. Whether the authors' 2014 release (bank-additional-full, with the month and weekday of each call, economic context and the true phone type of May-June 2008, in the same UCI zip) is the better version: no provenance reviewer ran on this tier.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Split by time on the file's order | the year and month rebuilt in `_clean` as the time key; five expanding windows, the first training on half the rows; the task text, the record's split and your earlier case updated | mirrors a bank choosing whom to call next; removes the recurring-client leak; follows the source's evaluation | reverses your earlier call; mean ROC AUC about 0.56 to 0.62 instead of 0.76; the first window scores below chance |
     | B | Random split (implemented) | the split stays; the notes and the fit text state the recurring-client leak (+0.020) and the period effect; the rule on recurring entities is amended to allow it | keeps your earlier call; scores as now | a known leak stays across the split; the test rows do not stand for a later campaign |

   * **Recommendation:** A, by rank: the rules against the recurring-client leak and for a split that mirrors the application are firm ones, your earlier call applied a weaker one, and the date order exists, so the random split is not forced[^rank]. Under A, a short follow-up question asks whether the call month comes back as a feature (the source keeps it as an input, and the period is known when a campaign is planned). **Decision:** split by time (A), or keep the random split and amend the rule (B)?

   **Notes for the AI:** on A, in `dataset.py`: rebuild the year in `_clean` from the file order (it steps up where the month sequence wraps from December to January) and use year and month as the time key; declare a temporal split with five expanding windows at the 50% floor (test windows of 4,521 rows, SPLIT-14); rewrite `split`, `fit`, `fit_reason` and `data_tags`; set the record's `required_split` to `Temporal (NON-IID)` with the `Non-IID (Temporal)` tag; move bank_marketing out of the SPLIT-31 Cases row in splits.md (and the matching line of leak_checks.md) with the facts that set it apart; run the task probes on the windows. On A, raise the call month as a new issue (LEAK-10, USE-6). On B: amend LEAK-17 or SPLIT-29 (a Must takes no exception) and write the +0.020 and the period effect into the notes and `fit_reason`. Under both options the task summary's `split` ("Random clients ... other clients") is refuted and is rewritten.

   **Consistency check (AI, 2026-11-08):** Your mark keeps the random split (B); what sets bank_marketing apart from
   the dated tasks that went to a split by time?

   * **Problem:**
     - B keeps a measured leak across the split (a recurring client's later row: +0.020 ROC AUC) and the period's base
       rate (5% to 52%), on a file whose date order the source states and that rebuilds into five windows above the
       floor[^b1a].
     - The rules on recurring entities are of the kind that changes only by amendment, and forest_fires settled that a
       weak score under the right split is no reason to keep the wrong one[^b1b].
     - Your earlier keep (SPLIT-31's case row, 2026-10) came before the leak and the period shift were measured, and the
       mark has no note, so no fact that sets the case apart is on record yet.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Split by time (the issue's A) | five expanding windows on the file's order; bank_marketing leaves SPLIT-31's case row | no rule changed; follows the source's own evaluation and forest_fires | mean ROC AUC about 0.56 instead of 0.76; reverses the earlier keep |
     | b | Amend the rules, as marked | e.g. "an IID split may stay over recurring entities on dated data when the leak is measured and stated and the windows leave little signal" | keeps the scores | needs the rules on recurring entities and on mirroring the application changed too; lets the score pick the split, which the rules' tensions forbid; reaches every dated task |
     | c | Forced IID with the leak in the notes | tag forced from temporal; the +0.020 and the period effect stated as an approximate fit | no rule text changed | the forced regime is for a release that cannot give the windows, and this one can |

   * **Recommendation:** (a): no amendment found holds in general without letting the score decide the split.
   * **Decision:** (a), (b) or (c)? A fact that sets this case apart, if you see one, keeps (b) open as an exception.

   **Notes for the AI:** the steps for A and B are in the issue's notes above; issue 2's answer gives `campaign`'s
   worth under both splits.

   **Lennart (2026-11-08, ok):** Reply (a): Split by time (the issue's A)

   **Resolved (2026-11-08, Lennart):** A, split by time: five expanding windows of 4,521 records on the file's date
   order (training on 50% to 90% of the records), keyed by the record's position in the file once `_clean` has checked
   the rebuilt dates against it (a month or a date as the key would leave records of the cut's day on both sides);
   the task text, the notes and the record's split changed. On the windows LightGBM scores ROC AUC 0.586 on average
   (0.522 to 0.679) and logistic regression 0.614, against 0.76 at random; the month of the last call is issue 4, and
   the newest window's recurring clients get a protocol line.

   [^b1a]: **LEAK-17**, **SPLIT-29**, **SPLIT-1**, **SPLIT-7** (Must); **SPLIT-22**, **SPLIT-19** (Should); **SPLIT-8**
     (Must) for forced splits.
   [^b1b]: principles.md, "Strengths", "Exceptions and amendments" and "Tensions" ("The right split against the score",
     P4 over P6; forest_fires); **SPLIT-4**.


   [^split31]: **SPLIT-31** (Should): over related entities, a random split can match how a task is framed even when it is optimistic; such a task is a candidate for a grouped or temporal variant, not a fix. Cases: amazon_employee_access, bank_marketing (applied).
   [^order]: **SPLIT-22** (Should): the raw file order can be the time order without a timestamp; keep it. **SPLIT-7** (Must): a missing or hidden timestamp does not make a task IID.
   [^split24]: **SPLIT-24** (Must): group on a true group id, or on one constructed exactly from the data; never on a similarity cluster.
   [^leak34]: **LEAK-34** (Must): an entity's own history under a temporal split is legitimate, also when it carries labels forward.
   [^split8]: **SPLIT-8** (Must): a task that is temporal by its use case but whose release cannot give the windows ships in the closest regime, tagged as forced from temporal. **SPLIT-14** (Must): at least 3 windows, and no window's training side holds less than 50% of the data.
   [^p4]: **P4** (honest evaluation: only what is known at the prediction point, and a split that mirrors the application) ranks above **P6** (worth benchmarking).
   [^rank]: **LEAK-17** (Must): repeated entities in different rows leak the target across the split even when the rows differ: keep one row per entity, or group. **SPLIT-29** (Must): a random split is wrong when many rows share an entity that new data would not have and the entity carries the label. **SPLIT-1** (Must): the split mirrors the real-world application. **SPLIT-19** (Should): follow the split the source defines, which is still a claim to check (**SPLIT-5**, Must). SPLIT-31 is a Should, and a Must has no exceptions, so keeping the random split needs an amendment (principles.md, "Exceptions and amendments").

2. **Is the model used before the campaign, so `campaign` goes, or at a call during it, so it stays?**

   * **Problem:**
     - `campaign` counts this campaign's calls to the client, the last one included, and the calls end at a subscription or when the bank stops calling.
     - The use case has the team pick which clients to call before any call of the campaign, when `campaign` exists for no row, yet the task summary lists it as known[^use3].
     - The source frames the decision as choosing the next client to call during a campaign, with the calls made so far as an input, and which of the two moments ships decides whether `campaign` may stay.
   * **Background:** Before the campaign nothing keeps the column: it did not exist then[^leak10], and a late value stays only when it weakens the signal[^leak11], which `campaign` does not. At a call during the campaign (the source: "selecting the next customers to be contacted during bank marketing campaigns", with the "number of previously scheduled calls during the same campaign" as an input, Moro et al. 2014, Table 2), the calls so far are `campaign` minus one, a constant shift; what remains is the last call, which a subscription or the bank's stopping rule ends, the case your ruling of 2026-11-06 keeps with a note giving its worth: a count whose end the outcome or the bank's own stopping rule sets[^span]. Under A and under B the `known` text changes, as it now lists this campaign's calls at a moment before the campaign; that change waits for your choice.
   * **Effect on the task:** Kept, `campaign` tells a model how long this campaign's calls to the client ran, and the outcome ends them for subscribers: at a fixed period, fewer calls go with more subscribing (2009: 19.0% at 1 call, 7.2% at 6 to 10). The gain is small: 0.006 ROC AUC, about 0.0013 once the period is known.
   * **Experiments:** LightGBM, 9 splits x 5 seeds: dropping it costs 0.0060 ROC AUC (lower on 9 of 9), logistic regression 0.0079; given the year of the last contact 0.0013 and 0.0016, about one seed SD, and given the year and month 0.0012. Within each year and month, clients called once subscribe 1.26 times as often as those called 4 or more times. Under the five time windows of issue 1 it is worth +0.0035 on average, from -0.006 to +0.020.
   * **Consistency:** A follows heart_failure_followup_survival, whose `time` (the follow-up from baseline to death or censoring, the same shape) was dropped as recorded after the prediction point. B fits that ruling as applied to noaa_storm_events_damage's `duration_hours` (kept with a note; that span closes before its prediction point), and the ruling must then name what sets bank_marketing apart from heart_failure: the prediction point lies inside the span, while heart_failure's baseline lies before it. Keeping `campaign` with the current use case would depart from heart_failure on size alone, and a confirmed leak goes even when small[^leak6].
   * **Panel:** The column auditor recommends dropping it, as the count does not exist at the use case's moment; the claim auditor recommends rewording the use case to the source's framing and keeping it, as you decided on 2026-11-06; the mediator finds both valid and the current pair of texts not.
   * **Unknown:** A release with one row per call would make B exact; the files keep only each client's last call per campaign, so under B the earlier failed calls to eventual subscribers are missing. A use case reworded only to close a gap weighs against B, though here the wording is the source's[^use9].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Before the campaign, drop `campaign` | `campaign` dropped (13 to 12 features); `known`, `changes`, `fit_reason` and the ruling's entry updated | follows heart_failure; keeps the use case as written; costs 0.006 ROC AUC, about 0.0035 under the time windows | departs from the source's framing; reverses your keep of 2026-11-06 |
     | B | At a call during the campaign, keep `campaign` | `use_case`, `row` and `known` reworded to "which client to call next", with the calls so far known and the row being the client's last call; the note stays; the ruling names what sets it apart from heart_failure | follows the source; keeps your decision of 2026-11-06; no column lost | only the last call per client and campaign is in the data; a use case reworded to fit the columns |
     | C | As now: use case before the campaign, `campaign` kept (implemented) | nothing changes | no work; no column lost | the inputs list a count that does not exist at the stated moment; departs from heart_failure on size alone |

   * **Recommendation:** Either A or B, not C: both A and B are valid, and the current pair of texts (C) is not. A is the cheaper to defend (it follows heart_failure and keeps the use case as written); B follows the source and your call of 2026-11-06. **Decision:** before the campaign without `campaign` (A), or at a call during it with `campaign` (B)?

   **Notes for the AI:** the mediator's change i waits for this decision (USE-3, Must): `known` must agree with the stated prediction point. On A: drop `campaign` in `_clean`; remove "the number of calls in this campaign" from `known` and add the drop to `changes`; rewrite the last sentence of `fit_reason`; turn the `Potential leak, kept on purpose:` bullet into a drop bullet (after the prediction point, LEAK-10); in leak_checks.md's span row, replace the bank_marketing entry with "dropped, after the prediction point"; add a first notes bullet naming the prediction point (before the campaign's first call; known then: the client's profile and the earlier campaigns). On B: reword `use_case` (during a term-deposit campaign, the team picks the next client to call), `row` (the client's last call in one campaign) and `known` (the calls made to the client so far in this campaign); keep the note; add the distinguishing fact to the span row; add a first notes bullet naming the prediction point. Re-run `dataset check` either way.

   **Lennart (2026-11-08, discuss):** How much smaller would the data become with (B) and how far away form the real
   use case is (A)?

   **Answer (AI, 2026-11-08):** Neither option drops a row: B's gap is the calls the release leaves out, A's is one
   input the source used.

   * **Problem:**
     - B keeps all 45,211 rows, but its moment (the next call) needs a row per call, and the release keeps only each
       client's last call: 45,211 of the campaign's 124,956 calls (36%).
     - A keeps the same rows and moves no text away from the use case as the summary states it (the team picks whom to
       call); it loses only this campaign's call count, worth 0.006 ROC AUC.
   * **Background:**
     - Counted on `bank-full.csv`: the 79,745 calls the release leaves out (64%) are each client's earlier calls, 6,035
       of them failed calls to clients who subscribed later; 17,544 rows (39%) had a single call, where both moments
       coincide.
     - Under B the rows are therefore no sample of the calls a model would score: each subscriber appears at the call
       that succeeded, each non-subscriber at the call after which the bank stopped, and no filter can rebuild the
       calls in between, since the release does not have them.
     - Under A the moment is before the first call, the inputs are the profile and the earlier campaigns, all known
       then, and every row is a client the bank did call, as a list drawn for the next campaign would be[^a2b]. The
       source frames its model at a call during the campaign (Moro et al. 2014, Table 2), with the calls so far as an
       input; that is the one point where A departs from it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | A: before the campaign, drop `campaign` | 13 to 12 features; `known`, `changes`, `fit_reason` and the span row's entry updated | the use case as written; no row lost; every input exists at the moment | departs from the source's framing; -0.006 ROC AUC (about -0.0035 under time windows) |
     | b | B: at a call during the campaign, keep `campaign` | `use_case`, `row` and `known` reworded to the next call | follows the source; keeps your keep of 2026-11-06 | the rows are 36% of the calls and selected by how each client's calls ended |
     | c | As now (implemented) | nothing changes | no work | the inputs list a count that does not exist at the stated moment |

   * **Recommendation:** (a): it matches the use case the task states with the data as released, while (b) needs rows
     the release does not have.
   * **Decision:** (a), (b) or (c)?

   **Notes for the AI:** the steps for A and B are in the issue's notes above. Counts from `bank-full.csv` (45,211
   rows; `campaign` sums to 124,956).

   **Lennart (2026-11-08, discuss):** Reply (a): A: before the campaign, drop campaign

   **Resolved (2026-11-08, Lennart):** A: the prediction point is before the campaign's first call, and `campaign` is
   dropped (twelve inputs and the time key); `known`, `changes`, `fit_reason` and the notes say so, the notes opening
   with the prediction point. On the five time windows `campaign` had added +0.0065 ROC AUC to logistic regression
   (higher in 5 of 5) and -0.014 to LightGBM (higher in 1 of 5).

   [^a2b]: **USE-3** (Must): name the prediction point and what is known then. **USE-9** (Should): weigh another use
     case practitioners have against one rephrased to excuse a gap.


   [^use3]: **USE-3** (Must): name the prediction point, when the model is used and what is known then; a value that did not exist at that point is a leak.
   [^leak10]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target away.
   [^leak11]: **LEAK-11** (Should): a value measured after the outcome that weakens the signal stays, with a note.
   [^span]: The span row of **LEAK-10** and **LEAK-37** (2026-11-06, Lennart): a span whose end the outcome or an outcome-free criterion draws stays with a `Potential leak, kept on purpose:` note giving its worth; it names bank_marketing `campaign` as kept. **LEAK-37** (Must): an input the actor knows at the prediction point is not a leak.
   [^leak6]: **LEAK-6** (Must): measure before acting; a confirmed leak goes even when small.
   [^use9]: **USE-9** (Should): ask whether the data mirrors another well-defined use case practitioners have; weigh it against a use case rephrased only to excuse a gap. **USE-1** (Must): a use case is an actor, a moment and a decision.

3. **Keep the 274 exact copies, with a note?**

   * **Problem:**
     - 274 rows are exact copies of another row, label included, and 32 more share every feature with another row but carry the other label, with no decision on them written[^leak16].
     - Under the random split 0.9% of the test rows have a copy of every feature in training, 0.8% one with the same label too.
   * **Background:** Thirteen columns with a balance to the euro would make a chance match rare, which points to a collection artefact[^leak18]; but almost all copies have a balance of 0, so most are clients with an empty account and a common profile, which can be distinct clients or one client in two campaigns (issue 1). Under a split by time (issue 1, A) an earlier copy is the client's history[^leak34b].
   * **Experiments:** Counts made when writing this file (2026-11-06, not by the panel), on the shipped frame and splits: 274 exact copies with the label and 306 copies of every feature, so 32 more rows carry a label that no earlier copy of their features had (32 groups of identical features hold both labels); the bundle check counts them the same way. The panel's reading, 32 of the 274 with conflicting labels, does not hold: a copy with the label cannot conflict. Per fold, 0.88% of the test rows (0.81% to 0.98%) have a copy of every feature in training and 0.79% (0.69% to 0.90%) one with the same label. Of the 494 rows in groups of exact copies, 92.7% have a balance of 0, against 7.8% of all rows.
   * **Panel:** The claim auditor raised it; neither auditor argued keep or drop; the mediator leans to A, with the numbers.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the rows (implemented), add a note | the rows stay, as now; the note with the counts and the reason is added on A | most copies are plausible repeats (balance 0, a common profile); under a split by time a copy is history | 0.9% of the test rows have a copy in training under the random split |
     | B | Drop the exact copies | 274 rows fewer (0.6%); the 32 feature-copies with the other label stay | no exact copy across the split | may remove distinct clients; changes little |

   * **Recommendation:** A, with the numbers: the copies are few and mostly plausible repeats. **Decision:** keep with a note (A), or drop the copies (B)?

   **Notes for the AI:** on A, add a notes bullet: "Duplicates (LEAK-16, LEAK-18): 274 exact copies (0.6%, label included) and 32 feature-copies with the other label; 93% of the copy rows have a balance of 0, plausible repeats of common profiles, so they stay; under the random split 0.9% of the test rows have a copy of every feature in training, 0.8% one with the same label." On B, `df = df.drop_duplicates()` in `_clean` after the column drops, and give the share in the notes. Re-run `dataset check` either way.

   [^leak16]: **LEAK-16** (Must): duplicate rows need a decision every time.
   [^leak18]: **LEAK-18** (Should): many degrees of freedom and an exact match point to a collection artefact (drop it and give the share); few features and plausible repeats are natural (keep them and say so).
   [^leak34b]: **LEAK-34** (Must): an entity's own history under a temporal split is legitimate.

   **Resolved (2026-11-08, Lennart):** A, as implemented: the 274 exact copies stay, and the notes gain the duplicates
   bullet with the counts and the reason (93% of the copy rows have a balance of 0, plausible repeats of common
   profiles; 0.9% of the test rows have a copy in training under the random split). `dataset check`: 0 errors, 0
   warnings (the copies show as info, 274 and 32 rows).

4. **Bring back the month of the last call as an input?**

   * **Problem:**
     - The source keeps the month of each call as an input, and the period of a campaign is known when it is
       planned[^m4a].
     - This file holds only the month of each client's last call, which the end of the calls sets, so it left with
       the day[^m4b].
     - On the five time windows the month adds nothing measurable, and the record's place in the date order is an
       input already.
   * **Background:** The source lists "month in which the call is made" among its inputs (Moro et al. 2014, Table 2),
     with one row per call; this release keeps one record per client and campaign, dated by its last call. `_clean`
     rebuilds the year and month only to check the file's date order and does not ship them; the time key, the
     record's position in the file, carries the period. A month as a category would add the season, but in the two
     oldest windows most test records fall in months with no record in training (the oldest window, August to
     November 2008, trains on May to August 2008).
   * **Effect on the task:** Brought back, the month tells a model the season and, inside a window, the period; for a
     subscriber it is also the month the calls stopped.
   * **Experiments:** On the five windows (LightGBM with 3 seeds and early stopping on the newest tenth of the
     training side; logistic regression), adding the month of the last call as a category changes ROC AUC by -0.0096
     for LightGBM (higher in 1 of 5 windows; seed SD 0.029 per window) and by -0.0019 for logistic regression (higher
     in 1 of 5); with `campaign` back as well, by -0.0044 and +0.0050. Under the random split the year and month
     together were worth +0.042 to LightGBM, with the records of each month on both sides of the split, which no
     window has but for the month of its cut.
   * **Consistency:** Leaving it out follows issue 2, which dropped `campaign` as set during the campaign; bringing it
     back would keep a value of the last call next to that drop, on the ground that it mostly marks the planned
     period[^m4c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave it out (implemented) | the month stays dropped with the day | every input exists before the first call; the period is in the time key | departs from the source's inputs |
     | B | Bring the month back | `month` kept in `_clean` as a category of 12 levels | the source's input; the season | the month of the last call, which the end of the calls sets; no gain on the windows |

   * **Recommendation:** A: on the windows the month adds nothing, and the value this file holds is the last call's.
     **Decision:** leave the month out (A), or bring it back (B)?

   **Notes for the AI:** on A, a CC line in the record. On B: keep `month` in `_clean`, mapped to 1 to 12 from the
   names and typed categorical in `_feature_types`, rewrite the dates bullet of the notes and `known`, and re-run
   `dataset check` and the task and leak probes; the measurements are in the record's Assessment of 2026-11-08.

   [^m4a]: **USE-6** (Must): anything known at the prediction point is a legitimate input. **LEAK-37** (Must): an
     input the actor knows at the prediction point is not a leak.
   [^m4b]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target
     away.
   [^m4c]: Issue 2 of this file (2026-11-08, Lennart): before the campaign, `campaign` dropped. **USE-3** (Must): name
     the prediction point, when the model is used and what is known then.

**Review panel:** ship after changes (mediator). Tier focused (claim auditor, column auditor, mediator), a re-review of 2026-11-06 under LEAK-41 and MET-14 to MET-16, which do not apply here (no weight, no rate target). Claims: 33; 22 hold (6 of them with a caveat), 8 refuted or partly refuted (5 fixed in wording; the use case's moment and the split go to issues 1 and 2, the record's year to the field row), 1 not established (when `pdays` is counted) and 1 untested (the date of `balance`), both reworded as notes, 1 not applicable. Blind review: not run on this tier. Agreed: `contact` and `pdays` stay; the measured worth of `campaign`; the recurring-client leak (raised by the claim auditor, not contested); the mediator's changes a to h, applied (change i waits for issue 2). Disputed: keep or drop `campaign`, which turns on the prediction point (issue 2); settled in wording: whether cellular and telephone differ within a period (change a) and when `pdays` is counted (change c).

<details><summary>Mediator</summary>

**Mediator report: bank_marketing (focused tier, exposure re-review, 2026-11-06).** Inputs: the claim auditor's and the column auditor's reports, the earlier measurements of `campaign` and `contact`, the probes, the definition and the record, the rules. Own check: temporal windows on the file's date order (section 2).

**1. Judgment record**

- Verdict: ship after changes. Two of the changes need the curator: the split (issue 1) and the prediction point that decides `campaign` (issue 2).
- Validity: LEAK-17 / SPLIT-29 triggered (repeat clients: a later row's `poutcome` gives away the earlier row's label across the random split, +0.020 ROC AUC once the match is made), not fixed. SPLIT-1 / SPLIT-5 / SPLIT-7 / SPLIT-19 point to a temporal split on the file's date order, against the SPLIT-31 precedent that names this dataset as IID. USE-3 fails as written: the use case is before the campaign, yet `known` lists this campaign's call count. LEAK-10 holds for `contact` and for `pdays`. For `campaign` it depends on issue 2. LEAK-16: no decision written. LEAK-41 and MET-15 do not apply (no weight).
- Value: MET-1, MET-2, MET-5 hold (roc_auc is the source's selection criterion). TP is fine under IID (1,763 positives per test fold). Under the temporal remedy the signal is weak: mean ROC AUC 0.56 to 0.62, and the first window is below chance (my check below). That is a P6 fact. It is no reason to keep the wrong split (P4 over P6, forest_fires).
- Quality: CLEAN-10 departures: `job` "unknown" is kept as a level, and the reason for keeping `pdays` = -1 is not written. Several sentences in the notes are wrong or one-sided (list below).
- Weighed: source + (a paper with a stated metric), use case + (a real decision), gap - (IID on dated data), signal - under temporal.
- For the curator: issue 1 (split: temporal, recommended by rank; it reverses a precedent you applied), issue 2 (prediction point: drop `campaign`, or reword the use case to the source's "which client to call next" and keep it; a weighing call), issue 3 (duplicates, low).

**2. Agreed facts** (neither report contests them; the claim auditor checked the numbers against the earlier runs)

- Rows: 45,211, 11.70% positive. The file is in date order (UCI: "ordered by date"). The year rebuilds from where the months wrap: 2008 has 27,729 rows (5.05% positive), 2009 has 14,862, and 2010 has 2,620 (51.6%).
- `campaign` (UCI: "includes last contact"). Dropping it costs 0.0060 ROC AUC with LightGBM (9 of 9 splits lower) and 0.0079 with logistic regression. Given the year it is worth 0.0013 and 0.0016, about one seed SD. Given the year-month it is worth 0.0012. The rate is flat over 1 to 10 calls in 2008 (rate ratio 1.05). It is not flat in 2009 (19.0% at 1 call, 7.2% at 6-10) or in 2010 (51.9% to 39.2%). Mantel-Haenszel rate ratio within the year-month: 1.26.
- `contact`: dropping it costs 0.021. Its "unknown" covers all 12,443 rows of May-June 2008. Replacing it by an unknown-or-not flag costs 0.0005, so 97% of its worth is the period flag. The raw rates of cellular and telephone do differ within a period (2009: 17.4% against 13.6%; 2010: 57.1% against 45.5%). The 2014 release codes May-June 2008 as "telephone".
- `pdays`: at a fixed date of the last contact it falls by 2.22 days per extra call. With `previous` and `poutcome` also held fixed, the slope is -1.01. Its worth: 0.0048 with LightGBM and +0.0001 with logistic regression. Without both `pdays` and `campaign` the loss is 0.0118, close to the sum of the two. -1 matches `previous` == 0 row for row (36,954 rows).
- Repeat clients: 995 profile pairs across years. In 95% the later row has the larger `previous`. Of 581 earlier subscribers, 562 have a later row whose `poutcome` is "success" (97%). Per test fold, about 557 test rows (3.7%) have the same client's later row on the train side. That row's `poutcome` predicts the test label at ROC AUC 0.97 to 0.99, and about 186 of these test rows (10.6% of the fold's positives) are marked "success". Given a lookup feature built from training features only, LightGBM rises from 0.7627 to 0.7827 (+0.020, SD 0.0024, 0 of 9 splits lower). The shipped LightGBM cannot make the match. A retrieval-style model can: 1-NN agreement on the closest tenth is 0.845 against chance 0.793. The count is a lower bound, because profiles with abs(balance) <= 50 cannot be matched.
- The period itself is worth +0.026 (year) to +0.042 (year-month) under the random split.
- Moro et al. 2014 evaluate on a time-ordered split. They criticise random splits, and they list "number of previously scheduled calls during the same campaign" as an input for "selecting the next customers to be contacted".
- Duplicates: 274 exact duplicate rows, 32 of them with conflicting labels. 0.9% of test rows have an exact copy in train. No decision is written.
- Naming: bank-full has `day` (day of the month), not `day_of_week`. The record's year is 2011 (the ESM paper), the definition's 2012 (the UCI donation).

Decisive experiment run by the mediator (the cost of the temporal remedy was not measured; it was cheap). Five expanding windows on the file order, each test window 4,521 rows, the train side 50% to 90% (meets SPLIT-14). LightGBM with an inner early stop on the latest 10% of train, 2 seeds (identical results):

- window 0 (2008): 279 positives (6.2%), ROC AUC 0.438
- window 1 (2008-2009): 473 positives (10.5%), 0.582
- window 2 (2009): 593 positives (13.1%), 0.603
- window 3 (2009): 726 positives (16.1%), 0.618
- window 4 (2009-2010): 2,130 positives (47.1%), 0.569
- Mean: 0.562. `campaign`'s worth under these windows: +0.0035 on average, with mixed sign (-0.006 to +0.020).
- Cross-check, fixed 300 trees / logistic regression per window: 0.49/0.47, 0.58/0.59, 0.65/0.67, 0.66/0.69, 0.61/0.66.
- The same test windows with an equal-size random training set drawn from all other rows: 0.54, 0.63, 0.70, 0.69, 0.61.

Reading: most of the IID 0.76 comes from telling the periods apart. The base rate moves from 5% to 52%, and the features mark the period. Within a period the signal is weak, and May-June 2008 predicts the rest of 2008 below chance. By construction, the temporal split puts no later twin on the train side: a client's earlier row sits in train and its history is legitimate (LEAK-34).

**3. Changes to make now (no decision needed)**

- a. Notes, `contact` (writing.md, EV-6): replace "within a period cellular and telephone barely differ" with the measured 0.0005 for the cellular-or-telephone part, and give the raw rates. Optionally add that the 2014 release codes May-June 2008 as "telephone".
- b. Notes, `campaign` (writing.md, EV-6): add the 2009 and 2010 rates (19.0% to 7.2%, 51.9% to 39.2%) next to the flat 2008. The note's numbers otherwise hold.
- c. Notes, `pdays` (EV-6, LEAK-10 spans row): "the data lean to counting to the campaign's start (slope -2.2 days per call at a fixed date, -1.0 with `previous` and `poutcome` held fixed), not settled; worth 0.0048 / 0.0001". Add why -1 stays: it means "not previously contacted" and matches `previous` == 0 row for row (CLEAN-10). Accept the bundle's pdays sentinel warning with that reason.
- d. `set_missing`: add `"job": ["unknown"]` (CLEAN-10, Should, the default). The 2014 codebook says "unknown" codes a missing value, `education` already treats it so, and the measured cost is 0.0000 on 9 of 9 splits. `contact` "unknown" stays a level: it means something (a period marker), which CLEAN-10 allows.
- e. Curation bullet 2: "month" and "day" (day of the month), not "day_of_week". The reason "not available in a real-world scenario" contradicts the source, which keeps the call month as an input. Write instead that the date of the last contact is set by the campaign's end (writing.md, LEAK-10).
- f. task_summary.row: "one client's record in one campaign (a client can recur across campaigns)", not "one client ... (45,211 clients)" (USE-1, writing).
- g. A note on `balance` (LEAK-3, Should; a question, not a leak): the year of the "average yearly balance" is not stated, and in 71% of the cross-year pairs it is identical to the euro while age moves +1. No mechanism or gain is shown, so keep it, as with the 2026-11-05 registry case (tunisian_fraud_detection_challenge).
- h. Record: reconcile the year (2011 against 2012). Replace or annotate the comment "features seem to be time-invariant" with the measured shift (EV-2, stages: a later measurement supersedes it).
- i. Under either outcome of issue 2, `known` must agree with the stated prediction point (USE-3, Must). The text depends on issue 2.

**4. Issues for the curator, ranked**

**Issue 1. P4, Must (LEAK-17, SPLIT-29, SPLIT-1), against a Should precedent (SPLIT-31). The split.**

- Problem: the random split puts a client's later row in train next to its earlier row in test. The later row's `poutcome` is the earlier row's label. The split also lets the model learn each period's base rate (5% to 52%) from rows of the same period, which a bank picking clients for its next campaign never has.
- Effect: +0.020 ROC AUC for a model that makes the client match (3.7% of test rows, 10.6% of positives). The cost of the honest split is large: IID 0.76 against a temporal mean of 0.56 to 0.62.
- Claim auditor's best evidence: the measured lookup (0.97-0.99 on the matched rows, +0.020 in 0 of 9 splits lower). The source's own split is time-ordered and it calls random splits unrealistic (Moro 2014, p.5; SPLIT-19, SPLIT-5). The file's date order rebuilds exactly (SPLIT-22). SPLIT-7: a hidden timestamp does not make a task IID.
- Column auditor: did not test the split. Nothing on its side argues for IID.
- The best case for IID (the precedent): SPLIT-31 keeps IID "optimistic, but it matches how the task is framed" and names bank_marketing. The temporal task is weak: window 0 is below chance, and the mean is 0.56 with LightGBM.
- By rank: LEAK-17 and SPLIT-1 are Musts. SPLIT-31 is a Should, and a precedent ranks below a rule. A grouped split on a rebuilt client key fails SPLIT-24 (profile with age +-1, zero balances unmatched: a near-match, not an exact key). Keeping IID with a note is SPLIT-8's path for forced splits, and this split is not forced: the date order exists. So the ladder gives "fix the definition: re-split temporally".
- It is still your call, because it reverses your SPLIT-31 application and changes the task's difficulty a great deal.
- Options:
  - (a) Temporal on the file's date order: the year and month rebuilt in `_clean` as the time key, five expanding windows from the 50% floor, tag the split temporal. Update `split`, `fit`, `fit_reason`, `data_tags`, the record's `required_split`, and the SPLIT-31 Cases row: bank_marketing moves out, with the facts that set it apart. Consider restoring the call month as a feature: the source keeps it and the period is known when a campaign is planned (LEAK-10/USE-6; a separate small call).
  - (b) Keep IID. This needs an amendment, not an exception (LEAK-17 is a Must): state the +0.020 and the period leak in the notes and in `fit_reason`.
- Recommendation: (a). A follow-up check under (a): TP probes on the windows, since window 0 is below chance. Also, the authors' 2014 release (bank-additional-full, with `month`, `day_of_week` and economic context, already in the warehouse zip) may be the better version (TP-6, PROV). No provenance reviewer was on this tier, so that question stays open.
- To settle the remaining doubt: none needed on the facts. The decision is the precedent.

**Issue 2. P3/P4, Must (USE-3, LEAK-10), resolved through the span row. The prediction point decides `campaign`; a weighing call.**

- Problem: the use case says the team "picks which clients to call in a ... campaign", which is before any call. At that point `campaign` does not exist for any row, so LEAK-10's first question fails and the span row (a span the actor knows, LEAK-37) is never reached. That is the column auditor's case. heart_failure's `time` was dropped for the same timing. The current state, a use case before the campaign with `campaign` kept, breaks USE-3 whatever else is decided.
- Column auditor's best evidence: the timing argument. The heart_failure precedent (follow-up from baseline to death or censoring, dropped). noaa's span closes before its prediction point. LEAK-6: "a confirmed leak goes even when small". Given the period, the rate still falls with the calls (MH 1.26), so the window clause is not met. Recommends drop.
- Claim auditor's best evidence: the source frames the decision as "selecting the next customers to be contacted during bank marketing campaigns", with the calls scheduled so far as an input (Moro 2014, Table 2; EV-2, a primary document). At the call the row records (the last one), the calls so far are `campaign` - 1, a constant shift. What remains is the span row's case: the row exists at the last call, and the last call is drawn by a subscription or by the bank's stopping rule. Your own row of 2026-11-06 names this dataset kept. The worth given the period is about one seed SD, and +0.0035 with mixed sign under the temporal windows.
- Rules: under prediction point A (before the campaign), LEAK-10 (Must) drops it. No rule keeps it: LEAK-11 needs a value that weakens the signal, and `campaign` adds signal. Under prediction point B (at a call during the campaign, the source's framing), the span row applies and it is kept with the note, as implemented. Which framing ships is a weighing call (USE-1, USE-9).
- Factors: for B, the source states it (+) and the curator has decided it once (+). Against B, the rows exist only at the last call, so earlier failed calls to the eventual subscribers are absent (the column auditor's (c)), and USE-9 warns against a use case reworded only to close a gap (-; weak here, since it is the source's wording).
- Options:
  - (a) Keep the use case before the campaign and drop `campaign` (cost 0.006 IID, about 0.0035 temporal). Update `known`, `changes`, `fit_reason`, and the span row's entry: "dropped, after the prediction point". Consistent with heart_failure.
  - (b) Reword `use_case`, `row` and `known` to the source's framing: at a call of the campaign, which client to call next, the calls so far known; the row is the client's last call. Keep the note. In the span row, add the fact that sets the case apart from heart_failure: the prediction point lies inside the span, whereas heart_failure's baseline lies before it.
- What would settle it: your choice of the actor's moment. A per-call release would make (b) exact; the files have none.
- Mediator's lean: either option is valid. The current state is not. (a) is cheaper to defend. (b) follows the source and your decision of today.

**Issue 3. P4, Must (LEAK-16), low effect. Duplicates.**

- Facts: 274 exact duplicates, 32 with conflicting labels; 0.9% of test rows have an exact copy in train, with the same label in 0.8%.
- Rule: LEAK-18 (Should) has many columns plus an exact match (with the balance to the euro) pointing to an artefact (drop), and plausible repeats pointing to keep. Neither report argued it.
- Options: (a) keep, with a notes line giving the counts (under a temporal split, a copy in an earlier window is entity history, LEAK-34); (b) drop the exact copies.
- Lean: (a), with the numbers.

**5. Disputed points and how they settle**

- `campaign` keep or drop. Not a dispute of fact: the numbers agree. It is a dispute of the prediction point, which USE-3 makes a Must to state and which the rules leave to the curator's framing. Hence issue 2.
- "Within a period cellular and telephone barely differ." The claim auditor calls it refuted (raw rates, MH OR 1.56). The column auditor says it holds in worth (0.0005). Both are measurements, and they answer different questions: rates against model worth. Settled by citing the worth and giving the rates (change 3a). No harm to the keep (USE-6, LEAK-37).
- `pdays` timing. The column auditor reads "known" from the -2.22 slope. The claim auditor shows that half of the slope is selection (-1.01 with controls). The evidence leans to "start" but does not establish it (EV-6), and the effect is small (0.0048 / 0.0001). Keep, with the hedged wording (change 3c).
- The repeat-client leak: raised by the claim auditor only and not contested. It stands as a fact (issue 1).

**6. Consistency with precedent**

- heart_failure_followup_survival `time` (LEAK-10, dropped). Option 2a follows it. Option 2b departs from it and must name the fact (the prediction point inside the span) in the span row. Keeping `campaign` under the current use case breaks it, and there is no distinguishing fact other than size, which LEAK-6 rules out. That would be consistency case 1 or 2 of principles.md.
- noaa_storm_events_damage `duration_hours` (the span row): fits bank_marketing only under 2b.
- SPLIT-31 (amazon_employee_access, bank_marketing, IID kept). Issue 1(a) departs from it. The facts that set this case apart: the source's own split is temporal, the date order is recoverable, there is a label leak through the recurring client (Must), and the base rate moves tenfold. amazon_employee_access is not affected.
- SPLIT-8 forced IID (account_debt_south_africa, bemtpl97, fremtpl2, the churn snapshots). Those have no dates or too few periods. bank_marketing has a recoverable year and month and enough rows for five windows above the 50% floor, so SPLIT-8 does not apply.
- LEAK-34 (ieee_fraud_detection `uid`, ghana): supports that `poutcome` is legitimate history once the split is temporal.
- forest_fires (P4 over P6): the weak temporal score is no argument for IID.
- tunisian_fraud_detection_challenge (registry fields kept with a note): followed for `balance` (change 3g).

</details>

<details><summary>Claim audit</summary>

_In this file: the auditor's findings A and B are issue 1, C is issue 2, F is issue 3; D, E, G and H are applied (the mediator's changes g, c, a/b/e/h and c). Its own "issue 1" and "issue 2" in the judgment record are both this file's issue 1._

**Claim auditor report: bank_marketing (re-review after the rule changes of 2026-11-06).** Definition `datasets/_dev/tabarena-v0pt2/bank_marketing/dataset.py` (README stale build, no data change); record `curation/records/bank_marketing.md`. Models: LightGBM (lr 0.05, 31 leaves, early stopping on a 10% inner split), 9 shipped splits x 2 seeds, ROC AUC.

**Verdict**

The new notes' numbers reproduce: campaign is worth 0.0060 / 0.0079 and 0.0013 / 0.0016 given the year; contact is worth 0.021. But two of their sentences are false or not established: "cellular and telephone barely differ" and "pdays counts to the campaign's start". The audit also found a Must-level leak that no note covers. The same clients recur across campaigns. A client's later row carries `poutcome` = the outcome of its earlier row, and under the random split that later row sits on the train side for about 557 test rows per fold. Those test rows get their label at ROC AUC 0.979 (LEAK-17, P4). The source paper evaluates on a time-ordered split and criticises random splits. The file is in date order. So a temporal split would remove both this leak and the fit gap.

Judgment record:

- Validity: LEAK-17 triggered (future-twin poutcome, +0.020 ROC AUC to a model given the lookup), not fixed; SPLIT-1/SPLIT-7 vs the SPLIT-31 precedent: consistency check due (source split temporal, data date-ordered); LEAK-10 Cases row (spans): campaign kept with a note, numbers hold; USE-3 wording conflict (use case before the campaign vs `campaign` known).
- Value: MET-1, MET-2, MET-5 hold for roc_auc; TP fine (1,763 positives per test fold).
- Quality: LEAK-16 decision on 274 duplicates not written; bundle warning on pdays=-1 not accepted although CLEAN-10 keeps it.
- For the curator: issue 1 (temporal split or grouped split), issue 2 (SPLIT-31 precedent reopened).

**New notes first**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | "Without it [campaign] ROC AUC falls by 0.0060 (LightGBM, 9 splits x 5 seeds, lower in 9 of 9) and 0.0079 (logistic regression)" | curation_comments bullet 4 | re-read the earlier measurement summary; own refit (2 seeds) | HOLDS | summary: -0.0060 (SD splits 0.0014, 9/9), LR -0.0079 (9/9) | LEAK-10 Cases row (spans), LEAK-6 |
| 2 | "given the year of the last contact ... it adds 0.0013 and 0.0016, about one seed SD of LightGBM" | bullet 4; fit_reason "about 0.0015 of it once the period is known" | summary (+year vs +year-campaign) and own fit given year-month | HOLDS | 0.7887-0.7874=0.0013, LR 0.7783-0.7767=0.0016; seed SD 0.0016; own: given year-month -0.0012 (SD 0.0007, lower in 8/9) | EV-8 |
| 3 | "3.2 calls per client at 5.1% subscribed in 2008, 1.9 at 51.6% in 2010" | bullet 4 | audit1 rebuild of the year from file order | HOLDS | 2008: 27,729 rows, mean campaign 3.19, rate 5.05%; 2010: 2,620 rows, 1.89, 51.60% | EV-1 |
| 4 | "in 2008 the rate is flat over 1 to 10 calls" | bullet 4 | MH rate ratio, 1 call vs 4+ calls, within months of each year (audit1) | HOLDS, BUT SELECTIVE | 2008 RR 1.05 (5.3/4.9/5.1/5.2/5.3%); 2009 RR 1.49 (19.0% at 1 call to 7.2% at 6-10); 2010 1.18. The note cites the flat year only. The residual worth is small anyway (claim 2) | writing.md, EV-6 |
| 5 | "The calls stop at a subscription or when the bank stops calling, so the outcome draws the end only for subscribers" (kept under the spans row) | bullet 4 | rule application read against leak_checks.md l.442 | HOLDS | outcome-or-criterion -> keep with a note giving its worth; the note gives it | LEAK-10 Cases row 2026-11-06 |
| 6 | `contact` "unknown covers all 12,443 rows of May-June 2008 (3.7% subscribed), so it marks the period" | bullet 5 | audit1 counts; audit3 worth of contact given the period | HOLDS | 12,443 rows, 100% unknown, 3.69%; contact's worth falls from 0.021 to 0.0066 given the year and to 0.0028 given the year-month (lower in 9/9) | EV-1 |
| 7 | "within a period cellular and telephone barely differ" | bullet 5 | Fisher test per period; Mantel-Haenszel OR within year-month | REFUTED | Jul-Dec 2008: 6.0% vs 6.8% (OR 0.87, p 0.23); 2009: 17.4% vs 13.6% (OR 1.33, p 5e-4); 2010: 57.1% vs 45.5% (OR 1.59, p 4e-4); MH OR within year-month 1.56. Also, 2010's 251 "unknown" rows subscribe at 12% against 57% for cellular | EV-6, writing.md (no harm to the keep: the phone type is known before the call, USE-6) |
| 8 | "It [contact] is worth 0.021 ROC AUC in both models" | bullet 5 | summary | HOLDS | LGBM -0.0210, LR -0.0215, 9/9 | |
| 9 | "`pdays` counts to this campaign's start, not its end (at a fixed last-contact date it falls by 2.2 days per extra call)" | bullet 5 | replicate the slope; add controls | NOT ESTABLISHED | slope within the exact date -2.22 (replicated); with previous x poutcome also held fixed, -1.01. Half of the slope is selection of who gets called more, so the reading is circumstantial. If pdays ran to the last contact, it would be a span the outcome ends, like campaign. Its worth was not measured given the period (-0.0048 LGBM overall, +0.0001 LR) | EV-6, LEAK-10 spans row |
| 10 | fit_reason: "kept, worth 0.006 ROC AUC, about 0.0015 of it once the period is known" | task_summary.fit_reason | as 1-2 | HOLDS (numbers) / INCOMPLETE | the kept repeat-client leak (finding A) is not named | USE-8 |

**The task summary**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 11 | row: "One client contacted in a phone campaign ... (45,211 clients)" | task_summary.row | match rows on job, marital, education, default, exact balance (absolute balance > 1000), housing and loan; check previous, poutcome and age in the later row (audit2, audit4) | REFUTED | the rows are client-campaign records. 995 cross-year pairs: in 95% the later row has the larger `previous`, its age is +1 in 71% (0 in 24%), and its poutcome = the earlier row's outcome (an earlier subscriber -> "success" in 562 of 581 pairs, 97%). UCI: "more than one contact to the same client was required" | USE-1, LEAK-17 |
| 12 | predicted: "Whether the client subscribed ... by the end of the campaign's calls; 11.7% did" | task_summary.predicted | count | HOLDS | 5,289 / 45,211 = 11.70% | |
| 13 | known: "... the number of calls in this campaign ..." known at prediction time; use_case: "picks which clients to call in a term-deposit campaign" | task_summary.known/use_case | read against USE-3 and Moro 2014 | REFUTED AS WRITTEN (internal conflict) | before a campaign, nobody has been called and `campaign` does not exist. The source frames the decision as "selecting the next customers to be contacted during bank marketing campaigns" (Moro 2014, p.5), with "number of previously scheduled calls during the same campaign" as an input (Table 2). Under that wording the count is known before the next call | USE-1, USE-3 |
| 14 | split: "Random clients, so the test data stands for other clients of the same campaigns and years" | task_summary.split | hold-out of a client's later row (audit3) | REFUTED ("other clients") | about 557 test rows per fold (3.7%) have the same client on the train side, and in about 186 of them the client's later row says "success" (97.6% are subscribers) | LEAK-17, SPLIT-29 |
| 15 | changes: drop duration, day and month | task_summary.changes, dataset.py | code | HOLDS (day = day of month; see 19) | | |
| 16 | fit approximate: "the dates are dropped and the split is random, so the test clients do not stand for a later campaign" | fit_reason | source and data | HOLDS as a gap statement | but the gap can be closed: the file is "ordered by date" (UCI), the year rebuilds from it (as the measurements did), and Moro 2014 used a time-ordered split. It criticises a random split because it "does not reflect the temporal dimension that a real prediction system would have to follow" (p.5) | SPLIT-1, SPLIT-5, SPLIT-7, SPLIT-19, SPLIT-22 |

**The curation comments**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 17 | "We removed the duration feature following its original description" | bullet 1 | UCI codebook, Moro 2014 p.4 | HOLDS | paper: models good only with "attributes that are only known on call execution, such as call duration" | LEAK-10 |
| 18 | "remove month and day_of_week ... relate to the last contact -- which is not available in a real-world scenario" | bullet 2 | Moro 2014 Table 2 | PARTLY REFUTED | the source keeps call.month ("month in which the call is made") as a known input. What is not known is which call will be the last one. The period itself is worth +0.026 (year) to +0.042 (year-month) ROC AUC | LEAK-10, USE-6 (dropping is defensible; the stated reason is not) |
| 19 | "day_of_week" | bullet 2 | raw columns of bank-full.csv | REFUTED (naming) | bank-full has `day` (day of month); day_of_week is a column of bank-additional | writing.md |
| 20 | campaign and previous are counts, numeric; "48 and 41 levels" | bullet 3 | dtypes, n_unique | HOLDS | int64, 48 / 41 | CLEAN-14 |
| 21 | education ordinal primary < secondary < tertiary; "unknown" missing | bullet 6 | codebook, counts | HOLDS | 1,857 missing (4.11%) | CLEAN-14, CLEAN-10 |

**The metric**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 22 | roc_auc, origin source: "AUC ... with ALIFT as second metric", Moro 2014 | Metric.source | read the paper's evaluation | HOLDS | "Using two metrics, ... (AUC) and ... (ALIFT)" (abstract); the forward selection keeps features "if they improve the predictive performance in terms of the AUC value". AUC is the deliberate selection criterion | MET-1, MET-5, MET-11 |
| 23 | the metric is computable on our folds | MET-2 | scorer(container) with a constant and a random prediction on all 9 folds | HOLDS | every test fold has 15,070-15,071 rows and 1,763 positives, train and test do not overlap; constant 0.500, random 0.483-0.508 | |
| 24 | the metric means the same on our task | MET-2 | compare the source's unit and balance | HOLDS with a caveat | the source's unit is a phone contact (52,944, 2008-2013, 12.38% success) scored on a rolling time window; ours is a client-campaign row (2008-2010, 11.7%) on a random split. Same target and classes, similar balance | MET-2 |
| 25 | no sample weight, no rate target | dataset.py | MET-15 / LEAK-41 check | NOT APPLICABLE | binary per-row target, no weight column and no amount at risk | MET-15, LEAK-41 |

**The record**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 26 | "Might actually require temporal split - but as features seem to be time-invariant the task should be fine" | record Comments | shift by year (audit1) | REFUTED | rate 5.1% -> 17.1% -> 51.6%; contact "unknown" only May-Jun 2008 (and 251 rows of 2010); mean campaign 3.19 -> 2.13 -> 1.89; age max 61 in 2008, 95 in 2009 | SPLIT-7, EV-2 |
| 27 | "Assessment (AI, 2026-10-21): source roc_auc - AUC (with ALIFT second)" | record | as 22 | HOLDS | | |
| 28 | "CC (2026-10-30): campaign and previous are counts" | record | as 20 | HOLDS | | |
| 29 | required_split: Random (IID); suggestion Yes; year '2011' | record front matter | the source's split; definition year '2012' | IID CHALLENGED (as 16, finding A); year mismatch | record 2011 = the ESM paper, definition 2012 = the UCI donation | SPLIT-5, writing |

**Implied claims**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 30 | No row is a copy across the split | implied | probe 5/6 and the bundle infos | HOLDS WEAKLY / NO DECISION WRITTEN | 274 exact duplicates, 32 conflicting; 0.9% of test rows have an exact copy in train. No duplicate decision in the notes | LEAK-16 |
| 31 | Each feature is known at the prediction point: age, balance | implied | twin pairs across years (audit4) | UNTESTED, A QUESTION | in 71% of the cross-year pairs age moves +1 while balance is identical to the euro. The balance is therefore one snapshot, of unknown date, possibly after the outcome (a subscription moves money). No source statement was found | LEAK-10 (lookup after the outcome), EV-3 |
| 32 | The frame's order does not leak the date | implied | container index vs raw position | HOLDS | RangeIndex after the shuffle, corr(index, raw position) 0.005 | |
| 33 | Bundle warning dataset_missing_value_sentinel (pdays = -1) | README bundle_checks, accepted {} | CLEAN-10 text | HOLDS ON SUBSTANCE, NOT RECORDED | CLEAN-10 keeps "not previously contacted" as a code, and the house_sales exception cites bank_marketing's -1. The warning is not accepted in the definition | CLEAN-10 |

**Refuted and untested, ranked (validity first, Must first)**

- A. [P4, Must, LEAK-17 / SPLIT-29; SPLIT-9 by analogy] Repeat clients carry the label across the random split. Changes: claims 11, 14 and 10, and the leak list. Per test fold, about 557 test rows (3.7%) have a later row of the same client on the train side. That row's poutcome gives the test row's label at ROC AUC 0.979, and 97.6% of the about 186 it marks "success" are subscribers (10.6% of the fold's positives). Given that lookup, built from train features only, LightGBM rises from 0.7627 to 0.7827 (+0.020, 0/9 splits lower). The shipped LightGBM cannot use the match without the feature, but a retrieval-style model (kNN, an in-context learner) can. The 1-NN probe already hints at it (closest tenth 0.845 against chance 0.793). The count is a lower bound, because the profiles with abs(balance) <= 50 cannot be matched. Mildest remedy: a temporal split on the file's date order (SPLIT-22; the year and month rebuild exactly as the 2026-11-06 measurements did; the later twin is then always on the test or future side). It also matches the source's evaluation (SPLIT-19) and closes the fit gap of claim 16. Alternative: group on a client key rebuilt from the profile with age +-1 (SPLIT-24). That is incomplete for zero balances, so a grouped split would still leak a little; say so. Keeping IID with a measured note is the weakest option, because SPLIT-8's keep-with-note path is for forced splits, and this one is not forced.
- B. [P4, Must vs Should precedent; SPLIT-1/SPLIT-7 vs SPLIT-31] The IID keep under SPLIT-31 cites bank_marketing as optimistic but matching the framing. New facts set it apart: the source's own split is time-ordered and it criticises random splits; the data is date-ordered; the base rate moves tenfold; finding A. Changes: the split, data_tags, record required_split, and claim 26. Remedy: a consistency check to the curator (principles.md): (a) temporal, with the SPLIT-31 Cases row updated; (b) keep IID as a deliberate exception, naming the fact and finding A in the notes.
- C. [P3, Must, USE-3] The use case (pick clients before the campaign) conflicts with `campaign` being known. Changes: the use case and known texts. Remedy: reword the use case to the source's "during a campaign, which client to call next", with the count of the calls so far known. No data change.
- D. [P4, Should-level question, LEAK-10] The balance looks like one snapshot of unknown date (claim 31), so it is untested. Remedy: look for the source's statement (Moro 2011 ESM) and, if none, measure the balance's worth by year of contact. Without a mechanism, keep it with a note (LEAK-10 Case of 2026-11-05, registry fields).
- E. [P4, EV-6] The pdays note states the direction as fact on a confounded slope (-2.22 -> -1.01). Remedy: write "the data lean to counting to the start (slope ...), not settled", and give pdays' worth given the period as for campaign. Changes: claim 9.
- F. [P4, Must, LEAK-16] No duplicate decision is written. Remedy: one notes line (274 exact, 32 conflicting, 0.9% of test rows have an exact copy in train; kept as distinct clients or dropped).
- G. [Writing] Claim 7 ("barely differ") is false for 2009-2010. Claim 4 cites only the flat year. Claim 18's reason contradicts the source, and claim 19 names day_of_week for `day`. The record's year is 2011, the definition's 2012. Remedy: wording only, with the numbers above.
- H. [P7, CLEAN-10] Accept the pdays sentinel warning with the CLEAN-10 reason.

Sources read: the UCI page (https://archive.ics.uci.edu/dataset/222/bank+marketing) and the Moro, Cortez, Rita 2014 preprint (https://repositorio.iscte-iul.pt/bitstream/10071/9499/5/dss_v3.pdf).

</details>

<details><summary>Column audit</summary>

_In this file: the auditor's issues 1 and 2 are issue 2; its issues 3, 4 and 5 are applied (the mediator's changes d, c and e); its issue 6 is under issue 1's unknowns._

**Column audit: bank_marketing (focused re-review after the rule changes of 2026-11-06).** Column auditor, 2026-11-06. Definition: `datasets/_dev/tabarena-v0pt2/bank_marketing/dataset.py` (branch zi-datasets).

**Verdict**

Ship after one change, or a curator decision that amends LEAK-10. `contact` and `pdays` hold up under the new measurements and stay. `campaign` does not fit the span row the way the definition reads it. The use case's moment is "the marketing team picks which clients to call", before any call of this campaign. At that moment `campaign` (the calls this campaign will make, including the last) exists for no row. The span row was set on noaa, where the span ends before the prediction point. `campaign` has the same timing as heart_failure's `time`, which was dropped under LEAK-10 (Must). The other columns are fine, apart from small cleaning and wording points.

Judgment record:

- Validity: USE-1 and USE-3 hold for the use case, but the prediction point is not written down and `known` contradicts it (it lists "the number of calls in this campaign"). LEAK-10 is triggered by `campaign`, kept with a note: an open call, consistency check below. LEAK-10 holds for `contact` (97% of its worth is the period flag, measured) and for `pdays` (counted to the campaign's start, measured). No training weight, so LEAK-41 does not apply.
- Quality: CLEAN-10 departure on `job` "unknown" (the source's 2014 codebook says "unknown" codes a missing value). The reason for keeping `pdays` = -1 is not written in the definition. One curation bullet names the wrong columns.
- For the curator: issue 1 (keep `campaign`: amend LEAK-10, or drop it).

**The three columns first**

**1. campaign.** Codebook (bank-names.txt, item 13): "number of contacts performed during this campaign and for this client (numeric, includes last contact)".

- When the value exists: at the end of this campaign's calls to the client, that is, at the outcome for subscribers and at the bank's last call for the others.
- The prediction point: the task_summary's use_case is "picks which clients to call in a term-deposit campaign", and `predicted` is "subscribed ... by the end of the campaign's calls". So the model is used before the first call, and no part of the count is known then: not the last call, and not the calls before it. `fit_reason` says the count "partly reflects how the campaign ended". The truer statement is that all of it comes after the prediction point, and the outcome draws its end for the subscribers.
- Measured (the earlier measurement summary): dropping it costs 0.0060 ROC AUC with LightGBM (lower on 9 of 9 splits; split SD 0.0014) and 0.0079 with LogReg. With the year of the last contact added, it is worth 0.0013 and 0.0016, about one seed SD (0.0016). Within the year-month of the last contact, the Mantel-Haenszel rate ratio of 1 call against 4 or more is 1.26.
- The note's "in 2008 the rate is flat over 1 to 10 calls" is true but selective. In 2009 the rate falls from 19.0% at 1 call to 7.2% at 6-10 calls, and in 2010 from 51.9% to 39.2%. So given the period, the count still moves with the outcome. LEAK-10's window clause ("unless the data shows the window's values do not move with the outcome given the covariates known at the prediction point") is therefore not met.
- Dtype: int64, a count, numeric. That is right (CLEAN-14, issue #34).
- Verdict: leak (LEAK-10 Must; USE-3). It is weak: 0.006 alone, about 0.0015 given the period. Remedy: drop it. No smaller fix exists (LEAK-7): a lag such as campaign-1 is still unknown at the campaign's start. Details under issue 1.

**2. contact.** Codebook: "contact communication type (cellular, telephone, unknown)", grouped under "related with the last contact of the current campaign".

- When the value exists: strictly, at the last call. In practice it is the number the bank dialled, close to a client attribute. Its "unknown" level covers all 12,443 rows of May-June 2008, so it marks the period, and the period is known when the campaign is planned.
- Measured (LightGBM 9 splits x 3 seeds): the shipped set scores 0.7589. Replacing `contact` by an unknown-or-not flag scores 0.7583, a cost of 0.0005 (split SD 0.0012). Dropping it costs 0.0207. So 97% of its worth is the period flag, and the cellular-or-telephone part, the only part tied to the last call, is worth about 0.0005. The note's "within a period cellular and telephone barely differ" agrees with that number. The raw rates differ more (2009: 17.4% against 13.6%; 2010: 57.1% against 45.5%), so cite the 0.0005 rather than the rates.
- Source fact: the authors' 2014 release (bank-additional-full.csv, same bank and period) has no "unknown". Its May-June 2008 rows (12,137) are all "telephone", at 3.5% subscribed. So the 2012 file's "unknown" stands for a known type, telephone, and the type of a whole period. That supports reading it as a period marker.
- Missingness and the outcome: the 577 "unknown" rows outside May-June 2008 (322 in Jul-Dec 2008, at 11.8% against about 6%; 251 in 2010, at 12.0% against 57%) do not differ from their period in one direction. That does not point to missingness caused by the outcome.
- Dtype: unordered category. That is right.
- Verdict: fine, kept. Optional wording: name the 2014 release's "telephone" for May-June 2008 in the note, and give the 0.0005 figure. Keeping "unknown" as a level is lossless and is the period marker the note describes. CLEAN-10 would make it missing, which holds the same information. That choice is the curator's (low priority).

**3. pdays.** Codebook: "number of days that passed by after the client was last contacted from a previous campaign (numeric, -1 means client was not previously contacted)".

- When the value exists: the definition says it is counted to this campaign's start. Evidence (the earlier measurement summary, section 3): at a fixed date of the last contact, pdays falls by 2.22 days per extra call (date-block bootstrap 95% interval -3.84 to -0.91). Counting to the last contact would leave it flat there. Counting to the first contact predicts the negative slope that was measured. So it is known at the prediction point.
- Caveat: this is circumstantial (EV-2: a measurement, not a statement by the source). The alternative reading, a count to the last contact, would hide this campaign's length inside it. The two readings differ by -2.2 days per call, which is small next to the median of about 190 days. Its worth: 0.0048 with LightGBM and nothing with LogReg (+0.0001). Without both it and `campaign`: 0.0118, close to the sum of the two (0.0108). So it does not carry much of the campaign's length on top of `campaign`.
- Cleaning: -1 means "not previously contacted". It matches previous == 0 row for row (36,954 rows, no mismatch). CLEAN-10 allows keeping such a code ("Keep a code and say why when it means something ('not previously contacted')"), and the house_sales Cases row names bank_marketing's -1 as kept. But the definition never says why. A linear model also reads -1 as "contacted one day ago" (the smallest real value is 1). `previous` == 0 and `poutcome` == "unknown" carry the same flag, so the harm is small.
- Dtype: int64. That is right.
- Verdict: fine, kept. Cleaning point (CLEAN-10, Should): add one sentence on why -1 stays. Alternative: set it to missing, since `previous` holds the flag.

**The column table**

| Column | Meaning (codebook) | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| age | client's age, numeric | yes | int64, 18-95 | fine | - |
| job | type of job; "unknown" in 288 rows | yes | unordered category; "unknown" kept as a level although education's "unknown" is missing, and the 2014 codebook says: "missing values ... all coded with the 'unknown' label" | cleaning point: set "unknown" to missing for consistency (measured: no score change, 0.0000 on 9 of 9 splits) | CLEAN-10 (Should) |
| marital | marital status; "divorced" means divorced or widowed | yes | unordered category, 3 levels, no unknown | fine | - |
| education | education level; "unknown" in 1,857 rows | yes | ordered primary < secondary < tertiary, as the codebook's meaning orders them; "unknown" is missing | fine | CLEAN-14, CLEAN-10 |
| default | "has credit in default?" yes/no | yes, as a status the bank holds; when it was read is not stated | category no/yes | fine (timing unstated; nothing points to a change after the call) | LEAK-10 second clause, not triggered |
| balance | "average yearly balance, in euros" | probably; the year is not stated. A balance averaged over a year that contains the subscription could move with it, since money goes into the deposit. No evidence: alone it scores 0.58, and higher balance means more subscribing, which is the expected sign | int64, -8,019 to 102,127; 3,766 negative values (an overdraft, plausible) | question, low: say in a note that the year is not stated | LEAK-10 (question only), LEAK-3 |
| housing | has a housing loan? | yes (status) | category | fine | - |
| loan | has a personal loan? | yes (status) | category | fine | - |
| contact | type of the last contact; "unknown" covers all of May-June 2008 | the type comes with the last call but is close to a client attribute; the period flag is known | unordered category | fine, kept (97% of its worth is the period flag; cellular-or-telephone worth 0.0005) | LEAK-10 holds, LEAK-37 |
| campaign | this campaign's contacts, including the last | NO: the use case's moment is before the first call; the outcome ends the count for subscribers | int64 count, numeric (right) | leak, weak (0.006; 0.0013-0.0016 given the year); remedy: drop, or keep under an amended LEAK-10 | LEAK-10 (Must), USE-3 |
| pdays | days since the last contact of a previous campaign; -1 = not contacted | yes (counted to this campaign's start, measured slope -2.22 days per call) | int64; -1 kept as a meaningful code, reason not written | fine; cleaning point: write why -1 stays | CLEAN-10 |
| previous | contacts before this campaign | yes | int64 count, 0-275 (one row at 275, next highest 58; unusual, not impossible) | fine | CLEAN-11, CLEAN-14 |
| poutcome | outcome of the previous campaign: failure, other, success, unknown | yes | unordered category; "unknown" = not previously contacted in 36,954 rows (previous == 0), and truly unknown in 5 rows with previous > 0; "other" is undocumented | fine (a state of its own, lossless) | - |
| SubscribeTermDeposit (target) | has the client subscribed a term deposit? | the label | category no/yes; the source's words, so it keeps them under CLEAN-25; 11.7% yes | fine | CLEAN-25 |
| dropped: duration | length of the last call | no (UCI: "should be discarded ... realistic predictive model") | dropped, right | fine | LEAK-10 |
| dropped: day, month | day and month of the last contact | the last contact's date is set by the end of the campaign; the period itself is known | dropped | fine. The curation bullet calls them "month" and "day_of_week". day_of_week is a column of the 2014 release only; this file has `day`, the day of the month. Fix the wording | writing |

Training weights: none (task_metadata.sample_weight is None), so the weight-proxy check (probe 22, LEAK-41) does not apply. Dtype probe (dtype_probes.py bank_marketing): 0 of 13 columns flagged; 13 of 13 matched to the codebook.

**The auditor's issues, ranked (P4 first, then P7)**

- Issue 1 (P4, LEAK-10 Must, USE-3; weak; a call for the curator). `campaign` is unknown at the prediction point, and the span row is being applied to a span that runs after that point.
  - Steelman of the keep: the curator decided on 2026-11-06 to keep it under the new span row (the row's text in this worktree names bank_marketing `campaign` as "kept with a note"). The row keeps a span "drawn by the outcome or an outcome-free criterion". Here the outcome ends the calls only for subscribers, and the bank's stopping rule ends them for everyone else. It is weak: 0.006 alone, about 0.0015 given the year.
  - Counter, which can be checked:
    - (a) The span row is filed under LEAK-10 and LEAK-37, and LEAK-37 covers "an input the actor knows at the prediction point". noaa's use case estimates the damage "before its damage is assessed", after the event, and lists the duration under `known`. That span closes before the prediction point. bank_marketing's use case decides whom to call before the campaign. Its span starts at the prediction point and runs after it, so the first question of LEAK-10 ("only what existed at the prediction point") fails for every row. Who draws the end, the second question, is never reached.
    - (b) Precedent, heart_failure_followup_survival: `time` was dropped under LEAK-10. It is the follow-up from baseline (the prediction point) to death (the outcome) or censoring (outcome-free), the same shape as `campaign`, which runs from the start of the campaign to a subscription or the bank's last call. Read literally, the span row would keep `time` with a note as well, since death or censoring is "the outcome or an outcome-free criterion". The fact that reconciles the span row with heart_failure is timing relative to the prediction point. That fact puts bank_marketing with heart_failure, not with noaa. The fact that sets them apart is strength: `time` alone scores ROC AUC 0.84, while `campaign` adds 0.006, and about 0.0015, one seed SD, given the period. But LEAK-6 says "a confirmed leak goes even when small", and LEAK-10 is a Must with no exceptions. Only LEAK-11 (a value that weakens the signal; `campaign` adds signal) and LEAK-30 (transductive scaling) keep a late value with a note, and neither applies. LEAK-10's window clause is not met either: given the year, the rate still falls with the calls (2009: 19.0% at 1 call, 7.2% at 6-10; MH 1.26).
    - (c) No other use case makes `campaign` known (USE-9). A "call once more?" decision would need one row per call and the count before the call. The file holds only the final count.
  - Options, mildest first:
    - (a) Drop `campaign` (LEAK-10). Cost: 0.006 ROC AUC. Update `known`, `changes` and `fit_reason`, and replace the Cases row's bank_marketing entry with "dropped, after the prediction point".
    - (b) Keep it, and amend LEAK-10 as a deliberate change, because a Must cannot carry an exception. A possible wording: "a count over a span that begins at the prediction point and whose end the outcome draws only in part may stay with a note when its gain given the covariates known at the prediction point is within seed noise". heart_failure stays dropped under it (0.84 alone). Then write the amendment's measurement into the note.
    - (c) Keep it as it is now. This breaks the heart_failure precedent with no distinguishing fact other than size. Principles flags this case for a consistency check (cases 1 and 2).
  - Recommendation: (a). It is cheap, and it makes the task match the written use case.
  - Under either choice, the `known` field must not list "the number of calls in this campaign" as known at prediction time (USE-3). With (b), write it as "kept, recorded after the prediction point".
- Issue 2 (P3 and P4, USE-3; wording, cheap). The prediction point is not written down. The first curation_comments bullet is the drop of `duration`. Add a first bullet such as: "Prediction point: before the campaign's first call to the client, when the team picks whom to call; known then are the client's profile and the earlier campaigns."
- Issue 3 (P7, CLEAN-10 Should). `job` keeps "unknown" (288 rows) as a level while `education`'s "unknown" is missing. The authors' 2014 codebook says: "There are several missing values in some categorical attributes, all coded with the 'unknown' label." Remedy: add "job": ["unknown"] to set_missing (measured: no score change). Also optional, the curator's call: `contact`'s "unknown". The note's reason, a period marker, is a fair reason to keep it as a level.
- Issue 4 (P7, CLEAN-10 Should). `pdays` = -1 is kept, as the rule allows, but the reason is not written. Remedy: one sentence in the notes ("-1 = not previously contacted, matches previous == 0 row for row; kept as the source's code").
- Issue 5 (writing). The curation bullet names "month" and "day_of_week". The dropped columns are `day` (day of the month) and `month`; day_of_week belongs to the 2014 bank-additional release.
- Issue 6 (beyond my brief; for the provenance reviewer). The authors' 2014 release (bank-additional-full.csv, 41,188 rows, in the warehouse zip) is the version the source paper (Moro et al. 2014, the metric's reference) describes. It keeps month and day_of_week, has economic context columns, and gives the true contact type for May-June 2008. Whether it is a better version (TP-6, PROV) is not this audit's call. I could not read the 2014 paper (core.ac.uk answered 403), so its own prediction point and its treatment of `campaign` are unchecked (LEAK-3, Should).

Evidence in the repository: `datasets/_dev/tabarena-v0pt2/heart_failure_followup_survival/dataset.py`, lines 65 and 83-84 (`time` dropped, 0.84 alone); `datasets/_dev/tabarena-v0pt2/noaa_storm_events_damage/dataset.py`, lines 71-90 (the use case after the event; duration under `known`).

</details>

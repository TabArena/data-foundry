# qsar_bioconcentration

**Outcome:** added. UCI 510's 776 chemicals with the three-class bioconcentration mechanism as the target, the 9 Dragon
descriptors plus 193 RDKit 2D descriptors of the repaired structures, IID; the review panel (full tier, 2026-10-20)
recommends shipping it after changes. Validity: SEL holds; USE-1 and USE-5 hold (the class is the source's target, its
rule and labels reproduce); USE-6 and USE-3 (Must) are triggered, since the use case presumes the logKOW the assessor
holds and the inputs leave it out (issue 8); USE-8 does not support the current `direct` while a potential leak is kept
(issue 9); LEAK-4, LEAK-10, LEAK-16 and LEAK-17 hold (logBCF dropped, no copies across the split); LEAK-31 is triggered
by the authors' descriptor selection, small and removable (issue 5); SPLIT-1, SPLIT-4 and SPLIT-29 hold, with a
scaffold-grouped variant a SPLIT-31 candidate (issue 10); PROV-13 holds (three swapped pairs repaired from the authors'
table, three rows dropped). Value: TP-2 and TP-5 hold (random forest macro ROC AUC 0.762, log loss 0.720 against 0.883
for the class prior; 21-22 rows of the rarest class in every test fold). Quality: CLEAN-11 and CLEAN-24 hold. Weighed: a
real assessor's decision, a documented source and a repair from the origin (for); 776 chemicals and a signal carried
mostly by congener series (against). Left for the curator: the logKOW input (issue 8), the fit label (issue 9), the
target framing (issue 1), the 9 selected descriptors (issue 5) and a scaffold variant (issue 10); the QSAR siblings'
joint fit label is an item at the end of the working copy's REVIEW.md. Their `domain` is settled: "chemistry & material
science" for all ten molecule-property datasets (Lennart, 2026-10-21).

**Main points:** Give the model the logKOW the class is read against, or rewrite the use case (issue 8); then
`direct` or `approximate` (issue 9), class or logBCF (issue 1), and keep or drop the authors' 9 descriptors (issue 5).

**Record fields that disagree with the definition:**

- `tag`: record `Free Text (Short)`, definition `none (no string feature since the SMILES was dropped on 2026-10-14)`.

**Record judgment:** valid. The class is the source's published target, a band of ±0.5 log units around the BCF the
EU's Technical Guidance Document (TGD) equation expects from the logKOW; the panel reproduced the rule (600 of 607
chemicals), matched the labels to the archived UCI page and confirmed the swap repair on 776 of 776 rows. The
record's 2026-10-07 statement that the 779 chemicals all have an experimental KOW holds only for the 2016
re-curation: the 2015 table lists 122 of the shipped chemicals with a predicted one.

**Issues for Lennart:**

8. **Add the logKOW as an input, or rewrite the use case?**
   - Problem: the logKOW (octanol-water partition coefficient) measures how readily a chemical dissolves in fat
     rather than water; it comes from a cheap lab test. The BCF (bioconcentration factor) is how much of the chemical
     builds up in a fish against the water around it, from an expensive fish test. The class says whether the BCF
     expected from the logKOW (the TGD line) holds for a chemical. `use_case` says the assessor uses the class to
     decide whether that logKOW-based estimate "can be trusted", which presumes the assessor holds the logKOW, while
     `known` says the structure only. So the definition states two prediction points, and the inputs leave out a
     value the actor has. MLOGP, a logKOW computed from the structure, is an input (correlation 0.87 with the
     measured value).
   - Effect: small on the score, but the use case as written assumes the assessor has the logKOW. On the shipped
     features a random forest scores macro ROC AUC 0.762 without the logKOW and 0.762 (measured values) or 0.764 (all
     values) with it. With the 9 descriptors as the only inputs, adding the logKOW raises macro ROC AUC by 0.018, and
     the ROC AUC of the rarest class (additional storage sites, the class that flags a BCF the logKOW screen would
     miss) from 0.762 to 0.797.
   - Evidence: under REACH (the EU chemicals regulation) the logKOW is required from 1 tonne a year and is the first
     tier of the bioaccumulation screen, before any fish test (practitioner); the chemicals were kept for having a
     curated logKOW (record, 2026-10-07). The authors' 2015 table (Chemosphere SI) gives it for 773 of the 776
     chemicals, measured for 651 and predicted for 122. It is no leak: the logKOW alone scores 0.659, and the class
     still needs the measured BCF.
   - Implemented: structure only, unchanged until you decide.
   - Alternative: (a) add `logKOW` and a measured/predicted flag from the 2015 table: a second source file, 3
     chemicals without a value (missing stays missing, or look them up), a build. (b) rewrite the use case to a
     moment before the logKOW is known: no data change, but a use case rephrased only to excuse a gap is weighed
     against (USE-9), and the REACH sequence has no such moment.
   - Rule: USE-6 and USE-3 (Must); USE-9 (Should) weighs against (b). Advocate and critic agree that one of the two
     fixes is required.
   - Recommendation: (a) (mediator, advocate, practitioner).
   - Decision: (a) add the logKOW with its flag, or (b) rewrite the use case?

9. **Is the fit `direct` or `approximate`?**
   - Problem: `direct` says the rows, features and split mirror the use case. The definition keeps a potential leak
     on purpose (the 9 selected descriptors, issue 5) and, until issue 8 (a) is applied, lacks an input the actor
     has. The test chemicals are also random members of the literature compilation of measured BCFs that
     the 776 chemicals come from, a third of them with relatives in training (issue 10).
   - Effect: a reader of `direct` takes the score as the score of the use case; it is optimistic for chemicals of
     new families (0.779 on test chemicals whose ring skeleton is in training, 0.655 on the others).
   - Evidence: for `direct` (advocate), the selection costs at most about 0.015 macro ROC AUC, a note rather than a
     stand-in, and the logKOW gap closes under issue 8 (a). For `approximate` (critic), USE-8 lists "a potential leak
     kept on purpose" as approximate with no size threshold, and a Must has no exceptions. qsar_aquatic_toxicity
     (same selection mechanism) and kick are `approximate`; qsar_fish_toxicity (same mechanism) is `direct`.
   - Implemented: `direct`, unchanged until you decide; `fit_reason` now names the compilation and the 0.015.
   - Alternative: `approximate` with the gaps named in `fit_reason`. `direct` holds only if the 9 go (issue 5) and
     the logKOW goes in (issue 8 (a)).
   - Rule: USE-8 (Must); by its text the critic's reading wins (mediator).
   - Recommendation: `approximate`, unless issues 5 and 8 remove both gaps. Decide it in the same pass as
     qsar_oral_toxicity's issue 6 (the item "Decide the fit label of the QSAR siblings in one pass" at the end of the
     working copy's REVIEW.md).
   - Decision: `direct` or `approximate` for this dataset? (The cross-dataset item only checks that the QSAR
     siblings agree with it.)

1. **Ship the class only, or add logBCF regression as a second dataset?**
   - Problem: logBCF is the measured BCF on a log scale. The class is read from it and the logKOW, so each framing
     has to drop the other column.
   - Effect: the class is what the stated decision reads (which BCF estimate to trust). The regulatory call on
     whether a chemical is bioaccumulative (BCF above 2,000) or very bioaccumulative (above 5,000) reads the BCF
     itself, so the regression is closer to that final call.
   - Evidence: class, random forest macro ROC AUC 0.762. logBCF, random forest R² 0.718, a straight line on MLOGP
     alone 0.626: a task driven mostly by the logKOW.
   - Implemented: the class, the source's named target and the task the 9 descriptors were selected for.
   - Alternative: a `_reg` folder with logBCF as the target. Cost: a second dataset from the same 776 chemicals.
   - Rule: USE-5 (Must) holds for both; a weighing call, which the PROV-6 / PROV-7 tension row ("a shared source with
     distinct tasks is not a duplicate") allows either way.
   - Precedent: qsar_oral_toxicity ships the source's class over the LD50 behind it (precedent check, decision 1).
   - Recommendation: class only; the regression adds mostly the logKOW line, which a model learns from MLOGP.
   - Decision: class only, or add the `_reg` dataset?

5. **Keep or drop the 9 descriptors the authors selected?**
   - Problem: the authors chose the 9 Dragon descriptors out of a larger set by fitting models on their 584 training
     chemicals, labels included. Those chemicals sit in our test folds, so the choice of columns has seen test
     labels (supervised feature selection on the labelled data).
   - Effect: small. A random forest scores 0.069 higher on the authors' training chemicals than on their test
     chemicals (p = 0.04), but also 0.054 higher (p = 0.09) on the 193 RDKit columns nobody selected, so at most
     about 0.015 is the selection; logistic regression shows 0.006. In the earlier fix round the random forest scored
     0.758 without the 9 and 0.763 with them.
   - Implemented: kept, with a `Potential leak, kept on purpose:` note.
   - Alternative: drop the 9 and ship the 193 RDKit descriptors only, as home_credit_default_risk removed its
     selection at zero effect (CC 2026-10-19, LEAK-31's only case). Cost: the source's published descriptors leave;
     a build.
   - Evidence: LEAK-31 says "keep with a note when small, remove it when we can"; CLEAN-24 says the source's
     descriptors stay next to RDKit's. Your CC of 2026-10-14 asked for RDKit "next to the 9 Dragon descriptors",
     five days before LEAK-31 was written. A keep serves P5 or P7, both below P4, so it would be an amendment of
     LEAK-31 ("a selection the source published stays with a note when small"), not an exception; then the
     CLEAN-24 / LEAK-31 tension row is added and qsar_fish_toxicity and qsar_aquatic_toxicity are listed as LEAK-31
     cases. Advocate and critic both read the effect as small enough to keep.
   - Rule: LEAK-31 (Should, P4) against CLEAN-24 (Should, P7); by rank LEAK-31 wins and removal is possible here.
   - Recommendation: drop the 9 (mediator).
   - Decision: drop the 9, or keep them and amend LEAK-31?

10. **A scaffold-grouped variant next to the IID dataset?**
    - Problem: a Murcko scaffold is a chemical's ring skeleton, computed exactly from its structure. 260 chemicals
      (34%) belong to 42 congener series (families sharing a scaffold, such as 64 biphenyls and 24 naphthalenes).
      A random split puts relatives on both sides, so a test chemical often has a close relative in training.
    - Effect: a random forest falls from 0.754 to 0.650 macro ROC AUC when the congener series are held out
      (a separate 5 x 3 cross-validation, not our splits); within our splits it scores 0.779
      on test chemicals with a scaffold seen in training and 0.655 on new ones. A full scaffold split cannot be
      scored (test folds of 30 to 556 rows, 3 of 30 without a class). Grouping only the rare scaffolds (benzene and
      acyclic chemicals left random) gives 0.737 to 0.746, with the model ranking unchanged.
    - Implemented: IID stays; the notes carry the gap and no longer claim that the file has no family key. A new
      chemical under assessment usually belongs to a family already measured (SPLIT-4), and no chemical recurs
      (SPLIT-29).
    - Alternative: build a second dataset with the rare scaffolds grouped. Cost: a split key we construct, and a
      second dataset of the same 776 chemicals.
    - Rule: SPLIT-31 (Should). Same question as qsar_oral_toxicity's issue 2, here with an exact key.
    - Recommendation: list it as a candidate only (advocate and critic agree on no re-split).
    - Decision: candidate only, or build it?

**Review panel:** ship after changes (mediator). Claim audit: 41 claims, 3 refuted (the split text's "no chemical
families", the attribution of the Train-vs-Test gap to the descriptor selection, the record's text tag), all fixed or
listed; the LightGBM numbers reproduce in direction only (restated). Blind review: include with changes; its main
concerns, the 776 of 779 rows and the RDKit block, are answered by the notes. Agreed: no exclusion, no re-split, the
repair of the swapped pairs (earlier issue 2 closed), the split text and the selection note rewritten, the pretraining
issue (earlier issue 7) removed. The mediator settled that one fix of the logKOW gap is required (issue 8) and that
USE-8's text favours `approximate` (issue 9). To the curator: issues 8, 9, 1, 5 and 10, and the domain convention across
datasets. The mediator's issues 1 to 7 are this file's 8, 9, 1, 5, (4 closed as an evidence task), 10 and the
cross-dataset domain item; "REVIEW issue N" in the reports means the earlier file, whose numbers 1 and 5 are kept.

<details><summary>Mediator</summary>

One fact settled here (no model run needed): the 2026-10-07 join of UCI 510 with the 2015 table gives a 2015 logKOW for
**773 of the 776** shipped chemicals (651 experimental, 122 predicted; no match for 18936-52-2, 218-165-4,
72490-01-8). This replaces the claim audit's 772 and the practitioner's 776 (652 / 124).

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL holds. USE-1, USE-5 hold (class = the source's target, labels confirmed by the rule 599/606 and the
archived UCI page). USE-6 / USE-3 triggered: the use case presumes the KOW the assessor holds and the inputs leave it
out; fix by adding logKOW (recommended) or by rewriting the use case (issue 1). USE-8: `direct` not supported while a
potential leak is kept on purpose; approximate unless issues 1 and 3 remove both gaps (issue 2). LEAK-4, LEAK-10 hold
(logBCF dropped; MLOGP band 471/776; logKOW alone 0.659, so adding it is no leak). LEAK-16/17 hold (0 copies across the
split). LEAK-31 triggered: removable, so by rank remove the 9 Dragon descriptors (issue 4). SPLIT-1, SPLIT-4, SPLIT-29
hold: IID stays; split text wrong, corrected; SPLIT-31 scaffold variant a candidate. PROV-13 holds (3 pairs repaired,
3 rows dropped). PROV-15 / EV-4: REVIEW issue 7 goes.
Value: TP-2 holds (RF macro AUC 0.762, log-loss skill +0.18 over the prior); TP-5 holds (21-22 class-2 rows per test
fold).
Quality: CLEAN-11 holds (RDKit extremes and 7 NaN rows are structure-caused); CLEAN-24 holds.
Weighed: use case +, source +, repair +, size -, congener-driven signal -.
For the curator: issues 1 to 4 (logKOW, fit label, descriptor selection, target framing), then 5 to 7.
```

No exclusion and no re-split. Adding logKOW (issue 1) or dropping the 9 descriptors (issue 4) makes a new container:
build only on the curator's ask, with a CHANGELOG entry and the README table updated.

**Changes to make now (no decision needed)**

1. **Split text** (SPLIT-4, SPLIT-31, EV-2; as qsar_oral_toxicity change 4). Delete "the file has no chemical families
   for a stricter split" from `task_summary.split` and "holds no key of chemical families" from the Split bullet. Rest
   IID on the use case (a new chemical each time, usually of a family already measured; no entity recurs, SPLIT-29).
   Add a note with the measured gap: 42 congener series hold 260 rows (34%); RF 0.754 to 0.650 with the series held
   out; 0.779 on test rows with a seen scaffold against 0.655 on a new one; the full scaffold split is not scorable
   (test folds 30 to 556 rows, 3 of 30 lack a class). Name the dataset a SPLIT-31 candidate. In `fit_reason`, say the
   test chemicals are random members of the historical BCF compilation.
2. **Descriptor-selection note** (LEAK-31, EV-2). Remove "as home_credit_default_risk" (that case was reversed on
   2026-10-19). Add the control: RF Train-vs-Test gap +0.069 (p = 0.04) on the 9, +0.054 (p = 0.09) on the 193 RDKit
   columns nobody selected, so at most about 0.015 is selection. If issue 4 keeps the 9, word it
   `Potential leak, kept on purpose:`; if it drops them, the note becomes the reason for the drop.
3. **Label provenance note** (USE-5, EV-7). 122 shipped chemicals have a predicted logKOW in the 2015 table and the
   band rule fits 72% of them; below logKOW 1 the class is mostly class 1 by convention. Same correction in the
   record's 2026-10-07 assessment ("the 779 are ... with an experimental KOW" holds only for the 2016 re-curation).
4. **REVIEW issue 7 removed** (PROV-15 Must, EV-4). The TabSTAR label swap moves from `curation_comments` to the
   record as a problem of that copy.
5. **REVIEW issue 2 closed** (PROV-13 Must): the drop-six alternative cleans around damage the origin repairs.
6. **Numbers** (EV-8). LightGBM 0.735 / 0.752 (13 of 15) reproduces as 0.745 / 0.757 (12 of 15) with defaults: state
   the settings or use the reproduced numbers.
7. **Record** (records.md). Remove the stale tag `Free Text (Short)` (no string feature since 2026-10-14); replace
   "no known risk" in the 2026-10-20 assessment with the open issues below (as qsar_oral_toxicity change 8).
8. **Spelling** (writing.md): "metabolised" in `task_summary.predicted` to "metabolized", as the label.

**Issues for the curator (ranked)**

1. **The logKOW the class is read against is not an input** (P3; USE-6 Must, USE-3 Must).
   * Problem: `use_case` says the assessor decides whether the KOW-based estimate "can be trusted", which presumes a
     known KOW; `known` says structure only. The definition states two prediction points.
   * Effect: small on the score (RF 0.762 to 0.762 / 0.764 on the shipped features; +0.018 and class 2 0.762 to 0.797
     on the 9 alone), real on the framing.
   * Both sides now agree one fix is required. For (a) add `logKOW` and an exp/pred flag from the 2015 table (advocate,
     practitioner): REACH requires the logKOW before any fish test, the cohort was kept for its curated KOW, and no
     leak (logKOW alone 0.659). For (b) rewrite the use case to "before the KOW is known" (critic accepts either): no
     new source file, no build.
   * Rule: USE-6 wins for the use case as written; (b) meets the weighed factor against "a use case rephrased only to
     excuse a gap" (USE-9) and a moment the REACH sequence does not have. Recommendation: (a).
   * Decision: (a), which adds the Chemosphere 2015 SI table as a source file, 3 rows without a value (missing stays
     missing, or look them up), and a build; or (b).
2. **Fit label: direct or approximate** (P3; USE-8 Must).
   * Problem: `fit = "direct"` while `fit_reason` names a kept potential leak (the 9) and the inputs miss the logKOW.
   * Advocate: the selection effect is at most 0.015 AUC, so a note, not a stand-in; direct once (a) is applied.
   * Critic: USE-8 lists "a potential leak kept on purpose" as approximate with no size threshold, and a Must has no
     exceptions; qsar_aquatic_toxicity (same mechanism) and kick are approximate.
   * Rule: the critic's reading wins by the text of USE-8. `direct` is reachable only if the 9 go (issue 4) and the
     logKOW goes in (issue 1). Recommendation: approximate with the gaps named, unless both happen.
   * Decision: the label, in the same pass as qsar_oral_toxicity issue 1 (random members of the tested set against the
     untested chemicals screened), which applies word for word here and to qsar_fish_toxicity (direct, same mechanism).
3. **Target framing: the class or logBCF regression** (P3, a weighing; REVIEW issue 1, unchanged). Class: the source's
   target and the stated decision (RF macro AUC 0.762). logBCF: closer to the final B/vB call (RF R^2 0.718, MLOGP
   alone 0.626, KOW-dominated). The PROV-6/7 tension row allows a `_reg` sibling. Decision: class only, or add `_reg`.
4. **Keep or drop the 9 selected Dragon descriptors** (P4; LEAK-31 Should against CLEAN-24 Should, P7).
   * A real conflict: keeping the source's descriptors keeps the selection. By rank LEAK-31 wins, and it says "remove
     it when we can"; here we can (RF 0.758 without the 9, 0.763 with). home_credit_default_risk removed its selection
     at zero effect (CC 2026-10-19). The remedy ladder prefers fixing the definition to a kept note.
   * For keeping: the selection is the source's published feature set, the effect is at most 0.015 AUC and not
     significant, and your CC of 2026-10-14 asked for RDKit "next to the 9". That CC predates LEAK-31 (2026-10-19),
     and the newer rule wins by default. An exception would serve P5 or P7, both below P4, so a keep is an amendment
     of LEAK-31 ("a selection the source published stays with a note when small"), not an exception.
   * Recommendation: drop the 9. Decision: drop (follows home_credit), or keep by amending LEAK-31 (then add the
     CLEAN-24 / LEAK-31 tension row and list qsar_fish_toxicity and qsar_aquatic_toxicity as LEAK-31 cases).
5. **Paper text unread** (EV-7; REVIEW issue 4). The thresholds are stated as inferred, not attributed to the paper
   (PROV-16 not triggered), and the labels are confirmed on the data and the archived UCI page. Critic: keep it open
   until the paper's wording is read. Decision: close as an issue and keep as an evidence task, or keep open.
6. **Scaffold-grouped variant** (P4; SPLIT-31 Should). Same question as qsar_oral_toxicity issue 2, with an exact key
   here (Murcko scaffolds from the SMILES). Rare scaffolds grouped, benzene and acyclic IID: 0.737 to 0.746, ranking
   unchanged. Decision: list as a candidate only, or build it.
7. **Domain convention** (no rule; REVIEW issue 6). "chemistry & material science" (qsar_oral_toxicity, qsar_tid_11)
   or "biology & life sciences" (qsar_fish_toxicity, qsar_aquatic_toxicity, qsar_biodeg). Decision: one value for the
   QSAR siblings.

**Agreed facts**

* UCI 510: 779 chemicals; shipped 776 (458 / 64 / 254), the 3 dropped rows have another chemical's structure; sha256
  reproduces.
* The class is a +-0.5 band around the TGD line on logBCF and the experimental logKOW: 599 of 606 with logKOW >= 1;
  labels match the archived UCI page; class 2 lies above the line (residual +0.79).
* logBCF dropped; with MLOGP the band gives 471 of 776; no feature completes the rule; best single feature 0.670.
* Three swapped pairs repaired (PubChem, PCD, the 2015 table agree); Dragon B02, F04, nHM match the repaired SMILES on
  776 / 776; random 60-row PubChem check 59 match, 1 no hit.
* 0 copies across the split (exact, InChIKey, connectivity block); 193 of 217 RDKit columns kept.
* IID: RF 0.762 +- 0.021, log loss 0.720 against a prior of 0.883; 21-22 class-2 rows per test fold.
* 34% of rows in 42 congener series; holding them out costs about 0.10 macro AUC; the full scaffold split is not
  scorable.
* The Train-vs-Test gap is about as large on unselected RDKit columns (+0.054) as on the 9 (+0.069).
* logKOW: 773 of 776 in the 2015 table (651 exp, 122 pred); adding it is no leak.

**Consistency with precedent**

* Follows qsar_oral_toxicity today: split text corrected and SPLIT-31 candidate (its change 4), "no known risk"
  replaced (change 8), fit label answered with its issue 1.
* Repair follows SUPPORT2 and ashrae (PROV-13); the three drops follow drug_induced_autoimmunity_prediction; SMILES to
  RDKit follows apistox and the CC of 2026-10-14 (CLEAN-24); REVIEW issue 7 removal follows the EV-4 cases.
* Approximate (issue 2) matches qsar_aquatic_toxicity and kick. Keeping `direct` with the 9 would depart from both with
  no distinguishing fact beyond size, which USE-8 does not admit: a question, not a recommendation.
* Keeping the 9 departs from home_credit_default_risk (LEAK-31's only case). The fact offered (the source published the
  selection) sets the case apart, but serves a lower principle, so it is issue 4's amendment question.

</details>

<details><summary>Claim audit</summary>

Data: the definition's frame and split plan (776 x 203, 30 splits), mapped back to
CAS / Set / SMILES / logBCF through the definition's own cleaning (all 776 rows matched, class agreement 1.0).
Models: untuned RandomForest (300 trees, min_samples_leaf 2) and default LightGBM, macro OvR ROC AUC and log loss;
class-prior log loss 0.883.

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 6, 26 | "the file has no chemical families for a stricter split" / "The file holds no key of chemical families" | task_summary.split; curation_comments "Split" | Build Murcko scaffolds exactly from the shipped SMILES; compare IID with series held out (StratifiedGroupKFold, 5 x 3, benzene and acyclic rows as singletons) | **refuted** (the fact); the IID choice itself is a weighing call | 297 Murcko groups; 42 multi-member series (biphenyls 64, naphthalenes 24, diphenyl ethers 21, diphenylmethanes 18, dibenzofurans 9, triazines 9, dioxins 8, anthraquinones 8) hold 260 rows (34%). RF OOF macro AUC IID 0.754 / log loss 0.724; series held out 0.650 / 0.835 (prior 0.883). Rows in a series: 0.804 IID vs 0.553 held out; rows outside: 0.714 vs 0.710. Plain GroupKFold on raw scaffolds: 0.756 -> 0.654. Leak probe's 1-NN closest-tenth agreement 0.808 vs 0.649 is the same effect. | SPLIT-24 (key constructible exactly from the data), SPLIT-29/30/31, SPLIT-4, USE-8 |
| 8 | fit "direct"; "a held-out chemical is an untested one" | task_summary.fit_reason | as above | holds in part | Each test chemical is new (0 duplicate canonical SMILES / InChIKey / connectivity block; 0.0% exact feature copies), but a third of them have congeners in train and that is where most of the IID signal sits (0.804 vs 0.553). Precedent qsar_oral_toxicity keeps IID and writes the scaffold gap down. | USE-8, SPLIT-31 |
| 8, 27 | "The authors chose the nine descriptors on chemicals that also sit in our test folds, which may favour those slightly"; RF +0.064 (p = 0.06), LR +0.003 | fit_reason; curation_comments Note | Re-run the paired OOF test on the shipped 30 splits (null: 50 random subsets of 195 per repeat), then the same with RDKit-only features, which the authors did not select | numbers hold; **the attribution is refuted** | RF on the 9: gap +0.069 (null -0.001, sd 0.043, p = 0.04); LR on the 9: +0.006 (p = 0.45). RF on the 193 RDKit columns only: +0.054 (p = 0.09); all features +0.051 (p = 0.10). The Train-vs-Test gap is about as large without the selected descriptors, so at most ~0.015 of it can be selection; the rest is the authors' Test chemicals being harder. | LEAK-31, EV-6 |
| 17, 5 | Implied: what is known at the prediction point is the structure only | curation_comments "Prediction point"; task_summary.known | The experimental logKOW is measured before a fish test (the cohort is the chemicals with a curated KOW). Join the 2015 table's LogKOW and add it as a feature | holds (gap immaterial) | 772 of 776 matched (650 exp, 122 pred). RF macro AUC 0.762 -> 0.762 with exp logKOW, 0.764 with any logKOW, 0.767 with logKOW and its TGD value; log loss 0.720 -> 0.718. MLOGP vs exp logKOW r = 0.87. | USE-3, USE-6 |
| 4, 18, 36 | The class is a +-0.5 band around the TGD line on logBCF and experimental logKOW; 600 of 607 with logKOW >= 1 | task_summary.predicted; curation_comments "Target"; record | Recompute with the 2015 LogKOW | holds | 599 of 606 (one row lost to a "/"-joined CAS in my join); 702 of 772 overall; 72% on the 122 rows whose 2015 KOW is "pred". logBCF equal to the 2015 table on 771 of 772. Paper text still unread (thresholds inferred). | USE-5, EV-7 |
| 13, 28 | Labels 1 lipid storage, 2 additional storage sites, 3 metabolized or eliminated, "as the old UCI page names them"; class 2 lies above the TGD line | CLASS_LABELS; curation_comments Note | Fetch the archived old UCI page; residual of logBCF from the TGD line on MLOGP by class | holds | Wayback snapshot 2023-03-27: "(1) is mainly stored within lipid tissues, (2) has additional storage sites (e.g. proteins), or (3) is metabolized/eliminated". Mean residual: class 1 +0.29, class 2 +0.79, class 3 -0.55. | PROV-8, EV-2 |
| 14, 23 | Three pairs carry each other's SMILES and descriptors; BCF and class belong to the CAS | SWAPPED_PAIRS; curation_comments | Raw rows; PubChem CAS -> structure; do the descriptors follow the SMILES? | holds | Raw: 71-43-2 has `C1CCCCC1`, 110-82-7 `c1ccccc1`, etc. PubChem: 71-43-2 benzene, 91-20-3 naphthalene, 108-90-7 chlorobenzene. After repair the aromatic rows carry PCD > 0 (1.22, 2.37, 1.23) and the saturated ones PCD 0, X2Av/MLOGP follow the structure. 2015 table lists the CAS chemicals with the file's logBCF. | PROV-13 |
| 15, 24 | Three rows carry another chemical's structure; checked for every row | WRONG_STRUCTURE | PubChem for the three; PubChem for a random 60 rows | holds (every-row claim tested on a sample) | 131983-72-7 is triticonazole in PubChem (file SMILES is a cyclohexanedione ester, trinexapac-ethyl); 33423-92-6 = 1,3,6,8-TCDD; 39227-28-6 = 1,2,3,4,7,8-HxCDD while the file's SMILES puts Cl at 6,7. Random 60: 59 connectivity blocks match, 1 no PubChem hit (3811-49-2). A full 779-row run was too slow and was stopped. | PROV-13, EV-7 |
| 3, 16 | 779 -> 776 chemicals, 59 / 33 / 8 % | task_summary.row; curation_comments | Counts | holds | raw 779 (460/64/255); shipped 776 (458/64/254); the three dropped rows are all authors' Train (581 Train, 195 Test shipped). | |
| 21, 30 | 193 of 217 RDKit descriptors (others constant or copies); 9 descriptors: 743 distinct, 61 sharing, 14 multi-class; with RDKit 776 distinct | curation_comments; Decision 3 | Recompute | holds | 217 - 17 constant - 7 copies = 193; 9-descriptor sharing 61 / 14 reproduced; RDKit 2026.03.6 installed. 88 molecular formulas are shared by 266 rows (36 mixed-class), all told apart by RDKit. 2 SMILES carry stereo. | CLEAN-22 |
| 21, 40 | LightGBM macro AUC 0.735 with the 9, 0.752 with RDKit added, better on 13 of 15 splits | curation_comments; record | Default LGBM on the first 15 shipped splits | holds in direction, numbers differ | 0.745 vs 0.757, better on 12 of 15; RDKit only 0.755. Default LGBM log loss 0.962 / 1.128, worse than the prior 0.883 (task probe says the same). Parameters of the original run not stated. | EV-8 |
| 29 | MLOGP band gives 471 of 776 | Decision 1 | Generated from code; diagonal 45 + 286 + 140 | holds | | |
| 37 | The 779 are the 2015 table's chemicals with an experimental KOW | record 2026-10-07 | 2015 table "KOW type" | holds in part | 280 of the 283 table rows not in UCI 510 are "pred", but 122 of the 772 shipped rows matched are also "pred" in 2015; the claim rests on the 2016 re-curation (Environ. Res. SI quote in the 2026-10-07 verify, not re-read here). | EV-2, EV-7 |
| 34 | Record tag "Free Text (Short)" | record front matter | README feature types | **refuted** (stale) | 0 string features shipped; SMILES dropped since 2026-10-14. | records.md |
| 22, 31 | SMILES as character n-grams lowers LightGBM from 0.735 to 0.723; "adds nothing" | curation_comments; Decision 3 | | untested | Not re-run: decision already taken by the curator (CC 2026-10-14) and the encoding of the original run is not stated. | EV-7 |
| 9, 10 | CC BY 4.0, UCI 510 donated 2019 | dataset.py | | untested here | Not re-fetched in this audit (the checklist fetched the UCI page). sha256 of the raw file matches (checklist). | EV-7 |
| 28 + REVIEW_before 7 | TabSTAR swaps classes 2 and 3; pretraining overlap as a curator issue | curation_comments; REVIEW_before | Rule check | process finding | Our labels are confirmed by the data and the old UCI page (row above), so the TabSTAR note is provenance only; pretraining overlap and another collection's labels are "never evidence" and "none of them is an issue for the curator". | EV-4 |
| 9 + REVIEW_before 6 | domain "chemistry & material science" | dataset.py | Siblings | weighing, unchanged | qsar_fish_toxicity, qsar_aquatic_toxicity, qsar_biodeg, bioresponse, apistox: biology & life sciences; qsar_oral_toxicity, qsar_tid_11, clock_protein_toxicity: chemistry. | P7 consistency |
| implied | No row is a copy across the split | (none) | Canonical SMILES, InChIKey, connectivity block, exact feature vectors | holds | 0 / 0 / 0 duplicates in the raw file; 0.0% exact copies (leak probe). Near relatives: see row 1. | LEAK-16, LEAK-17 |
| implied | The target is the real-world target | (none) | | holds as framed | The class is what the use case's decision reads (does the KOW estimate hold for this chemical); a REACH B/vB call reads the BCF itself, which is the logBCF regression of REVIEW_before issue 1 (weighing, already open). | USE-5 |

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. **P4, SPLIT-24 / SPLIT-31 (Should-level call; the fact behind it is wrong).** "No chemical families for a stricter
   split" is false: Murcko scaffolds are constructed exactly from the shipped SMILES (allowed by SPLIT-24), and 34% of
   rows sit in 42 congener series. Holding the series out costs RF 0.10 macro AUC (0.754 -> 0.650; log loss 0.724 ->
   0.835 against a prior of 0.883), and on the series rows the IID score (0.804) falls to near chance (0.553). What
   it changes: the split statement and the fit reason say less than the data shows; the benchmark mostly rewards
   recognising a congener's series. Not a Must violation: new chemicals keep having these scaffolds (SPLIT-4: a value
   new rows keep having is a feature), and the source split is random stratified. Mildest remedy: keep IID, follow the
   qsar_oral_toxicity precedent: rewrite task_summary.split and the "Split" bullet ("Random chemicals; a third belong to
   congener series that also sit in train; a scaffold key could be built from the SMILES") with the measured gap, and
   name the dataset a candidate for a grouped variant (SPLIT-31). Curator call whether the fit stays "direct".
2. **P4, LEAK-31 (Should).** The descriptor-selection note and fit_reason attribute the Train-vs-Test gap to the
   authors' selection. The numbers reproduce (+0.069, p = 0.04), but RDKit-only features, which nobody selected, show
   +0.054 (p = 0.09): at most ~0.015 is selection. What it changes: the stated risk is smaller than written, and the
   "may favour those slightly" in fit_reason can go or be reworded. Remedy: one sentence in the Note with the
   RDKit-only control.
3. **P3/P5, record (quality).** Tag "Free Text (Short)" is stale since the SMILES was dropped. Remedy: remove the tag
   (the curator's record edit).
4. **Procedure, EV-4.** REVIEW_before issue 7 (pretraining overlap) is an issue EV-4 says never goes to the curator;
   the TabSTAR label note is provenance only. Remedy: drop issue 7 from REVIEW.md, keep at most a one-line provenance
   note.
5. **EV-8, numbers.** LightGBM 0.735 / 0.752 (13 of 15) reproduces as 0.745 / 0.757 (12 of 15) with default
   parameters; direction holds. Remedy: state the model settings, or leave.
6. **Untested.** Claim 22/31 (SMILES n-grams 0.723), licence and donation date (not re-fetched), the paper's own
   threshold text (still unread; class names now confirmed on the archived old UCI page), the every-row PubChem check
   (confirmed on 9 named + 60 random rows, 59 match, 1 without a PubChem hit).

Held under attack: no copies across the split (0 exact, 0 InChIKey), the class rule and label names, the swap repair
and the three drops, the 193 RDKit columns, logBCF gone and no feature completing the rule (MLOGP 471 of 776), and
withholding the experimental logKOW (adds +0.002 AUC).

</details>

<details><summary>Column audit</summary>

Frame rebuilt from the definition: 776 rows x 203 columns (202 features + target), IID.

Prediction point (curation_comments, bullet 1): an organic chemical whose fish bioconcentration has not been
measured, before a fish test; its structure and descriptors computed from it are known; the measured BCF and the class
read from it are not. Every shipped feature is a function of the structure only, so every feature exists before the
prediction point by construction.

**Measurements made in this audit**

* **Dragon descriptors agree with the repaired SMILES on every row.** Recomputed from the shipped (repaired) SMILES
  with RDKit: `B02(C-N)` (C-N pair at topological distance 2) matches on 776/776, `F04(C-O)` (count of C-O pairs at
  distance 4) on 776/776, and `nHM` equals the count of atoms other than H, C, N, O, F on 776/776. So the swap-back of
  the three pairs put the authors' descriptors on the right rows, and no other row carries descriptors of a structure
  other than its SMILES (independent confirmation of PROV-13 work; it cannot see a SMILES that is wrong together with
  its descriptors, which is the CAS lookup's job).
* **MLOGP vs RDKit MolLogP**: r = 0.87; largest gaps are organotins, siloxanes, nitramines and perhalogenated
  aromatics, where Moriguchi's and Crippen's schemes are known to differ. No sign of experimental logKOW in MLOGP.
  Single-feature one-vs-rest AUC: MLOGP 0.61 / 0.37 / 0.60 (classes 2 / 1 / 3), MolLogP 0.60 / 0.35 / 0.64. No
  feature completes the label rule (decision table: MLOGP band 471/776; leak probe best single feature 0.670, all 0.742,
  no drop moves the score).
* **Missing values**: 12 RDKit columns (4 Gasteiger partial-charge columns and the 8 BCUT2D columns) are missing on the
  same 7 rows, all organotins (Gasteiger has no Sn parameters): CAS 1067-97-6, 1461-22-9, 41083-11-8, 56-35-9, 639-58-7,
  76-87-9, 900-95-8. Classes: 4 additional storage sites, 3 lipid storage (base rate of class 2 is 8%). The missingness
  is caused by the structure, not the outcome, and is real (the value is undefined), not a proxy. The leak probe's
  missing-indicator AUC is 0.5 at three folds; legitimate structure signal in any case.
* **Copies (CLEAN-5)**: 202 distinct columns, no exact copies, none constant; 18 `rdkit_fr_*` flags are non-zero on 1-3
  rows only (rare, not constant: keep). `rdkit_MolWt` and `rdkit_ExactMolWt` correlate at 0.99996 but differ
  (average vs monoisotopic mass): not a copy.
* **Extreme values**: `rdkit_Kappa3` = 9,508 for pivalic acid (next largest 137), a known blow-up of the Kier kappa-3
  formula for small, highly branched molecules (denominator near zero); `rdkit_Ipc` up to 7.7e9 (the unnormalised
  information content grows combinatorially; heavy tail, not an error). Both are what pinned RDKit 2026.03.6 returns
  for a valid structure: unusual, not impossible (CLEAN-11 keeps them). Tree models are unaffected; a note at most.
* **Target**: category with 3 levels, 458 / 64 / 254 as claimed; labels from `CLASS_LABELS`.

**Column table**

The 193 RDKit columns are grouped by descriptor family; the verdict holds for every member. "Known?" is whether the
value exists at the prediction point.

| Column | Meaning (source) | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `bioconcentration_mechanism` (target) | mechanistic class: 1 lipid storage, 2 additional storage sites, 3 metabolized or eliminated; a rule on measured logBCF and experimental logKOW (TGD line +-0.5) per the curation; labels "as the old UCI page" (the archived page was not fetched by the panel) | target, after the fish test | category, 3 levels, no NA; renamed from `Class` with labels | fine (labels' source wording unverified: question carried from checklist) | USE-5, CLEAN-17, EV-7 |
| `nHM` | Dragon: number of heavy atoms; measured here as every atom other than H, C, N, O, F (776/776) | yes, structure | int64, 0-12, no NA | fine | CLEAN-14 |
| `piPC09` | Dragon: molecular multiple path count of order 9 (ln(1+x) scale, per row) | yes | float64, 0-9.32 | fine | CLEAN-14, LEAK-30 (per-row transform is fine) |
| `PCD` | Dragon: difference between multiple path count and path count (a pi-bond / aromaticity measure) | yes | float64, 0-5.9 | fine | CLEAN-14 |
| `X2Av` | Dragon: average valence connectivity index of order 2 | yes | float64, 0.09-2.23 | fine | CLEAN-14 |
| `MLOGP` | Dragon: Moriguchi octanol-water partition coefficient, calculated from structure (not the experimental logKOW the label is read from) | yes | float64, -1.96 to 8.32 | fine; it is the calculated half of the label rule and completes it on 471/776 only | LEAK-10 (does not apply), USE-6 |
| `ON1V` | Dragon: overall modified Zagreb index of order 1 by valence vertex degrees | yes | float64, 0.08-7.19 | fine | CLEAN-14 |
| `N-072` | Dragon atom-centred fragment N-072 (RCO-N< / >N-X=X) count | yes | int64, 0-3 | fine | CLEAN-14 |
| `B02(C-N)` | Dragon: presence of a C-N pair at topological distance 2; verified 776/776 against SMILES | yes | int64 0/1 (binary flag as numeric: fine); renamed from `B02[C-N]` | fine | CLEAN-14 |
| `F04(C-O)` | Dragon: frequency of C-O pairs at topological distance 4; verified 776/776 | yes | int64, 0-25; renamed from `F04[C-O]` | fine | CLEAN-14 |
| The 9 Dragon columns, jointly | selected by the authors (genetic algorithm / tree) on their 584 training chemicals, labels included, which sit in our test folds | yes (values); the *choice* of columns used labels | per-row values, no scaling over rows | potential leak, weak, kept with a note (curation measured RF +0.064 macro AUC on the authors' training chemicals, p = 0.06; LR +0.003); the RDKit block dilutes it | LEAK-31 (Should) |
| `rdkit_MolWt`, `rdkit_ExactMolWt`, `rdkit_HeavyAtomMolWt`, `rdkit_HeavyAtomCount`, `rdkit_NumValenceElectrons` | size and mass | yes | float64, no NA | fine (MolWt and ExactMolWt 0.99996 correlated, not copies) | CLEAN-5 |
| `rdkit_MolLogP`, `rdkit_MolMR`, `rdkit_TPSA`, `rdkit_LabuteASA`, `rdkit_qed`, `rdkit_SPS`, `rdkit_FractionCSP3` | Crippen logP and molar refractivity, polar and approximate surface area, drug-likeness, spatial score, sp3 fraction | yes | float64, no NA | fine | |
| `rdkit_MaxPartialCharge`, `rdkit_MinPartialCharge`, `rdkit_MaxAbsPartialCharge`, `rdkit_MinAbsPartialCharge` | Gasteiger charge extremes | yes | float64, 7 NA (organotins, no Sn parameters: real missing) | fine | CLEAN-10 (no proxy), LEAK-10 (missingness by structure, not outcome) |
| `rdkit_BCUT2D_MWHI`, `_MWLOW`, `_CHGHI`, `_CHGLO`, `_LOGPHI`, `_LOGPLOW`, `_MRHI`, `_MRLOW` | Burden-matrix eigenvalue descriptors weighted by mass, charge, logP, MR | yes | float64, 7 NA (same organotins; the charge-weighted ones need Gasteiger) | fine | as above |
| `rdkit_MaxAbsEStateIndex`, `rdkit_MinAbsEStateIndex`, `rdkit_MinEStateIndex` | E-state index extremes | yes | float64, no NA | fine | |
| `rdkit_AvgIpc`, `rdkit_Ipc`, `rdkit_BalabanJ`, `rdkit_BertzCT`, `rdkit_HallKierAlpha`, `rdkit_Phi` | topological information and complexity indices | yes | float64; `Ipc` heavy-tailed up to 7.7e9 (valid output) | fine | CLEAN-11 (unusual stays) |
| `rdkit_Chi0`, `Chi0n`, `Chi0v`, `Chi1`, `Chi1n`, `Chi1v`, `Chi2n`, `Chi2v`, `Chi3n`, `Chi3v`, `Chi4n`, `Chi4v` | Kier-Hall connectivity indices | yes | float64, no NA | fine | |
| `rdkit_Kappa1`, `rdkit_Kappa2`, `rdkit_Kappa3` | Kier shape indices | yes | float64; `Kappa3` 9,508 on pivalic acid (formula blow-up, next 137) | fine; optional note | CLEAN-11 |
| `rdkit_FpDensityMorgan1/2/3` | Morgan fingerprint bit density | yes | float64 | fine | |
| `rdkit_EState_VSA1`-`10`, `rdkit_VSA_EState1`-`10`, `rdkit_PEOE_VSA1`-`14`, `rdkit_SMR_VSA1`-`7`, `9`, `10`, `rdkit_SlogP_VSA1`-`8`, `10`-`12` | surface area binned by E-state, Gasteiger charge, MR, logP contribution (fixed published bins, per molecule) | yes | float64, no NA; the bins missing from the numbering were dropped as constant or copies (curation: 193 of 217) | fine | LEAK-30 (fixed published scale), CLEAN-5 |
| `rdkit_NHOHCount`, `NOCount`, `NumHAcceptors`, `NumHDonors`, `NumHeteroatoms`, `NumRotatableBonds`, `NumAmideBonds`, `NumBridgeheadAtoms`, `NumAtomStereoCenters`, `NumUnspecifiedAtomStereoCenters` | counts | yes | float64 counts (numeric: fine) | fine | CLEAN-14 |
| `rdkit_RingCount`, `NumAliphaticCarbocycles`, `NumAliphaticHeterocycles`, `NumAliphaticRings`, `NumAromaticCarbocycles`, `NumAromaticHeterocycles`, `NumAromaticRings`, `NumHeterocycles`, `NumSaturatedCarbocycles`, `NumSaturatedHeterocycles`, `NumSaturatedRings` | ring counts | yes | float64 counts | fine | |
| `rdkit_fr_*` (68 columns: `Al_COO` ... `urea`) | RDKit functional-group fragment counts | yes | float64 counts; 18 non-zero on 1-3 rows only (not constant) | fine | CLEAN-5, CLEAN-22 |
| `CAS` (dropped) | CAS registry number(s); some cells hold two | n/a | dropped | fine: uninformative identifier, used only for the repair | CLEAN-3 |
| `Set` (dropped) | the authors' Train/Test assignment | n/a | dropped | fine (a split label, not a feature; its link to the descriptor selection is LEAK-31 above) | LEAK-33, CLEAN-3 |
| `logBCF` (dropped) | measured log bioconcentration factor in fish | no: the outcome measurement | dropped | fine: correctly removed (the class is read from it) | LEAK-10, CLEAN-22 |
| `Class` (dropped) | the integer class | target | replaced by the labelled target | fine | |
| `SMILES` (dropped) | structure as text | yes | replaced by RDKit descriptors, then dropped | fine (curator's CC 2026-10-14) | CLEAN-24 |

**Problems, ranked by principles.md**

No column is a leak under LEAK-10, no column needs a remedy in the definition, and the cleaning meets the P7 rules.
What remains, in rank order:

1. **P4, LEAK-31 (Should), weak: the 9 Dragon descriptors were selected on labelled rows that sit in our test folds.**
   Evidence: curation_comments' measurement (RF +0.064 macro AUC on the authors' 584 training chemicals vs their test
   chemicals, one-sided p = 0.06; LR +0.003); the leak probe shows no single feature carrying it (best 0.670, drops move
   nothing). The selection affects which columns exist, not their values, and the 193 RDKit columns are unselected.
   Mildest remedy: what the definition already does, keep with a note; for consistency with LEAK-30/LEAK-31 house style,
   the note could be worded `Potential leak, kept on purpose:` (it is now "Note:"). The alternative (drop the 9, ship
   RDKit only) is a curator call; the curation measured 0.735 with the 9 vs 0.752 with RDKit added, so the 9 are not
   what carries the score.
2. **P3, USE-6 / USE-5, question for the curator: the experimental logKOW.** The use case says the assessor decides
   "whether the usual estimate from its octanol-water partitioning can be trusted", which presumes a known KOW, and
   every one of the 779 chemicals was kept because it has an experimental KOW (record, 2026-10-07). A measured logKOW is
   a cheap test usually run before a fish BCF test, so under USE-6 it would be a legitimate input, not a leak; it is
   also half of the label rule, so adding it (from the 2015 SI table) would turn the task into "predict the residual of
   logBCF from the TGD line given KOW". The current framing (structure only) is coherent with "untested chemical" and
   the paper's QSAR framing. No change proposed; one sentence in the use case or curation_comments saying why the
   experimental logKOW is not an input would close it.
3. **P3/P5, USE-5 / EV-7, carried question: the class labels.** The labels follow "the old UCI page", which the panel
   could not fetch; the rule (class 2 above the TGD line) supports class 2 = additional storage sites. Not a column
   defect; listed because the target's naming is unverified from a primary document (REVIEW_before issue 4 and 7).
4. **P7, CLEAN-11, note only: two extreme RDKit values.** `rdkit_Kappa3` = 9,508 on pivalic acid and `rdkit_Ipc` up to
   7.7e9 are valid outputs of the pinned RDKit (formula blow-up / combinatorial growth), unusual, not impossible: keep.
   Applies to every SMILES dataset alike (CLEAN-24 uses one RDKit for all), so no per-dataset action.
5. **Writing nit (writing.md):** the target level is spelled "metabolized or eliminated" (`CLASS_LABELS`) and the
   task_summary says "metabolised". Mildest remedy: one spelling.

Confirmed fine and worth recording as positive evidence: the Dragon `B02(C-N)`, `F04(C-O)` and `nHM` values match the
repaired SMILES on all 776 rows (the swap-back is correct and no other row has mismatched descriptors); the only
missing values are 7 organotins without Gasteiger parameters (structure-caused, real missing); no exact or constant
columns; CAS, Set, logBCF, Class and SMILES are dropped for the right reasons.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** IID (stratified 3-fold x 10 repeats, 517-518 train / 258-259 test, smallest class in a
test fold 21) fits the use case: one row per chemical, a new untested chemical each time, no entity that recurs. Two
notes: the split text claims the file has no chemical families (wrong: the SMILES gives exact Murcko scaffolds), and
the dataset lacks the applicability-domain note its sibling qsar_oral_toxicity carries.

Data: the container rebuilt from the definition; 776/776 rows aligned to the raw SMILES by their 202 feature
values, class agreement 1.0. Models: random forest (500 trees,
min_samples_leaf 2) and L2 logistic regression (C 0.1, standardised), untuned; metric macro one-vs-rest ROC AUC and
log loss (dummy log loss 0.883).

**Regime against the use case**

* Use case: "a chemical assessor estimates the bioconcentration mechanism of an untested organic chemical from its
  structure". One prediction = one chemical; nothing is known about it but its structure. No time axis: BCF values
  come from a literature compilation (2015 table), not a stream; nothing points to a temporal use (SPLIT-6/7 not
  triggered). New-entity regime (USE-10, USE-11): one row per chemical, so the cold start is IID without grouping.
* Exact copies: 0 duplicate CAS / canonical SMILES (checklist), 776 distinct feature vectors, 0.0% copies across the
  split (leak probe). LEAK-17 / SPLIT-29 not triggered at the chemical level.
* Hidden-group probe: no hits (4 candidates, all count descriptors with negative gaps); near copies at Tanimoto 0.85:
  9 pairs, 2.3% of rows, gap -0.000. Nothing to re-split on (SPLIT-30).

**The structure family question (the one open point)**

A chemical family is not an entity in the SPLIT-24 sense, but a Murcko scaffold is constructed exactly from the SMILES
(not a similarity cluster), so it is a legal key if the use case needs unseen families.

| Fact | Number |
|---|---|
| Murcko scaffolds | 194 (generic: 115); 104 acyclic rows |
| Largest scaffolds | benzene 262 rows (34%), biphenyl 64, naphthalene 24, diphenyl ether 21, diphenylmethane 18 |
| Rows in a scaffold shared with another row | 626 of 776; 150 singletons |
| Ring test rows whose scaffold is in train (shipped splits) | 75.1% |
| Nearest-neighbour Tanimoto (Morgan r2) of a test row to train | median 0.51; 44.8% below 0.5; 2.4% at 0.85 or more |

Scores (RF; LR in brackets):

| Split | macro AUC | log loss |
|---|---|---|
| shipped IID, 30 folds | 0.762 +- 0.021 (0.719) | 0.720 (0.954) |
| scaffold-grouped, StratifiedGroupKFold 3x10 | 0.611 +- 0.051 (0.588), 3 of 30 folds lack a class, test sizes 30-556 | 0.882 (1.427) |
| generic scaffold grouped | 0.603 (0.603), 5 of 30 folds lack a class, test sizes 9-646 | 0.908 |
| scaffold grouped, scaffolds >= 60 rows and acyclic left IID | 0.737 +- 0.035 (0.696) | 0.756 (1.004) |
| same, >= 20 rows left IID | 0.746 +- 0.026 (0.701) | 0.740 (0.978) |
| only benzene and acyclic left IID (biphenyl grouped) | 0.668 (0.651) | 0.817 |
| authors' Train/Test (581 / 195), one split | 0.716 (0.740) | 0.764 (1.033) |

Within the shipped splits (9 folds), RF scores 0.779 on ring test rows whose scaffold is in train (1,511) and 0.655 on
those with a new scaffold (505); by nearest-neighbour similarity 0.654 (< 0.4), 0.734 (0.4-0.6), 0.817 (0.6-0.85),
0.937 (>= 0.85, 188 rows).

Reading (EV-3, SPLIT-4): the full scaffold split is not a usable alternative. A third of the rows is one benzene group,
so folds range from 30 to 556 test rows, some lack a class, and the RF falls to the dummy's log loss. Most of the drop
comes from holding out whole chemotypes that new chemicals keep having: benzene derivatives, and the biphenyls
(PCBs), which hold 17 of the 64 class-2 chemicals (27% of the class in 8% of the rows). A new chemical under assessment
very likely sits in a family already measured, so the family is a feature-like property (SPLIT-4, "new rows keep
having the value"), not an entity new data would lack (SPLIT-29). Leaving the large families IID and grouping the rare
ones costs 0.016-0.025 AUC with the model ranking unchanged (RF > LR in every variant). So IID matches the framing; it
is optimistic for structurally novel chemicals (SPLIT-31).

**Problems, ranked (principles.md)**

1. **P4, SPLIT-1 / SPLIT-4 / SPLIT-31 (Should, note): IID optimistic for novel chemotypes; the split text is inaccurate.**
   Evidence above (0.762 IID; 0.737-0.746 with rare scaffolds grouped; 0.655 on test rows with a new scaffold).
   `task_summary.split` and curation_comments say "the file has no chemical families for a stricter split" / "holds no
   key of chemical families"; the file has the SMILES, from which Murcko scaffolds are exact. Precedent
   qsar_oral_toxicity (same kind of task) keeps IID and states the scaffold drop as an applicability-domain note. Like
   cases alike: mildest remedy is a note, no re-split. Reword the split line (e.g. "Random chemicals, one row each, as in
   the source's random split; a new chemical mostly belongs to a family already measured") and add a curation_comments
   note with the numbers above. Optionally list it as a candidate for a grouped (scaffold) variant (SPLIT-31).

2. **P4, LEAK-13 to LEAK-15 (descriptor selection on labelled rows), weak, already noted.** 581 of 776 shipped
   chemicals (the authors' Train set, 73-77% of each test fold) chose the 9 Dragon descriptors. The authors' own split
   would be selection-clean, but it is one 195-row fold and RF scores 0.716 there vs 0.762 on CV (LR 0.740 vs 0.719, the
   other way), which matches the existing note's small, uncertain effect (RF +0.064, p = 0.06; LR +0.003). The 9 are
   9 of 202 features. A re-split to the authors' test set would trade a weak leak for one noisy fold; keep the note
   (as decided, home_credit_default_risk precedent). No change.

3. **P6, TP-5 (fine).** Smallest class (additional storage sites, 64 rows) has 21-22 rows in every test fold of the
   shipped split; scorable. Note that a scaffold split would not be (folds without class 2), another reason not to
   switch.

Rules that hold: SPLIT-1 (with note), SPLIT-2 (IID), SPLIT-3, SPLIT-5 (the source's random split checked against the
task and data: right), SPLIT-24 (no similarity cluster used), SPLIT-29 (no recurring entity), SPLIT-30 (no probe hit),
USE-10 / USE-11 (new chemical, one row each). Temporal and grouped checks: not applicable (no time column, no group
column, `splits_comment` absent, which is fine for IID).

</details>

<details><summary>Domain practitioner</summary>

Actor: a chemical assessor at a registrant or an agency doing the B (bioaccumulation) part of a PBT assessment
(REACH Annex XIII, ECHA guidance R.11). The tiers are: logKOW screen (>= 4.5 triggers B/vB), then (Q)SAR BCF
estimates, then the OECD 305 fish test. The mechanism class is the authors' tool for one step of that chain. It says
whether the KOW-based BCF estimate (the TGD equation) holds (class 1), underestimates the BCF (class 2, additional
storage sites) or overestimates it (class 3, metabolised or eliminated). Grisoni et al., Environ. Res. 148 (2016) use
the scheme to pick the BCF model for each class (three VEGA models and one KOW equation).

**Fit**

**Approximate as shipped, direct once the logKOW is added.** The decision is real and the structure is known before
a fish test. But the class says whether the KOW-based estimate can be trusted, and the logKOW that estimate uses is
an input the assessor always has at this point. The dataset drops it (USE-6, USE-8). The task_summary says `direct`.
I would keep `direct` only if the logKOW goes in.

**In the first person**

1. **Inputs at the prediction point.** I have the structure, so the 9 Dragon descriptors and RDKit's 2D descriptors
   are fine (USE-3). The **logKOW** is what I would always have and the dataset lacks. Under REACH it is an Annex VII
   requirement from 1 t/y and the first tier of the B screen, so I measure it, or take a curated value, long before
   anyone pays for an OECD 305 test. The class is defined against it: the residual of the measured logBCF from the TGD
   line at the chemical's logKOW (Env. Int. SI Sec. 1: "KOW values were fundamental for class determination"). MLOGP
   is only a calculated stand-in (r = 0.88 with the curated logKOW). Adding the logKOW is no leak. The class still
   needs logBCF, which stays unknown, and logKOW alone gives macro AUC 0.659. What I would not have is logBCF, and it
   is correctly dropped. CAS and Set are rightly dropped too.
2. **Target.** In the end I act on whether the chemical is B or vB (BCF > 2000 / 5000, which is 18% / 12% of these
   chemicals), or on a BCF number. The mechanism class is an intermediate. It tells me which BCF model to trust, and a
   high P(class 2) on a chemical with logKOW < 4.5 is the red flag that the logKOW screen would miss a B chemical.
   For the use case as written ("decide whether the usual estimate ... can be trusted") the class is what I act on, so
   USE-5 is met for that decision. I would want **probabilities**, above all P(class 2). Log loss suits that, and macro
   weighting helps the 8% class. Below logKOW 1 the label is mostly a convention (42 of 52 put in class 1, by the
   2015 table's logKOW). Those chemicals are never B, so these rows matter little to me.
3. **Rows and test data.** One row is one chemical with one curated BCF, which matches one assessment. A random IID
   split stands for "a chemical from the same chemical space as the historical BCF compilation": pesticides, PCBs,
   dioxins, PAHs, nitro-aromatics. The real stream is new REACH industrial substances, often outside that space. The
   leak probe shows 1-NN accuracy of 0.808 on the closest tenth vs 0.649 overall, so the task rewards close analogs
   (congener series). Read-across is standard practice, so I accept random chemicals (USE-10, USE-11: a new entity,
   one row each). A test on unseen chemical families would be harder and closer to the worst case. The source has
   no family key.
4. **Would I use it.** As a screening aid next to VEGA / EPI Suite BCFBAF, yes, if it outputs calibrated
   probabilities and an applicability-domain flag. The authors ship bounding boxes for the descriptors (Env. Int. SI
   Sec. 3). Macro AUC ~0.76 and a log-loss skill of +0.18 over the prior (task probe, random forest) are modest. I
   would not use it to replace a fish test. Two things would make me distrust it. It is not told my measured logKOW,
   which defines the class. And the labels for 124 chemicals rest on a *predicted* logKOW (2015 table `KOWtype` =
   pred), so for those the class is partly a model artefact.

**Gaps, ranked by how much they change the task**

1. **The logKOW is missing as an input (USE-6; USE-8 fit).** The assessor always has it and the class is read
   against it. Probe (RF with 500 trees, stratified 3-fold x 5, 776 rows, curated logKOW
   from the 2015 table):

   | features | macro AUC | log loss | class 2 vs rest AUC |
   |---|---|---|---|
   | 9 descriptors | 0.750 | 0.744 | 0.762 |
   | 9 descriptors + logKOW | 0.768 | 0.726 | 0.797 |
   | logKOW only | 0.659 | 1.536 | 0.708 |

   The gain is modest overall and clear on the class that drives the decision (class 2). The 2015 table holds the
   logKOW for every shipped row (652 experimental, 124 predicted). Caveat: the Env. Int. set added experimental KOWs
   from Mansouri, so its own logKOW may differ from the 2015 table for some rows. The rule reproduces 600 of 607 with
   these values, so they are close.
2. **The target is an intermediate of the real decision (USE-5).** The B/vB call or the BCF value is what I finally
   act on. The class is the right target for the stated use case (choosing or trusting the BCF model). The sibling
   framing, logBCF regression (REVIEW_before issue 1), is closer to the final decision. Shipping both would cover both
   uses. This is not a defect, but it is the honest reason the use case reads "for example".
3. **The test chemicals are random chemicals from a historical compilation (USE-10, USE-8).** They are not new
   chemical families. The scores are optimistic compared with novel industrial substances. It is acceptable because
   read-across is how assessors work, but `fit_reason` should say that the test stands for chemicals like the
   compiled ones.
4. **Labels resting on predicted logKOW or on the sub-1 convention.** 124 rows use a predicted logKOW and the
   logKOW < 1 rows mostly fall into class 1 by convention. This is label noise relative to the mechanism, not a
   decision gap. Minor.
5. **The authors chose the descriptors on 75% of the labelled rows** (LEAK-13 to LEAK-15, noted in
   curation_comments). From the practitioner's view it is negligible: RDKit's 193 descriptors carry the task as well.

**What a domain expert would change**

- Add the logKOW the class was computed from (the curated value of the 2015 table / Env. Int. set) as a feature,
  `logKOW` or similar. Document it as known at the prediction point (USE-6), and keep MLOGP and RDKit's MolLogP next
  to it. Then set fit to direct. Optionally add a flag for experimental vs predicted logKOW, which an assessor also
  knows.
- In `use_case`, name the downstream decision. The class picks the BCF model or flags a likely underestimate
  (class 2) before the B/vB call. Cite Grisoni et al. 2016 Environ. Res. 148:507-512 as the source of that use.
- In `fit_reason`, say the test chemicals are random members of the historical BCF compilation, not new chemical
  families.
- Optionally offer logBCF regression as a sibling (`_reg`) for the B/vB decision itself (REVIEW_before issue 1).

**Rules cited**

USE-1 (actor, moment, decision: present), USE-3 (prediction point: correct for logBCF), USE-5 (target: class is
right for the stated decision, an intermediate for the final one), USE-6 (logKOW known at prediction time and missing),
USE-8 (fit: approximate as shipped), USE-9 (not needed: the gap is fixable, not rephrasable), USE-10 / USE-11 (new
chemical, one row each, IID acceptable), USE-12 (n/a).

**Sources**

- The definition (task_summary, curation_comments); the Env. Int. 2016 SI (KOW fundamental for the class;
  descriptor bounding boxes); the 2015 table's logKOW per row (KOWtype exp/pred); the archived old UCI page; the task
  probe and the checklist
- Grisoni et al. 2016, Environ. Res. 148:507-512, integrated BCF model per class (abstract via
  https://www.boa.unimib.it/handle/10281/102780 and https://boa.unimib.it/handle/10281/116951)
- https://michem.unimib.it/download/data/mechanisms-of-bioconcentration (503 on fetch; search snippet only)
- ECHA R.11 / REACH B screening tiers, logKOW >= 4.5 trigger:
  https://www.umweltbundesamt.de/system/files/medien/2674/dokumente/information_requirements_r11_0.pdf,
  https://rivm.nl/sites/default/files/2018-11/02%20Traas.pdf

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** It is a real, curated QSAR task with modest but real signal. The changes: check or document how the 776 rows were derived from the 779, and clean up the computed RDKit block. Also consider a scaffold or grouped split if the benchmark wants to measure generalization to new chemistry.

**The task**
Grisoni et al. (2016, Environ. Int.) give fish bioconcentration factors (BCF) for 779 chemicals, curated by hand. Each chemical has one of three mechanistic classes: (1) mainly stored in lipid tissue, (2) additional storage sites such as proteins, (3) metabolized or eliminated. Regulators and risk assessors (for example under REACH) would use this to screen untested chemicals from structure alone. The target has a real use. All features come from the structure, so all are known at prediction time. logBCF, the source of the class, is correctly excluded.

**Concerns, most serious first**

1. **Weak signal, small rare class.** Classes are 458 / 254 / 64. 3-fold CV (3 repeats) log-loss:

   | Model | Log-loss | AUC-OVR | Accuracy | Balanced accuracy |
   |---|---|---|---|---|
   | Prior (dummy) | 0.883 | | | |
   | Logistic regression, 9 original descriptors | 0.806 | | | |
   | Random forest, 9 original descriptors | 0.744 | 0.748 | | |
   | Regularized LightGBM, all features | 0.719 | 0.756 | 0.696 | 0.56 |

   Default-ish LightGBM overfits (log-loss about 1.03, worse than the prior). With about 21 class-2 rows per test fold, scores will be noisy. The task still discriminates between methods, and that sensitivity to regularization is itself informative. Keep it, but expect high variance; 10x3 repeats is appropriate.

2. **The added RDKit block (193 columns) was not part of the source.** The UCI file has 9 descriptors plus CAS, SMILES, Set, Class and logBCF. The RDKit features come from SMILES, so they cause no leakage. They help only a little (log-loss 0.744 to 0.719 for RF). Problems:
   - 7 rows (about 1%; organometallic or charged structures) have NaN in the 12 partial-charge and BCUT2D columns.
   - `rdkit_Ipc` reaches 7.7e9, an extreme scale. Log-transform it or drop it.
   - Many `fr_*` columns are near-constant counts.

   Document the RDKit version. Either keep these columns as a deliberate, documented augmentation or provide the 9-descriptor version as the canonical one.

3. **Row count is 776, not 779.** The 3 dropped rows are unexplained. They may be SMILES parse failures or deduplication. Document the reason.

4. **Near-duplicates and isomers.** 61 rows share identical values on the 9 original descriptors (28 groups). Their RDKit features differ, and the matching molecular weights suggest positional isomers. 6 of these groups have conflicting labels. A random IID split puts close analogues on both sides of train and test, so it overstates generalization to new chemistry. The source had its own Train/Test split (the `Set` column). A scaffold or grouped split would be more honest, but IID is acceptable for a tabular benchmark.

5. **Minor preparation points.**
   - Count descriptors are stored as int or float inconsistently. `nHM` is int; the RDKit counts are float.
   - `B02(C-N)` is binary.
   - Column names contain parentheses and hyphens. This is harmless.
   - There are no exact duplicate rows across all features.

**What I could not check**
- The raw UCI CSV and SMILES. I could not see which 3 rows were dropped, whether the RDKit features match the SMILES, or whether the class labels match the source exactly. The counts (458/254/64) are plausible for the paper's distribution.
- The original paper's class counts and its selection of the 9 descriptors. Those descriptors may have been chosen using the full data, which would mean mild selection optimism.
- I did not open any files outside the clean room.

Sources: https://doi.org/10.24432/C56S46 , https://archive.ics.uci.edu/dataset/510/qsar+bioconcentration+classes+dataset

</details>

<details><summary>Precedent check</summary>

Checked against principles.md ("Consistent judgement", "Exceptions and amendments", "Tensions"),
leak_checks.md (LEAK-4, LEAK-10, LEAK-31), use_case.md (USE-5, USE-8, USE-9), provenance.md (PROV-13, PROV-15),
cleaning_features.md (CLEAN-24), evidence.md (EV-4), the register, the sibling definitions and records, the
2026-10-07 run report and today's qsar_oral_toxicity panel.

Register: none of the four cross-dataset flags (3 opposite_outcomes, 1 drift) involves this dataset. Its decisions
carry no rule IDs in the register (all `rule_ids: []`) except the CLEAN-24 case row, so the comparison below is by
mechanism, read from the texts. Curator decisions on this dataset: one, CC (2026-10-14, Lennart) "drop the SMILES,
add RDKit's 2D descriptors next to the 9 Dragon descriptors". Everything else (target, repair, drops, split, fit
label, the LEAK-31 note, REVIEW issues) is an AI decision or draft. The task summary (and so `fit`) was not on
Lennart's task-summaries page of 2026-10-14 (excluded from that page).

**Summary**

| # | Decision | Verdict | Closest precedents |
|---|---|---|---|
| 1 | Target = the source's 3-class mechanism; logBCF dropped (REVIEW issue 1) | consistent | qsar_oral_toxicity (ships the source's VT class over the LD50 behind it, 2026-10-07 / panel 2026-10-20); sdss_17 `redshift` (LEAK-10 case, CC Lennart 2026-10-01); mutual_funds_india `rating` (LEAK-10); PROV-6/7 tension row allows a `_reg` sibling |
| 2 | Swapped pairs repaired from the 2015 table (REVIEW issue 2) | consistent; the listed alternative (drop the six) would break PROV-13 (Must) | SUPPORT2, ashrae (PROV-13 cases); tension "Repair against cleaning around damage" |
| 3 | Three wrong-structure rows dropped | consistent (stated fact: the origin has the same wrong SMILES, Dragon values cannot be recomputed) | PROV-13 "when the origin cannot be reached, keep with a note or retire"; drug_induced_autoimmunity_prediction (streptomycin rows dropped, 2026-10-14) |
| 4 | SMILES dropped, RDKit 2D added next to the 9 Dragon descriptors | consistent: follows the curator's own CC and CLEAN-24 | CC Lennart 2026-10-14 (apistox issue 1; CHANGELOG 2026-10-14); apistox, drug_induced_autoimmunity_prediction (CLEAN-24 cases) |
| 5 | Authors' supervised descriptor selection kept with a note "as home_credit_default_risk" (REVIEW issue 5) | **departs from LEAK-31 ("remove it when we can") and cites a precedent that was decided the other way; a distinguishing fact exists but is not written down** | home_credit_default_risk (CC Lennart 2026-10-01 keep, superseded by CC Lennart 2026-10-19: selection not applied; LEAK-31 case); qsar_fish_toxicity, qsar_aquatic_toxicity (source-only selected descriptors, kept with notes) |
| 6 | `fit = "direct"` with a named gap (selection on test-fold chemicals) | **departs without a stated reason**: USE-8 lists "a potential leak kept on purpose" as approximate; the sibling with the same mechanism is approximate; the same-day oral toxicity question applies too | qsar_aquatic_toxicity (approximate, same mechanism); kick (approximate, USE-8 case); qsar_fish_toxicity (direct, same mechanism, gap not in fit_reason); qsar_oral_toxicity REVIEW issue 6 (open, 2026-10-20) |
| 7 | IID split, "the file has no chemical families for a stricter split" | consistent in substance; the stated reason is the one refuted for qsar_oral_toxicity today | qsar_oral_toxicity mediator change 4 (2026-10-20); qsar_tid_11, qsar_biodeg, hiva_agnostic (IID); SPLIT-24 (emscad), SPLIT-31 candidates |
| 8 | No accepted warnings | consistent (the SMILES `dataset_identifier_column` acceptance went with the SMILES, as for apistox, CHANGELOG 2026-10-14) | apistox |
| 9 | REVIEW issue 7: pretraining overlap raised for the curator; TabSTAR's label swap noted in curation_comments | **issue 7 departs from PROV-15 (Must) and EV-4 (Lennart 2026-10-12, 2026-10-15)**; the note itself is consistent (a problem of that copy, as nba_players_2016_2019) | EV-4 / PROV-15 case rows; nba_players_2016_2019 note; no other REVIEW.md in the working copy still raises pretraining |
| 10 | REVIEW issue 6, domain "chemistry & material science" | no rule decides it; no prompt | qsar_oral_toxicity precedents.md section 5 (same table) |
| 11 | Record metadata: tag `Free Text (Short)`; 2026-10-20 assessment "no known risk" | metadata drift, not a curation decision; fix as for the siblings | apistox, drug_induced_autoimmunity_prediction (no text tag after the SMILES drop); qsar_oral_toxicity mediator change 8 ("no known risk" replaced) |
| 12 | REVIEW issue 4 (class thresholds inferred, paper unread) | evidence question (EV), not a decision; nothing to compare | - |

No drift by the curator on this dataset (one CC). The curator's LEAK-31 change on home_credit (keep 2026-10-01, remove
2026-10-19) is a deliberate rule change written into LEAK-31 the same day, not drift; this dataset's note still cites
the older half. No third exception of one kind: the sibling keep-with-note cases under LEAK-31 (fish, aquatic) are
inside the rule's own "keep with a note when small" branch, not exceptions. One maintenance gap: the LEAK-31 Cases
table lists only home_credit; qsar_fish_toxicity, qsar_aquatic_toxicity and this dataset are unlisted keep cases.

**1. Target: the class, logBCF dropped (REVIEW issue 1)**

Consistent. USE-5 (Must): the source built the label from the measured logBCF and the experimental logKOW (Env. Int.
SI Sec. 1, quoted in the 2026-10-07 fix round); the class is what the paper models and what UCI names the dataset by.
LEAK-4 (Must) asks a tree on the defining columns: done as the decision table (with MLOGP in place of the absent
experimental logKOW the band gives 471 of 776), so no feature completes the rule. Dropping logBCF follows LEAK-10's
"fitted from the same measurement that gives the label" (sdss_17 `redshift`) and the snapshot case (mutual_funds_india
`rating`). Same choice as qsar_oral_toxicity, which ships the source's very toxic class over the LD50 behind it. The
regression would be a distinct task on a shared source, which the tension row "Uniqueness against a distinct task"
(PROV-6, PROV-7) allows as a `_reg` folder. The choice between them is a weighing call (no rule makes one wrong); no
prompt.

**2. Swapped pairs repaired (REVIEW issue 2)**

Consistent with PROV-13 (Must) and the tension "Repair against cleaning around damage (P5 over P7)": the origin (the
authors' 2015 table, Chemosphere SI) has the right SMILES with the same logBCF, and the class follows the rule with
each chemical's own logKOW. Precedents: SUPPORT2 (rows of the wrong patient restored from the study data), ashrae.
The repair moves the 9 Dragon values with the SMILES, which the fix round verified (nHM, B02, F04 recomputed with
RDKit match all 779 rows), so it reconstructs the release rather than inventing values; PROV-14 (a rebuild that does
not match the release is a new dataset) is not triggered, as for SUPPORT2.

The listed alternative, "drop the six rows as in the first round", would clean around damage the origin can repair:
a departure from a Must (PROV-13) with nothing ranked above it. It is not a reasonable exception under the ranking.
The issue can close as settled by rule; the drop was the AI's own first-round choice (2026-10-07 run report), not a
curator decision, so there is no drift.

**3. Three wrong-structure rows dropped**

Consistent. The stated fact sets these apart from the pairs: the 2015 table carries the same wrong SMILES, and the 9
Dragon values cannot be recomputed without Dragon, so the origin cannot repair them (PROV-13: "when the origin cannot
be reached, keep with a note or retire"; at row level, dropping three of 779 is the definition fix of the remedy
ladder). Comparable row drops for a wrong or ambiguous entity: drug_induced_autoimmunity_prediction (both
streptomycin rows, 2026-10-14). No prompt.

**4. SMILES dropped, RDKit descriptors added**

Consistent with the curator's own CC (2026-10-14, Lennart) and CLEAN-24 (Should): "descriptors the source ships stay
next to them", and "check for rows that become copies once the stereochemistry is gone" (done: 776 distinct vectors
with RDKit, 61 sharing among the 9 alone). Follows apistox (RDKit from the shared helper) and drug_induced (source
RDKit kept). No prompt.

**5. The authors' supervised descriptor selection, kept with a note (REVIEW issue 5)**

The rule. LEAK-31 (Should, Part 3, narrows LEAK-6 and LEAK-28): "Supervised feature selection on the full labelled
set: measure it; keep with a note when small, remove it when we can. Cases: home_credit_default_risk (2026-10-19)."

The decision. Measured (RF +0.064 macro AUC on the authors' training chemicals, p = 0.06; logistic +0.003, p = 0.48;
fix round: the 9 selected descriptors 0.752 against 217 unselected RDKit descriptors 0.758, both 0.763), kept with a
note "as home_credit_default_risk".

The cited precedent was decided the other way. home_credit_default_risk: CC (2026-10-01, Lennart) kept the kernel's
importance-based selection ("selecting inside folds or not selecting at all gives the same AUC"); CC (2026-10-19,
Lennart) removed it ("the kernel's importance-based column selection not applied (every column stays)"), with a
measured effect of zero, and that removal is the LEAK-31 case. So "as home_credit" now points at a removal.

Can it be removed here? Yes, since 2026-10-14: with RDKit's 193 descriptors in the frame, dropping the 9 Dragon
descriptors removes the selection and keeps an unselected description of the structure (RF 0.758 against 0.763 with
both). That is the "remove it when we can" branch. The siblings that keep a source selection could not remove it:
qsar_fish_toxicity (six GA-selected descriptors on the paper's training set; "a mild optimism we cannot measure";
UCI file holds no structure) and qsar_aquatic_toxicity (eight kNN-selected descriptors, kept with a note and
`approximate`). Neither has a SMILES to rebuild from.

What may set this case apart (not written down): (i) unlike home_credit, where the selection was a step of our own
definition copied from a kernel (closer to LEAK-29, "our own cleaning"), here the source published only the selected
descriptors, and CLEAN-24 (Should, P7) says the source's descriptors stay next to RDKit's; (ii) the effect may count
as small (no gap for the linear model, RF p = 0.06, and the selected 9 score no better than 217 unselected
descriptors). The conflict between CLEAN-24 (P7, keep the source's descriptors) and LEAK-31 (P4, remove when we can)
is not in the Tensions table; by rank LEAK-31 wins unless the effect is judged small, which LEAK-31 itself allows.

There is also an older curator decision in play: the CC of 2026-10-14 asked for RDKit "next to the 9 Dragon
descriptors", five days before LEAK-31 was written (2026-10-19). Under "a newer decision of the curator beats an older
one", the newer rule is the default unless the curator confirms the keep.

Verdict: departs from LEAK-31's "remove when we can" and from its only case, with a plausible distinguishing fact that
is not recorded. Reasonable as an exception (Should, serving P5: the data as the source published it), not a Must
breach.

**Consistency check (AI, 2026-10-20):** qsar_bioconcentration keeps the 9 descriptors the authors selected on 584
labelled chemicals that sit in our test folds (kept with a note "as home_credit_default_risk"), while
home_credit_default_risk had its importance-based selection removed (CC 2026-10-19, Lennart; the LEAK-31 case) even
at zero measured effect, and here the selection can be removed since the RDKit descriptors are in (RF 0.758 without
the 9, 0.763 with). What sets qsar_bioconcentration apart?
(a) the AI's best guess: the selection is the source's published feature set, not a step of our own definition (which
home_credit's was), CLEAN-24 keeps a source's descriptors next to RDKit's (CC 2026-10-14), and the effect is small
(logistic +0.003, the 9 score like 217 unselected descriptors), recorded as `Exception to LEAK-31` with the citation to
home_credit replaced by qsar_fish_toxicity / qsar_aquatic_toxicity; (b) treat it like home_credit: drop the 9 Dragon
descriptors and ship RDKit's 193 only; (c) reopen home_credit_default_risk to keep its selection; (d) change LEAK-31
(an amendment: "a selection the source published stays with a note when small; one we apply ourselves is removed"),
and add the CLEAN-24 / LEAK-31 tension row.

**6. Fit label `direct`**

USE-8 (Must) lists "a potential leak kept on purpose" among the approximate cases (kick). This definition keeps a
potential leak on purpose (decision 5) and names it in `fit_reason` ("may favour those slightly"), yet sets `direct`,
whose definition is that rows, features, label timing and split mirror the use case. Siblings with the same mechanism
(the authors' supervised selection on chemicals in our test folds):

| dataset | fit | selection in fit_reason | reviewed by Lennart |
|---|---|---|---|
| qsar_aquatic_toxicity | approximate | yes ("may carry information on the test chemicals into the features") | task-summaries page 2026-10-14 (processed) |
| qsar_fish_toxicity | direct | no (in curation_comments only) | task-summaries page 2026-10-14 (processed) |
| qsar_bioconcentration | direct | yes | no (excluded from that page) |

So the two siblings the curator saw are themselves split, and this dataset sits with fish on the label but with
aquatic on the reasoning. If decision 5 ends with the 9 dropped (option b), the gap goes and `direct` stands on this
ground. Separately, qsar_oral_toxicity's REVIEW issue 6 (open today: random test chemicals of the tested set against
the untested chemicals the actor screens; mediator recommends `approximate`) applies word for word to this use case
("an untested organic chemical"), and to qsar_biodeg and qsar_fish_toxicity. Whatever the curator answers there should
be applied here in the same pass.

**Consistency check (AI, 2026-10-20):** qsar_bioconcentration is `direct` while it keeps a potential leak on purpose
(the authors' descriptor selection, named in its own `fit_reason`), which USE-8 lists as approximate (kick), and
qsar_aquatic_toxicity is `approximate` for the same mechanism. What sets qsar_bioconcentration apart?
(a) the AI's best guess: the measured effect is small (logistic +0.003, the 9 score like 217 unselected
descriptors), so the gap is a note rather than a stand-in, recorded as an exception to USE-8's list (and the same
then holds for qsar_fish_toxicity); (b) treat it like qsar_aquatic_toxicity: `approximate`; (c) reopen
qsar_aquatic_toxicity to `direct`; (d) change USE-8 (an amendment saying when a kept potential leak is small enough
for `direct`). Answer together with qsar_oral_toxicity's issue 6, which raises the screening-set gap for every QSAR
sibling.

**7. IID split**

Consistent in substance with every molecule sibling (qsar_tid_11, qsar_biodeg, qsar_fish_toxicity,
qsar_aquatic_toxicity, hiva_agnostic, bioresponse, qsar_oral_toxicity; see the qsar_oral_toxicity panel's precedent
check, section 2), with SPLIT-24 (a similarity cluster or feature hash is not a group key: emscad, maternal_health_risk) and
with the near-copy probe (gap -0.000, no hits). One row per chemical (0 duplicate CAS, SMILES or InChIKey), so SPLIT-29
and LEAK-17 are not triggered.

The stated reason departs from today's precedent, though. `task_summary.split` and the Split bullet rest IID on "the
file has no chemical families for a stricter split". For qsar_oral_toxicity the mediator (change 4, 2026-10-20)
struck the parallel claim and asked that IID rest on the use case (a new chemical each time), SPLIT-29 and SPLIT-24,
with a scaffold-grouped variant listed as a SPLIT-31 candidate. This file has the SMILES, so scaffolds can be computed
directly. Text alignment, not a decision change; no prompt (the outcome is the same).

**9. REVIEW issue 7, pretraining overlap**

PROV-15 (Must): "Raise it as an issue only when it changes one of our decisions. Another collection's version of the
data, pretraining overlap and other benchmarks' scores never do"; EV-4 cases (Lennart, 2026-10-12: pretraining changes
no decision; 2026-10-15: TabSTAR's labels are no reference). Issue 7 ("your call, no change") was drafted on
2026-10-07, before those decisions, and was carried over; it is the only REVIEW.md in the working copy that still
raises pretraining. It should leave the issue list (an AI draft, not a curator decision, so no prompt). The
curation_comments note that TabSTAR's annotation swaps classes 2 and 3 is allowed by PROV-15 as "a problem of that
copy" (as nba_players_2016_2019's TabSTAR note), though PROV-15 puts such a note in the record; the 2026-10-07 draft of
issue 7 also named a company repository, already removed from the current REVIEW.md.

**10-11. Domain and record metadata**

Domain: no rule; the value matches qsar_oral_toxicity, qsar_tid_11, hiva_agnostic and clock_protein_toxicity, while
qsar_fish_toxicity, qsar_aquatic_toxicity, qsar_biodeg, bioresponse and apistox say "biology & life sciences" (REVIEW
issue 6 lists them correctly). A convention call for the curator, not a consistency departure.

Record: the tag `Free Text (Short)` described the SMILES, dropped on 2026-10-14; apistox and
drug_induced_autoimmunity_prediction carry no text tag after the same change. The 2026-10-20 assessment says "no known
risk" while REVIEW issues 4 and 5 are open; the qsar_oral_toxicity mediator (change 8) replaced the same phrase
today. Both are record fixes, no prompt.

**Prompts for the curator (one per decision)**

1. Decision 5 (LEAK-31, keep the authors' selected descriptors), prompt in section 5.
2. Decision 6 (USE-8, `direct` with a kept potential leak), prompt in section 6; to be answered with
   qsar_oral_toxicity's issue 6.

Everything else follows a rule and a precedent, or is an AI draft that the rules settle (issue 2's alternative breaks
PROV-13; issue 7 is barred by PROV-15).

</details>

<details><summary>Advocate</summary>

Position: ship as defined, with text fixes. No phase A finding is a Must failure that the definition doesn't
already handle. Every real problem has a remedy at the "fix the text" or "keep with a note" step of the remedy ladder.

**1. The target and the inputs are valid: no leak, the rule cannot be completed (P3/P4, USE-5 Must, LEAK-4/LEAK-10 Must)**

- Evidence: the class is the source's published target. Its rule (a +-0.5 band around the TGD line on logBCF and the
  experimental logKOW) reproduces 600 of 607 classes (claim audit: 599 of 606). The labels match the archived old UCI
  page (Wayback 2023-03-27), and the class 2 residual is +0.79 above the line.
- logBCF is dropped. With MLOGP standing in for the experimental logKOW, the band gives the class for only 471 of 776
  chemicals. The best single feature reaches 0.670 AUC, and no feature drop moves the score (leak probe).
- Every feature is a function of the structure. The column audit recomputed B02(C-N), F04(C-O) and nHM from the
  repaired SMILES and they match on 776/776 rows.
- Copies across the split: 0 exact, 0 InChIKey, 0 connectivity block.
- The claim audit's "held under attack" list covers all of this. This is the validity core, and it is intact.

**2. The data is repaired from its origin (P5, PROV-13 Must)**

- The three swapped pairs (benzene/cyclohexane, naphthalene/tetralin, chlorobenzene/chlorocyclohexane) are confirmed
  three ways: by PubChem, by PCD becoming > 0 on the aromatic rows after the repair, and by the 2015 table carrying the
  file's logBCF on the CAS chemical.
- The three wrong-structure rows have no origin to repair them from, so dropping them follows PROV-13's own fallback.
- A random 60-row PubChem sample: 59 match, 1 has no PubChem hit.
- Precedents: SUPPORT2, ashrae, drug_induced_autoimmunity_prediction. The alternative of dropping the six repaired
  rows (REVIEW issue 2) would break PROV-13 and should be closed as settled.
- The blind reviewer's worry ("776, not 779, unexplained") is already answered in curation_comments and Decision 2.

**3. IID is the right split; I concede the split text, not the regime (P4, SPLIT-4 Must, USE-10/11 Must, SPLIT-31 Should)**

- Concede: "the file has no chemical families" is false.
  - Murcko scaffolds are exact from the SMILES. 34% of rows sit in 42 congener series.
  - Holding the series out costs the RF about 0.10 macro AUC (claim audit 0.754 -> 0.650; split audit 0.762 -> 0.611).
- Why the regime stays:
  - SPLIT-4 Must: "If new rows keep having the value, the column is a feature and the split stays." A new chemical
    under assessment keeps being a benzene derivative, a PCB or a PAH, and read-across is standard practice
    (practitioner accepts IID).
  - The gap never decides (SPLIT-4, SPLIT-30, Tension "right split against the score").
  - The full scaffold split is not scorable. Benzene alone is 262 rows, test folds range from 30 to 556 rows, and 3 of
    30 folds lack a class (TP-5).
  - Grouping only the rare scaffolds costs 0.016-0.025 AUC and leaves the model ranking unchanged.
- Remedy (mildest, as the qsar_oral_toxicity mediator decided today, change 4):
  - Reword task_summary.split and the Split bullet, resting IID on the use case and SPLIT-29.
  - Add the measured scaffold gap as a note.
  - List the dataset as a SPLIT-31 candidate for a grouped variant.

**4. The descriptor selection is small, so LEAK-31 says keep with a note (P4, LEAK-31 Should; CLEAN-24 Should)**

- The gap the note attributes to the authors' selection is mostly not selection. On the authors' Train-vs-Test
  chemicals, the RF on the 193 unselected RDKit columns alone shows +0.054 (p = 0.09), against +0.069 on the 9
  selected descriptors.
  - So at most about 0.015 AUC can come from the selection (claim audit).
  - Logistic regression shows +0.006 (p = 0.45).
- LEAK-31 reads "keep with a note when small". This is its own branch, not an exception.
- What sets this case apart from home_credit: the selection is the source's published feature set, not a step of our
  own definition. CLEAN-24 keeps the source's descriptors next to RDKit's, and the curator's own CC (2026-10-14) asked
  for exactly that.
- Concede two points:
  - The citation "as home_credit_default_risk" is stale; that case was reversed on 2026-10-19.
  - The note overstates the effect.
- Remedy: cite qsar_fish_toxicity / qsar_aquatic_toxicity instead, word the note `Potential leak, kept on purpose:`
  with the RDKit-only control, and soften fit_reason.
- If the curator prefers option (b), dropping the 9 costs about 0.005 AUC (0.758 vs 0.763) and the dataset still ships.

**5. The fit label and the logKOW are text or one-column calls, not reasons to hold the dataset (P3, USE-8 Must, USE-6 Must)**

- Fit label:
  - Once point 4 shows the selection effect is at most about 0.015 AUC, `direct` is defensible.
  - If the curator follows qsar_aquatic_toxicity, the fix is one word (`approximate`). It should be answered in the
    same pass as qsar_oral_toxicity's issue 6.
- The logKOW (practitioner):
  - It is real that an assessor usually has it, and USE-6 makes it a legitimate input. But USE-6 says what *may* go
    in; it does not say the task fails without it.
  - The stated use case is an "untested chemical from its structure". 124 rows have only a predicted logKOW in the
    2015 table.
  - On the shipped features, adding it moves the RF from 0.762 to 0.762 (experimental) or 0.764 (any) (claim audit).
    The practitioner's +0.018 is on the 9 descriptors alone. So "the task changes without it" (USE-6's "Why") does not
    hold here on the measured data (EV-2).
- Remedy: one sentence saying why the logKOW is not an input, or add it as a column. Both keep the dataset.

**6. It is worth benchmarking (P6, TP-2, TP-5)**

- Task probe on the 30 shipped splits:

  | model | macro AUC | log loss |
  |---|---|---|
  | dummy (class prior) | n/a | 0.883 |
  | random forest | 0.762 +- 0.023 | 0.725 (skill +0.18) |
  | linear | 0.698 | n/a |
  | default LightGBM | 0.759 | 1.42 (overfits) |

- The smallest class has 21-22 rows in every test fold, so every fold is scorable.
- The blind reviewer independently says "include with changes": "the task still discriminates between methods, and
  that sensitivity to regularization is itself informative".
- This is a small, real, regularization-sensitive multiclass QSAR task, a gap in the collection (record priority 3).

**7. The rest is housekeeping (procedure and records; PROV-15 Must, EV-4)**

- Drop REVIEW issue 7 (pretraining overlap). PROV-15 and EV-4 bar it, and it is the only REVIEW.md left that raises it.
- Remove the stale record tag `Free Text (Short)`.
- Replace "no known risk" in the record.
- Fix the spelling to "metabolized".
- Optionally state the LightGBM settings behind 0.735 / 0.752. They reproduce in direction: 0.745 / 0.757, better on
  12 of 15 splits.
- Issue 4 (paper text unread) is an evidence gap, not a defect. The labels are now confirmed by both the data and the
  archived UCI page.

**Judgment record (advocate's reading)**

Verdict: ship after text changes.
Validity:
- USE-5 holds.
- LEAK-4/LEAK-10 hold (logBCF dropped).
- PROV-13 holds (repair, 3 drops).
- SPLIT-4/USE-10 hold (IID); SPLIT-31 note added; split text corrected.
- LEAK-31 is in its keep-with-note branch (effect at most about 0.015 AUC); the citation is fixed.
- USE-8: direct (curator may choose approximate with the QSAR siblings).

Value: TP-2 holds (real modest signal); TP-5 holds (21+ per fold).
Quality: CLEAN-24 holds; CLEAN-11 extremes kept.
For the curator:
- The LEAK-31 / CLEAN-24 keep-or-drop of the 9.
- The fit label, together with qsar_oral_toxicity issue 6.
- Optional logKOW column.

**Rebuttal**

We agree on the verdict: ship after changes, with no exclusion and no re-split. What is left is one framing fix and
the fit label.

**Critic 1: logKOW (USE-6 Must). Conceded.**

My opening argued that USE-6 permits the logKOW as an input but does not require it. That fails on the definition's
own text. The use_case says "decide whether the usual estimate from its octanol-water partitioning can be trusted".
That decision presumes the assessor holds the KOW, so the definition contradicts itself. A Must holds only when the
definition is fixed.

The two remedies are not equal:

- **(a) Add `logKOW` with an exp/pred flag.** This is the closer match. It costs nothing in validity: logKOW alone
  scores 0.659, and logBCF stays unknown. It barely moves the score: 0.762 -> 0.762 to 0.764 (claim audit).
- **(b) Rewrite the use_case to "before the KOW is known".** This would be a rephrase made only to excuse a gap, which
  is a factor weighed against it under USE-9. It also clashes with the cohort: every chemical was kept for having a
  curated KOW.

I recommend (a). If the curator prefers (b), it is still a text-only fix and the dataset ships.

**Critic 2: `fit = "direct"` (USE-8 Must). Partly conceded.**

I dispute two of the three gaps the critic names:

- **The congener optimism (point 3)** is not a fit gap. SPLIT-4 (Must) and SPLIT-31 say IID matches the framing when
  new chemicals keep their families. amazon_employee_access and bank_marketing carry the same note without that making
  their fit approximate.
- **The descriptor selection** is at most about 0.015 AUC (claim audit). Once the note says that, it is a small
  documented exception, not "a potential leak kept on purpose" of kick's size.

The logKOW gap was real but closes under remedy (a).

So: with (a) applied and the LEAK-31 note corrected, `direct` holds. Without (a), I concede `approximate`. Either way,
the curator should answer this in the same pass as qsar_oral_toxicity issue 6.

**Critic 3: the split text. Agreed.**

This is my point 3: same facts, same remedy. Rewrite the text, add the scaffold-gap note, and list the dataset as a
SPLIT-31 candidate.

**Critic 4: LEAK-31. Agreed.**

This is my point 4. Record it as `Exception to LEAK-31` with the distinguishing fact: the source published only the
selected set, and CLEAN-24 keeps a source's descriptors. Word the note `Potential leak, kept on purpose:`, cite
qsar_fish_toxicity and qsar_aquatic_toxicity instead of home_credit, and add the RDKit-only control. Dropping the 9
(option b) remains the curator's call.

**Critic 5: label noise. Conceded as a note.**

The critic agrees that USE-5 is met in substance. Under remedy (a), the exp/pred flag also puts the predicted-KOW rows
into the data rather than hiding them. Keep REVIEW issue 4 open until the paper's wording has been read.

**Critic 6: housekeeping. Agreed.**

This is my point 7: drop issue 7, fix the record tag and "no known risk", fix the spelling, and state the LightGBM
settings.

**Net**

Verdict: ship after changes. One definition fix (logKOW plus the exp/pred flag, or the use_case rewrite) and notes
(split, LEAK-31 exception, label provenance) are needed. The fit label goes to the curator together with
qsar_oral_toxicity issue 6.

</details>

<details><summary>Critic</summary>

Position: **ship after changes.** The task is real (an assessor's mechanism call), logBCF is correctly dropped, the
swap repair holds (Dragon B02, F04, nHM match the repaired SMILES on 776/776), and no column leaks. Nothing here calls
for exclusion. But the definition says three things the evidence contradicts, and one input the actor has is missing.
Points in rank order.

**1. The logKOW the class is read against is known at the prediction point and not given (P3, USE-6 Must)**

- Problem. The use case is "decide whether the usual estimate from its octanol-water partitioning can be trusted".
  That presumes a known KOW. Under REACH the logKOW is an Annex VII requirement and the first tier of the B screen, so
  it is in hand before any OECD 305 fish test (practitioner, gap 1). The 779 chemicals were kept *because* they have
  a curated KOW (record, 2026-10-07). The class is the residual of logBCF from the TGD line *at that logKOW*. The
  definition gives only MLOGP (r = 0.87 with the curated value).
- Effect. As shipped, the task is "guess the mechanism without the KOW the assessor holds", which is not the stated
  decision. USE-6: dropping a known input changes the task.
- Evidence, both sides. practitioner.md: RF on the 9 descriptors 0.750 -> 0.768 macro AUC, class 2 vs rest 0.762 ->
  0.797, log loss 0.744 -> 0.726. claim_audit.md row 4: on the shipped 202 features the gain is ~0 (0.762 -> 0.762;
  log loss 0.720 -> 0.718). So it is not a leak (logKOW alone 0.659; logBCF stays unknown) and adding it costs nothing
  in validity; the score effect is small with RDKit in. The point is the framing, not the score.
- Remedy (fix the definition, mildest that works). Either (a) add `logKOW` from the authors' 2015 SI table (772 of 776
  matched; 650 experimental, 122 predicted) with an `exp/pred` flag, or (b) move the prediction point to "before the
  KOW is known" and rewrite `use_case` so it no longer refers to trusting the KOW estimate, with one sentence saying
  why logKOW is not an input. Either one meets USE-6; the definition as written meets neither.

**2. `fit = "direct"` while the definition names a known gap (P3, USE-8 Must)**

- Problem. `fit_reason` itself says the 9 descriptors were chosen on chemicals in our test folds, "which may favour
  those slightly": that is "a potential leak kept on purpose", which USE-8 lists under approximate (kick). Point 1 is a
  second gap (a known input missing), and point 3 a third (random test chemicals where a third have congeners in
  train). qsar_aquatic_toxicity, same mechanism, is `approximate` (precedents.md section 6).
- Effect. A user reading `direct` takes the score as the use-case score; it is optimistic for new chemotypes (point 3).
- Remedy. Set `approximate` and name the gaps, or remove the gaps so `direct` is true (add logKOW, drop or exception
  the 9, see point 4). Answer together with qsar_oral_toxicity issue 6 so the QSAR siblings match.

**3. "The file has no chemical families for a stricter split" is false (P4, SPLIT-1 Must holds; SPLIT-31 Should)**

- Problem. Murcko scaffolds are exact from the SMILES (SPLIT-24 allows that key). 42 congener series hold 260 rows
  (34%): biphenyls 64, naphthalenes 24, diphenyl ethers 21 (claim_audit row 1). The biphenyls (PCBs) hold 17 of the
  64 class-2 chemicals (split_audit).
- Effect. Most of the IID signal is recognising a congener: RF 0.804 on series rows under IID vs 0.553 held out; rows
  outside a series 0.714 vs 0.710. Shipped splits: 0.779 on test rows with a seen scaffold, 0.655 on a new one.
- What I do not ask. A scaffold re-split: the full one leaves folds without class 2 and test sizes 30-556
  (split_audit), and families recur in new chemicals (SPLIT-4). IID stays.
- Remedy (a note). Rewrite `task_summary.split` and the Split bullet with the numbers above, rest IID on the use case
  (a new chemical, usually of a measured family), and list a scaffold-grouped variant as a SPLIT-31 candidate, as the
  qsar_oral_toxicity mediator did today (change 4).

**4. The descriptor-selection note misattributes the gap and cites a precedent decided the other way (P4, LEAK-31 Should)**

- Problem. LEAK-31: "keep with a note when small, remove it when we can". Here removal is possible (RDKit's 193 are in;
  RF 0.758 without the 9, 0.763 with). The note says "as home_credit_default_risk", but home_credit's selection was
  removed (CC 2026-10-19), which is LEAK-31's only case.
- Evidence that the keep is defensible but the note is wrong. claim_audit row 3: the Train-vs-Test gap reproduces
  (RF +0.069, p = 0.04), but RDKit-only features, which nobody selected, show +0.054 (p = 0.09). At most ~0.015 is
  selection; the rest is the authors' test chemicals being harder.
- Remedy (a note, not a drop). Keep the 9 as the "small" branch, recorded as `Exception to LEAK-31` with the fact
  that sets it apart (the source published only the selected set; CLEAN-24 keeps a source's descriptors), worded
  `Potential leak, kept on purpose:` with the RDKit-only control, citing qsar_fish_toxicity / qsar_aquatic_toxicity
  instead of home_credit. Curator's call if he prefers option (b), drop the 9.

**5. The label is partly a convention and partly built on a predicted KOW, and the paper is unread (P3, USE-5 Must; EV-7)**

- Problem. 122-124 shipped rows (16%) have a *predicted* logKOW in the 2015 table; the band rule reproduces only 72%
  of them (claim_audit row 5). Below logKOW 1 the class is mostly class 1 by convention (practitioner gap 4). The
  thresholds are inferred (600 of 607), the paper text still unread.
- Effect. Label noise on about a sixth of rows, concentrated where the mechanism is least defined. Not a reason to
  stop: the rule is checked on the data (USE-5 met in substance).
- Remedy (a note). State the exp/pred split and the sub-1 convention in curation_comments; keep REVIEW issue 4 open
  until the paper's own wording is read.

**6. Housekeeping the rules settle (PROV-15 Must; records)**

- REVIEW issue 7 (pretraining overlap) must leave the issue list: PROV-15 / EV-4 say it never changes a decision
  (precedents.md section 9). The TabSTAR label note moves to the record as a problem of that copy.
- Record tag `Free Text (Short)` is stale since the SMILES drop; the 2026-10-20 assessment's "no known risk" contradicts
  open issues 4 and 5. "metabolised" vs "metabolized" in task_summary vs the label.
- The stated LightGBM numbers (0.735 / 0.752, 13 of 15) reproduce as 0.745 / 0.757, 12 of 15 (EV-8): state settings
  or round the claim.

Dropped as unsupported: the clean-room "776 vs 779 unexplained" (documented in Decision 2); RDKit extreme values and
organotin NaN (valid, structure-caused, CLEAN-11); weak signal (RF skill +0.179 over the prior, 21-22 class-2 rows per
test fold: scorable, TP holds).

**Rebuttal**

We agree on the verdict: ship after changes, no exclusion. Two disputes are left. Both are about whether a change is
required or optional.

| Advocate point | Response |
|---|---|
| 1. Target and inputs valid, no leak | **Concede.** My brief says the same: logBCF dropped, MLOGP band 471/776, Dragon values match the SMILES on 776/776. |
| 2. Repair from origin | **Concede.** REVIEW issue 2's drop-six alternative breaks PROV-13 and should close. |
| 3. IID stays, split text rewritten, SPLIT-31 candidate | **Concede.** This is my point 3 and its remedy. |
| 4. LEAK-31 keep-with-note branch, not an exception | **Concede.** With at most ~0.015 AUC from the selection (RDKit-only control +0.054 vs +0.069), the rule's own "keep with a note when small" branch applies. No `Exception to` line is needed. The citation and the note's attribution must still be fixed, as the advocate agrees. |
| 5a. `direct` defensible because the effect is small | **Dispute.** USE-8 (Must) lists "a potential leak kept on purpose" as approximate and sets no size threshold. The advocate's own remedy in point 4 words the note `Potential leak, kept on purpose:`, which is USE-8's wording for approximate. A Must has no exceptions (principles.md, Strengths), so "small" cannot carry `direct`. The advocate also concedes, in point 3, that IID is optimistic for new chemotypes (0.779 vs 0.655 by scaffold seen / unseen). That is a second named gap. Rule that wins: USE-8. Required change: `approximate` with the gaps named, or drop the 9 descriptors and reword the split note so that no kept gap remains. Settle it in the same pass as qsar_oral_toxicity issue 6. |
| 5b. logKOW: USE-6 says what *may* go in; measured gain ~0 | **Partly concede, dispute "optional".** Concede the measurement: on the shipped features the gain is 0.762 -> 0.762/0.764 (EV-2), so the score does not change. But `use_case` reads "decide whether the usual estimate from its octanol-water partitioning can be trusted". That is a decision taken with the KOW in hand, and USE-6 (Must) makes a known input legitimate, while USE-1/USE-3 require the prediction point to be stated consistently. The definition states two prediction points: "structure only" and "judging the KOW estimate". The advocate's own point-5 remedy ("one sentence, or add the column") resolves this. His judgment record then lists the column as "optional" and leaves out the sentence. I ask that one of the two be required. The 124 predicted-KOW rows argue for an exp/pred flag if the column is added, not against adding it. |
| 6. Worth benchmarking | **Concede.** RF skill +0.18 and 21-22 class-2 rows per fold. My brief dropped weak signal as a point. |
| 7. Housekeeping | **Concede.** This is the same list as my point 6. On issue 4, I accept that the labels are confirmed (archived UCI page, rule 599/606). My point 5 remains a note only: state the exp/pred share (16% predicted, rule fits 72% of those) and the convention below logKOW 1. |

No new facts.

</details>

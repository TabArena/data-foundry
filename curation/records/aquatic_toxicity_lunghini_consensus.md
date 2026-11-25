---
unique_name: aquatic_toxicity_lunghini_consensus
name: 'Consensus QSAR models estimating acute aquatic toxicity for three trophic levels organisms: Algae, Daphnia and Fish (data)'
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Expanding Science Catalogue
- 'Samples: Over Time'
- 'Time: Dated'
original_source: Other
year: '2020'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.3708082
- https://doi.org/10.1080/1062936X.2020.1797872
v2_path: datasets/_dev/tabarena-v0pt2/aquatic_toxicity_lunghini_consensus/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes, and the changes are applied; disputed: USE-1 / USE-6 (which prediction point the dataset ships, issue 1), MET-5 / MET-11 (whether `rmse` is the source's criterion or the fallback, issue 2), SEL (a `Selection Bias` marker, settled against adding one: the family's tested compounds stand for the candidates a screen would test, and no QSAR sibling carries it); for the curator: issues 1-2. Priority 3: gap 0, use case +, source +, shape 0, risk 0 (the shape point falls away because the task has one feature, the structure; neither open issue raises a leak, an unclear target, a duplicate or a recommendation not to ship).

**Assessment (AI, 2026-11-25):** corrections to today's screening block below, measured on the file and on the shipped frame while the dataset was added (the block itself stays as it was written): the `DB` field names ten sources over the 3,680 compounds, not nine - ECHA 1,805 (not 1,791), Literature set 1,681, ECOTOX 1,114 (not 1,089), VEGA 960, OASIS 668, NITE 455, EPAFHM 389, EFSA 140, Aquatic ECETOC 63 and ECOTOX-EPA 51, which the block left out; 1,328 of the 2,200 fish compounds name two or more of them, not 1,339; the ADORE fathead-minnow comparison covers 801 compounds, not 766; and the "ridge linear model 0.788" is not reproducible - on the shipped splits the linear baselines reach RMSE 0.957 (selected) and 1.982 (plain) against LightGBM's 0.719 and the training mean's 1.281. The 8 pairs that share an InChIKey skeleton are tautomers, not stereoisomers: the file carries no stereochemistry, and 14 substances are drawn twice once the CAS-RN is used as well. The companion article is open after all (the first author's thesis reproduces it), so the merge rule, the model selection criterion and the evaluation are read and quoted in the definition.

**Assessment (AI, 2026-11-25):** collection fact `Time: Dated` in place of `Time: Lost`. The rule sets `Dated` when the release or a parent source keeps the date, even where the date turns out to carry nothing, and the reason the screening gave (the CAS-RN is a registration number) does not distinguish this record from six sibling records of this family that are `Dated` on the same key. Measured on 2026-11-25: ECOTOX, through the ADORE release of its mortality tests, holds an entry for 1,444 of the 2,186 shipped chemicals (66.1%) and dates each one, 1985 to 2022; the sibling qsar_fish_toxicity was dated the same way, 850 of its 908. The date does not move the split: the target barely changes with it (Spearman -0.03) and both readings of the catalogue question land on the same leaf.

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 3: this record's task is the fish 96-hour pLC50 on the 2,200 compounds that carry it, with the structure as the only published input and scaffold groups as the split; measured on the file today it holds 808 of `qsar_fish_toxicity`'s 908 chemicals at the same values and adds 1,392 more. The Daphnia 48-hour and algae 72-hour endpoints of the same file are other targets on other organisms, so they are separate tasks and separate records when a curator wants them (PROV-7), not part of this one.
- Source: Lunghini and Marcou (Université de Strasbourg), Azam, Enrici and Van Miert (Solvay), Varnek; Zenodo deposit of 2020-03-12, doi 10.5281/zenodo.3708082 (concept doi 10.5281/zenodo.3708081), CC BY 4.0, one file `MergedEndpoints.sdf` (6,325,348 bytes, md5 `412738140006ff5ad4394fa188885a43`). Companion article: "Consensus QSAR models estimating acute toxicity to aquatic organisms from different trophic levels: algae, Daphnia and fish", SAR and QSAR in Environmental Research 31(9):655-675, online 2020-08-17 (doi 10.1080/1062936X.2020.1797872); the year stays 2020. As published, measured on the file on 2026-11-25: 3,680 records that all parse, 3,680 distinct canonical structures, 3,659 CAS-RN; fields `SMILES_Canonical`, `CASRN`, `DB`, `endpoint` and, per endpoint, the value as `pLC50`/`pEC50` and in mg/L. Values per endpoint: fish 96-h 2,200, Daphnia 48-h 2,120, algae 72-h 1,440; of the fish compounds 984 carry the fish value alone, 531 fish and Daphnia, 501 all three, 184 fish and algae. The fish target spans -2.40 to 6.51 (sd 1.28). Corrections to the screening of 2026-10-31, which read the Zenodo page and a preview: the `DB` field names nine sources, not five (over all 3,680 compounds ECHA 1,791, Literature set 1,681, ECOTOX 1,089, VEGA 960, OASIS 668, NITE 455, EPAFHM 389, EFSA 140, Aquatic ECETOC 61); the unit reading is confirmed on every row, not only the first (below).
- Use case: an industrial or regulatory hazard assessor estimates a substance's acute fish toxicity from its structure instead of running the 96-hour test, for classification and for a REACH dossier (the article's own aim is industrial: "A benchmarking against existing tools has been carried out on a set of compounds considered more representative and relevant for the chemical space of the current chemical industry", and "industrial data performances were noticeably lower than those on public data"; `REACH` is one of the Zenodo record's keywords); fit direct, since a dossier reports short-term fish toxicity per substance and the test species varies between studies; collection `Samples: Over Time` (public values accumulated over decades of testing), `Time: Lost` (no date, species, test condition or count of underlying measurements ships; a parent source could date many entries - a publication year per test in ECOTOX, a study year in an ECHA dossier - but the CAS-RN in the file is a registration number, not an entry date); type `Expanding Science Catalogue`, the tag both siblings carry: the rows are a cut of public databases that keep growing, even though the deposit itself is one-off.
- Split: leaf `L-FAMILY.key` (Grouped, `UnseenGroup`, the family key) because the catalogue walk answers no at `CAT.next-items` - the source aims its models at chemicals like the ones it collected and at an industrial inventory it benchmarks separately, not at the databases' next entries (SPLIT-37 step 3) - and a scaffold key is computable (SPLIT-31, `FAMILY.key`). Measured on the fish subset today: 1,771 groups over 2,200 compounds, namely 676 ring-less compounds each alone, 650 compounds whose Bemis-Murcko scaffold is benzene (29.5%, above a tenth, so each alone) and 445 further scaffolds; no SMILES holds a `.`, so no salts or mixtures to split. Open: whether the 8 pairs that share an InChIKey skeleton (2,200 structures, 2,192 skeletons) are held to one side as copies of one item (SPLIT-37 step 1, LEAK-17).
- Siblings and duplicates: `qsar_fish_toxicity` (`Yes`, shipped, 908 fathead-minnow chemicals) - this record is the better data named in its open decision, and that decision waits on this record being added; `qsar_aquatic_toxicity` (`Yes (Disagreement)`, 546 Daphnia chemicals) - the Daphnia endpoint of this file holds 374 of its 546 (68.5%, values r 0.971), lower than the 89.0% containment on the fish side, so it settles nothing there and that record keeps its own decision; `adore_aquatic_toxicity` (`TBD -> Yes`, ECOTOX per-test entries, a cross-species task of its own); `bcf_lunghini_2019` (the same group, bioconcentration); `qsar_bioconcentration`, `qsar_biodeg` (the Milano family). Not a duplicate of the UCI pair: a different compilation published by different authors from overlapping public pools (PROV-4 traces each to its own first publication), and the shared chemicals are why the curator's question sits on `qsar_fish_toxicity` (PROV-6) and not here. External collections: none found.
- Better data: found as better data for `qsar_fish_toxicity`, and on its Daphnia endpoint for `qsar_aquatic_toxicity`. Nothing better than this one for a per-compound fish LC50 was found in a quick look: ADORE (its own record) is per-test and its fathead-minnow cut is 911 chemicals, no larger than the 908 already shipped; a fresh cut of ECOTOX would be our own compilation rather than a published table; Sheffield and Judson's ensemble fish model (Environ. Sci. Technol. 2019, doi 10.1021/acs.est.9b03957) builds an LC50 set of 2,656 chemicals from ECOTOX and ECHA through EPA ToxValDB, 2,124 of them in training, but publishes no per-compound file - the supporting information is a text document and the values sit behind the CompTox dashboard.
- Papers and pages: the Zenodo record (its description defines each field: fish "the log median lethal concentration measured at 96 hours", Daphnia immobilization "recorded at 48 hours", algae "growth inhibition effect ... measured at 72 hours"); the companion article, whose abstract was read through Semantic Scholar and OpenAlex. The full text was not reachable from here: the publisher's copy is paywalled, the HAL deposit hal-03130917 is closed access, and no open copy turned up; the merge rule and the evaluation section are therefore unread (PROV-17), and the PDF is worth asking for before either is written into a definition.
- Metric: none deliberate found. The only figure the abstract gives is "Reasonable predictive performances were achieved (RMSEext = 0.56 - 0.78)" over the three endpoints, a headline number, which MET-5 does not count as a deliberate choice, and the section that would say what the models were selected by could not be read; so the fallback `rmse` on the log scale (MET-8), which is what `qsar_fish_toxicity` ships. Inputs: none. The published `pLC50` is -log10(mmol/L): recomputing it as -log10(mg/L / molecular weight) matches the published value with a median absolute difference of 0.0003, while -log10(mol/L) differs by exactly 3.000 in the median, so adding 3 puts the target on `qsar_fish_toxicity`'s scale and leaves RMSE unchanged.
- Risks for /add-dataset: the consensus merge is undocumented - 1,339 of the 2,200 fish compounds name two or more source databases and up to eight, and nothing in the file says how several experimental values became one value (USE-5, EV-2); some `DB` entries carry a number in brackets (`ECOTOX(76)`, `ECHA(10)`), always 10 or above, which looks like a count of underlying values but is unverified. The fish value is pooled over fish species and no species column ships, where `qsar_fish_toxicity`'s target is the fathead minnow's, so the task summary has to say so (USE-5); measured today, where this value meets an ADORE fathead-minnow value it is that value (766 compounds, r 0.991, median difference 0.000) and against ADORE's rainbow trout r 0.955. `DB` is not a feature: a source list is not known for an untested chemical (LEAK-1). The two unit columns disagree for a few compounds: 34 of 2,199 fish compounds differ by more than 0.3 log from -log10(mg/L / molecular weight), at most 1.19, one fish compound ships no mg/L value and 13 Daphnia rows carry mg/L 0, so one column has to be chosen as authoritative with a note (CLEAN-1). Features are computed from the SMILES (CLEAN-24).
- Worth benchmarking: measured on 2026-11-25 on scaffold-grouped splits (10 x 3) with features encoded from the SMILES, an untuned LightGBM reaches RMSE 0.718 against 0.788 for a ridge linear model, on a target of sd 1.281, so there is a signal and the methods separate (TP-2); on the 1,392 compounds this set adds next to `qsar_fish_toxicity`'s 908 they separate as well (0.766 against 0.822, sd 1.226). 2,200 compounds in 1,771 groups is far from `Too Small` (TP-5).
- Priority: gap 0 (chemistry & material science 15 of 193 accepted, regression 85, grouped 51 - none thin in this run's coverage snapshot), use case + (the source names the actor and the decision), source + (a named group's deposit under CC BY 4.0 with a peer-reviewed companion article), shape + (2,200 compounds in 1,771 scaffold groups, the structure as the only published feature), risk - (the merge rule and the species pooling are undocumented).
- Fields set from the file today: `required_split: Grouped (NON-IID)` (was empty) and the tags `Non-IID (Grouped)`, `Expanding Science Catalogue`, `Samples: Over Time`, `Time: Lost`; `year: 2020`, `original_data_state: One Table` and `problem_type: Regression` are confirmed; `priority` stays 3 on the factors above.

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 3,680 public compounds with acute toxicity values for algae (72-h EC50), Daphnia (48-h EC50) and fish (96-h LC50), merged from public sources by Strasbourg and Solvay; a larger form of the two UCI aquatic toxicity tasks, with the structure as the only input.
- Source: Lunghini, Marcou, Azam, Enrici, Van Miert, Varnek (Université de Strasbourg, Solvay), Zenodo doi 10.5281/zenodo.3708082 (2020-03-12, CC BY 4.0): "3680 public unique compounds annotated by, at least, one experimental value for the given endpoint"; companion article "Consensus QSAR models estimating acute toxicity to aquatic organisms from different trophic levels: algae, Daphnia and fish", SAR and QSAR in Environmental Research 31(9):655-675, 2020 (doi 10.1080/1062936X.2020.1797872; not opened, 403). As published: one SDF (`MergedEndpoints.sdf`, 6.3 MB) with canonical SMILES, CAS number, the data sources (the preview shows NITE, VEGA, ECOTOX, OASIS and a "Literature set"), the endpoints present, and per endpoint the value in mg/L and as pEC50/pLC50 (the negative log of mmol/L, checked on the first record). The counts per endpoint and how repeated values were combined are not on the page.
- Use case: a hazard assessor at a chemical maker or a regulator estimates the acute aquatic toxicity of a new substance before testing, for classification and labelling; the Zenodo page names no actor (the industrial interest is Solvay's), fit approximate; regime not set by the source (grouped by scaffold or IID by compound, for /add-dataset).
- Siblings and duplicates: `qsar_aquatic_toxicity` (`Yes (Disagreement)`, 546 Daphnia chemicals) and `qsar_fish_toxicity` (`Yes`, 908 fathead minnow chemicals) draw on the same public pools, so many of their chemicals likely recur here (another source, its own record, PROV-4; check the overlap by CAS); `adore_aquatic_toxicity` (unscreened, per-test entries from ECOTOX), `fish_toxicity` (`No`), `bcf_lunghini_2019` (the same group, another endpoint). External collections: none found.
- Better data: found as better data for `qsar_aquatic_toxicity` and `qsar_fish_toxicity`; no further search this round.
- Papers and pages: the Zenodo record; the SAR QSAR Environ Res article.
- Metric: not read (the article was not reachable; the Zenodo page says only that the SVM models were validated following OECD principles), so the fallback `rmse` on the log scale (MET-8), to check against the article's ranked criterion; inputs none.
- Risks for /add-dataset: three endpoints, so one task per endpoint or one chosen (the per-endpoint counts decide whether algae is too small, TP-5); the features must be computed from the SMILES and the structures standardised (CLEAN-24; LEAK-17 for duplicate structures); the combination of repeated measurements is not documented.
- Priority: gap 0 (chemistry & material science and regression are not thin), use case 0 (no decision named on the page), source + (the authors' deposit with a peer-reviewed article), shape + (3,680 compounds).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `qsar_aquatic_toxicity`, `qsar_fish_toxicity`.
- as published: 3,680 unique public compounds, each with at least one of three endpoints (Daphnia 48-h EC50, fish 96-h LC50, algae 72-h EC50), one value per compound and endpoint in log and mg/L; one SDF with ...; target: Daphnia 48-h pEC50 (immobilization) or fish 96-h pLC50 per compound; access: open (CC BY 4.0).
- Why: Same target and unit (one toxicity value per chemical) as qsar_aquatic_toxicity (Daphnia magna 48 h) and qsar_fish_toxicity (fish 96 h), structure given
- Adds: One aggregated value per chemical (the shape of the UCI tasks, unlike ADORE's per-test entries) over up to 3,680 compounds against 546 and 908; structures given; open CC BY 4.0

## Review

**Outcome:** added. The fish 96-hour LC50 of the Lunghini et al. 2020 consensus collection: 2,186 chemicals, the structure as the only feature, scaffold-grouped splits, `rmse`. The review panel recommends shipping after changes, and the changes are applied. Judgment record:

```text
Verdict: ship after changes (applied).
Validity: SEL-2, SEL-3 hold. USE-1 triggered (the folder named two prediction points at once), fixed by text: it
  ships the screening moment, and which of the two moments ships is issue 1. USE-5 holds, now on the source's own
  rule, read in the article (p. 658). USE-8 direct, kept; the fact that sets it apart from
  drug_induced_autoimmunity_prediction is that the label rule is documented and verified. LEAK-1, LEAK-18, LEAK-19
  and LEAK-30 hold under a dedicated attack, and the task gamer found no exploit above its +-0.0005 noise floor.
  SPLIT-4, SPLIT-31 and SPLIT-37 hold (no re-split); the SPLIT-32 departure is fixed (`Time: Dated`). PROV-13
  triggered, fixed by repair (3 substances resolved from the registry, 2,186 rows). PROV-17 moot: the article is
  open and was read.
Value: MET-1 triggered (the recorded reason asserted a paywall that does not exist), fixed by rewriting it; the
  declared metric stays `rmse`, and its origin is issue 2. TP-2 and TP-5 met with margin.
Quality: CLEAN-16 round(3); nine corrections where the notes misstated the source or the shipped frame (EV-2).
Weighed: source +, shape +, gap 0, risk - (smaller than at screening: the article is read and the merge rule known).
For the curator: 2 issues - issue 1 a framing call (which prediction point), issue 2 a one-line metric-origin call.
  Nothing reaches the remedy ladder's third rung, and no agent asked for exclusion.
```

**Main points:** Two calls, neither of which blocks shipping: which moment the dataset predicts for (the untested substance, as built, or the registration dossier, which would add the file's Daphnia and algae values as two sparse features), and whether `rmse` is recorded as the source's own criterion or as the fallback. Applied without a decision: the three substances the file draws under two molecular formulas are repaired from the chemical registry instead of dropped whole (2,183 rows to 2,186), the target is rounded back to the three decimals the file publishes, the use case is narrowed to the screening moment, and the statements about the source, the split and the sibling overlap are rewritten from the article - which is open and was read - and from the shipped frame. The record's `Time: Lost` becomes `Time: Dated`, since a parent source dates most of these entries.

**Issues for Andrej:**

1. **Which moment does the dataset predict for: the untested substance, or the dossier that already holds the Daphnia and algae values?**

   * **Problem:**
     - The dataset ships the earlier moment, the substance that has not been tested, and drops the file's `pEC50 - DAPHNIA` and `pEC50 - ALGA`; the dossier moment, where the assessor already holds those two values, is as real a use case and no rule picks between them[^1b].
     - Until this review the folder named both moments at once, so the one it predicts for is now written down but not chosen[^1a].
     - The two dropped values are worth 0.031 RMSE over all test rows and 0.081 over the rows that carry one, so the choice changes the task and not only its wording.
   * **Effect on the task:** as built, the task is structure to fish LC50 with one feature over 2,186 chemicals; at the dossier moment it becomes structure plus two sparse assay inputs, present on 47.1% and 31.4% of the rows (55.6% carry at least one), which would also be what sets this dataset apart from `qsar_fish_toxicity` beyond its size.
   * **Experiments:** nine shipped splits, the recommended SMILES encoding and an untuned LightGBM (2026-11-25).

     | Inputs | RMSE, all test rows | RMSE, rows with a Daphnia or algae value |
     |---|---|---|
     | The structure alone (implemented) | 0.7167 | 0.6616 |
     | Structure and the two values | 0.6856 (SE 0.005, better on 9 of 9) | 0.5808 (SE 0.010, 9 of 9) |
     | Structure and only flags for whether each value is present | 0.7154 (SE 0.0014, better on 6 of 9) | not measured |

     The gain is chemistry, not a record of what the collection covered: the flags alone are not above noise, although the mean target does differ with which of the two values a chemical carries (4.63 for the chemicals that carry the Daphnia value and not the algae one, against 4.08 the other way round). The fish value correlates with the Daphnia value at r 0.79 and with the algae value at r 0.78.
   * **Consistency:** at the real dossier moment the two values exist for essentially every substance, since the Daphnia and algae tests bind from 1 t/y under REACH Annex VII while the short-term fish test binds only from 10 t/y under Annex VIII; here they exist for 55.6%, so option B mirrors that moment only in part and the gap would have to be named. `qsar_fish_toxicity`, the sibling on the same target, ships the structure alone.
   * **Panel:** the practitioner argues for the dossier moment, since those values are on their desk and they would use them; the advocate and the column auditor for the screening moment, as the source's own aim and the moment the single feature matches, with the other two endpoints left available as datasets of their own; the critic and the split auditor take no side on which, only that the folder must not sit between the two. Three rule citations made in the debate do not bear on this choice and are left out of the options[^1c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The untested substance (implemented) | one feature, the structure; the Daphnia and algae columns stay out | the moment the single feature matches, and the source's own aim; the other two endpoints stay available as datasets of their own | gives up a measured 0.031 RMSE; the dataset then differs from `qsar_fish_toxicity` mainly in size |
     | B | The dossier | ships `pEC50 - DAPHNIA` and `pEC50 - ALGA` as two numeric features, missing where the file has none, with their coverage named in the fit reason | a second real use case, with inputs a registrant holds by construction; a mixed task (a structure and two sparse numbers) that no sibling covers | the coverage is 55.6% here against essentially all substances at the real moment; the frame, the text and the panel's work on the inputs have to be redone |

   * **Recommendation:** A, weakly: it is the moment the frame was built for and the one the source aims at, and B's gain comes with a coverage gap that has to be disclosed. B is the better answer if this dataset should be more than a larger `qsar_fish_toxicity`. **Decision:** A or B?

   **Notes for the AI:** on B, keep `pEC50 - DAPHNIA` and `pEC50 - ALGA` in `_clean` as two numeric columns, missing where the file has none (USE-7: the missing value is itself what the actor sees at that moment); restore "and to fill a registration dossier" in `use_case`; name the two inputs and their 47.1% and 31.4% coverage in `known` and in `fit_reason`, with the gap against the real dossier moment (USE-8); update `row` and `changes`; re-run `dataset check` and the leak, task and group probes; and re-run the column and split auditors on the new inputs. On A nothing changes.

   [^1a]: **USE-1** (Must): write down one prediction point and the use case first, and check every later choice against it. A folder that names two moments at once fails on this alone, whichever of the two it keeps.
   [^1b]: **USE-6** (Must): anything known at the prediction point is a legitimate input. **USE-7**: a value that is missing at the prediction point ships missing rather than dropping its row. **USE-8**: the fit reason names the population a model fitted here is good for, including a gap of this kind.
   [^1c]: Three citations from the debate that the mediator set aside: **LEAK-1**'s text is "Write down the prediction point and the use case first (USE-1, USE-3)", which is procedural and cannot decide which moment is written down; **PROV-7** narrows PROV-4 and PROV-6 and is about duplicates, not about whether a measured column may be a feature; **CLEAN-22** ("Keep every relevant feature") excludes a column for what it is - a leak, an identifier, a copy, the measurement that defines the label - and a Daphnia 48-hour EC50 is none of those.

2. **Record `rmse` as the source's own criterion, or as the regression fallback?**

   * **Problem:**
     - What is left to decide is the metric's origin field: the recorded reason said the article's evaluation section was behind a paywall, which is false, and it is rewritten[^2a].
     - The article does name one criterion the authors select models by, "Cross-validated determination coefficient was selected as fitness function" (p. 660), but reports the r2 and the RMSE side by side for the models themselves (p. 661).
     - `rmse` ships either way and no score changes.
   * **Effect on the task:** none on the data or the scoring; the origin and the reason are what a reader of the task card sees, and `source` asserts that our metric is the one the authors ranked by.
   * **Unknown:** whether `rmse` really stands for the authors' criterion turns on a formula we could not read: 1 - MSE/Var(y) ranks every pair of models exactly as RMSE does on a fixed test set, a squared Pearson correlation does not, and which of the two the authors wrote down is in Table S5 of the supporting information, which the publisher gates[^2b].
   * **Consistency:** `open_soil_spectral_library` keeps the criterion a paper tunes by although it grades by another; `qsar_fish_toxicity`, the sibling on the same target and the same scale, ships `rmse` as the fallback.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `fallback` (implemented) | the reason says the article names no criterion for the task itself, so the target's scale decides | asserts nothing we could not check; the same choice as the sibling | leaves it to the reason to mention that the authors do name a criterion |
     | B | `source` | the original becomes "cross-validated determination coefficient (the genetic algorithm's fitness function)", with the identity and the unread table stated in the metric's definition | records what the source actually optimises, as the precedent does | the identity holds only if their r2 is 1 - MSE/Var(y), which is in the table nobody has read |

   * **Recommendation:** B, with the identity and the unread table stated; A if you would rather not assert an identity on a formula nobody has seen. **Decision:** A or B?

   **Notes for the AI:** on B, replace `Metric.fallback(reason=...)` with `Metric.source("rmse", original="cross-validated determination coefficient (the genetic algorithm's fitness function)", reference=<the open route to the article>, definition=...)`, where the definition carries the RMSE identity and the note that Table S5 is unread (MET-5, MET-11), and re-run `dataset check`. On A nothing changes.

   [^2a]: **MET-1** (Must): the declared metric scores the real task, and the notes record where we looked; a reason that asserts something false about the source fails it.
   [^2b]: **MET-5** (Should): a paper's metric is the source's metric only when it is one deliberate choice - "the criterion it ranks, tunes or selects models by" - and a paper that reports several metrics side by side without naming the deciding one has no unique original, so the fallback is declared. **MET-11** (Must): a metric may stand for the source's as `source` when it "ranks every pair of models the same by identity", and the `definition` says the identity.

**Review panel:** ship after changes (mediator). Claim audit: the companion article is open and was read, which refutes two of the definition's statements about the source; the sibling-overlap figures are refuted on the shipped frame, and the claims about the data, the target and the splits hold. Column audit: no leak a probe missed, and two of the three two-formula pairs are repairable from the registry rather than droppable (the mediator resolved the third). Split audit: the split is right, its description was not. Blind review: "not a tabular task" - settled against it, since the harness read the SMILES as a categorical string where the benchmark encodes it as a structure. Task gamer: no exploit above the +-0.0005 noise floor, and the benzene carve-out leaves three fifths of the rows as singletons. Precedent check: 5 findings, three departures corrected and two citations fixed. Debate: agreed on the repair, the rounding, the wording and that no re-split is called for; disputed: which prediction point ships (issue 1), the metric's origin (issue 2), and a `Selection Bias` marker, settled against adding one.

<details><summary>Mediator</summary>

**Mediator's report — `aquatic_toxicity_lunghini_consensus`**

**1. Judgment record**

```text
Verdict: ship after changes.
Validity: SEL-2, SEL-3 hold. USE-1 triggered (the folder names two prediction points at once) —
  fixed by text; which of the two moments ships is the curator's (issue 1). USE-5 holds, now on
  the source's own rule, read in the article (p. 658). USE-8 direct, kept (the fact that sets it
  apart from drug_induced_autoimmunity_prediction: the label rule is documented and verified).
  LEAK-1, LEAK-18, LEAK-19, LEAK-30 hold under a dedicated attack. SPLIT-4, SPLIT-31, SPLIT-37
  hold (no re-split); SPLIT-32 departure fixed (`Time: Dated`). PROV-13 triggered, fixed by repair
  (3 substances resolved from the registry, 2,186 rows). PROV-17 moot: the article is open and read.
Value: MET-1 triggered (the recorded reason asserted a paywall that does not exist), fixed by
  rewriting it; the declared metric stays `rmse`; its origin is issue 2. TP-2, TP-5 met with margin.
Quality: CLEAN-16 round(3); nine note corrections where the definition misstates the source or the
  shipped frame (EV-2).
Weighed: source +, shape +, gap 0, risk - (smaller than at screening: the article is read and the
  merge rule is known).
For the curator: 2 issues — issue 1 is a framing call (which prediction point), issue 2 a one-line
  metric-origin call. Nothing reaches the ladder's third rung.
```

No agent asked for exclusion, and nothing in the panel supports one: no leak survived attack, the task probes are clean, and the data is what the definition says it is.

**2. Changes to make now (no decision needed)**

1. **Repair the three two-formula substances instead of dropping both rows — 2,186 rows** (PROV-13, Must; the ladder's first rung; LEAK-19 then keeps one row per substance). I settled this with the registry (PubChem, queried 2026-11-25): CAS 275-51-4 azulene **C10H8**, CAS 3347-22-6 dithianon **C14H4N2O2S2** (MW 296.3, which is the `Mol Weight` on that very row), CAS 104653-34-1 difethialone **C31H23BrO2S** (MW 539.5, likewise). In each pair exactly one drawn formula matches, so all three are repairable — including the one the column-auditor could not resolve, which is why the count is **2,186**, not the 2,183 built or the 2,185 the advocate's rebuttal computes. The two rows of each pair carry the same measurement (|Δy| ≤ 0.016). Note in the definition that the kept dithianon row carries no `Molecular weight` and no mg/L value, so the unit cross-check is unavailable on it, and that the current tie-break ("the row whose `DB` names more sources") would have kept the **wrong** azulene drawing — the registry, not the source count, decides. Re-run the scaffold groups and splits after the repair.
2. **Rewrite the three statements about the source from the article** (MET-1 and PROV-17, Must; USE-5; EV-2). I verified the route and the text myself: `https://theses.fr/2020STRAF016/document` → `publication-theses.unistra.fr/.../Lunghini_Filippo_2020_ED222.pdf`, HTTP 200, and I read journal pp. 658, 660 and 661 as images. The merge bullet, the "Not read" bullet and `fit_reason`'s clause are replaced by the rule as published (p. 658): only measurements under OECD-guideline conditions (recommended test organism, mortality at 96 h, larval-stage studies discarded, "the value must be precisely determined (i.e. values reported as ranges were excluded)"), **"In case of multiple values per compound, the median was taken as a representative value. When the ratio between the minimum and the maximum reported value per compound was >10, the entry was discarded"**, compounds above measured water solubility or unstable in water excluded (that comparison was possible for 743 fish compounds), SMILES standardised with salts/solvents and stereo removed, duplicates removed on standardised SMILES, and "LC50 and EC50 values originally expressed in mg/l were transformed to the inverse log of the molar dose (pLC50 and pEC50 in mMol/L)" — the primary confirmation of the +3 shift. Cite the open route in the sources. Builder issue A closes rather than going to the curator.
3. **Add the provenance line the article opens** (PROV-8, EV-2): the paper modelled **2,110** fish compounds (p. 658 and Table 2) where the deposit's fish column holds 2,200; algae (1,440) and Daphnia (2,120) match exactly. The 90 extra are unexplained.
4. **Rewrite the metric `reason`** (MET-1, Must) to what the article says — p. 660, "Cross-validated determination coefficient was selected as fitness function" (of the genetic algorithm that picks descriptor spaces and SVM hyperparameters); p. 661, "To evaluate the models' performance the r² determination coefficient and the RMSE parameters are reported (formulas are reported in Table S5)" — with the open route cited. The declared metric stays `rmse`; only the origin field waits on issue 2.
5. **Make `splits_comment` and `task_summary.split` describe the split that ships** (SPLIT-37 step 5 and the writing rule; the split itself is correct and does not move): give both figures — group id in training 0% against 22.6% at random, **actual Bemis-Murcko scaffold shared 60.9% against 83.3%** — name the bare-benzene bucket (649 chemicals, 29.7%, singletons by SPLIT-31) beside the ring-less one, and replace "that is the pattern of the other datasets of this family" with the measured decomposition (the split removes 59% of close analogs where it can group, 8.3% → 3.4%, and nothing on the 60.7% of rows that are singletons by rule). Fix both sibling citations: the quoted "qsar_fish_toxicity 7.2% against 6.9%" and "qsar_oral_toxicity 12.4% against 13.1%" are forward-by-date pairs; the apt one is `qsar_fish_toxicity`'s own scaffold-against-random 12.4% / 13.1% (Andrej, 2026-11-12), and `molecules.md`'s scaffold table, where every other molecule dataset removes more overlap than this one, is the contrast to state rather than smooth over.
6. **`Time: Lost` → `Time: Dated`, and soften the time-basis sentence** (SPLIT-32, Should): the rule sets `Dated` when the release *or a parent source* keeps the date "even where the date turns out to carry nothing", six sibling records of this family are `Dated`, and the stated reason (the CAS-RN is a registration number) does not distinguish — the CAS-RN is the join key on the sibling too. The leaf does not move: both readings of `[CAT.next-items]` land on `L-FAMILY.key`. Preferably run the ECOTOX join for this set's own coverage (ADORE's `ecotox_tests.csv` is on this machine); citing the sibling's 850 of 908 is acceptable. If the curator wants `Time: Lost` kept, it needs the fact that sets this case apart.
7. **`round(3)` on the target** (CLEAN-16): 307 of 2,183 values carry 1–2 ULP of float residue from the `+3` shift. Not exploitable (it is a function of the label the model would already have), but a free hint about how the file was built.
8. **Reword the censoring note** (as the definition cites LEAK-22; `molecules.md`, censoring decided case by case): say what the check found — 11 compounds sit at exactly 100.000 mg/L, the OECD 203 limit concentration, against 45 others across the whole ±10% band, 9 of the 11 from ECHA/NITE/Literature — and that the source excluded ranges and above-solubility values but could run the solubility comparison for only 743 fish compounds. No data change; 0.5% of rows.
9. **Reword the `DB` sentence** (EV-2): "a small and consistent 0.005 RMSE (25 of 30 folds, p 1.5e-5), dropped under LEAK-1 regardless", not "costs nothing measurable". The decision is unaffected.
10. **Restate the sibling overlap on the shipped frame** (EV-2, PROV-6): 805 of `qsar_fish_toxicity`'s 908 (88.7%), 783 by CAS-RN, 568 within 0.01, **adds 1,378** — recounted after the repair. The decision item `issues/qsar_fish_toxicity.md` quotes the pre-dedup 808 / 1,392 in four places and must be corrected, since its option B turns on these numbers.
11. **Add the population and noise-floor disclosure** to `fit_reason` / `curation_comments` (USE-8, USE-9): the authors' own "industrial data performances were noticeably lower than those on public data" and that we ship the public cut *before* their industrial extension; the distance-banded error under the shipped split (RMSE 0.87 where the nearest training chemical is ≤0.40 Tanimoto, 1,995 of 6,549 scored test rows, against 0.49 above 0.9); and the label's own floor — the paper's Figure 3 puts inter-database agreement at RMSE 0.55–0.67 against our 0.715, so R² 0.67 is not "much headroom".
12. **Small corrections** (EV-2, writing): "ten public toxicity databases" (one is a literature set, one is plausibly ECOTOX twice); "the most frequent value in mg/L is 13" (tied with 1.4 and 1.5); the ADORE "another fish species" comparison includes 5,737 crustacean/algal rows and improves when restricted to fish (median 0.059, 61.0%); the `order_drift` sentence — the flag is lag-1 autocorrelation 0.33 (neighbouring rows are near-analogs), not a monotone drift (Spearman −0.03, p 0.18).
13. **In the review, mark the record's `Screening (AI, 2026-11-25)` block superseded** on the five numbers the definition's own measurements contradict (nine sources vs ten, ECHA 1,791 vs 1,805, 1,339 vs 1,328, 766 vs 801, ridge 0.788 not reproducible), so they are not quoted forward.

**3. Issues for the curator**

**Issue 1 — Which prediction point does this dataset ship? (P3, USE-1 Must; validity)**

**Problem.** The folder names two different moments. `task_summary.use_case` puts the actor at the dossier ("to classify and label it **and to fill a registration dossier**"); `curation_comments` puts him earlier ("a substance before it is tested on fish"), and the frame is built for the earlier one — the file's `pEC50 - DAPHNIA` and `pEC50 - ALGA` are dropped. USE-1 is a Must and fails on its own: the folder must not ship sitting between the two. Which moment ships is not settled by the rules — both are real use cases — so it is the curator's.

**Effect.** Option A (screening, as built): the task is structure → fish LC50, 2,186 rows, unchanged from what the panel measured. Option B (dossier): two numeric columns are added, present on 47.1% and 31.4% of rows (55.6% at least one), and the task becomes structure plus sparse assay inputs — which is also what distinguishes this set from `qsar_fish_toxicity`.

**Each side's best evidence.**
* For B (practitioner, critic): REACH Annex VII 9.1.1 (Daphnia, TG 202) and 9.1.2 (algae, TG 201) bind at 1 t/y, the short-term fish test at Annex VIII 9.1.3 at 10 t/y, so at the dossier moment the two values exist by construction, and they are in the same file. USE-6 (Must) makes anything known at the prediction point a legitimate input. Measured gain: RMSE 0.7167 → 0.6856 overall (SE 0.005, 9/9 splits) and 0.6616 → 0.5808 on the rows carrying a co-input (SE 0.010, 9/9), same sign in five model families; fish vs Daphnia r 0.79, vs algae r 0.78.
* For A (advocate, column-auditor): the screening moment is the one the data's single feature matches; the source's own aim is the untested substance; PROV-7 keeps the Daphnia endpoint available as its own record later.
* **My decisive experiment** (9 shipped splits, `encode_smiles` + LightGBM) removes the strongest argument *against* B: the objection that "which rows carry a co-endpoint is a record of what the collection covered" is measurable but worthless — the two presence flags alone are worth **−0.0013 RMSE (SE 0.0014, better on 6 of 9 splits)** against **−0.0311 (SE 0.0048, 9 of 9)** for the values. The mean target does differ by presence pattern (4.63 for `daphnia, fish` against 4.08 for `alga, fish`), but a model cannot turn it into skill. So the gain is chemistry, not a collection artefact.
* **And one fact against B that the practitioner states himself:** at the real dossier moment the two values exist for essentially every substance; here they exist for 55.6%, so option B mirrors that moment only partly (USE-8 would have to name that gap). USE-7 does not force dropping the other 44.4%: the input the prediction acts on is the structure, and the fish value is the target.

**Rules.** USE-1 (Must) decides that one moment must be written down and everything checked against it; USE-6 (Must) then decides the columns, and is satisfied under either moment once the moment is fixed. **Three rule citations in the panel do not hold and should not appear beside the options:** LEAK-1's text is "Write down the prediction point and the use case first (USE-1, USE-3)" — procedural, so it cannot be the authority for whichever moment happens to be written; PROV-7 narrows PROV-4/PROV-6 and is about duplicates, not about whether a measured column may be a feature; CLEAN-22's heading is "Keep every relevant feature" and it excludes columns for what they are (a leak, an identifier, a copy, the measurement that defines the label) — a Daphnia 48-h EC50 is none of those. The critic is right on all three; the advocate's reading would make the declared moment prove itself.

**Decision needed.** (a) Screening point: narrow `use_case` and `known` (drop "and to fill a registration dossier"), say the substance has not been tested on any trophic level, and add half a sentence on why the co-endpoints are not inputs — no data change. (b) Dossier point: keep the wording and ship `pEC50 - DAPHNIA` and `pEC50 - ALGA` as two numeric features, missing where absent (USE-7 keeps them missing), with the 55.6% coverage named in `fit_reason`. The panel's preferences: advocate and column-auditor (a), practitioner (b), critic and split-auditor neutral on which, insistent that the folder not ship between them.

**Issue 2 — Metric origin: `fallback` or `source`? (P6, MET-5 Should, MET-11 Must; no re-scoring either way)**

**Problem.** The recorded reason is false and is being rewritten (change 4). What remains is the origin field. `rmse` ships either way.

**Each side's best evidence.** For `source` (advocate): p. 660 names one deliberate criterion the authors select models by — "Cross-validated determination coefficient was selected as fitness function" — which is MET-5's own wording ("the criterion it ranks, tunes or selects models by") and the shape of the `open_soil_spectral_library` precedent (tunes by RMSE, grades by CCC with RPIQ: the tuning criterion kept). For `fallback` (builder, critic): p. 661 reports r² and RMSE side by side with no criterion named for the task, which is MET-5's "no unique original: declare the fallback"; `qsar_fish_toxicity` ships `rmse` as the fallback on the same target.

**What would settle it.** MET-11 lets `rmse` stand for the source's criterion only "by identity". R² = 1 − MSE/Var(y) ranks every pair of models exactly as RMSE does on a fixed test fold; a squared Pearson r does not. The formula the authors used is in **Table S5 of the Supporting Information**, which the thesis copy does not reproduce and the publisher gates — the one thing in this review I could not reach. **Recommendation:** origin `source`, with "cross-validated determination coefficient (the GA's fitness function)" as the original and the R²/RMSE identity stated in `definition`, plus a line that Table S5 is unread; keep `fallback` if the curator prefers not to assert an identity on an unread formula. **Decision needed:** `source` or `fallback`.

**4. Agreed facts**

**Settled between the sides, and checked where it mattered.**

* **Source and frame.** One Zenodo file, `MergedEndpoints.sdf`, 6,325,348 bytes at the pinned md5/sha256, one version, 3,680 records that all parse; fish 2,200, Daphnia 2,120, algae 1,440. Shipped: 2,183 chemicals (2,186 after the repair), one feature. `feature_columns(container) == ['SMILES']`; `scaffold` is the group column and never reaches a model. `dataset check`: 0 errors, 0 warnings, **no accepted warnings and no `Potential leak, kept on purpose:` notes** in the definition.
* **Target.** `pLC50 - FISH` + 3 = −log10(mol/L), verified three independent ways: against −log10(mg/L ÷ MW) (median 0.00027), against the sibling's scale (r 0.995 on 805 shared chemicals), and now against the article's own sentence that the published values are in mMol/L. Range 0.600–9.508, tails chemically sound.
* **Copies.** 14 substances drawn twice, all removed; on the shipped rows **0** duplicates under six keys (canonical SMILES, full InChIKey, InChIKey skeleton, tautomer-canonical, neutralised, CAS digits; plus 0 ECFP4-identical-and-same-target). 0 group overlap across all 30 splits.
* **Split.** `L-FAMILY.key`, Bemis-Murcko, 1,761 groups, 587 test groups per fold, 669–794 test rows; group id in training 0% (22.6% at random), actual scaffold shared 60.9% (83.3%), close analogs at Tanimoto 0.7 12.1% (14.0%). Removing *every* close analog moves RMSE by 0.008 — less than the fold spread; the 146 Tanimoto-1.0 pairs are alkyl homologs whose targets differ by 0.66 log in the median. 60.7% of rows are singleton groups by SPLIT-31's own rule (676 ring-less, 649 bare benzene at 29.7%).
* **Worth benchmarking.** LightGBM 0.715–0.722, random forest 0.767, selected linear 0.954, dummy 1.281; beats the dummy on 30 of 30 folds; methods separate on the 1,378 chemicals this set adds (0.766 against 0.822). No task-probe flag; 2,183 rows in 1,761 groups is far from `Too Small`.
* **The label's ceiling.** The paper's Figure 3: inter-database agreement on the fish endpoint RMSE 0.55–0.67. The source's own fish models: 5-fold-CV RMSE 0.60/0.73 on a stratified random split, external 0.56/0.61 over the 65–66% inside the applicability domain.
* **The target's meaning.** Against ADORE's ECOTOX cut: where a fathead-minnow value exists (801 compounds) this value is that value (median 0.001, r 0.991, 87.6% within 0.1); where another fish species only (481), it follows that species; where both (325), closer to the fathead minnow on 263. Not circular: on compounds whose `DB` names neither ECOTOX nor EPAFHM the agreement is as good (86.9% within 0.1, r 0.996). Interspecies scatter is of the order of the model's error (fathead vs rainbow trout r 0.927, 67.7% within 0.5 log).
* **Co-endpoints.** Present on 47.1% (Daphnia) and 31.4% (algae); values worth −0.031 RMSE overall and −0.081 on the rows that carry one; **presence alone worth −0.0013 (not above noise)** — mine.
* **The article is open**, and I read it: pp. 658, 660, 661 of the journal, reproduced verbatim in the author's thesis at the Unistra deposit. The deposit's fish column (2,200) exceeds the modelled fish subset (2,110) by 90.
* **Registry (PubChem, 2026-11-25):** azulene C10H8; dithianon C14H4N2O2S2 (MW 296.3); difethialone C31H23BrO2S (MW 539.5).

**Task-gamer exploits, mapped**

The kit attack found **no exploit above its ±0.0005 noise floor** — not from string formats, row order, copies across the split, kNN read-across, transductive statistics, count or percentile encodings, the target's quantisation lattice, or the mg/L reparametrisation. That is a result, and it is the answer to LEAK-1, LEAK-19 and LEAK-30.

| Gamer item | Rule | Kept-on-purpose note / accepted warning | New or known | Issue? |
|---|---|---|---|---|
| F1 — the benzene carve-out leaves 61% of rows as singletons, so the regime is not the one the task card promises (0.7217 kit / 0.7519 true-Murcko / 0.7047 random) | SPLIT-31 (mandates the carve-out, word for word), SPLIT-4 and SPLIT-30 (the gap size never decides), SPLIT-37 step 5 (the line must say what the split leaves) | none exist | the **mechanism is disclosed** in `splits_comment`'s second paragraph; the **headline sentence contradicts it** and the measured consequence is absent | yes, as wording only (change 5). **Not** a re-split: the proposed fix — one 649-member benzene group — is what SPLIT-31 forbids, and the only argument for it is the score gap, which SPLIT-4 bars |
| F2 — 307 target values carry 1–2 ULP of float residue | CLEAN-16 | none | **new** | yes, trivially: `round(3)` (change 7). Not exploitable — the gamer discards it himself, since it exists only for rows whose label you already hold |
| Lookup of the published Zenodo file (RMSE 0.000) | none | n/a | known and universal to public data | no |
| `DB` "costs nothing measurable" | LEAK-1, CLEAN-22, EV-1 | a disclosure in `curation_comments`, not a kept leak | **known, but the stated gain is wrong**: 0.0045 RMSE on 25 of 30 folds, p 1.5e-5 | yes, wording only (change 9); the column is dropped whatever it scores |

**One panel finding settled against its author.** The blind reviewer's headline ("not a tabular task, R² −0.003; ship 208 descriptor columns, else exclude") rests on a harness that feeds `SMILES` to a model as a categorical string. CLEAN-24 (Should, amended 2026-11-01, Lennart) says the structure ships as a SMILES column marked as a structure, **never pre-encoded**, and the benchmark encodes it; the definition declares `Smiles(column="SMILES")`, and the same measurement under the real pipeline is RMSE 0.715–0.722 / R² 0.67–0.69, which the blind reviewer itself reproduced once it computed descriptors and listed under "what I could not check". EV-1 and EV-2: a measurement under the real pipeline beats one under an assumed pipeline. Its points 2 (`scaffold` is a feature) and 4 (the +3 shift undocumented) fall the same way. Its points 3 and 6 are the gamer's F1 and F2, already handled. The advocate called CLEAN-24 a Must; it is a Should — which changes nothing here, since no fact sets this case apart and five shipped siblings do the same.

**And one marker settled against two agents.** No `Selection Bias` marker. `selection.md`'s "No marker when" list names this family in its own words — "tested compounds stand for the candidates a screen would test (the QSAR sets): how far a new candidate lies from the tested ones is a question for the split" — which covers the industrial-inventory gap; and its first bullet ("the selection is how the label comes to exist") covers the substances with no effect up to water solubility, which carry no number in any dataset of this task and which the source explicitly excluded (p. 658). None of the five QSAR siblings carries the marker. The gap is disclosed in `fit_reason` instead (change 11). If the curator wants the marker, it belongs to the family, not to this folder.

**5. Consistency with precedent**

I take the precedent-checker's report as the frame; its five findings end as follows.

* **F1 `Time: Lost`** — a departure from SPLIT-32 and six sibling records with no distinguishing fact. Corrected (change 6), as the advocate concedes and the critic asks. Following precedent, so no question for the curator.
* **F2 the skipped repair rung** — confirmed, and I went one step further than any panel agent: the registry resolves **all three** pairs, not two, so the precedent of `qsar_bioconcentration` (six rows repaired from Wikidata/PubChem, rows dropped only where no partner could repair them) is followed exactly, and the row count is 2,186 (change 1). This is the one place where my recommendation departs from a phase-A report (the column-auditor's "not resolvable from the registry number alone" for CAS 104653-34-1); the fact that sets it apart is the PubChem record I queried.
* **F3 `fit="direct"`** — kept, and no longer a borderline call. The precedents the checker put against it (`drug_induced_autoimmunity_prediction`, `diabetes_3`, `mobile_churn`) all rest on a label definition that is *undocumented and cannot be checked*; here it is documented in the source's own text and verified (change 2), so USE-5's approximate clause and USE-8's "unverified label definition" ground both fall away. The closest precedent on the split distance is `qsar_fish_toxicity` (direct, same endpoint, same curator, 2026-11-12, 12.4% against 13.1%, against this set's 12.1% against 14.0%). The family's open USE-8 row for `qsar_fish_toxicity` / `qsar_aquatic_toxicity` is still marked `proposed`; if the curator wants direct-vs-approximate reopened for the QSAR family, that row is where it belongs, not this folder.
* **F4 the two sibling citations in `splits_comment`** — confirmed and corrected, including the fact the comment smooths over: at 14.0% → 12.1% this set removes less overlap than any molecule dataset in `molecules.md`'s scaffold table (change 5).
* **F5 ask the curator for the PDF** — moot. The article is open; the ask becomes a cited route.

No drift flag and no third exception on any rule in play. The one precedent this build does **not** follow is `Time: Lost`, and it is being corrected rather than excused.

</details>

<details><summary>Claim audit</summary>

**Claim audit — `aquatic_toxicity_lunghini_consensus`**

Everything below was measured on the raw file and the definition's own frame and splits, or read in the source's own text. **The decisive result of this audit is that the companion article is reachable and I read it**, which refutes three of the definition's own claims.

**The article is open access**

The paywall claim fails. `https://theses.fr/2020STRAF016/document` redirects to `https://publication-theses.unistra.fr/public/theses_doctorat/2020/Lunghini_Filippo_2020_ED222.pdf` (49 MB, HTTP 200). Lunghini's thesis reproduces the published article verbatim as thesis pages 98–118 = journal pages 658–675. I read pages 658, 659, 660, 661, 662 and 666 as images myself; every quotation below is my own transcription from those pages, not a report of someone else's reading. (HAL's `tel-03505818` serves an anti-bot page — that is the route that failed before.)

**Claims table**

| # | Claim (exact) | Where | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | "3,680 compounds, each with at least one of three endpoints"; fish 2,200 / Daphnia 2,120 / algae 1,440; 984 / 531 / 501 / 184 | `curation_comments` | parse SDF, count | **holds** | 3,680 rows; 2,200 / 2,120 / 1,440; 984, 531, 501, 184 exactly | — |
| 2 | target = `pLC50 - FISH` + 3; median \|diff\| 0.0003 vs −log10(mg/L ÷ MW); −log10(mol/L) differs by exactly 3 | `curation_comments`, `MMOL_TO_MOL` | recompute over 2,199 | **holds** | median 0.000268; −log10(mol/L) median diff 3.000 | MET-3 |
| 3 | mg/L and pLC50 differ >0.3 log on 34 of 2,199, at most 1.19; one fish compound has no mg/L | `curation_comments`, Decision 2 | recompute; test "a wrong MW explains it" | **holds**, alternative refuted | 34; max 1.1857; CdId 3160. RDKit MW reproduces the same 34; implied MW ratios 0.065–6.8, so the columns genuinely disagree | CLEAN-1 |
| 4 | no censoring at a reporting limit (LEAK-22) | `curation_comments` | value pile-up vs near-round control | **holds, now with a primary source** | 1.68 % of fish rows at a round mg/L; only 11 at 100, 1 at 1,000. The article (p. 658): "the value must be precisely determined (i.e. values reported as ranges were excluded)" and compounds above measured water solubility were excluded | LEAK-22 |
| 5 | ADORE: 801 fathead compounds, median 0.001, 87.6 % within 0.1, r 0.991; 481 other-species, 0.082, r 0.952; 325 both → 263/60 | `curation_comments` | rebuild from `ecotox_mortality_processed.csv` | **holds exactly** | 801 / 0.001 / 87.6 % / 0.991; 481 / 0.082 / 0.952; 263 / 60 / 2 ties | EV-1 |
| 5b | (my attack) the ADORE agreement is circular because ECOTOX is a source | — | split by whether `DB` names ECOTOX/EPAFHM | **attack fails** | non-ECOTOX compounds (n 236): 86.9 % within 0.1, r 0.996 — as good as the ECOTOX ones (88.0 %, r 0.989) | EV-1 |
| 6 | fathead vs rainbow trout r 0.926, 68 % within 0.5 | `curation_comments` | recompute | **holds** | r 0.927, 67.7 % | — |
| 7 | 1,328 fish compounds name ≥2 databases, up to eight; ten DB names with those counts; 77 bracketed | `curation_comments` | count after stripping `(n)` | **holds exactly** | 1,328; max 8; all ten counts match; 77 rows, brackets 10–78 | — |
| 8 | 14 substances drawn twice, 28 rows; skeleton finds 8, CAS 12; spread ≤0.151, median 0.002; 11 share a formula (tautomers), 3 do not → 2,183 | `curation_comments`, Decision 1 | re-run the key, inspect all 14 pairs | **holds exactly, pair by pair** | 14 / 28 / 8 / 12 / 0.151 / 0.002; all 11 kept pairs are genuine tautomer drawings (azo↔hydrazone, pyridinone↔hydroxypyridine, guanidine, imidacloprid…) | LEAK-19 |
| 9 | all 3,680 parse, no `.`, no stereochemistry | `curation_comments` | regex + RDKit | **holds, and explained** | 0 and 0. Article p. 658: standardisation did "removal of salts/solvents … removal of stereo information" | LEAK-18 |
| 10 | 1,761 groups / 2,183 rows; 587 test groups per fold; 1,651 singletons (676 ringless, 649 benzene 29.7 %, 326 lone); 110 groups of 2–46 | `splits_comment` | rebuild splits | **holds exactly** | every number reproduced; 0 groups on both sides of any of the 30 folds | SPLIT-31 |
| 11 | 0 % of test scaffolds in training vs 22.3 % random; 12.1 % vs 13.5 % at Tanimoto ≥0.7; median nearest 0.489 vs 0.505 | `splits_comment` | recompute + random control | **holds** | 0.0 % vs 22.4 %; 12.2 % vs 14.3 %; 0.4875 vs 0.5075 | SPLIT-30 |
| 12 | (unwritten) no row is a copy across the split | implied | 146 Tanimoto-1.0 pairs; near-copy rate | **holds** | the Tanimoto-1.0 pairs are alkyl homologs (median \|Δy\| 0.664, 4 % within 0.05). t ≥ 0.9 & \|Δy\| < 0.1: 0.53 % of test rows, vs 0.63 % under random splits. One pair at t ≥ 0.8 & \|Δy\| < 0.005 (pentanal/hexanal) | LEAK-19 |
| 13 | (unwritten) every feature is known at the prediction point | implied | `feature_columns(container)` | **holds** | `['SMILES']`; `scaffold` is the group, `DB`/mg/L/`endpoint` dropped | LEAK-1 |
| 14 | row order is alphabetical, one of 3,680 out of order | `curation_comments` | adjacent inversions | **holds** | 1 inversion in 3,679 | — |
| 15 | metric computable on every fold | `metric`, README | score a dummy on all 30 folds | **holds** | unit = row, 669–794 rows per test fold; no scoring columns, no weight; dummy rmse 1.2103–1.3802 (mean 1.2805) | MET-2 |
| 16 | target on the sibling's scale | `MMOL_TO_MOL`, metric reason | join on flat SMILES | **holds** | `qsar_fish_toxicity` ships `LC50[-LOG(mol/L)]`; r 0.9951, median \|d\| 0.0010 on 805 shared chemicals | MET-3 |
| 17 | the source split at random | `curation_comments` | read p. 659 | **holds, more precisely** | "training and test sets were obtained by stratified (based on toxicity values) random splitting 70% and 30%" | SPLIT-5 |
| 18 | **"How several experimental values became one value is not documented (EV-2) … the companion article's full text is not reachable from here"** | `curation_comments`, `fit_reason`, "Not read" bullet | find the article | **REFUTED** | p. 658: "In case of multiple values per compound, **the median was taken as a representative value. When the ratio between the minimum and the maximum reported value per compound was >10, the entry was discarded.**" Plus: OECD-recommended species only, larval-stage studies discarded, above-solubility and water-unstable compounds excluded | EV-2, PROV-17, USE-5 |
| 19 | **metric reason: "its evaluation section is behind a paywall and could not be read, so no ranked criterion of the source was found"** | `Metric.fallback(reason=…)` | read pp. 660–661 | **REFUTED** | p. 660: "**Cross-validated determination coefficient was selected as fitness function**" (descriptor spaces + SVM hyperparameters). p. 661: "To evaluate the models' performance the *r²* determination coefficient and the RMSE parameters are reported" | MET-1, MET-11 |
| 20 | **"holds 808 of those 908 (89.0 % …, 793 by CAS-RN) … 571 of the 808 within 0.01 … adds 1,392 chemicals"** | `curation_comments` | join on the **shipped** 2,183 | **REFUTED as a statement about what we ship** | shipped: 805 of 908 (88.7 %), 783 by CAS, 568 within 0.01, **adds 1,378**. The quoted numbers are the 2,200-row pre-dedup subset | EV-2 |
| 21 | **"Dropping it costs nothing measurable … 0.713 against 0.717, a difference inside the 0.025 spread over folds"** | `curation_comments` | paired LightGBM over all 30 folds | **numbers hold, framing refuted** | 0.7150 vs 0.7106; paired Δ −0.0045 ± 0.0047, DB helps on **25 of 30** folds, p 1.5e-5. Small but systematic, not noise | LEAK-1, EV-1 |
| 22 | "merged from ten public toxicity databases" | `task_summary.row` | inspect the ten names | **imprecise** | one of the ten is "Literature set" (articles, per Zenodo and p. 658), and "ECOTOX-EPA" (49) is plausibly ECOTOX again | — |
| 23 | "the most frequent value in mg/L is 13 (12 compounds)" | `curation_comments` | value counts | **imprecise** | tied: 13, 1.4 and 1.5 each on 12. Conclusion unaffected | — |
| 24 | ADORE "another fish species" | `curation_comments` | check `tax_group` | **imprecise, conservative** | 5,737 of the 22,919 non-fathead 96-h LC50 rows are crustacea/algae. Fish only: median 0.059, 61.0 % within 0.1 (better than the quoted 0.082 / 54.3 %) | EV-2 |
| 25 | record's screening block: "nine sources … ECHA 1,791, ECOTOX 1,089"; "1,339 … two or more"; "766 compounds, r 0.991"; "ridge 0.788" | record, `**Screening (AI, 2026-11-25)**` | recount | **REFUTED (superseded)** | ten names, ECHA 1,805, ECOTOX 1,114, + ECOTOX-EPA 51 (the block counted `ECHA(10)` as its own name); 1,328; 801. Ridge on the shipped encoding gives 1.53, the probes' linear model 0.954 — 0.788 is not reproducible. The **definition's** numbers are the correct ones | EV-2 |
| 26 | accepted warnings | README `accepted: {}` | `dataset check` output | **holds** | 0 errors, 0 warnings, nothing accepted | — |
| 27 | SD-file parser reads every field correctly | implied by `_read_sd_fields` | count `>  <TAG>` lines in the file | **holds** | tag counts match the parsed counts exactly (fish 2,200, mg/L fish 2,199, `Molecular weight` 3,679); no odd tag shapes, no multi-line value, no CRLF | — |

**New facts from the primary document (not claims, but they change the review)**

* **The label's own noise floor.** Figure 3 (p. 662), which I read: on the fish endpoint, inter-database agreement is ECHA↔ECOTOX RMSE 0.64 (n 7,515), ECHA↔Literature 0.55 (n 1,312), ECOTOX↔Literature 0.67 (n 7,916). Our untuned LightGBM is at 0.715 on grouped splits against a dummy of 1.281 — i.e. **the model is already within ~0.05–0.16 RMSE of the measurement noise between the sources the target is merged from.** The signal is real and the methods separate (TP-2 unaffected), but the curator should know how much headroom the benchmark is measuring.
* **The source's own fish scores** (Table 4, p. 666, read): 5-fold-CV RMSE 0.60 (ECHA model) and 0.73 (All-Public) on a *stratified random* split; external test 0.56 / 0.61 but only over the 65–66 % of compounds inside the applicability domain. Our 0.715 at full coverage on a harder split is in the same band.
* **The deposit is not exactly the modelled set.** p. 658 and Table 2: the modelled subsets are algae 1,440, Daphnia 2,120, **fish 2,110** (1,450 train + 660 test). The deposited file carries algae 1,440 ✓, Daphnia 2,120 ✓, **fish 2,200** — 90 unexplained extra. (The target range matches exactly: Table 2 gives −2.4 to 6.51, the file gives −2.40 to 6.51.)
* **The abstract's "RMSE_ext = 0.56–0.78" is the 5-fold-CV column, not the external-test column** (which is 0.43–0.65). The metric `reason` quotes it as the article's headline; the quote is accurate, the subscript is the paper's own error.

---

**Refuted, ranked**

**1. (P6, MET-1 + MET-11, Must) The metric's reason asserts something false, and the look-before-falling-back was incomplete.** — claim 19.
*What it changes:* MET-1 requires looking at "the paper that defined the task … and record where you looked"; the recorded answer ("behind a paywall and could not be read") is wrong, and a deliberate selection criterion exists: the cross-validated determination coefficient used as the GA fitness function. MET-5's precedent `open_soil_spectral_library` ("tunes and cross-validates by RMSE … the tuning criterion kept") points at treating a named tuning criterion as the source's metric. The declared metric itself most likely does not move: on a fixed test fold R² = 1 − MSE/Var(y) ranks every pair of models exactly as RMSE does, so `rmse` is either the source metric by identity (MET-11 `source`) or the fallback under MET-5's "r² and RMSE reported side by side" reading.
*Mildest remedy:* rewrite the `reason` from the article (quote p. 660 and p. 661, cite the open route), and put one curator call in the review: keep origin `fallback`, or move to `source` with the cross-validated determination coefficient as `original` and the R²/RMSE identity in `definition`. No re-scoring either way.

**2. (P3/P5, USE-5 + EV-2 + PROV-17, Must) "The consensus merge is undocumented" is false — the rule is in the article.** — claim 18.
*What it changes:* the builder's issue A dissolves. The target is the **median** of the OECD-guideline-conforming values per compound, with any compound whose min/max ratio exceeded 10 discarded, ranges excluded, larval-stage studies discarded, and compounds above measured water solubility or unstable in water removed. This is a stronger basis for `fit="direct"` than the ADORE agreement was (USE-5's "undocumented *and cannot be checked*" clause is not even needed), it is independent confirmation of the LEAK-22 no-censoring finding, and it explains why the 14 tautomer pairs survived ("Duplicates were removed based on standardized SMILES matching"). It also sharpens claim 22's "pooled over the fish species": the species are restricted to the guideline's recommended list, not an open pool.
*Mildest remedy:* replace the "undocumented" bullet and the "Not read" bullet with the rule as quoted, fix `fit_reason`, and keep `fit="direct"`. Issue A can be closed rather than put to the curator.

**3. (P5, EV-2) The sibling-overlap figures describe 2,200 rows we do not ship.** — claim 20.
*What it changes:* a documented fact in the definition is wrong about the shipped dataset, and "adds 1,392" is quoted onward in the record and the hand-over. The direction of the PROV-4/PROV-6 argument is unchanged (805 shared, 1,378 added).
*Mildest remedy:* restate on the shipped frame — 805 of 908 (88.7 %), 783 by CAS-RN, r 0.995, median 0.0010, 568 within 0.01, adds 1,378 — or say "of the 2,200 before deduplication".

**4. (P5, PROV) The deposit carries 90 fish values more than the article's modelled fish subset.**
*What it changes:* the notes call the deposit "the collected public data of the companion article", which is right, but the fish column is not the set the paper modelled (2,110), while algae and Daphnia match it exactly. Nothing about our task breaks; it is a fact that belongs in the provenance note.
*Mildest remedy:* one line in `curation_comments` with the two numbers and that the gap is unexplained.

**5. (P7, writing) "Dropping `DB` costs nothing measurable".** — claim 21.
*What it changes:* nothing about the decision — `DB` is not known for an untested substance, so LEAK-1 drops it whatever it scores. Only the supporting sentence overstates: paired over the 30 shipped folds the flags are worth 0.0045 RMSE on 25 of 30 folds (p 1.5e-5).
*Mildest remedy:* "a small and consistent 0.005 RMSE, dropped under LEAK-1 regardless".

**6. (P7, writing) Three small inaccuracies.** — claims 22, 23, 24: "ten public toxicity databases" (one is a literature set, one is plausibly ECOTOX twice); "the most frequent value in mg/L is 13" (tied with 1.4 and 1.5); "another fish species" in the ADORE comparison includes 5,737 crustacean/algal rows (restricting to fish *improves* the figures to 0.059 / 61.0 %).
*Mildest remedy:* reword; optionally re-run the species comparison on `tax_group == "fish"` and quote the better numbers.

**7. (record only, superseded) The screening block of 2026-11-25 carries five numbers the definition's own measurements contradict.** — claim 25. The definition is right on all of them. *Mildest remedy:* none required in the folder; the review should say the screening block is superseded so its numbers are not quoted forward.

**Untested, and why**

* **Whether the paper's "determination coefficient" is 1 − MSE/Var or squared Pearson *r*.** The formulas are in Table S5 of the Supporting Information, which the thesis copy does not reproduce and the publisher gates. This decides whether `rmse` ranks models *identically* to the source's criterion (MET-11 `source` by identity) or only closely. It does not change which metric we would ship.
* **What the bracketed numbers in `DB` (`ECOTOX(76)`, 10–78, on 77 fish compounds) count.** The Data cleaning section does not mention them. `DB` does not ship, so nothing depends on it.
* **Why the deposit's fish column has 90 more compounds than the modelled set.** Not stated anywhere I could read.

**What I attacked and could not break**

Every count, every endpoint combination, the unit conversion and the +3 shift, all 14 copy pairs individually, the choice of the published pLC50 over mg/L (including the alternative explanation that a wrong molecular weight causes the 34 disagreements — refuted), the censoring check, the ADORE species comparison *including its independence from ECOTOX*, every splits_comment number, the no-copy-across-the-split claim, the SD-file parser, `feature_columns == ['SMILES']`, and the metric's computability on all 30 folds. The shipped data is what the definition says it is; the failures are in what the definition says about the **source**, and they all trace to one cause — the article was declared unreadable when it is open access.

</details>

<details><summary>Column audit</summary>

**Column audit — `aquatic_toxicity_lunghini_consensus`**


**The files of the release — clean**

Zenodo concept 10.5281/zenodo.3708081 has **exactly one version** (`/api/records/3708082/versions`, `total: 1`, `is_last: true`) holding **one file**, `MergedEndpoints.sdf`, 6,325,348 bytes, md5 `41273814…`. That is the file `_load_raw` reads, at the byte size and md5 the definition pins. Nothing is left out, so there is no g_research-style missing supplement here.

The deposit's description (verbatim from the API) defines every field and confirms the readings in the definition: fish = "the log median lethal concentration measured at 96 hours", Daphnia 48 h, algae 72 h, `DB` = "source of the data, 'Litterature set' means that the data is originated from an article". It explains nothing about the merge rule — the builder's PROV-17 note is right.

**The parser — verified independently**

`_read_sd_fields` is hand-rolled, so I re-read the file with RDKit's `SDMolSupplier` and compared all 14 fields on all 3,680 records: **0 differing values** (the only diffs are RDKit's float formatting of `1.8E-4`). 3,680 blocks, 40,958 field headers all in the one `>  <NAME>` form, **0 multi-line field values**, 0 connection tables that fail to parse. The parser loses nothing.

**The cleaned frame (3 columns)**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `SMILES` | the chemical's 2D structure, RDKit-canonical form of the deposit's `SMILES_Canonical` | **yes** — the structure is all that exists for an untested substance | `string`, declared `Smiles(column="SMILES")` in `special_features`, so the benchmark encodes it as a structure. All 2,183 parse; 2,183 distinct; no `.` (no salts/mixtures); no stereochemistry and no isotope anywhere in the *published* field either, so nothing was stripped; 35 rows (1.6%) are cations drawn without their counter-ion, as published | fine | CLEAN-24, CLEAN-9 |
| `LC50` | the fish 96-hour median lethal concentration as −log10(mol/L) = published `pLC50 - FISH` + 3 | **n/a (target)** | `float64`, 2,183 values, no missing, 0.600–9.508, 1,704 distinct. `+3` verified row by row (`pLC50+3 == target`, exact); the mmol reading verified against the mg/L column (median |gap| 0.00027 log). Tails chemically sound: most toxic are pyrethroids (tefluthrin 9.508 = 0.13 µg/L), least toxic are water-miscible glycols/amides at g/L — no impossible value to blank (CLEAN-11) | fine, with one note (finding 1) | CLEAN-15, CLEAN-16 |
| `scaffold` | the Bemis-Murcko scaffold, or `single: <SMILES>` for a ring-less chemical or one of a scaffold above a tenth | group column, not a model input | `string`, 1,761 levels; `feature_cols == ('SMILES',)`, so it never reaches a model; derived from the feature, so it adds no information even where a validation split reads it | fine | SPLIT-31, CLEAN-3 |

Temporal checks (step 4 of my brief: missing share and level by period, `splits_feature_missing_in_test`) **do not apply**: the task is grouped, there is no time column, and the frame has no missing value at all.

The dtype probe is vacuous here by construction (`columns: 0` — the one feature is special-typed, the target and the group are excluded). I re-derived it: there is no count typed categorical and no code typed numeric to find, and no ordinal scale.

**What left the raw table, field by field**

| raw field | meaning | known at the prediction point? | disposition | verdict |
|---|---|---|---|---|
| `CdId` | the record's number in the file | yes, but meaningless | dropped | correct (CLEAN-3) |
| `CASRN` | CAS registry number | yes for a registered substance | dropped; used only as a dedup key | correct — a near-identifier that would allow a lookup; 280 of 2,183 are written without dashes (`94677` = 94-67-7, `50293` = DDT), which the key's digit-stripping handles |
| `Formula`, `Mol Weight`, `Molecular weight` | formula and MW | yes | dropped | correct (CLEAN-24: computed from the structure). I checked they really are: RDKit MW from the SMILES matches `Mol Weight` to ≤0.04 on all 2,200 fish rows, and the 35 `Formula` mismatches are only the omitted charge on cations |
| `DB` | the source databases | **no** — unknown for an untested substance | dropped | correct (LEAK-1, CLEAN-22). My measurement on the 30 shipped splits: DB flags + count alone RMSE **1.230** vs dummy **1.281** (builder: 1.225) |
| `endpoint` | which of the three endpoints the compound carries | **no** — a record of the collection | dropped | correct. Fully redundant with value presence (0 inconsistencies), and numerically empty anyway: **1.269** vs dummy 1.281 |
| `pEC50/mg/L - DAPHNIA`, `pEC50/mg/L - ALGA` | the other two organisms' values | **no** at the declared prediction point (other tests, and present on only 47%/31% of rows) | dropped | correct, but see question 4: r = 0.79 (Daphnia) and 0.78 (algae) with the target; the two together reach RMSE **1.064** alone |
| `mg/L - FISH` | the target in mg/L | n/a | dropped | correct (the target in another unit). I confirmed the disagreements are **not** an MW/salt mismatch: on all 34 rows that differ by >0.3 log the file's MW equals the RDKit MW of the drawn structure, so one of the two reported numbers is simply wrong, and the builder's independent-value test decides it (spot check: ethylbenzene, pLC50 → 12.0 mg/L, the published literature value; the mg/L column says 82) |

**Copies — nothing left (LEAK-17/19)**

I attacked the dedup with four keys the builder did not all use. On the 2,183 shipped rows: **0** duplicate InChIKey skeletons, **0** duplicate full InChIKeys, **0** rows sharing an RDKit canonical tautomer (`TautomerEnumerator`), **0** rows sharing a neutralized structure, **0** rows sharing a CAS digit string, **0** ECFP4-identical *and* same-target pairs. The 14 substance components are all of size 2 (no accidental chaining into triples), and each pair is corroborated by both keys or by an identical formula plus a target spread ≤0.151. The 22 pairs that share a molecular formula and a target within 0.005 log are genuine isomer pairs (p-tert-butylphenol vs 4-n-butylphenol, 2,4- vs 2,5-dichloronitrobenzene), not copies.

---

**Findings, ranked**

**1. The censoring check (LEAK-22) is weaker than the note claims — 11 compounds sit exactly on the OECD 203 limit concentration (P4/P7, low)**

`curation_comments` says: "No sign that the values are censored at a reporting limit … the most frequent value in mg/L is 13 (12 compounds), 100 mg/L appears on 11 … no more than the other round values." The count is right, the comparison is not: 13 mg/L sits in the densest part of the distribution, 100 mg/L does not.

**Evidence (mine, on the 2,183 shipped rows).** Exactly 100.000 mg/L: 11 compounds, against 45 others spread over the whole ±10% band \[90, 110\] — 20% of the band at a single value. The same test one decade down: 10.000 mg/L holds 6 of the 67 compounds in \[9, 11\] (9%). 100 mg/L is the OECD 203 limit-test concentration, and a dossier that runs it reports "LC50 (96 h) > 100 mg/L"; **9 of those 11 come from `ECHA`, `NITE` or `Literature set`** (7 from ECHA alone, where ECHA is on 39% of the fish set) — the dossier sources where that outcome is standard. 1,000 mg/L appears once and 500 never, so if ">" values entered, they entered at 100.

I could not settle it: the file ships no operator column, and the copy of ECOTOX available here (ADORE's extract) has already removed every censored entry (0 rows with a `>` operator among 25,734 96-h LC50 results), so there is nothing to match against.

**Mildest remedy:** no data change — 11 of 2,183 is 0.5%, and dropping them would discard values that may be real. Replace the "no sign that the values are censored" sentence with what the check actually found (the spike at the limit concentration, its sources, and that the source ships no operator), so a user of the benchmark knows the target's least-toxic end may hold a few limit-test values. A `Decision` entry if the curator wants it visible in the README.

**2. For 2 of the 3 dropped "disagreeing drawing" pairs the CAS-RN does say which drawing is meant (issue C, P7, low)**

Issue C's option C4 drops **both** rows of the 3 pairs whose two drawings differ in molecular formula, on the ground that "nothing in the file says which is meant". The file does say, through a field it already carries:

* CAS **275-51-4** is azulene, C10H8 — so `c1ccc2cccc-2cc1` is the substance and the C10H18 row (decahydroazulene) is the wrong drawing; the two targets are 4.154 and 4.168, one measurement.
* CAS **3347-22-6** is dithianon, C14H4N2O2S2 (MW 296.3, which is the `Mol Weight` the file carries on that row) — so the C14H6N2O2S2 row is the wrong drawing; both targets are 6.254, one measurement.
* The third, CAS 104653-34-1 (C31H25BrO2S against C31H23BrO2S), I could not resolve from the registry number alone.

**Mildest remedy:** a "C5" on issue C — keep the drawing whose formula matches the registry where the registry settles it, drop both rows otherwise (2,185 rows instead of 2,183). Worth 2 chemicals of 2,183, so leaving C4 as it stands is defensible; what should change either way is the note's wording, since the claim "the file does not say which is meant" is not true of the CAS-RN, which is in the file.

**3. The target column is named `LC50` but holds −log10(mol/L), and the source names it `pLC50` (P7, low — question for the curator)**

The deposit's field is `pLC50 - FISH`; the shipped column is `LC50` with values 0.600–9.508 and no unit. CLEAN-16's `open_soil_spectral_library` precedent renamed a target because "the blind reviewer took them for something other than percent", which is the same failure mode (a reader can take 4.32 for mg/L).

**Against renaming:** the two shipped siblings on exactly this scale, `qsar_fish_toxicity` and `qsar_aquatic_toxicity`, both ship `target = "LC50"`, and `qsar_fish_toxicity` takes the name from its source's own column `LC50[-LOG(mol/L)]`. `task_summary.predicted` here says "as minus the log of moles per litre".

**Recommendation:** keep `LC50` for family consistency (the mildest remedy is no change), and raise it only if the curator wants the whole family renamed at once. I log it so the decision is deliberate rather than inherited.

**4. Question: the Daphnia and algae values are dropped as other tests — right at the declared prediction point, worth one line in the notes (P3, low)**

They are out by LEAK-1 as the definition declares the moment ("a substance before it is tested on fish"), and the house already treats the three endpoints as three tasks (PROV-7). But a real hazard assessor often holds the 48-hour Daphnia EC50 *before* commissioning the 96-hour fish test, which is a USE-6 reading and would make this a different, mixed-input task.

**Measured, 30 shipped splits:** Daphnia + algae alone RMSE **1.064** (dummy 1.281), against **0.715** for the structure — so they would not trivialize the task, but they are present on only 1,029 and 685 of 2,183 rows, and that presence is itself a record of what the collection happened to cover (its own selection signal: mean target 4.63 for `daphnia, fish` against 4.08 for `alga, fish`).

**Recommendation:** ship as defined; add half a sentence to the bullet that drops them saying why the assessor's possible Daphnia value is not an input here (the prediction point is before any aquatic test on this substance, and the endpoint's presence is a record of the collection), so the omission reads as a decision rather than an oversight.

---

**Checked and clean, for the record**

* `pLC50 + 3 == LC50` on every row; the mmol reading is confirmed by the mg/L column, not just asserted.
* No missing value anywhere in the frame; `_feature_types()` correctly empty.
* The one fish compound with no mg/L and no `Molecular weight` (CAS 3347-22-6) is already dropped by the copy rule, so no row ships with a half-filled target basis.
* `Mol Weight` and `Molecular weight` differ on 98 rows (≤1.02); both are dropped, so it costs nothing.
* 35 shipped structures (1.6%) are cations drawn without a counter-ion; the source's mg/L→molar conversion uses that ion's MW, so the file is internally consistent. As published; no action.
* Row order: the file is alphabetical by SMILES, the base class shuffles — the `order_drift` flag is explained and the explanation holds.

</details>

<details><summary>Split audit</summary>

**Split audit — `aquatic_toxicity_lunghini_consensus`**

**Verdict: right, with notes.** The leaf the tree gives is the leaf the definition names and the split it ships. Every finding below is wording or disclosure on a correct split; none asks for a re-split, a gap or a filter.

---

**1. The tree, walked from the record's collection type (SPLIT-36)**

Collection type on the record: `Expanding Science Catalogue` (+ `Samples: Over Time`, `Time: Lost`). Right type — the file is a 2020 cut of nine public toxicity databases that keep growing (ECHA, ECOTOX, VEGA, OASIS, NITE, EPAFHM, EFSA, Aquatic ECETOC, a literature set), not a designed experiment.

| Question | My answer | From what |
|---|---|---|
| `[CAT.next-items]` Does the use case predict for the items the catalogue adds next? | **no** — items like those it contains, and items from elsewhere (an industrial inventory) | The abstract, which the Zenodo description repeats verbatim (I fetched both today): "A benchmarking … on a set of compounds considered more representative and relevant for the chemical space of the current chemical industry"; "industrial data performances were noticeably lower than those on public data"; "final models were updated with the inclusion of new industrial compounds, extending applicability domain and relevance for application in an industrial context". Nothing aims at the next ECHA/ECOTOX entries. SPLIT-37 step 3. |
| → **Family-key step**, `[FAMILY.key]` Can the data compute a family key? | **yes** — the Bemis-Murcko scaffold of the shipped `SMILES` (SPLIT-31); enough-groups check passes: 1,761 groups over 2,183 rows, 587 test groups in every fold | measured below |

**Leaf: `L-FAMILY.key` — Grouped · `UnseenGroup` (the family key).**

The definition names `split_leaf = "L-FAMILY.key"`, declares `TimeBasis("UnseenGroup", …)`, ships `Grouping(on="scaffold", labels="per_sample", prediction_unit="row", context="none")` and carries `Non-IID (Grouped)` / `required_split: Grouped (NON-IID)`. **Leaf, split and tag agree.** No forced leaf, no unreached leaf, no question without a fitting answer.

**The leaf is robust to the one contestable answer.** If a reader answers `[CAT.next-items]` *yes* (the industrial aim could be read as reaching compounds not yet collected), the walk goes `[CAT.entry-date]` → a date is rebuildable from a parent source for part of the set (see finding 4) → `[CAT.arrival]` 4b. The sibling already measured that condition on 89% of these chemicals: `qsar_fish_toxicity`, forward by first ECOTOX test year, 7.2% close training analogs against 6.9% at random — no wave → *no* → **Family-key step → the same leaf**. Both readings land on `L-FAMILY.key`. I did not re-run the ECOTOX join (the bulk release is not in this worktree).

**Collection-type robustness:** read as `Experimental results` instead, `[EXP.meets]` = "a kind or family the data does not contain (a chemical series)" → `[EXP.kind-key]` yes → `L-EXP.kind`, Grouped · `UnseenGroup` (the kind). Same family, same column.

---

**2. Regime, and what I verified on the data**

All numbers from the definition's own `make_splits()` (loaded through `dataset_io`, 4 threads).

* **Regime.** Cold start, new entity: an assessor meets a substance never tested, with only its structure; `context="none"`, nothing known about a new group. One row per substance, so no entity recurs (USE-10; USE-11 does not apply). Declared regime matches.
* **Folds.** 10 repeats × 3 folds. 1,761 groups over 2,183 rows; 587 test groups per fold; test folds 669–794 rows, train 1,389–1,514 (63.6–69.4%). **Group overlap between train and test across all 30 splits: 0.**
* **SPLIT-33 repeats.** Groups do not each carry one label, so the unit is the scored unit = the row; train side 1,389–1,514 < 2,500 → 10 repeats. Correct.
* **Group id (SPLIT-24).** The Bemis-Murcko scaffold, computed by RDKit from the structure, never from the label — the family key SPLIT-37 step 2 and SPLIT-31 prescribe. Not a similarity cluster, not a hash. Deterministic and reproducible (I recomputed it independently: 676 ring-less, 649 bare benzene at 29.7%, next-largest pyridine 46 = 2.1%, so benzene is the only scaffold over the tenth).
* **Item key (SPLIT-37 step 1, LEAK-17/19) — the record's one open question, closed.** In the shipped frame: 2,183 rows, 2,183 distinct canonical SMILES, **0 rows sharing an InChIKey skeleton, 0 sharing a CAS-RN.** `_one_row_per_substance` removes all 14 doubled substances. No copy of one item sits on both sides.
* **Not temporal**, so the floor (SPLIT-14), the window count (SPLIT-15), the horizon and gap (SPLIT-12/SPLIT-10), late labels, training history and the three checks the 11-10/11 panels missed do not apply. The time probe's one flag and the entry-date question are findings 5 and 4.
* **Entity leakage (LEAK-42/43/44):** no unrecorded repeated unit to find — one measured value per substance, no order, no later record carrying an earlier label forward.

---

**3. What the split actually buys (my own measurement)**

Close training analog = a training chemical at Tanimoto ≥ 0.7, Morgan radius 2, 2,048 bits; 3 repeats of the shipped splits against 3 random 3-folds of the same rows.

| Test chemicals | n | shipped | random |
|---|---|---|---|
| all | 2,183 | **12.1%** | 14.0% |
| ring-less (own group by rule) | 676 | 21.7% | 21.6% |
| bare benzene (own group by rule) | 649 | 13.7% | 13.6% |
| **in a real multi-member scaffold** | 858 | **3.4%** | **8.3%** |

At Tanimoto ≥ 0.9: 4.9% shipped against 5.0% random. Same scaffold as a training chemical: 60.9% shipped against 83.3% random; same *group id*: 0% against 22.6%.

What that costs, untuned LightGBM on the recommended `encode_smiles` features, 9 folds each:

| Split | RMSE | close analogs |
|---|---|---|
| shipped scaffold groups | **0.722** | 12.1% |
| random 3-fold | 0.705 | 14.0% |
| single-linkage analog clusters at Tanimoto 0.7 (1,929 clusters; a *measurement*, not a proposal — SPLIT-24 bars a similarity cluster as a group id) | 0.714 | 0.0% |
| training mean | 1.280 | |

**Removing every close analog moves RMSE by 0.008 — less than the spread over folds.** The residual overlap is not worth a re-split, and the 146 Tanimoto-1.0 pairs are homologous chains ECFP4 cannot tell apart (n-alkanols, n-alkyl ketones) whose targets differ by 0.66 log in the median, so even an exact fingerprint match carries little of the label. The shipped split stands.

---

**4. Findings, ranked**

**1. The splits_comment states the opposite of what the split does (P4, SPLIT-37 step 5 / writing; Should)**

`splits_comment` and the generated README: *"no test chemical's scaffold is in training, against 22.3% under random splits"*.

Measured: **60.9% of test chemicals share their actual Bemis-Murcko scaffold with a training chemical** (83.3% at random). The 0% / 22.3% pair is the share whose **group id** is in training, not whose **scaffold** is — the two differ exactly because the rule makes the 676 ring-less and 649 bare-benzene chemicals (1,325 rows, **60.7% of the set**) groups of their own, which the same comment's first paragraph says. As written the two paragraphs contradict each other, and the sentence a curator reads to judge the split is the wrong one. `task_summary.split` has the same overstatement ("a test chemical belongs to a family the model has not seen"; it names the ring-less carve-out but not the 29.7% benzene one).

Rule: SPLIT-31 mandates the carve-out, so the split is right; SPLIT-37 step 5 and the house writing rule require the line to say what the split leaves. **Mildest remedy: reword** — name the group, give both figures (group id 0% / 22.6%; scaffold 60.9% / 83.3%), and name the benzene bucket in `task_summary.split`.

**2. Both sibling citations in that paragraph are wrong, and the corrected one cuts against the claim (P4; Should)**

The comment explains the small overall reduction with *"That is the pattern of the other datasets of this family … (qsar_fish_toxicity 7.2% against 6.9%, qsar_oral_toxicity 12.4% against 13.1%)"*.

* `qsar_fish_toxicity`'s own definition (CC 2026-11-12): **12.4% against 13.1%** on its shipped scaffold splits. The quoted "7.2% against 6.9%" is splits.md's *forward-by-year against random* pair for that dataset — a different measurement (its scaffold figure there is 5.9%).
* `qsar_oral_toxicity`'s own definition: **16.3% against 24.7%**; splits.md's SPLIT-37 table: scaffold 8.6% against random 13.1%. Either way its scaffold split removes about a third of the close analogs, so it is **not** an instance of the claimed pattern. The figures attributed to it are `qsar_fish_toxicity`'s.

And the stated mechanism ("a testing programme rather than the chemistry sets which compounds are measured") is not what the data shows: the decomposition in §3 says the split removes 59% of close analogs **where it can group** (8.3% → 3.4%) and nothing at all on the 60.7% of rows SPLIT-31 leaves as singletons. **Remedy: fix the two citations and replace the explanation with the measured decomposition.** (`qsar_bioconcentration`, benzene 34% and still 12.6% → 6.4%, shows the singleton share alone is not the mechanism either; this set's analogs simply sit in the ring-less and benzene buckets.)

**3. The applicability-domain gap is undisclosed, while the source itself measured it (P3, USE-9; Weigh → curator's call)**

Under the shipped split, LightGBM RMSE by distance to the training side: **0.87** where the nearest training chemical is ≤ 0.40 Tanimoto (1,995 of 6,549 scored test rows), 0.74 (0.4–0.5), 0.59 (0.5–0.7), 0.59 (0.7–0.9), **0.49** above 0.9. And the source states the gap in its own words: *"industrial data performances were noticeably lower than those on public data"*, and its final models were *"updated with the inclusion of new industrial compounds, extending applicability domain"* — the cut we ship is the public data **before** that extension, so a test chemical here is a public-database chemical, not the industrial substance the use case names.

`fit="direct"` and its reason ("a held-out series stands for a family not yet tested") carry none of this. Both siblings disclose it: `qsar_oral_toxicity` records `fit` **approximate** on exactly this argument; `qsar_fish_toxicity` records **direct** with the spread in a CC. Treating like cases alike, `qsar_fish_toxicity` is the closer precedent (same endpoint, 808 of its 908 chemicals are in this set) and **the fit should stay `direct`** — but the line is missing. **Remedy: a sentence in `curation_comments` with the two numbers above and the source's quote.** Whether that also moves the fit is a weighing call for the curator; I recommend keeping `direct`.

**4. "No entry date behind it" is stronger than the evidence (P4, SPLIT-37; Should)**

`time_basis` says *"no test date, species or condition in the file and no entry date behind it: the CAS-RN is a registration number for the substance, not the moment a value entered a database."* The first half is right; the second overstates. `[CAT.entry-date]` allows a date **in a parent source**, and `qsar_fish_toxicity` built exactly that — 850 of its 908 chemicals dated 1956–2005 through the EPA ECOTOX bulk release on the CAS-RN — and 808 of those 908 are in this set, so at least ~37% of these 2,183 rows are datable the same way. The definition also takes SPLIT-37 **step 3** where the two closest siblings (`qsar_fish_toxicity`, `qsar_aquatic_toxicity`) sit at **step 5**, whose `Time basis:` line is required to give the forward split's share against a random draw's — not given here.

The leaf does not change (§1: the sibling's forward measurement, 7.2% against 6.9%, says the date carries no wave). **Remedy: soften the sentence to "no entry date in the release; a parent source dates part of it" and cite the sibling's measurement** — or run the ECOTOX join if the curator wants it first-hand.

**5. The order-drift explanation is pointed the right way but worded wrong (P7; minor)**

`curation_comments`: *"the target does drift along it (the time probe's `order_drift`, p 5e-16)"*. The probe's flag comes from **lag-1 autocorrelation 0.333**, not from drift: its own Spearman is −0.031, and on the 2,200 raw fish rows I measure Spearman(position, target) = **−0.029, p 0.18** — not significant. The alphabetical claim itself checks out exactly: **1 of 3,680** records is out of ascending `SMILES_Canonical` order, and the mean target by leading character runs N 3.95 → I 5.13. So what the flag sees is that neighbouring rows are homologs with similar values, which is the same alphabetical-neighbour effect and no clock. **Remedy: reword to "neighbouring rows are near-analogs (lag-1 autocorrelation 0.33); the target does not drift monotonically (Spearman −0.03, p 0.18)."**

---

**5. Attacks that found nothing**

* No copy of one substance across the split (0 shared skeletons, 0 shared CAS, 2,183 distinct SMILES).
* No group leaks across any of the 30 splits.
* No hidden group the split ignores: the only candidate structure, the `DB` source list, is dropped, and the builder's measurement (source flags alone RMSE 1.225 against 1.281 for the mean; 0.713 against 0.717 beside the structure) is the SPLIT-37 step 6 disclosure.
* The residual near-analog overlap is worth 0.008 RMSE (§3), and a Tanimoto-1.0 neighbour carries a median 0.66 log difference in target — no label travels with similarity here.
* No model score chose the split: the `splits_comment` argues from the use case and the source's scope only.
* The leak and task probes are clean (all features R² 0.680 against 0.435 for the best single feature; no task-probe flags; `dataset check` 0 errors, 0 warnings).

</details>

<details><summary>Domain practitioner</summary>

**Who I am**

An ecotoxicologist / hazard assessor in a chemical company's product-stewardship group (the source's own setting — Solvay co-authored it). My decision: for a substance with no fish data, estimate the acute fish toxicity so I can (a) set the CLP/GHS aquatic hazard classification and label, (b) derive a PNEC for the chemical safety report, and (c) decide whether to commission an OECD TG 203 test or justify a waiver. I work from structure plus whatever physchem and lower-tier ecotox data the dossier already holds.

---

**1. Fit: direct, with one gap in the inputs that the stated use case itself opens**

The row is one substance, which is exactly one classification decision; the target is the quantity I act on, on the scale the field models it on; the test rows are chemical series I have not measured, which is my situation. I would use this model — it is the same thing ECOSAR and VEGA give me, trained on more compounds.

The gap: the definition's `use_case` names *"to classify and label it and to fill a registration dossier"*, and at that moment the dossier already contains the Daphnia 48-h EC50 and the algae 72-h ErC50. Under REACH these are Annex VII requirements at 1 t/y (9.1.1 Daphnia / OECD TG 202, 9.1.2 algae / TG 201), while the short-term fish test is Annex VIII, 9.1.3, at 10 t/y — so by construction the invertebrate and algal values exist *before* the fish value is wanted. They are in the very same SDF, and the definition drops them as "other tasks". That is a USE-6 problem: anything known at the prediction point is a legitimate input.

**Measured** (shipped splits, 3 repeats × 3 folds, `encode_smiles` features, untuned LightGBM; script and CSV in my scratch folder):

| | RMSE, all test rows | RMSE on the 55.6% of rows that carry a co-input | CLP band accuracy |
|---|---|---|---|
| structure only (as shipped) | 0.7167 | 0.6616 | 0.593 |
| + Daphnia pEC50 + algae pEC50 (NaN where absent) | 0.6856 | **0.5808** | 0.613 |

−0.031 overall (SE 0.005, better on 9/9 splits) and −0.081 on the affected rows (SE 0.010, 9/9); same sign for random forest (−0.081), shallow LightGBM (−0.079), ridge (−0.042), 5-NN (−0.009). Raw correlations: fish vs Daphnia r 0.79 (n 1,029), fish vs algae r 0.777 (n 685) — in line with the JRC's r² 0.64 for acute Daphnia predicting fish, and this is exactly what EPA's ICE tool and published Daphnia→minnow QTTRs are for. Availability: Daphnia on 47.1% of the shipped rows, algae 31.4%, at least one 55.6%.

So the gain is real and consistent but modest (about 5% of the task's skill), because the structure already predicts the Daphnia value well. The point is less the number than that the dataset as written answers a different question from the one its own use case asks.

---

**2. Gaps, ranked by how much they change the task**

**(1) The stated prediction point and the shipped inputs disagree (USE-6, USE-1).** Either of these is a clean task; the folder currently sits between them.
- *Screening / design point:* a chemist or regulator judges a substance with **no** test data (pre-registration, a new structure, a polymer breakdown product). Only the structure exists. → keep the frame as is, but narrow `use_case` and `known`: drop "to fill a registration dossier", say the substance has not been tested on any trophic level.
- *Dossier point (what the text says today):* the Annex VII results are in hand. → ship `pEC50 - DAPHNIA` and `pEC50 - ALGA` as two extra numeric features, missing where absent (USE-7 keeps the missing values missing; the fish value is what I act on, so rows without a co-input are still task rows).

My preference as the actor: **the dossier point with the two columns shipped**. It is the decision I actually make most often, it is the harder and more realistic modelling problem (mixed structure + sparse assay inputs), and it is what separates this dataset from `qsar_fish_toxicity`, which has no such columns. If the curator prefers the screening framing, fix the wording — either way the mismatch should not ship. Consequence to note: if the Daphnia endpoint later becomes its own dataset, the same column is a target there and a feature here; PROV-7 permits that (different tasks), but it should be a deliberate call.

**(2) The population I face is not the population measured — and the source says so (USE-8, `Selection Bias`).** The file holds only substances for which someone obtained a numeric LC50. Substances with no effect up to their water solubility — which CLP explicitly handles ("'No acute toxicity' is taken to mean that the L(E)C50(s) is/are above the water solubility", and they still fall into Chronic 3 / the safety net) — carry no number and are therefore absent; so are the untested low-tonnage substances that make up most of my inventory. The companion article's own abstract reports that *"industrial data performances were noticeably lower than those on public data"*, i.e. the authors measured that the model is worse on precisely my population. That belongs in `fit_reason` in those words, and the `Selection Bias` marker is warranted. Whether it moves the fit to approximate is a family call: `qsar_oral_toxicity` is approximate for the same reason, `qsar_bioconcentration` and `qsar_fish_toxicity` are direct. I would keep **direct** for consistency with the two siblings this one replaces, and name the gap — but the curator should decide the three together rather than per dataset.

**(3) The label is a pooled fish value, not the value my dossier reports (USE-5).** I report a species- and guideline-defined LC50 (TG 203; and for classification the lowest valid value across the fish studies I hold). This target is "whichever fish was tested", and the builder's own evidence shows interspecies scatter of the same size as the model error (fathead vs rainbow trout r 0.926, 68% within 0.5 log; published inter-laboratory LC50 spread around 1 log unit, CVs 33–88% for 96-h fathead/trout tests). I accept this — ECOSAR's "Fish 96-h LC50" is pooled the same way, so the field's own tool makes the same compromise — but `fit_reason` should say that the label's own scatter is of the order of the best model's RMSE (0.72), since that sets the benchmark's ceiling. I agree with the builder's recommendation B1 (direct); I would only strengthen the wording.

**(4) An input I would normally hold and is not here: measured log Kow and water solubility** (Annex VII physchem, generated before any ecotox test; ECOSAR takes log Kow and MW *from the user*). The file has no physchem columns, so a model must use a computed logP — and the leak probe already shows RDKit's `MolLogP` is the best single feature (63% of LightGBM's skill). The gap is measured-vs-computed only, it is not fixable from this source, and it is small. Name it, change nothing.

**(5) Trust, not a defect:** I would not put a bare point prediction into a dossier. ECHA wants a QMRF/QPRF with a defined applicability domain and a reliability statement (OECD validation principle 3) — the authors themselves say their models "extend the applicability domain". A tabular benchmark that scores point predictions cannot test that, which is fine; it just means the benchmark measures less than what makes me trust a model. No action.

**Checked and *not* a problem:** the molar scale. I classify in mg/L, but molecular weight is fixed and known for each compound, so an error of x log units on −log10(mol/L) is exactly x log units on mg/L. The `+3` shift and the molar target cost me nothing. Also: one row = one decision (one substance, one classification), and no censored ">" pile-up at round concentrations (the builder checked; I confirm the band shares are smooth: 18.0% ≤1 mg/L, 32.6% 1–10, 32.7% 10–100, 16.7% >100).

---

**3. Does the declared metric score my decision? Partly — and I would keep `rmse`**

My decision is banded: CLP/GHS cut off at 1, 10 and 100 mg/L (Acute 1 at ≤1 mg/L; the same bins ECOSAR prints as "toxic" and "harmful"), and my errors are asymmetric — calling a 0.5 mg/L substance 5 mg/L is a mis-classification with consequences, calling a 300 mg/L substance 900 mg/L costs nothing. `rmse` on the log molar value weighs those the same, and it spends 17% of the rows on a range above 100 mg/L where no acute classification exists at all.

So I tested whether that matters for *picking a model*, which is what MET-1 asks. Over 6 model families on 9 splits:

- Kendall tau between −RMSE and CLP band accuracy: **0.83 per split** (0.73–1.00), **0.87 on the mean ranking**; the same model (LightGBM) wins under both.
- Against the share of predictions landing in a *less* hazardous band than the truth (my unsafe errors): tau **0.65** — looser, and this is the dimension RMSE genuinely does not see (the best model still mis-calls 19% of chemicals as less hazardous than they are, and recovers only 55% of the Acute-1 compounds).

Verdict: **partly, keep `rmse`** (MET-8, MET-11 fallback). It ranks models the way my decision does on every split, and the alternative a threshold metric would need is not declarable here: MET-7 forbids inventing a cost or threshold, the source fixes none, and CLP fixes *three* cut-offs with no cost ratio between them, so there is no single operating point (the same reason `taiwanese_bankruptcy_prediction` fell back). A band-accuracy or cost-matrix metric would also require the mg/L scale and the molecular weight as a scoring input for no ranking gain. `rmse` is additionally what my field reports for this endpoint (the authors' own RMSEext 0.56–0.78; ECOSAR evaluations). What I *would* ask for is one sentence in the notes recording that the metric is scale-symmetric while the decision is banded and asymmetric, with the tau 0.83 measurement as the evidence that it nonetheless selects the same model — that is the honest version of "a practitioner would pick a model by it".

---

**4. What I would change, in order**

1. Resolve the prediction point (finding 1): ship `pEC50 - DAPHNIA` and `pEC50 - ALGA` as features and keep the dossier wording, **or** narrow `use_case`/`known` to the untested-substance screening point. My vote: the former.
2. `fit_reason`: add the industrial-chemical-space gap in the authors' own words, and that the label's interspecies/inter-laboratory scatter is of the order of the best model's error. Add the `Selection Bias` marker; raise direct-vs-approximate as a family call with `qsar_oral_toxicity`.
3. Metric note on the banded, asymmetric decision with the tau 0.83 evidence; `rmse` stays.
4. Everything else (fish-endpoint-only, the `DB` drop, the copy key, pLC50 over mg/L, the scaffold split) I agree with as built — dropping `DB` in particular is right: I have no source list for a substance nobody has tested (LEAK-1).

---

**Sources**


Domain:
- [CLP Annex I §4.1 aquatic hazard criteria (legislation.gov.uk)](https://www.legislation.gov.uk/eur/2008/1272/annex/I/division/4) and [reachonline CLP 4.1.2](https://reachonline.eu/clp/en/annex-i-4-4.1-4.1.2.html) — 1 / 10 / 100 mg/L bands, lowest trophic level decides
- [ECHA Guidance on CLP, introduction and environmental hazards](https://echa.europa.eu/documents/10162/13562/clp_guidance_introduction_and_env_en.pdf/a55869a8-e70e-4229-9320-c9b2bfc9ab22) — "no acute toxicity" = L(E)C50 above water solubility
- [REACH Annex VII §9 (Daphnia 9.1.1, algae 9.1.2)](https://legislation.gov.uk/eur/2006/1907/annex/VII/division/9) and [Annex VIII §9 (fish 9.1.3)](https://legislation.gov.uk/eur/2006/1907/annex/VIII/division/9/2018-12-01/data.htm?view=plain); [Regulation (EU) 2022/477](https://eur-lex.europa.eu/eli/reg/2022/477/oj/eng/pdf)
- [JRC technical report, Kienzler et al. 2016, interspecies correlations](https://publications.jrc.ec.europa.eu/repository/bitstream/JRC101327/jrc%20technical%20report%20kienzler%20et%20al%20waiving%20options%20for%20chronic%20fish%20toxicity%20may%202016.pdf) and [Daphnia–minnow QTTR](https://www.tandfonline.com/doi/abs/10.1080/1062936X.2022.2098814)
- [EPA ECOSAR methodology v2.2](https://19january2025snapshot.epa.gov/system/files/documents/2022-03/methodology-document-v.2.2.pdf) and [users guide](https://19january2021snapshot.epa.gov/sites/static/files/2015-09/documents/ecosarusersguide.pdf) — log Kow + class, user-supplied log Kow, hazard bins
- [Machine-learning prediction of fish acute mortality on ADORE (bioRxiv 2024)](https://www.biorxiv.org/content/10.1101/2024.03.14.584983v2.full) and [limitations/uncertainties of acute fish toxicity assessments](https://www.researchgate.net/publication/344381722_Limitations_and_uncertainties_of_acute_fish_toxicity_assessments_can_be_reduced_using_alternative_methods) — experimental LC50 variability
- [Lunghini et al. 2020, SAR QSAR Environ. Res. 31(9):655-675](https://www.tandfonline.com/doi/full/10.1080/1062936X.2020.1797872) (abstract only; full text paywalled, as the builder reported) and the [Semantic Scholar record](https://www.semanticscholar.org/paper/55c5794df79e9790324a2d08d5bcd95a6e4b1470)

</details>

<details><summary>Blind review</summary>

**Verdict**

**Include with changes** — the chemistry and curation are genuinely good (real, deduplicated, correctly-unit'd 96 h fish LC50 data with solid signal), but as delivered this is not a tabular task at all: the only predictor is a SMILES string, and LightGBM on the two columns as shipped scores **R² = −0.003**.

---

**1. There are no tabular features. The table is a target plus a molecule ID. (most serious)**

`data.parquet` is 2183 × 3: `SMILES` (string, 2183 unique), `LC50` (float), `scaffold` (string, group key). A tabular learner sees a free-text column with one value per row.

| features given to LightGBM | grouped-CV R² |
|---|---|
| **`SMILES` + `scaffold` as categoricals (the table as shipped)** | **−0.003** |
| SMILES as char 1–5-gram TF-IDF (ridge / LGBM) | 0.55 / 0.57 |
| RDKit 2D descriptors (208 cols) | **0.667 ± 0.035** |
| ECFP4-1024 | 0.491 |
| `MolLogP` alone | 0.433 |

So the dataset is either unlearnable or a test of whether the competing library happens to do character n-grams on strings — neither is a measurement of tabular modelling. Note the 0.67/RMSE 0.73 figure sits right inside the paper's own `RMSEext = 0.56 – 0.78`, so the *chemistry* is fine; it's the representation that is missing.

**Change:** ship the descriptor block as real columns (RDKit `CalcMolDescriptors`, 208 numeric columns after dropping constants — that alone gives a clean, non-trivial 2183 × 209 regression with headroom over the `logP` baseline), and keep `SMILES` only as an identifier. If the benchmark's rules forbid adding derived columns, then this is a QSAR task, not a tabular one, and should be excluded.

**2. The group key is shipped inside the feature set, and 61 % of the time it is a copy of the SMILES**

`task.md` counts 3 columns "target included", so `scaffold` is a feature. For 1325 rows its value is literally `"single: " + SMILES` — I verified the stripped string equals `SMILES` for 100 % of those rows. Under grouped CV it carries zero information (no train scaffold ever appears in test), so it is pure high-cardinality noise, and it duplicates the identifier.

**Change:** keep `scaffold` as a split/group column outside `X`, and say so in `task.md`.

**3. "Grouped by `scaffold` (whole groups are held out)" overstates the split — benzene was dissolved**

Recomputing Bemis–Murcko scaffolds shows exactly one scaffold was broken up: **`c1ccccc1`, 649 rows = 29.7 % of the data**, each given its own `single:` group. 676 acyclic rows have no Murcko scaffold and are likewise singletons. Every other scaffold was kept whole. Result: 1651 of 1761 groups are singletons and **60.7 % of rows are in a group of one**.

Consequences I measured:
- grouped-split R² **0.669** vs random-split R² **0.687** — the regime buys 0.018.
- **3.9 % of test compounds have an ECFP4 Tanimoto = 1.000 neighbour in train** — homologous series straddling the split, e.g. `CCCCCCCCCC(C)=O` (y = 5.05) / `CCCCCCCCC(C)=O` (y = 4.47), `CCCCCCCCCO` / `CCCCCCCCCCCCCO`. Median NN similarity to train is 0.48.

Dissolving a 650-row group is defensible (3-fold CV on it would be grotesque), but it is precisely the substituted-benzene class — the core of aquatic QSAR — that is now split at random.

**Change:** either describe the regime honestly ("near-random split; large scaffold families kept together"), or build a balanced split that caps group size, e.g. Butina clustering on ECFP4 at ~0.6, so no group exceeds ~10 % and chain-length analogs stay together.

**4. The target is the published column shifted by +3, undocumented**

Joining to the Zenodo SDF (`MergedEndpoints.sdf`, 3680 records, 2200 with `pLC50 - FISH`), every prepared value equals the source value **+ 3.000 exactly** (max |diff| 3.000000000000001 over all 2183 rows). This is a *correct* fix: the source column is −log₁₀(mmol/L), and the prepared values are true −log₁₀(mol/L), which I checked back against literature — phenol 3.495 → 30 mg/L (fathead minnow 96 h LC50 ≈ 29–34), chlorobenzene 3.770 → 19 mg/L, nitrobenzene 3.022 → 117 mg/L. But a silent constant offset from the cited source is the kind of thing that makes a reviewer think the numbers were mangled.

**Change:** one line in `task.md`: "target is pLC50 = −log₁₀(LC50 in mol/L); the Zenodo `pLC50 - FISH` field is in mmol/L, so 3.0 was added."

**5. The noise floor and the aggregation rule are unverifiable from the public record**

The Zenodo `DB` field shows each compound merged from 1–8 sources (ECHA, ECOTOX, OASIS, VEGA, NITE, EPAFHM, EFSA, "Litterature set"); **39 % are single-source**. The record says only "Fish, the log median lethal concentration measured at 96 hours is considered" — it names no species, and OECD TG 203 permits many with very different sensitivities. Nothing public states how several experimental values per compound were combined. Inter-lab/inter-species spread on this endpoint is typically 0.3–0.5 log units, so the practical ceiling is probably RMSE ≈ 0.5 against the observed 0.73 — fine for benchmarking, but reviewers should not read R² 0.67 as "much headroom left".

**6. Minor: float representation noise**

234 values carry 16-decimal float repr (`5.861000000000001`, `3.1189999999999998`). Round to 3 dp to match the source's precision.

---

**What is right, and I checked it**

- **Real data, right target.** Values reproduce literature fathead-minnow LC50s (above). Target distribution is smooth and near-Gaussian over 0.60–9.51, no censoring pile-up (only 0.5 % at exactly 100 mg/L; 18.6 % would be CLP Aquatic Acute 1).
- **Genuine use.** 96 h fish LC50 is the REACH / OECD TG 203 endpoint behind CLP aquatic hazard classification; in-silico estimates are used under REACH Annex XI to avoid vertebrate tests. A registrant or product steward makes this call before commissioning a study. Real decision, real timing — nothing in the row is unknown at prediction time.
- **No leakage.** The source's `mg/L - FISH` column (a deterministic transform of the target) was correctly dropped, as were `CASRN` and `DB`.
- **Excellent deduplication.** All 2183 SMILES parse; zero duplicate canonical SMILES, zero duplicate InChIKeys, zero duplicate InChIKey skeletons, zero salts or multi-component records. The 17 source rows dropped are exactly the duplicate casualties — 10 tautomer collisions where one of each pair was kept (`Oc1ccc(Cl)cn1` vs `Clc1ccc(=O)[nH]c1`), plus three CAS-duplicate pairs dropped wholesale including an azulene entry with a wrong structure (`C1CC2CCCCCC2C1` for CAS 275-51-4). Careful work.
- **Big enough to score.** ~728 test rows per fold × 30 splits; fold-level R² sd 0.035 → SEM ≈ 0.006.
- **No weight column** is declared, so there was nothing to assess there.

**What I could not check**

- The paper full text — `tandfonline.com` returns HTTP 403, so the aggregation rule for replicate measurements, the fish species mix, the authors' own train/test partition, and the per-endpoint RMSE breakdown are all unverified. Everything above about the source comes from the Zenodo record, the PubMed abstract, and the SDF I downloaded and parsed myself.
- Whether the benchmark harness featurizes SMILES. My "R² = −0.003" figure assumes the default tabular treatment (string → categorical); if the harness applies text featurization, the number is ~0.55 instead — still a text benchmark, not a tabular one.
- Whether a descriptor set computed at benchmark time would be stable across RDKit versions (I used 2026.03.6).

Sources: [Zenodo record 3708082](https://zenodo.org/records/3708082) · [PubMed 32799684](https://pubmed.ncbi.nlm.nih.gov/32799684/) · [Semantic Scholar entry](https://www.semanticscholar.org/paper/Consensus-QSAR-models-estimating-acute-toxicity-to-Lunghini-Marcou/55c5794df79e9790324a2d08d5bcd95a6e4b1470)

</details>

<details><summary>Task gamer</summary>

**Verdict**

This task is essentially un-gameable from inside the kit — I found no feature, rule or transform that beats an honest LightGBM by more than the random-column noise floor (±0.0005 RMSE); the one real defect is the split itself, which grants 649 benzene-scaffold compounds their own one-row "group" and so measures something ~36% of the way from a true scaffold split back toward a random split.

**Honest baseline:** LightGBM (untuned: 400 trees, lr 0.05, 31 leaves) on 210 RDKit descriptors + 1024-bit Morgan count fingerprints, fitted and scored on all 30 shipped splits with `score.py`: **RMSE 0.7167** (sd across splits 0.0269). No training weight in `task.json`. Noise floor from refitting with one extra column of random numbers: 0.7169 / 0.7165 / 0.7161 (seeds 0/1/2).

**Exploits ranked by gain**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| — | *none found above the noise floor* | — | 0.7167 | — | — | — | — |

Everything I tried is listed under "attacks that found nothing". The only thing that scores better than the baseline is the published-source lookup, which is not ranked: all 2183 kit rows match the Zenodo `MergedEndpoints.sdf` on canonical SMILES and `LC50 = pLC50_FISH + 3.0` **exactly** for every row, so a lookup scores RMSE 0.000000 on all 30 splits (`work/join.py`). Every public dataset allows this; it is not a flaw of the task.

**Flaws that hurt / distort the task**

| # | What is wrong | Script | Score as shipped | Score with the honest choice | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| F1 | The `scaffold` column does not group by scaffold for 61% of rows; the declared "whole groups are held out" regime is not delivered | `work/a_group.py` | 0.7217 (kit grouping, own 10×3) | 0.7519 (true Murcko grouping) — 0.7047 under a plain random split | n/a — a split-design defect, not a feature leak | Group all 649 benzene-Murcko compounds into one group (and keep acyclics singletons, or group them by a generic framework) |
| F2 | Target carries float-arithmetic residue from the `+3` shift: 307/2183 values (14%) sit 1–2 ULP off the exact 3-decimal double | `work/fmt.py` | — | — | No — but also not usable, it is a function of the label | `df["LC50"] = df["LC50"].round(3)` |

---

**F1 — the scaffold groups.** 1325 of 2183 rows (61%) have a group of the form `single: <full SMILES>`, i.e. a group of one. 676 of those are acyclic compounds with an empty Murcko scaffold, which is defensible; the other **649 all have the same Murcko scaffold, benzene `c1ccccc1`** — the single largest and most congeneric class in the set (phenols, anilines, nitrobenzenes, chlorobenzenes) — and were nevertheless split one molecule per group. Running my own 10×3 grouped CV on the same features: kit grouping 0.7217, true Murcko grouping with benzene as one 649-member group 0.7519, plain random 0.7047. The shipped regime therefore sits at 36% of the random→scaffold difficulty gap while the task card promises the scaffold end of it. Mildest fix: assign the benzene-Murcko rows to one group. (I verified the shipped splits are otherwise clean: no train/test overlap, every row is a test row exactly 10 times, no `scaffold` value appears on both sides of any split, row lists are sorted ascending, and fold-mean LC50 ranges only 4.198–4.405.)

This does **not** translate into an exploit: read-across is already saturated. Only 5.3% of test rows have a training neighbour at Tanimoto ≥ 0.9 (median max similarity 0.50), the 1-NN label alone scores 1.203, and adding explicit kNN read-across features (k = 1/3/5/10, similarity-weighted neighbour labels + similarity) moves the baseline to 0.7169 — nothing (`work/a_knn.py`).

**F2 — the target's low-order bits.** The kit target is the Zenodo `pLC50 - FISH` plus 3.0 computed in float64, so 307 values are one or two ULP away from the double nearest their 3-decimal value and print with 15–16 decimals (`5.861000000000001`). These rows have a visibly different mean (ulp −1: 4.879, ulp 0: 4.244, ulp +1: 4.706, n=175/1876/130). It looks like a provenance fingerprint but is not one: the residue is a deterministic function of the stored value, so it only exists for rows whose label you already have. Fitting it as a feature "works" (0.7145) purely as self-leakage of the test labels and I discard it. Still worth rounding the column, since it is a free hint about how the file was built.

**The target's quantisation lattice (checked, dead).** For 1899/2183 rows the source satisfies `pLC50 = round(log10(MW) − log10(mg/L), 3)` exactly, and MW is computable from SMILES, so the target lies on a lattice whose points are set by the mantissa of the reported mg/L. But mg/L is reported finely: 627 distinct mantissas among the 1678 rows with ≤4 significant figures, median gap between adjacent admissible target values 0.0013 log units, implying a snapping floor of 0.0004 against an RMSE of 0.717. There is no coarse limit-test sentinel to lever either — only 11 rows sit at exactly 100 mg/L.

**Attacks that ran and found nothing**

* **Formats.** Only one feature column exists and it is a SMILES string. All 2183 strings are byte-identical to current RDKit canonical SMILES, none carries stereochemistry, none is multi-fragment, and the bracket-atom vocabulary is ordinary (`[N+]`, `[O-]`, `[nH]`). No case, spacing, encoding or template channel survives canonicalisation. SMILES-string-only features (length, counts of lower/upper/digit/paren/bracket, first character) score 1.031 vs 1.28 for a mean predictor — that is molecular size and lipophilicity leaking through string length, i.e. chemistry, not a recording artefact.
* **Order and ids.** Row position alone scores 1.343, *worse* than predicting the training mean; honest + row position 0.7172. No id column. `splits.parquet` row lists are sorted ascending, so their order carries nothing.
* **Copies across the split.** 0 exact duplicate SMILES, 0 duplicates after stripping stereochemistry, 0 after RDKit tautomer canonicalisation, 0 sharing an InChIKey skeleton block. The preparation dropped 17 of the 2200 source fish rows; inspecting them, every one is a canonicalisation or tautomer collision with a row that was kept (e.g. `Cc1ccccc1NC(N)=Nc1ccccc1C`, `O=c1ccc(Cl)c[nH]1`), a label-independent clean-up. Nearest-neighbour prediction: see F1.
* **Columns from after the prediction point / the weight / temporal training rows.** Not applicable: one feature column, no time column, no sample weight, `prediction_time: null`.
* **Statistics over train and test together.** Transductive features (scaffold group size over all rows, mean/max/top-10 Tanimoto to the whole table, frequency and percentile-rank encodings of MolWt/MolLogP/TPSA/HBA) added to the honest model: 0.7168. Alone they give 0.854, which is just logP and size. A train-vs-test classifier reaches AUC 0.57–0.62 — the expected consequence of holding out whole groups, and it carries no label information.
* **Transforms over all rows.** Mean-0/SD-1 and rank/quantile transforms are monotone per column and cannot move a tree model; the cross-row count encodings that *can* were tested above and gave nothing.
* **Lookups and reparametrisations.** Predicting on the mass-concentration scale (`y − log10 MW`, then adding it back) gives 0.7216, worse. An RBF SVR on the same features gives 0.892 and a 50/50 SVR+LGBM blend 0.7487, both worse than the plain LightGBM, so the baseline stands as the honest reference.
* **Web search.** The Zenodo record and the Lunghini et al. 2020 paper describe the fish endpoint and the external RMSE range 0.56–0.78 that my 0.717 sits inside; I found no competition forum, "magic feature" thread or published critique of this dataset. The nearest relevant literature is the ADORE benchmark, which makes the general point that split choice inflates aquatic-toxicity model scores through similar-compound leakage — exactly the mechanism F1 describes — but does not audit this dataset.

**What I could not check**

Whether the benchmark's own SMILES featurizer matches mine (a different one could change the absolute numbers, though not the relative findings); which of the 2183 consensus labels are censored limit-test values, since the kit carries neither the mg/L column nor the `DB` provenance field; and the species / test-condition heterogeneity folded into the consensus, which is not recoverable from the kit or from the published SDF.

Sources: [Zenodo record 3708082](https://zenodo.org/records/3708082), [Lunghini et al. 2020, SAR QSAR Environ. Res.](https://www.x-mol.com/paper/1295543091613802496), [ADORE benchmark](https://www.nature.com/articles/s41597-023-02612-2), [ADORE follow-up modelling study](https://pubs.rsc.org/en/content/articlehtml/2024/va/d4va00072b).

</details>

<details><summary>Precedent check</summary>

**Precedent check — `aquatic_toxicity_lunghini_consensus`**

Read: the record, `dataset.py`, the builder's hand-over, the decision item `qsar_fish_toxicity`, the register of today, `principles.md`, `molecules.md`, `split_tree.md` (catalogue branch), `splits.md` (SPLIT-32/33), `leak_checks.md` (LEAK-16-22), `use_case.md` (USE-5/8), `provenance.md`, `metrics.md`, and the four sibling definitions + records (`qsar_fish_toxicity`, `qsar_aquatic_toxicity`, `qsar_oral_toxicity`, `qsar_bioconcentration`, plus `apistox`, `nci_aids_antiviral_screen`, `drug_induced_autoimmunity_prediction`).

**5 findings.** Three are departures (one without a reason, one whose stated reason the definition's own text contradicts, one with a partial reason); two are corrections to how precedent is cited. Nothing here touches the verdict: the task, the split family and the metric all follow the closest precedents.

---

**Decisions that follow precedent (no action)**

| Decision | Precedent | Verdict |
|---|---|---|
| Leaf `L-FAMILY.key`, Bemis-Murcko groups, ring-less and >1/10 scaffolds alone | SPLIT-31 as amended (Lennart, 2026-10-26, `qsar_bioconcentration` issue 10(d)); same leaf in `qsar_fish_toxicity`, `qsar_aquatic_toxicity`, `qsar_oral_toxicity`, `qsar_bioconcentration` | consistent |
| 10 × 3 splits | SPLIT-33 (train side under 2,500 units) | consistent |
| Fish endpoint alone, Daphnia/algae as separate records (PROV-7) | `global_findex_2025` / `global_findex_2025_mobile_banking` ("two targets of one survey file, PROV-7, weigh"); the base record keeps the plain name | consistent |
| Target `= pLC50 + 3` (to −log10(mol/L)) | the sibling's scale; the decision item's own instruction (2026-11-25, "add 3 for the −log10(mol/L) this record ships"); verified against mg/L ÷ MW | consistent |
| `pLC50` over the mg/L column (D1) | CLEAN-1 with an independent check; and "a fix of our own invention does not [replace the source]" (eryhemato, P5 over P6) rules out a per-row choice | consistent |
| One row per substance (InChIKey skeleton ∪ CAS-RN) | LEAK-17 (one row per entity); the curator-facing matching of 2026-11-25 used the same three keys. A widening of `molecules.md`'s structure key, stated and measured | consistent |
| `DB` dropped (LEAK-1, CLEAN-22), with the cost measured | `apistox`'s `source`; `qsar_bioconcentration`'s `logKOW_type` (Lennart, 2026-11-02, with the same "measure it first") | consistent |
| `Formula`, `Mol Weight`, `endpoint`, identifiers dropped; SMILES the one feature | CLEAN-24 as amended (Lennart, 2026-11-01) | consistent |
| `rmse`, `Metric.fallback` | MET-5 ("a headline number in the abstract is not by itself a deliberate choice", Lennart 2026-10-21); the sibling ships `rmse` on the same target | consistent |
| Sibling question deferred to `qsar_fish_toxicity`'s record (PROV-4/6/7) | the "better data is its own record" pattern (`body_density_prediction`, `fiat_500`); the register's PROV-6 history (curators excluded 5 of 6 times) favours the item's option B, which is where it belongs | consistent |
| No censoring (LEAK-22), `order_drift` explained, no accepted warnings | — | consistent |

No drift: the register's drift flags (TP-3, TP-4, USE-9, generated data, scaling) touch none of the rules in play, and no reason here has produced a third exception.

---

**F1 — `Time: Lost` departs from SPLIT-32's wording and from four sibling records, with no fact that sets it apart**

**Severity: the highest here** (a collection fact, P4's input). Not a change of split.

* The record sets `Time: Lost`, and the time basis says "no entry date behind it: the CAS-RN is a registration number, not the moment a value entered a database".
* SPLIT-32 (`splits.md`): `Time: Dated` **"when the release *or a parent source* keeps the date (… or a parent upload that matches the rows by an id)"**, and "a catalogue that a parent source dates is `Samples: Over Time` with `Time: Dated` **even where the date turns out to carry nothing**".
* Every sibling of this family is `Time: Dated` — `qsar_fish_toxicity`, `qsar_aquatic_toxicity`, `qsar_oral_toxicity`, `qsar_bioconcentration`, `drug_induced_autoimmunity_prediction`, `apistox` — and `nci_aids_antiviral_screen` is `Time: Inferred`. **None is `Time: Lost`.** All of them have no date column either: the date came from a parent source.
* The nearest precedent is the dataset this one replaces, decided by the same curator 13 days ago: `qsar_fish_toxicity`'s time basis, set by **Andrej on 2026-11-13** (`Timeless` before), is built on "the EPA's ECOTOX bulk release (`ecotox_ascii_09_15_2026`), **joined on the CAS-RN** … 850 of 908 chemicals (93.6%), 1956 to 2005". `qsar_oral_toxicity` was dated the same way by RTECS report year (Andrej, 2026-11-11).
* The stated reason does not distinguish: the CAS-RN is not the date — it is the join key, exactly as on the sibling. This file carries a CAS-RN on 3,659 of 3,680 compounds, and the builder already matched 1,282 fish compounds to ADORE's ECOTOX cut on it. ADORE's `before_aggregation/ecotox_tests.csv` carries `published_date` on 62% of its tests and a `reference_number` per test, keyed by `test_cas`.
* The leaf does not move either way: the walk answers no at `[CAT.next-items]` (SPLIT-37 step 3), which `molecules.md` backs ("First the source … the scaffold stands whatever the dates show"). Only the fact and the time-basis sentence change.

Draft issue (the reflection prompt filled in; option (a) is my best guess at the distinguishing fact):

```text
N. **Is this catalogue `Time: Lost`, where its four siblings are `Time: Dated`?**
   * **Problem:**
     - The record carries `Time: Lost` and the time basis says there is no entry date behind the rows.
     - SPLIT-32 sets `Time: Dated` when the release *or a parent source* keeps the date, "even where the
       date turns out to carry nothing"[^tag]; the parent sources here are ECOTOX, ECHA and EFSA, and the file
       carries a CAS-RN on 3,659 of its 3,680 compounds.
     - qsar_fish_toxicity, the dataset this one replaces, has no date column either and is `Time: Dated`:
       dated through the ECOTOX bulk release on the CAS-RN, 850 of 908 chemicals (Andrej, 2026-11-13)[^fish].
   * **Effect on the task:** none on the split. The leaf stays `L-FAMILY.key` (the walk answers no at
     `[CAT.next-items]`, SPLIT-37 step 3), and only the collection fact and one sentence of the time basis change.
   * **Consistency:** `Time: Dated` on qsar_fish_toxicity, qsar_aquatic_toxicity, qsar_oral_toxicity,
     qsar_bioconcentration, drug_induced_autoimmunity_prediction and apistox; `Time: Inferred` on
     nci_aids_antiviral_screen; no molecule record is `Time: Lost`.
   * **Options:**

     | | Option | Pro | Con |
     |---|---|---|---|
     | a | `Time: Lost` stays, as a fact of this release: its merged values have no single parent test, so no entry date belongs to a row (recorded as the fact that sets it apart) | honest about a consensus value that no one test dates | departs from the rule's wording and from six records of the same family |
     | b | Date it as the sibling was: join the CAS-RN to the ECOTOX release (ADORE's `ecotox_tests.csv` is on this machine: `published_date`, `reference_number`, keyed by `test_cas`), set `Time: Dated`, and write the coverage and the forward-against-random analog reading into the time basis | treats like cases alike; gives this set its own number where today it borrows the siblings' | one measurement to run |
     | c | `Time: Dated` on the rule's wording alone, with no measurement | cheapest | a fact without evidence |

   * **Recommendation:** b. **Decision:** a, b or c?

[^tag]: **SPLIT-32**: `Time: Dated` when the release or a parent source keeps the date; a catalogue a parent
    source dates is `Time: Dated` even where the date carries nothing.
[^fish]: `qsar_fish_toxicity`'s time basis, set by Andrej on 2026-11-13 (`Timeless` before).
```

---

**F2 — issue C's option set skips the repair rung (PROV-13, a Must), and its stated reason is contradicted by the definition's own text**

* Implemented (C4): for the 3 pairs whose two drawings differ in molecular formula, **both** rows go — 6 rows — "because the file does not say which [drawing] is meant".
* The remedy ladder (`principles.md`, step 5; PROV-13, Must) takes repair before dropping, and the family's precedent is a repair from a registry lookup: `qsar_bioconcentration` repaired 6 rows (three pairs carrying each other's SMILES) by looking the **CAS numbers up in Wikidata and PubChem** — "the BCF and the class belong to the CAS number" — and dropped only the rows that had **no partner row to repair them from**. Here every one of the three pairs has a partner row.
* The definition itself already names the answer for one pair: "CAS 275-51-4 (**azulene**) is drawn once as C10H8 and once as C10H18, its fully saturated form". Azulene is C10H8; the registry does say which drawing is meant. So the stated reason ("the file does not say") is true of the file and beside the point under the precedent, which goes outside the file.
* Small in size (6 rows of 2,189), real in kind: it is a Must-ranked ladder step the option table does not offer.

Draft issue (the missing option as (a)):

```text
N. **Repair the three substances drawn with two formulas, or drop both their rows?**
   * **Problem:**
     - 3 of the 14 duplicated substances are drawn under one CAS-RN with two different molecular formulas, so
       one of the two drawings is a different chemical; the implemented C4 drops both rows of each (6 rows).
     - PROV-13 (Must) asks whether the origin settles it before the damage is kept or dropped[^repair], and the
       definition already names the answer for one pair: CAS 275-51-4 is azulene, C10H8, not C10H18.
     - The precedent is a lookup, not a drop: qsar_bioconcentration repaired 6 rows from Wikidata and PubChem
       by their CAS numbers and dropped only the rows with no partner row to repair from[^bcf].
   * **Effect on the task:** 3 chemicals and their values return (2,186 rows), or stay out (2,183).
   * **Options:**

     | | Option | Rows | Pro | Con |
     |---|---|---|---|---|
     | a | Look the 3 CAS-RNs up (PubChem / CAS Common Chemistry), keep the row whose formula matches the registry, drop the other | 2,186 | the mildest remedy that resolves it; the house's own move on qsar_bioconcentration | three lookups, recorded in the notes |
     | b | C4 as implemented: both rows of the three pairs go | 2,183 | no structure the file contradicts | drops values the registry can place |
     | c | C3: keep the better-sourced row without a lookup | 2,186 | no lookup | 2 kept rows carry the wrong drawing |

   * **Recommendation:** a. **Decision:** a, b or c?

[^repair]: **PROV-13 (Must)**: when a release is damaged, check whether the origin has the clean data before
    keeping the damage or retiring, and repair from the origin when it has them.
[^bcf]: `qsar_bioconcentration`'s curation comments, "Repaired rows, 6" (2026-10-07).
```

---

**F3 — `fit="direct"` (issues A1/B1): departs with a reason, but the reason is stated against the wrong precedent**

Classify: **departs with a stated reason**, the reason partial. Not a rule break; a weighing call the curator should see with both precedent rows on the table.

* For the **split distance**, `direct` matches the closest precedent exactly: `qsar_fish_toxicity`, CC of **2026-11-12 (Andrej)** — "the fit stays direct (USE-8) … 12.4% of the test chemicals have a close training analog … against 13.1% under random 3-fold splits: holding out series removes few close analogs here". This build measures 12.1% against 13.5%. Same curator, same endpoint, two weeks ago.
* For the **label definition**, precedent points the other way, and the panel's issues A and B do not cite it:
  * `drug_induced_autoimmunity_prediction` ships **`approximate`** with the reason "The source does not say how the negative drugs were chosen …, **an unverified label definition**" — the same family, the same scaffold split, the same mechanism as the undocumented consensus merge.
  * USE-5's wording comes from the curator's own call on `diabetes_3` (Lennart, **2026-10-21**): "I would like to keep the data and just mark it as **approximate**, and we can case-by-case decide the details" — a label from a named publication whose construction is undocumented **and cannot be checked** may ship approximate. USE-8 names "a label definition the sources do not settle" as approximate.
  * `mobile_churn`: approximate because no churn rule and no horizon is stated.
* The fact that sets this case apart is real and measured — the merge *was* checked against ADORE/ECOTOX — but it covers **1,282 of 2,183 rows (59%)** and answers only "is it an arbitrary average", not what the rule is, and not which species. And the `fit_reason` as written reads like USE-8's approximate definition ("a stand-in with a known gap, named as such"): it names two gaps and, unlike every `direct` fit in this family (`qsar_bioconcentration` 6.4% vs 12.6%, `nci_aids_antiviral_screen` 15.5% vs 32.0%), cites no analog numbers.

Minimum action: add a `**Consistency:**` bullet to the builder's issue B so the curator decides against both precedents, e.g.

```text
   * **Consistency:** qsar_fish_toxicity keeps `direct` on the same endpoint with the same analog reading
     (12.4% against 13.1%, Andrej, 2026-11-12), while drug_induced_autoimmunity_prediction ships `approximate`
     for an unverified label definition, and USE-5's "may ship approximate" clause comes from diabetes_3
     (Lennart, 2026-10-21). This label is undocumented but partly checkable: the merge reproduces ADORE's
     ECOTOX values on 1,282 of the 2,183 compounds (59%); the other 901 and the unnamed species are unchecked.
```

---

**F4 — the `splits_comment` backs its scaffold measurement with the siblings' *forward-split* numbers**

* It writes: "the test chemicals stay about as close to the training side either way, 12.1% … against 13.5%. That is the pattern of the other datasets of this family … (**qsar_fish_toxicity 7.2% against 6.9%, qsar_oral_toxicity 12.4% against 13.1%**)".
* Both cited pairs are **forward-by-date against random**, not scaffold against random: `qsar_oral_toxicity`'s record table rows T (12.4%) and R (13.1%); `qsar_fish_toxicity`'s table rows "Forward by first test year" (7.2%) and "Random, any year" (6.9%). `molecules.md` lists them under "a testing programme sets the pace rather than the chemistry" — the evidence for *scaffold over temporal*, a different question.
* The apt precedent exists and is stronger: `qsar_fish_toxicity`'s own **scaffold against random, 12.4% vs 13.1%** (Andrej, 2026-11-12) — nearly this dataset's numbers.
* What the comment does not say: `molecules.md`'s scaffold table runs the other way for the rest of the family — `qsar_bioconcentration` 12.6% → 6.4%, `qsar_oral_toxicity` 24.7% → 16.3%, `qsar_tid_11` 79.7% → 59.2%, `nci_aids_antiviral_screen` 32.4% → 15.3%. At 13.5% → 12.1% this set removes **less** than any molecule dataset in that table. That is a fact for the fit question (F3) and for reading the group probe's small IID-vs-grouped gap (0.699 vs 0.684); it should be stated, not smoothed into "the pattern of this family".
* Fix in the definition's `splits_comment`: cite `qsar_fish_toxicity`'s scaffold-against-random pair, and name the family's scaffold table as the contrast.

---

**F5 — the paywalled article should be an issue, not only a note (PROV-17, a Must)**

PROV-17: "ask the curator for the PDF. If you go on without it, say so and mark the claim as unverified." The build does the second half well (`curation_comments`, the hand-over). The house pattern for the first half is an issue of its own: `australian_vehicle_insurance_2004_2005` — "**Can you get de Jong and Heller (2008)?**"; `boreal_postfire_lichen_biomass` — "Read the paper's Methods?". Two open decisions hang on this PDF (the merge rule behind F3's fit, and the authors' ranked criterion behind MET-5's fallback), so the review should carry the ask as a numbered issue rather than a line in "what could not be checked".

---

Nothing else in this build departs from a precedent I could find, and nothing here breaks a Must that the definition does not already fix. No file was edited.

</details>

<details><summary>Advocate, opening brief</summary>

**Advocate's opening brief — `aquatic_toxicity_lunghini_consensus`**

**Verdict I argue for: ship as defined, after text fixes and one repair.** Not one of the seven reports found a defect in the shipped data. The single Must that fails (MET-1) fails on a *sentence about the source*, not on the data, the split or the metric; every other finding is wording, a record field, or a weighing call. No remedy above "fix the definition" is needed anywhere.

---

**1. The only verdict-level objection — "this is not a tabular task, R² = −0.003" — is an error about our harness, not about the dataset**

**Claim.** The blind reviewer's headline finding is that LightGBM on the shipped table scores R² −0.003, so the dataset is "either unlearnable or a test of character n-grams".

**Evidence.** That number assumes a harness that feeds `SMILES` to a model as a categorical string. Ours does not. `examples/benchmark_container.py` (the reference script, lines 129–135) calls `encode_special_feature` on every column in `special_features(container)`; `dataset.py:110` declares `Smiles(column="SMILES")`. With the house encoding, three agents measured independently and agreed: RMSE **0.7167** (task-gamer, 30 splits), **0.722** (split-auditor, 9 folds), **0.715** (builder probes) — R² 0.667–0.687. The blind reviewer listed this among "what I could not check": *"Whether the benchmark harness featurizes SMILES … if the harness applies text featurization, the number is ~0.55 instead."* It also measured 0.667 itself once it computed descriptors.

**Rule.** CLEAN-24 as amended (Lennart, 2026-11-01, **Must**): "The structure ships as a SMILES column marked as a structure, never as plain text and **never pre-encoded**. The benchmark encodes it." Its proposed change — ship 208 descriptor columns — is the thing the rule forbids, and five shipped siblings (`qsar_fish_toxicity`, `qsar_oral_toxicity`, `qsar_tid_11`, `drug_induced_autoimmunity_prediction`, `nci_aids_antiviral_screen`) all ship SMILES-only through `special_features`.

**Why it wins.** EV-1/EV-2: a measurement under the real pipeline beats a measurement under an assumed one. The blind reviewer is valuable precisely because it has no house rules — but a finding that rests on not knowing the harness is not evidence against the dataset. Its points 2 (`scaffold` "is a feature") and 4 (the +3 shift "undocumented") fail the same way: `feature_columns(container) == ['SMILES']` (claim-auditor #13), and the shift is documented in `MMOL_TO_MOL`, `curation_comments`, `task_summary.changes` and Decision 2.

---

**2. The benzene carve-out the task-gamer calls the dataset's "one real defect" is what SPLIT-31 mandates, word for word**

**Claim.** Task-gamer F1 and blind-reviewer #3 both say the split "does not deliver the declared regime" because the 649 bare-benzene compounds are singleton groups.

**Evidence.** SPLIT-31 (amended 2026-10-26, Lennart, on `qsar_bioconcentration`): *"A molecule without a ring is a group of its own, **and so is each molecule of a scaffold that holds more than a tenth of the molecules**, which is no series and would leave folds of very unequal size (`scaffold_groups`)."* Benzene is 29.7% here. The same carve-out shipped at 34% (`qsar_bioconcentration`) and 18% (`qsar_oral_toxicity`). The definition states it plainly in `splits_comment`, `Grouping.definition` and `task_summary.split`.

**Rule.** SPLIT-31 (Should) prescribes it; SPLIT-30 and SPLIT-4: *"The size of the gap never decides."* The gamer's own fix (one 649-member group) would be a departure from SPLIT-31 with no fact setting this case apart.

**Why it wins.** The gamer argues from the score gap (0.7217 kit vs 0.7519 true-Murcko vs 0.7047 random) — exactly the argument SPLIT-4/SPLIT-30 bar. And the split-auditor measured what the residual overlap is worth: removing *every* close analog (single-linkage Tanimoto-0.7 clusters) moves RMSE by **0.008**, less than the spread over folds; the 146 Tanimoto-1.0 pairs are alkyl homologs whose targets differ by 0.66 log in the median. There is no label travelling across the split to remove.

---

**3. P4 holds under a dedicated attack: the task-gamer found nothing above the noise floor**

**Claim.** Honest evaluation is intact — no leak, no copy, no format channel, no transductive shortcut.

**Evidence.** Task-gamer: *"none found above the noise floor"* (±0.0005 RMSE), after trying string artefacts, row order, kNN read-across, transductive statistics, count encodings, quantisation lattices and the mg/L reparametrisation. Copies: 0 duplicate SMILES, 0 after stereo-stripping, 0 after tautomer canonicalisation, 0 shared InChIKey skeletons — confirmed independently by the column-auditor on **six** keys (adding full InChIKey, neutralised structure, CAS digits, ECFP4-identical-and-same-target) and by the split-auditor across all 30 splits (group overlap **0**). `dataset check`: 0 errors, 0 warnings, nothing accepted.

**Rule.** LEAK-1, LEAK-10, LEAK-19 (all Must) — each tested and held.

**Why it wins.** Under principles step 4, "independent failures are not conflicts": every Must has to hold, and here the P4 Musts *do* hold under adversarial test. The only residue the gamer flags is float-arithmetic noise in the target's last bits (307 of 2,183 values 1–2 ULP off), which he himself discards as unusable ("a deterministic function of the stored value… only exists for rows whose label you already have"). **Conceded, mildest remedy: `round(3)` on the target** — one line, CLEAN-level, no effect on any score.

---

**4. It is worth benchmarking, and the article now lets us say how much headroom there is**

**Claim.** TP-2 and TP-5 are met with room to spare, and the benchmark's ceiling is now a documented number rather than a guess.

**Evidence.** LightGBM 0.715 against a dummy 1.281, beating it on **30 of 30** splits by 44% of its loss; methods separate (LightGBM 0.715 / random forest 0.767 / selected linear 0.954). 2,183 chemicals, 1,761 groups, 587 test groups and 669–794 rows per test fold. No task-probe flag. On the 1,392 compounds this set adds beyond `qsar_fish_toxicity`, methods separate too (0.766 / 0.822). New from the claim-auditor's reading of Figure 3 (p. 662): the sources the target merges disagree with each other at RMSE 0.55–0.67, so an untuned model at 0.715 on a *grouped* split is already near the label's own noise floor.

**Rule.** TP-2 (Should) met; TP-5 (Must) not remotely triggered.

**Why it wins.** Nothing in the panel argues otherwise. The noise-floor figure is a disclosure for the review, not a defect: it is the honest reading of why R² 0.67 should not be read as "much headroom", and it belongs in `curation_comments` in one sentence.

---

**5. The one real Must failure is a false sentence about the source — and the fix is text, with the data, split and metric unchanged**

**Claim.** The claim-auditor refuted three statements: the article is **not** paywalled (the thesis reproduces it verbatim at `publication-theses.unistra.fr`, pages 658–675, read as images), the merge rule **is** documented, and the metric `reason` therefore asserts something false.

**Evidence.** p. 658: *"In case of multiple values per compound, **the median was taken as a representative value. When the ratio between the minimum and the maximum reported value per compound was >10, the entry was discarded**"*, plus OECD-recommended species only, ranges excluded, above-solubility and water-unstable compounds excluded. p. 660: *"Cross-validated determination coefficient was selected as fitness function"*; p. 661: *"the r² determination coefficient and the RMSE parameters are reported"*.

**Rule.** MET-1 (**Must**): the look must be real and recorded. PROV-17 (Must): a paywalled paper that matters is asked for — here it need not be, it is open.

**Why the dataset still ships as defined.** The ladder's second rung (fix the definition) resolves it, and the *declared* metric does not move: on a fixed test fold R² = 1 − MSE/Var(y) ranks every pair of models exactly as RMSE does, so `rmse` is either the source's criterion by identity (MET-11 `source`) or the fallback under MET-5 — and the sibling `qsar_fish_toxicity` ships `rmse` on the same target and the same scale. **Conceded and welcomed:** rewrite the metric `reason`, the "undocumented merge" bullet and the "Not read" bullet from the article, and restate the sibling overlap on the shipped frame (805 of 908, 88.7%, adds **1,378**, not 808/1,392 — the quoted figures are the pre-dedup 2,200). The article makes the dataset *stronger*: builder issue A closes rather than going to the curator, `fit="direct"` no longer needs USE-5's "undocumented and cannot be checked" clause, and it independently confirms the LEAK-22 no-censoring finding and the LEAK-18 absence of stereochemistry ("removal of salts/solvents … removal of stereo information", p. 658).

---

**6. The domain practitioner's Daphnia/algae point is a framing call whose mildest remedy is one sentence of wording — not a data change**

**Claim.** The practitioner wants `pEC50 - DAPHNIA` and `pEC50 - ALGA` shipped as features under USE-6, because REACH Annex VII puts them in the dossier before the Annex VIII fish test.

**Evidence I accept:** the gain is real and consistent — −0.031 RMSE overall, −0.081 on the 55.6% of rows that carry a co-input, same sign in five model families. **Evidence on the other side:** it is 4% of the task's skill; the co-endpoints are present on only 47.1% and 31.4% of rows, and *that presence is itself a record of what the collection covered* — the column-auditor measured the selection signal directly (mean target 4.63 for `daphnia, fish` against 4.08 for `alga, fish`). The practitioner also states the mechanism against himself: the structure already predicts the Daphnia value well.

**Rule.** USE-6 (an input known at the prediction point is legitimate) against LEAK-1 (**Must**: the prediction point is written down first — here *"a substance before it is tested on fish"*, at which moment no aquatic test exists) and PROV-7 (**Must**: the Daphnia endpoint is its own task and its own record). CLEAN-22 keeps out a column that records how the source filled its table.

**Why it wins.** The two framings are both valid; the definition picked one and the panel's disagreement is about which, not about a failure. Under the remedy ladder the mildest fix that resolves the mismatch is **wording**: narrow `use_case` and `known` to the screening point (drop "to fill a registration dossier") and add half a sentence saying why the co-endpoints are not inputs. That keeps the dataset, keeps PROV-7 intact, and leaves the dossier framing available as a separate record later. I concede this should go to the curator as a weighing call with both options on the table — not as a defect.

---

**7. The two precedent departures are conceded: both are small, both keep the dataset, and one is the ladder's first rung**

**7a — `Time: Lost` → `Time: Dated` (precedent-checker F1).** Conceded. SPLIT-32 sets `Time: Dated` *"when the release or a parent source keeps the date … even where the date turns out to carry nothing"*; six siblings including `qsar_fish_toxicity` (dated by Andrej on 2026-11-13 through the ECOTOX bulk release on the CAS-RN, 850 of 908) are `Time: Dated`, and none of this family is `Time: Lost`. The stated reason ("the CAS-RN is a registration number") does not distinguish — the CAS-RN is the *join key* there too. **The leaf does not move**: the walk answers no at `[CAT.next-items]` (SPLIT-37 step 3), confirmed by the split-auditor on both readings. This is a record field and one sentence of `time_basis`.

**7b — repair the three two-formula pairs instead of dropping both rows (precedent-checker F2, PROV-13 Must).** Conceded, and I would go further than the builder: PROV-13 puts repair above dropping, and the column-auditor resolved two of the three from a field the file already carries — CAS **275-51-4** is azulene, C₁₀H₈ (so the C₁₀H₁₈ drawing is wrong); CAS **3347-22-6** is dithianon, C₁₄H₄N₂O₂S₂, matching the `Mol Weight` 296.3 on that very row. The house did exactly this on `qsar_bioconcentration` (6 rows repaired from Wikidata/PubChem). Keep the drawing the registry confirms, drop both rows only for CAS 104653-34-1: **2,185 rows**. Two chemicals, a two-minute fix, and it removes the one Must-ranked ladder step the option table skipped.

**Also conceded, same class (text only):** the censoring note should say what the check found rather than "no sign" — 11 compounds sit at exactly 100 mg/L, the OECD 203 limit concentration, 9 of them from dossier sources (column-auditor 1), now read alongside the article's "values reported as ranges were excluded"; the `splits_comment`'s "no test chemical's scaffold is in training" should give both figures (group id 0%/22.6%, scaffold 60.9%/83.3%) and cite `qsar_fish_toxicity`'s *scaffold-against-random* pair rather than its forward-by-year pair (split-auditor 1–2, precedent F4); the applicability-domain gap and the "DB is worth a small but systematic 0.005 RMSE, dropped under LEAK-1 regardless" belong in the notes.

---

**What this adds up to.** Validity: SEL/USE/LEAK/SPLIT/PROV all hold, one PROV-13 repair applied. Value: TP-2 and TP-5 met with margin; MET-1 fails on a sentence and is fixed by rewriting it, with no change to the declared metric. Quality: a `round(3)`, and a set of wording corrections the claim-auditor has already done the work for. Weighed: source +, shape +, gap 0, risk − now smaller than at screening because the article was found. Nothing on the panel's table reaches the ladder's third rung, let alone the fourth.

</details>

<details><summary>Critic, opening brief</summary>

**Critic's opening brief — `aquatic_toxicity_lunghini_consensus`**

**Position: ship after changes.** The task is real, the data is clean, the gamer found no exploit, and nothing here is a Must that cannot be fixed — so I ask for no exclusion. But the folder as written misstates its own source in three places, asks the curator two questions the source already answers, and describes a split that is not the split it ships. Those are definition fixes, and they should land before it goes out.

---

**1. The stated prediction point and the shipped inputs contradict each other (P3; USE-1 Must, USE-6 Must)**

**Problem.** `task_summary.use_case` puts the actor at the dossier: "to classify and label it **and to fill a registration dossier**". `curation_comments` puts him earlier: "a substance before it is tested on fish". The two moments have different inputs, and the definition drops the Daphnia and algae columns on the earlier reading while advertising the later one.

**Effect on the real task.** At the dossier moment the Annex VII values exist by construction — Daphnia (TG 202) and algae (TG 201) are required at 1 t/y, the short-term fish test (TG 203) only at 10 t/y — so a model fitted here answers a question the stated actor does not ask. USE-6 is a Must: anything known at the prediction point is a legitimate input, and dropping it changes the task.

**Evidence.** Domain practitioner, §1: the two columns are present on 55.6% of shipped rows and are worth −0.031 RMSE overall and −0.081 on the rows that carry one (9/9 splits, same sign for five model families). Column auditor §4: the pair alone scores 1.064 against a dummy of 1.281. PROV-7 settles that Daphnia is a separate *target*; it says nothing about whether a known value may be a *feature*.

**Remedy (mildest that works).** Fix the definition's wording: narrow `use_case` and `known` to the untested-substance screening point and drop "to fill a registration dossier". Shipping the two columns instead is the practitioner's preference and a legitimate alternative — that one is a weighing call for the curator. What must not ship is the folder sitting between the two.

---

**2. "The merge is undocumented and the article unreachable" is false, and it is load-bearing (P3/P5; PROV-17 Must, USE-5 Must, EV-2)**

**Problem.** Three places in the definition — `curation_comments`' merge bullet, its "Not read" bullet, and `fit_reason` — state that the companion article could not be read and that the consensus rule is unknown. The article is open access and the claim auditor read it.

**Effect on the real task.** The target's construction rule is a USE-5 question (what the actor acts on), and the source answers it: **the median of the per-compound values; any compound whose min/max ratio exceeded 10 discarded; reported ranges excluded; OECD-recommended species only; larval-stage studies and above-solubility compounds removed**. That is a better basis for `fit="direct"` than the ADORE agreement the definition leans on, and it also confirms the no-censoring and no-stereochemistry notes from the primary document. Builder issue A ("the undocumented merge") should be closed, not put to the curator.

**Evidence.** Claim auditor, claim 18 and the header section: `https://theses.fr/2020STRAF016/document` → the Unistra thesis PDF, which reproduces the article verbatim at journal pages 658–675. I re-ran that fetch myself: HTTP 200, `application/pdf`. PROV-17 is a Must about what you may write when you go on without the text; here you did not have to go on without it.

**Remedy.** Replace the two bullets and `fit_reason`'s clause with the rule as quoted, cite the open route in the sources, keep `fit="direct"`. The README ships these sentences to every reader of the benchmark (README lines 88, 215, 223), so this is not an internal note.

---

**3. `fit="direct"` is argued without the population gap the source itself measured (P3; USE-8 Must, USE-9)**

**Problem.** `fit_reason` names two gaps (undocumented consensus, no species) and no numbers. It does not say that the shipped cut is the **public** data *before* the authors extended their models with industrial compounds, while the use case names an industrial assessor.

**Effect on the real task.** The actor's population is his inventory; the test rows are public-database chemicals, and the authors state the difference in their own words: "industrial data performances were noticeably lower than those on public data", final models "updated with the inclusion of new industrial compounds, extending applicability domain". Under the shipped split, error tracks that distance: RMSE 0.87 where the nearest training chemical is ≤0.40 Tanimoto (1,995 of 6,549 scored test rows) against 0.49 above 0.9. A benchmark user reading `direct` with no numbers will read the headline 0.715 as the number the assessor gets.

**Evidence.** Split auditor F3; domain practitioner §2 (also the absence of substances with no effect up to water solubility — CLP's "no acute toxicity" case — which carry no number and so cannot be in the file: a `Selection Bias` marker is warranted).

**Remedy.** Two sentences in `fit_reason`/`curation_comments`: the source's quote, the distance-banded RMSE, and that the label's own interspecies scatter (fathead vs rainbow trout r 0.927, 68% within 0.5 log) is of the order of the best model's error — the claim auditor's reading of the paper's Figure 3 puts the inter-database noise floor at 0.55–0.67 RMSE against our 0.715. I do **not** ask for `approximate`: `qsar_fish_toxicity`, same endpoint, same curator, 2026-11-12, is `direct` on the same analog reading. Keep `direct`, state the gap.

---

**4. The split's own description states the opposite of what the split does (P4; SPLIT-37 step 5, SPLIT-32, Should)**

**Problem.** `splits_comment` says "no test chemical's scaffold is in training, against 22.3% under random splits", and `task_summary.split` says "a test chemical belongs to a family the model has not seen". Measured: **60.9%** of test chemicals share their actual Bemis-Murcko scaffold with a training chemical (83.3% at random). The 0%/22.3% pair is the share whose *group id* is in training — a different quantity, and the one that flatters the split.

**Effect on the real task.** 60.7% of rows (676 ring-less, 649 bare benzene at 29.7%) are groups of one, so for most of the set this is a random split. The gamer measured the consequence end to end: kit grouping RMSE 0.7217, true Murcko grouping 0.7519, plain random 0.7047 — the shipped regime sits about a third of the way from the scaffold end toward the random end, while the task card promises the scaffold end. A curator reading the current sentence cannot see that.

**Evidence.** Split auditor F1 and §3 (the decomposition: the split removes 59% of close analogs where it can group, 8.3%→3.4%, and nothing on the 60.7% it cannot); task gamer F1.

**Remedy.** **Wording only — I am not asking for a re-split.** SPLIT-31 mandates the benzene carve-out, every sibling does the same, and the residual overlap is worth 0.008 RMSE (split auditor §3), so the split is right. Give both figures (group id 0%/22.6%, scaffold 60.9%/83.3%) and name the benzene bucket in `task_summary.split`. Same bullet: `Time: Lost` departs from SPLIT-32, which sets `Time: Dated` when *a parent source* keeps the date "even where the date turns out to carry nothing" — six sibling records are `Dated`, including `qsar_fish_toxicity`, dated by Andrej on 2026-11-13 through the ECOTOX release on the CAS-RN, 850 of 908, and 808 of those chemicals are in this file (precedent checker F1). The leaf does not move; the collection fact and one sentence do.

---

**5. The metric's recorded reason asserts something false (P6; MET-1 Must, MET-5)**

**Problem.** `Metric.fallback(reason=…)` says "its evaluation section is behind a paywall and could not be read, so no ranked criterion of the source was found". MET-1 is a Must to look at the paper that defined the task *and record where you looked*; the recorded answer is wrong, and a deliberate criterion exists: p. 660, "Cross-validated determination coefficient was selected as fitness function"; p. 661, r² and RMSE reported.

**Effect on the real task.** Probably none on scoring — on a fixed test fold R² = 1 − MSE/Var(y) ranks every pair of models exactly as RMSE does, so `rmse` is right either way, and the practitioner confirms it selects the model his banded decision would pick (Kendall tau 0.83 per split against CLP band accuracy). The defect is that a Must-rule's recorded evidence is false, and it is the reason a reader would check.

**Evidence.** Claim auditor, claim 19. Precedent `open_soil_spectral_library` (MET-5) treats a named tuning criterion as the source's metric.

**Remedy.** Rewrite the reason from the article with the open route cited; put one line to the curator — keep origin `fallback`, or move to `source`/MET-11 `source` with the cross-validated determination coefficient as the original and the RMSE identity in `definition`. No re-scoring either way.

---

**6. The repair rung of the ladder was skipped on the three two-formula pairs (P5; PROV-13 Must)**

**Problem.** For the 3 substances drawn under one CAS-RN with two molecular formulas, both rows are dropped because "nothing in the file says which is meant". The registry does say, and the definition itself names the answer for one of them.

**Effect on the real task.** Small — 2 to 3 chemicals of 2,183 — but it is a Must-ranked ladder step the option table does not offer, and the stated reason is wrong rather than merely conservative.

**Evidence.** Column auditor F2: CAS 275-51-4 is azulene, C10H8 (the C10H18 row is the wrong drawing; the two targets are 4.154 and 4.168, one measurement); CAS 3347-22-6 is dithianon, C14H4N2O2S2, which is the `Mol Weight` that row already carries; the third (104653-34-1) is not resolvable from the registry number alone. Precedent checker F2: `qsar_bioconcentration` repaired six rows by looking CAS numbers up in Wikidata and PubChem and dropped only rows with no partner to repair from.

**Remedy.** Two registry lookups; keep the drawing whose formula matches, drop both rows where it does not resolve (2,185–2,186 rows). If the curator prefers the current drop, the note must stop saying the file does not say which is meant — the CAS-RN is in the file.

---

**7. Several documented numbers do not describe what we ship (P7/P5; EV-2, writing — Should)**

**Problem and evidence**, each measured by a panel agent:

* **The sibling overlap is stated on 2,200 rows we do not ship.** Definition: "holds 808 of those 908 (89.0%) … adds 1,392". Shipped frame: **805 (88.7%), 783 by CAS-RN, 568 within 0.01, adds 1,378** (claim auditor, claim 20). This is the number the open `qsar_fish_toxicity` decision turns on and that gets quoted forward, so it is worth more than its size.
* **"Dropping `DB` costs nothing measurable"** — paired over all 30 shipped folds it is worth 0.0045 RMSE on 25 of 30 folds, p 1.5e-5: small and systematic, not noise (claim auditor, claim 21). The decision is unaffected (LEAK-1 drops it whatever it scores); only the sentence overstates.
* **"No sign that the values are censored"** — 11 compounds sit at exactly 100.000 mg/L, the OECD 203 limit-test concentration, against 45 others across the whole ±10% band, and 9 of the 11 come from ECHA/NITE/Literature, the dossier sources where "LC50 > 100 mg/L" is the standard outcome (column auditor F1). 0.5% of rows, no data change asked — but the sentence should say what the check found.
* **Both sibling citations in `splits_comment` are wrong**, and the corrected one cuts against the claim: the quoted pairs are forward-by-date figures, and on the proper scaffold-against-random comparison this set removes *less* overlap than any molecule dataset in `molecules.md`'s table (precedent checker F4, split auditor F2).
* Minor: 307 target values carry 1–2 ULP float residue from the `+3` shift (task gamer F2) — `round(3)`.

**Remedy.** Restate each on the shipped frame, fix the two citations, reword the censoring and `DB` sentences. No data change except the optional rounding.

---

**What I attacked and dropped**

* **"There are no tabular features; LightGBM scores R² −0.003" (blind reviewer §1–2).** An artefact of the clean room. `SMILES` is declared in `special_features`, `feature_columns(container)` is exactly `['SMILES']` with `scaffold` excluded (claim auditor, claim 13), and the house contract is that a benchmark encodes a special feature by its kind. Four shipped siblings ship the same way. Not a point.
* **A re-split.** SPLIT-31 mandates the carve-out, the residual near-analog overlap is worth 0.008 RMSE, and a Tanimoto-1.0 neighbour carries a median 0.66 log difference in target. The split stands; only its description is wrong (point 4).
* **The gamer's exploit search.** Nothing above the ±0.0005 noise floor. I have no leak to argue.
* **The task's worth (P6).** LightGBM 0.715 against a dummy 1.281, wins on 30 of 30 folds, methods separate on the 1,378 chemicals this set adds. No `Too Small`, no triviality. A quality problem is not a reason to exclude a real task, and I am not using one as such.

</details>

<details><summary>Advocate, rebuttal</summary>

**Advocate's rebuttal — `aquatic_toxicity_lunghini_consensus`**

The critic and I reach the same verdict (**ship after changes**) and the same remedy on five of seven points. He asks for no exclusion, no re-split, no re-score, and no data change beyond the PROV-13 repair and `round(3)`. So this rebuttal is short: I concede most of it, and dispute three things — one substantive (a marker), two of framing, plus one arithmetic correction.

---

**1. Prediction point — concede the defect, dispute the rule it is filed under.**

Conceded: `use_case` ("and to fill a registration dossier") and `curation_comments` ("a substance before it is tested on fish") name two different moments, and the folder must not ship sitting between them. The remedy is the one we both wrote: narrow `use_case` and `known` to the screening point, drop the dossier clause.

Disputed: this is not a **USE-6** failure. USE-6 ("anything known at the prediction point is a legitimate input") only bites *after* USE-1 fixes the prediction point; it does not choose the moment. Fix USE-1's sentence and USE-6 is satisfied, because at "a substance before it is tested on fish" no aquatic test exists. It is a writing defect under USE-1, not a validity failure — which decides whether the curator reads an issue or a weighing call.

Also disputed: "at the dossier moment the Annex VII values exist by construction." In the shipped file they exist on **55.6%** of rows (Daphnia 47.1%, algae 31.4%), so even on the dossier reading the file does not supply the dossier's inputs. And *which* rows carry them records what the collection covered, not what an assessor holds: mean target 4.63 on `daphnia, fish` against 4.08 on `alga, fish` (column-auditor §4). That is the CLEAN-22/LEAK-1 objection to shipping them, and the reason the earlier moment is the honest one to write down. Shipping the two columns stays a legitimate alternative for the curator — as the critic agrees.

**2. The article is open and the merge is documented — conceded in full.** This is my own point 5. Rewrite the merge bullet, the "Not read" bullet and `fit_reason`'s clause from p. 658, cite the Unistra route. Builder issue A closes rather than going to the curator, and the article independently confirms the LEAK-22 (ranges excluded) and LEAK-18 (stereo removed) notes.

**3. The population gap — concede the sentences, dispute the `Selection Bias` marker.**

Conceded: `fit_reason` should carry the authors' "industrial data performances were noticeably lower" quote, the distance-banded RMSE (0.87 at ≤0.40 Tanimoto on 1,995 of 6,549 scored test rows against 0.49 above 0.9), and the label's own noise floor (0.55–0.67, Figure 3) against our 0.715. Keep `direct`.

Disputed: the marker. `selection.md`, "Selection bias", the **"No marker when"** list, fourth bullet (added on the PR #16 review, Lennart, 2026-10-27):

> *tested compounds stand for the candidates a screen would test (the QSAR sets): how far a new candidate lies from the tested ones is a question for the split.*

That clause names this family by name. Both gaps the critic cites — the industrial inventory, and the substances with no effect up to water solubility — are exactly "how far a new candidate lies from the tested ones". None of the five QSAR siblings (`qsar_fish_toxicity`, `qsar_oral_toxicity`, `qsar_bioconcentration`, `qsar_aquatic_toxicity`, `qsar_tid_11`) carries the marker.

The marker is also not free. USE-8 ties it to the fit: *"the fit is direct when the real-world setting of the use case has the same bias, and approximate when it does not."* Adding it while keeping `direct` asserts that the screening setting shares the bias — the opposite of the critic's own argument. If the curator wants the fit reopened, it should be reopened **for the family**: `use_case.md`'s USE-8 case row for `qsar_fish_toxicity` / `qsar_aquatic_toxicity` is still marked `proposed` and is open for precisely this question. Route it there; don't settle it with a marker in this folder.

**4. The split's description — concede the wording, dispute the gloss.**

Conceded: "no test chemical's scaffold is in training" is false of Bemis-Murcko scaffolds (60.9% share one, 83.3% at random) and true only of group ids (0% / 22.6%). The existing caveat ("similar but not identical scaffolds can be on both sides") does not cover two bare-benzene chemicals, whose scaffolds are *identical*. Give both figures, name the benzene bucket in `task_summary.split`, and fix the two sibling citations to the scaffold-against-random pair.

Disputed: "the shipped regime sits about a third of the way from the scaffold end toward the random end." That measures against a split SPLIT-31 forbids. The gamer's 0.7519 "true Murcko" grouping puts the 649 benzene chemicals (29.7%) in one group, and SPLIT-31 as amended (2026-10-26, Lennart, on `qsar_bioconcentration`) carves them out word for word; SPLIT-4 bars the score gap from deciding. The honest sentence is "the carve-out SPLIT-31 mandates leaves 60.7% of rows as singletons, and the residual near-analog overlap is worth 0.008 RMSE" — not a ladder whose top rung is not an option. We agree on no re-split; I only ask that the curator not be handed 0.7047 / 0.7217 / 0.7519 as a menu.

**5. The metric reason — conceded, and I go one step further than the critic.** The recorded reason is false and must be rewritten. On origin I'd not leave it on `fallback`: MET-5's own case list has `open_soil_spectral_library` — *"tunes and cross-validates by RMSE on log1p …, grades by CCC with RPIQ: the tuning criterion kept."* p. 660's "cross-validated determination coefficient was selected as fitness function" is the same shape, so the source does have one deliberate criterion, and MET-11 `source` covers shipping `rmse` for it: *"a metric that ranks every pair of models the same by identity counts"*, with R² = 1 − MSE/Var(y) on a fixed test fold stated in `definition`. Recommend `source`; no re-scoring either way.

**6. The PROV-13 repair — conceded; we asked for the same thing.** One correction: the count is **2,185**, not "2,185–2,186". Each repaired pair is one substance entered twice (azulene's two targets are 4.154 and 4.168, one measurement), so LEAK-19 keeps one row of the pair, not both: 2,183 + 2 = 2,185.

**7. The misstated numbers — conceded, every item.** These are my points 5 and 7. Two notes: the sibling overlap correction (805 of 908, 88.7%, adds **1,378**) is worth more than its size because the open `qsar_fish_toxicity` decision turns on it — agreed. And on `DB`: the sentence overstates (0.0045 RMSE on 25 of 30 folds, p 1.5e-5, small and systematic), but the reword changes no decision — LEAK-1 and CLEAN-22 drop the column whatever it scores.

---

**Where we end up.** No Must survives that cannot be fixed by text plus one two-row repair. Three narrow disputes are left for the mediator: (a) whether point 1 is a USE-6 validity failure or a USE-1 writing defect; (b) whether a `Selection Bias` marker is added here — I say no, on `selection.md`'s QSAR clause and five siblings, and the fit question goes to the family's open USE-8 row instead; (c) whether the metric origin moves from `fallback` to `source` — I say yes, on MET-5 and `open_soil_spectral_library`. Nothing on the table reaches the remedy ladder's third rung.

</details>

<details><summary>Critic, rebuttal</summary>

**Critic's rebuttal — `aquatic_toxicity_lunghini_consensus`**

Our positions now nearly coincide: ship after definition fixes plus one repair, no exclusion. I concede five of the advocate's seven points outright. The live disagreement is point 6 — not the remedy, which we agree on, but the three rules the advocate uses to prefer one option, which do not say what the brief says they say.

---

**1. Blind reviewer's "R² = −0.003, not a tabular task" — conceded in full.** I dropped it in my own brief for the same reason (CLEAN-24 as amended, `feature_columns(container) == ['SMILES']`, five siblings the same). It is not a verdict-level objection.

**2. The benzene carve-out — conceded; one qualification on how SPLIT-4 is used.** SPLIT-31 mandates it, the residual close-analog overlap is worth 0.008 RMSE, and I asked for no re-split. But SPLIT-4/SPLIT-30 bar the score gap as a reason to *change* a split; they do not bar it as evidence about what the split *is*. The gamer's 0.7217 / 0.7519 / 0.7047 is the second use, and it is why the description has to change. The advocate concedes the wording at 7, so the remedy is agreed — I only add that both figures (group id 0%/22.6%, scaffold 60.9%/83.3%) and the benzene bucket must appear in `task_summary.split`, the sentence a benchmark user reads, not only in `splits_comment`.

**3. P4 holds, no exploit above the noise floor — conceded.** I argued the same. `round(3)` on the target is the whole residue.

**4. Worth benchmarking — conceded, one number corrected.** "1,392 compounds this set adds" is the pre-dedup frame; on what ships it is **1,378** (claim auditor 20) — the advocate restates this correctly at point 5, so the brief contradicts itself once. The Figure 3 noise floor (0.55–0.67 inter-database RMSE against our 0.715) is the right disclosure and belongs in `curation_comments`.

**5. "The single Must that fails is MET-1" — remedy conceded, the count disputed.** The rewrite from the article is exactly what I asked for, and `rmse` stays (R² and RMSE rank identically on a fixed fold). But three Must-ranked items fail here, not one:
* **MET-1** — the recorded reason asserts a paywall that does not exist (p. 660, "Cross-validated determination coefficient was selected as fitness function").
* **PROV-17** — it governs what you may write when you go on without the text. Three sentences in the shipped README (lines 88, 215, 223) tell every reader the article could not be read and the merge rule is unknown. That is a false statement in the product, not an internal note.
* **PROV-13** — the advocate's own 7b concedes the repair rung was skipped.

All three are fixed by text plus a two-row repair, so nothing about shipping changes; the curator should just see three corrections rather than one. One further fact the advocate's "the article closes builder issue A" overlooks: the deposit's fish column holds 2,200 rows while the paper modelled **2,110** (claim auditor, p. 658 / Table 2) — 90 unexplained, where algae and Daphnia match exactly. Issue A closes on the merge rule; that residual goes in the provenance note.

**6. Daphnia / algae — the remedy is agreed; the three rules cited against shipping the columns are disputed.** The advocate and I both put this to the curator as a weighing call with both options. My dispute is that the option text must not carry rule citations that do not hold.

* **LEAK-1 does not adjudicate which moment is right.** Its text is "Write down the prediction point and the use case first (USE-1, USE-3)" — a procedural rule that makes you fix a moment before testing columns against it. It is not authority for whichever moment happens to be written. The column auditor states the circle in its own words: "They are out by LEAK-1 *as the definition declares* the moment." The advocate's "at which moment no aquatic test exists" restates the disputed premise as its own proof. The moment is settled by USE-1/USE-3, and there the practitioner's evidence is one-sided: REACH Annex VII 9.1.1 (Daphnia, TG 202) and 9.1.2 (algae, TG 201) bind at 1 t/y, the short-term fish test at Annex VIII 9.1.3 at 10 t/y — at the dossier moment the two values exist by construction. The definition advertises that moment and then drops them.
* **PROV-7 is about duplicates, not about features.** "Records that share a source but give different tasks are not duplicates." Nothing in it forbids a column being a target in one record and a known input in another; the practitioner says so explicitly, and USE-6's own case table has that exact shape (`bias_correction_r_bias_correction_r_2`: the LDAPS forecast the task corrects is the task's input).
* **CLEAN-22 is the rule that keeps features in** — its heading is "Keep every relevant feature"; columns leave for what they are, never for how many. The `qsar_bioconcentration` row the advocate leans on dropped `logKOW_type`, a flag recording *how the authors filled their table* (measured vs predicted), expressly "not a property of the chemical". A Daphnia 48-h EC50 is a measured property of the chemical. What is a collection record here is the *missingness pattern* (47.1% / 31.4%, mean target 4.63 for `daphnia, fish` against 4.08 for `alga, fish`) — a genuine point, but it argues for care in the note, not for discarding a measured value.
* **"About 4% of the task's skill" understates it where it applies.** On the 55.6% of rows that carry a co-input, 0.6616 → 0.5808 is 12% of that error, better on 9/9 splits, same sign in five model families.

So: both options go up with these numbers; the option text cites USE-6 and USE-1 on one side and the missingness-pattern argument on the other, and drops LEAK-1, PROV-7 and CLEAN-22 as settling it.

**7. Both precedent departures — conceded, as I asked.** 2,185 rows (azulene C₁₀H₈, dithianon C₁₄H₄N₂O₂S₂ confirmed by the `Mol Weight` on that row; both rows dropped for 104653-34-1), and `Time: Dated` with the leaf unmoved. The advocate goes further than the builder here and is right to.

One gap in the advocate's "also conceded" list: it accepts the applicability-domain sentences but is silent on the **`Selection Bias` marker** the practitioner asks for (substances with no effect up to water solubility carry no number and so cannot be in the file). I keep that ask; it is a marker, not a data change.

---

**Where this leaves the curator.** Nothing on the table reaches exclusion, and neither of us argues for it. The disagreement that remains is one framing call (Daphnia/algae), which both of us hand over, and the reasons printed beside it.

</details>

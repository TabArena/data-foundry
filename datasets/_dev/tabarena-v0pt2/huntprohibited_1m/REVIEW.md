# huntprohibited

**Outcome:** added as `huntprohibited_1m`. A binary classification of Avito ads (blocked by moderators or not) from
Russian title, description and form text plus a few structured columns, IID (`ForcedIIDFromTemporal`), sub-sampled
to 1.5M ads. The AI recommends shipping it; the forced IID split and the weight of the text are for the curator.

**Main points:** IID, because the file has no time index (the record asks for temporal). Text carries most of the
signal.

**Record fields that disagree with the definition:**

- `required_split`: record `Temporal (NON-IID), ?`, definition `Random (IID)`.
- `tag`: record `Non-IID (Temporal)`, definition `Random (IID)`.

**Record judgment:** valid with concerns: the text carries most of the signal (Russian), the temporal split the
record asks for cannot be built, and the sellers cannot be grouped (issues 1, 2, 4).

**Issues for Lennart:**

1. **Temporal split asked for, no time index available.** The record says `required_split: Temporal (NON-IID), ?` and
   tags `Non-IID (Temporal)`. The data page: training ads "sampled from Dec 2013 - Mar 2014", test ads "from Apr 2014";
   but the file has no date, and the host wrote "The ids have been randomly assigned" (discussion 9554). Checked: block
   rate (6.81-6.93%), real-estate share and seasonal words ("новый год", "8 марта") are flat over the ten id deciles
   (README decision 2), and the April ids fill every train-id decile at 10.0% with no shared id; the verifier adds that
   the id-sorted file has a next-row label match of 0.8718, equal to chance (0.8718), and that block rate and seasonal
   words are flat over 100 position bins (lag-1 autocorrelation -0.09 to 0.16). Implemented: IID splits with
   `ForcedIIDFromTemporal` (as aps_failure, forest_fires, labour_inspection_compliance). Alternative: none from the
   released files (test labels were never published). Question: keep the forced-IID version, or drop it because the
   source task is temporal? If kept, the record's split fields should say IID.

2. **Text carries most of the signal (criterion 4A, the record's own concern).** Data page: "Data for this competition
   consists mainly of Russian text." On the same fold (fold 0, 1M train / 500k test): structured columns alone ROC AUC
   0.9324 (AP 0.511); LightGBM on structured plus 32 TF-IDF SVD dims per text column 0.9870 (AP 0.893); TF-IDF logistic
   regression 0.9944 (AP 0.950). The TabArena default pipeline gives models each text column as a 32-dim
   Qwen3-Embedding-8B vector with n-grams off (tabarena `text_cache.py` `SEMANTIC_EMBEDDING`,
   `model_agnostic_default_preprocessing.py` `enable_text_ngram_features=False`), so the text cache must embed about
   2.67M distinct strings (titles 739k, descriptions 1.45M, attrs 479k). A bag-of-words linear model suffices (the 2014
   winners used SGD/SVM on TF-IDF plus a random forest over category, subcategory and counts), so no deep text model is
   required, but the benchmark ranks pipelines by how they encode Russian text. Implemented: kept, text as string
   columns (precedents in the copy: emscad, consumer_complaints_1m, mercari_price_suggestion). Alternative: exclude
   under 4A. My view: keep, as the record decided.

3. **`attrs` kept as one JSON string.** It is the category's form (79 keys, 1-12 per ad; 72 keys on at least 1,000 ads;
   6,004 strings malformed: quotes written as `/"`, tabs). 735,975 ads, all real estate, repeat a key: 735,772 give
   `Этаж` and `Этажей в доме` twice (a range or class and the exact value); json.loads keeps the later value, which is
   the exact floor in 550,009 and the range in 185,763 of them, so an unpacking needs a rule (both values, or the exact
   one). It is the strongest single column in the task probes (ROC AUC 0.945). Implemented: string column, parsing left
   to the pipelines (the winners treated it as text). Alternative: unpack into up to 72 sparse categorical/numeric
   columns with Russian keys (kickstarter decodes its JSON fields), using the host's regex fix (discussion 9677) and a
   rule for repeated keys. Question: which do you prefer?

4. **Sellers ("malicious users" in the CC comment).** The file has no seller id, and phones, e-mails and URLs are masked
   without a hash, so ads cannot be grouped by seller exactly (no similarity clusters, per the guidelines). Exact copies
   are dropped (32,103 plus 212 conflicting ads). Edited reposts stay: 128,355 of the 3,963,488 kept ads share a 30+
   character description with another ad (10.2% blocked against 6.9%); like for like (fold-0 train as the reference),
   1.39% of the shipped test ads have such a copy in train, against 0.50% of the deduplicated April ads (99.4% label
   agreement), so the random split adds copies, but they move fold-0 ROC AUC by at most 0.002. Implemented: IID with
   exact deduplication. Alternative: group by exact description text (an exact key, as emscad's identical profile text);
   the 0.002 above bounds what it would change. Question: does the "detect users, not ads" remark need more than this?

5. **Hidden-group hits dismissed.** `subcategory` (gap 0.816) and `attrs` (gap 0.250) are attributes every new ad has;
   holding their values out measures generalisation to unseen categories or form values, not entity memorisation.
   Implemented: no re-split. Question: agree?

6. **`is_proved` as an alternative label** (the CC comment: it "could be used to sub-filter data"). 83,810 of 274,996
   blocked ads were blocked by an experienced moderator. Implemented: `is_proved` dropped, target `is_blocked` as in the
   competition. Alternative: positives = proved blocks only, dropping the 191,186 unproved blocked ads (cleaner label,
   not the source's target). Recommendation: keep `is_blocked`.

7. **Real estate kept.** 1,149,136 ads (28.8%), 0.12% blocked; the winners left them out of training (discussion 10178).
   They are easy negatives that lift ROC AUC (subcategory alone 0.908). Verifier, fold 0: without the real-estate test
   ads (28.4% of them, 186 positives) text LR 0.9944 to 0.9925 (AP 0.950 to 0.951), structured LightGBM 0.9324 to 0.9071
   (AP 0.511 to 0.514). Implemented: kept, since moderation covers every ad. Alternative: drop the category (2.8M ads
   remain, still a `_1m` version).

8. **Licence and content.** Kaggle Competition Rules: use limited to the competition, no redistribution. The ads include
   illicit or offensive content (rules page warning), and dating ads carry first names and ages (Avito masked phones,
   e-mails and URLs). Noted, not a verdict reason.

9. **`Spatial` tag?** `attrs` holds a free-text address ("Адрес": a street, sometimes the town) for 901,011 ads (22.5%),
   all real estate. Implemented: no `Spatial` tag (no region or coordinates). Alternative: add the tag. Your call.

---
unique_name: huntprohibited
name: huntprohibited
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- Free Text (Sentences)
- Larger IID Data
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2014'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/avito-prohibited-content/data?select=avito_train.zip
v2_path: datasets/_dev/tabarena-v0pt2/huntprohibited_1m/dataset.py
source_row: 642
type_adapter_id: curation-record-v1
---

## Comments

CC: "Russian text; text to features script exists; free-text categorical in json format, extra leaking column, that could be used to sub-filter data; close_hours leaking test data; some count features from text; likely some problem with malicious users, who one should detect instead of the ads itself"

needs some basic preprocessing as shown by the hosts; non-English language might be a problem for downstream models

**Assessment (AI, 2026-10-07):** The temporal split cannot be built: the file has no date, and the competition admin wrote "The ids have been randomly assigned" (Kaggle discussion 9554); block rate and seasonal words are flat across id deciles. Defined as IID `huntprohibited_1m` (ForcedIIDFromTemporal; 1.5M of 3,963,488 ads after dropping 32,315 duplicates). `close_hours` is post-outcome ("not available at scoring phase", discussion 9729) and `is_proved` exists only for blocked ads; both dropped. With no seller id, sellers cannot be grouped; 1.39% of test ads share a description with a train ad (0.50% of April ads), worth at most 0.002 ROC AUC. Text carries most of the signal (fold 0): structured columns ROC AUC 0.932, TF-IDF text 0.994.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case -, source +, shape +, no known risk. A large ad-moderation task, but Russian text carries the signal and the temporal split is lost, so it mostly ranks text encoders.

**Assessment (AI, 2026-10-20):** review panel (full tier): ship after changes, all to text in dataset.py; data, cleaning, target and split unchanged. The notes now say what a date would change (the April labels were never published, so the cost of the random split cannot be measured), name the second gap of the fit (content only: no seller, region, posting time or photos), the cohort (closed ads, blocked for illicit content or never blocked) and that the row is the ad's last version (`price` is the final price), and keep `price` codes 999,999,999 (29 ads, 65.5% blocked) and 1 (19.0% blocked) as seller-entered. Sellers: the label is per ad (data page wording); grouping by exact description keys gives ROC AUC 0.99384 / 0.99386 against 0.99390 random (1.4-4.9% of test ads have a near copy in train, 99.5% with its label); the call against emscad's poster grouping and the `Spatial` tag are open in REVIEW.md. Text against structured (fold 0): structured columns ROC AUC 0.932 (AP 0.51), LightGBM with TF-IDF SVD 0.987, TF-IDF logistic regression 0.994 (AP 0.95). Priority 3: gap -, use case -, source +, shape +, risk - (no thin domain, problem type or regime; the fit is approximate; Avito's own competition data; 1.5M ads with categorical, string and numeric features; no leak left and the open issues raise none).

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric set to `average_precision` (was the default ROC AUC) for the competition's AP@k (Kaggle API: "AP@{K}"; k = 32,500 per the participants). On fold 0 of the shipped splits, over eight pipelines (LightGBM on the structured columns, TF-IDF logistic regressions, two blends; AP 0.51 to 0.95), average precision ranks them as AP@k at k = 12,000 and at k = 34,324 (the fold's blocked ads), Kendall tau 1.0, and at k = 17,162 with tau 0.93; ROC AUC ranks them the same way. The notes name AP@k. Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source average_precision_at_k k=12500 — AP@{K} (https://www.kaggle.com/competitions/avito-prohibited-content/overview/evaluation).

CC (2026-10-22, Lennart): issue 4: (a), keep the random split by ad (exact copies dropped; the per-ad label and the grouped run are the fact that sets it apart from emscad). Issue 9: (a), no `Spatial` tag, with the reason in the notes (the addresses sit inside one category's form text; no geographic column).

**Assessment (AI, 2026-10-22):** date check (Lennart's note): no per-ad date or order; `itemid` is random (April ids spread evenly over train ids, KS p = 0.17). A used-car form change during December-March bounds the cost of the random split at about 0.002 ROC AUC and 0.02 AP (old form to new, TF-IDF logistic regression, 4 seeds). The competition validated at random and local scores tracked the leaderboard. The notes give the bounded cost; issue 10 asks to confirm the random split. Scripts: local-data-warehouse/_runs/2026-10-22_marks/huntprohibited/.

CC (2026-10-22, Lennart): issue 10: keep the random split (no date recoverable).

**Assessment (AI, 2026-10-22):** all issues settled; REVIEW.md removed. Not built yet.

## Reference

Kaggle

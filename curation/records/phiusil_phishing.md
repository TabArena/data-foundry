---
unique_name: phiusil_phishing
name: PhiUSIIL Phishing URL (Website)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Data Quality Issue
tags:
- Larger IID Data
collections:
- New (BeyondArena)
original_source: Other
year: '2024'
domain: technology & internet
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
- https://doi.org/10.1016/j.cose.2023.103545
source_row: 2
type_adapter_id: curation-record-v1
---

## Comments

Recent dataset for phishing website detection, best I know so far (AT). Features extracted from website source code. Might also be approached with LLMs, but since the paper is recent that's not a concern. Might need to double check that the feature extraction doesn't introduce leaks

Discussion: unclear if this is grouped data or not!

**Assessment (AI, 2026-10-07):** Recommend excluding it (`Data Quality Issue`). The two classes were collected differently, and every feature family shows it. All 134,850 legitimate rows are ranked domains written as https://www.<host> with no path, a form only 627 of the 100,520 phishing URLs share (URL features alone: AUC 0.9989). The phishing pages were fetched after the URLs were listed: 50.5% of phishing rows sit on 115 shared pages, none with a password field. A fixed rule with no training reaches AUC 0.9998. Andrej's leak question: the definition drops URLSimilarityIndex, Title and the two title scores, which does not change this. Hosts repeat only among phishing rows, and a host-grouped split scores the same. The file first appeared on Mendeley Data (2023).

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape +, risk - (Issue 1: run recommends exclusion; collection artefacts separate classes (fixed rule AUC 0.9998)). Not useful: a fixed rule solves it because phishing and legitimate rows were collected differently; no version of the file is a valid task.

**Assessment (AI, 2026-10-20):** The review panel recommends `No` with `Data Quality Issue` (the curator's call). The two classes were collected in different forms (LEAK-13 to LEAK-15, Must): every legitimate row is a ranked homepage written as https://www.<host>, and 50.5% of the phishing rows sit on 115 pages shared across hosts, such as takedown and 'site not found' pages fetched after the URL was listed (LEAK-10). A fixed rule with no training reaches ROC AUC 0.9998, the URL features alone 0.9989, the page features alone 0.99994, and every split (random, by host, by registered domain) ROC AUC 1.0. Mendeley v1 and v2 hold the same file, so there is nothing to repair from; `Trivial` is not proven (TP-4). Priority 2: gap -, use case -, source +, shape +, risk - (the fit is approximate, as the negatives are ranked homepages only; the panel recommends not to ship).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: 19 columns (IsDomainIP, HasObfuscation, IsHTTPS, HasTitle, HasFavicon, Robots, IsResponsive, NoOfURLRedirect, NoOfSelfRedirect, HasDescription, HasExternalFormSubmit, HasSocialNet, HasSubmitButton, HasHiddenFields, HasPasswordField, Bank, Pay, Crypto, HasCopyrightInfo).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: the 17 yes/no features (IsDomainIP, HasObfuscation, IsHTTPS, HasTitle, HasFavicon, Robots, IsResponsive, HasDescription, HasExternalFormSubmit, HasSocialNet, HasSubmitButton, HasHiddenFields, HasPasswordField, Bank, Pay, Crypto, HasCopyrightInfo). Reverted: the counts NoOfURLRedirect and NoOfSelfRedirect.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — the first publication reports accuracy, precision, recall and F1 without one task metric; no competition (full text paywalled, not verified).

CC (2026-10-26, Lennart): "Yes exclude" (issue 1): `No` + `Data Quality Issue`; "Yes" (issue 2): the folder leaves the working copy.

**Assessment (AI, 2026-10-26):** excluded: the two classes were collected in different forms (every legitimate row a ranked site's homepage as https://www.<domain>, half of the phishing rows takedown or error pages), so a fixed rule without training reaches ROC AUC 0.9998 and every split gives 1.0; Mendeley versions 1 and 2 hold the same file, so nothing can be repaired from the origin. The definition with its six decision tables is in git history before this change; the evidence is in the assessment of 2026-10-20.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `pilwd_134k_phishing` (TBD -> 2nd Tier, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-25, Andrej): reopened on the better-data review and kept retired (Review issue 1, A): no repair removes the artefact and the file has no dates.

## Review

**Outcome:** not added; retired on 2026-10-26 (`No`, `Data Quality Issue`) and reopened as a question on 2026-11-25. No repair removes the class-form artefact from the page features, and the file carries no date; only a host-name table rebuilt from the URLs scores below the ceiling.

**Main points:** Reopen PhiUSIIL with host-name features rebuilt from its URLs, or keep it retired?

**Issues for Andrej:**

1. **Reopen PhiUSIIL with host-name features rebuilt from its URLs, or keep it retired?**

   * **Problem:**
     - The page features still separate the classes after every repair tried (LightGBM 0.9995 ROC AUC grouped by domain, even with the 81,856 phishing rows on shared pages dropped), and the file has no date per row, so it cannot serve a temporal split.
     - Only features rebuilt from the host name alone, with scheme, `www.` and path removed, fall below the ceiling (LightGBM 0.840 grouped by domain), but 96% of legitimate hosts are bare registered domains against 46% of phishing ones, the top list's form.
     - Reopening reverses Lennart's decision of 2026-10-26 to exclude it[^len].
   * **Background:** 235,795 rows (134,850 legitimate, 100,945 phishing), 51 features as published plus `URL`, `Domain`, `TLD`, `Title` and `FILENAME`. The only per-row identifier is `FILENAME`, a page number in separate ranges per class (legitimate up to 904,971, phishing up to 8,139,518), not a date; Mendeley versions 1 and 2 hold the same file.
   * **Experiments:** 2026-11-25, batch, on the UCI file (sha256 a236549cd369cd80...); phishing as the positive class; registered domain by a public-suffix heuristic; 5 folds, ROC AUC; untuned depth-1 and depth-2 trees as fixed rules, logistic regression on standardised features, LightGBM defaults. "Shared pages": rows whose 11 page counts (lines, longest line, images, CSS, JS, external, self and empty references, title, iframes, pop-ups) occur on two or more registered domains.

     Class-form probes:

     | Probe | Legitimate | Phishing |
     |---|---|---|
     | URL written as `https://www.<host>` with no path | 100% | 1.0% |
     | host, without `www.`, is a bare registered domain | 96.2% | 45.5% |
     | row on a shared page | 211 rows (0.2%) | 81,856 rows (81.1%) |

     Repairs:

     | Features | Rows (phishing) | Split | Depth-1 tree | Depth-2 tree | Logistic regression | LightGBM |
     |---|---|---|---|---|---|---|
     | as published (51) | 235,795 (100,945) | random | 0.963 | 0.985 | 1.000 | 1.000 |
     | as published (51) | 235,795 (100,945) | grouped by domain | 0.954 | 0.984 | 1.000 | 1.000 |
     | URL features only (21) | 235,795 (100,945) | grouped by domain | 0.731 | 0.958 | 0.998 | 0.999 |
     | page features only (30) | 235,795 (100,945) | grouped by domain | 0.954 | 0.973 | 1.000 | 1.000 |
     | page features only, shared pages dropped | 153,728 (19,089) | grouped by domain | 0.863 | 0.910 | 0.998 | 0.9995 |
     | host + page, shared pages dropped | 153,728 (19,089) | grouped by domain | 0.863 | 0.940 | 0.999 | 0.9996 |
     | host name only, rebuilt (12) | 235,795 (100,945) | random | 0.713 | 0.759 | 0.803 | 0.855 |
     | host name only, rebuilt (12) | 235,795 (100,945) | grouped by domain | 0.692 | 0.746 | 0.797 | 0.840 |
     | host name only, shared pages dropped | 153,728 (19,089) | grouped by domain | 0.623 | 0.751 | 0.869 | 0.895 |

     - The 12 host features: length, dots, hyphens, digits and their share, labels, longest label, entropy, IP form, TLD length, punycode, vowel share.
     - The depth-2 rule on the host reads the number of dots, then the digit share or the TLD length: a bare registered domain without digits is legitimate, the top list's form.
     - The page features fail because every legitimate page is a ranked site's homepage and every phishing page a lure or a takedown page; the file keeps no HTML to rebuild them from.
   * **Effect on the task:** the host-name table would ask "is this domain name a phishing host or a ranked site", without the page and without the URL path, a narrower task than web_page_phishing_detection's and with a top list as the legitimate side; it gives no date for the temporal need of the phishing family.
   * **Consistency:** an artefact that runs through the features a practical model relies on and cannot be undone retires the dataset; a feature subset does not help when it keeps the artefact[^l15]. Hannousse was taken for its URL showing no such shortcut[^form].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep it retired (implemented) | record stays `No`, `Data Quality Issue` | no table whose classes differ by collection form; the phishing task is covered by web_page_phishing_detection | none found |
     | B | Reopen with host-name features rebuilt from the URLs | new definition: 12 lexical features of the host without scheme, `www.` and path; all 235,795 rows; split grouped by registered domain | below the ceiling (LightGBM 0.840, logistic regression 0.797); 20 times Hannousse's size | features are ours; the legitimate side is still the top list's bare registered domains (96% against 46%); no page, no path, no date; reverses the decision of 2026-10-26 |
     | C | Reopen as B, with the shared-page phishing rows dropped | as B on 153,728 rows (19,089 phishing) | drops the takedown and error pages | loses 81% of the phishing rows; the host-name task then scores 0.895, closer to the ceiling than B; the same top-list form |

   * **Recommendation:** A: no repair removes the artefact from the page features, the host-name rebuild keeps the top list's form and drops the page, and the file has no date, so it serves neither a clean task nor the temporal need, which PhreshPhish (the dated candidate in website_phishing's review) meets. **Decision:** A, B or C?

   **Notes for the AI:** on B or C: CC (<date>, Andrej) line reversing the 2026-10-26 exclusion, suggestion back to the curator's choice, `Data Quality Issue` removed only if the curator says so; definition from the UCI file, `URL` to host (drop scheme, `www.` and everything after the host), the 12 host features of this batch, group by registered domain (public suffixes without private domains), drop every published feature. On A, close with a Resolved line; nothing changes.

   [^len]: CC (2026-10-26, Lennart): "Yes exclude" (issue 1): `No` + `Data Quality Issue`; "Yes" (issue 2): the folder leaves the working copy.
   [^l15]: LEAK-15 (Must): a recording artefact that runs through several features that would matter for prediction in practice, and that cannot be undone, retires the dataset: a feature subset does not help when it also separates same-label groups.
   [^form]: LEAK-13 to LEAK-15 (Must): classes recorded in different forms or from different sources are checked for a shortcut that separates them, and such a dataset is not shipped.

   **Andrej (2026-11-25, correct):** the decision stands.

   **Resolved (2026-11-25, Andrej):** A: PhiUSIIL stays retired (`No`, `Data Quality Issue`), as Lennart decided on 2026-10-26; no repair removes the class-form artefact and the file carries no dates. The dated phishing task is PhreshPhish (`phreshphish_phishing_pages`).

## Reference

Prasad, A., & Chandra, S. (2023). PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning. Computers & Security, 103545. doi: https://doi.org/10.1016/j.cose.2023.103545

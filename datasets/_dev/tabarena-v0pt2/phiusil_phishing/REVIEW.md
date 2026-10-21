# phiusil_phishing

**Outcome:** added; recommended `No` (`Data Quality Issue`). PhiUSIIL's file of 235,370 URLs (after dropping 425
repeats), phishing or legitimate, on a random split. The two classes were collected in different forms, so a fixed
rule with no training separates them, and no version of the file is a valid task.

```text
Verdict: don't ship. `No` + `Data Quality Issue` (the curator's call).
Validity: SEL-1, SEL-2 hold. USE-2 holds (a real actor and decision); USE-8 fit approximate, with the gap named in
  fit_reason (negatives are ranked homepages only). LEAK-13/14/15 triggered (Must), no fix in the definition: every
  legitimate row is https://www.<host>, and every feature family separates the classes. LEAK-10 triggered: half the
  phishing pages were fetched after takedown. SPLIT-1 holds (random split; grouped by host scores the same).
  PROV-1: the record's year is wrong (field row).
Value: TP-6 (the task is solved) and TP-3 (the models score the same, so nothing is ranked), both from the leak.
  TP-4 not proven, so no `Trivial` marker.
Quality: wording fixed in the definition; the URLLength note states a LEAK-13 departure, acceptable only
  because the dataset is excluded.
For the curator: issue 1 (exclude), issue 2 (the folder after exclusion).
```

**Main points:** Exclude as `Data Quality Issue` (issue 1, recommended); then remove the folder, as for the three
datasets retired on 2026-10-16 (lgg_low_grade_glioma, coad_colon_adenocarcinoma, corporate_credit_rating; issue 2).

**Record fields that disagree with the definition:**

- `year`: record `2024`, definition `2023`.

**Record judgment:** valid. The record names the leak question (Andrej) that the run confirms; its 2026-10-20
assessment holds the measured evidence, so the evidence outlives the folder.

**Issues for Lennart:**

1. **Exclude phiusil_phishing as `No` with `Data Quality Issue`?** The two classes were collected in different
   forms. Every legitimate row is the homepage of a ranked site, written as `https://www.<domain>` with no path (the
   source's FILENAME is its rank). The phishing rows are URLs from phishing feeds, and for half of them the page
   features describe what the address served when it was fetched after the site was taken down: an empty, stub or
   error page, such as Firebase Hosting's "site not found".
   - Effect: a model learns the URL template of the legitimate list and the takedown pages, not phishing. A real
     detector meets legitimate URLs with paths, with http and without www., and live phishing pages; the scores say
     nothing about those, and every method reaches the ceiling, so the dataset cannot rank methods.
   - Evidence: a fixed rule with no training (the URL is https://www.<host> without a path and the page has at least
     102 lines) reaches ROC AUC 0.9998 and calls 38 of the 100,520 phishing rows legitimate. The URL features alone
     reach 0.9989, the page features alone 0.99994; untuned LightGBM, random forest and a linear model all reach
     0.99999 or above. Every split, random or grouped by host or by registered domain, gives ROC AUC 1.0. 50,748
     phishing rows (50.5%) and no legitimate row sit on one of 115 shared pages: pages whose 26 page features are
     identical on at least 100 rows across several hosts; the largest (6,159 rows) is Firebase Hosting's "site not
     found" page. Mendeley Data
     version 1 and version 2 hold the same file, so there is no other version to repair from (PROV-13).
   - Implemented: the definition drops the columns that encode the collection (FILENAME, URLSimilarityIndex, the
     Title the source rebuilt from the URL and its two scores, and Domain, a copy of the URL's host) and states the
     exclusion in its notes. No drop removes the URL template or the takedown pages. Cost of excluding: the
     benchmark loses its only large URL-based phishing task; website_phishing (kept 2026-10-14, page signals coded
     by the donor) stays.
   - Alternative: ship anyway. Then three changes are needed, each a rule the definition departs from only because
     it is excluded: recompute URLLength and the URL counts and ratios from `URL` (LEAK-13, Must: URLLength is one
     character short for every legitimate row but only 52% of phishing rows, as hepatitis_c_prediction); drop
     URLCharProb, the mean probability of the URL's characters under a distribution of legitimate domain names,
     unless the paper shows it comes from an outside list (LEAK-28, Must: it matches this file's own legitimate rows
     three times more closely than all rows, MAD 0.0036 vs 0.0115, so it may have been fitted with the labels, as
     santander_customer_transaction_prediction); drop both rows of the 43 homepages listed under both labels
     (LEAK-20, Should, as jm1). Cost: these fix details, not the collection; the scores stay at ROC AUC 1.0.
   - Rule: LEAK-13, LEAK-14, LEAK-15 and LEAK-10 (P4, Must); a Must has no exceptions. The advocate and the critic
     agree, and the blind reviewer, without our notes, also says exclude. Precedent: follows
     prostate_cancer_detection (`Data Quality Issue`, no fix existed); hepatitis_c_prediction and
     biogeographical_ancestry_prediction were kept because a fix existed. `Trivial` stays off: TP-4 needs a single
     feature that matches the models fold by fold, and the best single feature, the URL text, reaches ROC AUC 0.998
     against the models' 0.99999 (claim audit, row 18), as for lgg_low_grade_glioma (`Data Quality Issue` only); anneal's `Trivial` (2026-07-27) predates TP-4
     and is not followed.
   - Recommendation: exclude.
   - Decision: `No` + `Data Quality Issue`, or ship with the three changes.

2. **If excluded: remove the folder, as for lgg, coad and corporate_credit_rating?** On 2026-10-16 three datasets
   retired before they were built (lgg_low_grade_glioma, coad_colon_adenocarcinoma, corporate_credit_rating, all
   `Data Quality Issue`) had their folders removed from the working copy and `v2_path` cleared in the record, and the
   record cites the commit that last held the definition, so the definition stays in git.
   - Effect: none on the benchmark. It decides where a later reader finds the evidence: the record's assessment line
     holds the numbers, git holds the definition with its six decision tables.
   - Implemented: the folder stays until you decide; it has no build and no UUID.
   - Alternative: keep the folder in the working copy. Cost: it needs a fact that sets this case apart from the three
     retirements, recorded as an exception; none was found.
   - Rule: the working copy's house rule (a retired dataset leaves the copy) and consistency with precedent. The
     advocate and the critic agree.
   - Recommendation: remove the folder, clear `v2_path`, cite the commit in the record.
   - Decision: remove, or keep as an exception.

**Review panel:** don't ship, `No` + `Data Quality Issue` (mediator). All nine review roles ran. Claim audit: the
definition's numbers reproduce; two statements refuted (the record's year 2024, "the collection period is not
stated"), the second fixed, the first a field row; the paper, URLCharProb's origin and the licence untested. Blind
review: exclude, the URL form gives the label away. Debate: agreed on exclusion, no `Trivial`, the random split and
the folder; disputed only the label of the URLLength note, settled for the critic (a LEAK-13 departure, fixed).
The fit stays approximate: the critic dropped "none", which would bring the `No Good Target` marker. The reports
number the issues of the earlier draft: its 1 and 2 are issues 1 and 2 here, its 4 and 5 are conditions in issue
1's alternative, and its 3 (the marker) is answered in issue 1's rule.

<details><summary>Claim audit</summary>

**phiusil_phishing: claim audit (2026-10-20, re-check)**

Data: raw UCI 967 csv (sha256 a236549c...d1c6, matches claim 13), deduplicated as `_clean` does (235,370 rows).
Methods: counts and rules; LightGBM with 300 trees, 3 folds, seed 0; character 3- to 5-gram tf-idf with logistic
regression; filenames, page 1 and password fields.

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1-2 | question / use case: detector fetches the page before the user opens it | D task_summary | password-field rate and stub pages by class | holds as a statement of the use case; the data does not match it (see 16) | | USE-1 |
| 3 | "the collection period is not stated" | D row | Mendeley v1 page | **refuted** (minor) | Mendeley: "Most of the URLs ... are latest URLs, mostly from 2023" | PROV / writing |
| 4 | 43% phishing | D | count | holds | 100,520 / 235,370 = 42.7% | |
| 5 | known features | D | column list vs URL_FEATURES/PAGE_FEATURES | holds | | |
| 6, 28 | random split; hosts not held out | D | LightGBM all features: random / host / registered domain / near-copy groups | holds | AUC 1.0 everywhere; log loss 0.00041 / 0.00049 / 0.00038 / 0.00041 | SPLIT-1 |
| 7, 19-21 | drops FILENAME, URLSimilarityIndex, Title, 2 title scores, Domain | D | recompute Title via title_rewrite; FILENAME form; Domain vs URL authority | holds | Title = URL rewrite for 99.96% legit / 99.21% phishing HasTitle=1 rows; FILENAME numeric < 1M for 100% legit, 0 phishing; Domain = authority (incl. port/userinfo) for all rows | LEAK-13..15 |
| 8-9 | fit approximate; fixed rule AUC 0.9998 | D | rule on kept rows | holds | rule AUC 0.99981; 134,850 legit + 38 phishing called legitimate | USE-1, TP-4 |
| 10 | year 2023, source_url Mendeley | D | Mendeley page | holds | v1 published 2023-08-29 | PROV-1 |
| 11, 14 | licence, bibtex | D | not tested (licence never evidence) | untested | | |
| 12, 32 | ForcedIIDFromTemporal; only phishing rows carry an order | D | FILENAME forms by class | holds (order of feed ids not verified as time) | phishing ids: plain 55,021, mw 36,283, oph 8,288; legit ids are ranks | SPLIT-3 |
| 13 | identical file, sha256 | D | sha256sum | holds | a236549c...d1c6 | PROV |
| 15 | paper not read | D | | untested (paywalled) | | EV-2 |
| 16 | phishing pages fetched after listing | D | password field and stub pages by class | holds | HasPasswordField 13.8% legit vs 5.3% phishing; LineOfCode <= 10 for 46.5% of phishing | LEAK (prediction point) |
| 17 | label 1 = legitimate | D | label-1 count vs abstract; URL form | holds | 134,850 label-1 rows, all ranked homepages | USE-5 |
| 18 | rule calls 38 phishing legit; Data Quality Issue not Trivial (no single feature matches the models) | D | rule; task probe single feature | holds | single feature (URL) AUC 0.9981, log loss 0.027 vs LightGBM 0.0013 | TP-4 |
| 22 | URL features 0.9989, page 0.99994 | D | LightGBM 3-fold | holds | 0.99881 / 0.99995 | |
| 23, 38 | 115 shared pages, 50.5% phishing, 0 legit, 0 password; page 1 Firebase "site not found" | D, README | recompute | holds | 115 pages; 50.49%; 0 legit; 0 password; page 1: 6,159 rows, 0 legit, 2 titles "site not found" | |
| 24 | URLLength cut counts; len(URL) moves AUC 0.99893 -> 0.99895 | D | crosstab; LightGBM | holds (counts); the AUC shift is noise (ours 0.99881 -> 0.99878) | cut 1: 134,850 legit, 52,090 phish; cut 0: 48,428; 2 phishing rows cut 4 and 35 (unmentioned) | LEAK-30 |
| 25 | TLDLegitimateProb from an outside list; without both AUC 1.0000 | D | per-TLD constancy; corr with in-file legit share; LightGBM without both | holds | one value per TLD (695 TLDs); corr 0.995 with in-file share but values differ (com 0.523 vs 0.510, org 0.080 vs 0.123); AUC 1.0, log loss 0.00041 both ways. URLCharProb origin untested | LEAK-28 |
| 26 | 425 URLs twice, all phishing, first copy kept | D | duplicated() | holds; copies are not identical | all 425 pairs differ in URLLength (one cut, one not), 37 in LineOfCode: two fetches, not two listings | PROV-6 |
| 27, 39 | hosts recur for phishing only; 43 homepages under both labels | D | host groups | holds with a gap | 5,251 repeated hosts: 5,197 only phishing, 0 only legit, 54 with both classes; 43 both-label URLs | SPLIT |
| 29-30 | host-held-out numbers | D | LightGBM and char n-gram LR by random/host/reg. domain | holds | n-gram: 0.99898/0.0145, 0.99883/0.0159, 0.99863/0.0174 | SPLIT-1 |
| 31 | v1 put multi-row hosts into train | D | v1 notebook (git 2475ea2^) | holds | `predefined_train_indices = df.Domain.value_counts()>1` | |
| 33 | URL unique after dedup | D | | holds | 235,370 unique | |
| 34 | TLD 'na' = Namibia, 19 legit rows | D | count | holds | 19 rows, all legit | |
| 35 | pure values NoOfSubDomain=0, NoOfQMarkInURL=1, IsHTTPS=0 phishing only; HasSocialNet=1 marks ranked homepages | D warning | counts by class | holds for the three; HasSocialNet=1 is not pure | 13,904 / 5,564 / 51,142 phishing, 0 legit; HasSocialNet=1: 107,146 legit, 511 phishing | writing |
| 36-37 | TEMPLATE_URL; min legit lines 102 | D | fullmatch; min | holds | 100% legit; 627 phishing; min 102 | |
| 40 | record year 2024 | R | Mendeley v1 2023-08-29 | **refuted** | first publication 2023 (D is right) | PROV-1 |
| 41-46 | record comments and assessments | R | same tests as above | hold (numbers reproduced) | | |

Implied claims:
* Every feature known at the prediction point: refuted for the page family of half the phishing rows (fetched later,
  stub/error pages), already stated by the definition (claim 16); not fixable by a drop since the URL family alone
  gives 0.9988 (LEAK, P4, Must; the definition already recommends exclusion).
* No row is a copy across the split: 6,856 rows in 3,276 near-copy groups (scheme, www., final /); grouping them
  leaves log loss at 0.00041: no effect.
* Target is the real-world target: holds (label mapping consistent with the URL forms).

Ranked refuted: (1) record year 2024 vs first publication 2023 (P5, PROV-1; remedy: set the record year to 2023).
(2) "collection period is not stated" (P7/writing; remedy: say "mostly 2023, per the Mendeley page").
Wording gaps (hold with a gap): hosts with both classes (54) unmentioned in "hosts recur for phishing only";
HasSocialNet=1 is not a pure value (511 phishing rows); duplicate pairs are two fetches, not identical rows.
Untested: the paper (paywalled; claim 15), URLCharProb's distribution (claim 25), licence (never evidence), whether
feed ids order phishing rows in time (claim 32).

</details>

<details><summary>Column audit</summary>

**phiusil_phishing: column audit (column-auditor, 2026-10-20)**

Frame: `dataset_io.from_definition` on `datasets/_dev/tabarena-v0pt2/phiusil_phishing/dataset.py`, 235,370 rows x 50
columns (48 features, URL as string, label). No missing values in any column. Each URL feature was
recomputed from URL, by class. The paper is paywalled and was not read; meanings come from the column names,
the UCI page and recomputation from the URL (EV-2: measurement over page). Prediction point (curation_comments bullet 1):
a detector fetches the page of a URL and decides before the user opens it.

**Facts measured on the frame**

* **How the URL features are computed (both classes):** the counts (letters, digits, `=`, `?`, `&`, other specials)
  are taken on the URL with the scheme and a leading `www.` removed; `URLLength` is the full length. Legitimate:
  URLLength - (letters + digits + other + `=` + `?` + `&`) = 12 (`https://www.`) in 134,850 of 134,850 rows; phishing:
  7, 8, 11 or 12 by scheme and www. The ratios are count / URLLength rounded to 3 decimals (legit 100%, phishing
  99.9%; SpacialCharRatioInURL 93.3% in phishing).
* **The last-character cut is a class convention, not a URL-form rule (LEAK-13):** URLLength = len(URL) - 1 for all
  134,850 legitimate rows. Among phishing URLs of the very same form (`https://www.<host>`, no path, no slash) only
  1,145 of 1,848 are cut; across phishing forms the cut rate is 35-77% with no pattern by scheme, www or trailing slash.
  The letter counts carry the same cut (legit: letters = all letters - 9 = `https` + `www` + the cut last character).
* **Template values (legit by construction):** legit rows never have NoOfSubDomain 0 (`www` counts), `?`, `=`, `&`,
  obfuscated characters, an IP host, or http; IsHTTPS equals the URL scheme in 100% / 99.5% of rows.
* **Page features look like two different fetches:** phishing medians LineOfCode 12, NoOfImage 0, NoOfJS 0, NoOfCSS 0,
  NoOfSelfRef 0, NoOfExternalRef 0 against legit 1,105 / 25 / 14 / 6 / 76 / 46. The phishing maxima (NoOfSelfRef 120,
  NoOfImage 158, NoOfJS 102, NoOfCSS 131) sit below the legit medians or 90th percentiles; 58% of legitimate rows have a
  NoOfSelfRef value no phishing row has, 77% of phishing rows a LineOfCode value no legitimate row has (no legit page
  under 102 lines). Every legit page has HasTitle in 99.9% of rows, phishing 67.7%. This is a dead / placeholder page
  profile (the definition's shared-pages decision: 50.5% of phishing rows on 115 shared pages), not phishing kits.
* **TLDLegitimateProb = 0** for 623 phishing rows and no legitimate row (TLDs absent from the outside list).

**Column table**

Known? = known at the prediction point in the use case. "Template" = the value follows from every legitimate row being
written as `https://www.<host>` with no path; "late fetch" = page measured after the phishing URL was listed.

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| URL | the address classified | yes; but its form encodes the class (template) | string, unique after the 425 repeats are dropped; fine | leak by construction (strong, AUC 0.998 alone); no column remedy | LEAK-14, LEAK-15 |
| URLLength | length of URL | yes | int; len(URL)-1 for all legit, cut in 52% of phishing | leak (class recording convention, weak: +0.00002 AUC measured by the definition); remedy recompute from URL | LEAK-13 |
| DomainLength | length of the authority part | yes | int; matches len(host) 100% / 99.99% | fine (template influences range) | - |
| IsDomainIP | host is an IP address | yes | int 0/1; matches recomputation 99.97% | fine (legit never IP by construction of a ranked list) | - |
| TLD | top-level domain | yes | category, 695 levels; `na` = Namibia, kept as a value (accepted warning, correct) | fine | CLEAN-14 |
| CharContinuationRate | share of the URL in runs of one character type (paper's definition, unread; inferred) | yes | float 0-1; legit 78% at 1.0, phishing 35% | fine (follows the template) | - |
| TLDLegitimateProb | share of the TLD in an outside list of ~10M domains (per definition) | yes, if the list predates the rows | float; 0 only for 623 phishing rows | question: is the outside list the list the legitimate rows were drawn from? then it is a per-TLD statistic of one class | LEAK-14 (question) |
| URLCharProb | mean probability of the URL's characters under a distribution of legitimate domains | unknown: may be fitted on this file's legitimate rows | float; AUC 0.77 alone | question (REVIEW issue 4); dropping it with TLDLegitimateProb leaves AUC 1.0000 | LEAK-28 (weak, open) |
| TLDLength | length of TLD | yes | int; = len(TLD) 100% | fine; derivable from TLD, not an exact copy | CLEAN-5 (keep) |
| NoOfSubDomain | dots in host minus one | yes | int; recomputes 100% / 99.99% | fine; value 0 only phishing (template: legit always `www.`) | - |
| HasObfuscation | URL has obfuscated (percent-encoded) characters | yes | int 0/1; = NoOfObfuscatedChar > 0 in 100% | fine (redundant flag, not an exact copy) | CLEAN-5 (keep) |
| NoOfObfuscatedChar | count of obfuscated characters | yes | int; legit all 0 (template) | fine | - |
| ObfuscationRatio | NoOfObfuscatedChar / URLLength | yes | float 3 dp; inherits the cut | fine (see URLLength) | LEAK-13 (inherits) |
| NoOfLettersInURL | letters after scheme and `www.`, last character cut where URLLength is cut | yes | int; carries the class cut | leak (class convention, weak); recompute | LEAK-13 |
| LetterRatioInURL | letters / URLLength | yes | float 3 dp; inherits the cut | as above | LEAK-13 |
| NoOfDegitsInURL | digits ("Degits" sic) | yes | int; matches full URL 100% / 98.8% | fine (name typo is the source's) | - |
| DegitRatioInURL | digits / URLLength | yes | float 3 dp; inherits URLLength cut | as URLLength | LEAK-13 (inherits) |
| NoOfEqualsInURL | count of `=` | yes | int; legit all 0 (template) | fine | - |
| NoOfQMarkInURL | count of `?` | yes | int; legit all 0 (template) | fine | - |
| NoOfAmpersandInURL | count of `&` | yes | int; legit all 0; phishing 96.9% match the URL | fine | - |
| NoOfOtherSpecialCharsInURL | other special characters after scheme and `www.` | yes | int; AUC 0.82 | fine (template: legit = dots of host) | - |
| SpacialCharRatioInURL | specials / URLLength ("Spacial" sic) | yes | float 3 dp; 6.7% of phishing rows do not recompute | fine with note | - |
| IsHTTPS | scheme is https | yes; for legit rows the scheme was written by the authors (template) | int 0/1; = URL scheme 100% / 99.5%; legit all 1 | fine as a column; the template is the leak (see URL) | LEAK-14 |
| LineOfCode | lines of the page source | no for phishing: late fetch | int; legit >= 102, phishing median 12; AUC 0.993 alone | leak by collection (late fetch, separate source), no column remedy | LEAK-10, LEAK-14, LEAK-15 |
| LargestLineLength | longest source line | late fetch | int; up to 14M chars (minified), not impossible | as LineOfCode (AUC 0.82) | LEAK-14 |
| HasTitle | page has a `<title>` | late fetch | int 0/1; legit 99.9%, phishing 67.7% | as LineOfCode | LEAK-14 |
| HasFavicon | page has a favicon | late fetch | int 0/1 | as LineOfCode | LEAK-14 |
| Robots | robots meta / robots.txt present (unknown which) | late fetch | int 0/1 | as LineOfCode; meaning unknown | LEAK-14 |
| IsResponsive | page has a viewport / responsive layout (inferred) | late fetch | int 0/1 | as LineOfCode | LEAK-14 |
| NoOfURLRedirect | page redirects to another URL; binary despite "NoOf" | late fetch | int 0/1 only; meaning unknown | fine (weak, AUC 0.52); name misleads | CLEAN-14 (note) |
| NoOfSelfRedirect | page redirects within its domain; binary | late fetch | int 0/1 only | as above | CLEAN-14 (note) |
| HasDescription | page has a meta description | late fetch | int 0/1; AUC 0.85 | as LineOfCode | LEAK-14 |
| NoOfPopup | popups in the page script | late fetch | int; phishing max 10, legit to 602 | as LineOfCode | LEAK-14 |
| NoOfiFrame | iframes | late fetch | int; phishing max 25 | as LineOfCode | LEAK-14 |
| HasExternalFormSubmit | a form posts to another domain | late fetch | int 0/1; legit 7.4%, phishing 0.4% (inverted from the phishing hypothesis) | as LineOfCode | LEAK-14 |
| HasSocialNet | links to social networks | late fetch | int 0/1; 79.5% / 0.5%; AUC 0.89 | as LineOfCode | LEAK-14 |
| HasSubmitButton | page has a submit button | late fetch | int 0/1; 66% / 8% | as LineOfCode | LEAK-14 |
| HasHiddenFields | hidden form fields | late fetch | int 0/1 | as LineOfCode | LEAK-14 |
| HasPasswordField | password input | late fetch | int 0/1; legit 13.8%, phishing 5.3% (inverted) | as LineOfCode | LEAK-14 |
| Bank | page text mentions banking keywords | late fetch | int 0/1; legit 18%, phishing 5% (inverted) | as LineOfCode | LEAK-14 |
| Pay | payment keywords | late fetch | int 0/1; 37% / 6% (inverted) | as LineOfCode | LEAK-14 |
| Crypto | crypto keywords | late fetch | int 0/1 | as LineOfCode | LEAK-14 |
| HasCopyrightInfo | copyright notice | late fetch | int 0/1; 81% / 6% | as LineOfCode | LEAK-14 |
| NoOfImage | images | late fetch | int; phishing median 0, max 158; AUC 0.980 | as LineOfCode | LEAK-14, LEAK-15 |
| NoOfCSS | stylesheets | late fetch | int; legit max 35,820 (unusual, not impossible) | as LineOfCode | LEAK-14 |
| NoOfJS | scripts | late fetch | int; phishing max 102 | as LineOfCode | LEAK-14 |
| NoOfSelfRef | links to the same domain | late fetch | int; phishing median 0, max 120; legit median 76 | as LineOfCode (AUC 0.973) | LEAK-14 |
| NoOfEmptyRef | empty links (`#`) | late fetch | int | as LineOfCode | LEAK-14 |
| NoOfExternalRef | links to other domains | late fetch | int; AUC 0.989 | as LineOfCode | LEAK-14 |
| label | Legitimate / Phishing (UCI: 1 = legitimate) | target | category; mapping checked against the abstract's 134,850 | fine | CLEAN-15 |

Dropped by the definition, re-checked and agreed: FILENAME (an id whose form gives the class away, LEAK-10 / CLEAN-3),
URLSimilarityIndex (similarity to the legit source list, LEAK-14), Title (the URL rewritten, not a title; LEAK-13),
DomainTitleMatchScore and URLTitleMatchScore (computed from Title), Domain (copy of the URL authority, CLEAN-5).

**Problems, ranked (principles.md)**

1. **P4, LEAK-14 / LEAK-15 (Must), whole feature space.** Legitimate rows are a ranked domain list written as
   `https://www.<host>`; phishing rows come from feeds, their pages fetched later. Both families carry it: the URL form
   (text alone 0.998, IsHTTPS, NoOfSubDomain, the `?=&%` counts) and the page counts (phishing maxima below legit
   medians; LineOfCode alone 0.993). A subset does not help (URL features 0.9989, page features 0.99994). Mildest remedy:
   none at the column level; exclude (`Data Quality Issue`), as the definition already recommends. Agrees with REVIEW
   issue 1.
2. **P4, LEAK-10 (Must), the 26 page features for phishing rows.** They describe the page at the authors' fetch, after
   listing (dead and placeholder pages: median 12 lines, no images, no scripts; keyword flags Bank/Pay/HasPasswordField
   are *more* common among legitimate rows), not the page a user would meet at the prediction point. Remedy: none
   without a re-fetch at listing time; part of issue 1.
3. **P4, LEAK-13 (Must, weak effect), URLLength and every count/ratio that uses it.** The last character is dropped for
   100% of legitimate rows and a random-looking 52% of phishing rows, even within the same URL form (1,145 of 1,848
   `https://www.<host>` phishing rows). Mildest remedy: recompute URLLength, the counts and the ratios from URL for every
   row with one rule; the definition measured the effect as negligible and keeps the source values with a
   `Potential leak, kept on purpose:` note, which is acceptable only because the dataset is not shipped. Should it ever
   ship, recompute (the comment says so).
4. **P4, LEAK-28 (question), URLCharProb and TLDLegitimateProb.** Possibly statistics of the legitimate class's own
   list. No measurable effect (AUC 1.0000 without both). Question for the curator; settle by reading the paper.
5. **P7, CLEAN-14 (note).** NoOfURLRedirect and NoOfSelfRedirect hold only 0/1 despite "NoOf" names; Robots,
   IsResponsive and CharContinuationRate have no codebook definition in hand. Keep; say so in a note if shipped.

No dtype problem: no object column, no proxy missing value, no impossible value (LargestLineLength of 14M characters and
NoOfCSS of 35,820 are unusual, not impossible). Not a column issue: the record's `year` 2024 against the definition's
2023 (REVIEW).

</details>

<details><summary>Split audit</summary>

**phiusil_phishing: split audit (re-check, 2026-10-20)**

Setup: the definition frame and split plan (via
`dataset_io.from_definition`, 235,370 rows, IID, 3 repeats x 3 folds; LightGBM 200 trees on all numeric features + TLD,
thread caps 2).

**Verdict: right with notes**

The IID split is defensible (SPLIT-1, SPLIT-4, SPLIT-8) and the grouped alternatives give the same score. The split is
not what makes the task invalid: the decisive problem is the class-dependent collection (LEAK-13 to LEAK-15), which no
re-split, gap or filter removes.

**Regime**

* Use case: a detector classifies a URL before the user opens it. New data holds URLs on known shared hosts (ipfs.io
  1,192 rows, docs.google.com 526, cloudflare-ipfs.com 359) and on new hosts; the host is a property every new URL has,
  so under SPLIT-4 it is a feature, not an entity new data lacks. IID holds (SPLIT-1, SPLIT-29 not triggered).
* Temporal: no time column; only the phishing rows carry an order (feed file ids), so a temporal split cannot be built
  across both classes. Tag ForcedIIDFromTemporal applies SPLIT-8; the cost of the missing time axis cannot be measured
  (the definition says so). Holds.
* Grouped: no true group id in the source beyond the URL's host (SPLIT-24). The shared-page fingerprints (115 pages on
  >= 100 rows) are page templates, not entities, and would be a cluster key barred by SPLIT-24.

**Numbers**

| group key | groups | repeated groups (rows) | only phishing | only legitimate | both classes (rows) |
|---|---|---|---|---|---|
| host | 220,077 | 5,256 (20,549) | 5,202 | 0 | 54 (112) |
| host without www. | 219,094 | 5,673 (21,949) | 5,615 | 0 | 58 (159) |
| last two labels | 157,351 | 5,906 (83,925) | 4,883 | 735 | 288 (18,187) |

Shipped split, repeat 0: test rows whose host (without www.) is in train 7.96-8.06%; phishing 18.6-18.8%, legitimate
0.02-0.03%. By last two labels: 34.6-34.7% (phishing 61.6-61.9%, legitimate 14.2-14.6%).

| split (3 folds) | ROC AUC | log loss |
|---|---|---|
| shipped splits (9) | 1.000000 | 0.00042 |
| random, seed 0 | 1.000000 | 0.00032 |
| grouped by host | 1.000000 | 0.00037 |
| grouped by last two labels | 1.000000 | 0.00061 |

Hidden-group probe: 11 candidates, no hits (top LargestLineLength, gap -0.000); near-copy clusters at 0.85 cover 17.2%
of rows, gap -0.000. These agree with the splits_comment numbers (0.0003 / 0.0003 / 0.0004).

**Problems, ranked**

1. **P4, LEAK-13 to LEAK-15 (context, not a split problem).** The classes were collected in different forms; every
   split scores AUC 1.0000. No split remedy exists; exclusion as Data Quality Issue stands (owned by the leak auditor).
2. **P4, SPLIT-29 / SPLIT-31 (note).** "Seen host" is class-asymmetric: 18.8% of phishing test rows vs 0.03% of
   legitimate ones have their host in train, so a random split admits a "known host means phishing" shortcut (a
   blocklist lookup). At saturation it costs nothing (log loss 0.00032 -> 0.00037 grouped by host). Remedy: none now;
   if a repaired version ever ships (legitimate rows with paths, pages fetched at listing time), re-measure and
   consider a host-grouped variant (SPLIT-31).
3. **Writing (note).** "Hosts recur for phishing only, by construction" (Decision 6 text and the curation_comments
   Note bullet) is loose: 54 hosts (112 rows) hold both classes; no host with several rows is legitimate only. Remedy:
   "hosts with several rows are phishing hosts, apart from 54 hosts that hold both classes".

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: phiusil_phishing (2026-10-20, re-check)**

Actor (USE-1): the engineer who owns the URL classifier of a secure web gateway / mail filter / browser-protection
service. Moment: a URL arrives (in an e-mail, a click, a crawl queue); the service fetches it in a sandbox and must
decide block / warn / allow before the user lands on it. Decision: block or warn, at a threshold set by the false-positive
budget on legitimate traffic.

**Fit: none (as a benchmark of that decision; at most "approximate" in name only)**

The definition says approximate (USE-8). As the actor I would say none for practical purposes: the label is
recoverable from how each class was collected (legitimate = bare `https://www.<host>` homepage of a ranked domain with a
full page; phishing = feed URL fetched later, half on 115 shared stub/error pages), so the model learns "is this a
top-list homepage" rather than "is this phishing". A fixed rule with no training reaches ROC AUC 0.9998. No decision I
make is mirrored by that contrast (USE-2), and the gap is not one of the named approximate gaps of USE-8 (snapshot for
forecast, kept leak, missing horizon); it replaces the task. The curation notes already recommend excluding
(`Data Quality Issue`), and I agree.

**1. Inputs at the prediction point (USE-3, USE-6)**

* Have, and the dataset has: the URL string, TLD, URL counts/ratios, the page HTML features (forms, password field,
  iframes, scripts, external refs). These are exactly what a sandbox fetch gives me; no future information in principle.
* Have but distorted here: the page features of phishing rows describe the page at fetch time, after the feed listed
  the URL; 50.5% are takedown/parking/"site not found" pages. At my decision moment a live phish shows its kit (login
  form, brand assets), not a Firebase 404. So the page features in this file are a post-outcome state for half the
  positives (closest to LEAK-10 in spirit: the takedown is the outcome having happened).
* Would always have, missing: domain age / WHOIS registration date, certificate issuer and age (Let's Encrypt within
  hours of first sighting), DNS/ASN/hosting reputation, redirect chain, the referrer context (e-mail sender, campaign),
  the visual/brand similarity of the page, and the time of first sighting. Domain age and certificate age are among the
  strongest signals in production.
* Cut-string artifact (URLLength = len(URL) - 1 differs by class): a feature I would compute myself correctly; kept on
  purpose here (USE-8 "potential leak kept on purpose"), minor next to the above.

**2. Target (USE-5)**

The target I act on is "malicious credential-harvesting/phishing page at the time of the visit". The label here is
"came from a phishing feed" vs "is in a top-domain list". Feed membership is a reasonable proxy for the positive class
if the page is fetched while live; a top-list homepage is a poor proxy for the negative class: my legitimate traffic is
deep links with paths and query strings, login pages of real banks, SaaS pages, shortened links, long-tail small sites,
and benign pages on the same shared hosts phishers abuse (docs.google.com, ipfs gateways, firebaseapp, weebly). None of
those are negatives here. Output: I want a calibrated probability (to set a block threshold at a fixed false-positive
rate, often 1e-4 or lower), so log loss / ROC AUC are the right metric family, but the 43% prevalence is far from the
<1% I see; ranking metrics survive this, calibration does not.

**3. Row and test data (USE-10, SPLIT-3)**

One row = one URL decision: matches. The test should be "URLs seen next week", because phishing campaigns and kits
drift fast and detectors are always validated forward in time. The file has no timestamp (tag ForcedIIDFromTemporal),
so the random split cannot test that. Hosts: I meet both known and new hosts, so not grouping is defensible
(USE-10, known entity; the splits comment shows grouping changes nothing anyway). The test data is not what I face:
its negatives are homepages only and its positives are partly dead pages.

**4. Would I use the model?**

No. A model at AUC 0.9999 on this file would, in deployment, flag any legitimate URL with a path, a query string, a
missing `www.` or http scheme, and any short page, which is most of real benign traffic: the false-positive rate would
be unusable. I would trust it only after evaluation on (a) benign deep links and login pages of real sites, (b) phishing
pages fetched at first sighting, (c) a later time window. Public critique points the same way: HTTPS presence is highly
discriminative in PhiUSIIL but much less in GramBeddings (cross-dataset shortcut).

**Gaps ranked by how much they change the task**

1. Negative class is homepages of ranked domains only (form `https://www.<host>`, no path): the task becomes
   "top-list homepage vs anything else". Changes the task entirely (USE-5, USE-2).
2. Phishing pages fetched after listing, half on shared takedown/stub pages: page features describe the outcome, not the
   live phish (USE-3, LEAK-10).
3. No time axis, no forward test; phishing drifts (ForcedIIDFromTemporal; USE-8 approximate at best).
4. Class balance 43% vs real prevalence well under 1% (matters for calibration, not for ROC AUC).
5. Missing inputs I always have: domain/certificate age, DNS/hosting reputation, redirect chain, brand similarity.
6. URLLength cut artifact kept on purpose (minor; USE-8, USE-12 say fix and keep if the task were real).

USE-12 does not save the dataset: gaps 1 and 2 are not leaks in a column that can be dropped, they are in how the rows
were sampled, and every feature family (URL alone AUC 0.9989, page alone 0.99994) inherits them. USE-9 offers no
alternate use case: "is this URL a top-site homepage" is not a decision anyone makes with a model.

**What a domain expert would change**

* Reject this file (agree with `Data Quality Issue`; fit none or excluded rather than approximate).
* If a phishing task is wanted: negatives sampled from real click/mail traffic or crawls with full URLs (paths, login
  pages, shared-hosting benign pages), positives fetched at first sighting (e.g. live OpenPhish/PhishTank crawls with
  timestamps), a temporal split, and domain-age / certificate features.
* If the file were kept anyway: label fit as none-to-approximate with the sampling gap named, not "approximate" alone,
  and recompute the URL features from the URL string.

**Rules cited**

USE-1, USE-2, USE-3, USE-5, USE-6, USE-8, USE-9, USE-10, USE-12; LEAK-10; SPLIT-3.

**Sources**

* datasets/_dev/tabarena-v0pt2/phiusil_phishing/dataset.py (task_summary, curation_comments, decisions, splits_comment)
* curation/records/phiusil_phishing.md
* .claude/skills/knowledge-curation/references/use_case.md
* UCI dataset 967: https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
* Mendeley Data: https://data.mendeley.com/datasets/shwpxscxy2
* Cross-dataset shortcut (HTTPS discriminative in PhiUSIIL, not GramBeddings): https://arxiv.org/pdf/2606.21690
* Domain knowledge of production URL classifiers (sandbox fetch, domain/cert age, forward-in-time validation).

</details>

<details><summary>Blind review</summary>

**Blind review: PhiUSIIL phishing URL (UCI 967)**

**Verdict: exclude.** The task is solved by artifacts of how the data was collected, so the score says nothing about the methods being compared.

**Task**
A browser or email gateway decides whether a URL or page is phishing before the user loads or trusts it. The use is real. This dataset does not measure it.

**Concerns (most serious first)**
1. **Labels are given away by how the URLs were collected.** Every one of the 114,562 legitimate rows is a bare homepage of the form `https://www.<domain>`. None has a path, none uses http, and none lacks `www.` (sample: `https://www.proterra.com`). Phishing rows come from feeds and look different:
   - 43,486 phishing rows use http, against 0 legitimate.
   - 49,743 phishing rows lack `www.`, against 0 legitimate.
   - 51,033 phishing rows have a path, against 0 legitimate.

   Each of these rules on its own yields legitimate=0. With the raw `URL` string kept as a column, a regex is a near-perfect classifier.
2. **The task is trivial.** LightGBM on the 48 engineered features reaches ROC AUC 0.9999999 (3-fold). Using only the URL features, accuracy is 0.9974. One-feature stumps reach 0.96 accuracy (NoOfExternalRef 0.9615, LineOfCode 0.9551). Every page with LineOfCode < 20 is phishing. There is no room left to rank methods.
3. **Target-derived columns.** `TLDLegitimateProb` and `URLCharProb` are corpus statistics. The paper does not make clear whether they were computed from the labelled data. If they were, they leak across the folds.
4. **Preparation.** The `URL` column is a free-text string with 200k unique values, which acts as an identifier. 872 rows are exact duplicates once URL is dropped. There are no missing values, and the types are fine.

**What would have to change**
Nothing short of new sampling fixes this: legitimate URLs drawn from the same kind of process as the phishing ones (deep links, mixed http and https). Dropping columns does not remove the artifact. The page-content features alone already reach about 0.96.

**Could not check**
- The paper's full text (it is behind a paywall), so I could not see how the TLD and character probabilities were computed.
- The 35k rows not in the parquet sample.

</details>

<details><summary>Precedent check</summary>

**phiusil_phishing: precedent check (2026-10-20, re-check)**

Inputs: the register of past decisions (808), the previous REVIEW.md (6 issues), the verification checklist, the
claims list, `dataset.py`, the record, sibling records (`website_phishing`, `website_phishing_duplicate`, `phishing_url_websites`),
the Cases tables of `leak_checks.md`, `task_probes.md`, `evidence.md`, and the working copy's `CHANGELOG.md`.
The register's flags that touch this dataset: group 4 (`opposite_outcomes: trivial`) and the `Trivial` / `Data
Quality Issue` groups; none flags phiusil_phishing itself. The flagged pair aps_failure (keep) vs anneal / fitness_club /
haberman (exclude) does not bear on this case (aps is `one_feature` with no artefact; it is not a pair to phiusil).

**Summary**

| # | Decision | Result | Closest precedents |
|---|---|---|---|
| 1 | Recommend exclusion (`No`, `Data Quality Issue`): class-specific collection artefacts in every feature family | consistent | prostate_cancer_detection (retired 2026-09-30, Lennart, LEAK-15, crit. 4D); hepatitis_c_prediction (fixed 2026-09-30, LEAK-13) and biogeographical_ancestry_prediction (fixed 2026-09-30, LEAK-14) set apart: a fix existed there |
| 2 | Folder stays in the working copy if excluded (or the move to `_too_late_to_add`) | departs, neither option follows the precedent | lgg_low_grade_glioma, coad_colon_adenocarcinoma, corporate_credit_rating (2026-10-16, Lennart): folder removed, `v2_path` cleared, definition kept in git |
| 3 | Marker `Data Quality Issue`, not `Trivial` | consistent with the rules; one old precedent the other way (anneal) | prostate (DQI); fitness_club (2026-10-05, Trivial with TP-4 proof); anneal (2026-07-27, Trivial without proof, predates TP-4) |
| 4 | Keep URLCharProb (possibly from this file's legitimate rows) | consistent while unconfirmed; departs from LEAK-28 if confirmed | santander `has_one`/`has_zero` (LEAK-28, dropped); LEAK-32 ieee_fraud / kdd_cup_09 (2026-10-19, unconfirmed hidden transform: no action) |
| 5 | Keep near-identical URLs, incl. 43 homepages under both labels | departs without a stated fact (Should; moot if excluded) | jm1 (2026-10-01, LEAK-20, both-label copies dropped); emscad (LEAK-21, reposts dropped); wine_quality (LEAK-19) |
| 6 | Keep URL as a string feature | consistent (no settled precedent against) | perth_house_prices ADDRESS kept as string (AI, open); website_phishing (2026-10-14, raw page signals kept) |
| 7 | URLLength kept with a `Potential leak, kept on purpose` note | departs from a Must (LEAK-13) with a reason (moot unless shipped) | hepatitis_c_prediction (2026-09-30, conventions harmonised); LEAK-30 notes (2026-10-19) are a different mechanism |
| 8 | IID, hosts not held out, `ForcedIIDFromTemporal` | consistent | account_debt_south_africa (SPLIT-8, 2026-10-12, Lennart); huntprohibited_1m REVIEW lists phiusil among the consistent forced-IID cases |
| 9 | `year` 2023 (definition) vs 2024 (record) | consistent in the definition | PROV-1/PROV-2: the year of first publication (Mendeley 2023-08-29) |

No drift found: Lennart's `Data Quality Issue` retirements for class- or batch-specific artefacts (prostate 2026-09-30)
and his fixes where a harmonisation existed (hepatitis_c, biogeographical, both 2026-09-30) follow one line: fix when a
fix exists, retire when none does. No third exception of one kind: the definition holds one Must departure
(decision 7) and one Should departure (decision 5), each the first of its kind.

**Per decision**

**1. Exclusion as `Data Quality Issue` (LEAK-13 to LEAK-15, Must; TP-6)**

Consistent. The closest precedent is **prostate_cancer_detection** (retired 2026-09-30, Lennart, `No (Retired)`,
`Data Quality Issue`, "the label is readable from sample-processing artefacts, across the whole spectrum, and no batch
IDs survive (crit. 4D)"; LEAK-15 Cases row: "a feature subset does not help when it also separates same-label
groups"). Same facts: the label is readable from how the rows were produced, through every feature family, and no
subset removes it (URL features alone AUC 0.9989, page features alone 0.99994, fixed rule 0.9998).

Set apart from the cases that were fixed and kept:
- **hepatitis_c_prediction** (2026-09-30, LEAK-13): four formatting flags, removed by rounding seven columns and dropping
  `ALP`; the stage signal survived. Here the artefact is the URL template and the page fetch timing, which no rounding or
  column drop removes (Decision 3 of the definition).
- **biogeographical_ancestry_prediction** (2026-09-30, LEAK-14): the artefact sat in one class among ten, which was
  dropped. Here both classes of a binary task come from different sources; dropping a class leaves no task.

Tension row "A real task against a leak": fix and keep unless the leak cannot be undone (yeast, LEAK-27). Phishing
detection is a real task (P3), so the exclusion rests on the "cannot be undone" side of that row, as prostate did. The
sibling **website_phishing** (kept `Yes`, 2026-10-14) does not contradict this: its nine signals are donor-coded page
properties with no class-by-construction template (Phishy vs Legitimate AUC 0.973, not saturated).

**2. Where the folder lives if excluded**

Departs from the latest precedent, and neither option in REVIEW_before issue 2 follows it. On **2026-10-16 Lennart
retired coad_colon_adenocarcinoma, corporate_credit_rating and lgg_low_grade_glioma** (all `No`, `Data Quality Issue`,
none built): "folders removed, `v2_path` cleared; the definitions stay in git at 2475ea2" (CHANGELOG 2026-10-16). The
house rule in CLAUDE.md says the same for `No (Retired)`. The proposed target `datasets/_maintenance/_out_of_scope/
_too_late_to_add/` does not exist (only `_too_small_to_add` and `_iid_version_of_non_iid`); the v0.1 retirements
anneal and fitness_club went to `_maintenance/_old_collections/tabarena-v0pt1/` because they had shipped. Keeping the
folder while the verdict is still open is fine (digicow, stroke_prediction are in the same state); this is about what
happens after the curator's decision.

**Consistency check (AI, 2026-10-20):** issue 2 offers to keep the excluded phiusil_phishing folder in the working copy
or to move it to a new `_too_late_to_add` folder, while lgg_low_grade_glioma, coad_colon_adenocarcinoma and
corporate_credit_rating (retired 2026-10-16, also `Data Quality Issue`, never built) had their folders removed, their
`v2_path` cleared and the definition left in git. What sets phiusil_phishing apart?
(a) its definition carries the measured evidence (Decisions 1-6) that a future reader of the record would need, so it
is kept outside git history, recorded as an exception; (b) treat it like lgg/coad: remove the folder, clear `v2_path`,
cite the commit in the record; (c) reopen the 2026-10-16 retirements to keep their folders too; (d) change the rule
(an amendment: retired-before-shipping definitions go to a `_maintenance/_out_of_scope/` subfolder).

**3. The marker: `Data Quality Issue` rather than `Trivial` (TP-4, Must)**

Consistent with the rules and the recent precedents. TP-4 requires proof (the raw feature, chosen per training side,
matches the methods fold by fold); fitness_club (2026-10-05) is the case that set that standard. Here the best single
feature (URL text) gets AUC 0.9973 / log loss 0.026 against the models' 0.99999 / 0.0008-0.0041, and the fixed rule is
a hand-built rule, not a training-side choice, so TP-4 is not proven. evidence.md ranks the `solved` readings with a
leak first and a trivial task third, which puts the decisive reading under LEAK-13 to LEAK-15, as for prostate.
lgg_low_grade_glioma (AI assessment 2026-10-07: "whether `Trivial` applies too is the curator's call"; Lennart retired it
with `Data Quality Issue` only, 2026-10-16) is the closest precedent for leaving `Trivial` off.

The one precedent the other way is **anneal** (2026-07-27, Lennart: "All models achieved perfect accuracy (trivial)",
marker `Trivial`). It predates TP-4's proof requirement, so it is a precedent that conflicts with the current rule, not
one to follow. If the curator adds `Trivial`, that departs from TP-4 (Must) unless the per-fold raw-feature test is run.
No reflection prompt needed: the draft follows the rule.

**4. Keep URLCharProb (LEAK-28, Must)**

Consistent while the fact is open; it would depart from a Must once confirmed. LEAK-28's case,
**santander_customer_transaction_prediction** (`has_one`, `has_zero`, label-aware over all rows, dropped), says a
confirmed class-conditional statistic over all rows goes, whatever its effect size. The precedent for an unconfirmed
transform is LEAK-32 (ieee_fraud_detection, kdd_cup_09_appetency, Lennart 2026-10-19: a known risk, no action), but that
row is about masked features, and here the suspicion has a measurement behind it (MAD 0.0036 against the legitimate
rows, 0.0115 against all rows). The removal costs nothing (AUC unchanged without it). Since EV-1 asks to settle a
disputed fact before arguing rules, the question is really "read the paper or drop it", and either way the precedent
points to dropping it if it ships. The draft names the open fact, so this is a departure with a stated reason, pending.
TLDLegitimateProb as an outside prior: no conflict.

**5. Near-identical URLs kept (LEAK-19 to LEAK-21, Should)**

Departs without a stated fact, a Should, moot while the dataset is recommended for exclusion. The definition drops the
425 exact URL repeats (LEAK-19, as wine_quality) but keeps 461 pairs that differ only by a trailing `/` after the host
(the same URL under RFC 3986) and 43 homepages listed under both labels. Precedents: **jm1** (2026-10-01, Lennart, LEAK-20:
the 176 rows whose feature vector occurs with both labels dropped, "to be on the safe side"); **emscad** (LEAK-21, reposts
identical except an id or location dropped). The reason given, "the rule is to keep the source's rows", is not a fact
that sets this case apart: jm1 and emscad were source rows too. The 43 conflicting homepages are not exact feature
copies (the fetched pages can differ), so LEAK-20 applies by analogy, not to the letter.

**Consistency check (AI, 2026-10-20):** your call on phiusil_phishing (keep the 461 trailing-slash twins and the 43
homepages listed under both labels, a departure from LEAK-19 to LEAK-21) differs from jm1 (2026-10-01, both-label copies
dropped) and emscad (reposts dropped), and from this definition's own drop of the 425 exact repeats. What sets
phiusil_phishing apart? (a) the twins and the conflicting homepages were fetched as different pages (their page
features differ), so they are distinct observations and the conflict is genuine label ambiguity of the source lists,
recorded as an exception; (b) treat it like jm1/emscad: drop the second copy of each trailing-slash pair and both rows of
the 43 conflicts (86 rows); (c) reopen jm1's drop; (d) change LEAK-19 to say what counts as the same URL.

**6. URL kept as a string (CLEAN rules; v1 dropped URL and Domain)**

Consistent. No curator precedent drops an input the deployed model would see because it is a string; the only related
register entry is perth_house_prices (ADDRESS kept as a string, AI, open). The check `dataset_identifier_column` is
accepted with the reason that URL is the input, not a row id, which matches website_phishing's practice of keeping the
raw signals a detector reads (2026-10-14). The verdict does not depend on it (LightGBM without URL text AUC 1.0000).

**7. URLLength kept with a `Potential leak, kept on purpose` note (LEAK-13, Must)**

Departs from a Must, with a reason. URLLength is `len(URL) - 1` for 100% of legitimate rows and 51.8% of phishing rows:
a class-specific recording convention, which LEAK-13 says to harmonise (recompute `len(URL)` for every row), as
**hepatitis_c_prediction** did (2026-09-30). The note borrows the wording LEAK-30 reserves for scaling over all rows
(bioresponse and others, Lennart 2026-10-19), a different mechanism. The stated reason is that the fix moves AUC from
0.99893 to 0.99895 and the definition says "recompute them if the dataset ever ships". LEAK-13 asks to measure first,
which was done, but a Must has no exceptions (principles.md). This is acceptable only while exclusion stands. If the
curator decides to ship, the precedent requires the recompute. Not a separate question for the curator now; the
mediator should state it as a condition attached to "ship anyway" in issue 1.

**8. Split: IID, hosts not held out, `ForcedIIDFromTemporal` (SPLIT-8, SPLIT-29, SPLIT-30)**

Consistent. **account_debt_south_africa** (SPLIT-8, Lennart 2026-10-12) ships IID tagged forced-IID when no time column
allows a temporal split; the huntprohibited_1m panel already listed phiusil_phishing among the consistent cases. Under
SPLIT-29 a host that carries the label would call for grouping, but the host-grouped and registered-domain-grouped
splits were measured and score the same (SPLIT-30: a probe hit is a question settled by measurement). Minor wording
point (checklist issue 4): "hosts recur for phishing only" conflicts with Decision 6's 54 hosts with both classes
(112 rows). It is a writing.md fix, not a precedent question.

**9. Year 2023 vs record 2024 (PROV-1, PROV-2)**

The definition follows the first publication (Mendeley Data, 2023-08-29), as PROV-1/PROV-2 ask; the record's 2024 is the
paper/UCI year. This is a field to sync, with no consistency question.

**For the mediator**

- Issue 1 (exclusion) and issue 3 (marker) follow prostate_cancer_detection and TP-4; no prompt.
- Issue 2 departs from the 2026-10-16 retirements (lgg, coad, corporate_credit_rating): prompt above. Neither drafted
  option matches the precedent, and the proposed `_too_late_to_add` path does not exist.
- Issue 5 departs from jm1 / emscad without a distinguishing fact: prompt above (moot if excluded).
- Decision 7 (URLLength) and issue 4 (URLCharProb): Must departures that are acceptable only while exclusion stands. If
  the curator ships, attach both as conditions (recompute URLLength per LEAK-13 as hepatitis_c; drop URLCharProb per
  LEAK-28 as santander unless the paper shows an outside list).
- anneal (2026-07-27, Trivial without proof) conflicts with TP-4 as it reads now. Flag it; do not follow it.

</details>

<details><summary>Advocate</summary>

**phiusil_phishing: advocate, opening brief (2026-10-20)**

"As defined" here means the definition as it stands: the folder, its drops, its IID split, and its recommendation to
exclude the dataset as `Data Quality Issue`. I argue for that definition. I do not argue that the file belongs in the
benchmark. The evidence rules that out, and the definition already says so.

**1. The verdict is right: exclude as Data Quality Issue (LEAK-13 to LEAK-15, Must; remedy ladder, last rung)**

* Evidence: every phase A agent reached this verdict on its own. A fixed rule with no training gets AUC 0.99981 and
  calls 38 of 100,520 phishing rows legitimate (claim audit, rows 8-9). URL features alone get 0.99881 and page
  features alone 0.99995 (claim audit, row 22). All 134,850 legitimate rows match `https://www.<host>`. In the column
  audit, the phishing page maxima sit below the legitimate medians. The blind reviewer, who read none of our files,
  says "exclude", and the practitioner says "reject this file".
* Rule: these are Must leaks in every feature family. The remedy ladder's milder rungs do not work here: no column
  drop, subset or re-split removes them (split audit: AUC 1.0 under the random, host and registered-domain splits).
  Exclusion is the rung for "a Must that cannot be fixed" (principles.md, How to decide 5).
* Outranks: the tension row "a real task against a leak" says to fix the leak and keep the task. That stops where the
  leak cannot be undone, which is the case here, as it was for prostate_cancer_detection (Lennart, 2026-09-30,
  precedents, decision 1).

**2. The marker is right: Data Quality Issue, not Trivial (TP-4, Must)**

* Evidence: the best single feature (the URL text) gets AUC 0.9973 and log loss 0.026, against the models' 0.99999
  and 0.0008-0.0041 (REVIEW issue 3; claim audit, row 18). TP-4's fold-by-fold proof therefore fails. The fixed rule
  is hand-built, so it is not a choice made on the training side.
* Precedent: prostate and lgg_low_grade_glioma were retired with DQI alone. anneal (Trivial without proof, 2026-07-27)
  predates TP-4, so it is flagged, not followed (precedents, decision 3).
* Outranks: P4 comes before P6. The leak is the decisive reading (evidence.md puts "solved" from a leak first).

**3. The drops are verified and needed whatever the outcome (LEAK-10, LEAK-14, CLEAN-5)**

* Evidence (claim audit, rows 7 and 19-21):
  * Title equals the URL rewrite in 99.96% of legitimate and 99.21% of phishing rows that have a title.
  * FILENAME is a number below 1M for 100% of legitimate rows and 0% of phishing rows.
  * Domain equals the URL authority in every row.
* The column audit re-checked all six drops and agrees. These drops are the cheapest fixes on the ladder and they are
  correct. They are the reason the definition is the cleanest version of this file.

**4. The split is right (SPLIT-1, SPLIT-4, SPLIT-8; split audit: "right with notes")**

* Evidence: log loss 0.00042 on the shipped splits, 0.00037 grouped by host and 0.00061 grouped by the last two host
  labels. The hidden-group probe found nothing: 11 candidates, gap -0.000 (split audit).
* The host is a property every new URL has, so SPLIT-4 counts it as a feature. There is no time axis for both classes,
  so ForcedIIDFromTemporal applies, as for account_debt_south_africa (Lennart, 2026-10-12).
* The "seen host" asymmetry the split audit raises (SPLIT-31) costs nothing at saturation. Its remedy belongs to a
  repaired version, not to this one.

**5. The definition's claims hold; the errors are wording, fixed by rewording (writing.md, PROV-1)**

* Evidence: the claim audit reproduced every number. Two claims were refuted, both minor:
  * "the collection period is not stated" is wrong: Mendeley says "mostly from 2023".
  * The record's `year` 2024 is wrong; the definition's 2023 is right.
* Three statements hold but need narrowing:
  * "Hosts recur for phishing only" leaves out 54 hosts (112 rows) that hold both classes.
  * HasSocialNet=1 is not a pure value (511 phishing rows have it).
  * The 425 duplicate pairs are two fetches, not identical rows.
* I concede all five. The fix that keeps the definition: reword those sentences and set the record's year to 2023.
  None of them touches the verdict.

**6. The kept-on-purpose items are moot under exclusion; they become conditions only if the curator ships**

* Three choices were noted and kept rather than fixed:
  * URLLength cut (LEAK-13, Must): effect AUC 0.99893 to 0.99895, which is noise.
  * URLCharProb (LEAK-28, still unconfirmed): AUC 1.0, log loss 0.00041, with and without it.
  * The near-copies and the 43 both-label homepages (LEAK-20/21, Should).
* Rule: independent failures are not conflicts. None of these changes the verdict, and fixing them would not rescue
  the dataset.
* I concede the precedents (hepatitis_c, santander, jm1): if the curator ships anyway, all three are conditions.
  Recompute URLLength, drop URLCharProb unless the paper shows an outside list, and drop the both-label pairs.
* I also concede issue 2. Once the curator decides on exclusion, follow the 2026-10-16 retirements (lgg, coad,
  corporate_credit_rating): remove the folder, clear `v2_path`, and cite the commit. The proposed `_too_late_to_add`
  path does not exist. Keeping the folder while the verdict is open is consistent (digicow, stroke_prediction).

**7. Fit "approximate" is the right label, not "none" (USE-8, USE-2, Must)**

* The practitioner says "none for practical purposes". USE-8 defines None as "no decision fits (USE-2)", with the
  marker No Good Target. But a decision does fit here: a gateway blocks or warns on a URL before the click, and the
  practitioner describes that actor (P3 holds).
* The failure is in the data (P4), which DQI records. Fit None would put the wrong marker on a real task.
* Concede: the gap is not one of the kinds USE-8 lists. The mildest fix is to name it in fit_reason as a sampling gap
  ("negatives are ranked homepages only"), not to switch to None.

Verdict as argued: keep the definition with its recommendation of exclusion (DQI). Reword the five statements, sync
the record's year, and remove the folder after the curator's decision, as the precedent requires.

**phiusil_phishing: advocate, rebuttal (2026-10-20)**

The critic and I agree on the verdict: exclude as `Data Quality Issue`. We disagree on one branch of one point.

**1. Label readable from collection (LEAK-13 to LEAK-15): concede**

This is my point 1. The facts and the precedent are the same: fixed rule 0.9998, URL-only 0.9989, page-only 0.99994,
every split at AUC 1.0, and prostate_cancer_detection. Mendeley v1 and v2 hold the same file, so no repair from the
origin exists (PROV-13). Exclusion is the remedy.

**2. Post-outcome pages (LEAK-10): concede**

50.5% of the phishing rows sit on 115 shared pages. Dropping the page features would not save the task, because the
URL features alone get 0.9989. It adds to the exclusion; it is not a separate remedy.

**3. Fit "approximate": concede the rewording, dispute the "otherwise none" branch**

* Conceded: the gap is not one of the kinds USE-8 names, and fit_reason should name it as a sampling of the negative
  class that replaces the task. This matches my point 7.
* Disputed: setting the fit to None. USE-8 defines None as "no decision fits (USE-2)", and its marker is `No Good
  Target / Scientific Discovery`. The critic itself keeps the marker at DQI because "the use case is real". A fit of
  None with a DQI marker would contradict USE-8 (Must).
* What wins: USE-8's own definition of None. Rewording fit_reason is the only change that is consistent with it.

**4. Record year (PROV-1): concede**

Set the record's year to 2023 (claim audit, row 40).

**5. Wording (writing): concede all three**

Mendeley's "mostly from 2023", the 54 hosts that hold both classes, and HasSocialNet=1 not being pure. These are my
point 5. I add the duplicate pairs: they are two fetches, not identical rows (claim audit, row 26).

**6. Conditions if shipped: concede**

These are my point 6: recompute the URL counts (LEAK-13), drop URLCharProb (LEAK-28) and drop the 43 both-label pairs
(LEAK-20). I also concede the wording point. `Potential leak, kept on purpose` is the LEAK-30 form, made for scaling
over all rows. A class-specific string cut is a LEAK-13 Must, so a note cannot carry it if the dataset ships. Under
exclusion it is moot.

**7. Folder after exclusion: concede**

Follow lgg, coad and corporate_credit_rating (2026-10-16). I accept the critic's addition: move the measured evidence
(fixed rule 0.9998, URL-only 0.9989, page-only 0.99994) into the record as an Assessment line before the folder goes,
so that it outlives the folder (EV-2: the measurement is the evidence).

**Net**

* Shared verdict: exclude as `Data Quality Issue`. Do not add `Trivial` (TP-4 is not proven; the critic agrees).
* One open point for the mediator: point 3's "otherwise none". USE-8 settles it toward rewording fit_reason and
  keeping "approximate".

</details>

<details><summary>Critic</summary>

**phiusil_phishing: critic's opening brief (2026-10-20, re-check)**

Position: **do not ship.** Exclude as `Data Quality Issue` (the definition's own recommendation). Points 4-7 are
changes to make whatever the curator decides, and conditions if the curator ships anyway.

**1. The label is readable from how each class was collected, in every feature family (P4; LEAK-13, LEAK-14, LEAK-15, Must)**

* Problem: all 134,850 legitimate rows are bare `https://www.<host>` homepages of a ranked list with full pages (>= 102
  lines); phishing rows are feed URLs (627 of 100,520 share the template) whose pages were fetched later.
* Effect: a model learns "top-list homepage or not", not "phishing or not". Every method scores AUC 1.0000, so the
  dataset ranks nothing and measures the wrong thing.
* Evidence: fixed rule with no training AUC 0.9998 (38 of 100,520 phishing misread; claim audit 8-9). URL features alone
  0.9989, page features alone 0.99994 (claim 22, column audit problem 1). Random, host-, registered-domain- and
  near-copy-grouped splits all AUC 1.0000 (split audit). The blind reviewer, with no notes, reached the same verdict on
  its own (http 0 legit, no-`www.` 0 legit, path 0 legit). Source has no repaired version: Mendeley v1 and v2 hold the
  same file (checklist, P5 row; PROV-13 cannot apply).
* Rule: LEAK-15 says a subset does not help when the artefact runs across the whole feature space: "retires the
  dataset". Precedent: prostate_cancer_detection (retired 2026-09-30, same facts); hepatitis_c and biogeographical were
  kept only because a fix existed (precedents, decision 1). The tension row "a real task against a leak" stops at a leak
  that cannot be undone.
* Remedy: exclusion. No milder rung works: no repair (one file), no drop or subset (both families saturate), no re-split
  (all splits saturate), and a note cannot carry a Must.

**2. Half the positives are post-outcome pages (P4; LEAK-10, Must)**

* Problem: 50,748 phishing rows (50.5%) sit on 115 shared stub or takedown pages (page 1: Firebase "site not found",
  6,159 rows); 0 legitimate rows do. Password fields, Bank and Pay flags are more common among legitimate rows.
* Effect: the page features describe the page after the phish was taken down, not what the detector sees at the
  prediction point.
* Evidence: claim audit 16 and 23; column audit facts (phishing medians LineOfCode 12, NoOfImage 0, NoOfJS 0);
  practitioner section 1.
* Remedy: dropping the 26 page features would be the LEAK-10 fix, but point 1 shows the URL family alone still gives
  0.9989, so it does not save the task. Part of the exclusion.

**3. The fit "approximate" understates the gap (P3; USE-8, USE-5, Must)**

* Problem: USE-8 names the approximate gaps (snapshot for forecast, kept leak, reconstructed time, no horizon, one
  judge). "Negatives are only top-list homepages, positives partly dead pages" is none of them; it replaces the target
  the actor acts on (USE-5): the practitioner's real negatives are deep links, login pages and benign pages on the same
  shared hosts, none of which are in the file.
* Evidence: practitioner, "Fit: none ... at most approximate in name only"; gaps 1 and 2.
* Remedy (definition text, mild): keep `fit = "approximate"` only if fit_reason names the gap as a sampling of the
  negative class that replaces the task; otherwise set the fit to none. The marker stays `Data Quality Issue` (point 1
  decides), not `No Good Target`: the use case is real, the data is not.

**4. Record year is wrong (P5; PROV-1, Must)**

* Evidence: record `year: 2024`; first publication Mendeley v1 2023-08-29 (claim audit 40, refuted). Definition 2023 is
  right.
* Remedy: set the record's year to 2023.

**5. Two statements in the definition are refuted or loose (writing; P7-level, no bearing on the verdict)**

* task_summary `row`: "the collection period is not stated" is refuted: Mendeley says "mostly from 2023" (claim 3).
  Remedy: say so.
* "hosts recur for phishing only" (curation_comments Note, Decision 6): 54 hosts (112 rows) hold both classes (split
  audit problem 3). Remedy: "apart from 54 hosts that hold both classes".
* accepted warning `dataset_pure_feature_value`: HasSocialNet = 1 is not pure (511 phishing rows; claim 35). Remedy:
  reword.

**6. Conditions if the curator ships anyway (P4; LEAK-13 and LEAK-28, Must; LEAK-19/20, Should)**

A Must has no exceptions (principles.md), so a "ship" must carry these, not notes:
* LEAK-13: recompute URLLength and every count and ratio from `URL` with one rule. The `Potential leak, kept on
  purpose` wording is LEAK-30's (scaling over all rows), a different mechanism (precedents, decision 7;
  hepatitis_c harmonised).
* LEAK-28: drop URLCharProb unless the paper shows an outside list; its fit to this file's legitimate rows (MAD 0.0036
  vs 0.0115 for all rows) is a measured suspicion, and dropping it costs nothing (AUC 1.0000 without it).
* LEAK-20 (Should): drop both rows of the 43 homepages under both labels, as jm1; no fact sets this case apart.
These would not change point 1; they only make a shipped version honest about what it is.

**7. After exclusion, follow the 2026-10-16 retirements for the folder (house rule, consistency)**

* Problem: REVIEW issue 2 offers to keep the folder or move it to `_maintenance/_out_of_scope/_too_late_to_add/`,
  a path that does not exist; lgg_low_grade_glioma, coad_colon_adenocarcinoma and corporate_credit_rating (Data Quality
  Issue, never built) had their folders removed, `v2_path` cleared and the definition left in git (precedents,
  decision 2; CLAUDE.md working-copy rule).
* Remedy: treat it like them, with the measured evidence (fixed rule 0.9998, URL-only 0.9989, page-only 0.99994) moved
  into the record as an Assessment line before the folder goes. Not a reason to exclude; a consequence of it.

Judgment record (critic's view):

```text
Verdict: don't ship.
Validity: SEL-1, SEL-2 hold; USE-8 fit overstated (fix text); LEAK-13/14/15 triggered, cannot be fixed (exclude,
  Data Quality Issue, as prostate_cancer_detection); LEAK-10 triggered (page features, half the positives); SPLIT-1
  holds; PROV-1 record year wrong (fix).
Value: TP-6 solved, TP-3 no spread (consequences of the leak; TP-4 Trivial not proven, keep it off).
Quality: wording fixes (point 5).
For the curator: issue 1 (exclude), issue 2 (folder, follow lgg/coad).
```

**phiusil_phishing: critic's rebuttal (2026-10-20)**

The two briefs agree on the verdict (exclude, `Data Quality Issue`). The advocate argues for the definition as it
stands with its recommendation to exclude; I argued against shipping the file. These are the same outcome. Nothing new
came up, so I add no points.

| Advocate point | Answer | Why |
|---|---|---|
| 1. Exclude as DQI (LEAK-13/14/15) | concede | Same evidence and rule as my points 1-2 (fixed rule 0.99981, URL-only 0.99881, page-only 0.99995, every split AUC 1.0; prostate_cancer_detection). |
| 2. DQI, not Trivial (TP-4) | concede | URL text 0.9973 / 0.026 against 0.99999 / 0.0008-0.0041 fails TP-4's fold-by-fold proof; anneal predates TP-4. My judgment record already leaves Trivial off. |
| 3. The six drops are verified | concede | The claim audit (rows 7, 19-21) and the column audit agree. I raised nothing against them. |
| 4. IID split is right | concede | Split audit: "right with notes"; host-grouped 0.00037 vs 0.00042. The SPLIT-31 asymmetry belongs to a repaired version only. |
| 5. Wording errors, record year | concede | These are my points 4-5, with the same remedy. One addition: the advocate's third narrowing (duplicate pairs are two fetches, claim 26) is right and should be part of the same rewording. |
| 6. Kept-on-purpose items moot; conditions if shipped; folder per lgg/coad | concede, with one narrow dispute | The conditions and the folder match my points 6-7. Dispute: "moot" holds for the verdict, not for the text. The definition calls a LEAK-13 (Must) departure `Potential leak, kept on purpose`, the wording LEAK-30 reserves for scaling over all rows (precedents, decision 7). A Must has no exceptions (principles.md, Strengths), and the definition stays in git as the evidence. So its URLLength bullet should say "a LEAK-13 departure, acceptable only because the dataset is excluded; recompute if shipped", not borrow LEAK-30's label. This is a wording fix and does not change the verdict. |
| 7. Fit stays "approximate", name the gap in fit_reason | concede | My point 3 offered the same mildest remedy. The advocate is right that None would bring the `No Good Target` marker (USE-8) onto a task whose actor and decision are real (USE-2 holds), so I drop "or set the fit to none". The remaining ask: fit_reason names the sampling gap ("negatives are ranked homepages only, half the positives are pages fetched after takedown"). |

**Remaining for the mediator**

* Agreed: exclude as DQI; keep the six drops and the IID split; fix the six wording points and the record's year; name
  the sampling gap in fit_reason; if shipped, the three conditions (LEAK-13 recompute, URLCharProb drop, LEAK-20 drop);
  after exclusion, remove the folder as for lgg/coad.
* Open (wording only): relabel the URLLength bullet from LEAK-30's "kept on purpose" to a stated LEAK-13 departure.

</details>

<details><summary>Mediator</summary>

**phiusil_phishing: mediator (2026-10-20, re-check)**

**Judgment record**

```text
Verdict: don't ship (No, Data Quality Issue; the curator's call).
Validity: SEL-1, SEL-2 hold; USE-2 holds (real actor and decision); USE-8 fit stays approximate, fit_reason names the
  sampling gap; LEAK-13/14/15 triggered, cannot be fixed (exclude, as prostate_cancer_detection); LEAK-10 triggered
  (page features fetched after takedown for 50.5% of phishing rows), adds to the exclusion; SPLIT-1 holds (IID,
  ForcedIIDFromTemporal; host-grouped scores the same); PROV-1 record year wrong (fix to 2023).
Value: TP-6 solved and TP-3 no spread, both consequences of the leak; TP-4 not proven, no `Trivial` marker.
Quality: wording fixes (below); URLLength bullet relabelled as a LEAK-13 departure.
For the curator: issue 1 (exclude), issue 2 (folder after exclusion, follow lgg/coad/corporate_credit_rating).
```

**The disputed point: the URLLength label**

* **Critic:** the label is LEAK-30's. The departure is from LEAK-13, which is a Must. So the bullet should state it as a LEAK-13 departure, acceptable only because the dataset is excluded, with a recompute required if it ships.
* **Advocate:** conceded the substance (rebuttal point 6) but called it moot under exclusion.
* **Rules:**
  * LEAK-30's keep-with-a-note form (`Potential leak, kept on purpose:`) is scoped to "features the source transformed with statistics over all rows". A string cut that differs by class is outside that scope.
  * LEAK-13 (Must) says to harmonise the convention.
  * Under principles.md, Strengths, a Must has no exceptions: a violation is fixed in the definition or the verdict is `No`. The "keep with a documented note" rung of the remedy ladder is therefore not available for a LEAK-13 violation.
  * The text is not moot. The definition stays in git as the evidence the record cites, and a borrowed label would teach the wrong remedy for LEAK-13.
* **Outcome:** this is a conflict of wording, not of rules, and the critic wins by rule scope. The fix is the cheapest remedy and changes nothing about the verdict. If the curator ever ships, the rule's own remedy applies: recompute len(URL) and the counts derived from it, as for hepatitis_c_prediction.

**Changes that need no decision**

1. **URLLength bullet** (dataset.py, curation_comments): replace "Potential leak, kept on purpose:" with wording such as "LEAK-13 departure, acceptable only because the dataset is excluded: …; recompute len(URL) and the URL counts if it ever ships." Rule: LEAK-13 (Must); LEAK-30 scope; principles.md, Strengths.
2. **fit_reason** (USE-8): keep `fit="approximate"`. Name the gap as a sampling of the negative class that replaces the task: "negatives are ranked homepages only; half the positives are pages fetched after takedown". Do not use None: USE-8 defines None as "no decision fits", and that would bring the `No Good Target` marker, which both sides reject.
3. **Record year** 2024 → 2023 (PROV-1; Mendeley v1, 2023-08-29).
4. **Wording** (writing.md):
   * task_summary: the collection period is "mostly 2023" (Mendeley), not "not stated".
   * "hosts recur for phishing only" → "apart from 54 hosts (112 rows) that hold both classes".
   * The accepted warning `dataset_pure_feature_value`: HasSocialNet = 1 is not pure (511 phishing rows).
   * Duplicate pairs: they are two fetches, not identical rows (claim 26).
5. **No `Trivial` marker** (TP-4 not proven: URL text 0.9973 against the models' 0.99999; anneal predates TP-4 and is not followed).
6. **Conditions if shipped anyway**, written into issue 1's "ship" alternative. They are not notes:
   * recompute URLLength and the counts from `URL` (LEAK-13);
   * drop URLCharProb unless the paper shows an outside list (LEAK-28; santander);
   * drop both rows of the 43 homepages listed under both labels (LEAK-20; jm1).
7. **Before the folder goes**, add an Assessment line to the record with the measured evidence: fixed rule AUC 0.9998, URL-only 0.9989, page-only 0.99994, every split AUC 1.0 (EV-2).

**Questions for the curator**

1. **Exclude phiusil_phishing as `No`, `Data Quality Issue`?** (P4, LEAK-13/14/15, Must.)
   * The problem: the two classes were collected in different forms. Every legitimate row is `https://www.<domain>`, and half of the phishing pages were fetched after takedown. Every feature family separates the classes.
   * Evidence: fixed rule 0.9998 with no training; URL-only 0.9989; page-only 0.99994; untuned models 0.99999+.
   * Mendeley v1 and v2 hold the same file, so there is nothing to repair from (PROV-13).
   * Both sides recommend exclusion. If you ship instead, change 6 applies.
2. **The folder after exclusion** (consistency; house rule).
   * Both sides recommend following lgg, coad and corporate_credit_rating (2026-10-16): remove the folder, clear `v2_path`, cite the commit in the record.
   * The draft's `_maintenance/_out_of_scope/_too_late_to_add/` path does not exist.
   * Keeping the folder would need a fact that sets this case apart, recorded as an exception.

**Agreed facts**

* Fixed rule AUC 0.9998 (38 of 100,520 phishing rows wrong).
* Untuned LightGBM / RF / linear: AUC 0.9999992 / 0.9999981 / 0.9999875; log loss 0.0008 / 0.0041 / 0.0024.
* URL-only 0.9989; page-only 0.99994; URL text alone 0.9973 / 0.026.
* 50,748 phishing rows (50.5%) sit on 115 shared pages.
* All legitimate rows are https://www. homepages.
* Mendeley v1 equals v2; first publication 2023-08-29.
* URLLength = len(URL) − 1 for every legitimate row and 52,090 phishing rows. The fix moves AUC from 0.99893 to 0.99895.
* URLCharProb fits this file's legitimate rows (MAD 0.0036 vs 0.0115 for all rows); AUC unchanged without it.
* Host-grouped split scores the same as IID.
* 54 hosts (112 rows) hold both classes.
* The six column drops are verified.

**Consistency with precedent**

* **Exclusion:** follows prostate_cancer_detection (LEAK-15, DQI). It is set apart from hepatitis_c_prediction and biogeographical_ancestry_prediction, where a fix existed.
* **Marker:** follows lgg (DQI only). anneal (Trivial without proof) conflicts with TP-4: flag it, do not follow it.
* **Folder:** follows lgg, coad and corporate_credit_rating.
* **Split:** follows account_debt_south_africa (forced IID).
* **URLLength relabel:** follows hepatitis_c_prediction (LEAK-13 harmonised) and keeps LEAK-30's label for its own cases (bioresponse and others, 2026-10-19).
* **Near-duplicates (Should):** keeping them departs from jm1 and emscad with no distinguishing fact. Moot under exclusion and carried as condition 6 if shipped.
* No drift and no third exception found.

Sources: all panel reports; `dataset.py` (the URLLength bullet, fit_reason); the record (year, v2_path);
`leak_checks.md` (LEAK-13, LEAK-30).

</details>

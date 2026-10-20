# phiusil_phishing

**Outcome:** added; recommended exclusion (`Data Quality Issue`). The UCI 967 file (235,370 URLs), binary target
phishing or legitimate, IID; FILENAME, URLSimilarityIndex, Title and the two scores computed from Title are dropped
as construction artifacts. The two classes were collected in different forms (URL template, page fetch timing), so
every feature family separates them and no version of the file is a valid task; the AI recommends excluding it.

**Main points:** Solved by how the two classes were collected (URL template, page fetch timing). No version of the
file is a valid task.

**Record fields that disagree with the definition:**

- `year`: record `2024`, definition `2023`.

**Issues for Lennart:**

1. **Should phiusil_phishing go into TabArena v0.2 at all?**
   - Implemented: Exclusion is recommended in curation_comments and in the accepted-warning reason. The definition is
     the cleanest one available: FILENAME, URLSimilarityIndex, Title, DomainTitleMatchScore, URLTitleMatchScore and
     Domain are dropped, URL is kept as text, the split is IID, and every remaining artifact is documented with numbers.
   - Alternative: Ship it anyway. Reviewer 1 points out that this is not a fixed version of the task: for half of the
     phishing rows the page side records what the URL served after it was listed, and without the page features the URL
     template alone still separates the classes. No version of this file is a valid task.
   - Numbers: Fixed rule with no training: AUC 0.9998, 38 of 100,520 phishing rows misclassified. Untuned LightGBM /
     random forest / linear: AUC 0.9999992 / 0.9999981 / 0.9999875, log loss 0.0008 / 0.0041 / 0.0024, spread 0.000023.
     URL features alone 0.9989, page features alone 0.99994. 50,748 phishing rows (50.5%) sit on 115 shared pages, none
     with a password field. Published audits say the same (ollivianguy/phishing-url-detection: AUC 1.000 all features,
     0.999 URL-only; awesomedudeworld13/phish-drift: an https://www. regex gets TSS 0.99).

2. **If the dataset is excluded, where does its folder live? (Reviewer 3, finding 7)**
   - Implemented: The folder stays in datasets/_dev/tabarena-v0pt2/phiusil_phishing/, since Lennart asked to add the
     dataset. It has no build or UUID; the README table lists it as not built.
   - Alternative: Move dataset.py and README.md next to the v1 notebook under
     datasets/_maintenance/_out_of_scope/_too_late_to_add/phiusil_phishing/, give the working copy no README row, and
     add one line with the published results to the record.
   - Numbers: tuned_results.py: not in the cached results, so no tuned evidence can overturn the flags. Published
     results: AUC 1.000 with all features and 0.999 URL-only (ollivianguy); regex TSS 0.99 and 0.000 on live URLs
     (phish-drift README); Kaggle notebook without URLSimilarityIndex, AUC 0.9995 (somanshumahajan).

3. **Which marker goes on the record? (Reviewer 3, finding 6)**
   - Implemented: Data Quality Issue is the decisive marker: the classes were recorded differently through every feature
     family, as in LEAK-13 to LEAK-15 and prostate_cancer_detection. Trivial is used only in the sense of 'solved
     perfectly' (TP-4, criterion 4C).
   - Alternative: Also justify Trivial with the fixed rule or rule 4, or use Trivial alone.
   - Numbers: Rule 4 needs the raw feature to match the methods fold by fold. The URL text gets 0.9973 and the fixed
     rule 0.9998, while all three families reach >= 0.99999 with log loss 0.0008-0.0041 against a prior of 0.682.

4. **Keep URLCharProb, whose character distribution may come from this file's legitimate rows? (Reviewer 3, finding 4; TLDLegitimateProb is settled as an outside prior)**
   - Implemented: Kept, with the comment reworded: it is the mean probability of the URL's characters under a
     distribution of legitimate domain names, either this file's legitimate rows or the outside list, which is open
     until someone reads the paper.
   - Alternative: Drop URLCharProb as a possible class-conditional statistic over all rows (LEAK-28, criterion 4D), or
     ask Lennart for the paper PDF first.
   - Numbers: Frequencies from legitimate rows: MAD 0.0036, and 0.0015 for alphanumerics only. From all rows: MAD
     0.0115, correlation 0.96. No variant matches more than 4.6% of rows within 1e-4. AUC 0.77 alone. Without
     URLCharProb and TLDLegitimateProb, LightGBM gets AUC 1.000000, log loss 0.00042 (the same as with them).

5. **Near-identical URLs: keep them or drop them? (Reviewer 2, finding 3)**
   - Implemented: All rows are kept (the rule is to keep the source's rows) and documented in the Duplicates and Note
     bullets and in decision table 6.
   - Alternative: (a) Drop the second copy of the 461 pairs that differ only by '/' after the host, the same URL under
     RFC 3986 §6.2.3, for consistency with the exact-repeat drop. (b) Drop both rows of the 43 homepages listed under
     both labels (86 rows, 0.04%).
   - Numbers: 3,276 groups (6,856 rows: 6,813 phishing, 43 legitimate) are one URL up to scheme, www. or a trailing
     slash. Per final split, 1,551-1,624 phishing test rows (4.6-4.8%) have such a twin in train (493-558 for a trailing
     slash alone), and 13-20 of the 43 conflicting pairs straddle train and test. None of this moves the scores, which
     are at AUC 1.0000.

6. **Keep the raw URL as a string feature (v1 dropped URL and Domain)?**
   - Implemented: URL is kept: it is what a detector classifies. Domain is dropped as the URL's authority part.
     dataset_identifier_column is accepted.
   - Alternative: Drop URL as v1 did and keep only the source's numeric URL features and TLD.
   - Numbers: URL text alone: AUC 0.9973 / log loss 0.026 (task probe) and 0.99915 / 0.0133 (character n-gram LR).
     Without the URL text, LightGBM gets AUC 1.0000 / 0.0004, so the verdict does not depend on this choice.

# qsar_oral_toxicity

**Outcome:** added. The very toxic endpoint (rat oral LD50) of UCI 508 from 1,024 ECFP bits, binary, IID with the
default random splits; copies of a parent structure and vectors with both classes are dropped (8,493 chemicals). The
AI recommends shipping it.

**Main points:** Parent-structure copies are dropped, unlike the source. The split is random, while the scores depend
on close analogues.

**Record judgment:** valid. The labels are the very toxic endpoint of the calibration set of the ICCVAM acute oral
toxicity project (CATMoS), and the data is unique. Fingerprints are in scope by the qsar_tid_11 precedent: on our
folds a random forest (ROC AUC 0.883) matches a Tanimoto nearest-neighbour model of the paper's N3 kind (0.877).

**Issues for Lennart:**

1. **Parent-structure copies dropped, unlike the source.**
   - Question: drop the salt-form copies (implemented) or keep the source's rows?
   - Evidence: 499 of 8,992 rows (5.5%) are dropped. The paper says "No molecules were removed". 7.6% of the authors'
     test molecules have an exact bit-vector copy in their training set. 237 of the project's 2,894 evaluation chemicals
     (8.2%) have their parent in the training file.
   - Implemented: drop exact copies and conflicting vectors (wine_quality / jm1 precedent).
   - Alternative: keep all 8,992 rows and group the split on the bit vector (8,504 groups). Each salt form keeps its own
     label, and a test parent is still never in train.
   - **Verification:** closed in favour of what is implemented. The drop is class-neutral (33 of 741 very toxic rows,
     4.5%, against 466 of 8,251, 5.6%; the positive share moves from 8.24% to 8.34%), and it is exactly what
     `leak_checks.md` §5 prescribes (exact copies with one label dropped as in wine_quality, every copy of a both-class
     vector dropped as in jm1). The 11 conflicting vectors are real chemistry rather than label noise, so they are
     unpredictable from the bits either way, and 22 of 8,515 rows cannot move the score.

2. **Random split, while the score depends on close analogs.**
   - Question: is the IID split what you want for a QSAR set?
   - Evidence: random forest AUC rises from 0.681 for test chemicals with no training analog above Tanimoto 0.5 (11% of
     the test rows) to 0.954 for those above 0.85. Both source protocols are random. The real use is screening lists of
     regulatory interest (48,137 chemicals in the project's prediction set), which hold many analogs of tested
     chemicals.
   - Implemented: IID (no group key in the file; "hidden groups need context").
   - Alternative: a scaffold or cluster split. It needs structures. The UCI rows carry no identifier: within each block
     they look like CASRN order (next-row class agreement 0.873 against 0.876 in the NTP file), but linking them would
     need Dragon 7's ECFP. It would be a new dataset built from the NTP structures with a featurisation of our own,
     which I do not recommend.
   - **Verification:** closed in favour of the IID split. The clustering above shows no congeneric series to memorise
     (692 distinct clusters for 708 very toxic chemicals at Tanimoto 0.9, largest cluster 6 rows overall), and both
     classes have the same analog density, so the similarity gradient is the applicability domain every QSAR model has.
     Both source protocols are random, and the project's is structure-blind on purpose. After the deduplication no
     chemical occurs twice, so there is no repeated entity to hold out, and a similarity-threshold cluster is barred as
     a group key (`leak_checks.md` §5). The `curation_comments` "Note" bullet now carries these numbers.

3. **Only the calibration part of the VT data is on UCI.**
   - Question: extend the dataset with the project's evaluation set?
   - Evidence: the full VT data is 11,886 chemicals. The evaluation set (2,894 chemicals, 243 very toxic; labels in NTP
     `validationset.txt`) has fingerprints only in the Milano group's download ("Molecular descriptors calculated in
     this study for the training, test and validation molecules are available for download", Sec. 2.2). That download
     needs a form with your name and e-mail, and its site blocks this machine.
   - Implemented: UCI only (8,493 after deduplication).
   - Alternative: download the package by hand (up to +34% chemicals, fewer after the parent copies are dropped). The
     page offers "MATLAB code and data to reproduce the QSAR models" of the paper, so it presumably also holds the
     nontoxic (NT, LD50 >= 2,000 mg/kg) endpoint with ECFP_1024_05 bits, a better-balanced second task (3,848 of 8,981
     positive, confirmed in the NTP file). Not verified: the package was not downloaded.
   - **Verification:** stays open, Lennart's call. The verifier did not try the form either and proposes no change to
     the shipped dataset.

4. **Scope of fingerprint features** (the notes asked).
   - Question: keep vectorised molecules in scope?
   - Evidence and implemented: kept, by the qsar_tid_11 precedent and the numbers in "Record judgment".
   - Alternative: a stricter modality rule would also remove qsar_tid_11 and hiva_agnostic.
   - **Verification:** closed, in scope. The guideline's exclusion covers features describing image content; a
     fingerprint is a vectorised molecular graph, qsar_tid_11 is the shipped precedent, and on our folds a random forest
     matches a nearest-neighbour model of the paper's own kind.

5. **Minor.**
   - The fingerprint variant is not stated (ECFP_1024_02 or _02R; the data fits 2 bits per fragment, so it is not _05).
     The comments say so. **Verification:** the verifier confirmed the three variants and their bits per fragment in
     Table 2, and that the two rows with 2 bits set are the two chemicals whose QSAR-ready structure is a single carbon.
   - `domain` follows the record ("chemistry & material science", as qsar_tid_11 and hiva_agnostic). qsar_biodeg,
     qsar_aquatic_toxicity, qsar_fish_toxicity, clock_protein_toxicity and bioresponse use "biology & life sciences";
     one convention for these QSAR sets would be cleaner. **Verification:** closed, the value is right: UCI gives the
     subject area as "Physics and Chemistry". The inconsistency among the older folders is a separate question.
   - The BibTeX cites Ballabio et al. 2019 (key) and Mansouri et al. 2021 for the label data. **Verification:** matches
     UCI's citation request.

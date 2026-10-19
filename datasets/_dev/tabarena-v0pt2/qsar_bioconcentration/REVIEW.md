# qsar_bioconcentration

**Outcome:** added. UCI 510's 776 chemicals with the three-class bioconcentration mechanism as the target, the 9
Dragon descriptors plus 193 RDKit 2D descriptors of the repaired SMILES (the string itself dropped), IID. The AI
recommends shipping it.

**Main points:** The three-class task. Three swapped chemical pairs are repaired from the authors' 2015 table. In
TabSTAR's pretraining with two classes swapped.

**Record judgment:** valid with concerns: the paper text is unread (the class thresholds are inferred from the data,
600 of 607); the 9 descriptors were selected on 75% of the labelled data.

**Issues for Lennart:**

1. **Target: class (implemented) or logBCF regression.** The class is a rule on logBCF and the experimental logKOW,
   so each framing must drop the other column. Implemented: the class, the dataset's published name and
   the task the 9 descriptors were selected for; modest, real signal (random forest macro AUC 0.751, log loss 0.746 vs
   0.883; with the 9 descriptors). Alternative: logBCF regression (random forest R^2 0.718, a line on MLOGP alone
   0.626), a KOW-dominated task, as a `_reg` folder if both are wanted.

2. **Swapped pairs repaired (implemented) or dropped.** Repaired: the 2015 table gives all six chemicals with their
   right SMILES and the logBCF of UCI 510, and each file class follows the rule with the chemical's own experimental
   logKOW (four of six would change class with the partner's). Alternative: drop the six rows as in the first round (770
   rows: 452 / 64 / 254). Either way the swap is worth reporting to the authors or UCI.

4. **Class thresholds inferred, paper text unread.** The ±0.5 log-unit band around the TGD line reproduces 600 of 607
   classes (experimental logKOW >= 1); below logKOW 1 the authors put 38 of 45 chemicals in class 1, a convention only
   the paper can state. Google `"Investigating the mechanisms of bioconcentration through QSAR classification trees"
   pdf` (BOA/IRIS 10281/101916 has no file).

5. **Descriptor selection on labelled data (kept with a note).** Paired test inside one cross-validation (776 rows,
   out-of-fold, 10 repeats): random forest macro AUC +0.064 on the authors' training chemicals vs their test chemicals
   (null -0.002, sd 0.041, p = 0.06); logistic regression +0.003 (p = 0.48); the 9 descriptors score like 217 RDKit
   descriptors. Same call as home_credit_default_risk.

6. **Domain convention among the QSAR siblings.** Implemented "chemistry & material science" (the record;
   qsar_oral_toxicity too), while qsar_fish_toxicity, qsar_aquatic_toxicity and qsar_biodeg use "biology & life
   sciences".

7. **Pretraining overlap (your call, no change).** TabSTAR lists OpenML 46585 (this data) in
   `tabstar_paper/benchmarks/folds_pretrain.py`. Its annotation also maps "2" to "Metabolized/Eliminated" and "3" to
   "Additional Storage Sites", the reverse of the old UCI page and of the rule (class 2 lies above the TGD line).

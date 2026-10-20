# sarcoma

**Outcome:** added. TCGA sarcoma from the multi-omic benchmark of Rappoport & Shamir (2018): 201 patients, 25,971
expression, methylation and miRNA features, multiclass target the expert-reviewed histological type (five classes),
IID over patients. The AI recommends shipping it.

**Main points:** Labels from TCGA's expert review (pinned GDC file). DDLPS is defined by MDM2 (a one-feature class).
Merge UPS and MFS?

**Record fields that disagree with the definition:**

- `problem_type`: record `Binary Classification`, definition `Multiclass Classification`.

**Record judgment:** valid with concerns (the label is the pathology diagnosis, not an omics output).

**Issues for Lennart:**

1. **Label from a second source (implemented: TCGA's reviewed histology, pinned GDC file).** Alternative: the
   submitted `histological_type` on all 246 rows (random forest macro AUC 0.940, log loss 0.742 in the first
   version), which keeps non-sarcomas and genotype-discordant samples.

2. **DDLPS is a one-feature class under the reviewed labels (MDM2 mRNA ROC AUC 1.000; generated probe `rule_leaves`).**
   Implemented: kept as the entity's definition. Alternative: none that keeps the reviewed label; the submitted label
   is less crisp (0.936) because it holds misdiagnoses the review fixed.

3. **MFS vs UPS:** the study finds them "largely indistinguishable across multiple platforms" and analyses them "as
   a single spectrum of disease"; here a model separates them at about AUC 0.73 (verifier). Implemented: five
   classes. Alternative: one UPS/MFS class (61 rows), the study's own convention.

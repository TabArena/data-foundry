---
unique_name: freddie_mac_single_family_lgd
name: 'Freddie Mac Single-Family Loan-Level Dataset: loss given default'
original_source: Company
year: '2026'
domain: finance
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.freddiemac.com/research/datasets/sf-loanlevel-dataset
needs_review:
- suggestion
type_adapter_id: curation-record-v1
---

## Comments

Created on 2026-10-26 at Lennart's ask (lgd, REVIEW issue 10): "retire it, and create a record for the better LGD source please". A real source for the loss-given-default task the textbook lgd file could not stand for. Not screened yet.

CC (2026-10-26, Lennart): create a record for the better LGD source.

**Note (AI, 2026-10-26):** facts gathered for screening (records_research run of 2026-10-26):
- Data: about 56 million US single-family mortgages originated from 1999 to March 2026 (Standard and Non-Standard); release 47 (2026-07-29) holds 49.21M Standard loans; a monthly performance file per loan. Free registration on Freddie Mac's Clarity portal; a random sample of 50,000 loans per vintage.
- Loss fields per disposed loan: Zero Balance Code (02 third-party sale, 03 short sale or charge-off, 09 REO disposition, 15 whole-loan sale), its effective date and the due date of the last paid installment, Net Sales Proceeds, MI and non-MI recoveries, expenses (legal, maintenance and preservation, taxes and insurance, other), Zero Balance Removal UPB, delinquent accrued interest, Estimated LTV (from April 2017), and Actual Loss, empty for loans disposed in the 3 months before the cutoff.
- Task: LGD = Actual Loss / Zero Balance Removal UPB for the loans with codes 02, 03, 09 or 15 and no defect settlement, predicted at default (90 or 180 days past due) from the origination fields and the state at default (UPB, ELTV, loan age, modification, mortgage insurance); split by default date, leaving out recent defaults not yet resolved (the target would lean to quick resolutions).
- Terms (fre_terms_conditions_sflld.pdf): internal research use; no making the data or derived products available to third parties without a separate licence; published research may not let anyone recreate the data. Only a definition could ship, built by each user from their own download.
- Alternative: Fannie Mae's Single-Family Loan Performance Data (registration, internal use only), with more detailed loss components but no ready actual-loss field.

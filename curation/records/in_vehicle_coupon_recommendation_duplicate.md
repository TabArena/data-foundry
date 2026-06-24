---
unique_name: in_vehicle_coupon_recommendation_duplicate
name: in_vehicle_coupon_recommendation
suggestion: 'No'
decision_markers:
- Duplicate
original_source: UCI
year: '2017'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C5GS4P
type_adapter_id: curation-record-v1
---

# in_vehicle_coupon_recommendation

## Comments

Shipped in the BeyondArena / TabArena (v0.1) collection(s).

TabArena curation verdict: Tabular.

data was collected via a survey on Amazon Mechanical Turk. The survey describes different driving scenarios including the destination, current time, weather, passenger, etc., and then ask the person whether they will accept the coupon if they are the driver. features might be time invariant, but need to check

Potential issue: "faked" data via a survey

Lennart: Leaning towards yes, features seem time invariant; but data source might be fake

Andrej: Need to test whether time-invariant; Mechanical turk data might be interesting to include

## Reference

A Bayesian framework for learning rule sets for interpretable classification By Wang, Tong, Cynthia Rudin, Finale Doshi-Velez, Yimin Liu, Erica Klampfl, and Perry MacNeille. 2017
 Published in The Journal of Machine Learning Research 18, no. 1

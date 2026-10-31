"""Curated dataset definition for `coil_2000` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary

# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "avgAge": ["20-30 years", "30-40 years", "40-50 years", "50-60 years", "60-70 years", "70-80 years"],
    "romanCatholic": [
        "0%",
        "1 - 10%",
        "11 - 23%",
        "24 - 36%",
        "37 - 49%",
        "50 - 62%",
        "63 - 75%",
        "76 - 88%",
        "89 - 99%",
        "100%",
    ],
    "contributionPrivateThirdPartyInsurance": ["f 0", "f 1 - 49", "f 50 - 99", "f 100 - 199"],
    "protestant": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "otherReligion": [0, 1, 2, 3, 4, 5],
    "noReligion": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "married": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "livingTogether": [0, 1, 2, 3, 4, 5, 6, 7],
    "otherRelation": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "singles": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "householdWithoutChildren": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "householdWithChildren": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "highLevelEducation": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "mediumLevelEducation": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "lowerLevelEducation": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "highStatus": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "entrepreneur": [0, 1, 2, 3, 4, 5],
    "farmer": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "middleManagement": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "skilledLabourers": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "unskilledLabourers": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "socialClassA": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "socialClassB1": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "socialClassB2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "socialClassC": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "socialClassD": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "rentedHouse": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "homeOwners": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "oneCar": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "twoCars": [0, 1, 2, 3, 4, 5, 6, 7, 9],
    "noCar": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "nationalHealthService": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "privateHealthInsurance": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "incomeLessThan30k": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "income30To45k": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "income45To75k": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "income75To122k": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "incomeAbove123k": [0, 1, 2, 3, 4, 5, 6, 7, 9],
    "averageIncome": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "purchasingPowerClass": [1, 2, 3, 4, 5, 6, 7, 8],
    "contributionThirdPartyInsuranceFirms": [0, 1, 2, 3, 4, 5, 6],
    "contributionThirdPartyInsuranceAgriculture": [0, 1, 2, 3, 4],
    "contributionCarPolicies": [0, 4, 5, 6, 7, 8, 9],  # open-ended
    "contributionDeliveryVanPolicies": [0, 5, 6, 7],
    "contributionMotorcycleScooterPolicies": [0, 3, 4, 5, 6, 7],
    "contributionLorryPolicies": [0, 4, 6, 7, 9],  # open-ended
    "contributionTrailerPolicies": [0, 1, 2, 3, 4, 5],
    "contributionTractorPolicies": [0, 3, 4, 5, 6, 7],
    "contributionAgriculturalMachinesPolicies": [0, 1, 2, 3, 4, 6],
    "contributionMopedPolicies": [0, 2, 3, 4, 5, 6],
    "contributionLifeInsurances": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # open-ended
    "contributionPrivateAccidentInsurancePolicies": [0, 1, 2, 3, 4, 5, 6],
    "contributionFamilyAccidentsInsurancePolicies": [0, 2, 3],
    "contributionDisabilityInsurancePolicies": [0, 4, 5, 6, 7],
    "contributionFirePolicies": [0, 1, 2, 3, 4, 5, 6, 7, 8],
    "contributionSurfboardPolicies": [0, 1, 2, 3],
    "contributionBoatPolicies": [0, 1, 2, 3, 4, 5, 6],
    "contributionPropertyInsurancePolicies": [0, 1, 2, 3, 4, 5, 6],
    "contributionSocialSecurityInsurancePolicies": [0, 2, 3, 4, 5],
}


class Coil2000(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Does a customer of an insurer hold a caravan insurance policy?",
        use_case=(
            "An insurer selects customers for a direct-mail offer of caravan (mobile home) insurance, the question of"
            " the CoIL Challenge 2000: who would be interested in buying such a policy."
        ),
        row=(
            "One customer of an insurance company (CoIL Challenge 2000, data from a Dutch data-mining company; 9,822 "
            "customers)."
        ),
        predicted="Whether the customer holds a caravan insurance policy (6% do).",
        known=(
            "43 socio-demographic figures shared by all customers of the same postal area (customer type, household, "
            "religion, education, occupation, social class, income, cars, home ownership), and the customer's number "
            "of, and contributions to, 21 other insurance products."
        ),
        split="Random customers.",
        changes=(
            "We pool the challenge's training and evaluation customers instead of keeping its fixed held-out set."
        ),
        fit="approximate",
        fit_reason=(
            "Holding a policy now stands in for interest in buying one, and the other products are recorded at the "
            "same time as the label. The area figures are shared by neighbours, and 15% of the rows are duplicates."
        ),
    )

    # Dataset
    unique_name = "coil_2000"
    year = "2000"
    domain = "business & marketing"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5630S"
    license = "CC BY 4.0"
    download_description = """
        We download the data from the UCI repository and unzip it to a predefined folder.

        mkdir -p local-data-warehouse/coil_2000/ && wget -P local-data-warehouse/coil_2000/ https://archive.ics.uci.edu/static/public/125/insurance+company+benchmark+coil+2000.zip && unzip local-data-warehouse/coil_2000/insurance+company+benchmark+coil+2000.zip -d local-data-warehouse/coil_2000/
    """
    bibtex = """
        @techreport{van2000coil,
          title={CoIL challenge 2000: The insurance company case},
          author={Van Der Putten, Peter and van Someren, Maarten and others},
          year={2000},
          institution={Technical Report 2000--09, Leiden Institute of Advanced Computer Science}
        }
    """
    curation_comments = """
        - We created semantic meaningful names for the features.
        - We combined the original training and validation data into one new dataset.
        - We reversed the ordinal encoding of the original data where possible.
        - Anomaly: the data has 15% duplicates.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 59 columns are ordered categories in
          the order of the source's codebook (`ORDINAL_LEVELS`); 56 of them were shipped as numbers.
    """

    # Task
    target = "MobileHomePolicy"
    problem_type = "binary_classification"
    metric = Metric.source(
        "precision_at_k",
        original=("number of caravan policy owners among the 800 customers selected from the 4,000 test customers"),
        reference=(
            "https://kdd.ics.uci.edu/databases/tic/tic.task.html; van der Putten and van Someren 2000, "
            "CoIL Challenge 2000 tech report"
        ),
        definition=(
            "share of caravan policy owners among the 20% of the test fold with the highest scores (the "
            "challenge's 800 of 4,000, scaled to the fold)"
        ),
        params={"k_fraction": 0.2},
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        data = pd.read_csv(f"{raw_dir}/ticdata2000.txt", sep="\t", header=None)
        val_data = pd.concat(
            [
                pd.read_csv(f"{raw_dir}/ticeval2000.txt", sep="\t", header=None),
                pd.read_csv(f"{raw_dir}/tictgts2000.txt", sep="\t", header=None).rename(columns={0: 85}),
            ],
            axis=1,
        )
        return {"data": data, "val_data": val_data}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        data, val_data = raw["data"], raw["val_data"]
        df = pd.concat([data, val_data], axis=0, ignore_index=True)
        target_feature = "MobileHomePolicy"
        df.columns = [
            "customerSubtype",
            "numberOfHouses",
            "avgSizeHousehold",
            "avgAge",
            "customerMainType",
            "romanCatholic",
            "protestant",
            "otherReligion",
            "noReligion",
            "married",
            "livingTogether",
            "otherRelation",
            "singles",
            "householdWithoutChildren",
            "householdWithChildren",
            "highLevelEducation",
            "mediumLevelEducation",
            "lowerLevelEducation",
            "highStatus",
            "entrepreneur",
            "farmer",
            "middleManagement",
            "skilledLabourers",
            "unskilledLabourers",
            "socialClassA",
            "socialClassB1",
            "socialClassB2",
            "socialClassC",
            "socialClassD",
            "rentedHouse",
            "homeOwners",
            "oneCar",
            "twoCars",
            "noCar",
            "nationalHealthService",
            "privateHealthInsurance",
            "incomeLessThan30k",
            "income30To45k",
            "income45To75k",
            "income75To122k",
            "incomeAbove123k",
            "averageIncome",
            "purchasingPowerClass",
            "contributionPrivateThirdPartyInsurance",
            "contributionThirdPartyInsuranceFirms",
            "contributionThirdPartyInsuranceAgriculture",
            "contributionCarPolicies",
            "contributionDeliveryVanPolicies",
            "contributionMotorcycleScooterPolicies",
            "contributionLorryPolicies",
            "contributionTrailerPolicies",
            "contributionTractorPolicies",
            "contributionAgriculturalMachinesPolicies",
            "contributionMopedPolicies",
            "contributionLifeInsurances",
            "contributionPrivateAccidentInsurancePolicies",
            "contributionFamilyAccidentsInsurancePolicies",
            "contributionDisabilityInsurancePolicies",
            "contributionFirePolicies",
            "contributionSurfboardPolicies",
            "contributionBoatPolicies",
            "contributionBicyclePolicies",
            "contributionPropertyInsurancePolicies",
            "contributionSocialSecurityInsurancePolicies",
            "numberOfPrivateThirdPartyInsurance",
            "numberOfThirdPartyInsuranceFirms",
            "numberOfThirdPartyInsuranceAgriculture",
            "numberOfCarPolicies",
            "numberOfDeliveryVanPolicies",
            "numberOfMotorcycleScooterPolicies",
            "numberOfLorryPolicies",
            "numberOfTrailerPolicies",
            "numberOfTractorPolicies",
            "numberOfAgriculturalMachinesPolicies",
            "numberOfMopedPolicies",
            "numberOfLifeInsurances",
            "numberOfPrivateAccidentInsurancePolicies",
            "numberOfFamilyAccidentsInsurancePolicies",
            "numberOfDisabilityInsurancePolicies",
            "numberOfFirePolicies",
            "numberOfSurfboardPolicies",
            "numberOfBoatPolicies",
            "numberOfBicyclePolicies",
            "numberOfPropertyInsurancePolicies",
            "numberOfSocialSecurityInsurancePolicies",
            target_feature,
        ]
        # Reverse ordinal encoding where possible
        df["customerSubtype"] = df["customerSubtype"].map(
            {
                1: "High Income, expensive child",
                2: "Very Important Provincials",
                3: "High status seniors",
                4: "Affluent senior apartments",
                5: "Mixed seniors",
                6: "Career and childcare",
                7: "Dinki's (double income no kids)",
                8: "Middle class families",
                9: "Modern, complete families",
                10: "Stable family",
                11: "Family starters",
                12: "Affluent young families",
                13: "Young all american family",
                14: "Junior cosmopolitan",
                15: "Senior cosmopolitans",
                16: "Students in apartments",
                17: "Fresh masters in the city",
                18: "Single youth",
                19: "Suburban youth",
                20: "Etnically diverse",
                21: "Young urban have-nots",
                22: "Mixed apartment dwellers",
                23: "Young and rising",
                24: "Young, low educated",
                25: "Young seniors in the city",
                26: "Own home elderly",
                27: "Seniors in apartments",
                28: "Residential elderly",
                29: "Porchless seniors: no front yard",
                30: "Religious elderly singles",
                31: "Low income catholics",
                32: "Mixed seniors",
                33: "Lower class large families",
                34: "Large family, employed child",
                35: "Village families",
                36: "Couples with teens 'Married with children'",
                37: "Mixed small town dwellers",
                38: "Traditional families",
                39: "Large religous families",
                40: "Large family farms",
                41: "Mixed rurals",
            }
        )
        df["avgAge"] = df["avgAge"].map(
            {
                1: "20-30 years",
                2: "30-40 years",
                3: "40-50 years",
                4: "50-60 years",
                5: "60-70 years",
                6: "70-80 years",
            }
        )
        df["customerMainType"] = df["customerMainType"].map(
            {
                1: "Successful hedonists",
                2: "Driven Growers",
                3: "Average Family",
                4: "Career Loners",
                5: "Living well",
                6: "Cruising Seniors",
                7: "Retired and Religeous",
                8: "Family with grown ups",
                9: "Conservative families",
                10: "Farmers",
            }
        )
        df["romanCatholic"] = df["romanCatholic"].map(
            {
                0: "0%",
                1: "1 - 10%",
                2: "11 - 23%",
                3: "24 - 36%",
                4: "37 - 49%",
                5: "50 - 62%",
                6: "63 - 75%",
                7: "76 - 88%",
                8: "89 - 99%",
                9: "100%",
            }
        )
        df["contributionPrivateThirdPartyInsurance"] = df["contributionPrivateThirdPartyInsurance"].map(
            {
                0: "f 0",
                1: "f 1 - 49",
                2: "f 50 - 99",
                3: "f 100 - 199",
                4: "f 200 - 499",
                5: "f 500 - 999",
                6: "f 1000 - 4999",
                7: "f 5000 - 9999",
                8: "f 10.000 - 19.999",
                9: "f 20.000 - ?",
            }
        )
        df[target_feature] = df[target_feature].map({0: "No", 1: "Yes"})
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[
                "customerSubtype",
                "customerMainType",
                "romanCatholic",
                "avgAge",
                "contributionPrivateThirdPartyInsurance",
            ],
        )

"""Curated dataset definition for `ames_housing` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
    object_columns,
    set_missing,
)

# The data end in July 2010 with 8 sales (101-122 in July 2006-2009): the month was cut by the extract.
FIRST_INCOMPLETE_MONTH = 201007

# De Cock (2011, p. 4): the houses over 4,000 sq ft of living area are the five unusual sales of the file.
OUTLIER_LIVING_AREA = 4000

# `Sale Condition` codes whose price is not this house's market value (DataDocumentation.txt): a sale between family
# members, an allocation of two linked properties with separate deeds (a condo and its garage unit) and a purchase of
# adjoining land.
NON_MARKET_SALES = ("Family", "Alloca", "AdjLand")

# The documentation's labels of the dwelling-type codes (DataDocumentation.txt, "MS SubClass").
MS_SUBCLASS_LABELS = {
    "020": "1-STORY 1946 & NEWER ALL STYLES",
    "030": "1-STORY 1945 & OLDER",
    "040": "1-STORY W/FINISHED ATTIC ALL AGES",
    "045": "1-1/2 STORY - UNFINISHED ALL AGES",
    "050": "1-1/2 STORY FINISHED ALL AGES",
    "060": "2-STORY 1946 & NEWER",
    "070": "2-STORY 1945 & OLDER",
    "075": "2-1/2 STORY ALL AGES",
    "080": "SPLIT OR MULTI-LEVEL",
    "085": "SPLIT FOYER",
    "090": "DUPLEX - ALL STYLES AND AGES",
    "120": "1-STORY PUD (Planned Unit Development) - 1946 & NEWER",
    "150": "1-1/2 STORY PUD - ALL AGES",
    "160": "2-STORY PUD - 1946 & NEWER",
    "180": "PUD - MULTILEVEL - INCL SPLIT LEV/FOYER",
    "190": "2 FAMILY CONVERSION - ALL STYLES AND AGES",
}

# `Exterior 2nd` spellings that differ from the documentation and from `Exterior 1st`.
EXTERIOR_2ND_SPELLINGS = {"Brk Cmn": "BrkComm", "CmentBd": "CemntBd", "Wd Shng": "WdShing"}

# The documentation's labels of the text codes of the other 43 categorical columns (DataDocumentation.txt), for the
# codes the file uses. The file spells five codes unlike the documentation: `A (agr)`, `C (all)`, `I (all)` (MS Zoning: A,
# C, I), `NAmes` (Neighborhood: Names), `2fmCon`, `Duplex`, `Twnhs` (Bldg Type: 2FmCon, Duplx, TwnhsI). Typos of the
# documentation are corrected ("Gabrel", "postive", "Contrete", "Mimimum", "Unfinshed"), and its two spellings of
# the grade TA are written "Typical/Average".
CODE_LABELS: dict[str, dict[str, str]] = {
    "MS Zoning": {
        "A (agr)": "Agriculture",
        "C (all)": "Commercial",
        "FV": "Floating Village Residential",
        "I (all)": "Industrial",
        "RH": "Residential High Density",
        "RL": "Residential Low Density",
        "RM": "Residential Medium Density",
    },
    "Street": {
        "Grvl": "Gravel",
        "Pave": "Paved",
    },
    "Alley": {
        "Grvl": "Gravel",
        "Pave": "Paved",
    },
    "Lot Shape": {
        "IR1": "Slightly irregular",
        "IR2": "Moderately Irregular",
        "IR3": "Irregular",
        "Reg": "Regular",
    },
    "Land Contour": {
        "Bnk": "Banked - Quick and significant rise from street grade to building",
        "HLS": "Hillside - Significant slope from side to side",
        "Low": "Depression",
        "Lvl": "Near Flat/Level",
    },
    "Utilities": {
        "AllPub": "All public Utilities (E,G,W,& S)",
        "NoSeWa": "Electricity and Gas Only",
        "NoSewr": "Electricity, Gas, and Water (Septic Tank)",
    },
    "Lot Config": {
        "Corner": "Corner lot",
        "CulDSac": "Cul-de-sac",
        "FR2": "Frontage on 2 sides of property",
        "FR3": "Frontage on 3 sides of property",
        "Inside": "Inside lot",
    },
    "Land Slope": {
        "Gtl": "Gentle slope",
        "Mod": "Moderate Slope",
        "Sev": "Severe Slope",
    },
    "Neighborhood": {
        "Blmngtn": "Bloomington Heights",
        "Blueste": "Bluestem",
        "BrDale": "Briardale",
        "BrkSide": "Brookside",
        "ClearCr": "Clear Creek",
        "CollgCr": "College Creek",
        "Crawfor": "Crawford",
        "Edwards": "Edwards",
        "Gilbert": "Gilbert",
        "Greens": "Greens",
        "GrnHill": "Green Hills",
        "IDOTRR": "Iowa DOT and Rail Road",
        "Landmrk": "Landmark",
        "MeadowV": "Meadow Village",
        "Mitchel": "Mitchell",
        "NAmes": "North Ames",
        "NPkVill": "Northpark Villa",
        "NWAmes": "Northwest Ames",
        "NoRidge": "Northridge",
        "NridgHt": "Northridge Heights",
        "OldTown": "Old Town",
        "SWISU": "South & West of Iowa State University",
        "Sawyer": "Sawyer",
        "SawyerW": "Sawyer West",
        "Somerst": "Somerset",
        "StoneBr": "Stone Brook",
        "Timber": "Timberland",
        "Veenker": "Veenker",
    },
    "Condition 1": {
        "Artery": "Adjacent to arterial street",
        "Feedr": "Adjacent to feeder street",
        "Norm": "Normal",
        "PosA": "Adjacent to positive off-site feature",
        "PosN": "Near positive off-site feature--park, greenbelt, etc.",
        "RRAe": "Adjacent to East-West Railroad",
        "RRAn": "Adjacent to North-South Railroad",
        "RRNe": "Within 200' of East-West Railroad",
        "RRNn": "Within 200' of North-South Railroad",
    },
    "Condition 2": {
        "Artery": "Adjacent to arterial street",
        "Feedr": "Adjacent to feeder street",
        "Norm": "Normal",
        "PosA": "Adjacent to positive off-site feature",
        "PosN": "Near positive off-site feature--park, greenbelt, etc.",
        "RRAe": "Adjacent to East-West Railroad",
        "RRAn": "Adjacent to North-South Railroad",
        "RRNn": "Within 200' of North-South Railroad",
    },
    "Bldg Type": {
        "1Fam": "Single-family Detached",
        "2fmCon": "Two-family Conversion; originally built as one-family dwelling",
        "Duplex": "Duplex",
        "Twnhs": "Townhouse Inside Unit",
        "TwnhsE": "Townhouse End Unit",
    },
    "House Style": {
        "1.5Fin": "One and one-half story: 2nd level finished",
        "1.5Unf": "One and one-half story: 2nd level unfinished",
        "1Story": "One story",
        "2.5Fin": "Two and one-half story: 2nd level finished",
        "2.5Unf": "Two and one-half story: 2nd level unfinished",
        "2Story": "Two story",
        "SFoyer": "Split Foyer",
        "SLvl": "Split Level",
    },
    "Roof Style": {
        "Flat": "Flat",
        "Gable": "Gable",
        "Gambrel": "Gambrel (Barn)",
        "Hip": "Hip",
        "Mansard": "Mansard",
        "Shed": "Shed",
    },
    "Roof Matl": {
        "CompShg": "Standard (Composite) Shingle",
        "Membran": "Membrane",
        "Metal": "Metal",
        "Roll": "Roll",
        "Tar&Grv": "Gravel & Tar",
        "WdShake": "Wood Shakes",
        "WdShngl": "Wood Shingles",
    },
    "Exterior 1st": {
        "AsbShng": "Asbestos Shingles",
        "AsphShn": "Asphalt Shingles",
        "BrkComm": "Brick Common",
        "BrkFace": "Brick Face",
        "CBlock": "Cinder Block",
        "CemntBd": "Cement Board",
        "HdBoard": "Hard Board",
        "ImStucc": "Imitation Stucco",
        "MetalSd": "Metal Siding",
        "Plywood": "Plywood",
        "PreCast": "PreCast",
        "Stone": "Stone",
        "Stucco": "Stucco",
        "VinylSd": "Vinyl Siding",
        "Wd Sdng": "Wood Siding",
        "WdShing": "Wood Shingles",
    },
    "Exterior 2nd": {
        "AsbShng": "Asbestos Shingles",
        "AsphShn": "Asphalt Shingles",
        "BrkComm": "Brick Common",
        "BrkFace": "Brick Face",
        "CBlock": "Cinder Block",
        "CemntBd": "Cement Board",
        "HdBoard": "Hard Board",
        "ImStucc": "Imitation Stucco",
        "MetalSd": "Metal Siding",
        "Other": "Other",
        "Plywood": "Plywood",
        "PreCast": "PreCast",
        "Stone": "Stone",
        "Stucco": "Stucco",
        "VinylSd": "Vinyl Siding",
        "Wd Sdng": "Wood Siding",
        "WdShing": "Wood Shingles",
    },
    "Mas Vnr Type": {
        "BrkCmn": "Brick Common",
        "BrkFace": "Brick Face",
        "CBlock": "Cinder Block",
        "None": "None",
        "Stone": "Stone",
    },
    "Exter Qual": {
        "Ex": "Excellent",
        "Fa": "Fair",
        "Gd": "Good",
        "TA": "Typical/Average",
    },
    "Exter Cond": {
        "Ex": "Excellent",
        "Fa": "Fair",
        "Gd": "Good",
        "Po": "Poor",
        "TA": "Typical/Average",
    },
    "Foundation": {
        "BrkTil": "Brick & Tile",
        "CBlock": "Cinder Block",
        "PConc": "Poured Concrete",
        "Slab": "Slab",
        "Stone": "Stone",
        "Wood": "Wood",
    },
    "Bsmt Qual": {
        "Ex": "Excellent (100+ inches)",
        "Fa": "Fair (70-79 inches)",
        "Gd": "Good (90-99 inches)",
        "Po": "Poor (<70 inches)",
        "TA": "Typical (80-89 inches)",
    },
    "Bsmt Cond": {
        "Ex": "Excellent",
        "Fa": "Fair - dampness or some cracking or settling",
        "Gd": "Good",
        "Po": "Poor - Severe cracking, settling, or wetness",
        "TA": "Typical - slight dampness allowed",
    },
    "Bsmt Exposure": {
        "Av": "Average Exposure (split levels or foyers typically score average or above)",
        "Gd": "Good Exposure",
        "Mn": "Minimum Exposure",
        "No": "No Exposure",
    },
    "BsmtFin Type 1": {
        "ALQ": "Average Living Quarters",
        "BLQ": "Below Average Living Quarters",
        "GLQ": "Good Living Quarters",
        "LwQ": "Low Quality",
        "Rec": "Average Rec Room",
        "Unf": "Unfinished",
    },
    "BsmtFin Type 2": {
        "ALQ": "Average Living Quarters",
        "BLQ": "Below Average Living Quarters",
        "GLQ": "Good Living Quarters",
        "LwQ": "Low Quality",
        "Rec": "Average Rec Room",
        "Unf": "Unfinished",
    },
    "Heating": {
        "Floor": "Floor Furnace",
        "GasA": "Gas forced warm air furnace",
        "GasW": "Gas hot water or steam heat",
        "Grav": "Gravity furnace",
        "OthW": "Hot water or steam heat other than gas",
        "Wall": "Wall furnace",
    },
    "Heating QC": {
        "Ex": "Excellent",
        "Fa": "Fair",
        "Gd": "Good",
        "Po": "Poor",
        "TA": "Typical/Average",
    },
    "Central Air": {
        "N": "No",
        "Y": "Yes",
    },
    "Electrical": {
        "FuseA": "Fuse Box over 60 AMP and all Romex wiring (Average)",
        "FuseF": "60 AMP Fuse Box and mostly Romex wiring (Fair)",
        "FuseP": "60 AMP Fuse Box and mostly knob & tube wiring (poor)",
        "Mix": "Mixed",
        "SBrkr": "Standard Circuit Breakers & Romex",
    },
    "Kitchen Qual": {
        "Ex": "Excellent",
        "Fa": "Fair",
        "Gd": "Good",
        "Po": "Poor",
        "TA": "Typical/Average",
    },
    "Functional": {
        "Maj1": "Major Deductions 1",
        "Maj2": "Major Deductions 2",
        "Min1": "Minor Deductions 1",
        "Min2": "Minor Deductions 2",
        "Mod": "Moderate Deductions",
        "Sal": "Salvage only",
        "Sev": "Severely Damaged",
        "Typ": "Typical Functionality",
    },
    "Fireplace Qu": {
        "Ex": "Excellent - Exceptional Masonry Fireplace",
        "Fa": "Fair - Prefabricated Fireplace in basement",
        "Gd": "Good - Masonry Fireplace in main level",
        "Po": "Poor - Ben Franklin Stove",
        "TA": "Average - Prefabricated Fireplace in main living area or Masonry Fireplace in basement",
    },
    "Garage Type": {
        "2Types": "More than one type of garage",
        "Attchd": "Attached to home",
        "Basment": "Basement Garage",
        "BuiltIn": "Built-In (Garage part of house - typically has room above garage)",
        "CarPort": "Car Port",
        "Detchd": "Detached from home",
    },
    "Garage Finish": {
        "Fin": "Finished",
        "RFn": "Rough Finished",
        "Unf": "Unfinished",
    },
    "Garage Qual": {
        "Ex": "Excellent",
        "Fa": "Fair",
        "Gd": "Good",
        "Po": "Poor",
        "TA": "Typical/Average",
    },
    "Garage Cond": {
        "Ex": "Excellent",
        "Fa": "Fair",
        "Gd": "Good",
        "Po": "Poor",
        "TA": "Typical/Average",
    },
    "Paved Drive": {
        "N": "Dirt/Gravel",
        "P": "Partial Pavement",
        "Y": "Paved",
    },
    "Pool QC": {
        "Ex": "Excellent",
        "Fa": "Fair",
        "Gd": "Good",
        "TA": "Typical/Average",
    },
    "Fence": {
        "GdPrv": "Good Privacy",
        "GdWo": "Good Wood",
        "MnPrv": "Minimum Privacy",
        "MnWw": "Minimum Wood/Wire",
    },
    "Misc Feature": {
        "Gar2": "2nd Garage (if not described in garage section)",
        "Othr": "Other",
        "Shed": "Shed (over 100 SF)",
        "TenC": "Tennis Court",
    },
    "Sale Type": {
        "COD": "Court Officer Deed/Estate",
        "CWD": "Warranty Deed - Cash",
        "Con": "Contract 15% Down payment regular terms",
        "ConLD": "Contract Low Down",
        "ConLI": "Contract Low Interest",
        "ConLw": "Contract Low Down payment and low interest",
        "New": "Home just constructed and sold",
        "Oth": "Other",
        "VWD": "Warranty Deed - VA Loan",
        "WD": "Warranty Deed - Conventional",
    },
    "Sale Condition": {
        "Abnorml": "Abnormal Sale - trade, foreclosure, short sale",
        "Normal": "Normal Sale",
        "Partial": "Home was not completed when last assessed (associated with New Homes)",
    },
}

# Columns whose "NA" is a documented level ("NA No Basement", ...), the label we write for it, and the column that
# says whether the item exists (None: the column alone says it).
ABSENT_LEVELS = {
    "Alley": ("No alley access", None),
    "Bsmt Qual": ("No basement", "Bsmt Qual"),
    "Bsmt Cond": ("No basement", "Bsmt Qual"),
    "Bsmt Exposure": ("No basement", "Bsmt Qual"),
    "BsmtFin Type 1": ("No basement", "Bsmt Qual"),
    "BsmtFin Type 2": ("No basement", "Bsmt Qual"),
    "Fireplace Qu": ("No fireplace", None),
    "Garage Type": ("No garage", "Garage Type"),
    "Garage Finish": ("No garage", "Garage Type"),
    "Garage Qual": ("No garage", "Garage Type"),
    "Garage Cond": ("No garage", "Garage Type"),
    "Pool QC": ("No pool", None),
    "Fence": ("No fence", None),
    "Misc Feature": ("None", None),
}


# The ordinal scales, lowest level first, from the source's codebook (curation notes; the README lists
# them). An open-ended level holds everything beyond it.
ORDINAL_LEVELS = {
    "Lot Shape": ["Regular", "Slightly irregular", "Moderately Irregular", "Irregular"],
    "Utilities": [
        "Electricity and Gas Only",
        "Electricity, Gas, and Water (Septic Tank)",
        "All public Utilities (E,G,W,& S)",
    ],
    "Land Slope": ["Gentle slope", "Moderate Slope", "Severe Slope"],
    "Exter Qual": ["Fair", "Typical/Average", "Good", "Excellent"],
    "Exter Cond": ["Poor", "Fair", "Typical/Average", "Good", "Excellent"],
    "Heating QC": ["Poor", "Fair", "Typical/Average", "Good", "Excellent"],
    "Kitchen Qual": ["Poor", "Fair", "Typical/Average", "Good", "Excellent"],
    "Functional": [
        "Salvage only",
        "Severely Damaged",
        "Major Deductions 2",
        "Major Deductions 1",
        "Moderate Deductions",
        "Minor Deductions 2",
        "Minor Deductions 1",
        "Typical Functionality",
    ],
    "Garage Qual": ["Poor", "Fair", "Typical/Average", "Good", "Excellent"],
    "Garage Cond": ["Poor", "Fair", "Typical/Average", "Good", "Excellent"],
    "Paved Drive": ["Dirt/Gravel", "Partial Pavement", "Paved"],
    "Pool QC": ["Fair", "Typical/Average", "Good", "Excellent"],
    "Overall Qual": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Overall Cond": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "Bsmt Qual": [
        "No basement",
        "Poor (<70 inches)",
        "Fair (70-79 inches)",
        "Typical (80-89 inches)",
        "Good (90-99 inches)",
        "Excellent (100+ inches)",
    ],  # open-ended
    "Bsmt Cond": [
        "No basement",
        "Poor - Severe cracking, settling, or wetness",
        "Fair - dampness or some cracking or settling",
        "Typical - slight dampness allowed",
        "Good",
        "Excellent",
    ],
    "Bsmt Exposure": [
        "No basement",
        "No Exposure",
        "Minimum Exposure",
        "Average Exposure (split levels or foyers typically score average or above)",
        "Good Exposure",
    ],
    "BsmtFin Type 1": [
        "No basement",
        "Unfinished",
        "Low Quality",
        "Average Rec Room",
        "Below Average Living Quarters",
        "Average Living Quarters",
        "Good Living Quarters",
    ],
    "BsmtFin Type 2": [
        "No basement",
        "Unfinished",
        "Low Quality",
        "Average Rec Room",
        "Below Average Living Quarters",
        "Average Living Quarters",
        "Good Living Quarters",
    ],
    "Electrical": [
        "60 AMP Fuse Box and mostly knob & tube wiring (poor)",
        "60 AMP Fuse Box and mostly Romex wiring (Fair)",
        "Fuse Box over 60 AMP and all Romex wiring (Average)",
        "Standard Circuit Breakers & Romex",
    ],
    "Fireplace Qu": [
        "Poor - Ben Franklin Stove",
        "Fair - Prefabricated Fireplace in basement",
        "Average - Prefabricated Fireplace in main living area or Masonry Fireplace in basement",
        "Good - Masonry Fireplace in main level",
        "Excellent - Exceptional Masonry Fireplace",
    ],
    "Garage Finish": ["No garage", "Unfinished", "Rough Finished", "Finished"],
}


class AmesHousing(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What price will a house in Ames, Iowa sell for?",
        use_case=(
            "For example, the city assessor of Ames values residential properties from recent sales: a model "
            "refit every two months, as new sales arrive, estimates what each house would sell for from its record."
        ),
        row=(
            "One sale of residential property in Ames, Iowa, January 2006 to June 2010, from the city assessor's "
            "office, at market value (2,837 sales)."
        ),
        predicted="The sale price in US dollars, on a log scale.",
        known=(
            "The assessor's record of the property (neighbourhood, lot, building type, areas, rooms, quality and "
            "condition grades, year built and remodelled, basement, garage) and the sale's month, type and condition."
        ),
        split=(
            "Each test window is two calendar months, 13 windows from May-June 2008 to May-June 2010; training is "
            "every earlier sale."
        ),
        changes=(
            "We use De Cock's full file instead of the Kaggle competition's random half, split by sale month instead "
            "of at random, drop the sales whose price is not this house's market value (sales between family "
            "members, allocations, adjoining land, and his three partial sales of very large new houses), and write "
            "out the text codes."
        ),
        fit="direct",
        fit_reason=(
            "The assessor's file of about 2010 describes the house at the sale: no remodel year postdates its sale "
            "except one new house (2008, sold 2007), set to missing. Whether a grade was revised after the sale "
            "cannot be checked. The windows follow time. De Cock kept only the latest sale of a home sold twice, so "
            "the older months miss about 100 sales."
        ),
    )

    # Dataset
    unique_name = "ames_housing"
    year = "2011"
    domain = "business & marketing"
    source = "Other"
    source_url = "https://doi.org/10.1080/10691898.2011.11889627"
    license = (
        "JSE data policy: free to use in teaching; use in papers, books or other published material needs the "
        "consent of the contributing author (https://jse.amstat.org/jse_users.htm)"
    )
    data_tags = ("Spatial",)
    download_description = """
        We download the text version of the data file published with De Cock (2011): AmesHousing.txt, tab-separated,
        2,930 rows and 82 columns (sha256 6cfe6cb525ba437de428653a1040e2aed7d696640bf75203786a6d7a0e67cfcc). Its
        documentation is https://jse.amstat.org/v19n3/decock/DataDocumentation.txt.

        mkdir -p local-data-warehouse/ames_housing
        wget -P local-data-warehouse/ames_housing https://jse.amstat.org/v19n3/decock/AmesHousing.txt

        The Kaggle competition house-prices-advanced-regression-techniques and OpenML 42165 (its
        train.csv), hold 1,460 of these sales with prices; see curation_comments.
    """
    bibtex = """
        @article{decock2011ames,
          author = {De Cock, Dean},
          title = {Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project},
          journal = {Journal of Statistics Education},
          volume = {19},
          number = {3},
          year = {2011},
          doi = {10.1080/10691898.2011.11889627}
        }
    """
    curation_comments = """
        We start with AmesHousing.txt, the data file of De Cock (2011): 2,930 sales of residential property in Ames, Iowa, January 2006 to July 2010, from the Ames City Assessor's Office.

        - Prediction point: a house sells, and a valuation model refit every two months on all earlier sales predicts its price from the assessor's record of the property and the sale's type and condition.
        - Source: we use this file rather than the Kaggle competition (OpenML 42165; its record house_prices_nominal is now a `Duplicate` of this one, CC 2026-10-26), whose 1,460 labelled rows it holds: twice the labelled rows, values as published.
        - Anomaly: De Cock kept only the latest sale of a home sold more than once (p. 4), so the older months miss about 100 sales.
        - We drop the 8 sales of July 2010: the extract cut the month (decision table).
        - We drop `Order` (the file's row number) and `PID` (the parcel number). Its block prefix, a location, adds nothing as a feature: LightGBM's RMSE changes by -0.0005 (SE 0.0005) with the block and -0.0001 (SE 0.0007) with the section (13 windows, 3 seeds).
        - `Yr Sold` and `Mo Sold` become `Month Sold`, the month of the sale and the time column (the file gives no day).
        - In 14 columns "NA" is a documented level for an absent item ("NA No Basement", ...). We write it out ("No basement", ...); empty fields are the missing values. Where the item exists (two houses with a detached garage), "NA" is missing.
        - `MS SubClass` codes ("020", ...) become the documentation's labels. We strip the trailing blank of `Sale Type` "WD ". `Exterior 2nd` spells three materials unlike the documentation and `Exterior 1st` (`Brk Cmn`, `CmentBd`, `Wd Shng`, 225 rows); we use the documentation's codes `BrkComm`, `CemntBd`, `WdShing`.
        - `Garage Yr Blt` = 2207 (a house built in 2006 and sold new in 2007) is a typo; we set it to missing.
        - The 23 nominal and 21 text-coded ordinal variables are categorical; the rest is numeric. The text codes of the 43 other than `MS SubClass` become the documentation's labels too (`TA` "Typical/Average", `GLQ` "Good Living Quarters", `Gtl` "Gentle slope"; CLEAN-12, CC 2026-10-26), with five codes the file spells unlike the documentation matched by hand and the documentation's typos corrected (`CODE_LABELS`). The 21 graded columns stay unordered categories (CLEAN-14). Total and part areas are kept as published.
        - The target is the natural log of `SalePrice`, renamed to `log_SalePrice`, the scale the competition scored on.
        - CLEAN-11 as amended (Lennart, 2026-10-21: a row whose target the source names as not the task's quantity may leave, with the source's words): we drop De Cock's three "true outliers" (p. 4), partial sales of new houses over 4,000 sq ft that "likely don't represent actual market values" ($28-$40 per sq ft against a median of $150 for partial sales), and keep his two other houses over 4,000 sq ft (decision table). The three would only train, yet without them the task probe's linear model goes from RMSE 0.125 to 0.119 (13 windows). It was the third drop of target-outlier rows, after mercedes_benz_greener_manufacturing and qsar_tid_11, and prompted that amendment. With the non-market sales below, the drop rests on USE-5 as well.
        - USE-5 (CC 2026-10-26): we drop the 82 sales whose price is not this house's market value by the file's `Sale Condition`: 46 between family members (`Family`), 24 allocations of two linked properties with separate deeds, such as a condo and its garage unit (`Alloca`), and 12 purchases of adjoining land (`AdjLand`) (DataDocumentation.txt). The assessor values a house at its market value, and assessors' sales-ratio studies leave such sales out (IAAO standards). house_sales drops its related-party sales and its sales of several parcels on the same reasons (CC 2026-10-22 and 2026-10-26). 34 of them were test rows, where they carried large errors (RMSE 0.291 for Family and 0.228 for Alloca against 0.095 for normal sales, 500-tree LightGBM, 3 seeds, 13 windows). Foreclosures and short sales (`Abnorml`, 190) are sales on the market and stay (decision table).
        - The records describe the house at the sale: no house built two or more years before its sale has a remodel year after it. One new house (built 2007, sold in June 2007) shows a remodel in 2008, a value from after the sale, and one house shows a remodel in 2001 before it was built in 2002, impossible by the documentation; both remodel years become missing. Whether the grades were revised after a sale cannot be checked from the file.
        - Anomaly: `Year Remod/Add` starts at 1950: 337 of the 629 houses built before 1950 show 1950, where the documentation gives the construction year for no remodel. Kept as recorded.
        - No duplicate rows. Two pairs of neighbouring parcels share every feature and sold in one month at different prices; kept.
        - Not trivial (TP-4; the record's `Trivial` marker was removed, CC 2026-10-26): `Overall Qual` alone reaches R² 0.682 in the task probe (13 windows) and De Cock's two-variable model 0.766, against 0.911 for the probe's linear model and 0.900 for its LightGBM.
        - Ordinal scales (2026-10-30, the curator's marks of 2026-10-31, CLEAN-14): 22 columns are ordered categories in
          the order of the source's codebook (`ORDINAL_LEVELS`); 2 of them were shipped as numbers; 8 hold a state
          outside the scale, placed by the curator's rule (missing when the column has no other missing value, else the
          lowest level; a state that is simply not on the scale, such as Other, is missing); codes that mean unknown are
          missing (CLEAN-10).
    """

    # Task
    target = "log_SalePrice"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="RMSE between the logarithm of the predicted and the observed sale price",
        reference="https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/overview/evaluation",
        definition="RMSE on log_SalePrice (= RMSE of log predicted vs log observed SalePrice, RMSLE-like on the raw price).",
    )

    # Splits: two-month calendar windows down to half of the rows for training (13 windows of 46-191 sales).
    temporal = Temporal(on="Month Sold", splits=TemporalSplits(window=2, unit="months", min_train_fraction=0.5))
    splits_comment = """
        A price model refit every two months predicts the sales of the next two months: 13 test windows of two calendar months, from May-June 2010 back to May-June 2008, newest first, each trained on all earlier sales. The windows stop where the training side would fall below half of the rows (a March-April 2008 window would train on 47% of them). An IID task of this size would get 10 x 3 splits; monthly windows would hold 19-109 sales, so we use two months (46-187 sales per window). Each window trains on every earlier month without a gap. Sales reach the file with a delay: the extract's last full month, June 2010, holds 82 sales against 97-112 in the Junes of 2006-2009, about 78% of a usual June. Its 73 normal sales show no price selection (mean residual -0.001 of a 500-tree LightGBM), and June 2010 is only ever tested, never trained on. A one-month gap changes LightGBM's RMSE by +0.0004 to +0.0010 and a two-month gap by +0.0016 to +0.0026 (500-tree LightGBM, 3 seeds, 13 windows), within noise. Exception to SPLIT-10 (2026-10-26, Lennart): no gap. The only visible recording shortfall is the extract's last month, and its normal sales show no price selection; sales are dated by month, so the smallest possible gap is a whole month, longer than the delay. The windows train on every recorded sale before them, as a valuation model refit each month on all earlier sales would (P4).
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # "NA" is a documented level in 14 columns and empty fields are missing, so only "" is read as missing. The
        # parcel number and the dwelling-type code are codes: read as text to keep the leading zeros.
        return pd.read_csv(
            raw_dir / "AmesHousing.txt",
            sep="\t",
            keep_default_na=False,
            na_values=[""],
            dtype={"PID": str, "MS SubClass": str},
        )

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # The extract cut July 2010 (8 sales).
        month = df["Yr Sold"] * 100 + df["Mo Sold"]
        df = df[month < FIRST_INCOMPLETE_MONTH]
        # De Cock's "true outliers" (p. 4): partial sales of new houses over 4,000 sq ft at $28-$40 per sq ft. The two
        # other houses over 4,000 sq ft are market sales and stay.
        outliers = (df["Gr Liv Area"] > OUTLIER_LIVING_AREA) & (df["Sale Condition"] == "Partial")
        assert outliers.sum() == 3, "expected De Cock's three partial-sale outliers"
        df = df[~outliers]
        # Sales whose price is not this house's market value: family, allocations and adjoining land (82 sales).
        non_market = df["Sale Condition"].isin(NON_MARKET_SALES)
        assert non_market.sum() == 82, "expected 82 family, allocation and adjoining-land sales"
        df = df[~non_market]
        # The time column: the month of the sale (the file gives no day).
        df["Month Sold"] = (df["Yr Sold"] * 100 + df["Mo Sold"]).astype(str)
        # Absent items: write out the documented "NA" level; where the item exists, "NA" is a missing value. The
        # anchors are read before any column is rewritten.
        anchors = {col: df[col] == "NA" for col in ("Bsmt Qual", "Garage Type")}
        for col, (label, anchor) in ABSENT_LEVELS.items():
            is_na = df[col] == "NA"
            absent = anchors[anchor] if anchor is not None else is_na
            df[col] = df[col].mask(is_na & absent, label).mask(is_na & ~absent)
        assert not any((df[c] == "NA").any() for c in object_columns(df)), "an undocumented NA level is left"
        # Dwelling-type codes to the documentation's labels.
        assert df["MS SubClass"].isin(list(MS_SUBCLASS_LABELS)).all(), "an undocumented MS SubClass code"
        df["MS SubClass"] = df["MS SubClass"].map(MS_SUBCLASS_LABELS)
        df["Sale Type"] = df["Sale Type"].str.strip()
        # A typo: a garage built in 2207 (house built 2006, sold new in 2007).
        typo = df["Garage Yr Blt"] > df["Yr Sold"].max()
        assert typo.sum() == 1, "expected one garage year after the data end"
        df.loc[typo, "Garage Yr Blt"] = np.nan
        # Remodel years that cannot hold at the sale: one after the sale (a new house sold in 2007, remodelled 2008)
        # and one before the construction (remodelled 2001, built 2002).
        bad_remodel = (df["Year Remod/Add"] > df["Yr Sold"]) | (df["Year Remod/Add"] < df["Year Built"])
        assert bad_remodel.sum() == 2, "expected two impossible remodel years"
        df["Year Remod/Add"] = df["Year Remod/Add"].mask(bad_remodel)
        # `Exterior 2nd` spells three materials unlike the documentation and `Exterior 1st`.
        df["Exterior 2nd"] = df["Exterior 2nd"].replace(EXTERIOR_2ND_SPELLINGS)
        # The text codes of the other 43 categorical columns to the documentation's labels; the absent-item labels stay.
        absent_labels = {label for label, _ in ABSENT_LEVELS.values()}
        for col, labels in CODE_LABELS.items():
            assert df[col].dropna().isin([*labels, *absent_labels]).all(), f"an undocumented code in {col}"
            df[col] = df[col].replace(labels)
        # Target: the log of the sale price, renamed in place.
        df = df.rename(columns={"SalePrice": "log_SalePrice"})
        df["log_SalePrice"] = np.log(df["log_SalePrice"])
        # codes outside a scale that mean unknown, and states outside it placed as missing (CLEAN-10,
        # CLEAN-14): don't know, refused, not asked, other
        df = set_missing(
            df,
            {
                "Garage Qual": ["No garage"],
                "Garage Cond": ["No garage"],
                "Pool QC": ["No pool"],
                "Electrical": ["Mixed"],
                "Fireplace Qu": ["No fireplace"],
            },
        )
        return drop_columns(df, ["Order", "PID", "Yr Sold", "Mo Sold"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The non-numeric columns are the 23 nominal and 21 text-coded ordinal variables of the documentation (text
        # in the cleaned frame, categories in the final one).
        return FeatureTypes(
            ordinal=ORDINAL_LEVELS,
            categorical=[c for c in df.columns if c != "Month Sold" and not pd.api.types.is_numeric_dtype(df[c])],
            datetime={"Month Sold": "%Y%m"},
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        july = raw[raw["Mo Sold"] == 7].groupby("Yr Sold").size().rename("sales in July")

        windows = []
        for months in (1, 2, 3):
            splits = TemporalSplits(window=months, unit="months", min_train_fraction=0.5).splits(df, "Month Sold")
            sizes = pd.Series([len(test) for folds in splits.values() for _, test in folds.values()])
            windows.append(
                {
                    "window (months)": months,
                    "windows": len(sizes),
                    "fewest test rows": int(sizes.min()),
                    "median test rows": int(sizes.median()),
                    "most test rows": int(sizes.max()),
                }
            )

        large = raw.loc[
            raw["Gr Liv Area"] > OUTLIER_LIVING_AREA,
            ["Gr Liv Area", "Neighborhood", "Yr Sold", "Mo Sold", "Sale Condition", "SalePrice"],
        ].sort_values(["Yr Sold", "Mo Sold"], kind="stable")
        large["price per sq ft"] = (large["SalePrice"] / large["Gr Liv Area"]).round(1)
        large["kept"] = large["Sale Condition"] != "Partial"
        partial = raw[raw["Sale Condition"] == "Partial"]
        partial_median = (partial["SalePrice"] / partial["Gr Liv Area"]).median()

        # the sales of every Sale Condition before the cut, and how many fall in the months the shipped windows test
        shipped = TemporalSplits(window=2, unit="months", min_train_fraction=0.5).splits(df, "Month Sold")
        test_rows = np.concatenate([test for folds in shipped.values() for _, test in folds.values()])
        oldest_test_month = int(pd.to_datetime(df["Month Sold"].iloc[test_rows], format="%Y%m").min().strftime("%Y%m"))
        before_cut = raw[raw["Yr Sold"] * 100 + raw["Mo Sold"] < FIRST_INCOMPLETE_MONTH]
        conditions = before_cut.assign(
            in_test_windows=(before_cut["Yr Sold"] * 100 + before_cut["Mo Sold"]) >= oldest_test_month,
            price_per_sq_ft=before_cut["SalePrice"] / before_cut["Gr Liv Area"],
        )
        by_condition = conditions.groupby("Sale Condition").agg(
            sales=("SalePrice", "size"),
            in_test_windows=("in_test_windows", "sum"),
            median_price=("SalePrice", "median"),
            median_price_per_sq_ft=("price_per_sq_ft", "median"),
        )
        by_condition["median_price_per_sq_ft"] = by_condition["median_price_per_sq_ft"].round(1)
        by_condition["kept"] = ~by_condition.index.isin(NON_MARKET_SALES)
        return [
            Decision(
                "Sales of July 2010 dropped: the extract cut the month",
                "The file ends in July 2010 with 8 sales, against 101-122 in July of every earlier year.",
                july,
            ),
            Decision(
                "Two-month test windows",
                "The convention asks for as many windows as an IID task gets splits (30), at least half of the rows "
                "for training and about 50 test rows per window. Monthly windows hold as few as 19 sales in winter; "
                "two-month windows hold at least 46.",
                pd.DataFrame(windows).set_index("window (months)"),
            ),
            Decision(
                "The 3 partial sales over 4,000 sq ft dropped, the 2 market sales kept",
                'De Cock (p. 4) names the five houses over 4,000 sq ft: three are "true outliers (Partial Sales that '
                'likely don\'t represent actual market values)" and two are "very large houses priced relatively '
                f'appropriately". The three sold at $28-$40 per sq ft, against a median of ${partial_median:.0f} for '
                "partial sales; the record describes the finished house, the price does not. All five sold before the "
                "oldest test window, so they would only train.",
                large.reset_index(drop=True),
            ),
            Decision(
                "Sales whose price is not a market value dropped",
                "The assessor values a house at its market value. Sales between family members, allocations of two "
                "linked properties with separate deeds and purchases of adjoining land are not market sales of this "
                "house (DataDocumentation.txt) and are dropped; foreclosures and short sales (Abnorml) are sold on "
                "the market and stay. All sales before the July 2010 cut, by Sale Condition.",
                by_condition,
            ),
        ]

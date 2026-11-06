"""Curated dataset definition for `pricing_game_2016_french_fleet` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    ScoringColumn,
    SplitPlan,
    TaskSummary,
    Temporal,
    drop_columns,
)

# The organisers' French column names, renamed after their descriptions in the game's rules (pricing-game-2016-FR.pdf,
# Sec. 1); CASdatasets' names for the same columns are in its pricingame.Rd.
RENAME = {
    "Num_contrat": "contract_id",  # "Numéro d'affaire"
    "IMMAT": "vehicle_id",  # "Immatriculation"
    "Date_Deb_Situ": "period_start",  # "Date de début de situation"
    "ANNEE": "year",  # "Année de situation"
    "Date_Fin_Situ": "period_end",  # "Date de fin de situation"
    "Classe_Age_Situ_Cont": "contract_age_class",  # "Classe age du contrat"
    "Type_Apporteur": "distribution_channel",  # "Type d'apporteur (agents ou courtiers ou autres)"
    "Creation_Entr": "new_company",  # "Indicateur de création entreprise (à 2 si création)"
    "Mode_gestion": "fleet_management",  # "Mode de gestion de la flotte"
    "Activite": "client_activity",  # "Activité du client (niveau contrat)"
    "Zone": "zone",  # "Zone géographique"
    "Segment": "fleet_size_class",  # "Taille de la flotte"
    "Fractionnement": "payment_frequency",  # "Fractionnement de paiement de la prime"
    "Exposition_au_risque": "exposure",  # "Véhicules année (exposition au risque)"
    "Age_du_vehicule": "vehicle_age_class",  # "Classe d'âge du véhicule"
    "ValeurPuissance": "power_value_class",  # "Combiné puissance valeur du véhicule"
    "franchise": "deductible_class",  # "Classe de franchise de la garantie DTA"
    "Nombre_vehicule": "n_vehicles",  # "Nombre de véhicule"
    "Valeur_assuree": "insured_value_class",  # "Valeur assurée"
    "FORMULE": "formula",  # "Formule souscrite"
    "Categorie_ensemble": "vehicle_category",  # "Catégorie du véhicule"
    "nombre_de_sinistre": "claim_count",  # "Nombre de sinistres"
}
# A claim's period: the contract, the vehicle, the year and the period's dates (every claim joins one period).
CLAIM_KEYS = ["Num_contrat", "IMMAT", "ANNEE", "Date_Deb_Situ", "Date_Fin_Situ"]
TARGET = "claim_charge_per_vehicle_year"
# The source's realized vehicle-years: the rate's denominator and each period's weight in training and scoring.
WEIGHT = "exposure"
CATEGORICAL = [
    "contract_age_class",
    "distribution_channel",
    "new_company",
    "fleet_management",
    "client_activity",
    "zone",
    "fleet_size_class",
    "payment_frequency",
    "vehicle_age_class",
    "power_value_class",
    "deductible_class",
    "insured_value_class",
    "formula",
]
# The test windows: the periods starting in 2013, in thirds of the year, newest first. Every window trains on the
# periods that started before 2013, all closed by 31 December 2012 (the curator's call of 2026-11-06): no training
# period is admitted by its realized end.
WINDOWS = (("2013-09-01", "2014-01-01"), ("2013-05-01", "2013-09-01"), ("2013-01-01", "2013-05-01"))
TRAIN_BEFORE = "2013-01-01"
# The game's rules (the columns in Sec. 1, the market in Sec. 4).
RULES_URL = "http://web.archive.org/web/20210422004748/https://freakonometrics.hypotheses.org/files/2016/08/pricing-game-2016-FR.pdf"


class PricingGame2016FrenchFleet(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What will a vehicle of a French company's fleet cost in material-damage claims per vehicle-year of "
            "cover, from the contract's and the vehicle's rating classes and the length of cover to the year's end, "
            "known when its period of cover starts?"
        ),
        use_case=(
            "A fleet insurer setting its tariff: it fits the pure premium, the expected claim cost per vehicle-year, "
            "on the closed years and charges it for the time each vehicle stays in the fleet. The 2016 actuarial "
            "pricing game posed this pricing task on this portfolio."
        ),
        row=(
            "One vehicle of a fleet contract over one period with unchanged contract terms, cut at each change and at "
            "the year's end: 87,228 periods of 68,485 vehicles in 18,037 contracts of an unnamed French insurer, "
            "2011 to 2013."
        ),
        predicted=(
            "The period's claim charges summed, per vehicle-year of the period (0 for 95.7% of the periods), net of "
            "the flat amounts recovered under the IDA convention between insurers, where the insurer pays its client "
            "and recovers a flat amount from the other insurer; a net recovery counts as 0. Each period counts by its "
            "vehicle-years in training and scoring. The charges are scaled by one constant of the release."
        ),
        known=(
            "The contract's age, the client's activity, zone, fleet size and management, a new-company flag, the "
            "distribution channel, payment frequency, formula, deductible and insured value classes; the vehicle's "
            "age and power-value classes; the period's start date and the length of cover to the year's end. Most "
            "periods end earlier, at a cut nobody scheduled, so the period's vehicle-years are no input."
        ),
        split=(
            "Tested on the periods starting in 2013 in three four-month windows, each trained on the periods of "
            "2011-2012, all closed by then, as the year's tariff fit on the closed years; most fleets of 2013 were "
            "insured before."
        ),
        changes=(
            "We summed each period's claim charges, set the 537 net negative totals to 0 and divided by the period's "
            "vehicle-years, which weight the period; added the length of cover to the year's end; dropped the "
            "identifiers, the year and the period's end date, made the unknown insured value missing, and gave two "
            "codes their labels."
        ),
        fit="direct",
        fit_reason=(
            "The rows are the periods an insurer prices, the features the rating classes and the length of cover it "
            "knows then, and each test window follows its training side. The target is the claim cost per "
            "vehicle-year a fleet tariff charges, weighted by the vehicle-years over which it is earned; the signal "
            "is in the claim frequency."
        ),
    )

    # Dataset
    unique_name = "pricing_game_2016_french_fleet"
    year = "2016"
    domain = "insurance"
    source = "Other"  # the organisers' files on Arthur Charpentier's site; no closer schema value
    source_url = "https://actinfo.hypotheses.org/69"
    license = None  # none stated by the organisers; CASdatasets, which redistributes the tables, is GPL (>= 2)
    data_tags = ("Anonymized", "Spatial")
    download_description = """
        The second actuarial pricing game (Arthur Charpentier, Romuald Elie and Jérémie Jakubowicz, for the 100% Data
        Science day of the Institut des Actuaires on 8 November 2016; announced on https://actinfo.hypotheses.org/69,
        DOI 10.58079/al7p) gave its players three CSV files, still on the organiser's site (Last-Modified 13 July
        2016) and archived by the Wayback Machine on 12 September 2025 with the same bytes. The rules describe the
        columns: http://web.archive.org/web/20210422004748/https://freakonometrics.hypotheses.org/files/2016/08/pricing-game-2016-FR.pdf.
        We use the two training files; test_contrats.csv (the 32,772 periods of 2014 to price) has no claims.
        The R package CASdatasets holds the same tables, renamed and recoded, as pg16trainpol, pg16trainclaim and
        pg16test (man/pricingame.Rd); its DirectComp column disagrees with the organisers' IDA flag on 1,064 claims.

        mkdir -p local-data-warehouse/pricing_game_2016_french_fleet && cd local-data-warehouse/pricing_game_2016_french_fleet
        for f in train_contrats train_sinistres; do wget http://freakonometrics.free.fr/pricinggame/$f.csv; done
        # or: wget -O $f.csv http://web.archive.org/web/20250912080148id_/http://freakonometrics.free.fr/pricinggame/$f.csv
        sha256sum train_contrats.csv train_sinistres.csv
        # d0f9caeb8146a03bdfe8ef67be2a5df576f35ae31a34d91f4c10946885c4f14a  train_contrats.csv
        # d41f7b18afea4767c50d750909be669c272696fd9d75587ca83a00d1ce6e45fe  train_sinistres.csv
    """
    bibtex = r"""
        @misc{Charpentier2016PricingGame,
          author = {Charpentier, Arthur and Elie, Romuald and Jakubowicz, J{\'e}r{\'e}mie},
          title = {Pricing Game 100\% Data Science},
          year = {2016},
          howpublished = {\url{https://actinfo.hypotheses.org/69}},
          note = {Second actuarial pricing game, Institut des Actuaires, 100\% Data Science day of 8 November 2016;
            data files train\_contrats.csv and train\_sinistres.csv at http://freakonometrics.free.fr/pricinggame/;
            DOI 10.58079/al7p; distributed as pg16trainpol and pg16trainclaim in the R package CASdatasets (Dutang
            and Charpentier)}
        }
    """
    curation_comments = """
        We start with train_contrats.csv and train_sinistres.csv, the files the organisers of the second actuarial pricing game (2016) gave its players.

        - Prediction point: the start of a vehicle's period of cover, when the insurer prices it with the year's tariff, fit on the closed years. The game asked for "une prime pure" (a pure premium) for each of the 32,772 periods of 2014 in test_contrats.csv (rules, Sec. 2, which write 37,772), with the periods of 2011 to 2013 to learn from; the claim charge per vehicle-year is the pure premium's rate, which times a period's vehicle-years gives the period's pure premium. Known then: the contract's and the vehicle's rating classes, the period's start and its length of cover to the year's end. Not known: the period's claims, and when a period cut short will end.
        - Source and year: the game's page (actinfo.hypotheses.org/69, 17 July 2016) dates the first stage "entre le 15 juillet et le 15 septembre", and the files carry a Last-Modified date of 13 July 2016. The rules (pricing-game-2016-FR.pdf, Sec. 1) describe every column; CASdatasets' copy holds the same values, its levels renamed one to one, except its DirectComp, which is 0 for 1,064 of the 1,190 claims the organisers flag IDA (a problem of that copy, not used here).
        - The portfolio is commercial fleets with a material-damage cover, not the "private motor insurance" of CASdatasets' documentation: the rules describe "Mode de gestion de la flotte", "Taille de la flotte" and "Classe de franchise de la garantie DTA" (DTA is the usual French abbreviation of an all-accident damage cover), and 1,190 of the 4,568 claims fall under the IDA convention between insurers. The row names of the training file and the 2014 file together run exactly from 1 to 120,000, so the files are likely a sample of the portfolio: counts per contract (at most 12 vehicles of a contract at once) and a vehicle's last period describe the file, not the fleets.
        - Target `claim_charge_per_vehicle_year`: the charges (CHARGE_SINISTRE) of the period's claims summed, 0 without a claim, divided by the period's vehicle-years `exposure` (MET-14); the summed charge leaves the frame as a part of the target, and `_clean` checks that the target times `exposure` gives it back. Each of the 4,568 claims joins one period on the contract, the registration, the year and the period's dates, and the claim count equals the joined claims on every period (checked in `_load_raw`). 4,250 periods have a claim (286 two or more, at most 7); 3,711 have a positive total (median 1,339, at most 13,992), so 95.7% of the targets are 0; per vehicle-year the positive values run up to 75,929, a large charge on a period of a month or two. The curator first chose the claim indicator (2026-10-30, record), switched to the charge per period on 2026-11-02 after a measurement (the charge is what the insurer prices and what the game asked for), and to the charge per vehicle-year on 2026-11-06 (CC below).
        - 537 periods net below 0 set to 0 (down to -1,863), as pricing_game_2017_french_mtpl and frempl_french_motor_personal_line do (the family call of 2026-10-30: "a net recovery is no claim cost of the year"). They are claims under the IDA convention ("1 si sinistre Indemnisation Direct de l'Assuré", rules Sec. 1), where the insurer pays its client and recovers a flat amount, not the cost, from the other insurer; every claim with a charge of 0 or less is IDA, and 126 of the 1,190 IDA claims are at 50% responsibility. Tweedie and Poisson losses need a non-negative target. The total is clipped, not each claim (65 periods mix signs, 16 of them net below 0); the clip raises the total claim cost by 4.3%.
        - Only the frequency carries signal. Among the periods with a positive charge, the log charge is not predictable from the classes (R^2 -0.06 for LightGBM, -0.02 for ridge, measured on 2011-2012 to 2013), and a weighted Poisson model of the claims per vehicle-year ranks the charges per vehicle-year at 0.164, 0.167 and 0.210 on the windows (newest first), against 0.114, 0.158 and 0.190 for the weighted Tweedie model of the charge (normalized weighted Gini, regularised LightGBM, 5 seeds). The task is the frequency task with severity noise on top. Raw rate, not log1p (CLEAN-16 as amended: a rate scored by a Gini keeps the scale the curator chose): the Gini ranks by the expected charge per vehicle-year, which a log1p fit transformed back orders by its geometric mean instead. A fit weighted by the vehicle-years on this scale estimates E[charge | x] / E[vehicle-years | x], the charge per vehicle-year that breaks even.
        - Exposure (LEAK-41, MET-14, MET-15; issue 5, resolved 2026-11-06): `exposure` is the source's Exposition_au_risque, "Véhicules année (exposition au risque)": the period's vehicle-years, (end - start + 1) / 365 (/ 366 in the leap year 2012) times the period's vehicles (2 on two periods), rounded to 0.01, which `_clean` checks on every period. It is realized: of the 87,228 periods of 68,485 vehicles (2011 to 2013), 57.4% end before 31 December at a cut nobody scheduled and 0.8% at a contract anniversary, so their length is known only at their end. The task divides the period's charge by it and weights each period by it in training and scoring (the weight scoring column and the `sample_weight`), never as a feature. The part known at the start ships as the feature `exposure_to_year_end`, the same formula to 31 December (LEAK-7, LEAK-37). The shipped features were leak-free since the fix of 2026-11-02 (next bullet), but the target summed over the realized period still rewarded predicting how long a vehicle stays: about 0.03 of the row Gini (the direct model of the total 0.210 against 0.182 for its rate times the length to 31 December; a rough attribution of the exposure study of 2026-11-05). A fit that ignores the weight loses 0.010 of the declared metric on the shipped windows (SD 0.009, lower on 4 of 5 seeds; 0.006 in the study), little, since no period is shorter than 30 days.
        - Why the rate (CC below): a fleet's premium is revised per vehicle as vehicles come in and go out (AMRAE, as cited by the review panel; not checked), so a fleet tariff charges a rate per vehicle-year, earned over the time the vehicle stays. A realized time on risk is also a valid weight when the outcome cuts it short: when a period's end is a stopping time of its claim history, the weighted fit estimates E[charge | x] / E[vehicle-years | x], the rate that breaks even per vehicle-year (the exposure study's stopping-time argument, checked there by simulation; a stopping rule driven by unobserved risk was not simulated). The game's 2014 file gave its players each period's realized end and length (58.2% end before 31 December 2014); that is no ground here, since a host's test file is a holdout of the same snapshot, not deployment data (LEAK-38).
        - The realized length as a feature (fixed on 2026-11-02): until then `exposure` was a feature holding the realized length, and with `period_start` a feature it gave back the dropped end. On the three windows it added ROC AUC on the claim indicator +0.040, +0.055 and +0.052 over the length known at the start (regularised LightGBM on the rating classes and the start's day of the year, 3 seeds), and the early ends go with claims: a rate ratio of 1.22 [1.12, 1.33] given the rating classes (Poisson GLM with the length as offset, 2011-2012). Confirmed by the curator (Andrej, 2026-11-02) and recorded as the LEAK-10 case for time on risk cut short by the outcome: the cut is fixed where the data locates it. With the rate, the realized length is the weight alone. Probe 22 (LEAK-41): the features predict the realized vehicle-years at R^2 0.38, mostly through `fleet_management` and `exposure_to_year_end`, both known at the start, so they stay (USE-6); no feature's gain goes through the weight above noise, and 1/vehicle-years alone scores 0.029, the ceiling a proxy would reach. On the shipped windows (5 seeds) the time features (`exposure_to_year_end`, `period_start`) add 0.007 to the weighted Tweedie fit (SD 0.009) and 0.001 to the weighted L2 fit; the realized vehicle-years as a feature would add 0.013 to the Tweedie fit (on 5 of 5 seeds).
        - The covariates carry the signal: on the three windows (newest first) a regularised Tweedie LightGBM fitted with the weight scores a normalized weighted Gini of 0.114, 0.158 and 0.190 (bootstrap standard errors 0.068, 0.054 and 0.023), an untuned one 0.105, 0.098 and 0.183, a weighted Tweedie GLM 0.159, 0.171 and 0.200, the length to 31 December and the start's day of the year alone 0.005, -0.027 and -0.027, and the weighted constant 0 (5 seeds; the start enters as its day of the year). The models beat the constant on every window, so the task is not trivial (TP-4), on the newest window (103 positive charges) by about 1.7 standard errors. A weighted Tweedie deviance (power 1.5) orders them otherwise, and by little: it puts the GLM below the weighted constant on every window (89.9 against 91.2 on average) and the LightGBM above it on the two newest (94.9), as it also scores the level, and the charges per vehicle-year of the 2013 windows (180 to 205) run above those of 2011-2012 (167). The task probes flag `no_signal` and `drift_baseline` (TP-1, TP-2): they score R^2, which follows a few large rates (best family linear, R^2 0.001); under the declared metric the linear family scores 0.168, the random forest 0.121 and the probes' untuned L2 LightGBM 0.003, against 0 for the weighted dummy, as for pricing_game_2017_french_mtpl. The leak probes find nothing: every feature alone at R^2 0.001 or below; 9.8% of the test rows have a copy of their features in training once the start date is left out, none with it.
        - Not added, measured on all of 2013 on the claim indicator (the same LightGBM, trained on 2011-2012): the contract's and the vehicle's claims and exposure of the previous year (ROC AUC 0.667 with them, 0.668 without; a known entity's history is legitimate, USE-10, but it carries nothing here), and the contract's vehicles in force at the period's start (0.667).
        - Dropped: `contract_id` (apparently numbered in the order of subscription: median 14,885 for contracts of at most a year, 2,027 for those over 5 years, which the contract's age class carries) and `vehicle_id` (the anonymised registration), `year` (the year of the period's start on every row), `period_end` (unknown at the start for the periods that end early; the realized length it sets ships as the weight `exposure`), `vehicle_category` (one value) and the files' unnamed row index.
        - `insured_value_class` "ND" (not available) made missing: 87,093 periods (99.8%); the 135 others hold five value classes.
        - Labels restored: `payment_frequency` A, S, T as annual, semi-annual, quarterly (the French "annuel", "semestriel", "trimestriel"); `new_company` 2 as Yes and 1 as No ("à 2 si création", rules Sec. 1). The other classes keep the organisers' codes: French labels for the ages and the deductible, anonymised numbers for the zone, activity, channel, formula, fleet size and power-value class.
        - Dtypes: every class column categorical; the power-value class (11 levels, a combined power and value grid) has no documented order. `exposure_to_year_end` and `n_vehicles` numeric (`n_vehicles` is 1 on every period but 2, which hold 2; kept as the source ships it); `period_start` a date. `exposure` is the weight scoring column, never a feature.
        - 11,807 periods (13.5%) repeat the features of another, 10,828 of them with the same target and 979 with another: vehicles of one fleet in the same period share every contract class and the start, so the length to the year's end, and differ only by their own two classes. Natural, kept (LEAK-18).
        - Anomaly: no period is shorter than 30 days, in the training file and the 2014 pricing file alike, and no period of a year starts after 2 December: the organisers seem to have left the shortest periods out, so the task covers periods of a month or more.
        - Anomaly: the categorical levels are anonymised and the charges scaled by one constant (the record's generated-data tests of 2026-11-01: disclosure control, not generation); the charges are kept as published (the constant, 1.077841, changes no ranking).
        - The newest periods lose no claims: claims per vehicle-year are 0.117, 0.119 and 0.119 in 2011 to 2013, and 0.115, 0.114 and 0.117 for the periods ending in the fourth quarter (LEAK-24 not triggered).
        - Note: claims of the periods that close late in 2012 may have been reported only after the year's tariff is fit. The files hold the counts as of their extract (claims closed up to 2014, 41 still open) and no report date, so the delay can only be simulated: hiding the training charges of the claims that fall in the last 30 or 90 days of 2012 (each claim placed uniformly in its period; 134 and 377 periods, 5 seeds) moves the January window from 0.190 to 0.192 and 0.187 (regularised Tweedie LightGBM fitted with the weight); at the May and September windows' start those claims are four and eight months old. Applied to every window, as if the year's tariff were fit once on 1 January 2013, it moves the window mean from 0.154 to 0.151 and 0.119: the September window falls to 0.101 and 0.015, as the training periods that start late in 2012 lose most of their claims and the model learns that late starts claim little. 41 claims were still open at the extract, so their charges may still move. A simulation, not a measurement. No gap separates the January window from its training side: an exception to SPLIT-10 that serves SPLIT-14's floor (Andrej, 2026-11-02). With every training label fixed at 31 December 2012, a gap inside 2012 would admit the 2012 periods by their realized end (LEAK-41), and a whole year leaves 2011 alone, 30.4% of the rows. The May and September windows start four and eight months after the training side ends.
        - CC (2026-11-06, Lennart): the target is the claim charge per vehicle-year over the realized period, `exposure` (the source's Exposition_au_risque, restored) its denominator, the weight scoring column and the `sample_weight`, never a feature (MET-14, MET-15, LEAK-41; issue 5, D11 of the exposure review); the length to 31 December stays a feature as `exposure_to_year_end` (LEAK-7, LEAK-37); the metric is the normalized weighted Gini of the rate, still a stand-in for the game's market; the scale stays the identity (CLEAN-16 as amended). Supersedes Andrej's call of 2026-11-02 on the target (the claim charge per period, issue 4): the exposure study measured later that the total over the realized period rewards predicting how long a vehicle stays (about 0.03 of the row Gini) and that the rate model ranks the rate better under the weighted Gini (0.153 against 0.138 for the model of the total; 0.154 against 0.136 on the shipped windows).
        - CC (2026-11-06, Lennart): every window trains on the periods that started before 2013 (56,178 periods of 2011-2012, 24,674 vehicle-years), all closed by 31 December 2012, so no training row is admitted by its realized end (LEAK-41; issue 5, D11 of the exposure review). Supersedes Andrej's expanding training sides of 2026-11-02 (issue 2 (d)): the exposure study's red team measured later that the 2013 periods they admitted, those that ended early, claim more (0.127 and 0.131 claims per vehicle-year against 0.115 and 0.116 for the 2013 periods they left out; 10.8% and 4.0% of the training vehicle-years of the September and May windows), and LEAK-41 (2026-11-06) bars training on rows selected by their realized end.
    """

    # Task
    target = TARGET
    problem_type = "regression"
    metric = Metric.stand_in(
        "normalized_weighted_gini",
        original=(
            "each player's result in the 2014 market the organisers ran as a price aggregator: each insured going to "
            "a company drawn at random among the cheapest premiums, every player's premiums scaled by one uniform "
            "factor to a total of 2.5 million euros (rules, Sec. 4 'Règles du Jeu')"
        ),
        reason=(
            "The market needs the other players' premiums and the claims of 2014, neither published. The uniform "
            "scaling ('un facteur d'inflation appliqué uniformément') took away each player's price level, so the "
            "market rewarded the ranking of the risks; the normalized Gini scores that ranking, the metric of the "
            "insurers' Kaggle competitions (Allstate 2011, Liberty Mutual 2014), here in Liberty Mutual's weighted "
            "form: the periods are ranked by the predicted charge per vehicle-year and each counts by its "
            "vehicle-years, so the score rewards the rate a fleet tariff charges, not a guess of how long a vehicle "
            "stays (MET-15). pricing_game_2017_french_mtpl, whose game kept the price level and ruined a player at "
            "170% losses, scores a Tweedie deviance instead. The game's page (actinfo.hypotheses.org/69) and "
            "CASdatasets' pricingame.Rd name no other metric. On the shipped windows (newest first, 5 seeds) a "
            "regularised Tweedie LightGBM fitted with the weight scores 0.114, 0.158 and 0.190, a weighted Tweedie "
            "GLM 0.159, 0.171 and 0.200, the length to 31 December and the start alone -0.016 on average, the "
            "weighted constant 0; a model of the charge over the realized period, the target until 2026-11-06, ranks "
            "the rate at 0.136 on average against 0.154. A weighted Tweedie deviance moves little from the "
            "constant's, and in both directions (the GLM 89.9, the LightGBM 94.9, the constant 91.2): it also scores "
            "the year's level, which the market's uniform scaling took away."
        ),
        reference=RULES_URL,
        inputs={"weight": WEIGHT},
    )
    scoring_columns = (
        ScoringColumn(
            column=WEIGHT,
            role="weight",
            used_by="normalized_weighted_gini",
            description=(
                "the period's vehicle-years (the source's Exposition_au_risque, 0.08 to 1), realized: 57.4% of the "
                "periods end before 31 December at a cut nobody scheduled, known only when it comes. The rate's "
                "denominator; each row's weight in the metric and in training; never a feature"
            ),
        ),
    )
    sample_weight = WEIGHT
    accepted_check_warnings = {
        "dataset_duplicate_rows": (
            "Vehicles of one fleet in the same period share every contract class and the start, so the length to the "
            "year's end, and differ only by their own two classes: natural repeats (LEAK-18). With `period_start` a "
            "feature no copy crosses the split."
        ),
        "dataset_conflicting_duplicate_rows": (
            "The same repeats as dataset_duplicate_rows: vehicles of one fleet with the same classes in the same "
            "period, with different claim charges per vehicle-year (another charge, or the same charge over another "
            "realized length). Natural (LEAK-18); the outcome of one vehicle is not the other's."
        ),
        "task_target_value_dominant": (
            "Zero-inflated by nature: the claim charge per vehicle-year is 0 for 95.7% of the periods, those with no "
            "claim (95.1%) or whose claims net to 0 or less after IDA recoveries (0.6%, negative totals set to 0); "
            "not a cap or a placeholder."
        ),
        "meta_license_unknown": (
            "The organisers state no licence for the game's files; CASdatasets, which redistributes the same tables, "
            "is GPL (>= 2)."
        ),
    }
    temporal = Temporal(on="period_start", horizon=4, horizon_unit="months")
    splits_comment = """
        Three test windows, the periods starting in 2013 by thirds of the year (September to December, May to August,
        January to April, newest first): 5,312, 6,509 and 19,229 periods, 987, 2,218 and 10,659 vehicle-years. Every
        window trains on the periods that started before 2013, the 56,178 periods of 2011-2012 (64.4% of the rows,
        24,674 of the 38,538 vehicle-years); rows are cut at 31 December, so each of them closed by 31 December 2012
        and its label is known at every window's start. The use case is a tariff: the game priced every period of 2014
        from 2011-2013, and the claims of 2014 were never published, so 2013 is the test year (suggested on 2026-10-30
        and accepted with the curator's Yes). Until 2026-11-06 each window trained on every period closed before it
        starts (67,886, 61,797 and 56,178 periods; Andrej, 2026-11-02). From 2013 on that admitted only the periods
        that ended early, which claim more: 0.127 and 0.131 claims per vehicle-year against 0.115 and 0.116 for the 2013
        periods still running, 10.8% and 4.0% of the training vehicle-years of the September and May windows. No
        training row is now admitted by its realized end (LEAK-41; the curator's call of 2026-11-06). The claims carry
        no dates, so a period still running cannot enter with its claims to date, and between two year ends a training
        side can grow only by the periods that ended early: the three windows share one training side, one model
        scored on three cohorts. SPLIT-14 as amended on 2026-11-02 counts windows that share a training side as one
        window; whether to amend it for this case or ship the task forced (SPLIT-8) is open for the curator. On the old
        training sides the same model scored 0.137, 0.160 and 0.190 (newest first), on the shared one 0.114, 0.158 and
        0.190 (regularised Tweedie LightGBM fitted with the weight, 5 seeds). Three windows, not the nine of the
        convention (SPLIT-15): finer windows only cut the same test rows into noisier pieces. A period's start caps its
        length, so each window holds one cohort of lengths: the commonest start is 1 January (12,028 periods in 2013),
        the claims per vehicle-year are 0.129, 0.122 and 0.117 (newest first), and the share of periods with a claim
        follows the length (2.3%, 3.9%, 6.0%). A window's score ranks the periods within its cohort, and the mean over
        the windows runs below a score pooled over 2013 (0.154 against 0.171, the same model). The newest window is the
        smallest and the noisiest (123 periods with a claim, 103 with a positive charge; bootstrap standard error
        0.068). No gap separates the January window from the training side (SPLIT-10; the notes give the reason and
        the simulated bound); the May and September windows start four and eight months after it ends. Fleets and
        vehicles recur across the cutoff, as a tariff prices the insurer's known fleets (SPLIT-13): 76-81% of the test
        periods belong to a contract in training, 23-26% to a vehicle in training.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        periods = pd.read_csv(raw_dir / "train_contrats.csv", index_col=0)
        claims = pd.read_csv(raw_dir / "train_sinistres.csv", index_col=0)
        assert not periods.duplicated(CLAIM_KEYS).any()
        # Each claim's period, on the contract, the registration, the year and the period's dates (the join of
        # CASdatasets' own check: every claim has a period, and the count equals the joined claims).
        per_period = claims.groupby(CLAIM_KEYS, sort=True).agg(
            joined_claims=("CHARGE_SINISTRE", "size"),
            claim_total=("CHARGE_SINISTRE", "sum"),
            claims_positive_charge=("CHARGE_SINISTRE", lambda s: int((s > 0).sum())),
            claims_ida=("IDA", "sum"),
        )
        raw = periods.merge(per_period.reset_index(), on=CLAIM_KEYS, how="left", validate="one_to_one")
        raw = raw.fillna({"joined_claims": 0, "claim_total": 0.0, "claims_positive_charge": 0, "claims_ida": 0})
        assert raw["joined_claims"].sum() == len(claims)
        assert (raw["joined_claims"] == raw["nombre_de_sinistre"]).all()
        return raw

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. English names after the rules' descriptions (RENAME).
        df = raw.rename(columns=RENAME)
        # 2. The period's dates. Rows are cut at 31 December, so a period ends in the year it starts: every period that
        #    started before 2013 closed by 31 December 2012, the training side of every window (_make_splits).
        df["period_start"] = pd.to_datetime(df["period_start"], format="%d/%m/%Y")
        end = pd.to_datetime(df["period_end"], format="%d/%m/%Y")
        assert (df["period_start"].dt.year == df["year"]).all()
        assert (end.dt.year == df["year"]).all()
        # 3. The period's vehicle-years: the source's `exposure` is realized, (end - start + 1) / 365 (/ 366 in 2012)
        #    times the period's vehicles, rounded to 0.01. The length to 31 December, the same to the year's end, is
        #    known at the start and is a feature (LEAK-7, LEAK-37).
        start = df["period_start"]
        year_end = pd.to_datetime(start.dt.year.astype(str) + "-12-31")
        days_in_year = np.where(start.dt.is_leap_year, 366, 365)
        realized = (((end - start).dt.days + 1) / days_in_year * df["n_vehicles"]).round(2)
        assert np.isclose(realized, df[WEIGHT]).all()
        df["exposure_to_year_end"] = (((year_end - start).dt.days + 1) / days_in_year * df["n_vehicles"]).round(2)
        # 4. The target: the period's claim charges summed, a net negative total (IDA recoveries) set to 0, per realized
        #    vehicle-year (MET-14). The summed charge leaves the frame as a part of the target, and `exposure` stays
        #    only as the weight scoring column, never a feature (LEAK-41, MET-15).
        charge = df["claim_total"].clip(lower=0)
        assert (df[WEIGHT] > 0).all()
        df[TARGET] = charge / df[WEIGHT]
        assert np.allclose(df[TARGET] * df[WEIGHT], charge, rtol=1e-12, atol=1e-9)
        # 5. Labels for two codes: the payment frequency (annuel, semestriel, trimestriel) and the new-company flag
        #    ("à 2 si création").
        df["payment_frequency"] = df["payment_frequency"].map({"A": "annual", "S": "semi-annual", "T": "quarterly"})
        df["new_company"] = df["new_company"].map({1: "No", 2: "Yes"})
        assert df[["payment_frequency", "new_company"]].notna().all().all()
        # 6. The insured value "ND" (not available): missing.
        df["insured_value_class"] = df["insured_value_class"].replace("ND", np.nan)
        # 7. Drops: the identifiers, the year (the start's year), the period's end (unknown at the start when the
        #    period ends early; the realized length it sets is the weight), the constant vehicle category, the claim
        #    count and the join's columns (parts of the target).
        assert df["vehicle_category"].nunique() == 1
        return drop_columns(
            df,
            [
                "contract_id",
                "vehicle_id",
                "year",
                "period_end",
                "vehicle_category",
                "claim_count",
                "claim_total",
                "joined_claims",
                "claims_positive_charge",
                "claims_ida",
            ],
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=CATEGORICAL, datetime=["period_start"])

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        """Three windows of 2013 (newest first), each trained on the periods that started before 2013."""
        start = df[self.temporal.on]
        train = np.flatnonzero(start < pd.Timestamp(TRAIN_BEFORE)).tolist()
        splits = {}
        for split, (lo, hi) in enumerate(WINDOWS):
            test = np.flatnonzero((start >= pd.Timestamp(lo)) & (start < pd.Timestamp(hi))).tolist()
            splits[split] = {0: (train, test)}
        return SplitPlan(splits=splits)

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        periods = raw.assign(
            start=pd.to_datetime(raw["Date_Deb_Situ"], format="%d/%m/%Y"),
            end=pd.to_datetime(raw["Date_Fin_Situ"], format="%d/%m/%Y"),
            claim=raw["nombre_de_sinistre"] > 0,
        ).sort_values(["Num_contrat", "IMMAT", "start"], kind="stable")
        later = periods.groupby(["Num_contrat", "IMMAT"])["start"].shift(-1).notna()
        year_end = (periods["end"].dt.month == 12) & (periods["end"].dt.day == 31)
        ending = pd.Series(
            np.select(
                [year_end, later],
                ["31 December", "earlier, the vehicle goes on"],
                "earlier, the vehicle's last period in the file",
            ),
            index=periods.index,
            name="the period ends",
        )
        closed = periods["ANNEE"] < 2013
        rates = (
            periods.loc[closed]
            .groupby(ending[closed])
            .agg(
                periods=("claim", "size"),
                vehicle_years=("Exposition_au_risque", "sum"),
                claims=("nombre_de_sinistre", "sum"),
            )
            .rename(columns={"vehicle_years": "vehicle-years (realized)"})
        )
        rates["claims per vehicle-year"] = (rates["claims"] / rates["vehicle-years (realized)"]).round(3)
        rates["vehicle-years (realized)"] = rates["vehicle-years (realized)"].round().astype(int)
        trained = periods["start"] < pd.Timestamp(TRAIN_BEFORE)
        sides = {}
        for lo, hi in WINDOWS:
            test = (periods["start"] >= pd.Timestamp(lo)) & (periods["start"] < pd.Timestamp(hi))
            # The rule until 2026-11-06: every period closed before the window starts. From 2013 on it admitted the
            # periods that ended early and left out those still running.
            admitted = ~trained & (periods["end"] < pd.Timestamp(lo))
            running = ~trained & (periods["start"] < pd.Timestamp(lo)) & ~admitted
            sides[f"{lo} to {hi}"] = {
                "test periods": int(test.sum()),
                "test vehicle-years": round(periods.loc[test, "Exposition_au_risque"].sum()),
                "training periods": int(trained.sum()),
                "training vehicle-years": round(periods.loc[trained, "Exposition_au_risque"].sum()),
                "2013 periods closed before (admitted until 2026-11-06)": int(admitted.sum()),
                "their claims per vehicle-year": _claims_per_vehicle_year(periods[admitted]),
                "2013 periods still running (left out)": int(running.sum()),
                "claims per vehicle-year of those": _claims_per_vehicle_year(periods[running]),
            }
        windows = pd.DataFrame(sides).T.rename_axis("test window")
        positive = periods.loc[periods["claim"]]
        kinds = pd.Series(
            {
                "periods with a claim": len(positive),
                "with two or more claims": int((positive["nombre_de_sinistre"] >= 2).sum()),
                "with an IDA claim": int((positive["claims_ida"] > 0).sum()),
                "with no claim of positive charge": int((positive["claims_positive_charge"] == 0).sum()),
                "with a net total below 0 (set to 0)": int((positive["claim_total"] < 0).sum()),
            },
            name="periods",
        )
        return [
            Decision(
                "The charge per realized vehicle-year, weighted by the vehicle-years",
                "The source's length is realized: a period that ends before 31 December is known only at its end, "
                "and 57.4% of the periods end at a cut nobody scheduled. Those ends go with claims: in 2011-2012 a "
                "vehicle's last period in the file that ends early has more claims per vehicle-year than a period "
                "that runs to the year's end (a rate ratio of 1.22 given the rating classes). The target is "
                "therefore the charge per vehicle-year, each period weighted by its vehicle-years and never given "
                "them as a feature; the length to 31 December, known at the start, is the feature "
                "`exposure_to_year_end` (curation_comments).",
                rates,
            ),
            Decision(
                "Every window trains on the periods of 2011-2012",
                "Rows are cut at 31 December, so every period that started before 2013 closed by 31 December 2012. "
                "Training on the periods closed before each window starts admitted from 2013 on only the periods "
                "that ended early, which claim more than the 2013 periods still running then; claims carry no "
                "dates, so those could not join with their claims to date.",
                windows,
            ),
            Decision(
                "A net recovery counts as no cost",
                "The target is the period's claim charges summed, per vehicle-year. Claims under the IDA convention, "
                "where the insurer pays its client and recovers a flat amount from the other insurer, can net below "
                "0; such a total is set to 0, as in pricing_game_2017_french_mtpl and "
                "frempl_french_motor_personal_line.",
                kinds,
            ),
        ]


def _claims_per_vehicle_year(periods: pd.DataFrame) -> float:
    """Claims per realized vehicle-year of ``periods`` (NaN for none)."""
    vehicle_years = periods["Exposition_au_risque"].sum()
    return round(periods["nombre_de_sinistre"].sum() / vehicle_years, 3) if vehicle_years else float("nan")

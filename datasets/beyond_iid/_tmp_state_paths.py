"""Saving some paths to final data warehouse objects we can use to test pipelines."""

# All datasets from TabArena-v0.1 except for anneal
from __future__ import annotations

OLD_IID = [
    "airfoil_self_noise/019d5a0c-3004-72c3-b77b-bc348a86d057",
    "amazon_employee_access/019d5a13-37b4-7594-8a48-a780986aac02",
    "aps_failure/019d5a19-a77e-7e75-9285-03d7590d92ac",
    "bad_customer_detection/019d5a1d-5e57-75cc-bcc3-d7a64a60be6f",
    "bank_customer_churn/019d5a1f-9a7c-7d72-904c-1d93d5022c45",
    "bank_marketing/019d5a21-1299-7155-9284-2b70845773c6",
    "bioresponse/019d5a23-4b00-71bc-b7e0-165aa7637026",
    "blood_transfusion/019d5a26-127f-7829-a7aa-b8f64453817c",
    "churn/019d5a30-5048-7343-a874-cba1cec352f8",
    "coil_2000/019d5a33-6f75-728d-9c68-b914c36b2cc4",
    "concrete_compressive_strength/019d5a35-f183-77c9-86c8-31aba89919d0",
    "credit_card_clients_default/019d5a3b-bdd6-77da-b7ac-8e0530344f06",
    "credit_g/019d5a3e-45e9-73c3-8bbc-51310c58e706",
    "customer_satisfaction_in_airline/019d5a40-723c-766e-9204-b4b7a43433b9",
    "diabetes/019d5a42-a734-7a8e-ab43-f20a26441cdf",
    "diabetes_130_us/019d5a45-e831-764b-acac-3b1d4b86efc1",
    "diamonds/019d5a49-17e3-7e0b-96e4-a249e9811d58",
    "ecommerce_shipping/019d5a4d-7f92-7bc7-a5fc-5a63ac679eef",
    "fiat_500/019d5a4f-cfd0-7f95-843b-6a5809c4dad6",
    "fitness_club/019d5a51-af8e-757c-8da2-a796806da5ec",
    "food_delivery_time/019d5a56-f4f0-7a67-ba99-b4488a29da26",
    "give_me_some_credit/019d5a5a-0489-724b-8585-d85f7f89ef19",
    "hazelnut_spread_contaminant_detection/019d5a5e-88ba-798d-b9ce-5d608eb75376",
    "healthcare_insurance_expenses/019d5a62-7abf-7865-8e8a-52175c085ace",
    "heloc/019d5a64-d939-7d49-bb24-54f75fe34648",
    "hiva_agnostic/019d5a6c-8da8-76cc-b302-67c9e72919e3",
    "houses/019d5a72-4a30-70a4-aebc-51ac3e1b5919",
    "hr_analytics/019d5a75-800d-73ee-9562-257f920156af",
    "in_vehicle_coupon_recommendation/019d5a7b-062c-76a7-932c-23529541fe88",
    "jm1/019d5a7c-b7d2-7552-901d-84a3d2cdf8cf",
    "kdd_cup_09_appetency/019d5a82-90fb-75cf-8d91-f257af303383",
    # FIXME finish: stopped at marketing_campaign
]

NEW_IID = []


TEMPORAL = [
    "acquire_valued_shoppers_challenge/019d3061-8d31-7283-b44d-95d0027d9b1e",
    "climate_model_weather_forecasting/versions/019d307b-f29b-7d7a-ada3-a8786a9bc50b",
    "cooking_time/versions/019d308c-c2ae-71dc-9c65-e4b185c97eb4",
    "delivery_eta/versions/019d308d-e4dd-7cea-b6b0-d751f87f28bd",
    "home_credit_default_stability/versions/019d308f-f814-7a3e-bf8f-508273a0e8f1",
    "hotel_booking_demand/019d3094-d6dc-7d0e-94bf-e347bcf57b62",
    "kick/019d309d-6946-7ce9-8855-d4eaa085cc8a",
    "mercedes_benz_greener_manufacturing/019d30a6-ff90-7266-9415-6b6387c7bfa1",
    "real_estate_valuation/019d30a8-1b61-74d7-965e-ea11cb5e3b00",
    "sberbank_housing_market_forecasting/019d30ac-bd6e-752a-9af2-64a92030816c",
    "maps_router_eta/versions/019d30d6-9695-72cc-a7ac-cef01b6aac2f",
    # Has Text features
    "california_house_prices_2020/019d3064-3158-7e93-b010-51a7b6c72ba1",
    "coffee_rating_prediction/019d3070-4a03-7b94-937b-c85548fb18a8",
    "consumer_complaints/versions/019d3082-8081-7605-9ad1-b222b1b92bc8",
    "lending_club/versions/019d309f-8ab1-72ee-9362-8ddd9a37cf6b",
    "kickstarter/019d30a1-68be-7d5c-b949-bbf4cef2bfe2",
    "sf_permit_time/019d30b1-17ef-798e-9e04-3313c31ada6b",
]

GROUPED = [
    # labels per group
    "mice_protein_trisomy_discriminant/019d3198-e47c-7c16-8878-751d864d733a",
    "musk/019d3199-b80d-7a81-913b-6bf76f29a4b8",
    "micro_mass/019d319c-d4d7-7b90-9c84-1201e1f4eb51",
    "parkinsons_biomedical_voice_measurements/019d31a1-372f-7747-8f85-5a2f4db00156",
    "amex_non_iid/versions/019d31ff-7b8d-7085-ad19-77fecaae5d49",
    # labels per sample
    "telemonitoring_parkinsons_biomedical_voice_measurements/019d3199-5680-7c5b-a46f-4e903e243c78",
    "dementia_prediction/019d319a-9692-77bc-adc4-1d10e79a59d6",
    "covertype/019d319b-4e2b-7eb3-b3ba-5082672806cb",
    "sepsis_prediction/versions/019d31fc-b169-742d-b28a-140b6c6163a5",
    "cardiotocography/019d436b-554c-7414-9550-bcd4d9b807dc",
    "sat11_hand_algo_runtime/019d4414-2726-7318-8ad1-e4c6d6f5907a",
    "asp_potassco_classification/019d446e-400c-7e01-96ee-3842694b51ef",
    "video_transcoding_time_prediction/019d4511-c926-7192-9183-35f9cd8adb70",
    "video_game_fps_prediction/019d4555-8f57-70ec-b003-1946e22f6185",
    "electric_motor_temperature_prediction/019d459a-334a-7077-812d-776a08a70ee2",
]

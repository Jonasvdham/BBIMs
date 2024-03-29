import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from constants import (
    MATERIALS,
    CURRENT_YEAR,
    M2FACADE,
    RVALUE,
    BUILDING_LIFETIME,
)
from data_loader import load_data

MATERIAL_DATA, WASTE_DATA, ENERGY_DATA, TRANSPORT_DATA = load_data()


def make_datasets(
    materials=[
        "straw",
        "hemp",
        "flax",
        "wood fiber",
        "EPS",
        "XPS",
        "stone wool",
        "glass wool",
        "gypsum",
    ],
    building_scenario="normal",
    total_houses=97500,
    time_horizon=2050,
    timeframe=200,
    waste_scenario=0,
):
    datasets = {}
    for material in materials:
        df = make_dataset(
            material,
            building_scenario,
            total_houses,
            time_horizon,
            timeframe,
            waste_scenario,
        )
        datasets[material] = df
    return datasets


def make_dataset(
    material="straw",
    building_scenario="normal",
    total_houses=97500,
    time_horizon=2050,
    timeframe=200,
    waste_scenario=0,
):
    if material not in MATERIALS.keys():
        raise ValueError("Material not supported")

    mph = mass_per_house(material)
    mpy = mass_per_year(
        building_scenario,
        mph,
        total_houses,
        time_horizon - CURRENT_YEAR,
        timeframe,
    )
    no_replacements = int(
        np.ceil(BUILDING_LIFETIME / MATERIALS[material]["lifetime"]) - 1
    )
    waste_per_kg = waste_emissions(material, timeframe, waste_scenario)

    construction_emissions = construction(
        material, timeframe, mpy, no_replacements
    )
    replacement_emissions = replacement(
        material, timeframe, mpy, no_replacements, waste_per_kg
    )
    demolition_emissions = demolition(material, timeframe, mpy, waste_per_kg)
    return (
        construction_emissions + replacement_emissions + demolition_emissions
    )


def construction(material, timeframe, mpy, no_replacements):
    dataset = pd.DataFrame(
        MATERIAL_DATA[MATERIAL_DATA["Name"] == MATERIALS[material]["name"]][
            ["CO2", "CH4", "N2O", "CO"]
        ]
        .reset_index(drop=True)
        .loc[[0 for i in range(timeframe)]]
        .multiply(mpy, axis=0)
    )

    if MATERIALS[material]["plant_based"]:
        dataset["CO2"] += CO2bio(material, mpy, timeframe)
        dataset += pd.DataFrame(transport50km(kg) for kg in mpy)

    tmp = pd.DataFrame(
        np.zeros((timeframe, 4)), columns=["CO2", "CH4", "N2O", "CO"]
    )
    for i in range(no_replacements):
        timeshift = pd.DataFrame(
            np.zeros(((i + 1) * MATERIALS[material]["lifetime"], 4)),
            columns=["CO2", "CH4", "N2O", "CO"],
        )
        tmp += (
            pd.concat([timeshift, dataset], ignore_index=True)
            .reset_index(drop=True)
            .iloc[:timeframe]
        )
    return dataset.reset_index(drop=True) + tmp


def replacement(material, timeframe, mpy, no_replacements, waste_per_kg):
    dataset = pd.DataFrame(
        np.zeros((timeframe, 4)), columns=["CO2", "CH4", "N2O", "CO"]
    )
    for j in range(no_replacements):
        for i in range(timeframe):
            dataset.loc[i + MATERIALS[material]["lifetime"] * (j + 1)] = (
                waste_per_kg * mpy[i]
            )

    return dataset[:timeframe]


def demolition(material, timeframe, mpy, waste_per_kg):
    dataset = pd.DataFrame(
        np.zeros((timeframe, 4)), columns=["CO2", "CH4", "N2O", "CO"]
    )
    for i in range(timeframe):
        dataset.loc[i + BUILDING_LIFETIME] = waste_per_kg * mpy[i]
    return dataset[:timeframe]


def waste_emissions(material, timeframe, waste_scenario):
    if (
        MATERIALS[material]["CO2bio"] != 0
        and MATERIALS[material]["waste"][waste_scenario] == "incineration"
    ):
        waste_per_kg = pd.Series(
            [-MATERIALS[material]["CO2bio"], 0, 0, 0],
            index=["CO2", "CH4", "N2O", "CO"],
        )
        waste_per_kg += transport50km(1)
    else:
        waste_per_kg = WASTE_DATA[
            WASTE_DATA["Name"] == MATERIALS[material]["waste"][waste_scenario]
        ][["CO2", "CH4", "N2O", "CO"]].iloc[0]
    return waste_per_kg


def mass_per_year(building_scenario, mph, total_houses, years, timeframe):
    if building_scenario == "normal":
        mpy = np.array(
            [
                mph * total_houses / years if i < years else 0.0
                for i in range(timeframe)
            ]
        )
    elif building_scenario == "fast":
        mpy = [
            mph * houses_per_year_fast(total_houses, years)[i]
            if i < years
            else 0
            for i in range(timeframe)
        ]
    elif building_scenario == "slow":
        mpy = [
            mph * houses_per_year_slow(total_houses, years)[i]
            if i < years
            else 0.0
            for i in range(timeframe)
        ]
    else:
        raise ValueError("Choose building scenario normal/fast/slow")
    return mpy


def houses_per_year_fast(houses, years):
    return np.diff(
        [(houses / (years ** 0.5)) * (x) ** 0.5 for x in range(years + 1)]
    )


def houses_per_year_slow(houses, years):
    return np.diff(
        [(houses / (years ** 2)) * (x) ** 2 for x in range(years + 1)]
    )


def mass_per_house(material):
    if material == "gypsum":
        # 0.012m = 12mm of fibreboard
        volume = M2FACADE * 0.012
    else:
        volume = M2FACADE * RVALUE * MATERIALS[material]["lambda"]
    return volume * MATERIALS[material]["density"]


def transport50km(kg):
    "1000kg per truck - 50km"
    return (
        kg
        / 1000
        * 50
        * TRANSPORT_DATA[TRANSPORT_DATA["Name"] == MATERIALS["truck"]["name"]][
            ["CO2", "CH4", "N2O", "CO"]
        ]
        .reset_index(drop=True)
        .loc[0]
    )


def CO2bio(material, mpy, timeframe):
    CO2bio_per_year = np.zeros(len(mpy) + MATERIALS[material]["rotation"])
    for i, kg in enumerate(mpy):
        for j in range(MATERIALS[material]["rotation"]):
            CO2bio_per_year[i + j + 1] += (
                kg
                * MATERIALS[material]["CO2bio"]
                / MATERIALS[material]["rotation"]
            )
    return CO2bio_per_year[:timeframe]

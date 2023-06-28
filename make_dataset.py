import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CURRENT_YEAR = 2023
M2FACADE = 4  # placeholder
RVALUE = 3.5  # placeholder
MATERIALS = {
    "cellulose": {  # Ecoinvent
        "name": "Cellulose fibre, inclusive blowing in {CH}| production | Cut-off, S",
        "lambda": 0.038,
        "density": 52,
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "Biowaste {CH}| treatment of biowaste, industrial composting | Cut-off, S",
            "Biowaste {CH}| treatment of biowaste by anaerobic digestion | Cut-off, S",
            "Biowaste {CH}| treatment of, municipal incineration with fly ash extraction | Cut-off, S",
        ],
    },
    "cork": {  # Ecoinvent
        "name": "Cork slab {RER}| production | Cut-off, S",
        "lambda": 0.04,  # placeholder
        "density": 100,  # placeholder
        "CO2bio": -0.496,
        "rotation": 11,
        "lifetime": 50,
        "waste": [
            "Biowaste {CH}| treatment of biowaste, industrial composting | Cut-off, S",
            "Biowaste {CH}| treatment of biowaste by anaerobic digestion | Cut-off, S",
            "Biowaste {CH}| treatment of, municipal incineration with fly ash extraction | Cut-off, S",
        ],
    },
    "flax": {
        "name": "",
        "lambda": 0.04,  # placeholder
        "density": 40,
        "CO2bio": -0.44,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "Biowaste {CH}| treatment of biowaste, industrial composting | Cut-off, S",
            "Biowaste {CH}| treatment of biowaste by anaerobic digestion | Cut-off, S",
            "Biowaste {CH}| treatment of, municipal incineration with fly ash extraction | Cut-off, S",
        ],
    },
    "hemp": {
        "name": "",
        "lambda": 0.041,
        "density": 36,
        "CO2bio": -0.44,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "Biowaste {CH}| treatment of biowaste, industrial composting | Cut-off, S",
            "Biowaste {CH}| treatment of biowaste by anaerobic digestion | Cut-off, S",
            "Biowaste {CH}| treatment of, municipal incineration with fly ash extraction | Cut-off, S",
        ],
    },
    "straw": {  # Ecoinvent
        "name": "Straw {CH}| wheat production, Swiss integrated production, extensive | Cut-off, S",
        "lambda": 0.44,
        "density": 100,
        "CO2bio": -0.368,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "Biowaste {CH}| treatment of biowaste, industrial composting | Cut-off, S",
            "Biowaste {CH}| treatment of biowaste by anaerobic digestion | Cut-off, S",
            "Biowaste {CH}| treatment of, municipal incineration with fly ash extraction | Cut-off, S",
        ],
    },
    "glass wool": {  # Ecoinvent
        "name": "Glass wool mat {CH}| production | Cut-off, S",
        "lambda": 0.036,
        "density": 22,
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "Waste mineral wool {Europe without Switzerland}| market for waste mineral wool | Cut-off, S",
            "Waste mineral wool {Europe without Switzerland}| treatment of waste mineral wool, collection for final disposal | Cut-off, S",
            "Waste mineral wool, for final disposal {Europe without Switzerland}| treatment of waste mineral wool, inert material landfill | Cut - off, S",
        ],
    },
    "stone wool": {  # Ecoinvent
        "name": "Stone wool {CH}| stone wool production | Cut-off, S",
        "lambda": 0.036,
        "density": 29.5,
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "Waste mineral wool {Europe without Switzerland}| market for waste mineral wool | Cut-off, S",
            "Waste mineral wool {Europe without Switzerland}| treatment of waste mineral wool, collection for final disposal | Cut-off, S",
            "Waste mineral wool, for final disposal {Europe without Switzerland}| treatment of waste mineral wool, inert material landfill | Cut - off, S",
        ],
    },
    "XPS": {  # Ecoinvent
        "name": "Polystyrene, extruded {RER}| polystyrene production, extruded, CO2 blown | Cut-off, S",
        "lambda": 0.033,
        "density": 40,  # placeholder
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "Waste polystyrene {Europe without Switzerland}| market for waste polystyrene | Cut-off, S",
            "Waste expanded polystyrene {CH}| treatment of, municipal incineration | Cut-off, S",
            "Waste polystyrene {Europe without Switzerland}| treatment of waste polystyrene, sanitary landfill | Cut-off, S",
        ],
    },
}

MATERIAL_DATA = pd.read_csv("data/ecoinvent_material.csv", sep=";")
MATERIAL_DATA[["CO2-eq", "CO2", "CH4", "N2O", "CO"]] = MATERIAL_DATA[
    ["CO2-eq", "CO2", "CH4", "N2O", "CO"]
].apply(lambda x: x.str.replace(",", ".").astype(float))

WASTE_DATA = pd.read_csv("data/ecoinvent_waste.csv", sep=";")


def make_datasets(
    materials=["straw", "cellulose", "glass wool", "stone wool", "XPS"],
    building_scenario="normal",
    total_houses=150000,
    time_horizon=2050,
    timeframe=200,
):
    dataset = {}
    for material in materials:
        df = make_dataset(
            material, building_scenario, total_houses, time_horizon, timeframe
        )
        dataset[material] = df
    return dataset


def make_dataset(
    material,
    building_scenario,
    total_houses=150000,
    time_horizon=2050,
    timeframe=200,
):
    if material not in MATERIALS.keys():
        raise ValueError("Material not supported")

    years = time_horizon - CURRENT_YEAR
    mass_per_house = insulation_per_house(material)

    if building_scenario == "normal":
        insulation_per_year = np.array(
            [
                mass_per_house * total_houses / years if i < years else 0.0
                for i in range(timeframe)
            ]
        )
    elif building_scenario == "fast":
        insulation_per_year = [
            mass_per_house * houses_per_year_fast(total_houses, years)[i]
            if i < years
            else 0
            for i in range(timeframe)
        ]
    elif building_scenario == "slow":
        insulation_per_year = [
            mass_per_house * houses_per_year_slow(total_houses, years)[i]
            if i < years
            else 0.0
            for i in range(timeframe)
        ]
    else:
        raise ValueError("Choose building scenario normal/fast/slow")

    dataset = pd.DataFrame(
        (
            MATERIAL_DATA[
                MATERIAL_DATA["Name"] == MATERIALS[material]["name"]
            ][["CO2", "CH4", "N2O", "CO"]]
            .reset_index(drop=True)
            .loc[[0 for i in range(timeframe)]]
            .multiply(insulation_per_year, axis=0)
        )
    )
    dataset["CO2bio"] = CO2bio(
        material,
        insulation_per_year,
        MATERIALS[material]["lifetime"],
        timeframe,
    )

    # TBD how EoL works
    # dataset["BiogenicPulse"] = np.append(
    #     np.zeros(MATERIALS[material]["lifetime"]),
    #     [i * MATERIALS[material]["CO2bio"] for i in insulation_per_year],
    # )[:timeframe]

    return dataset  # .iloc[:timeframe].reset_index(drop=True)


def houses_per_year_fast(houses, years):
    return np.diff(
        [(houses / (years ** 0.5)) * (x + 1) ** 0.5 for x in range(years)],
        prepend=0,
    )


def houses_per_year_slow(houses, years):
    return np.diff(
        [(houses / (years ** 2)) * (x + 1) ** 2 for x in range(years)],
        prepend=0,
    )


def insulation_per_house(material):
    volume = M2FACADE * RVALUE * MATERIALS[material]["lambda"]
    return volume * MATERIALS[material]["density"]


def CO2bio(material, insulation_per_year, lifetime, timeframe):
    CO2bio_per_year = np.zeros(
        len(insulation_per_year) + MATERIALS[material]["rotation"]
    )
    for i, kg in enumerate(insulation_per_year):
        for j in range(MATERIALS[material]["rotation"]):
            CO2bio_per_year[i + j] += (
                kg
                * MATERIALS[material]["CO2bio"]
                / MATERIALS[material]["rotation"]
            )
    return CO2bio_per_year[:timeframe]


def plot(
    material="cellulose",
    GHG="CO2",
    houses=150000,
    time_horizon=2050,
    scenario="normal",
):
    plt.plot(
        np.arange(time_horizon - 2023) + 2023,
        make_dataset(material, scenario, houses, time_horizon)["kg " + GHG],
    )
    plt.xlabel("Years")
    plt.ylabel("kg " + GHG)
    plt.title("Emissions per Year")
    plt.grid(True)
    plt.show()

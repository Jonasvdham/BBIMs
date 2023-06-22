import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CURRENT_YEAR = 2023
INSULATION_PER_HOUSE_KG = 1000
M2FACADE = 4  # placeholder
RVALUE = 4.5  # placeholder
MATERIALS = {
    "cellulose": {
        "name": "Cellulose fibre. inclusive blowing in {GLO}| market for | Cut-off. S",
        "lambda": 0.038,
        "density": 52,
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
    },
    "cork": {
        "name": "Cork slab {GLO}| market for | Cut-off. S",
        "lambda": 0.04,  # placeholder
        "density": 100,  # placeholder
        "CO2bio": -0.496,
        "rotation": 11,
        "lifetime": 50,
    },
    "flax": {
        "name": "",
        "lambda": 0.04,  # placeholder
        "density": 40,
        "CO2bio": -0.44,
        "rotation": 1,
        "lifetime": 50,
    },
    "hemp": {
        "name": "",
        "lambda": 0.041,
        "density": 36,
        "CO2bio": -0.44,
        "rotation": 1,
        "lifetime": 50,
    },
    "straw": {
        "name": "",
        "lambda": 0.44,
        "density": 100,
        "CO2bio": -0.368,
        "rotation": "1",
        "lifetime": 50,
    },
    "glass wool": {
        "name": "Glass wool mat {GLO}| market for | Cut-off. S",
        "lambda": 0.036,
        "density": 22,
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
    },
    "stone wool": {
        "name": "Stone wool {GLO}| market for stone wool | Cut-off. S",
        "lambda": 0.036,
        "density": 29.5,
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
    },
    "XPS": {
        "name": "Polystyrene. extruded {GLO}| market for | Cut-off. S",
        "lambda": 0.033,
        "density": 40,  # placeholder
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
    },
}

insulation = pd.read_csv(
    "data/Ecoinvent.tsv",
    sep="\t",
    skiprows=(lambda x: x > 0 and (x < 3086 or x > 3143)),
)
insulation = insulation[insulation["type"] == "Market"]


def make_datasets(
    materials=["cellulose", "cork", "glass wool", "stone wool", "XPS"],
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
    mass_per_house = insul_per_house(material)

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
            insulation[insulation["Name"] == MATERIALS[material]["name"]][
                ["kg CO2", "kg CH4", "kg N2O", "kg CO"]
            ]
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

    return dataset.iloc[:timeframe].reset_index(drop=True)


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


def insul_per_house(material):
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

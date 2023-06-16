import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CURRENT_YEAR = 2023
INSULATION_PER_HOUSE_KG = 1000
MATERIALS = {
    "cellulose": {
        "name": "Cellulose fibre. inclusive blowing in {GLO}| market for | Cut-off. S",
        "CO2bio": -0,
        "amount": 1000,
        "rotation": 1,
        "lifetime": 30,
    },
    "cork": {
        "name": "Cork slab {GLO}| market for | Cut-off. S",
        "CO2bio": -0.496,
        "amount": 1000,
        "rotation": 11,
        "lifetime": 30,
    },
    "flax": {
        "name": "",
        "CO2bio": -0.44,
        "amount": 1000,
        "rotation": "0.5",
        "lifetime": 30,
    },
    "hemp": {
        "name": "",
        "CO2bio": -0.44,
        "amount": 1000,
        "rotation": "0.5",
        "lifetime": 30,
    },
    "straw": {
        "name": "",
        "CO2bio": -0.368,
        "amount": 1000,
        "rotation": "0.5",
        "lifetime": 30,
    },
    "glass wool": {
        "name": "Glass wool mat {GLO}| market for | Cut-off. S",
        "CO2bio": -0,
        "amount": 1000,
        "rotation": 1,
        "lifetime": 30,
    },
    "stone wool": {
        "name": "Stone wool {GLO}| market for stone wool | Cut-off. S",
        "CO2bio": -0,
        "amount": 1000,
        "rotation": 1,
        "lifetime": 30,
    },
    "XPS": {
        "name": "Polystyrene. extruded {GLO}| market for | Cut-off. S",
        "CO2bio": -0,
        "amount": 1000,
        "rotation": 1,
        "lifetime": 30,
    },
}


insulation = pd.read_csv(
    "data/Ecoinvent.tsv",
    sep="\t",
    skiprows=(lambda x: x > 0 and (x < 3086 or x > 3143)),
)
insulation = insulation[insulation["type"] == "Market"]


def make_dataset(
    material,
    building_scenario,
    total_houses=150000,
    time_horizon=2050,
    timeframe=200,
    outfile=None,
):
    years = time_horizon - CURRENT_YEAR
    if building_scenario == "normal":
        insulation_per_year = np.array(
            [
                INSULATION_PER_HOUSE_KG * total_houses / years
                if i < years
                else 0
                for i in range(timeframe)
            ]
        )
    elif building_scenario == "fast":
        insulation_per_year = [
            INSULATION_PER_HOUSE_KG
            * houses_per_year_fast(total_houses, years)[i]
            if i < years
            else 0
            for i in range(timeframe)
        ]
    elif building_scenario == "slow":
        insulation_per_year = [
            INSULATION_PER_HOUSE_KG
            * houses_per_year_slow(total_houses, years)[i]
            if i < years
            else 0
            for i in range(timeframe)
        ]
    else:
        raise ValueError("Choose building scenario normal/fast/slow")
    if material not in MATERIALS.keys():
        raise ValueError("Material not supported")
    else:
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
        dataset = pd.DataFrame(
            np.zeros((MATERIALS[material]["lifetime"], 4)),
            columns=dataset.columns,
        ).append(dataset, ignore_index=True)
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


def CO2bio(material, insulation_per_year, lifetime, timeframe):
    CO2bio_per_year = np.zeros(
        len(insulation_per_year) + MATERIALS[material]["rotation"] + lifetime
    )
    for i, kg in enumerate(insulation_per_year):
        for j in range(MATERIALS[material]["rotation"]):
            CO2bio_per_year[i + j] += (
                kg
                * MATERIALS[material]["CO2bio"]
                / MATERIALS[material]["rotation"]
            )
    return CO2bio_per_year[: timeframe + lifetime]


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

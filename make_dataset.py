import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CURRENT_YEAR = 2023
M2FACADE = 4  # placeholder
RVALUE = 3.5  # placeholder
BUILDING_LIFETIME = 75
MATERIALS = {
    "test": {
        "name": "test",
        "lambda": 0.05,
        "density": 50,
        "CO2bio": -100,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "Biowaste {CH}| treatment of biowaste, industrial composting | Cut-off, S"
        ],
    },
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
    "EPS": {  # Ecoinvent
        "name": "Polystyrene foam slab {CH}| production, 45% recycled | Cut-off, S",
        "lambda": 0.035,
        "density": 30,
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "Waste polystyrene {Europe without Switzerland}| market for waste polystyrene | Cut-off, S",
            "Waste expanded polystyrene {CH}| treatment of, municipal incineration | Cut-off, S",
            "Waste polystyrene {Europe without Switzerland}| treatment of waste polystyrene, sanitary landfill | Cut-off, S",
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
WASTE_DATA[["CO2-eq", "CO2", "CH4", "N2O", "CO"]] = WASTE_DATA[
    ["CO2-eq", "CO2", "CH4", "N2O", "CO"]
].apply(lambda x: x.str.replace(",", ".").astype(float))

ENERGY_DATA = pd.read_csv("data/ecoinvent_energy.csv", sep=";")
ENERGY_DATA[["CO2-eq", "CO2", "CH4", "N2O", "CO"]] = ENERGY_DATA[
    ["CO2-eq", "CO2", "CH4", "N2O", "CO"]
].apply(lambda x: x.str.replace(",", ".").astype(float))


def make_datasets(
    materials=["straw", "cellulose", "glass wool", "stone wool", "EPS", "XPS"],
    building_scenario="normal",
    total_houses=150000,
    time_horizon=2050,
    timeframe=200,
    waste_scenario=0,
):
    dataset = {}
    for material in materials:
        df = make_dataset(
            material,
            building_scenario,
            total_houses,
            time_horizon,
            timeframe,
            waste_scenario,
        )
        dataset[material] = df
    return dataset


def make_dataset(
    material="straw",
    building_scenario="normal",
    total_houses=150000,
    time_horizon=2050,
    timeframe=200,
    waste_scenario=0,
):
    if material not in MATERIALS.keys():
        raise ValueError("Material not supported")

    mass_per_house = insulation_per_house(material)
    ipy = insulation_per_year(
        building_scenario,
        mass_per_house,
        total_houses,
        time_horizon - CURRENT_YEAR,
        timeframe,
    )
    no_replacements = int(
        np.ceil(BUILDING_LIFETIME / MATERIALS[material]["lifetime"]) - 1
    )
    waste_emissions = WASTE_DATA[
        WASTE_DATA["Name"] == MATERIALS[material]["waste"][waste_scenario]
    ][["CO2", "CH4", "N2O", "CO"]].iloc[0]

    construction_emissions = construction(
        material, timeframe, ipy, no_replacements
    )
    replacement_emissions = replacement(
        material, timeframe, ipy, no_replacements, waste_emissions
    )
    demolition_emissions = demolition(
        material, timeframe, ipy, waste_emissions
    )
    return (
        construction_emissions + replacement_emissions + demolition_emissions
    )


def construction(material, timeframe, ipy, no_replacements):
    dataset = pd.DataFrame(
        (
            MATERIAL_DATA[
                MATERIAL_DATA["Name"] == MATERIALS[material]["name"]
            ][["CO2", "CH4", "N2O", "CO"]]
            .reset_index(drop=True)
            .loc[[0 for i in range(timeframe)]]
            .multiply(ipy, axis=0)
        )
    )
    dataset["CO2"] += CO2bio(
        material, ipy, MATERIALS[material]["lifetime"], timeframe
    )

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


def replacement(material, timeframe, ipy, no_replacements, waste_emissions):
    dataset = pd.DataFrame(
        np.zeros((timeframe, 4)), columns=["CO2", "CH4", "N2O", "CO"]
    )
    for j in range(no_replacements):
        for i in range(timeframe):
            dataset.loc[i + MATERIALS[material]["lifetime"] * (j + 1)] = (
                waste_emissions * ipy[i]
            )

    return dataset[:timeframe]


def demolition(material, timeframe, ipy, waste_emissions):
    dataset = pd.DataFrame(
        np.zeros((timeframe, 4)), columns=["CO2", "CH4", "N2O", "CO"]
    )
    for i in range(timeframe):
        dataset.loc[i + BUILDING_LIFETIME] = waste_emissions * ipy[i]
    return dataset[:timeframe]


def insulation_per_year(
    building_scenario, mass_per_house, total_houses, years, timeframe
):
    if building_scenario == "normal":
        ipy = np.array(
            [
                mass_per_house * total_houses / years if i < years else 0.0
                for i in range(timeframe)
            ]
        )
    elif building_scenario == "fast":
        ipy = [
            mass_per_house * houses_per_year_fast(total_houses, years)[i]
            if i < years
            else 0
            for i in range(timeframe)
        ]
    elif building_scenario == "slow":
        ipy = [
            mass_per_house * houses_per_year_slow(total_houses, years)[i]
            if i < years
            else 0.0
            for i in range(timeframe)
        ]
    else:
        raise ValueError("Choose building scenario normal/fast/slow")
    return ipy


def houses_per_year_fast(houses, years):
    return np.diff(
        [(houses / (years ** 0.5)) * (x) ** 0.5 for x in range(years + 1)]
    )


def houses_per_year_slow(houses, years):
    return np.diff(
        [(houses / (years ** 2)) * (x) ** 2 for x in range(years + 1)]
    )


def insulation_per_house(material):
    volume = M2FACADE * RVALUE * MATERIALS[material]["lambda"]
    return volume * MATERIALS[material]["density"]


def CO2bio(material, ipy, lifetime, timeframe):
    CO2bio_per_year = np.zeros(len(ipy))
    for i in range(len(ipy)):
        CO2bio_per_year[i] += ipy[i] * MATERIALS[material]["CO2bio"]
    return CO2bio_per_year


def hpy(houses=150000, years=27, plottype="inst", outfile=False):
    if plottype == "inst":
        slow = houses_per_year_slow(houses, years)
        fast = houses_per_year_fast(houses, years)
        normal = [houses / years for i in range(years)]
        title = "Number of houses constructed per year"
        x = np.arange(years) + 2023
    else:
        slow = [(houses / (years ** 2)) * x ** 2 for x in range(years + 1)]
        fast = [(houses / (years ** 0.5)) * x ** 0.5 for x in range(years + 1)]
        normal = [i * houses / years for i in range(years + 1)]
        title = "Total number of houses constructed"
        x = np.arange(years + 1) + 2023
    plt.plot(x, slow, label="slow")
    plt.plot(x, fast, label="fast")
    plt.plot(x, normal, label="normal")
    plt.legend()
    plt.title(title)
    plt.grid(True)

    if outfile:
        plt.savefig(f"plots/houses_per_year.svg")
    else:
        plt.show()
    plt.close()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CURRENT_YEAR = 2023
INSULATION_PER_HOUSE_KG = 1000
# Check dots/commas from tsv file
MATERIALS = {
    "cellulose": {
        "name": "Cellulose fibre. inclusive blowing in {GLO}| market for | Cut-off. S",
        "CO2bio": 0,
        "amount": 1000,
    },
    "cork": {
        "name": "Cork slab {GLO}| market for | Cut-off. S",
        "CO2bio": 0.496,
        "amount": 1000,
    },
    "flax": {"name": "", "CO2bio": 0.44, "amount": 1000},
    "hemp": {"name": "", "CO2bio": 0.44, "amount": 1000},
    "straw": {"name": "", "CO2bio": 0.368, "amount": 1000},
    "glass wool": {
        "name": "Glass wool mat {GLO}| market for | Cut-off. S",
        "CO2bio": 0,
        "amount": 1000,
    },
    "stone wool": {
        "name": "Stone wool {GLO}| market for stone wool | Cut-off. S",
        "CO2bio": 0,
        "amount": 1000,
    },
    "XPS": {
        "name": "Polystyrene. extruded {GLO}| market for | Cut-off. S",
        "CO2bio": 0,
        "amount": 1000,
    },
}


insulation = pd.read_csv(
    "data/Ecoinvent.tsv",
    sep="\t",
    skiprows=(lambda x: x > 0 and (x < 3086 or x > 3143)),
)

# Type == Transformation or Market - is this new vs retrofit?
# insulation = insulation[(insulation["Process"] == "Insulation") & (insulation["Type"] == "Market")]
insulation = insulation[insulation["type"] == "Market"]


def make_dataset(
    material,
    building_scenario,
    total_houses=150000,
    time_horizon=2050,
    outfile=None,
):
    years = time_horizon - CURRENT_YEAR
    if building_scenario == "normal":
        insulation_per_year = np.array(
            [
                INSULATION_PER_HOUSE_KG * total_houses / years
                for i in range(years)
            ]
        )
    elif building_scenario == "fast":
        insulation_per_year = [
            INSULATION_PER_HOUSE_KG * x
            for x in houses_per_year_fast(total_houses, years)
        ]
    elif building_scenario == "slow":
        insulation_per_year = [
            INSULATION_PER_HOUSE_KG * x
            for x in houses_per_year_slow(total_houses, years)
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
                .loc[[0 for i in range(years)]]
                .multiply(insulation_per_year, axis=0)
            )
        )
        dataset["CO2bio"] = [
            MATERIALS[material]["CO2bio"] * kg for kg in insulation_per_year
        ]
    return dataset


def houses_per_year_slow(houses, years):
    n = 3 * houses / (years ** 3)
    return [
        slow_primitive(n, i + 1) - slow_primitive(n, i) for i in range(years)
    ]


def houses_per_year_fast(houses, years):
    n = 3 * houses / (2 * (years ** (3 / 2)))
    return [
        fast_primitive(n, i + 1) - fast_primitive(n, i) for i in range(years)
    ]


def slow_primitive(n, x):
    return n / 3 * (x ** 3)


def fast_primitive(n, x):
    return 2 * n / 3 * (x ** (3 / 2))


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

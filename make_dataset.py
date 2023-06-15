import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CURRENT_YEAR = 2023
INSULATION_PER_UNIT_KG = 1000
MATERIAL_NAMES = {
    "cellulose": "Cellulose fibre. inclusive blowing in {GLO}| market for | Cut-off. S",
    "cork": "Cork slab {GLO}| market for | Cut-off. S",
    "glass wool": "Glass wool mat {GLO}| market for | Cut-off. S",
    "stone wool": "Stone wool {GLO}| market for stone wool | Cut-off. S",
    "XPS": "Polystyrene. extruded {GLO}| market for | Cut-off. S",
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
                INSULATION_PER_UNIT_KG * total_houses / years
                for i in range(years)
            ]
        )
    elif building_scenario == "fast":
        insulation_per_year = [
            INSULATION_PER_UNIT_KG * x
            for x in houses_per_year_fast(total_houses, years)
        ]
    elif building_scenario == "slow":
        insulation_per_year = [
            INSULATION_PER_UNIT_KG * x
            for x in houses_per_year_slow(total_houses, years)
        ]
    else:
        raise ValueError("Choose building scenario normal/fast/slow")
    if material not in MATERIAL_NAMES.keys():
        raise ValueError("Material not supported")
    else:
        dataset = pd.DataFrame(
            (
                insulation[insulation["Name"] == MATERIAL_NAMES[material]][
                    ["kg CO2", "kg CH4", "kg N2O", "kg CO"]
                ]
                .reset_index(drop=True)
                .loc[[0 for i in range(years)]]
                .multiply(insulation_per_year, axis=0)
            )
        )
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

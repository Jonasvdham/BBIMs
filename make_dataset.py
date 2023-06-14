import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CURRENT_YEAR = 2023
INSULATION_PER_UNIT_KG = 1000

insulation = pd.read_csv(
    "data/Ecoinvent.tsv",
    sep="\t",
    skiprows=(lambda x: x > 0 and (x < 3086 or x > 3143)),
)

# Type == Transformation or Market - is this new vs retrofit?
# insulation = insulation[(insulation["Process"] == "Insulation") & (insulation["Type"] == "Market")]

material_names = {
    "cellulose": "Cellulose fibre, inclusive blowing in {GLO}| market for | Cut-off, S",
    "cork": "Cork slab {GLO}| market for | Cut-off, S",
    "glass wool": "Glass wool mat {GLO}| market for | Cut-off, S",
    "stone wool": "Stone wool {GLO}| market for stone wool | Cut-off, S",
    "XPS": "Polystyrene, extruded {GLO}| market for | Cut-off, S",
}


def make_dataset(
    material,
    building_scenario,
    time_horizon=2050,
    total_houses=100000,
    outfile=None,
):
    years = time_horizon - CURRENT_YEAR
    # dataset = pd.DataFrame(
    #     index=range(years), columns=["CO2", "CH4", "CO", "N2O", "CO2bio"]
    # )
    if building_scenario == "normal":
        insulation_per_year = np.array(
            [
                INSULATION_PER_UNIT_KG * total_houses / years
                for i in range(years)
            ]
        )
    elif building_scenario == "fast":
        insulation_per_year = np.diff(
            [
                INSULATION_PER_UNIT_KG
                * houses_built_per_year(i, total_houses, years)
                for i in range(years)
            ],
            prepend=0,
        )
    elif building_scenario == "slow":
        pass
    else:
        raise ValueError("Choose building scenario normal/fast/slow")
    if material not in material_names.keys():
        raise ValueError("Material not supported")
    else:
        print(years, len(insulation_per_year))
        dataset = pd.DataFrame(
            (
                insulation[insulation["Name"] == material_names[material]][
                    ["kg CO2", "kg CH4", "kg N2O", "kg CO"]
                ]
                .reset_index(drop=True)
                .loc[[0 for i in range(years)]]
                .multiply(insulation_per_year, axis=0)
            )
        )
    return dataset


def sigmoid(x, A, B, C, D):
    return A / (1 + np.exp(-B * (x - C))) + D


def houses_per_year_slow(houses, years):
    # quadratic: n * x² -> n/3x³
    n = 3 * houses / (years ** 3)
    print(n)
    return [n / 3 * ((i + 1) ** 3) - n / 3 * (i ** 3) for i in range(years)]


def houses_per_year_fast(houses, years):
    # square root: n * sqrt(x) -> 2n/3x^(3/2)
    n = houses / (2 / 3) * (years ** 3 / 2)
    print(n)
    return [
        n * 2 / (3 * ((i + 1) ** (3 / 2)) - n * 2 / 3 * (i ** (3 / 2)))
        for i in range(years)
    ]


def plot(GHG):
    plt.plot(np.arange(27) + 2023, df[GHG])
    plt.xlabel("Years")
    plt.ylabel(GHG)
    plt.title("Emissions per Year")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Code to be executed if the script is run from the command line
    print("This script is being run from the command line.")

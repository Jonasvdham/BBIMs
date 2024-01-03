import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from DLCA import DLCA


def demonstrate(timeframe=200, plottype="inst_tot", outfile=False):
    dataset = dummy_data(timeframe)
    GWIs = DLCA(
        dataset.keys(),
        building_scenario="normal",
        total_houses=1,
        time_horizon=2024,
        timeframe=timeframe,
        waste_scenario=0,
        dataset=dataset,
    )

    plot_GWI(
        GWIs,
        dataset.keys(),
        timeframe=timeframe,
        plottype=plottype,
        dataset=dataset,
        outfile=outfile,
    )
    return GWIs


def dummy_data(timeframe):
    dataset = {}
    data = np.zeros((timeframe, 4))
    data[0, 0] = 1
    df = pd.DataFrame(data, columns=["CO2", "CH4", "N2O", "CO"])
    dataset["1kgCO2"] = df

    data = np.zeros((timeframe, 4))
    data[0, 0] = 10
    df = pd.DataFrame(data, columns=["CO2", "CH4", "N2O", "CO"])
    dataset["10kgCO2"] = df

    data = np.zeros((timeframe, 4))
    data[:70, [0]] = -1 / 7
    data[69, 0] = 10
    df = pd.DataFrame(data, columns=["CO2", "CH4", "N2O", "CO"])

    dataset["10kgCO2_storage"] = df

    return dataset


def plot_GWI(
    GWIs,
    materials=[
        "stone wool",
        "glass wool",
        "EPS",
        "XPS",
        "cellulose",
        "wood fiber",
        "straw",
        "grass",
        "hemp",
        "flax",
        "gypsum",
    ],
    building_scenario="normal",
    total_houses=1,
    time_horizon=2024,
    timeframe=200,
    waste_scenario=0,
    dataset=None,
    plottype="inst_tot",
    outfile=False,
):
    EoL = ["Incineration", "Biogas"]

    x = np.arange(timeframe) + 2023
    plt.figure(figsize=(8, 6))
    for material in GWIs.keys():
        plt.plot(x, GWIs[material][plottype])  # , **FORMATTING[material])

    plt.xlabel("Year")
    if plottype == "cum":
        plt.ylabel(r"Cumulative radiative forcing $(Wm^{-2}yr)$")
    else:
        plt.ylabel(r"Radiative forcing $(Wm^{-2})$")
    plt.grid(True)
    plt.legend(dataset.keys())
    if outfile:
        plt.savefig(
            f"plots/{total_houses}housesby{time_horizon}_{plottype}_{building_scenario}_{EoL[waste_scenario]}.pdf",
            bbox_inches="tight",
        )

    else:
        plt.show()

    plt.close()


def generate_plots(outfile=False):
    for scenario in [
        (592, 2024, ["normal"]),
        (97500, 2050, ["slow", "normal", "fast"]),
    ]:
        for plottype in ["cum", "inst_tot"]:
            for waste_scenario in [0, 1]:
                for building_scenario in scenario[2]:
                    plot_GWI(
                        [
                            "stone wool",
                            "glass wool",
                            "EPS",
                            "XPS",
                            "cellulose",
                            "wood fiber",
                            "straw",
                            "grass",
                            "hemp",
                            "flax",
                            "gypsum",
                        ],
                        building_scenario,
                        scenario[0],
                        scenario[1],
                        200,
                        waste_scenario,
                        plottype,
                        outfile,
                    )


if __name__ == "__main__":
    generate_plots(True)
from DLCA import DLCA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from make_dataset import MATERIALS


def plot_GWI(
    materials=[
        "straw",
        "hemp",
        "flax",
        "EPS",
        "XPS",
        "stone wool",
        "glass wool",
        "gypsum",
    ],
    building_scenario="normal",
    total_houses=1,
    time_horizon=2024,
    timeframe=200,
    waste_scenario=0,
    plottype="inst_tot",
    outfile=False,
):
    GWIs = DLCA(
        materials,
        building_scenario,
        total_houses,
        time_horizon,
        timeframe,
        waste_scenario,
    )
    x = np.arange(timeframe) + 2023
    color = iter(plt.cm.rainbow(np.linspace(0, 1, len(materials))))
    for material in materials[:-1]:
        c = next(color)
        plt.plot(x, GWIs[material][plottype], label=material, c=c)
        if MATERIALS[material]["CO2bio"] != 0 and "gypsum" in materials:
            plt.plot(
                x,
                GWIs[material][plottype] + GWIs["gypsum"][plottype],
                c=c,
                linestyle="dashed",
            )
    plt.xlabel("Years")
    plt.ylabel("Radiative forcing " + plottype)
    plt.legend()
    plt.title(f"Global warming Impact ({plottype}, {building_scenario})")
    plt.grid(True)

    if outfile:
        plt.savefig(
            f"plots/{total_houses}housesby{time_horizon}_{plottype}_{building_scenario}_EoL{waste_scenario}.svg"
        )

    else:
        plt.show()

    plt.close()


def generate_plots(outfile=False):
    for scenario in [
        (1, 2024, ["normal"]),
        (150000, 2050, ["slow", "normal", "fast"]),
    ]:
        for plottype in ["cum", "inst_tot"]:
            for waste_scenario in [0, 1]:
                for building_scenario in scenario[2]:
                    plot_GWI(
                        [
                            "straw",
                            "hemp",
                            "flax",
                            "EPS",
                            "XPS",
                            "stone wool",
                            "glass wool",
                            # "gypsum",
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

from DLCA import DLCA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from constants import MATERIALS, FORMATTING
from datetime import datetime


def plot_GWI(
    materials=[
        "stone wool",
        "glass wool",
        "EPS",
        "XPS",
        "cellulose",
        "wood fiber",
        "straw",
        "hemp",
        "flax",
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

    EoL = ["Incineration", "Biogas"]
    color = iter(plt.cm.rainbow(np.linspace(0, 1, len(GWIs.keys()))))

    x = np.arange(timeframe) + 2023
    for material in GWIs.keys():
        c = next(color)
        test = {"label": material, "c": c}
        plt.plot(x, GWIs[material][plottype], **FORMATTING[material])

    plt.xlabel("Years")
    plt.ylabel("Radiative forcing " + plottype)
    plt.legend()
    plt.title(
        f"Global warming Impact ({plottype}, {building_scenario} - EoL: {EoL[waste_scenario]})"
    )
    plt.grid(True)

    if outfile:
        plt.savefig(
            f"plots/{datetime.today().strftime('%Y-%m-%d')}_{total_houses}housesby{time_horizon}_{plottype}_{building_scenario}_{EoL[waste_scenario]}.svg"
        )

    else:
        plt.show()

    plt.close()


def generate_plots(outfile=False):
    for scenario in [
        (592, 2024, ["normal"]),
        (150000, 2050, ["slow", "normal", "fast"]),
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

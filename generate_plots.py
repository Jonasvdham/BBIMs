from DLCA import DLCA, GWPdyn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.gridspec import GridSpec
from constants import MATERIALS, M2FACADE, FORMATTING
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

    x = np.arange(timeframe) + 2023
    plt.figure(figsize=(8, 6))
    for material in GWIs.keys():
        plt.plot(x, GWIs[material][plottype], **FORMATTING[material])

    plt.plot([], [], color="grey", linestyle="--", label="Added Gypsum")

    # legend = plt.legend(
    #     bbox_to_anchor=(1.05, 1),
    #     loc=2,
    #     borderaxespad=0.0,
    #     prop={"size": 12},
    # )
    # return legend
    plt.xlabel("Year")
    if plottype == "cum":
        plt.ylabel(r"Cumulative radiative forcing $(Wm^{-2}yr)$")
    else:
        plt.ylabel(r"Radiative forcing $(Wm^{-2})$")
    plt.grid(True)

    if outfile:
        plt.savefig(
            f"plots/{total_houses}housesby{time_horizon}_{plottype}_{building_scenario}_{EoL[waste_scenario]}.pdf",
            bbox_inches="tight",
        )

    else:
        plt.show()

    plt.close()


def hpy(houses=97500, years=27, plottype="inst", outfile=False):
    slow = [(houses / (years ** 2)) * x ** 2 for x in range(years + 1)]
    fast = [(houses / (years ** 0.5)) * x ** 0.5 for x in range(years + 1)]
    normal = [i * houses / years for i in range(years + 1)]
    title = "Total number of houses constructed"
    x = np.arange(years + 1) + 2023
    if plottype == "inst":
        slow = np.diff(slow)
        fast = np.diff(fast)
        normal = np.diff(normal)
        title = "Number of houses constructed per year"
        x = np.arange(years) + 2023
    plt.plot(x, slow, label="slow")
    plt.plot(x, fast, label="fast")
    plt.plot(x, normal, label="normal")
    plt.legend()
    plt.title(title)
    plt.grid(True)

    if outfile:
        plt.savefig(f"plots/houses_per_year.pdf")
    else:
        plt.show()
    plt.close()


def export_legend(legend, filename="plots/legend.pdf", expand=[-5, -5, 5, 5]):
    fig = legend.figure
    fig.canvas.draw()
    bbox = legend.get_window_extent()
    bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi="figure", bbox_inches=bbox)


def plot_GWPdyn(
    total_houses=1 / M2FACADE, time_horizon=2024, timeframe=2223, outfile=False
):
    timerange = timeframe - 2023
    dataset = GWPdyn(total_houses, time_horizon)
    dataset = dataset[dataset["year"] < timerange]
    x = np.arange(timerange) + 2023
    for material in dataset.material.unique():
        print(material)
        plt.plot(
            x,
            dataset.loc[dataset["material"] == material, "GWPdyn"],
            **FORMATTING[material],
        )
    plt.xlabel("Year")
    plt.ylabel("GWP (kg CO2-equivalents)")

    plt.grid(True)

    if outfile:
        plt.savefig(f"plots/GWPdyn_{total_houses}_{timeframe}.pdf")

    else:
        plt.show()

    plt.close()


def generate_plots(outfile=False):
    plot_GWPdyn(outfile=outfile)
    plot_GWPdyn(97500, 2050, 2100, outfile=outfile)
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

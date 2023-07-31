from DLCA import DLCA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from make_dataset import MATERIALS
from brokenaxes import brokenaxes
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
    color = iter(plt.cm.rainbow(np.linspace(0, 1, len(materials))))

    x = np.arange(timeframe) + 2023
    for material in materials:
        if material != "gypsum":
            c = next(color)
            plt.plot(x, GWIs[material][plottype], label=material, c=c)
            if (
                MATERIALS[material]["fire_class"] != "A1"
                and "gypsum" in materials
            ):
                plt.plot(
                    x,
                    GWIs[material][plottype] + GWIs["gypsum"][plottype],
                    c=c,
                    linestyle="dashed",
                )

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


def ensemble_plot(
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
        "gypsum",
    ],
    building_scenario="normal",
    total_houses=592,
    time_horizon=2024,
    timeframe=200,
    waste_scenario=0,
    plottype="inst_tot",
    outfile=False,
):
    GWIs = [
        DLCA(
            materials,
            building_scenario,
            total_houses,
            time_horizon,
            timeframe,
            i,
        )
        for i in [0, 1]
    ]

    EoL = ["Incineration", "Biogas"]
    plottypes = ["inst_tot", "cum"]

    plt.close()
    fig = plt.figure()
    x = np.arange(timeframe) + 2023
    sps1, sps2, sps3, sps4 = GridSpec(2, 2, fig)
    subplots = [sps1, sps2, sps3, sps4]
    baxes = [
        brokenaxes(
            ylims=((-2.5e-12, -0.88e-12), (-0.4e-12, 1.8e-12)),
            hspace=0.05,
            subplot_spec=sps1,
        ),
        brokenaxes(
            ylims=((-1e-10, -0.6e-10), (-0.2e-10, 0.5e-10)),
            hspace=0.05,
            subplot_spec=sps2,
        ),
        brokenaxes(
            ylims=((-3e-12, -1.1e-12), (-0.3e-12, 0.5e-12)),
            hspace=0.05,
            subplot_spec=sps3,
        ),
        brokenaxes(
            ylims=((-3.2e-10, -2.5e-10), (-0.4e-10, 0.4e-10)),
            hspace=0.05,
            subplot_spec=sps4,
        ),
    ]

    for i in range(2):
        for j in range(2):
            color = iter(plt.cm.rainbow(np.linspace(0, 1, len(materials))))
            for material in materials:
                if material != "gypsum":
                    c = next(color)
                    baxes[i + j].plot(
                        x, GWIs[i][material][plottypes[j]], label=material, c=c
                    )
                    if (
                        MATERIALS[material]["fire_class"] != "A1"
                        and "gypsum" in materials
                    ):
                        baxes[i + j].plot(
                            x,
                            GWIs[i][material][plottypes[j]]
                            + GWIs[i]["gypsum"][plottypes[j]],
                            c=c,
                            linestyle="dashed",
                        )

    # bax.set_xlabel("Years")
    # bax.set_ylabel("Radiative forcing " + plottype)
    # bax.legend()
    # bax.set_title(
    #     f"Global warming Impact ({plottype}, {building_scenario} - EoL: {EoL[waste_scenario]})"
    # )
    # bax.grid(True)

    if outfile:
        fig.savefig(
            f"plots/{datetime.today().strftime('%Y-%m-%d')}_{total_houses}housesby{time_horizon}_{plottype}_{building_scenario}_{EoL[waste_scenario]}.svg"
        )
    else:
        fig.show()


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

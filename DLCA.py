import numpy as np
from scipy.integrate import quad
import pandas as pd
import matplotlib.pyplot as plt
from make_dataset import make_datasets, MATERIALS

"""
aCH4 - instant. radiative forcing per unit mass [W/m2 /kg]
aCO2 - instant. radiative forcing per unit mass [W/m2 /kg]
aN2O - instant. radiative forcing per unit mass [W/m2 /kg]
tauCO2 - parameters according to Bern carbon cycle-climate model
tauCH4 - lifetime (years)
tauN2O - lifetime (years)
aBern - CO2 parameters according to Bern carbon cycle-climate model
a0Bern - CO2 parameters according to Bern carbon cycle-climate model
tf - TimeFrame in years
"""

aCO2 = 1.76e-15
aCH4 = 1.28e-13
aN2O = 3.90e-13
TauCO2 = [172.9, 18.51, 1.186]
TauCH4 = 12
TauN2O = 114
aBern = [0.259, 0.338, 0.186]
a0Bern = 0.217
EMISSIONFACTOR = 1


def DLCA(
    materials=[
        "straw",
        "hemp",
        "flax",
        "EPS",
        "XPS",
        "stone wool",
        "glass wool",
    ],
    building_scenario="normal",
    total_houses=150000,
    time_horizon=2050,
    timeframe=200,
):
    dataset = make_datasets(
        materials, building_scenario, total_houses, time_horizon, timeframe
    )
    GWIs = {}
    for material in materials:
        GWI_inst = GWI(dataset[material], timeframe)
        GWI_inst_tot = GWI_inst.sum(axis=1)
        GWI_cum = GWI_inst_tot.cumsum()
        GWIs[material] = {
            "inst": GWI_inst,
            "inst_tot": GWI_inst_tot,
            "cum": GWI_cum,
        }
    return GWIs


def GWI(dataset, timeframe):
    DCF_CO2_ti, DCF_CH4_ti, DCF_N2O_ti = DCF(timeframe)
    GWI_inst = pd.DataFrame(
        np.zeros((timeframe, 3)), columns=["CO2", "CH4", "N2O"]
    )
    for t in range(timeframe):
        GWI_inst["CO2"] += (dataset["CO2"][t] + dataset["CO"][t]) * DCF_CO2_ti[
            t
        ]
        GWI_inst["CH4"] += dataset["CH4"][t] * DCF_CH4_ti[t]
        GWI_inst["N2O"] += dataset["N2O"][t] * DCF_N2O_ti[t]
    return GWI_inst


def DCF(tf):
    DCF_CO2 = [
        quad(lambda x: aCO2 * C_CO2(x), t - 1, t)[0] for t in range(1, tf + 1)
    ]
    DCF_CH4 = [
        quad(lambda x: aCH4 * C_CH4(x), t - 1, t)[0] for t in range(1, tf + 1)
    ]
    DCF_N2O = [
        quad(lambda x: aN2O * C_N2O(x), t - 1, t)[0] for t in range(1, tf + 1)
    ]

    DCF_CO2_ti = np.zeros((tf, tf))
    DCF_CH4_ti = np.zeros((tf, tf))
    DCF_N2O_ti = np.zeros((tf, tf))
    for t in range(tf):
        for i in range(t + 1):
            DCF_CO2_ti[i, t] = DCF_CO2[t - i]
            DCF_CH4_ti[i, t] = DCF_CH4[t - i]
            DCF_N2O_ti[i, t] = DCF_N2O[t - i]
    return DCF_CO2_ti, DCF_CH4_ti, DCF_N2O_ti


def C_CO2(t):
    return (
        a0Bern
        + aBern[0] * np.exp(-t / TauCO2[0])
        + aBern[1] * np.exp(-t / TauCO2[1])
        + aBern[2] * np.exp(-t / TauCO2[2])
    )


def C_CH4(t):
    return np.exp(-t / TauCH4)


def C_N2O(t):
    return np.exp(-t / TauN2O)


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
    total_houses=150000,
    time_horizon=2050,
    timeframe=200,
    plottype="inst_tot",
    outfile=False,
):
    GWIs = DLCA(
        materials, building_scenario, total_houses, time_horizon, timeframe
    )
    x = np.arange(timeframe) + 2023
    color = iter(plt.cm.rainbow(np.linspace(0, 1, len(materials))))
    for material in materials:
        c = next(color)
        plt.plot(x, GWIs[material][plottype], label=material, c=c)
        if MATERIALS[material]["CO2bio"] != 0:
            plt.plot(
                x,
                GWIs[material][plottype] + GWIs["gypsum"][plottype],
                label=material + " + gypsum",
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
            f"plots/EOL_exp_{total_houses}housesby{time_horizon}_{plottype}_{building_scenario}.svg"
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
                        "gypsum",
                    ],
                    building_scenario,
                    scenario[0],
                    scenario[1],
                    200,
                    plottype,
                    outfile,
                )

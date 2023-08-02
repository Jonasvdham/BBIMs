import numpy as np
from scipy.integrate import quad
import pandas as pd
from make_dataset import make_datasets
from constants import (
    MATERIALS,
    ACO2,
    ACH4,
    AN2O,
    TAUCO2,
    TAUCH4,
    TAUN2O,
    ABERN,
    A0BERN,
)


def DLCA(
    materials=[
        "straw",
        "hemp",
        "flax",
        "wood fiber",
        "EPS",
        "XPS",
        "stone wool",
        "glass wool",
    ],
    building_scenario="normal",
    total_houses=150000,
    time_horizon=2050,
    timeframe=200,
    waste_scenario=0,
):
    dataset = make_datasets(
        materials + ["gypsum"],
        building_scenario,
        total_houses,
        time_horizon,
        timeframe,
        waste_scenario,
    )
    for material in materials:
        if MATERIALS[material]["fire_class"] != "A1":
            dataset[material + " + gypsum"] = (
                dataset[material] + dataset["gypsum"]
            )
    del dataset["gypsum"]

    GWIs = {}
    for material in dataset.keys():
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
        quad(lambda x: ACO2 * C_CO2(x), t - 1, t)[0] for t in range(1, tf + 1)
    ]
    DCF_CH4 = [
        quad(lambda x: ACH4 * C_CH4(x), t - 1, t)[0] for t in range(1, tf + 1)
    ]
    DCF_N2O = [
        quad(lambda x: AN2O * C_N2O(x), t - 1, t)[0] for t in range(1, tf + 1)
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
        A0BERN
        + ABERN[0] * np.exp(-t / TAUCO2[0])
        + ABERN[1] * np.exp(-t / TAUCO2[1])
        + ABERN[2] * np.exp(-t / TAUCO2[2])
    )


def C_CH4(t):
    return np.exp(-t / TAUCH4)


def C_N2O(t):
    return np.exp(-t / TAUN2O)

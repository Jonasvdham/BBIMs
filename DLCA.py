import numpy as np
from scipy.integrate import quad
import pandas as pd
import matplotlib.pyplot as plt
from make_dataset import make_dataset

"""
aCH4 - instant. radiative forcing per unit mass [10^-12 W/m2 /kgCH4]
tauCH4 - lifetime (years)
aCO2 - instant. radiative forcing per unit mass [10^-12 W/m2 /kgCO2]
tauCO2 - parameters according to Bern carbon cycle-climate model
aBern - CO2 parameters according to Bern carbon cycle-climate model
a0Bern - CO2 parameters according to Bern carbon cycle-climate model
tf - TimeFrame in years
"""
aCO2 = 0.0018088
aCH4 = 0.129957
TauCO2 = [172.9, 18.51, 1.186]
TauCH4 = 12
TauNO2 = 114
aBern = [0.259, 0.338, 0.186]
a0Bern = 0.217


def DLCA(material, building_scenario, total_houses, time_horizon, time_frame):
    dataset = make_dataset(
        material, building_scenario, total_houses, time_horizon
    )
    DCF_CO2_ti, DCF_CH4_ti = DCF(time_frame)
    GWI_inst = GWI(dataset, time_frame, DCF_CO2_ti, DCF_CH4_ti)
    GWI_inst_tot = GWI_inst.sum(axis=1)
    GWI_cum = GWI_inst_tot.cumsum()
    return GWI_inst_tot, GWI_cum


def DCF(tf):
    DCF_CO2 = [
        quad(lambda x: aCO2 * C_CO2(x), t - 1, t)[0] for t in range(1, tf + 1)
    ]

    DCF_CH4 = [
        quad(lambda x: aCH4 * C_CH4(x), t - 1, t)[0] for t in range(1, tf + 1)
    ]

    DCF_CO2_ti = np.zeros((tf, tf))
    DCF_CH4_ti = np.zeros((tf, tf))
    for t in range(tf):
        for i in range(t + 1):
            DCF_CO2_ti[i, t] = DCF_CO2[t - i]
            DCF_CH4_ti[i, t] = DCF_CH4[t - i]
    return DCF_CO2_ti, DCF_CH4_ti


def GWI(dataset, timeframe, DCF_CO2_ti, DCF_CH4_ti):
    GWI_inst = pd.DataFrame(columns=["CO2", "CH4"], index=range(timeframe))
    for t in range(timeframe):
        GWI_inst["CO2"][t] = np.sum(
            (dataset["kg CO2"][t] + dataset["CO2bio"][t]) * DCF_CO2_ti[:, t]
        )
        GWI_inst["CH4"][t] = np.sum(dataset["kg CH4"][t] * DCF_CH4_ti[:, t])
    return GWI_inst


def C_CO2(t):
    return (
        a0Bern
        + aBern[0] * np.exp(-t / TauCO2[0])
        + aBern[1] * np.exp(-t / TauCO2[1])
        + aBern[2] * np.exp(-t / TauCO2[2])
    )


def C_CH4(t):
    return np.exp(-t / TauCH4)


def plot(
    material,
    building_scenario,
    total_houses,
    time_horizon,
    time_frame,
    plottype=None,
):
    inst, cum = DLCA(
        material, building_scenario, total_houses, time_horizon, time_frame
    )
    x = np.arange(time_frame)
    if plottype == "inst":
        plt.plot(x, inst)
    else:
        plt.plot(x, cum)
    plt.show()


# plot('cork', 'fast', 150000, 2050, 27, 'inst')

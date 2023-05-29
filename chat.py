import numpy as np
from scipy.integrate import quad
import pandas as pd

# General Parameters
aCH4 = (
    0.129957
)  # methane - instantaneous radiative forcing per unit mass [10^-12 W/m2 /kgCH4]
TauCH4 = 12  # methane - lifetime (years)
aCO2 = (
    0.0018088
)  # CO2 - instantaneous radiative forcing per unit mass [10^-12 W/m2 /kgCO2]
TauCO2 = [
    172.9,
    18.51,
    1.186,
]  # CO2 parameters according to Bern carbon cycle-climate model
aBern = [
    0.259,
    0.338,
    0.186,
]  # CO2 parameters according to Bern carbon cycle-climate model
a0Bern = 0.217  # CO2 parameters according to Bern carbon cycle-climate model
tf = 200  # set TimeFrame in years
Time = np.arange(tf)  # Time Vector with length = tf
Import_file = "P1_Matlab1_Input.xlsx"
Export_file = "P1_Matlab2_Output.xlsx"

# Import Excel Information
Inventory_input = pd.read_excel(
    Import_file,
    sheet_name="Matlab Values",
    usecols="D:CO",
    skiprows=4,
    nrows=112,
)
products = 5
scenario = 6 * products
Inventory = np.zeros((tf, scenario * 3))
g_length = Inventory_input.iloc[:, 1].values
glength = len(g_length)
for i in range(scenario * 3):
    for j in range(glength):
        Inventory[j, i] = Inventory_input.iloc[j, i]

# CO2 calculation formula
# time dependent atmospheric load for CO2, Bern model
def C_CO2(t):
    return (
        a0Bern
        + aBern[0] * np.exp(-t / TauCO2[0])
        + aBern[1] * np.exp(-t / TauCO2[1])
        + aBern[2] * np.exp(-t / TauCO2[2])
    )


# DCF for CO2, for tf years
DCF_CO2 = np.zeros(tf)
for t in range(1, tf + 1):
    DCF_CO2[t - 1], _ = quad(lambda x: aCO2 * C_CO2(x), t - 1, t)

# AUX-Matrix: DCF(t-i); Row = i (start at 0), Column = t (start at 1)
DCF_CO2_ti = np.zeros((tf, tf))
for t in range(tf):
    for i in range(t + 1):
        DCF_CO2_ti[i, t] = DCF_CO2[t - i]

# CH4 calculation formula
# time dependent atmospheric load for non-CO2 GHGs (Methane)
def C_CH4(t):
    return np.exp(-t / TauCH4)


# DCF for CH4 for tf years
DCF_CH4 = np.zeros(tf)
for i in range(tf):
    DCF_CH4[i], _ = quad(lambda x: aCH4 * C_CH4(x), i - 1, i)

# AUX-Matrix of DCF t-i; Row = i (start at 0), Column = t (start at 1)
DCF_CH4_ti = np.zeros((tf, tf))
for t in range(tf):
    for i in range(t + 1):
        DCF_CH4_ti[i, t] = DCF_CH4[t - i]

# Output calculation
# calculation GWI_inst
GWI_inst = np.zeros((tf, scenario * 3))
for n in range(scenario):
    for t in range(tf):
        GWI_inst[t, (1 + n * 3)] = np.sum(
            Inventory[:, (1 + n * 3)] * DCF_CO2_ti[:, t]
        )
        GWI_inst[t, (2 + n * 3)] = np.sum(
            Inventory[:, (2 + n * 3)] * DCF_CH4_ti[:, t]
        )
        GWI_inst[t, (3 + n * 3)] = np.sum(
            Inventory[:, (3 + n * 3)] * DCF_CO2_ti[:, t]
        )

# total
# GWI instantaneous - sum of all gases
# solve with matrix, 1 column = 1 scenario
GWI_inst_tot = np.zeros((tf, scenario))
for i in range(scenario):
    GWI_inst_tot[:, i] = np.sum(GWI_inst[:, (1 + i * 3) : (4 + i * 3)], axis=1)

# calculate GWI cumulative
GWI_cum = np.zeros((tf, scenario))
for i in range(scenario):
    for t in range(tf):
        GWI_cum[t, i] = np.sum(GWI_inst_tot[: t + 1, i])

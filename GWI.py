import numpy as np
from scipy.integrate import quad
import pandas as pd
import matplotlib.pyplot as plt


class GWI:
    def __init__(self):
        """
        aCH4 - instant. radiative forcing per unit mass [10^-12 W/m2 /kgCH4]
        tauCH4 - lifetime (years)
        aCO2 - instant. radiative forcing per unit mass [10^-12 W/m2 /kgCO2]
        tauCO2 - parameters according to Bern carbon cycle-climate model
        aBern - CO2 parameters according to Bern carbon cycle-climate model
        a0Bern - CO2 parameters according to Bern carbon cycle-climate model
        tf - TimeFrame in years
        time - Time Vector with length = tf
        """
        self.constants = {
            "CO2": {
                "a": 0.0018088,
                "tau": [172.9, 18.51, 1.186],
                "decay_func": self.C_CO2,
            },
            "CH4": {"a": 0.129957, "tau": 12, "decay_func": self.C_CH4},
        }
        self.aBern = [0.217, 0.259, 0.338, 0.186]
        self.tf = 200
        self.time = np.arange(self.tf)

        # tmp
        self.data = {"CO2": np.zeros(200), "CH4": np.zeros(200)}
        self.data["CO2"][0] = 1
        self.data["CH4"][0] = 1
        self.df = pd.DataFrame(self.data)

    def read_infile(self, skiprows=range(1, 3), sep=";"):
        self.df = pd.read_csv(self.infile, skiprows=skiprows, sep=sep)

    # CO2 calculation formula
    # time dependent atmospheric load for CO2, Bern model
    def C_CO2(self, t):
        return (
            self.aBern[0]
            + self.aBern[1] * np.exp(-t / self.constants["CO2"]["tau"][0])
            + self.aBern[2] * np.exp(-t / self.constants["CO2"]["tau"][1])
            + self.aBern[3] * np.exp(-t / self.constants["CO2"]["tau"][2])
        )

    # CH4 calculation formula
    # time dependent atmospheric load for non-CO2 GHGs (Methane)
    def C_CH4(self, t):
        return np.exp(-t / self.constants["CH4"]["tau"])

    def DCF(self, GHG, t):
        return quad(
            lambda x: self.constants[GHG]["a"]
            * self.constants[GHG]["decay_func"](x),
            t,
            t + 1,
        )[0]

    def GWI_inst(self, t):
        GWI_GHG = 0
        for GHG in self.constants.keys():
            for year in range(t):
                GWI_GHG += self.data[GHG][year] * self.DCF(GHG, t - year)
        return GWI_GHG

    def GWI_cum(self, t):
        tmp = 0
        for year in range(t):
            tmp += self.GWI_inst(year)
        return tmp

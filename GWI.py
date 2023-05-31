import numpy as np
from scipy.integrate import quad
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt


class GWI:
    def __init__(self, tf=100, lifetime=50, rotation_period=10):
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

        # GHG constants from Hoxha et al. 2020
        self.constants = {
            "GHGs": {
                "CO2": {
                    "a": 1.76e-15,
                    "tau": [172.9, 18.51, 1.186],
                    "decay_func": self.C_CO2,
                },
                "CH4": {"a": 1.28e-13, "tau": 12, "decay_func": self.C_CH4},
                "N2O": {"a": 3.9e-13, "tau": 114, "decay_func": self.C_CH4},
            },
            "aBern": [0.217, 0.259, 0.338, 0.186],
        }
        self.tf = tf
        self.lifetime = lifetime
        self.rotation_period = rotation_period

        # tmp
        self.data = {"CO2": np.zeros(self.tf), "CH4": np.zeros(self.tf)}
        self.data["CO2"][0] = 1
        self.data["CH4"][0] = 1
        self.df = pd.DataFrame(self.data)
        self.tmp = 0

    def read_infile(self, skiprows=range(1, 3), sep=";"):
        self.df = pd.read_csv(self.infile, skiprows=skiprows, sep=sep)

    # CO2 calculation formula
    # time dependent atmospheric load for CO2, Bern model
    def C_CO2(self, t):
        return (
            self.constants["aBern"][0]
            + self.constants["aBern"][1]
            * np.exp(-t / self.constants["GHGs"]["CO2"]["tau"][0])
            + self.constants["aBern"][2]
            * np.exp(-t / self.constants["GHGs"]["CO2"]["tau"][1])
            + self.constants["aBern"][3]
            * np.exp(-t / self.constants["GHGs"]["CO2"]["tau"][2])
        )

    # CH4 calculation formula
    # time dependent atmospheric load for non-CO2 GHGs (Methane)
    def C_CH4(self, t):
        return np.exp(-t / self.constants["GHGs"]["CH4"]["tau"])

    def DCF(self, GHG, t):
        return quad(
            lambda x: self.constants["GHGs"][GHG]["a"]
            * self.constants["GHGs"][GHG]["decay_func"](x),
            t,
            t + 1,
        )[0]

    def GWI_inst(self, t):
        GWI_GHG = 0
        for GHG in self.constants["GHGs"].keys():
            for year in range(t):
                GWI_GHG += self.data[GHG][year] * self.DCF(GHG, t - year)
        return GWI_GHG

    def GWI_cum(self, t):
        return sum([self.GWI_inst(i) for i in range(t)])

    def plot(self, lifetime, rotation_period):
        x = np.arange(self.tf)
        y = [
            self.f_total(i, lifetime, rotation_period) for i in range(self.tf)
        ]
        plt.plot(x, y)
        plt.show()

    def GWPbio(self, c0=1, lifetime=None, rotation_period=None):
        if lifetime == None:
            lifetime = self.lifetime
        if rotation_period == None:
            rotation_period = self.rotation_period

        return c0 * (
            quad(
                lambda x: self.constants["GHGs"]["CO2"]["a"]
                * self.f_total(x, lifetime, rotation_period),
                0,
                self.tf,
            )[0]
            / quad(
                lambda x: self.constants["GHGs"]["CO2"]["a"] * self.C_CO2(x),
                0,
                self.tf,
            )[0]
        )

    def f_total(self, t, lifetime, rotation_period):
        if t < lifetime:
            return -(
                quad(
                    lambda x: self.growth(x, rotation_period)
                    * self.C_CO2(t - x),
                    0,
                    t,
                )[0]
            )
        elif t == lifetime:
            self.tmp = -(
                quad(
                    lambda x: self.growth(x, rotation_period)
                    * self.C_CO2(t - x),
                    0,
                    t,
                )[0]
            )
            print(self.tmp)
            return self.tmp
        else:
            return (
                self.C_CO2(t - lifetime)
                - quad(
                    lambda x: self.growth(x, rotation_period)
                    * self.C_CO2(t - x),
                    lifetime,
                    t,
                )[0]
            )

    def growth(self, t, rotation_period):
        return norm.pdf(t, loc=rotation_period / 2, scale=rotation_period / 4)

    def AGWP(self, GHG, t):
        return quad(
            lambda x: self.constants["GHGs"][GHG]["a"]
            * self.constants["GHGs"][GHG]["decay_func"](x),
            0,
            t,
        )[0]


GWI = GWI(tf=500)

"""
    def c_CO2_vector(self, t):
        return self.constants["aBern"][0] + sum(
            [
                self.constants["aBern"][i + 1]
                * np.exp(
                    [-j / self.constants["GHGs"]["CO2"]["tau"][i] for j in t]
                )
                for i in range(3)
            ]
        )

    def c_CH4_vector(self, t):
        return np.exp([-i / self.constants["GHGs"]["CH4"]["tau"] for i in t])

"""

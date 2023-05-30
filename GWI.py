import numpy as np
from scipy.integrate import quad, cumtrapz
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt


class GWI:
    def __init__(self, tf=200):
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
            "GHGs": {
                "CO2": {
                    "a": 0.0018088,
                    "tau": [172.9, 18.51, 1.186],
                    "decay_func": self.C_CO2,
                },
                "CH4": {"a": 0.129957, "tau": 12, "decay_func": self.C_CH4},
            },
            "aBern": [0.217, 0.259, 0.338, 0.186],
        }
        self.tf = tf
        self.time = np.arange(self.tf)
        self.lifetime = 75

        # tmp
        self.data = {"CO2": np.zeros(self.tf), "CH4": np.zeros(self.tf)}
        self.data["CO2"][0] = 1
        self.data["CH4"][0] = 1
        self.df = pd.DataFrame(self.data)

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

    def plot(self, GHG):
        x = np.arange(self.tf)
        y = self.constants[GHG]["decay_func"](x)
        plt.plot(x, y)
        plt.show()

    def GWPbio(self, c0):
        # c0 - The emission pulse (kg CO2)
        return c0 * (
            quad(
                lambda x: self.constants["GHGs"]["CO2"]["a"] * self.f_total(x),
                0,
                self.tf,
            )
            / quad(
                lambda x: self.constants["GHGs"]["CO2"]["a"] * self.C_CO2(x),
                0,
                self.tf,
            )
        )

    def f_total(self, t):
        if t < self.lifetime:
            return -(
                quad(
                    lambda x: self.growth(x) * self.C_CO2(t - x),
                    0,
                    self.lifetime,
                )
            )
        else:
            return self.C_CO2(t - self.lifetime) - quad(
                lambda x: self.growth(x) * self.C_CO2(t - x), self.lifetime, t
            )

    def growth(self, t):
        return self.normal_dist(t)

    def normal_dist(x, mean=2, sd=1):
        prob_density = (np.pi * sd) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
        return prob_density


GWI = GWI()

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

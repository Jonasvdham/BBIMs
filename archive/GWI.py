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
        self.data = {
            "CO2": np.zeros(self.tf),
            "CH4": np.zeros(self.tf),
            "N2O": np.zeros(self.tf),
        }
        self.data["CO2"][0] = 1
        self.data["CH4"][0] = 1
        self.data["N2O"][0] = 1
        self.df = pd.DataFrame(self.data)
        self.tmp = 0

    def read_infile(self, skiprows=range(1, 3), sep=";"):
        self.df = pd.read_csv(self.infile, skiprows=skiprows, sep=sep)

    # CO2 calculation formula
    # time dependent atmospheric load for CO2, Bern model
    # c(x)=0.217+0.259*e^(-x/172.9)+0.338*e^(-x/18.51)+0.186*e^(-x/1.186)
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

    def DCF(self, GHG, tj, t):
        return quad(
            lambda x: self.constants["GHGs"][GHG]["a"]
            * self.constants["GHGs"][GHG]["decay_func"](x),
            tj,
            t,
        )[0]

    def GWI_inst(self, t):
        GWI_GHG = 0
        for GHG in self.constants["GHGs"].keys():
            for year in range(t):
                GWI_GHG += self.data[GHG][year] * self.DCF(
                    GHG, t - year, t + 1 - year
                )
        return GWI_GHG

    def GWI_cum(self, t):
        return sum([self.GWI_inst(i + 1) for i in range(t)])

    def GWPbio(self, c0, lifetime=None, rotation_period=None):
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

    # TODO: Check if rotation period is over
    # it seems the influence of bio-genic is stopped there
    def f_total(self, t, lifetime, rotation_period):
        if t <= rotation_period:
            if t < lifetime:
                self.tmp = -(
                    quad(
                        lambda x: self.growth(x, rotation_period)
                        * self.C_CO2(t - x),
                        0,
                        t,
                    )[0]
                )
                return self.tmp
            else:
                self.tmp2 = (
                    self.C_CO2(t - lifetime)
                    + self.tmp
                    - quad(
                        lambda x: self.growth(x, rotation_period)
                        * self.C_CO2(t - x),
                        lifetime,
                        t,
                    )[0]
                )
            return self.tmp2
        else:
            if self.tmp2 < 0:
                return -self.C_CO2(t - lifetime) + self.tmp

    def growth(self, t, rotation_period):
        return norm.pdf(t, loc=rotation_period / 2, scale=rotation_period / 4)

    def AGWP(self, GHG, t):
        return quad(
            lambda x: self.constants["GHGs"][GHG]["a"]
            * self.constants["GHGs"][GHG]["decay_func"](x),
            0,
            t,
        )[0]

    def plotftotal(self, plottype, lifetime, rotation_period):
        x = np.arange(self.tf)
        y = [
            self.f_total(i, lifetime, rotation_period) for i in range(self.tf)
        ]
        plt.plot(x, y)
        plt.show()

    def plotGWIcum(self, t):
        x = np.arange(t)
        y = [self.GWI_cum(i) for i in range(t)]
        plt.plot(x, y)
        plt.show()

    def plotGWIinst(self, t):
        x = np.arange(t)
        y = [self.GWI_inst(i) for i in range(t)]
        plt.plot(x, y)
        plt.show()


GWI = GWI(tf=500)


def test_biogenic():
    for i in range(10):
        print(10 * (i + 1), GWI.GWPbio(1, 10 * (i + 1), 10 * (i + 1)))

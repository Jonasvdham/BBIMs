import numpy as np
from scipy.integrate import quad
import pandas as pd


class GWI:
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

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

        self.aCH4 = 0.129957
        self.tauCH4 = 12
        self.aCO2 = 0.0018088
        self.tauCO2 = [172.9, 18.51, 1.186]
        self.aBern = [0.259, 0.338, 0.186]
        self.a0Bern = 0.217
        self.tf = 200
        self.time = np.arange(tf)
        self.data = {"CO2": [1.5], "CH4": [0.5]}
        self.df = pd.DataFrame(self.data)

    def read_infile(self, skiprows=range(1, 3), sep=";"):
        self.df = pd.read_csv(self.infile, skiprows=skiprows, sep=sep)

    # CO2 calculation formula
    # time dependent atmospheric load for CO2, Bern model
    def C_CO2(self, t):
        return (
            self.a0Bern
            + self.aBern[0] * np.exp(-t / self.tauCO2[0])
            + self.aBern[1] * np.exp(-t / self.tauCO2[1])
            + self.aBern[2] * np.exp(-t / self.tauCO2[2])
        )

    # CH4 calculation formula
    # time dependent atmospheric load for non-CO2 GHGs (Methane)
    def C_CH4(self, t):
        return np.exp(-t / self.tauCH4)

    def DCF_CO2(self):
        # DCF for CO2, for tf years
        DCF = np.zeros(self.tf)
        # AUX-Matrix: DCF(t-i); Row = i (start at 0), Column = t (start at 1)
        DCF_ti = np.zeros((tf, tf))
        for t in range(self.tf):
            DCF[t], _ = quad(lambda x: self.aCO2 * self.C_CO2(x), t, t + 1)
        for t in range(tf):
            for i in range(t + 1):
                DCF_ti[i, t] = DCF[t - i]
        return DCF_ti

    def DCF_CH4(self):
        # DCF for CH4, for tf years
        DCF = np.zeros(self.tf)
        # AUX-Matrix: DCF(t-i); Row = i (start at 0), Column = t (start at 1)
        DCF_ti = np.zeros((tf, tf))
        for t in range(self.tf):
            DCF[t], _ = quad(lambda x: self.aCH4 * self.C_CH4(x), t, t + 1)
        for t in range(tf):
            for i in range(t + 1):
                DCF_ti[i, t] = DCF[t - i]
        return DCF_ti

    def calc_GWI(self):
        self.GWI_inst_CO2 = self.df["CO2"] * self.DCF_CO2()
        self.GWI_inst_CH4 = self.df["CH4"] * self.DCF_CH4()
        self.GWI_inst_tot = self.GWI_inst_CO2 + self.GWI_inst_CH4
        self.GWI_cum = self.GWI_inst_tot.cumsum()
        return

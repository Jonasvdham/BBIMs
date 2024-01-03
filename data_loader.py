import pandas as pd


def load_data():
    try:
        MATERIAL_DATA = pd.read_csv("data/ecoinvent_material.csv", sep=";")
        MATERIAL_DATA[["CO2-eq", "CO2", "CH4", "N2O", "CO"]] = MATERIAL_DATA[
            ["CO2-eq", "CO2", "CH4", "N2O", "CO"]
        ].apply(lambda x: x.str.replace(",", ".").astype(float))

        WASTE_DATA = pd.read_csv("data/ecoinvent_waste.csv", sep=";")
        WASTE_DATA[["CO2-eq", "CO2", "CH4", "N2O", "CO"]] = WASTE_DATA[
            ["CO2-eq", "CO2", "CH4", "N2O", "CO"]
        ].apply(lambda x: x.str.replace(",", ".").astype(float))

        ENERGY_DATA = pd.read_csv("data/ecoinvent_energy.csv", sep=";")
        ENERGY_DATA[["CO2-eq", "CO2", "CH4", "N2O", "CO"]] = ENERGY_DATA[
            ["CO2-eq", "CO2", "CH4", "N2O", "CO"]
        ].apply(lambda x: x.str.replace(",", ".").astype(float))

        TRANSPORT_DATA = pd.read_csv("data/ecoinvent_transport.csv", sep=";")
        TRANSPORT_DATA[["CO2-eq", "CO2", "CH4", "N2O", "CO"]] = TRANSPORT_DATA[
            ["CO2-eq", "CO2", "CH4", "N2O", "CO"]
        ].apply(lambda x: x.str.replace(",", ".").astype(float))

        return MATERIAL_DATA, WASTE_DATA, ENERGY_DATA, TRANSPORT_DATA
    except:
        return None, None, None, None

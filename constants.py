"""
aCH4 - instant. radiative forcing per unit mass [W/m2 /kg]
aCO2 - instant. radiative forcing per unit mass [W/m2 /kg]
aN2O - instant. radiative forcing per unit mass [W/m2 /kg]
tauCO2 - parameters according to Bern carbon cycle-climate model
tauCH4 - lifetime (years)
tauN2O - lifetime (years)
aBern - CO2 parameters according to Bern carbon cycle-climate model
a0Bern - CO2 parameters according to Bern carbon cycle-climate model
"""
ACO2 = 1.76e-15
ACH4 = 1.28e-13
AN2O = 3.90e-13
TAUCO2 = [172.9, 18.51, 1.186]
TAUCH4 = 12
TAUN2O = 114
ABERN = [0.259, 0.338, 0.186]
A0BERN = 0.217

CURRENT_YEAR = 2023
M2FACADE = 7.6
RVALUE = 3.5
BUILDING_LIFETIME = 75

FORMATTING = {
    "cellulose": {"label": "Cellulose", "c": "#189AB4"},
    "straw": {"label": "Straw", "c": "#05445E"},
    "hemp": {"label": "Hemp", "c": "#81B622"},
    "flax": {"label": "Flax", "c": "#59981A"},
    "wood fiber": {"label": "Wood fiber", "c": "#3D550C"},
    "EPS": {"label": "EPS", "c": "#5F093D"},
    "XPS": {"label": "XPS", "c": "#B21368"},
    "stone wool": {"label": "Stone wool", "c": "#D67BA8"},
    "glass wool": {"label": "Glass wool", "c": "#EFD3B5"},
    "cellulose + gypsum": {"c": "#189AB4", "linestyle": "dashed"},
    "straw + gypsum": {"c": "#05445E", "linestyle": "dashed"},
    "hemp + gypsum": {"c": "#81B622", "linestyle": "dashed"},
    "flax + gypsum": {"c": "#59981A", "linestyle": "dashed"},
    "wood fiber + gypsum": {"c": "#3D550C", "linestyle": "dashed"},
    "EPS + gypsum": {"c": "#5F093D", "linestyle": "dashed"},
    "XPS + gypsum": {"c": "#B21368", "linestyle": "dashed"},
}
MATERIALS = {
    "truck": {
        "name": "Transport, freight, lorry 7.5-16 metric ton, EURO3 {GLO}| market for | Cut-off, S"
    },
    "gypsum": {
        "name": "Gypsum fibreboard {CH}| production | Cut-off, S",
        "plant_based": False,
        "density": 1150,  # placeholder
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "Waste gypsum plasterboard {CH}| treatment of, sorting plant | Cut-off, S",
            "Waste gypsum plasterboard {CH}| treatment of, sorting plant | Cut-off, S",
        ],
    },
    "cellulose": {  # Ecoinvent
        "name": "Cellulose fibre, inclusive blowing in {CH}| production | Cut-off, S",
        "plant_based": False,
        "lambda": 0.038,
        "fire_class": "B",
        "density": 52,
        "CO2bio": -0.404 * 44 / 12,
        "rotation": 1,
        "lifetime": 50,
        "waste": ["incineration", "incineration"],
    },
    "flax": {
        "name": "Fibre, flax {RoW}| fibre production, flax, retting | Cut-off, U",
        "plant_based": True,
        "lambda": 0.041,  # placeholder
        "fire_class": "E",
        "density": 40,
        "CO2bio": -0.44 * 44 / 12,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "incineration",
            "Biowaste {CH}| treatment of biowaste by anaerobic digestion | Cut-off, S",
            "Biowaste {CH}| treatment of biowaste, industrial composting | Cut-off, S",
            "Biowaste {CH}| treatment of, municipal incineration with fly ash extraction | Cut-off, S",
        ],
    },
    "hemp": {
        "name": "Fibre, hemp {RoW}| fibre production, hemp, retting | Cut-off, U",
        "plant_based": True,
        "lambda": 0.041,
        "fire_class": "E",
        "density": 36,
        "CO2bio": -0.377 * 44 / 12,  # from biofib'chanvre EPD
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "incineration",
            "Biowaste {CH}| treatment of biowaste by anaerobic digestion | Cut-off, S",
        ],
    },
    "wood fiber": {
        "name": "Wood wool {RER}| production | Cut-off, S",
        "plant_based": True,
        "lambda": 0.046,  # placeholder
        "fire_class": "E",
        "density": 34.5,
        "CO2bio": -0.4 * 44 / 12,  # placeholder
        "rotation": 50,  # placeholder
        "lifetime": 50,
        "waste": [
            "incineration",
            "Waste gypsum plasterboard {CH}| treatment of, sorting plant | Cut-off, S",
        ],
    },
    "straw": {  # Ecoinvent
        "name": "Straw {CH}| wheat production, Swiss integrated production, extensive | Cut-off, S",
        "plant_based": True,
        "lambda": 0.044,
        "fire_class": "E",
        "density": 100,
        "CO2bio": -0.368 * 44 / 12,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "incineration",
            "Biowaste {CH}| treatment of biowaste by anaerobic digestion | Cut-off, S",
        ],
    },
    "glass wool": {  # Ecoinvent
        "name": "Glass wool mat {CH}| production | Cut-off, S",
        "plant_based": False,
        "lambda": 0.036,
        "fire_class": "A1",
        "density": 22,
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            # "Waste mineral wool {Europe without Switzerland}| market for waste mineral wool | Cut-off, S",
            # "Waste mineral wool {Europe without Switzerland}| treatment of waste mineral wool, collection for final disposal | Cut-off, S",
            "Waste mineral wool {Europe without Switzerland}| treatment of waste mineral wool, sorting plant | Cut-off, S",
            "Waste mineral wool, for final disposal {Europe without Switzerland}| treatment of waste mineral wool, inert material landfill | Cut-off, S",
            "Waste mineral wool, for final disposal {Europe without Switzerland}| market for waste mineral wool, final disposal | Cut-off, S",
        ],
    },
    "stone wool": {  # Ecoinvent
        "name": "Stone wool {CH}| stone wool production | Cut-off, S",
        "plant_based": False,
        "lambda": 0.036,
        "fire_class": "A1",
        "density": 29.5,
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            # "Waste mineral wool {Europe without Switzerland}| market for waste mineral wool | Cut-off, S",
            # "Waste mineral wool {Europe without Switzerland}| treatment of waste mineral wool, collection for final disposal | Cut-off, S",
            "Waste mineral wool {Europe without Switzerland}| treatment of waste mineral wool, sorting plant | Cut-off, S",
            "Waste mineral wool, for final disposal {Europe without Switzerland}| treatment of waste mineral wool, inert material landfill | Cut-off, S",
            "Waste mineral wool, for final disposal {Europe without Switzerland}| market for waste mineral wool, final disposal | Cut-off, S",
        ],
    },
    "EPS": {  # Ecoinvent
        "name": "Polystyrene foam slab {CH}| production, 45% recycled | Cut-off, S",
        "plant_based": False,
        "lambda": 0.035,
        "fire_class": "E",
        "density": 30,
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            # "Waste polystyrene {Europe without Switzerland}| market for waste polystyrene | Cut-off, S",
            "Waste expanded polystyrene {CH}| treatment of, municipal incineration | Cut-off, S",
            "Waste polystyrene {Europe without Switzerland}| treatment of waste polystyrene, sanitary landfill | Cut-off, S",
        ],
    },
    "XPS": {  # Ecoinvent
        "name": "Polystyrene, extruded {RER}| polystyrene production, extruded, CO2 blown | Cut-off, S",
        "plant_based": False,
        "lambda": 0.033,
        "fire_class": "E",
        "density": 40,  # placeholder
        "CO2bio": -0,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            # "Waste polystyrene {Europe without Switzerland}| market for waste polystyrene | Cut-off, S",
            "Waste expanded polystyrene {CH}| treatment of, municipal incineration | Cut-off, S",
            "Waste polystyrene {Europe without Switzerland}| treatment of waste polystyrene, sanitary landfill | Cut-off, S",
        ],
    },
}

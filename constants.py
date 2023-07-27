CURRENT_YEAR = 2023
M2FACADE = 7.6
RVALUE = 3.5
BUILDING_LIFETIME = 75
MATERIALS = {
    "truck": {
        "name": "Transport, freight, lorry 7.5-16 metric ton, EURO3 {GLO}| market for | Cut-off, S"
    },
    "test": {
        "name": "test",
        "plant_based": False,
        "lambda": 0.05,
        "density": 50,
        "CO2bio": -100 * 44 / 12,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "Biowaste {CH}| treatment of biowaste, industrial composting | Cut-off, S"
        ],
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
        "density": 52,
        "CO2bio": -0.404 * 44 / 12,
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "Biowaste {CH}| treatment of biowaste by anaerobic digestion | Cut-off, S",
            "Biowaste {CH}| treatment of biowaste by anaerobic digestion | Cut-off, S",
        ],
    },
    "flax": {
        "name": "Fibre, flax {RoW}| fibre production, flax, retting | Cut-off, U",
        "plant_based": True,
        "lambda": 0.041,  # placeholder
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
        "density": 36,
        "CO2bio": -0.377 * 44 / 12,  # from biofib'chanvre EPD
        "rotation": 1,
        "lifetime": 50,
        "waste": [
            "incineration",
            "Biowaste {CH}| treatment of biowaste by anaerobic digestion | Cut-off, S",
        ],
    },
    "straw": {  # Ecoinvent
        "name": "Straw {CH}| wheat production, Swiss integrated production, extensive | Cut-off, S",
        "plant_based": True,
        "lambda": 0.44,
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
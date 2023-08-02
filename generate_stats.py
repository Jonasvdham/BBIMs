from DLCA import DLCA
import numpy as np
import pandas as pd
from operator import itemgetter


def prep_data(
    materials=[
        "cellulose",
        "straw",
        "hemp",
        "flax",
        "wood fiber",
        "EPS",
        "XPS",
        "stone wool",
        "glass wool",
    ],
    building_scenario="normal",
    total_houses=592,
    time_horizon=2024,
    timeframe=200,
    waste_scenario=0,
):

    gwis = DLCA(
        materials,
        building_scenario,
        total_houses,
        time_horizon,
        timeframe,
        waste_scenario,
    )

    column_names = ["material", "year", "inst", "cum"]
    df = pd.DataFrame(columns=column_names)
    for material in list(gwis.keys()):
        tmp_df = pd.concat(
            [
                pd.Series([material for i in range(200)]),
                pd.Series([i for i in range(200)]),
                gwis[material]["inst_tot"],
                gwis[material]["cum"],
            ],
            axis=1,
            keys=column_names,
        )
        df = pd.concat([df, tmp_df])
    df = df.reset_index(drop=True)
    return df


def print_stats(df):
    for i in ["inst", "cum"]:
        y0min = df[df["year"] == 0][i].idxmin()
        y0max = df[df["year"] == 0][i].idxmax()
        minimum = df[i].idxmin()
        maximum = df[i].idxmax()

        print(i)
        print("y0 min - ", df.loc[y0min]["material"], df.loc[y0min][i])
        print("y0 max - ", df.loc[y0max]["material"], df.loc[y0max][i])
        print(
            "min - year: ",
            df.loc[minimum]["year"],
            df.loc[minimum]["material"],
            df.loc[minimum][i],
        )
        print(
            "max - year: ",
            df.loc[maximum]["year"],
            df.loc[maximum]["material"],
            df.loc[maximum][i],
        )


if __name__ == "__main__":
    for scenario in [(592, 2024), (150000, 2050)]:
        print(f"Total houses: {scenario[0]} - Timeframe: {scenario[1]}")
        print_stats(
            prep_data(total_houses=scenario[0], time_horizon=scenario[1])
        )

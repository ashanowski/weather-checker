""" Script visualizing modified data contained
    in a csv.
"""

from modify_csv import *
import pandas as pd


if __name__ == '__main__':
    df = clear_dataframe(pd.read_csv('weather.csv'))
    plot_temps(df)
    print(df.head())

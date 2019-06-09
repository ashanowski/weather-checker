""" Main script that runs gathering, manipulation
    and visualization tasks one by one
"""
from gather_data import fetch_data
from modify_csv import clear_dataframe, plot_temps
import pandas as pd


if __name__ == '__main__':
    fetch_data()
    df = clear_dataframe(pd.read_csv('weather.csv'))
    plot_temps(df)

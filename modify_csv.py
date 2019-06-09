""" File containing functions to manipulate
    csv data gathered with gather_data.py
"""
import datetime
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')


def clear_dataframe(df):
    """ Performs dataset clear on given dataframe """
    # remove unnamed column
    df = df.iloc[:, 1:]

    # remove % sign from 'humidity' and 'precip'
    df.humidity = [x[:-1] for x in df.humidity]
    df.precip = [x[:-1] for x in df.precip]

    # distribute 'temp' to 'temp_hi' and 'temp_low'
    # df['temp_hi'] = [x[:2] for x in df.temp]
    # df['temp_low'] = [x[3:5] for x in df.temp]
    regex = r'(--|\d+)'
    df['temp_hi'] = [re.findall(regex, x)[0]
                     if re.findall(regex, x)[0] != '--'
                     else np.nan
                     for x in df.temp]

    df['temp_low'] = [re.findall(regex, x)[1]
                      if re.findall(regex, x)[1] != '--'
                      else np.nan
                      for x in df.temp]

    # drop 'temp'
    df = df.drop(['temp'], axis=1)

    # substract actual wind speed in mph as a number from 'wind'
    df.wind = [re.findall(r'\d+', x)[0] for x in df.wind]


    def month_to_number(string):
        """ function changing month to its number, 'MAR' -> 03 (str) """
        months = [
            'JAN', 'FEB', 'MAR', 'APR', 'MAY',
            'JUN', 'JUL', 'AUG', 'SEP', 'OCT',
            'NOV', 'DEC'
        ]

        for num, mth in zip(range(1, 13), months):
            if mth == string.upper():
                if num < 10:
                    num = "0" + str(num)
                return str(num)
        return None


    def convert_date(data):
        """ function converting date, ie. 'MAR 28' -> '28/03/2019' (str) """
        now = datetime.datetime.now()
        year = str(now.year)
        month = month_to_number(data[:3])
        day = str(re.findall(r'\d+', data)[0])

        return "{}/{}/{}".format(day, month, year)

    # apply convert_date function and convert column to dt type
    df['date'] = df['date'].apply(convert_date)
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)

    # cast other numerical columns to int64
    df['humidity'] = df['humidity'].astype('int64')
    df['precip'] = df['precip'].astype('int64')
    df['wind'] = df['wind'].astype('int64')
    df['temp_hi'] = df['temp_hi'].astype('Float64')
    df['temp_low'] = df['temp_low'].astype('Float64')

    # convert F to C and mph to kph
    df.temp_hi = df['temp_hi'].apply(lambda x: (x-32) // 1.8)
    df.temp_low = df['temp_low'].apply(lambda x: (x-32) // 1.8)
    df.wind = [round(mph/0.62137119, 1) for mph in df.wind]

    for col in df.columns[3:]:
        mean = df[col].mean()
        df[col] = df[col].fillna(mean)
    return df


def get_data(df, prop='temp'):
    """ Get data from pandas dataframe

        df -> Pandas DataFrame
        prop -> string:
            'temp' for temperature data
            'humidity' for humidity data
            'precipitation' for precipitation data
            'wind' for wind data
    """
    day_names = np.array(df.day)
    days = [i for i in range(len(day_names))]

    if prop == 'temp':
        temps_hi = np.array(df.temp_hi)
        temps_low = np.array(df.temp_low)
        return [days, day_names, temps_hi, temps_low]

    if prop == 'humidity':
        hums = np.array(df.humidity)
        return [days, day_names, hums]

    if prop == 'precipitation':
        precips = np.array(df.precip)
        return [days, day_names, precips]

    if prop == 'wind':
        winds = np.array(df.wind)
        return [days, day_names, winds]

    if prop == 'weather':
        temps_hi = np.array(df.temp_hi)
        temps_low = np.array(df.temp_low)
        hums = np.array(df.humidity)
        precips = np.array(df.precip)
        winds = np.array(df.wind)

        return [days, day_names, temps_hi, temps_low, hums,
                precips, winds]


def plot_temps(df):
    """ Plot min and max temperatures during weekday"""
    plt.figure(1, figsize=(12, 6))

    days, day_names, temps_hi, temps_low = get_data(df)

    plt.bar(days, temps_hi, color='xkcd:red', label='Highest possible')
    plt.bar(days, temps_low, color='xkcd:lightblue', label='Lowest possible')

    plt.xticks(ticks=[i for i in range(len(days))], labels=day_names)

    plt.title('Temperature through the week')
    plt.xlabel('Weekday')
    plt.ylabel('Temperature [*C]')

    plt.legend(loc='best', fontsize=15)
    plt.show()


def plot_precip(days, day_names, precips):
    """ Plot the precipitation"""
    plt.figure(2, figsize=(12, 6))

    plt.bar(days, precips, label='Precipitation')

    plt.title('Precipitation through the week')
    plt.xlabel('Weekdays')
    plt.ylabel('Precipitation percentage')

    plt.xticks(ticks=[i for i in range(len(days))], labels=day_names)
    plt.legend(loc='best', fontsize=15)
    plt.show()


def plot_wind(days, day_names, winds):
    """ Plot the wind velocity """
    fig = plt.figure(3, figsize=(12, 6))

    plt.bar(days, winds, color='xkcd:magenta', label='Wind velocity')

    plt.title('Wind velocity through the week')
    plt.xlabel('Weekdays')
    plt.ylabel('Wind velocity [km/h]')

    plt.xticks(ticks=[i for i in range(len(days))], labels=day_names)
    plt.legend(loc='best', fontsize=15)

    return fig


def plot_hum(days, day_names, hums):
    """ Plot the humidity """
    fig = plt.figure(4, figsize=(12, 6))

    plt.bar(days, hums, color='xkcd:cyan', label='Humidity')

    plt.title('Humidity through the week')
    plt.xlabel('Weekdays')
    plt.ylabel('Humidity percentage')

    plt.xticks(ticks=[i for i in range(len(days))], labels=day_names)
    plt.legend(loc='best', fontsize=15)

    return fig


def plot_weather(days, day_names, temps_hi, temps_low, hums,
                 precips, winds):
    """ Plot every weather data possible """
    fig = plt.figure(5, figsize=(12, 6))

    # upper left
    plt.subplot(221)
    plt.bar(days, temps_hi, color='xkcd:red',
            label='Highest possible')
    plt.bar(days, temps_low, color='xkcd:lightblue',
            label='Lowest possible')

    plt.xticks(ticks=[i for i in range(len(days))],
               labels=day_names, rotation='vertical')

    plt.title('Temperature through the week')
    plt.ylabel('Temperature [*C]')

    #plt.legend(loc='best', fontsize=15)

    # upper right
    plt.subplot(222)
    plt.bar(days, hums, color='xkcd:cyan', label='Humidity')

    plt.title('Humidity through the week')
    plt.ylabel('Humidity percentage')

    plt.xticks(ticks=[i for i in range(len(days))],
               labels=day_names, rotation='vertical')
    #plt.legend(loc='best', fontsize=15)

    # lower left
    plt.subplot(223)
    plt.bar(days, precips, label='Precipitation')

    plt.title('Precipitation through the week')
    plt.xlabel('Weekdays')
    plt.ylabel('Precipitation percentage')

    plt.xticks(ticks=[i for i in range(len(days))],
               labels=day_names, rotation='vertical')
    #plt.legend(loc='best', fontsize=15)

    # lower right
    plt.subplot(224)
    plt.bar(days, winds, color='xkcd:magenta',
            label='Wind velocity')

    plt.title('Wind velocity through the week')
    plt.xlabel('Weekdays')
    plt.ylabel('Wind velocity [km/h]')

    plt.xticks(ticks=[i for i in range(len(days))],
               labels=day_names, rotation='vertical')
    #plt.legend(loc='best', fontsize=15)

    plt.subplots_adjust(wspace=0.2, hspace=0.2)

    return fig

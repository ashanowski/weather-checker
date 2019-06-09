""" Script scraping web data about weather
    and saving it as a csv file.
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging
logging.getLogger().setLevel(logging.INFO)


def fetch_data():
    """ Fetch weather data from url """
    url = "https://weather.com/weather/tenday/l/PLXX0029:1:PL"

    logging.info("Requesting url...")
    try:
        page = requests.get(url)
    except requests.exceptions.Timeout() as exception:
        logging.info("Connection timed out! %s", exception)
    except requests.exceptions.InvalidURL() as exception:
        logging.info("Invalid URL provided! %s", exception)
    else:

        logging.info("Accessing data...")
        soup = BeautifulSoup(page.content, "html.parser")

        logging.info("Creating data table...")
        table = soup.find_all("table", {"class": "twc-table"})
        data_list = []

        for items in table:
            for i in range(len(items.find_all("tr")) - 1):
                day_data = {}
                day_data["day"] = items.find_all(
                    "span", {"class": "date-time"})[i].text
                day_data["date"] = items.find_all(
                    "span", {"class": "day-detail clearfix"})[i].text
                day_data["desc"] = items.find_all(
                    "td", {"class": "description"})[i].text
                day_data["temp"] = items.find_all(
                    "td", {"class": "temp"})[i].text
                day_data["precip"] = items.find_all(
                    "td", {"class": "precip"})[i].text
                day_data["wind"] = items.find_all(
                    "td", {"class": "wind"})[i].text
                day_data["humidity"] = items.find_all(
                    "td", {"class": "humidity"})[i].text
                data_list.append(day_data)

        logging.info("Converting to Pandas DataFrame...")
        pd_dataframe = pd.DataFrame(data_list)

        logging.info("Saving data to 'weather.csv'...")
        pd_dataframe.to_csv("weather.csv")
        logging.info("Success!")

if __name__ == '__main__':
    fetch_data()

from scrape_weather import WeatherScraper
from pprint import pprint
from db_context_manager import UseDatabase
import os


class DBOperations():

    def create_database(self):
        test = WeatherScraper(
            'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1999&EndYear=1999&Day=1&Year=2015&Month=11#')
        weather = test.scrape_weather()

        if os.path.exists("weather.sqlite"):
            os.remove("weather.sqlite")
        with UseDatabase('weather.sqlite') as cursor:
            execute_str = '''create table weather
                                (id integer primary key autoincrement not null,
                                sample_date text not null,
                                location text not null,
                                min_temp real not null,
                                max_temp real not null,
                                avg_temp real not null,
                                UNIQUE (sample_date));'''

            cursor.execute(execute_str)

            sqlite_insert = """INSERT INTO weather
                                    (sample_date,location,min_temp,max_temp,avg_temp)
                                    VALUES (?,?,?,?,?);"""

            for item in weather.items():
                cursor.execute(sqlite_insert,
                               (item[0], "Winnipeg,MB", item[1]["Max"], item[1]["Min"], item[1]["Mean"]))

    def update_database(self, data):
        with UseDatabase('weather.sqlite') as cursor:
            sqlite_insert = """INSERT OR IGNORE INTO weather
                                    (sample_date,location,min_temp,max_temp,avg_temp)
                                    VALUES (?,?,?,?,?);"""
            for item in data.items():
                cursor.execute(sqlite_insert,
                               (item[0], "Winnipeg,MB", item[1]["Max"], item[1]["Min"], item[1]["Mean"]))


if __name__ == '__main__':
    full_set = DBOperations()
    full_set.create_database()

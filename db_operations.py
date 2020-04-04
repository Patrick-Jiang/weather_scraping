from scrape_weather import WeatherScraper
from pprint import pprint
import sqlite3


class UseDatabase:
    def __init__(self) -> None:
        pass

    def __enter__(self) -> 'cursor':
        self.conn = sqlite3.connect("weather.sqlite")
        print("Opened the database")
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class DBOperations:
    test = WeatherScraper(
        'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1999&EndYear=1999&Day=1&Year=2015&Month=11#')
    weather = test.scrape_weather()

    with UseDatabase() as cursor:
        execute_str = '''create table weather
                            (id integer primary key autoincrement not null,
                            sample_date text not null,
                            location text not null,
                            min_temp real not null,
                            max_temp real not null,
                            avg_temp real not null);'''
        cursor.execute(
            """SELECT name FROM sqlite_master WHERE type='table' AND name='weather';""")
        if(cursor.fetchone() is None):
            cursor.execute(execute_str)

        sqlite_insert = """INSERT INTO weather
                                (sample_date,location,min_temp,max_temp,avg_temp)
                                VALUES (?,?,?,?,?);"""

        for item in weather.items():
            cursor.execute(sqlite_insert,
                           (item[0], "Winnipeg,MB", item[1]["Max"], item[1]["Min"], item[1]["Mean"]))

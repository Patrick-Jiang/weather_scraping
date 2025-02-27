"""This is the main program use console """
from scrape_weather import WeatherScraper
from db_context_manager import UseDatabase
from db_operations import DBOperations
from plot_operations import PlotOperations
from datetime import datetime
from html.parser import HTMLParser
import urllib.request
import warnings


class WeatherProcessor:
    """This class is to launch and manage all the other tasks. """

    def __init__(self):
        """Get the lastest date in the database"""
        with UseDatabase('weather.sqlite') as cursor:
            execute_str = \
                '''SELECT * FROM weather ORDER BY sample_date DESC LIMIT 1 '''
            cursor.execute(execute_str)
            row = cursor.fetchall()
        self.newest_date = row[0][1]
        self.db_date = row[0][1].split("-")

    def generate_data_url(self):
        """This method is to generate all the urls"""
        data_url_list = []
        startYear = int(self.db_date[0])
        endYear = datetime.now().year
        endMonth = datetime.now().month

        endDay = 31
        for x in (range(startYear, endYear+1)):
            if(datetime.now().year == x):
                for y in range(1, datetime.now().month + 1):
                    current_year = x
                    endMonth = y
                    url = 'https://climate.weather.gc.ca/climate_data/'\
                        'daily_data_e.html?StationID=27174&timeframe=2&'\
                        'StartYear={}&EndYear={}&Day={}&Year={}&Month={}#'\
                        .format(startYear, endYear, endDay, current_year, endMonth)
                    data_url_list.append(url)
            else:
                for y in range(1, 13):
                    current_year = x
                    endMonth = y
                    url = 'https://climate.weather.gc.ca/climate_data/'\
                        'daily_data_e.html?StationID=27174&timeframe=2&'\
                        'StartYear={}&EndYear={}&Day={}&Year={}&Month={}#'\
                        .format(startYear, endYear, endDay, current_year, endMonth)
                    data_url_list.append(url)
        return data_url_list

    def update_db(self):
        """Update database to most recent day of year"""
        data_url_list = self.generate_data_url()
        weather = dict()
        for url in data_url_list:
            print('Scraping data from: ')
            print(url)
            myparser = WeatherScraper()
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
            myparser.feed(html)
            weather.update(myparser.temps_data)
        db = DBOperations()
        db.update_database(weather)

    @staticmethod
    def db_selection():
        """This is to create selection for update or download fullset"""
        print('Please select from (1)download a full set of'
              ' weather data or (2)update it')
        x = int(input())

        if x != 1 and x != 2:
            raise Exception()

        if(x == 1):
            full_set = DBOperations()
            full_set.create_database()
        if(x == 2):
            test = WeatherProcessor()
            print('Most recent date in database is', test.newest_date)
            print("Updating Database to today's date")
            test.update_db()
            print("Updating Database successed")

    @staticmethod
    def plot_selection():
        """This method is to create weather plot"""
        print(
            'Please enter  year range of interest '
            '(from year, to year example: 2000,2017)')
        x = input().split(",")
        test = PlotOperations(int(x[0]), int(x[1]))
        test.create_weather_data()
        test.create_plot(test.weather_data)


if __name__ == '__main__':
    warnings.filterwarnings(
        "ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)
    try:
        WeatherProcessor.db_selection()
        WeatherProcessor.plot_selection()
    except:
        print("Please verify inputs!!!")

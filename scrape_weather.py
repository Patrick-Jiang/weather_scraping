"""Scrape weather data from https://climate.weather.gc.ca/ ."""
import json
import urllib.request
from html.parser import HTMLParser
from datetime import datetime
from pprint import pprint


class WeatherScraper(HTMLParser):
    """Weather scraper inherit from HTMLParser."""

    def __init__(self, url=None):
        """Initialize class variables."""
        HTMLParser.__init__(self)
        self.is_tbody = False
        self.is_tr = False
        self.is_td = False
        self.end_of_row = False
        self.end_of_td = False
        self.estimated = False
        self.date = ''
        self.td_counter = 0
        self.daily_temps = dict()
        self.temps_data = dict()
        self.url = url
        self.start_year = None
        self.is_select = False
        self.is_option = False

    def handle_starttag(self, tag, attrs):
        """Handle the start tags"""
        if (tag == 'tbody'):
            self.is_tbody = True
        if (tag == 'tr'):
            self.is_tr = True
        if (tag == 'select'):
            for attr in attrs:
                if (attr[0] == 'id' and attr[1] == 'Year1'):
                    self.is_select = True
                    break

        if (tag == 'option' and self.is_select):
            self.is_option = True

        if (tag == 'abbr' and self.is_tbody and self.is_tr):
            if(attrs[0][1] == 'Average' or attrs[0][1] == 'Extreme'):
                self.end_of_row = True
            if not self.end_of_row:
                input_format = "%B %d, %Y"
                output_format = "%Y-%m-%d"
                self.date = datetime.strptime(
                    attrs[0][1], input_format).strftime(output_format)

        if (tag == 'td' and self.is_tbody and self.is_tr and
                not self.end_of_row):
            self.is_td = True
            self.end_of_td = False
            self.td_counter += 1

    def handle_endtag(self, tag):
        """Handle the end tags"""
        if (tag == 'td'):
            self.is_td = False
        if (tag == 'td' and self.td_counter == 3):
            self.end_of_td = True
            if(self.date != ''):
                self.temps_data.update({self.date: self.daily_temps})
            self.daily_temps = {}
            self.td_counter = 0
            self.is_tr = False
            self.date = ''
        if (tag == 'tbody'):
            self.is_tbody = False
        if (tag == 'select' or self.start_year is not None):
            self.is_select = False
            self.is_option = False

    def handle_data(self, data):
        """Handle the data"""
        if (self.is_option and self.is_select):
            self.start_year = data

        if(data == "Sum"):
            self.end_of_row = True
        if(data == "E" or data == "LegendE"):
            return
        if(data == 'M' or data == "LegendM" or data == "\u00a0"):
            data = ''
        if(self.is_td and self.is_tbody and
           self.is_tr and not self.end_of_row and
                not self.end_of_td and self.td_counter == 1):
            self.daily_temps.update({'Max': data})
        if(self.is_td and self.is_tbody and
           self.is_tr and not self.end_of_row and
                not self.end_of_td and self.td_counter == 2):
            self.daily_temps.update({'Min': data})
        if(self.is_td and self.is_tbody and
           self.is_tr and not self.end_of_row and
                not self.end_of_td and self.td_counter == 3):
            self.daily_temps.update({'Mean': data})

    def generate_data_url(self, start_year, end_year=datetime.now().year):
        """This method is to generate all the urls"""
        data_url_list = []
        startYear = int(start_year)
        endYear = end_year
        endMonth = 12
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

    def scrape_weather(self, start_year=None):
        """This is main method to scrape the data"""
        weather = dict()
        with urllib.request.urlopen(self.url) as response:
            html = str(response.read())
        self.feed(html)

        data_url_list = self.generate_data_url(self.start_year)
        for url in data_url_list:
            print('Scraping data from: ')
            print(url)
            myparser = WeatherScraper()
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
            myparser.feed(html)
            weather.update(myparser.temps_data)
        return weather


if __name__ == '__main__':
    test = WeatherScraper(
        'https://climate.weather.gc.ca/climate_data/'
        'daily_data_e.html?StationID=27174&timeframe=2&'
        'StartYear=1999&EndYear=1999&Day=1&Year=2015&Month=11#')
    weather = test.scrape_weather()
    with open('weather_all.json', 'w') as fp:
        json.dump(weather, fp)
    pprint(weather)


import urllib.request
from html.parser import HTMLParser
from datetime import datetime
from pprint import pprint


class WeatherScraper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.is_tbody = False
        self.is_tr = False
        self.is_td = False
        self.end_of_row = False
        self.end_of_td = False
        self.no_data = False
        self.estimated = False
        self.date = ''
        self.td_counter = 0
        self.daily_temps = dict()
        self.temps_data = dict()

    def handle_starttag(self, tag, attrs):
        if (tag == 'tbody'):
            self.is_tbody = True
        if (tag == 'tr'):
            self.is_tr = True
        if (tag == 'abbr' and self.is_tbody and self.is_tr):
            if(attrs[0][1] == 'Average' or attrs[0][1] == 'Extreme'):
                self.end_of_row = True
            if(self.end_of_row == False):
                input_format = "%B %d, %Y"
                output_format = "%Y-%m-%d"
                self.date = datetime.strptime(
                    attrs[0][1], input_format).strftime(output_format)
        if (tag == 'td' and self.is_tbody and self.is_tr and self.end_of_row == False and self.no_data == False):
            self.is_td = True
            self.end_of_td = False
            self.td_counter += 1
            # print('111')

    def handle_endtag(self, tag):
        if (tag == 'td'):
            self.is_td = False
        if (tag == 'td' and self.td_counter == 3):
            self.end_of_td = True
            self.temps_data.update({self.date: self.daily_temps})
            self.daily_temps = {}
            self.td_counter = 0
            self.is_tr = False
        if (tag == 'tbody'):
            self.is_tbody = False

    def handle_data(self, data):
        if(data == "Sum"):
            self.end_of_row = True
        if(data.replace('\xa0', '') == '' and self.is_tbody and self.is_tr and self.end_of_row == False):
            self.no_data = True

        if(self.is_td and self.is_tbody and self.is_tr and self.end_of_row == False and self.end_of_td == False and self.td_counter == 1):
            self.daily_temps.update({'Max': data})
        if(self.is_td and self.is_tbody and self.is_tr and self.end_of_row == False and self.end_of_td == False and self.td_counter == 2):
            self.daily_temps.update({'Min': data})
        if(self.is_td and self.is_tbody and self.is_tr and self.end_of_row == False and self.end_of_td == False and self.td_counter == 3):
            self.daily_temps.update({'Mean': data})


def generate_data_url():
    data_url_list = []
    startYear = 2019
    endYear = 2020
    endMonth = 12
    endDay = 31
    for x in reversed(range(startYear, endYear+1)):
        if(datetime.now().year == x):
            for y in range(1, datetime.now().month + 1):
                current_year = x
                endMonth = y
                url = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear={}&EndYear={}&Day={}&Year={}&Month={}#'.format(
                    startYear, endYear, endDay, current_year, endMonth)
                data_url_list.append(url)
        else:
            for y in range(1, 13):
                current_year = x
                endMonth = y
                url = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear={}&EndYear={}&Day={}&Year={}&Month={}#'.format(
                    startYear, endYear, endDay, current_year, endMonth)
                data_url_list.append(url)
    return data_url_list


data_url_list = generate_data_url()
for url in data_url_list:
    print(url)

weather = dict()
for url in data_url_list:
    myparser = WeatherScraper()
    with urllib.request.urlopen(url) as response:
        html = str(response.read())
    myparser.feed(html)

    weather.update(myparser.temps_data)

pprint(weather)

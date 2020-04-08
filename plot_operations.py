from db_context_manager import UseDatabase
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class PlotOperations():
  def __init__(self,start_year=1996,end_year=2020):
    self.start_year = start_year
    self.end_year = end_year
    self.weather_data = dict()
    self.month = 0

  def create_weather_data(self,start_year=0,end_year=0):
    start_year = self.start_year
    end_year = self.end_year

    with UseDatabase('weather.sqlite') as cursor:
      for x in range(1,13):
        monthly_list = []
        for year in range(start_year,end_year + 1):
          self.month = x
          year = str(year)
          cursor.execute("SELECT avg_temp FROM weather WHERE sample_date LIKE ?", ('%{}%'.format(year +'-'+ str(x).zfill(2)),))

          rows = cursor.fetchall()

          for row in rows:
            if '{}'.format(row[0]) != '':
              monthly_list.append(float('{}'.format(row[0])))
          self.weather_data.update({self.month : monthly_list})


test = PlotOperations(2000,2017)
test.create_weather_data()
# print(test.weather_data)

fig, ax = plt.subplots()
ax.boxplot(test.weather_data.values())
ax.set_xticklabels(test.weather_data.keys())



plt.show()
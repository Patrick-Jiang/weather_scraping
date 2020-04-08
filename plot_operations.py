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

  def create_weather_data(self,self.start_year,self.end_year):
    with UseDatabase('weather.sqlite') as cursor:
      # execute_str = "SELECT avg_temp FROM weather WHERE sample_data LIKE ?",(str(year),)
      if year == 2020:
        end_month = datetime.now().month + 1
      else:
        end_month = 13

      if year == 1996:
        start_month = 10
      else:
        start_month = 1

      for x in range(start_month,end_month):
        self.month = x
        monthly_list = []
        year = str(year)
        cursor.execute("SELECT avg_temp FROM weather WHERE sample_date LIKE ?", ('%{}%'.format(year +'-'+ str(x).zfill(2)),))

        rows = cursor.fetchall()

        for row in rows:
          if '{}'.format(row[0]) is not '':
            monthly_list.append(float('{}'.format(row[0])))
        self.weather_data.update({self.month : monthly_list})


test = PlotOperations(2000,2017)
test.create_weather_data()
print(test.weather_data)
  # # fake up some data
  # spread = np.random.rand(50) * 100
  # center = np.ones(25) * 50
  # flier_high = np.random.rand(10) * 100 + 100
  # flier_low = np.random.rand(10) * -100
  # data = np.concatenate((spread, center, flier_high, flier_low), 0)


  # # basic plot
  # plt.boxplot(data)


  # # notched plot
  # plt.figure()
  # plt.boxplot(data, 1)

  # # change outlier point symbols
  # plt.figure()
  # plt.boxplot(data, 0, 'gD')

  # # don't show outlier points
  # plt.figure()
  # plt.boxplot(data, 0, '')

  # # horizontal boxes
  # plt.figure()
  # plt.boxplot(data, 0, 'rs', 0)

  # # change whisker length
  # plt.figure()
  # plt.boxplot(data, 0, 'rs', 0, 0.75)

  # # fake up some more data
  # # spread = np.random.rand(50) * 100
  # # center = np.ones(25) * 40
  # # flier_high = np.random.rand(10) * 100 + 100
  # # flier_low = np.random.rand(10) * -100
  # # d2 = np.concatenate((spread, center, flier_high, flier_low), 0)
  # # data.shape = (-1, 1)
  # # d2.shape = (-1, 1)
  # # # data = concatenate( (data, d2), 1 )
  # # # Making a 2-D array only works if all the columns are the
  # # # same length.  If they are not, then use a list instead.
  # # # This is actually more efficient because boxplot converts
  # # # a 2-D array into a list of vectors internally anyway.
  # # data = [data, d2, d2[::2, 0]]
  # # # multiple box plots on one figure
  # # plt.figure()
  # plt.boxplot(data)

  # plt.show()

# yn = PlotOperations(1996,2006)

# print(yn.end_year)
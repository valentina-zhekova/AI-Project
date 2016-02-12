#!/usr/bin/env python
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
import csv
import string
from matplotlib.lines import Line2D 

# (Year, month, day) tuples suffice as args for quotes_historical_yahoo
date1 = (2004, 2, 1)
date2 = (2004, 4, 12)


mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
alldays = DayLocator()              # minor ticks on the days
# weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
dayFormatter = DateFormatter('%b %d')      # e.g., 12

# Get historical data for ticker between date1 and date2.
# quotes = quotes_historical_yahoo_ohlc('INTC', date1, date2)
# if len(quotes) == 0:
#     raise SystemExit

# with open('EURUSD240.csv', 'r') as csvfile:
# 	datareader = list(csv.reader(csvfile))

import main
datareader = main.get_result() 

def parse_time(date, hour):
	year, month, day = map(lambda x: int(x), date.split('.'))
	hour, minutes = map(lambda x: int(x), hour.split(':'))
	return datetime(year, month, day, hour, minutes)

def parse(row):
	time = parse_time(row[0], row[1])
	# print(time)
	return [date2num(time), float(row[2]), float(row[3]), float(row[4]), float(row[5])]

datareader2 = []
for x in datareader:
	datareader2.append(parse(x))

datareader2 = datareader2
# print(datareader[0])
# print(type(datareader2[0][0]))


# http://matplotlib.org/api/pyplot_api.html
# http://matplotlib.org/api/ticker_api.html
# Create two subplots
fig, ax = plt.subplots()
# Adjust subplots... dude...
fig.subplots_adjust(bottom=0.2)
# ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(alldays)
# ax.xaxis.set_major_formatter(weekFormatter)
# ax.xaxis.set_minor_formatter(dayFormatter)

# plot_day_summary(ax, quotes, ticksize=3)
# quotes = [(time, open, close, high, low, ...), () ]
# http://matplotlib.org/api/finance_api.html -> docu
# time must be a float date (the fuck)
# width = fraction of a day for the rectangle width (the fuck?)
# we're drawing on the ax subplot
candlestick_ohlc(ax, datareader2)
plt.axhline(y=main.get_desired_value())


# http://matplotlib.org/api/axes_api.html
# Sets up x-axis ticks and labels that treat the x data as dates.
ax.xaxis_date()
# Autoscale the view limits using the data limits.
ax.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

# draw the plot
plt.show()

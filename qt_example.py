#!/usr/bin/env python
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc


# (Year, month, day) tuples suffice as args for quotes_historical_yahoo
date1 = (2004, 2, 1)
date2 = (2004, 4, 12)


mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
alldays = DayLocator()              # minor ticks on the days
weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
dayFormatter = DateFormatter('%d')      # e.g., 12

# Get historical data for ticker between date1 and date2.
quotes = quotes_historical_yahoo_ohlc('INTC', date1, date2)
if len(quotes) == 0:
    raise SystemExit

# http://matplotlib.org/api/pyplot_api.html
# http://matplotlib.org/api/ticker_api.html
# Create two subplots
fig, ax = plt.subplots()
# Adjust subplots... dude...
fig.subplots_adjust(bottom=0.2)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(weekFormatter)
#ax.xaxis.set_minor_formatter(dayFormatter)

# plot_day_summary(ax, quotes, ticksize=3)
# quotes = [(time, open, close, high, low, ...), () ]
# http://matplotlib.org/api/finance_api.html -> docu
# time must be a float date (the fuck)
# width = fraction of a day for the rectangle width (the fuck?)
# we're drawing on the ax subplot
candlestick_ohlc(ax, quotes, width=0.6)

# http://matplotlib.org/api/axes_api.html
# Sets up x-axis ticks and labels that treat the x data as dates.
ax.xaxis_date()
# Autoscale the view limits using the data limits.
ax.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

# draw the plot
plt.show()

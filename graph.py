import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime
from matplotlib.dates import DayLocator
from matplotlib.finance import candlestick_ohlc



def parse_time(date, hour):
	year, month, day = map(lambda x: int(x), date.split('.'))
	hour, minutes = map(lambda x: int(x), hour.split(':'))
	return datetime(year, month, day, hour, minutes)

def parse(row):
	time = parse_time(row[0], row[1])
	return [date2num(time), float(row[2]), float(row[3]), float(row[4]), float(row[5])]

def set_plt(data, limit):
	data = list(map(lambda x: parse(x), data))

	alldays = DayLocator() # minor ticks on the days

	# Create two subplots
	fig, ax = plt.subplots()
	fig.subplots_adjust(bottom=0.2)
	ax.xaxis.set_minor_locator(alldays)

	# parse data to plot
	candlestick_ohlc(ax, data)
	plt.axhline(y=limit)

	ax.xaxis_date()
	ax.autoscale_view()
	plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

	return plt
	

def show_graphic(data, limit):
	plt = set_plt(data, limit)
	# draw the plot
	plt.show()
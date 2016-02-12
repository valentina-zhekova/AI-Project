from sklearn import linear_model
import csv

# Create linear regar2 closing_prices and return list of r2 values
def get_r2(times, closing_prices):
    result = []
    regr = linear_model.LinearRegression()
    for i in range(len(times)):
        regr.fit(times[:i+1], closing_prices[:i+1])
        result.append(int(regr.score(times[:i+1], closing_prices[:i+1])))
    return list(map(lambda x: round(x,6), result))

class SMA():
	def __init__(self, navg, items):
		self.navg = navg
		self.items = items

	def calculate(self):
		av = []
		for i in range(len(self.items)):
			if i + 1 < self.navg:
				av.append(0)
			else:
				av.append(sum(self.items[i + 1 - self.navg:i + 1]) / self.navg)
		return av

#SMA returns list of SMAs
def get_sma(values):
    first = SMA(10,values).calculate()
    second = SMA(24,values).calculate()
    return list(map(lambda x: round(x,6), [first[i]/(second[i] + 1) for i in range(len(first))]))

def get_r2_values():
	return r2_values_CP

def get_sma_values():
	return sma_values_CP

def get_times():
	return times

def get_closing_prices():
	return closing_prices

# DATA: Reading data: datareader[(date, hour, openPrice, maxPrice, minPrice, closePrice, volume)]
with open('EURUSD240.csv', 'r') as csvfile:
	data = list(csv.reader(csvfile))

closing_prices = [float(row[5]) for row in data]
times = [[count + 1] for count in range(len(data))] # [[1], [2] ... ]

r2_values_CP = get_r2(times, closing_prices)[23:] 
sma_values_CP = get_sma(closing_prices)[23:]
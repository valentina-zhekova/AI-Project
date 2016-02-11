'''
This is out main file - yay!
'''

from sklearn import tree
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import r2_score
import csv

# x1 - GARCH модели - волативност
# x2 - SMA(за два времеви периода) x[24] = x[24,23..15] / x[24..1]
# ?x3 -  авторегресия y = a*x + b -> y = c[101]  x = c[1..100]
# x4 -  цената -> oтклик | времева единица -> предиктор
# x5 - затваряне 


# Reading data: datareader[(date, hour, openPrice, maxPrice, minPrice, closePrice, volume)]
with open('EURUSD240.csv', 'r') as csvfile:
	datareader = list(csv.reader(csvfile))
	# print(spamreader[0])
	
closing_prices = []
times = [] # [[1], [2] ... ]
counter = 0;

# Prepare regression data
for row in datareader:
	counter+=1
	test = []
	test.append(counter)
	times.append(test)
	closing_prices.append(float(row[5]))




# a = times[:len(times)-100]
# a = times
# b = list(map(lambda times: float(times), closing_prices[:len(closing_prices)-100]))
# b = list(map(lambda x: float(x), closing_prices)) 



# Create linear regar2 closing_prices and return list of r2 values
def get_r2_values(times, closing_prices):
    result = []
    regr = linear_model.LinearRegression()
    for i in range(len(times)):
        regr.fit(times[:i+1], closing_prices[:i+1])
        result.append(int(regr.score(times[:i+1], closing_prices[:i+1])))
    return list(map(lambda x: round(x,6), result))



class Simplemovingaverage():
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
    first = Simplemovingaverage(10,values).calculate()
    second = Simplemovingaverage(24,values).calculate()
    return list(map(lambda x: round(x,6), [first[i]/(second[i] + 1) for i in range(len(first))]))

# Koe shte chukne po doby rezultat s 23 ili bez
# All SMA values before 24 are 0, so they are not interesting
r2_values = get_r2_values(times, closing_prices)[23:] 
sma_values = get_sma(closing_prices)[23:]




X = [[r2_values[i], sma_values[i]] for i in range(len(r2_values) - 1)] #tree arguments

Y = closing_prices[23:len(closing_prices) - 1]

print("The action starts here")
# Fit the tree
decision_tree = tree.DecisionTreeRegressor()
decision_tree = decision_tree.fit(X, Y)



print([r2_values[-1], sma_values[-1]], closing_prices[-1])
new_closing_price = decision_tree.predict([r2_values[-1], sma_values[-1]])
print(new_closing_price)
print(len(sma_values))

def update_times_values():
	times.append([len(times) + 1])
	return times

def update_closing_prices_values(new_closing_price):
	closing_prices.append(new_closing_price[0])
	return closing_prices


def update_r2_values():
	regr = linear_model.LinearRegression()
	regr.fit(times, closing_prices)
	new_new_r2 = int(regr.score(times, closing_prices))
	r2_values.append(round(new_new_r2, 6))
	return r2_values

def update_sma_values():
	return get_sma(closing_prices)[23:]


times = update_times_values()
closing_prices = update_closing_prices_values(new_closing_price)
r2_values = update_r2_values()
sma_values = update_sma_values()


new_closing_price = decision_tree.predict([r2_values[-1], sma_values[-1]])

print(new_closing_price)
print(len(sma_values))




print("Boooom boooom...")
# array([1])

# nulite sa zaradi int casta gore !!!!

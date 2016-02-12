'''
This is out main file - yay!
'''
from sklearn.externals import joblib
import pickle

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
max_prices = []
min_prices = []

times = [] # [[1], [2] ... ]
counter = 0;

# Prepare regression data
for row in datareader:
	counter+=1
	test = []
	test.append(counter)
	times.append(test)
	closing_prices.append(float(row[5]))
	max_prices.append(float(row[3]))
	min_prices.append(float(row[4]))


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
r2_values_CP = get_r2_values(times, closing_prices)[23:] 
sma_values_CP = get_sma(closing_prices)[23:]

r2_values_MAX = get_r2_values(times, max_prices)[23:]
sma_values_MAX = get_sma(max_prices)[23:]

r2_values_MIN = get_r2_values(times, min_prices)[23:]
sma_values_MIN = get_sma(min_prices)[23:]


with open('tree_cp.pickle', 'rb') as handle:
  decision_tree_CP = pickle.load(handle)


with open('tree_min.pickle', 'rb') as handle:
  decision_tree_MIN = pickle.load(handle)

with open('tree_max.pickle', 'rb') as handle:
  decision_tree_MAX = pickle.load(handle)

# print([r2_values[-1], sma_values[-1]], closing_prices[-1])
new_closing_price = decision_tree_CP.predict([[r2_values_CP[-1], sma_values_CP[-1]]]) # so much array cause otherwise throw an annoying warning
new_min = decision_tree_MIN.predict([[r2_values_MIN[-1], sma_values_MIN[-1]]])
new_max = decision_tree_MAX.predict([[r2_values_MAX[-1], sma_values_MAX[-1]]])
# print(new_closing_price)
# print(len(sma_values))

def update_times_values():
	times.append([len(times) + 1])
	return times

def update_values(array, new_price):
	array.append(new_price[0])
	return array


def update_r2_values(array, r2_array):
	regr = linear_model.LinearRegression()
	regr.fit(times, array)
	new_new_r2 = int(regr.score(times, array))
	r2_array.append(round(new_new_r2, 6))
	return r2_array

def update_sma_values(array):
	return get_sma(array)[23:]

current_closing_price = closing_prices[-2]
# desired_value = 1.4032
DEFAULT_VALUE = 1.4200

def get_aim_value():
	prompt = "Please, enter the desired value: "
	try:
		value = float(input(prompt))
	except:
		print("That's not a number! I will show you prediction for {}".format(DEFAULT_VALUE))
		value = DEFAULT_VALUE
	return value

def condition(new_value, desired_value):
	if desired_value > current_closing_price:
		return new_value >= desired_value
	elif desired_value < current_closing_price:
		return new_value <= desired_value

start_day = "2016.02.12"
start_time = "00:00"

def date(days, hours):
	tralala = ["00:00", 1, 2, 3, "04:00", 5, 6, 7, "08:00", 9, 10, 11, "12:00", 13, 14, 15, "16:00", 17, 18, 19, "20:00"]
	new_days = start_day.split('.')
	new_days[2] = str(int(new_days[2]) + days)
	return '.'.join(new_days), tralala[hours]

desired_value = get_aim_value()

print("Current price is ", current_closing_price, " and we want to reach price of ", desired_value, ":\n")
# day = 1
print(start_day, start_time, " closing price is ", new_closing_price)

def validate_max(max, open1, close):
	if max < open1 and max < close:
		max = close + 0.0050 if open1 < close else open1 + 0.0050
	return max

def validate_min(min, open1, close):
	if min > open1 and min > close:
		min = open1 - 0.0050 if open1 < close else close - 0.0050
	return min

result = []

days, hours = 0, 0
while not condition(new_closing_price, desired_value):
	hours += 4
	if hours % 24 == 0:
		days += 1
		hours = 0

	d1, h1 = date(days, hours)
	
	times = update_times_values()
	closing_prices = update_values(closing_prices, new_closing_price)
	min_prices = update_values(min_prices, new_min)
	max_prices = update_values(max_prices, new_max)

	r2_values_CP = update_r2_values(closing_prices, r2_values_CP)
	sma_values_CP = update_sma_values(closing_prices)
	
	r2_values_MAX = update_r2_values(max_prices, r2_values_MAX)
	sma_values_MAX = update_sma_values(max_prices)
	
	r2_values_MIN = update_r2_values(min_prices, r2_values_MIN)
	sma_values_MIN = update_sma_values(min_prices)

	new_closing_price = decision_tree_CP.predict([[r2_values_CP[-1], sma_values_CP[-1]]])
	new_max = decision_tree_MAX.predict([[r2_values_MAX[-1], sma_values_MAX[-1]]])
	new_min = decision_tree_MIN.predict([[r2_values_MIN[-1], sma_values_MIN[-1]]])

	new_row = [d1, h1, closing_prices[-1], validate_max(new_max[0], closing_prices[-1], new_closing_price[0]),
	validate_min(new_min[0], closing_prices[-1], new_closing_price[0]), new_closing_price[0]]
	print(111, new_row)
	result.append(new_row)
	print(d1, h1, " closing price is ", new_closing_price, " max is ", new_max, " min is ", new_min)

def get_result():
	return result

def get_desired_value():
	return desired_value

# POTATO!!!!!!

# print("\nAfter ", day, " days you will be there.\nIf it's too slow a piece of Milka may help with teleporting;)\n...or vodka, for more information please check: http://lefunny.net/wp-content/uploads/2013/10/Funny-meme-about-how-to-teleport.jpg")
# print(new_closing_price)
# print(len(sma_values))

# print("Boooom boooom... boooom, shte si kupq avtomat!!!")
# array([1])

# nulite sa zaradi int casta gore !!!!

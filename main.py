import data
import pickle
from sklearn import linear_model
from random import uniform
import graph

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
	return data.get_sma(array)[23:]

def volatility_max(value1, value2):
	vol = uniform(0.0030, 0.0070)
	return round(value2 + vol if value1 < value2 else value1 + vol, 4)

def volatility_min(value1, value2):
	vol = uniform(0.0030, 0.0070)
	return round(value1 - vol if value1 < value2 else value2 - vol, 4)

def get_aim_value():
	prompt = "Please, enter the desired value: "
	try:
		value = float(input(prompt))
	except:
		print("That's not a number! I will show you prediction for {}".format(DEFAULT_VALUE))
		value = DEFAULT_VALUE
	return value

def condition(max_value, min_value, desired_value):
	if desired_value > current_closing_price:
		return max_value >= desired_value
	elif desired_value < current_closing_price:
		return min_value <= desired_value

def date(days, hours):
	tralala = ["00:00", 1, 2, 3, "04:00", 5, 6, 7, "08:00", 9, 10, 11, "12:00", 13, 14, 15, "16:00", 17, 18, 19, "20:00"]
	new_days = start_day.split('.')
	new_days[2] = str(int(new_days[2]) + days)
	return '.'.join(new_days), tralala[hours]

def get_result():
	return result

def get_desired_value():
	return desired_value

r2_values_CP = data.get_r2_values()
sma_values_CP = data.get_sma_values()
times = data.get_times()
closing_prices = data.get_closing_prices()

current_closing_price = closing_prices[-2]
DEFAULT_VALUE = 1.4200 # 1.4032

start_day = "2016.02.12"
start_time = "00:00"

desired_value = get_aim_value()

with open('tree_cp.pickle', 'rb') as handle:
	decision_tree_CP = pickle.load(handle)

print("{} {}: Current price is {} and we want to reach price of {:.4f}:\n".format(start_day, start_time, current_closing_price, desired_value))
############## MAIN
days, hours = 0, 4
result = []


new_closing_price = decision_tree_CP.predict([[r2_values_CP[-1], sma_values_CP[-1]]])
d1, h1 = date(days, hours)
new_max = volatility_max(closing_prices[-1], new_closing_price[0])
new_min = volatility_min(closing_prices[-1], new_closing_price[0])
new_row = [d1, h1, closing_prices[-1], new_max, new_min, new_closing_price[0]]
result.append(new_row)
print("{} {} - open: {:.4f} | max: {:.4f} | min: {:.4f} | value2: {:.4f}".format(d1, h1, new_row[2], new_row[3], new_row[4], new_row[5]))


while not condition(new_max, new_min, desired_value):
	hours += 4
	if hours % 24 == 0:
		days += 1
		hours = 0

	d1, h1 = date(days, hours)
	
	times = update_times_values()
	closing_prices = update_values(closing_prices, new_closing_price)

	r2_values_CP = update_r2_values(closing_prices, r2_values_CP)
	sma_values_CP = update_sma_values(closing_prices)

	new_closing_price = decision_tree_CP.predict([[r2_values_CP[-1], sma_values_CP[-1]]])
	new_max = volatility_max(closing_prices[-1], new_closing_price[0])
	new_min = volatility_min(closing_prices[-1], new_closing_price[0])
	new_row = [d1, h1, closing_prices[-1], new_max, new_min, new_closing_price[0]]
	
	result.append(new_row)
	print("{} {} - open: {:.4f} | max: {:.4f} | min: {:.4f} | value2: {:.4f}".format(d1, h1, new_row[2], new_row[3], new_row[4], new_row[5]))

graph.show_graphic(result, desired_value)
print("PREDICTION: {} will be reached on {} {}".format(desired_value, d1, h1))
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



X_CP = [[r2_values_CP[i], sma_values_CP[i]] for i in range(len(r2_values_CP) - 1)] #tree arguments
Y_CP = closing_prices[23:len(closing_prices) - 1]

X_MAX = [[r2_values_MAX[i], sma_values_MAX[i]] for i in range(len(r2_values_MAX) - 1)] #tree arguments
Y_MAX = max_prices[23:len(max_prices) - 1]

X_MIN = [[r2_values_MIN[i], sma_values_MIN[i]] for i in range(len(r2_values_MIN) - 1)] #tree arguments
Y_MIN = min_prices[23:len(min_prices) - 1]

# print("The action starts here")
# Fit the tree
decision_tree_CP = tree.DecisionTreeRegressor()
decision_tree_CP = decision_tree_CP.fit(X_CP, Y_CP)

decision_tree_MAX = tree.DecisionTreeRegressor()
decision_tree_MAX = decision_tree_MAX.fit(X_MAX, Y_MAX)

decision_tree_MIN = tree.DecisionTreeRegressor()
decision_tree_MIN = decision_tree_MIN.fit(X_MIN, Y_MIN)



from sklearn.externals import joblib
import pickle
print("Done training")

with open('tree_cp.pickle', 'wb') as handle:
  pickle.dump(decision_tree_CP, handle) 

with open('tree_max.pickle', 'wb') as handle:
  pickle.dump(decision_tree_MAX, handle)

with open('tree_min.pickle', 'wb') as handle:
  pickle.dump(decision_tree_MIN, handle)

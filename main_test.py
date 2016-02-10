from sklearn import tree

# import datetime as dt
# import pandas.io.data as web
# st = dt.datetime(1990,1,1)
# en = dt.datetime(2014,1,1)
# data = web.get_data_yahoo('^FTSE', start=st, end=en)
# returns = 100 * data['Adj Close'].pct_change().dropna()
# figure = returns.plot()

# # print(type(returns))

# from arch import arch_model

# # returns = 100 * sp500['Adj Close'].pct_change().dropna()
# am = arch_model(returns)
# # In either case, model parameters are estimated using

# res = am.fit()
# print(str(res))

# x1 - GARCH модели - волативност
# x2 - SMA(за два времеви периода) x[24] = x[24,23..15] / x[24..1]
# ?x3 -  авторегресия y = a*x + b -> y = c[101]  x = c[1..100]
# x4 -  цената -> oтклик | времева единица -> предиктор
# x5 - затваряне 

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import r2_score


from sklearn import tree
import csv

with open('EURUSD240.csv', 'r') as csvfile:
	spamreader = list(csv.reader(csvfile))
	# print(spamreader[0])
	
y=[]
x=[]
time = 0;
for i in spamreader:
	time+=1
	test = []
	test.append(time)
	x.append(test)
	y.append(float(i[5]))


a = x[:len(x)-100]
b = list(map(lambda x: float(x), y[:len(y)-100]))
# Create linear regar2 array
def get_r2_values(x, y):
    result = []
    regr = linear_model.LinearRegression()
    for i in range(len(x)):
        regr.fit(x[:i+1], y[:i+1])
        result.append(int(regr.score(x[:i+1], y[:i+1])))
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

#SMA
def get_sma(values):
    first = Simplemovingaverage(10,values).calculate()
    second = Simplemovingaverage(24,values).calculate()
    return list(map(lambda x: round(x,6), [first[i]/(second[i] + 1) for i in range(len(first))]))

# Koe shte chukne po doby rezultat s 23 ili bez
rmalyk = get_r2_values(a, b)[23:]
rgolqm = get_sma(b)[23:]



ala_bala = [[rmalyk[i], rgolqm[i]] for i in range(len(rmalyk) - 1)]


X = ala_bala

Y = b[23:len(b) - 1]

for i in range(10):
    print(Y[i], X[i])


print("The action starts here")
clf = tree.DecisionTreeRegressor()

X = np.array(X).astype(float)

clf = clf.fit(X, Y)


print(ala_bala[-1], b[-1])

print(clf.predict(ala_bala[-1]))

print("Boooom boooom...")
# array([1])

# nulite sa zaradi int casta gore !!!!
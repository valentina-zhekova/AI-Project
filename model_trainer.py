from sklearn import tree
import pickle
import data

r2_values_CP = data.get_r2_values()
sma_values_CP = data.get_sma_values()
times = data.get_times()
closing_prices = data.get_closing_prices()

X_CP = [[r2_values_CP[i], sma_values_CP[i]] for i in range(len(r2_values_CP) - 1)] #tree arguments
Y_CP = closing_prices[23:len(closing_prices) - 1]

decision_tree_CP = tree.DecisionTreeRegressor()
decision_tree_CP = decision_tree_CP.fit(X_CP, Y_CP)

with open('tree_cp.pickle', 'wb') as handle:
	pickle.dump(decision_tree_CP, handle) 

print("Done training")
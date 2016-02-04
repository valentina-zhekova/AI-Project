from sklearn import tree
import csv

with open('EURUSD240.csv', 'r') as csvfile:
	spamreader = list(csv.reader(csvfile))
	print(spamreader[0])

from arch import arch_model
am = arch_model(returns)
res = am.fit(update_freq=5)
print(res.summary())



[array([ 0.06169621]), 
array([-0.05147406]), 
array([ 0.04445121]), 
array([-0.01159501]), 
array([-0.03638469]), 
array([-0.04069594]), 
array([-0.04716281]), 
array([-0.00189471]), 
array([ 0.06169621]), 
array([ 0.03906215])]



151.0, 75.0, 141.0, 206.0, 135.0, 97.0, 138.0, 63.0, 110.0, 310.0



[array([-0.08380842]), 
array([ 0.01750591]), 
array([-0.02884001]), 
array([-0.00189471]), 
array([-0.02560657]), 
array([-0.01806189]), 
array([ 0.04229559]), 
array([ 0.01211685]), 
array([-0.0105172]), 
array([-0.01806189])]

[101.0, 69.0, 179.0, 185.0, 118.0, 171.0, 166.0, 144.0, 97.0, 168.0]
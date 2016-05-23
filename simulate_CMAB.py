#Simulation Of CMAB
from CMAB import CMAB
from random import randint
from numpy.random import binomial
from operator import mul
import sys
import csv

precision = 3
N_Random_users = 1
N_inter = 24
users = []
N_strategies = 6
# stats = []
# temp = []
total_regret = 0
print "Number of interactions:", N_inter
print "Number of strategies:", N_strategies


datafile = open('one_inter.csv', 'r')
datareader = csv.reader(datafile, delimiter =",")
data = list(datareader)
del data[0]
# print data
for i in xrange(0,len(data)):
	for j in xrange(1,len(data[i])):
		try:
			data[i][j] = float(data[i][j])
		except:
			del data[i] 
users = {dat[0]: [CMAB(N_strategies), dat[1:], [], []] for dat in data}

for j in xrange(N_Random_users):
	temp = []	#Contains user liklihood parameters(P(X=1|strategy)) for the user	
	for i in xrange(N_strategies):
		temp.append(randint(0,10**precision))
	temp = [float(i)/10**precision for i in temp]
	users['rand_user_' + str(j)] = [CMAB(N_strategies), temp, [], []]


print "Number of users:", len(users)
for id in users:
	regret = 0
	# users[id][0] = CMAB(N_strategies)
	for s in xrange(N_inter):
		users[id][0].reward(binomial(1,users[id][1][users[id][0].strategy()]))
	for x in xrange(N_strategies):
		users[id][3].append(int((float(users[id][0].strategies.count(x))/len(users[id][0].strategies))*(10**precision))/(1.0*10**precision))
		users[id][2].append(float(users[id][0].strategies.count(x))/len(users[id][0].strategies))		
	regret = max(users[id][1]) - sum(map(mul,users[id][1],users[id][2]))
	users[id].append(regret)  
	total_regret = total_regret + regret
	# Write some code to calculate regret
	print "User", id, ":"
	print map(list,zip(*[users[id][1], users[id][3]]))	#Contains temp and stats clubbed
	print map(list,zip(*[users[id][0].strategies, users[id][0].rewards]))
	print "Regret:", regret
	
total_regret = total_regret/len(users)
print "Total Regret:", total_regret 
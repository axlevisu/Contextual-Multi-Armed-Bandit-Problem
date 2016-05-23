#Simulation Of CMAB
from CMAB import CMAB
from random import randint
from numpy.random import binomial
from operator import mul
import sys
import csv

def make_user(steps,N):
	user = CMAB(N, steps = steps)
	return user
precision = 3
N_Random_users = 3
N_inter = 100
users = []
N_strategies = 6
# stats = []
# temp = []
total_regret = 0
total_percent = 0
print "Number of interactions:", N_inter
print "Number of strategies:", N_strategies


datafile = open('three_inter.csv', 'r')
datareader = csv.reader(datafile, delimiter =",")
data = list(datareader)
del data[0]
# print data
try:
	steps = int(len(data[0][1:])/N_strategies)
except:
	steps = 1
print "Number Of Steps", steps
for i in xrange(0,len(data)):
	for j in xrange(1,len(data[i])):
		try:
			data[i][j] = float(data[i][j])
		except:
			del data[i] 
users = {dat[0]: [make_user(steps, N_strategies), [dat[1:][j:j+steps] for j in xrange(0, len(dat[1:]), steps)], [], []] for dat in data}


for j in xrange(N_Random_users):
	temp = []	#Contains user liklihood parameters(P(X=1|strategy)) for the user	
	for i in xrange(N_strategies*steps):
		temp.append(randint(0,10**precision))
	temp = [float(i)/10**precision for i in temp]
	temp = [temp[k:k+steps] for k in xrange(0, len(temp), steps)]
	users['rand_user_' + str(j)] = [make_user(steps, N_strategies), temp, [], []]

print "Number of users:", len(users)
for id in users:
	users[id][0] = make_user(steps, N_strategies)
	weights = users[id][0].weights
	for s in xrange(N_inter):
		rewards = [binomial(1,param) for param in users[id][1][users[id][0].strategy()]]
		# try:
		# 	i = rewards.index(0)
		# 	rewards[i:] = [0]*len(rewards[i:])
		# except:
		# 	pass		
		if rewards[0] is 0: rewards = [0]*len(rewards)
		users[id][0].reward(rewards)
	times = 0
	for x in xrange(N_strategies):
		users[id][3].append(int((float(users[id][0].strategies.count(x))/len(users[id][0].strategies))*(10**precision))/(1.0*10**precision))
		users[id][2].append(float(users[id][0].strategies.count(x))/len(users[id][0].strategies))	
	# regret = max(users[id][1]) - sum(map(mul,users[id][1],users[id][2]))
	regret = max([map(mul,x,weights)[0] for x in users[id][1]]) - sum(map(mul, [map(mul,x,weights)[0] for x in users[id][1]], users[id][2]))
	users[id].append(regret)  
	total_regret = total_regret + regret
	percent = regret*100/max([map(mul,x,weights)[0] for x in users[id][1]])
	total_percent = total_percent + percent
	print "User", id, ":"
	print map(list,zip(*[users[id][1], users[id][3]]))	#Contains temp and stats clubbed
	print map(list,zip(*[users[id][0].strategies, users[id][0].rewards]))
	print "Regret:", regret
	print "Regret Percentage:", regret*100/max([map(mul,x,weights)[0] for x in users[id][1]])
	
total_regret = total_regret/len(users)
total_percent = total_percent/len(users)
print "Total Regret:", total_regret 
print "Total Regret Percentage:", total_percent 
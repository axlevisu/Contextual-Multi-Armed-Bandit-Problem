#Simulation Of CMAB
from CMAB import CMAB
from random import randint
from numpy.random import binomial
from operator import mul

precision = 3
N_users = 5
N_inter = 200
# users = []
N_strategies = 6
# stats = []
# temp = []
total_regret = 0
print "Number of interactions:", N_inter
print "Number of strategies:", N_strategies
print "Number of users:", N_users

for j in xrange(N_users):
	temp = []	#Contains user liklihood parameters(P(X=1|strategy)) for the user
	stats =[]	
	stats_trunc =[]	
	regret = 0
	for i in xrange(N_strategies):
		temp.append(randint(0,10**precision))
	temp = [float(i)/10**precision for i in temp]
	# users.append([CMAB(),temp])
	agent = CMAB(N_strategies)
	for s in xrange(N_inter):
		agent.reward(binomial(1,temp[agent.strategy()]))
	for x in xrange(N_strategies):
		stats_trunc.append(int((float(agent.strategies.count(x))/len(agent.strategies))*(10**precision))/(1.0*10**precision))
		stats.append(float(agent.strategies.count(x))/len(agent.strategies))		
	pref_stats = map(list,zip(*[temp, stats_trunc]))
	regret = max(temp) - sum(map(mul,temp,stats))  
	total_regret = total_regret + regret
	# Write some code to calculate regret
	print "User", j, ":"
	print pref_stats	#Contains temp and stats clubbed
	print regret
	# print temp
	# print stats
	# print agent.rewards
	# print agent.strategies
total_regret = total_regret/N_users
print "Total Regret:", total_regret 
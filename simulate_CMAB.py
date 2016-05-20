#Simulation Of CMAB
from CMAB import CMAB
from random import randint
from numpy.random import binomial
from operator import mul

precision = 3
N_Random_users = 0
N_inter = 24
users = []
N_strategies = 6
# stats = []
# temp = []
total_regret = 0
print "Number of interactions:", N_inter
print "Number of strategies:", N_strategies

for j in xrange(N_Random_users):
	temp = []	#Contains user liklihood parameters(P(X=1|strategy)) for the user	
	for i in xrange(N_strategies):
		temp.append(randint(0,10**precision))
	temp = [float(i)/10**precision for i in temp]
	users.append([CMAB(N_strategies), temp, [], []])

users.append([CMAB(N_strategies),[0,0,0,0,0,1],[],[]])
users.append([CMAB(N_strategies),[0,0.5,0,0.5,0,0],[],[]])
users.append([CMAB(N_strategies),[0.2,0.8,0.2,0.8,0.2,0.2],[],[]])
users.append([CMAB(N_strategies),[0.1,0.1,0.1,0.1,0.1,.9],[],[]])
users.append([CMAB(N_strategies),[0.1,0.1,0.1,0.7,0.7,0.8],[],[]])
users.append([CMAB(N_strategies),[0.3,0.3,0.3,0.9,0.3,0.4],[],[]])
users.append([CMAB(N_strategies),[0.2,0.1,0.3,0.4,0.5,.8],[],[]])
users.append([CMAB(N_strategies),[0.2,0.4,0.6,0.8,0.9,.5],[],[]])

u = 0
print "Number of users:", len(users)
for user in users:
	regret = 0
	user[0] = CMAB(N_strategies)
	for s in xrange(N_inter):
		user[0].reward(binomial(1,user[1][user[0].strategy()]))
	for x in xrange(N_strategies):
		user[3].append(int((float(user[0].strategies.count(x))/len(user[0].strategies))*(10**precision))/(1.0*10**precision))
		user[2].append(float(user[0].strategies.count(x))/len(user[0].strategies))		
	regret = max(user[1]) - sum(map(mul,user[1],user[2]))
	user.append(regret)  
	total_regret = total_regret + regret
	# Write some code to calculate regret
	print "User", u, ":"
	print map(list,zip(*[user[1], user[3]]))	#Contains temp and stats clubbed
	print map(list,zip(*[user[0].strategies, user[0].rewards]))
	print "Regret:", regret
	u = u+1
	
total_regret = total_regret/len(users)
print "Total Regret:", total_regret 
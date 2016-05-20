from scipy.stats import beta
from scipy.integrate import quad
from random import randint
import numpy as np
from operator import add



#Contextual Multi-Armed Bandit for Bernoulli Case
class CMAB:
	rewards = []
	strategies = []
	current_strategy = None
	strategy_info = None
	#Constructor
	def __init__(self, number_of_strategies = 6):
		self.N_strategies = number_of_strategies
		#Somehow this should be changed according to average of thetha vectors of other users
		self.Param = [1.0/self.N_strategies]*self.N_strategies    #Optimality Probability Array (P(S|Dt U X))	#D is information available before reward
		self.strategy_info = [[0,0]]*self.N_strategies
		self.current_strategy = randint(0,self.N_strategies-1)
	#Returns strategy 
	def strategy(self): 
		return self.current_strategy
	#This method gives strategy to be used for new reward

	def reward(self, x):
		#Figure Out Why It's not working
		# self.strategy_info[self.current_strategy][0] = (self.strategy_info[self.current_strategy][0]) + x
		# self.strategy_info[self.current_strategy][1] = (self.strategy_info[self.current_strategy][1]) + 1
		self.strategy_info[self.current_strategy] = map(add, [x,1], self.strategy_info[self.current_strategy])
		self.rewards.append(x)
		self.strategies.append(self.current_strategy)
		def wat(x, s_n, ar):
			f = 1
			for i in xrange(len(ar)):
				if i is s_n:
					f = f*beta.pdf(x, ar[i][0] + 1, ar[i][1] - ar[i][0] + 1)	#f(Sa|Dt)	#Dt is information available before reward
				else:
					f = f*beta.cdf(x, ar[i][0] + 1, ar[i][1] - ar[i][0] + 1)	#F(S < Sa|Dt)	#D is information available before reward
			return f
		for i in xrange(self.N_strategies):
			self.Param[i] = quad(wat, 0, 1, args= (i, self.strategy_info))[0]	#Calculate optimality probability
		# print self.strategy_info
		# print self.Param
		m = max(self.Param)
		m_array = [i for i, j in enumerate(self.Param) if j == m]
		try:
			self.current_strategy = m_array[randint(0,len(m_array)-1)]
		except:
			self.current_strategy = m_array[0]
		return self.current_strategy


def main():
	pass

if __name__ == '__main__':
	main()
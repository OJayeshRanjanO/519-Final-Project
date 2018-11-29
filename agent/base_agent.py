import pdb
from agent.stateEngine import *
import random
class Agent(object):
	def __init__(self, id):
		self.id = id

	def getBMSTDecision(self, state):
		s = State(self.id,state)
		if s.agentLiquidCash() < s.agentDebt():#PAY OFF ALL DEBT
			try:
				for i in s.agentProperties():
					if abs(i) == 1:
						return ("B",[i])
			except:
				pass

		return None

	def respondTrade(self, state):
		return False

	def buyProperty(self, state):
		s = State(self.id,state)
		if s.getPhaseInfo() <= s.agentLiquidCash():
			return True
		return False

	def auctionProperty(self, state):
		s = State(self.id,state)
		print(state)
		return random.randrange(0,s.getPhaseInfo())

	def jailDecision(self, state):
		s = State(self.id,state)
		if s.agentGetOutOfJail() != 0:
			return ("C",s.agentGetOutOfJail())
		if len(s.opponentProperties())/28 > 0.25: #If 50% owned by opponent
			return ("R")#Simply roll or wait
		if s.agentLiquidCash() >= 50:
			return ("C")
		else:
			return ("R")
	
	def receiveState(self, state):
		print(state)
		return None

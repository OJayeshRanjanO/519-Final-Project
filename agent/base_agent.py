import pdb
from agent.stateEngine import *
import random

class Agent(object):
:q	def __init__(self, id):
		self.id = id

	def getBMSTDecision(self, state):
		s = State(self.id,state)
		debt = s.agentLiquidCash() - s.agentDebt()

		if(debt < 0):
			buyOff = []
			for prop in s.agentProperties():
				if(debt > 0):
					break

				v = abs(s.properties()[prop])
				p = board[prop]["price"]//2
				if(v == 1):
					buyOff.append(prop)
					debt += p

			if(buyOff):
				return ("M", buyOff)
		

		return True

	def respondTrade(self, state):
		return False

	def buyProperty(self, state):
		s = State(self.id,state)
		if s.getPhaseInfo() <= s.agentLiquidCash()*0.5:
			return True
		return False

	def auctionProperty(self, state):
		s = State(self.id,state)
		# print(state)
		return random.randrange(0,s.getPhaseInfo())

	def jailDecision(self, state):
		s = State(self.id,state)
		if s.agentJailCards() != 0:
			return ("C",s.agentJailCards())
		if len(s.opponentProperties())/28 > 0.25: #If 50% owned by opponent
			return ("R")#Simply roll or wait
		if s.agentLiquidCash() >= 50:
			return ("C")
		else:
			return ("R")
	
	def receiveState(self, state):
		# print(state)
		return None

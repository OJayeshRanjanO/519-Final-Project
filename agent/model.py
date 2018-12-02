from agent.stateEngine import *
import random
from agent.lookup import board

class Oracle(object):
	def getExpected_Short(self, state):
		return 10

	def getExpected_Medium(self, state):
		return 10

	def getExpected_Long(self, state):
		return 10

	def getRegression(self, state):
		return state

	def getComparison(self, state1, state2):
		v1 = self.getRegression(state1)
		v2 = self.getRegression(state2)
		return v1 - v2

	def getValue(self, state, state_prev):
		short  = self.getExpected_Short(state)
		medium = self.getExpected_Medium(state)
		long   = self.getExpected_Long(state)
		rgrss  = self.getComparison(state, state_prev)
		return short + medium + long + rgrss

	def action(self, modList, original_state):
		f = lambda v: self.getValue(v, original_state)
		vals = [(i, f(m)) for i, m in enumerate(modList, 0)]
		vals = sorted(vals, key=lambda k: k[1], reverse=True)
		return vals[0][0]


class Agent(object):
	def __init__(self, id):
		self.id = id

	def getBMSTDecision(self, state):
		s = State(self.id, state)

	def respondTrade(self, state):
		s = State(self.id, state)

	def buyProperty(self, state):
		s = State(self.id, state)

	def auctionProperty(self, state):
		s = State(self.id, state)

	def jailDecision(self, state):
		s = State(self.id, state)

	def receiveState(self, state):
		s = State(self.id, state)

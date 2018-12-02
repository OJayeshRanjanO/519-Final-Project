from agent.stateEngine import *
import random
from agent.lookup import board
from random import randint as rand

class RandomWalk(object):
	
	def __init__(self, s_len=5, m_len=15, l_len=30):
		rollNum = 10000
		self.dice = [rand(1, 6) + rand(1, 6) for i in range(rollNum)]
		self.l_len = l_len
		self.s_len = s_len
		self.m_len = m_len

	def walk(self, player, target):
		s, m, l = 0, 0, 0
		roll = lambda c: (c + self.dice.pop()) % 40
		curr = roll(player)
		prev = player
		for n in range(self.l_len):
			if(prev < target < curr):
				l += 1
				if(n < self.s_len):
					s += 1
				if(n < self.m_len):
					m += 1
			prev = currs
			curr = roll(curr)
		return (s, m, l)

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

	def getValue(self, state):
		short  = self.getExpected_Short(state)
		medium = self.getExpected_Medium(state)
		long   = self.getExpected_Long(state)
		rgrss  = self.getRegresion(state)
		return short + medium + long + rgrss

	def getComparison(self, state, state_prev):
		return self.getValue(state) - self.getValue(state_prev)

	def action(self, modList, original_state):
		modList = [original_state] + modList
		f = lambda v: self.getValue(v, original_state)
		vals = [(i, f(m)) for i, m in enumerate(modList, 0)]
		vals = sorted(vals, key=lambda k: k[1], reverse=True)
		return vals[0][0]

class Agent(object):
	def __init__(self, id):
		self.id = id
    self.oracle = Oracle()

	def getBMSTDecision(self, state):
		s = State(self.id, state)

	def respondTrade(self, state):
		s = State(self.id, state)

	def buyProperty(self, state):
		s = State(self.id, state)
		cost = s.getPhaseInfo()
		ind = s.getBuyPropertyIndex()

		if(s.agentAgentLiquidCash() > cost):
			mod_s = s.clone()
			mod_s.agentBuyProperty(ind, cost)
      return self.oracle.action([mod_s], s) > 0

	def auctionProperty(self, state):
		s = State(self.id, state)

	def jailDecision(self, state):
		s = State(self.id, state)

	def receiveState(self, state):
		s = State(self.id, state)

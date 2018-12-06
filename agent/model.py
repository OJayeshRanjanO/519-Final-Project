from agent.stateEngine import *
import random
from agent.lookup import board
from random import randint as rand
import pdb

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
			prev = curr
			curr = roll(curr)
		return (s, m, l)

class Oracle(object):
	def __init__(self, player_index):
		self.walk = RandomWalk()
		self.agent = player_index

	def getExpectations(self, state, origin, target, revenue, cost):
		vals = self.walk.walk(origin, target)
		vals = [(.6*v*revenue)-cost for v in vals]
		return tuple(vals)

	def getRegression(self, state):
		regressors = [1, 1]
		reg1 = regressors[state.agentIndex()]-state.agentNetWealth()
		reg2 = regressors[state.opponentIndex()]-state.opponentNetWealth()
		return reg1 - reg2

	def getValue(self, state, p_id, t_pos, cost, bought):
		rev = max(state.getRent(p_id, t_pos), state.getRent((p_id+1)%2, t_pos))
		if(not bought):
			rev *= -1
		
		p_pos = state.positions()[p_id]
		s,m,l = self.getExpectations(state, p_pos, t_pos, rev, cost)

		rgrss  = self.getRegression(state)
		return s + .75*m + .75*.75*l + rgrss

	# modList = [(p_id, [(b_id, s_id, [(prop, val, bought)], c, b_c, s_c),...]),...]
	def action(self, modList, state, closeToZero=False):
		modList = [(0, []),] + modList
		values  = []
		for index, (p_id, mods) in enumerate(modList, 0):
			s_mod = state.clone()
			s_mod.updateProperties(mods)
			value = 0
			count = 0
			if(index > 0):
				for b_id, s_id, props, cost, b_cost, s_cost in mods:
					for p, val, bought in props:
						value += self.getValue(s_mod, p_id, p, (1.0*cost)/len(props), bought)
						count += 1
			else:
				value = self.getRegression(s_mod)
			value /= float(max(count, 1))
			values.append((index, value))
	
		values = sorted(values, key=lambda k: k[1], reverse=True)
		if(closeToZero):
			for (ind, (k, v)) in enumerate(values, 0):
				if(k==0):
					return ind-1
		else:
			return values[0][0] - 1

class Agent(object):
	def __init__(self, id):
		self.id = id
		self.oracle = Oracle(id)

	def getBMSTDecision(self, state):
		s = State(self.id, state)

	def respondTrade(self, state):
		s = State(self.id, state)
		c_offer, p_offer, c_req, p_req = s.getTradeInfo()
		opp_id = s.opponentIndex()
		agent_id = s.agentIndex()

		mods = []
		vals =  [(p, 1, 1) for p in p_offer]
		vals += [(p, 1, 0) for p in p_req]
		mod = (opp_id, [(agent_id, opp_id, vals, c_offer-c_req, c_req, c_offer)])
		
		enoughMoney = s.agentLiquidCash() > (c_offer - c_req)
		action = self.oracle.action([mod], s)

		return enoughMoney and action >= 0

		
	def buyProperty(self, state):
		s = State(self.id, state)
		cost = s.getPhaseInfo()
		ind = s.getBuyPropertyIndex()
		opp_id = s.opponentIndex()
		agent_id = s.agentIndex()

		enoughMoney = s.agentLiquidCash() > cost
		mods = [(opp_id, [(agent_id, 0, [(ind, 1, 1)], cost, cost, 0)])]
		action = self.oracle.action(mods, s)

		return enoughMoney and action >= 0


	def auctionProperty(self, state):
		s = State(self.id, state)
		opp_id = s.opponentIndex()
		agent_id = s.agentIndex()
		cost = s.getPhaseInfo()
		ind = s.getBuyPropertyIndex()
		
		mods   = []
		amtMod = 10
		pctMod = 0.1
		for i in range(1, amtMod+1):
			c = cost*(i*pctMod)
			mods.append((opp_id, [(agent_id, 0, [(ind, 1, 1)], c, c, 0)]))

		baseWilling = s.agentLiquidCash()*0.3
		expctAmount = self.oracle.action(mods, s, closeToZero=True)*pctMod*cost
		prevAmount  = 0.55*cost

		return int((expctAmount > 0) * (min(baseWilling, max(expctAmount, prevAmount))))


	def jailDecision(self, state):
		s = State(self.id, state)
		j_thresh = 0.3
		o_ratio = len(s.opponentProperties()) / 28.0
		if(o_ratio < j_thresh):
			card = s.agentJailCards()
			if(card):
				return ("C", card)
			elif(s.agentLiquidCash() > 200):
				return ("P", )
		return ("R", )
			

	def receiveState(self, state):
		s = State(self.id, state)

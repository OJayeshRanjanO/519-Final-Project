from agent.stateEngine import *
import random
from agent.lookup import board
from random import randint as rand
import pdb
import csv
import collections
from os.path import abspath, exists

class RandomWalk(object):
	
	def __init__(self, s_len=5, m_len=15, l_len=30):
		rollNum = int(1e2)
		self.dice = [rand(1, 6) + rand(1, 6) for i in range(rollNum)]
		self.l_len = l_len
		self.s_len = s_len
		self.m_len = m_len
		self.regression_vectors = []


	def loadRegressors(self):
		f_path = abspath("weight_vectors.csv")
		if exists(f_path):
			file = open(f_path)
			reader = csv.reader(file, delimieter=",")

			for row in reader:
				self.regression_vectors.append(row)

			file.close()


	def walk(self, player, target):
		s, m, l = 0, 0, 0
		roll = lambda c: (c + self.dice.pop()) % 40
		repl = lambda c: self.dice.insert(0, c)
		curr = roll(player)
		repl(curr)
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
			repl(curr)

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
		debt = s.agentDebt() - s.agentLiquidCash()
		if(debt > 0):
			# Mortgage Properties First
			props = sorted(s.agentUnbuiltProperties(), key=lambda k: board[k]['price'])
			gains = [board[p]['price']//2 for p in props]
			mortgage = []
			for i in range(1, len(props)+1):
				if(sum(gains[:i]) > debt):
					mortgage = props[:i]
					break
			if(mortgage):
				return ("M", tuple(mortgage))

			#Sell houses is possible
			props = sorted(s.seeSellHouse(), key=lambda k: board[k]['price'])		
			to_sell = []
			while props and debt > 0:
				h_sell = props[0]
				to_sell.append(h_sell)
				s.setSellHouse(h_sell)
				debt -= board[h_sell]['build_cost']//2
				props = sorted(s.seeSellHouse(), key=lambda k: board[k]['price'])		
			if(to_sell):
				return ("S", collections.Counter(to_sell).most_common())

			return None
		else:
			pos_acts = []
			#I would start buy unmortaging properties
			#sorted by most to least valuable
			props = sorted(s.agentMortgagedProperties(), key=lambda k: board[k]['price'], reverse=True)
			cost = [(board[p]['price'] * .55) for p in props]  
			unmortgage = []
			money_to_spend = s.agentLiquidCash() * .40
			mortgage_cost = 0
			
			#Go down the list, see what what amalgamation of properties you can
			#Unmortage based on some proportion of your cash on hand.
			#Really should be based on expectation and board state buuuuuut
			#that's okay 
			for i in range(0, len(props)):
				if(cost[i] <= money_to_spend):
					unmortgage.append(props[i])
					money_to_spend -= cost[i]
					mortgage_cost += cost[i]
			if(unmortgage):
				pos_acts.append((s.opponentIndex(),[(s.agentIndex(), 0, [(p, 1, 1) for p in unmortgage], mortgage_cost, mortgage_cost, 0 )]))

			#Grab all properties that we could possibly build on
			props = sorted(s.seeBuyHouse(), key=lambda k: board[k]['build_cost'])
			houses_to_buy = []
			build_cost = 0
			#Set a buy threshold
			money_to_spend = s.agentLiquidCash() * .50
			while(props and money_to_spend > 0):
				buy = props[0]
				cost_h = board[buy]['build_cost']//2
				something = money_to_spend - cost_h


				if(something <= money_to_spend):
					money_to_spend = something
					houses_to_buy.append(buy)
					s.setBuyHouse(buy)
					build_cost += cost_h
					props = sorted(s.seeBuyHouse(), key=lambda k: board[k]['build_cost'])
				else:
					break

			if(houses_to_buy):
				pos_acts.append((s.opponentIndex(),[(s.agentIndex(), 0, [(p, abs(s.properties()[p])+1, 1) for p in houses_to_buy], build_cost, build_cost, 0)]))

		# Build a world for generating trades
		needed_props = s.agentToCompleteMonopoly(need=1)
		#If the opponent has a property that completes a monopoly
		current_monies = s.agentLiquidCash() * 0.6

		toTrade = [0, [], 0, []]
		if(needed_props):
			allotment = current_monies * .6
			how_many = len(needed_props)
			props = sorted([p[0] for p in needed_props], key=lambda k: board[k]['price'])
			if(props):
				props = props[0]
				costs = board[props]['price']
				if(costs <= allotment):
					toTrade[3].append(props)
					toTrade[0] += costs
					current_monies += -costs

		else:
			allotment = current_monies *.15
			opp_monopolies = s.opponentMonopolies()
				
			if(opp_monopolies):
				opp_monopolies = opp_monopolies[0][0]
				toTrade[3].append(opp_monopolies)
				toTrade[0] = allotment
				current_monies -= allotment
			else:
				opp_needed = s.opponentToCompleteMonopoly(need=1)
				props = sorted([p[0] for p in needed_props], reverse=True, key=lambda k: board[k]['price'])
				if(props):
					props = props[0]
					toTrade[1].append(props)
					toTrade[2] = s.opponentLiquidCash()*.8

		c_offer, p_offer, c_req, p_req = toTrade
		vals =  [(p, 1, 0) for p in p_offer]
		vals += [(p, 1, 1) for p in p_req]
		opp_id = s.opponentIndex()
		agent_id = s.agentIndex()
		mod = (opp_id, [(agent_id, opp_id, vals, c_req-c_offer, c_offer, c_req)])
		pos_acts.append(mod)

		# Generate the best action
		action = self.oracle.action(pos_acts, s)
		if(action < 0):
			return None
		elif(action == 0):
			return ("M", unmortgage)
		elif(action == 1):
			
			return ("B", collections.Counter(houses_to_buy).most_common())
		else:
			return ["T"] + toTrade


	def respondTrade(self, state):
		s = State(self.id, state)
		c_offer, p_offer, c_req, p_req = s.getTradeInfo()

		c_offer += sum([50 for p in p_offer if p >= 40])
		c_req   += sum([50 for p in p_req if p >= 40])

		p_offer = [p for p in p_offer if p < 40]
		p_req   = [p for p in p_req if p < 40]

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

		cost = min(s.opponentLiquidCash(), min(baseWilling, max(expctAmount, prevAmount)))

		return int((expctAmount > 0) * (cost))


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

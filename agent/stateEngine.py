import lookup

def same_sign(x, y):
	return (x < 0 and y < 0) or (x > 0 and y > 0)

class State(object):
	def __init__(self, iden, state):
		self.state = state[:-1]
		self.iden = iden

	## BASE VALUES EXTRACTED FROM STATE

	def currentTurnNumber(self):
		return self.state[0]

	def agentIndex(self):
		return self.iden % 2
	
	def opponentIndex(self):
		return (self.iden + 1) % 2

	def agentSign(self):
		return (-1)**(self.agentIndex())

	def opponentSign(self):
		return (-1)**(self.opponentIndex())

	def positions(self):
		return self.state[2]
	
	def agentPosition(self):
		return self.positions()[self.agentIndex()]
	
	def opponentPosition(self):
		return self.positions()[self.opponentIndex()]

	def liquidCash(self):
		return self.state[3]

	def agentLiquidCash(self):
		return self.cash()[self.agentIndex()]

	def opponentLiquidCash(self):
		return self.cash()[self.opponentIndex()]

	def debt(self):
		return self.state[6]

	def agentDebt(self):
		self.debt()[(2*self.agentIndex()) + 1]

	def opponentDebt(self):
		self.debt()[(self.opponentIndex()) + 1]

	def properties(self):
		return self.state[1][:-2]


#    1, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
#(11, 0), (1360, 1500), 2, (5, 4, False), (0, 0, 0, 0)


	## DERIVED FEATURES ABOUT PLAYERS
	def agentLiquidAsset(self):
		liquidAsset = 0
		for i in range(len(self.state[1])):
			if 1 < self.state[i] < 7:#Player 1# i = 2 - 6
				liquidAsset+= ((board[i])['build_cost'] * (self.state[i] -1))/2 + ((board[i])['price'])/2
			elif self.state[i] == 1:
				liquidAsset+=(board[i])['price']/2
		return liquidAsset
	
	def opponentLiquidAsset(self):
		liquidAsset = 0
		for i in range(len(self.state[1])):
			if -7 < self.state[i] < -1:#Player 2# i = -2 - -6
				liquidAsset+= ((board[i])['build_cost'] * ((self.state[i] +1) * -1))/2 + ((board[i])['price'])/2
			elif self.state[i] == -1:
				liquidAsset+=(board[i])['price']/2
		return liquidAsset 

	def agentNetWealth(self):
		value = self.agentLiquidCash()
		for i, p in enumerate(self.properties):
			propValue = 0
			if(same_sign(self.agentSign(), p)):
				propValue += lookup.board[i]["price"]
				if(abs(p) == 7):
					propValue /= 2
				else:
					propValue += ((abs(p)-1)*lookup.board[i]["build_cost"])
			value += propValue
		return value
	
	def opponentNetWealth(self):
		value = self.opponentLiquidCash()
		for i, p in enumerate(self.properties):
						propValue = 0
						if(same_sign(self.opponentSign(), p)):
				propValue += lookup.board[i]["price"]
				if(abs(p) == 7):
					propValue /= 2
				else:
					propValue += ((abs(p)-1)*lookup.board[i]["build_cost"])
			value += propValue
		return value

	def agentProperties(self):
		#valid = lambda p: same_sign(
		#return [p for p in self.properties if ]

	def opponentProperties(self):
		pass

	def agentMonopolies(self):
		pass

	def opponentMonopolies(self):
		pass

	## DERIVED FEATURES ABOUT THE GAME

	def housesUsed(self):
		valid = lambda h: abs(h) > 1 and abs(h) < 6
		return sum([abs(h)-1 for h in self.properties() if valid(h)])

	def housesLeft(self):
		return 32 - self.housesUsed()

	def hotelsUsed(self):
		valid = lambda h: abs(h) == 6
		return sum([1 for h in self.properties() if valid(h)])

	def hotelsLeft(self):
		return 12 - self.hotelsUsed()

	def propertiesOwned(self):
		valid = lambda p: abs(p) != 0
		return sum([1 for p in self.properties() if valid(p)])

	def propertiesMortgaged(self):
		valid = lambda p: abs(p) == 7
		return sum([1 for p in self.properties() if valid(p)])

	def totalLiquidCash(self):
		pass

	def totalLiquidAssets(self):
		pass

	def totalWealth(self):
		pass

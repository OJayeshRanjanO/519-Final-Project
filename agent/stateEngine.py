import lookup
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


	## DERIVED FEATURES ABOUT THE GAME
	def homesLeft(self):
		pass

	def homesUsed(self):
		pass

	def hotelsLeft(self):
		pass 

	def hotelsUsed(self):
		pass

	def totalLiquidCash(self):
		pass

	def totalLiquidAssets(self):
		pass

	def totalWealth(self):
		pass

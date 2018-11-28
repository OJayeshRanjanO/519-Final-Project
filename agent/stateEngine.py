
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
		return self.debt()[(2*self.agentIndex()) + 1]

	def opponentDebt(self):
		return self.debt()[(self.opponentIndex()) + 1]

	## DERIVED FEATURES ABOUT PLAYERS
	def agentLiquidAsset(self):
		pass
	
	def opponentLiquidAsset(self):
		pass

	def agentNetWealth(self):
		pass
	
	def opponentNetWealth(self):
		pass

	def agentProperties(self):
		pass

	def opponentProperties(self):
		pass

	def agentMonopolies(self):
		pass

	def opponentMonopolies(self):
		pass


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

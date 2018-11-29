from lookup import board

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
		return self.iden - 1 
	
	def opponentIndex(self):
		return (self.agentIndex() + 1) % 2

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
		return self.liquidCash()[self.agentIndex()]

	def opponentLiquidCash(self):
		return self.liquidCash()[self.opponentIndex()]

	def debt(self):
		return self.state[6]

	def agentDebt(self):
		return self.debt()[(2*self.agentIndex()) + 1]

	def opponentDebt(self):
		return self.debt()[(self.opponentIndex()) + 1]

	def properties(self):
		return self.state[1][:-2]


	## DERIVED FEATURES ABOUT PLAYERS

	def agentLiquidAsset(self):
		return self.calculateLiquidAsset(self.agentSign())

	def opponentLiquidAsset(self):
		return self.calculateLiquidAsset(self.opponentSign())

	def calculateLiquidAsset(self,sign):
		same = lambda p: same_sign(sign, p)
		props = [(i,abs(p)) for i,p in enumerate(self.properties()) if same(p)]
		val =  sum([board[i]["price"]/2 for i,p in props if p < 7])
		val += sum([(board[i]["build_cost"]/2)*(p-1) for i,p in props if p < 7])
		return val

	def calculateNetWealth(self, sign):
		same = lambda p: same_sign(sign, p)
		props = [(i,abs(p)) for i,p in enumerate(self.properties()) if same(p)]
		val =  sum([board[i]["price"] for i,p in props if p < 7])
		val += sum([board[i]["price"]/2 for i,p in props if p == 7])
		val += sum([board[i]["build_cost"]*(p-1) for i,p in props if p < 7])
		return val
		
	def agentNetWealth(self):
		value = self.calculateNetWealth(self.agentSign())
		return value + self.agentLiquidCash()
	
	def opponentNetWealth(self):
		value = self.calculateNetWealth(self.opponentSign())
		return value + self.opponentLiquidCash()

	def agentProperties(self):
		valid = lambda p: same_sign(self.agentSign(), p)
		return [i for i, p in enumerate(self.properties()) if valid(p)]

	def opponentProperties(self):
		valid = lambda p: same_sign(self.opponentSign(), p)
		return [i for i, p in enumerate(self.properties()) if valid(p)]

	def calculateMonopolies(self, properties):
		monopolies = {}
		for p in properties:
			group = board[p]["monopoly"]
			if(not group in monopolies):
				monopolies[group] = [0, board[p]["monopoly_size"]]
			monopolies[group][0] += 1
		return sum([1 for k in monopolies if monopolies[k][0] == monopolies[k][1]])

	def agentMonopolies(self):
		return self.calculateMonopolies(self.agentProperties())

	def opponentMonopolies(self):
		return self.calculateMonopolies(self.opponentProperties())

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
		return self.agentLiquidCash() + self.opponentLiquidCash()

	def totalLiquidAssets(self):
		return  self.agentLiquidAsset() + self.opponentLiquidAsset()

	def totalWealth(self):
		return self.agentNetWealth() + self.opponentNetWealth()

from stateEngine import State

class Agent(object):
	def __init__(self, id):
		self.id = id

	def getBMSTDecision(self, state):
		state = State(self.id, state)
		return False

	def respondTrade(self, state):
		state = State(self.id, state)
		print(state)
		return False

	def buyProperty(self, state):
		state = State(self.id, state)
		print(state)
		return True

	def auctionProperty(self, state):
		state = State(self.id, state)
		print(state)
		return True

	def jailDecision(self, state):
		state = State(self.id, state)
		print(state)
		return False
	
	def receiveState(self, state):
		return None

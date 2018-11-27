import pdb

class Agent(object):
	def __init__(self, id):
		self.id = id

	def getBMSTDecision(self, state):
		print(state)
		return True

	def respondTrade(self, state):
		print(state)
		return False

	def buyProperty(self, state):
		print(state)
		return True

	def auctionProperty(self, state):
		print(state)
		return True

	def jailDecision(self, state):
		print(state)
		return False
	
	def receiveState(self, state):
		print(state)
		return None

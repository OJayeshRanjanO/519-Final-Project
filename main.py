import pdb
import itertools
import json
#from agent import base_agent
#from adjudicator import Adjudicator
#import random
#
#def getAgent():
#	agents = [base_agent.Agent]
#	ind = random.randint(0, len(agents)-1)
#	return agents[ind]
#
#amount = 100
#adj = Adjudicator()
#for i in range(amount):
#	a1, a2 = getAgent(), getAgent()
#	for i in range(2):
#		adj.runGame(a1(i%2), a2((i+1)%2))
#

with open("monopoly.log", "r") as fp:
	lines = fp.readlines()
	valid = lambda l: "end of the turn" in l
	state_ind = [i+1 for i, l in enumerate(lines) if valid(l)]
	state = [json.loads(lines[i].lower()) for i in state_ind]
	[(s.pop(5), s.pop(4)) for s in state]
	flatten = lambda l: list(itertools.chain.from_iterable(l))
	state = [[s[0]] + flatten(s[1:]) for s in state]
	state = [json.dumps(s)[1:][:-1] for s in state]
	state = "\n".join(state)
	with open("output.csv", "w") as wr:
		wr.write(state)

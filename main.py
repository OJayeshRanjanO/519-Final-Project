import itertools
import json
import os.path
import random

if (not os.path.isfile('monopoly.log')):
	from agent import flagship_agent, kid_agent, drunk_agent, probabilistic_agent, cheapskate_agent, asset_hoarder_agent
	from adjudicator import Adjudicator
	
	def getAgent():
		agents = [flagship_agent, kid_agent, drunk_agent, probabilistic_agent, cheapskate_agent, asset_hoarder_agent]
		ind = random.randint(0, len(agents)-1)
		return agents[ind].Agent
	
	amount = 100
	adj = Adjudicator()
	for i in range(amount):
		print("Batch %d/%d"%(i+1, amount))
		a1, a2 = getAgent(), getAgent()
		for j in range(20):
			for k in range(2):
				adj.runGame(a1(k%2), a2((k+1)%2))
	
header = ["turn"]
header += ["property_%d" % i for i in range(1, 41)]
header += ["jail_card_%d" % i for i in range(1, 3)]
header += ["agent_position_%d" % i for i in range(1, 3)]
header += ["agent_cash_%d" % i for i in range(1, 3)]
header += ["agent_%d_owed, agent_%d_debt"%(i,i) for i in range(1, 3)]
header =  ", ".join(header) + "\n"

with open("monopoly.log", "r") as fp:
	lines = fp.readlines()
	valid = lambda l: "end of the turn" in l
	state_ind = [i+1 for i, l in enumerate(lines) if valid(l)]
	state = [json.loads(lines[i].lower()) for i in state_ind]
	[(s.pop(5), s.pop(4)) for s in state]
	flatten = lambda l: list(itertools.chain.from_iterable(l))
	state = [[s[0]] + flatten(s[1:]) for s in state]
	state = [json.dumps(s)[1:][:-1] for s in state]
	with open("output.csv", "w") as wr:
		wr.write(header)
		for s in state:
			wr.write(s)
			wr.write("\n")

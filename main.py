from agent.base_agent import Agent
from adjudicator import Adjudicator

adj = Adjudicator()
agentOne = Agent(1)
agentTwo = Agent(2)

adj.runGame(agentOne, agentTwo)

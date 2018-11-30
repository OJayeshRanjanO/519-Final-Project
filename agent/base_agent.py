import pdb
from agent.stateEngine import *
import random
import copy


class Agent(object):
    def __init__(self, id):
        self.id = id
        self.buyPct = 0.4

    def getBMSTDecision(self, state):
        s = State(self.id, state)
        debt = s.agentLiquidCash() - s.agentDebt()

        if (debt < 0):#Trying to get money by mortgaging properties
           	sellOff = []
            for prop in s.agentProperties():
                if (debt > 0):
                    break

                v = abs(s.properties()[prop])
                p = board[prop]["price"] // 2
                if (v == 1):
                    sellOff.append(prop)
                    debt += p
            if(sellOff):
                # print(buyOff)
                return ("M", sellOff)

        # This is when we sell houses if we couldn't mortgage anything or have debt left
            listHousesToSell = {}
            continueLoop = True
            monopolies = s.getAgentMonopolies()
            while continueLoop:
                continueLoop = False
                for index in monopolies:
                    if s.agentSign() == 1:
                        eachMonopoly = sorted(monopolies[index].items(), key=lambda x: x[1], reverse=True)#Sort by reverse order of houses bought for +1
                    elif s.agentSign() == -1:
                        eachMonopoly = sorted(monopolies[index].items(), key=lambda x: x[1])#Sort by reverse order of houses bought for -1
                    for prop in eachMonopoly:  # prop is the (index of property, num houses on propery) #Should not cause issues with eachMonopoly as agentSign() is +1 or -1
                        if (debt >= 0):#Try to break the loops if debt can be resolved
                            continueLoop = False
                            break
                        v = abs(s.properties()[prop[0]])  # This gives us the value associated with the property 1 - 7
                        p = board[prop[0]]["build_cost"] // 2
                        if (1 < v < 7):
                            listHousesToSell.setdefault(prop[0], 0)  # Add to dictionary with 0 houses
                            if (listHousesToSell[prop[0]] < v - 1):  # 2 - 6
                                listHousesToSell[prop[0]] += 1
                                continueLoop = True
                                debt += p

            sellHousesList = []
            for i in listHousesToSell:
                if 0 < listHousesToSell[i]:
                    sellHousesList.append((i, listHousesToSell[i]))
            # print(sellHousesList)
            return ("S",sellHousesList)

        #AFTER THE PLAYER HAS BECOME DEBT FREE
        #PLAYER TRIES TO UNMORTGAGE ALL PROPERTIES
        if debt == 0:
        	buyOff = []
	        money_spent = 0
	        money = s.agentLiquidCash()        
	        for prop in s.agentProperties():
	        	v = abs(s.properties()[prop])
                if (v == 7):
                	p = (board[prop]["price"] // 2) * 1.1 #10% interest on mortgage price
                	if money_spent+p > money * self.buyPct:#If money_spent + p is more than 40% (self.buyPct) of original money - Stop purchasing
                		break
                	buyOff.append(prop)
                	money_spent+=p
            if buyOff:
            	return ("M", buyOff)

	        #PLAYER TRIES TO BUY HOUSES
	        monopolies = s.getAgentMonopolies()
	        if len(monopolies) != 0:
	            continueLoop = True
	            monopolies = s.getAgentMonopolies()
	            money = s.agentLiquidCash()
	            money_spent = 0
	            listHousesToBuy = {}
	            while continueLoop:
	                continueLoop = False
	                for index in monopolies:
	                    if s.agentSign() == -1:
	                        eachMonopoly = sorted(monopolies[index].items(), key=lambda x: x[1], reverse=True)#Tile with the least number of houses comes first if agent is -1
	                    elif s.agentSign() == 1:
	                        eachMonopoly = sorted(monopolies[index].items(), key=lambda x: x[1])#Tile with the least number of houses comes first if agent is +1
	                    for prop in eachMonopoly:#Should not cause issues with eachMonopoly as agentSign() is +1 or -1
	                        v = abs(s.properties()[prop[0]])  # This gives us the value associated with the property 1 - 7
	                        p = board[prop[0]]["build_cost"]
	                        if (money_spent+p >= money*self.buyPct):#Try to break loop if money spent + next house cost is more than 40% (self.buyPct) of available cash
	                            continueLoop = False
	                            break
	                        if (0 < v < 6):#property is already bought and is not a hotel or mortgaged
	                            listHousesToBuy.setdefault(prop[0], 0)  # Add to dictionary with 0 houses
	                            listHousesToBuy[prop[0]] += 1
	                            continueLoop = True
	                            money_spent += p
	            buyHousesList = []
	            for i in listHousesToBuy:
	                if 0 < listHousesToBuy[i]:
	                    buyHousesList.append((i, listHousesToBuy[i]))
	            # print(buyHousesList)
	            return ("B",buyHousesList)
        return True

    def respondTrade(self, state):
        return False

    def buyProperty(self, state):
        s = State(self.id, state)
        if s.getPhaseInfo() <= s.agentLiquidCash() * 0.5:
            return True
        return False

    def auctionProperty(self, state):
        s = State(self.id, state)
        # print(state)
        return random.randrange(0, s.getPhaseInfo())

    def jailDecision(self, state):
        s = State(self.id, state)
        if s.agentJailCards() != 0:
            return ("C", s.agentJailCards())
        if len(s.opponentProperties()) / 28 > 0.25:  # If 50% owned by opponent
            return ("R")  # Simply roll or wait
        if s.agentLiquidCash() >= 50:
            return ("C")
        else:
            return ("R")

    def receiveState(self, state):
        # print(state)
        return None

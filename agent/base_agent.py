import pdb
from agent.stateEngine import *
import random
import copy


class Agent(object):
    def __init__(self, id, _bmst_modifier=0.2,_buyPct=0.4,_jailStay=0.25,_buy_prop=0.5):
        self.id = id
        self._buyPct = _buyPct
        self._jailStay = _jailStay
        self._buy_prop = _buy_prop
        self._auction_prop = _auction_prop
        self._bmst_modifier = _bmst_modifier



    ######## HELPER FUNCTIONS FOR BSMT ########


    def _mortgageProps(self,debt,s):
        sellOff = []
        agent_properties = [i for i in s.agentProperties()]
        random.shuffle(agent_properties)#Pick any property for mortgage
        for prop in agent_properties:
            if (debt > 0):
                break

            v = abs(s.properties()[prop])
            p = board[prop]["price"] // 2
            if (v == 1):
                sellOff.append(prop)
                debt += p
        return sellOff

    def _sellHouses(self,debt,s):
        # This is when we sell houses if we couldn't mortgage anything or have debt left
        listHousesToSell = {}
        continueLoop = True
		monopolies = [i for i in s.getAgentMonopolies()]
        random.shuffle(monopolies)#Pick any random monopoly
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
        return sellHousesList

    def getBMSTDecision(self, state):
        s = State(self.id, state)
        debt = s.agentLiquidCash() - s.agentDebt()

        #SIMPLY RESOLVE DEBT AND DO NOTHING ELSE
        if (debt < 0):#Trying to get money by mortgaging properties
            sellOff = self._mortgageProps(debt,s)
            if sellOff:
                return ("M", sellOff)

            sellHousesList = self._sellHouses(debt,s)
            if sellHousesList:
                return ("S",sellHousesList)

        return False

    def respondTrade(self, state):
        return False

    def buyProperty(self, state):
        s = State(self.id, state)
        if s.getPhaseInfo() <= s.agentLiquidCash():#If I have money, I will buy the property
            return True
        return False

    def auctionProperty(self, state):
        s = State(self.id, state)
        #Auction for 1 less than the same price
        return s.getPhaseInfo()-1

    def jailDecision(self, state):
        s = State(self.id, state)
        if s.agentJailCards() != 0:#Use cards if I have them
            return ("C", s.agentJailCards())
        elif s.agentLiquidCash() >= 50: #If I have money I will spend it
            return ("C")
        else:
            return ("R")

    def receiveState(self, state):
        # print(state)
        return None




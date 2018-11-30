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

    def _mortgageProps(self,money,s):
        sellOff = []
        for prop in s.agentProperties():
            if (money > 0):
                break

            v = abs(s.properties()[prop])
            p = board[prop]["price"] // 2
            if (v == 1):
                sellOff.append(prop)
                money += p
        return sellOff

    def _sellHouses(self,money,s):
        # This is when we sell houses if we couldn't mortgage anything or have money left
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
                    if (money >= 0):#Try to break the loops if money can be resolved
                        continueLoop = False
                        break
                    v = abs(s.properties()[prop[0]])  # This gives us the value associated with the property 1 - 7
                    p = board[prop[0]]["build_cost"] // 2
                    if (1 < v < 7):
                        listHousesToSell.setdefault(prop[0], 0)  # Add to dictionary with 0 houses
                        if (listHousesToSell[prop[0]] < v - 1):  # 2 - 6
                            listHousesToSell[prop[0]] += 1
                            continueLoop = True
                            money += p

        sellHousesList = []
        for i in listHousesToSell:
            if 0 < listHousesToSell[i]:
                sellHousesList.append((i, listHousesToSell[i]))
        # print(sellHousesList)
        return sellHousesList

    def _unmortgageProps(self,s,money):
        #PLAYER TRIES TO UNMORTGAGE ALL PROPERTIES
        buyOff = []
        money_spent = 0
        for prop in s.agentProperties():
            v = abs(s.properties()[prop])
            if (v == 7):
                p = (board[prop]["price"] // 2) * 1.1 #10% interest on mortgage price
                if money_spent+p > money * self._buyPct:#If money_spent + p is more than 40% (self._buyPct) of original money - Stop purchasing
                    break
                buyOff.append(prop)
                money_spent+=p
        return buyOff

    def _buyHouses(self,s,money):
        #PLAYER TRIES TO BUY HOUSES
        buyHousesList = []
        monopolies = s.getAgentMonopolies()
        if len(monopolies) != 0:
            continueLoop = True
            monopolies = s.getAgentMonopolies()
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
                        if (money_spent+p >= money*self._buyPct):#Try to break loop if money spent + next house cost is more than 40% (self._buyPct) of available cash
                            continueLoop = False
                            break
                        if (0 < v < 6):#property is already bought and is not a hotel or mortgaged
                            listHousesToBuy.setdefault(prop[0], 0)  # Add to dictionary with 0 houses
                            listHousesToBuy[prop[0]] += 1
                            continueLoop = True
                            money_spent += p
            for i in listHousesToBuy:
                if 0 < listHousesToBuy[i]:
                    buyHousesList.append((i, listHousesToBuy[i]))
            # print(buyHousesList)
        return buyHousesList

    def getBMSTDecision(self, state):
        s = State(self.id, state)
        money = s.agentLiquidCash() - s.agentDebt()

        if (money < 0):#Trying to get money by mortgaging properties
            sellOff = self._mortgageProps(money,s)
            if sellOff:
                return ("M", sellOff)

            sellHousesList = self._sellHouses(money,s)
            if sellHousesList:
                return ("S",sellHousesList)


        #AFTER THE PLAYER HAS BECOME DEBT FREE
        if money >= 0:
            sellOff = self._unmortgageProps(s,money)
            if sellOff:
                return ("M", sellOff)
            buyHousesList = self._buyHouses(s,money)
            if buyHousesList:
                return ("B", buyHousesList)

        return False

    def respondTrade(self, state):
        return False

    def buyProperty(self, state):
        s = State(self.id, state)
        if s.getPhaseInfo() <= s.agentLiquidCash() * self._buy_prop:
            return True
        return False

    def auctionProperty(self, state):
        s = State(self.id, state)
        #Auction from 50% of the price to 100% of the price
        return random.randrange(s.getPhaseInfo()*0.5, s.getPhaseInfo())

    def jailDecision(self, state):
        s = State(self.id, state)
        if s.agentJailCards() != 0:
            return ("C", s.agentJailCards())
        elif len(s.opponentProperties()) / 28 > self._jailStay:  # If 25% owned by opponent
            return ("R")  # Simply roll or wait
        elif s.agentLiquidCash() >= s.agentLiquidCash() * self._jailStay:
            return ("C")
        else:
            return ("R")

    def receiveState(self, state):
        # print(state)
        return None




import pdb
from agent.stateEngine import *
import random
from  agent.lookup import *


class Agent(object):
    def __init__(self, id, _bmst_modifier=0.2,_buyPct=0.4,_jailStay=0.25,_buy_prop=0.5,_auction_prop=0.5):
        self.id = id
        self._buyPct = _buyPct
        self._jailStay = _jailStay
        self._buy_prop = _buy_prop
        self._auction_prop = _auction_prop
        self._bmst_modifier = _bmst_modifier
        self._dickness = 0.5 #Higher value = more dick


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


    def getBMSTDecision(self, state):
        # print("getBMSTDecision")
        s = State(self.id, state)
        money = s.agentLiquidCash() - s.agentDebt()

        if (money < 0):#Trying to get money by mortgaging properties
            sellOff = self._mortgageProps(money,s)
            if sellOff:
                return ("M", sellOff)

            # sellHousesList = s.seeSellHouse()
            # if sellHousesList:
            #     listToReturn = {}
            #     while sellHousesList:#Keep selling houses until there is no debt
            #         breakLoop = True
            #         for eachProp in sellHousesList:
            #             p = board[eachProp]["build_cost"] // 2
            #             if money < 0:#Keep doing until money is
            #                 money+=p
            #                 s.setSellHouse(eachProp)
            #                 breakLoop = False
            #                 listToReturn.setdefault(eachProp,0)
            #                 listToReturn[eachProp]+=1
            #         if breakLoop:
            #             break
            #         sellHousesList = s.seeSellHouse()
            #
            #     listToReturn = [(i,listToReturn[i]) for i in listToReturn.keys()]
            #     return ("S", listToReturn)


        #AFTER THE PLAYER HAS BECOME DEBT FREE
        if money >= 0:
            buyOff = self._unmortgageProps(s,money)
            if buyOff:
                return ("M", buyOff)
            # buyHousesList = s.seeBuyHouse()
            # if buyHousesList:
            #     money_spent = 0
            #     listToReturn = {}
            #     for eachProp in buyHousesList:#Simply add 1 house to all possible houses
            #         p = board[eachProp]["build_cost"]
            #         if p + money_spent <= money * self._buyPct:
            #             money_spent+=p
            #             s.setBuyHouse(eachProp)
            #             listToReturn.setdefault(eachProp,0)
            #             listToReturn[eachProp]+=1
            #
            #     listToReturn = [(i,listToReturn[i]) for i in listToReturn.keys()]
            #     return ("B", listToReturn)
        return True

    def respondTrade(self, state):
        # print("respondTrade")
        return False

    def buyProperty(self, state):
        # print("buyProperty")
        s = State(self.id, state)
        if s.getPhaseInfo() <= s.agentLiquidCash() * self._buy_prop:
            return True
        return False

    def auctionProperty(self, state):
        # print("auctionProperty")
        s = State(self.id, state)
        #Auction from 50% of the price to 100% of the price
        money = s.agentLiquidCash() - s.agentDebt()
        if money > 0:
            return min([s.opponentLiquidCash(),s.agentLiquidCash(),s.getPhaseInfo()])*0.2

        #     if money * self._auction_prop < s.getPhaseInfo():#Only bid if I have self._auction_prop * property value
        #         return random.randrange(s.getPhaseInfo()*self._auction_prop, s.getPhaseInfo())
        #     else:
        #         return random.randrange(0,int(money * self._auction_prop)) #I am not interested in buying if I don't have enough money
        return 0
    def jailDecision(self, state):
        # print("jailDecision")
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




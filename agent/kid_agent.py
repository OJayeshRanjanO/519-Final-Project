import pdb
from agent.stateEngine import *
import random
import copy


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
        agent_properties = [i for i in s.agentProperties()]
        random.shuffle(agent_properties)#Pick any property for mortgage
        for prop in agent_properties:
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
        s = State(self.id, state)
        money = s.agentLiquidCash() - s.agentDebt()

        #SIMPLY RESOLVE DEBT AND DO NOTHING ELSE
        if (money < 0):#Trying to get money by mortgaging properties
            sellOff = self._mortgageProps(money,s)
            if sellOff:
                return ("M", sellOff)

        #AFTER THE PLAYER HAS BECOME DEBT FREE
        if money >= 0:
            buyOff = self._unmortgageProps(s,money)
            if buyOff:
                return ("M", buyOff)

        return False

    def respondTrade(self, state):#Kid responds accepts everything
        return True

    def buyProperty(self, state):
        s = State(self.id, state)
        if s.getPhaseInfo() <= s.agentLiquidCash():#If I have money, I will buy the property
            return True
        return False

    def auctionProperty(self, state):
        s = State(self.id, state)
        #Auction for 1 less than the same price
        money = s.agentLiquidCash() - s.agentDebt()
        if money > 0:
            return random.randrange(0, 10)
        else:
            return 1

    def jailDecision(self, state):
        s = State(self.id, state)
        if s.agentJailCards() != 0:#Use cards if I have them
            return ("C", s.agentJailCards())
        elif s.agentLiquidCash() >= 50: #If I have money I will spend it
            return ("P",)
        else:
            return ("R",)

    def receiveState(self, state):
        # print(state)
        return None




import pdb
from agent.stateEngine import *
import random
from agent.lookup import board


class Agent(object):
    def __init__(self, id, _bmst_modifier=0.2,_buyPct=0.4,_jailStay=0.25,_jailStay_threshold=20,_buy_prop=0.5,_auction_prop=0.5,_dickness=0.9,_mercy_money=200):
        self.id = id
        self._buyPct = 0.8#JUST TRY TO BUY NO MATTER WHAT _buyPct
        self._jailStay = _jailStay
        self._jailStay_threshold = _jailStay_threshold
        self._buy_prop = 0.8#JUST TRY TO BUY NO MATTER WHAT
        self._auction_prop = _auction_prop
        self._bmst_modifier = _bmst_modifier
        self._dickness = _dickness #Higher value = more dick
        self._mercy_money = 1500#_mercy_money #Some Value for player money ...
        self.currentTurn = -1

    ######## HELPER FUNCTIONS FOR BSMT ########

    def _mortgageProps(self, money, s):
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

    def _unmortgageProps(self, s, money):
        # PLAYER TRIES TO UNMORTGAGE ALL PROPERTIES
        buyOff = []
        money_spent = 0
        for prop in s.agentProperties():
            v = abs(s.properties()[prop])
            if (v == 7):
                p = (board[prop]["price"] // 2) * 1.1  # 10% interest on mortgage price
                if money_spent + p > money * self._buyPct:  # If money_spent + p is more than 40% (self._buyPct) of original money - Stop purchasing
                    break
                buyOff.append(prop)
                money_spent += p
        return buyOff

    def _proposeTrade(self, s,money):
        monopolies = s.opponentMonopolies()
        properties = s.opponentProperties()
        opponentCash = s.opponentLiquidCash() - s.opponentDebt()
        all_properties = s.properties()

        if (opponentCash < self._mercy_money):#Sees opponent in trouble
            if len(monopolies) != 0:#Opponent has monopolies
                for eachMonopoly in monopolies:
                    for eachProp in eachMonopoly:
                        v = all_properties[eachProp]
                        if abs(v) == 1:#Unimproved property
                            cost = (board[eachProp])['price'] * self._dickness
                            if money * self._buy_prop >= cost:
                                return ["T",cost,[eachProp],0,[]]
                        elif 1 < abs(v) < 7:
                            cost = ((board[eachProp])['price'] + ((board[eachProp])['build_cost'] * abs(v)-1)) *  self._dickness
                            if money * self._buy_prop >= cost:
                                return ["T",cost,[eachProp],0,[]]
                        elif abs(eachProp) == 7:
                            cost = ((board[eachProp])['price'] * 2 * 1.1) *  self._dickness
                            if money * self._buy_prop >= cost:
                                return ["T",cost,[eachProp],0,[]]

            else:#Opponent has no monopolies, ask for cheap properties
                for eachProp in properties:
                    v = all_properties[eachProp]
                    if abs(v) == 1:  # Unimproved property
                        cost = (board[eachProp])['price'] * self._dickness
                        if money * self._buy_prop >= cost:
                            return ["T",cost,[eachProp],0,[]]
                    elif 1 < abs(v) < 7:
                        cost = ((board[eachProp])['price'] + ((board[eachProp])['build_cost'] * abs(v) - 1)) * self._dickness
                        if money * self._buy_prop >= cost:
                            return ["T",cost,[eachProp],0,[]]
                    elif abs(v) == 7:
                        cost = ((board[eachProp])['price'] * 2 * 1.1) * self._dickness
                        if money * self._buy_prop >= cost:
                            return ["T",cost,[eachProp],0,[]]
        return None

    def getBMSTDecision(self, state):
        s = State(self.id, state)
        money = s.agentLiquidCash() - s.agentDebt()

        if (money < 0):  # Trying to get money by mortgaging properties
            sellOff = self._mortgageProps(money, s)
            if sellOff:
                return ("M", sellOff)
            sellHousesList = s.seeSellHouse()

            if sellHousesList:
                listToReturn = {}
                while sellHousesList:#Keep selling houses until there is no debt
                    breakLoop = True
                    for eachProp in sellHousesList:
                        p = board[eachProp]["build_cost"] // 2
                        if money < 0:#Keep doing until money is
                            money+=p
                            s.setSellHouse(eachProp)
                            breakLoop = False
                            listToReturn.setdefault(eachProp,0)
                            listToReturn[eachProp]+=1
                    if breakLoop:
                        break
                    sellHousesList = s.seeSellHouse()

                listToReturn = [(i,listToReturn[i]) for i in listToReturn.keys()]
                if listToReturn:
                    return ("S", listToReturn)

        # AFTER THE PLAYER HAS BECOME DEBT FREE PLAYER BUYS BUILDINGS
        if money >= 0:
            sellOff = self._unmortgageProps(s, money)
            if sellOff:
                return ("M", sellOff)
            buyHousesList = s.seeBuyHouse()
            if buyHousesList:
                money_spent = 0
                listToReturn = {}
                for eachProp in buyHousesList:#Simply add 1 house to all possible houses
                    p = board[eachProp]["build_cost"]
                    if p + money_spent <= money * self._buyPct:
                        money_spent+=p
                        s.setBuyHouse(eachProp)
                        listToReturn.setdefault(eachProp,0)
                        listToReturn[eachProp]+=1

                listToReturn = [(i,listToReturn[i]) for i in listToReturn.keys()]
                if listToReturn:
                    return ("B", listToReturn)
        return False

    def respondTrade(self, state):
        return False

    def buyProperty(self, state):
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
        return 0

    def jailDecision(self, state):
        s = State(self.id, state)
        if s.agentJailCards() != 0:
            return ("C", s.agentJailCards())
        elif len(s.opponentProperties()) / 28 > self._jailStay:  # If 25% owned by opponent
            return ("R",)  # Simply roll or wait
        elif self._jailStay_threshold <= s.agentLiquidCash() * self._jailStay:#Stay in jail if user has less than $200
            return ("P",)
        else:
            return ("R",)

    def receiveState(self, state):
        # print(state)
        return None




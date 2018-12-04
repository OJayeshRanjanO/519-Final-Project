import pdb
from agent.stateEngine import *
import random
from agent.lookup import board


class Agent(object):
    def __init__(self, id, _bmst_modifier=0.2,_buyPct=0.4,_jailStay=0.25,_jailStay_threshold=20,_buy_prop=0.5,_auction_prop=0.5,_dickness=0.9,_mercy_money=200):
        self.id = id
        self._buyPct = 0
        self._jailStay = 0
        self._jailStay_threshold = 0
        self._buy_prop = 0
        self._auction_prop = 0
        self._bmst_modifier = 0
        self._dickness = 0
        self._mercy_money = 0
        self.currentTurn = 0
        self._probablity = 0

    ######## HELPER FUNCTIONS FOR BSMT ########

    def getBMSTDecision(self, state):
        s = State(self.id, state)
        self.getGameData(state, s)
        print()
        while True:
            i = input("(B)uy, Un/(M)ortgage, (S)ell, (T)rade, (Q)uit ")
            if i.upper() == "B":
                b = ""
                buy_houses = {}
                money_remaining = s.agentLiquidCash() - s.agentLiquidCash()
                if money_remaining < 0:
                    print("Insuffcient cash: ",str(money_remaining))
                    return ("B",[])
                while b!="Q":
                    print()
                    possible_houses = s.seeBuyHouse()
                    print("Houses that can be bought: ", str(possible_houses))
                    print("Money Left: ", str(money_remaining))
                    b = input("(Q) to Quit return list otherwise type the property number BUY")
                    if b.upper() == "Q":
                        return ("B",[(i,buy_houses[i]) for i in buy_houses.keys()])
                    else:
                        for monopolies in possible_houses:
                            if int(b) in monopolies:
                                if board[int(b)]['build_cost'] < money_remaining:
                                    s.setBuyHouse(int(b))
                                    money_remaining -= board[int(b)]['build_cost']
                                    buy_houses.setdefault(int(b),0)
                                    buy_houses[int(b)]+=1
                            else:
                                print("Invalid property number")
                        b = ""
            elif i.upper() == "M":
                b = ""
                money = s.agentLiquidCash() - s.agentLiquidCash()
                properties_to_mortgage = []
                while b.upper()!="Q":
                    print()
                    props = s.properties()
                    mortgagble_prop = [i for i in s.agentProperties() if (abs(props[i]) == 1 or abs(props[i]) == 7) and i not in properties_to_mortgage]
                    print("Possible properties to mortgage: ", str(mortgagble_prop))
                    print("Money Left: ", str(money))
                    b = input("(Q) to Quit return list otherwise type the property number to (un)mortgage")
                    if b.upper() == "Q":
                        return ("M",properties_to_mortgage)
                    elif int(b) in mortgagble_prop:
                        if abs(props[int(b)]) == 7:#UNMORTGAGE BACK PROPERTY
                            money-=(board[int(b)]["price"] // 2) * 1.1
                            if money <= 0:
                                properties_to_mortgage.append(int(b))
                            else:
                                print("Not Enough Money")
                        else:#MORTGAGE BACK PROPERTY
                            money+=(board[int(b)]["price"] // 2)
                        b = ""
                    else:
                        print("Invalid property number")
                        b = ""
            elif i.upper() == "S":
                b = ""
                sell_houses = {}
                money_remaining = s.agentLiquidCash() - s.agentLiquidCash()
                while b.upper()!="Q":
                    print()
                    possible_houses = s.seeSellHouse()
                    print("Houses that can be sold: ", str(sell_houses))
                    print("Money Left: ", str(money_remaining))
                    b = input("(Q) to Quit return list otherwise type the property number to SELL")
                    if b.upper() == "Q":
                        return ("S",[(i,sell_houses[i]) for i in sell_houses.keys()])
                    else:
                        for monopolies in possible_houses:
                            if int(b) in monopolies:
                                s.setBuyHouse(int(b))
                                money_remaining += board[int(b)]['build_cost']//2
                                sell_houses.setdefault(int(b),0)
                                sell_houses[int(b)]+=1
                            else:
                                print("Invalid property number")
                        b = ""
            elif i.upper() == "T":
                if self.currentTurn == s.currentTurnNumber():
                    print("Can't propose 2 trades in same turn")
                    return False
                self.currentTurn = s.currentTurnNumber()
                b = ""
                current_trade_list = ["T",0,[],0,[]]
                while b.upper()!="Q":
                    print()
                    print("Trades: ",current_trade_list)
                    print("Opponent Properties: ",s.opponentProperties())
                    print("Agent Properties: ",s.agentProperties())
                    print("Opponent Monopolies: ",s.opponentMonopolies())
                    print("Agent Monopolies: ",s.agentMonopolies())
                    money = s.agentLiquidCash() - s.debt()
                    b = input("(Q) to Quit and return list for trade, (R) to Request, (O) to Offer")
                    if b.upper() == "Q":
                        return current_trade_list
                    elif b.upper() == "O":
                        c = ""
                        while c.upper()!="S":#I AM OFFERING STUFF TO BUY FROM OTHER PLAYER
                            print("Cash Offer: ", str(current_trade_list[1])," Properties for offer: ",str(current_trade_list[1]))
                            c = input("(S) to quit offer menu otherwise enter the property number, type the number again to remove it")
                            if c.upper() != "S":
                                if int(c) not in s.opponentProperties():
                                    print("Invalid property")
                                    continue
                                m = input("Cash Offer: ")
                                if m > money:
                                    current_trade_list[1] = m
                                    if int(c) in current_trade_list[2]:
                                        current_trade_list[2].append(int(c))
                                    else:
                                        current_trade_list[2].remove(int(c))
                                else:
                                    print("Insufficient Cash")
                            else:
                                b = ""
                                break
                        b=""
                    elif b.upper() == "R":#REQUESTING PROPERTY TO BE SOLD TO OTHER PLAYER
                        c = ""
                        while c.upper()!="S":#I AM OFFERING STUFF TO BUY FROM OTHER PLAYER
                            print("Cash Request: ", str(current_trade_list[3])," Properties to request: ",str(current_trade_list[4]))
                            c = input("(S) to quit request menu otherwise enter the property number, type the number again to remove it")
                            if c.upper() != "S":
                                if int(c) not in s.agentProperties():
                                    print("Invalid property")
                                    continue
                                m = input("Cash Offer: ")
                                if m > money:
                                    current_trade_list[3] = m
                                    if int(c) in current_trade_list[4]:
                                        current_trade_list[4].append(int(c))
                                    else:
                                        current_trade_list[4].remove(int(c))
                                else:
                                    print("Insufficient Cash")
                            else:
                                b = ""
                                break
                        b=""
                    else:
                        print("Invalid option")
                        b=""
                return False
            else:
                return False

    def respondTrade(self, state):
        s = State(self.id, state)
        print("Turn State: ",str(state[:-1]))
        print("Turn Number", str(s.currentTurnNumber()))
        print("Agent Cash",str(s.agentLiquidCash()), "||Opponent Cash",str(s.opponentLiquidCash()))
        print("Agent Debt",str(s.agentDebt()), "||Opponent Debt",str(s.opponentDebt()))
        print("Agent Liquid Asset",str(s.agentLiquidAsset()), "||Opponent Liquid Asset",str(s.opponentLiquidAsset()))
        print("Agent Net Asset",str(s.agentNetWealth()), "||Opponent Net Asset",str(s.opponentNetWealth()))
        print("Agent Properties:"+str(s.agentProperties())+"\n||Opponent Properties:"+str(s.opponentProperties()))
        print("Agent Percentage Ownership:",str(s.agentPctOwnership()),"Opponent Percentage Ownership:",str(s.opponentPctOwnership()))
        print("Agent Monopolies:",str(s.agentMonopolies()),"Opponent Monopolies:",str(s.opponentMonopolies()))
        print()
        print(s.getPhaseInfo())
        while True:
            n = input("Accept Trade? (Y) or Deny (N)")
            if n.upper() == "Y":
                s.state[5][0] = True
                return s.state[5]
            elif n.upper() == "N":
                s.state[5][0] = False
                return s.state[5]
    def buyProperty(self, state):
        s = State(self.id, state)
        self.getGameData(state, s)
        print()
        print("Property Index: ", s.state[5][0])
        print("Property Price: ",s.getPhaseInfo())
        while True:
            n = input("Buy Trade? (Y) or Deny (N)")
            if n.upper() == "Y":
                return True
            elif n.upper() == "N":
                return False

    def auctionProperty(self, state):
        s = State(self.id, state)
        self.getGameData(state, s)
        print()
        print("Property Index: ", s.state[5][0])
        print("Property Price: ",s.getPhaseInfo())
        while True:
            n = int(input("Bid Value: "))
            return n
    def jailDecision(self, state):
        s = State(self.id, state)
        print(s.agentJailCards())
        while True:
            n = input("(C) to use Jail Card, (P) to pay $50, (R) to Roll")
            if n == "C":
                if s.agentJailCards() == 0:
                    print("No Jail Cards available")
                else:
                    print(n,s.agentJailCards())
            elif n == "P":
                if s.agentLiquidCash() - s.agentDebt() > 50:
                    return (n)
                else:
                    print("Insufficient Cash")
            elif n == "R":
                return (n)
    def receiveState(self, state):
        # print(state)
        s = State(self.id, state)
        self.getGameData(state, s)
        return None


    def getGameData(self,state,s):
        print("Turn State: ",str(state[:-1]))
        print("Turn Number", str(s.currentTurnNumber()))
        print("Agent Cash",str(s.agentLiquidCash()), "||Opponent Cash",str(s.opponentLiquidCash()))
        print("Agent Debt",str(s.agentDebt()), "||Opponent Debt",str(s.opponentDebt()))
        print("Agent Liquid Asset",str(s.agentLiquidAsset()), "||Opponent Liquid Asset",str(s.opponentLiquidAsset()))
        print("Agent Net Asset",str(s.agentNetWealth()), "||Opponent Net Asset",str(s.opponentNetWealth()))
        print("Agent Properties:"+str(s.agentProperties())+"\n||Opponent Properties:"+str(s.opponentProperties()))
        print("Agent Percentage Ownership:",str(s.agentPctOwnership()),"Opponent Percentage Ownership:",str(s.opponentPctOwnership()))
        print("Agent Monopolies:",str(s.agentMonopolies()),"Opponent Monopolies:",str(s.opponentMonopolies()))
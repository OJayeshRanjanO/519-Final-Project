from lookup import board


def same_sign(x, y):
    return (x < 0 and y < 0) or (x > 0 and y > 0)


class State(object):
    def __init__(self, iden, state):
        self.state = state[:-1]
        self.iden = iden
        self.monopolies = {
            0: [1, 3], 1: [6, 8, 9], 2: [11, 13, 14], 3: [16, 18, 19], 4: [21, 23, 24], 5: [26, 27, 29],
            6: [31, 32, 34], 7: [37, 39], 8: [5, 15, 25, 35], 9: [12, 28]
        }

    def getAgentMonopolies(self):
        monopolies = {}
        for i in self.monopolies:
            if set(self.monopolies[i]) < set(self.agentProperties()):
                monopolies[i] = {}
                for j in self.monopolies[i]:
                    (monopolies[i])[j] = (self.properties())[j]
        return monopolies

    def getOpponentMonopolies(self):
        monopolies = {}
        for i in self.monopolies:
            if set(self.monopolies[i]) < set(self.opponentProperties()):
                monopolies[i] = {}
                for j in self.monopolies[i]:
                    (monopolies[i])[j] = (self.properties())[j]
        return monopolies

    ## BASE VALUES EXTRACTED FROM STATE

    def currentTurnNumber(self):
        return self.state[0]

    def agentIndex(self):
        return self.iden - 1

    def opponentIndex(self):
        return (self.agentIndex() + 1) % 2

    def agentSign(self):
        return (-1) ** (self.agentIndex())

    def opponentSign(self):
        return (-1) ** (self.opponentIndex())

    def positions(self):
        return self.state[2]

    def agentPosition(self):
        return self.positions()[self.agentIndex()]

    def opponentPosition(self):
        return self.positions()[self.opponentIndex()]

    def liquidCash(self):
        return self.state[3]

    def agentLiquidCash(self):
        return self.liquidCash()[self.agentIndex()]

    def opponentLiquidCash(self):
        return self.liquidCash()[self.opponentIndex()]

    def debt(self):
        return self.state[6]

    def agentDebt(self):
        return self.debt()[(2 * self.agentIndex()) + 1]

    def opponentDebt(self):
        return self.debt()[(self.opponentIndex()) + 1]

    def properties(self):
        return self.state[1][:-2]

    def jailCards(self):
        return self.state[1][-2:]

    def calculateJailCards(self, sign):
        valid = lambda c: same_sign(c, sign)
        return [abs(i) for i, c in enumerate(self.jailCards()) if valid(c)]

    def agentJailCards(self):
        cards = self.calculateJailCards(self.agentSign())
        return 40 + cards[0] if cards else 0

    def opponentJailCards(self):
        cards = self.calculateJailCards(self.opponentSign())
        return 40 + cards[0] if cards else 0

    ## DERIVED FEATURES ABOUT PLAYERS

    def agentLiquidAsset(self):
        return self.calculateLiquidAsset(self.agentSign())

    def opponentLiquidAsset(self):
        return self.calculateLiquidAsset(self.opponentSign())

    def calculateLiquidAsset(self, sign):
        same = lambda p: same_sign(sign, p)
        props = [(i, abs(p)) for i, p in enumerate(self.properties()) if same(p)]
        val = sum([board[i]["price"] / 2 for i, p in props if p < 7])
        val += sum([(board[i]["build_cost"] / 2) * (p - 1) for i, p in props if p < 7])
        return val

    def calculateNetWealth(self, sign):
        same = lambda p: same_sign(sign, p)
        props = [(i, abs(p)) for i, p in enumerate(self.properties()) if same(p)]
        val = sum([board[i]["price"] for i, p in props if p < 7])
        val += sum([board[i]["price"] / 2 for i, p in props if p == 7])
        val += sum([board[i]["build_cost"] * (p - 1) for i, p in props if p < 7])
        return val

    def agentNetWealth(self):
        value = self.calculateNetWealth(self.agentSign())
        return value + self.agentLiquidCash()

    def opponentNetWealth(self):
        value = self.calculateNetWealth(self.opponentSign())
        return value + self.opponentLiquidCash()

    def agentProperties(self):
        valid = lambda p: same_sign(self.agentSign(), p)
        return [i for i, p in enumerate(self.properties()) if valid(p)]

    def opponentProperties(self):
        valid = lambda p: same_sign(self.opponentSign(), p)
        return [i for i, p in enumerate(self.properties()) if valid(p)]

    def agentPctOwnership(self):
        return len(self.agentProperties()) / max((1.0*(len(self.agentProperties()) + len(self.opponentProperties()))), 1)

    def opponentPctOwnership(self):
        return len(self.opponentProperties()) / max((1.0*(len(self.agentProperties()) + len(self.opponentProperties()))), 1)

    def calculateMonopolies(self, properties):
        monopolies = {}
        for p in properties:
            group = board[p]["monopoly"]
            if (not group in monopolies):
                monopolies[group] = [0, board[p]["monopoly_size"]]
            monopolies[group][0] += 1
        return sum([1 for k in monopolies if monopolies[k][0] == monopolies[k][1]])

    def agentMonopolies(self):
        return self.calculateMonopolies(self.agentProperties())

    def opponentMonopolies(self):
        return self.calculateMonopolies(self.opponentProperties())

    ## DERIVED FEATURES ABOUT THE GAME
    def housesUsed(self):
        valid = lambda h: abs(h) > 1 and abs(h) < 6
        return sum([abs(h) - 1 for h in self.properties() if valid(h)])

    def housesLeft(self):
        return 32 - self.housesUsed()

    def hotelsUsed(self):
        valid = lambda h: abs(h) == 6
        return sum([1 for h in self.properties() if valid(h)])

    def hotelsLeft(self):
        return 12 - self.hotelsUsed()

    def propertiesOwned(self):
        valid = lambda p: abs(p) != 0
        return sum([1 for p in self.properties() if valid(p)])

    def propertiesMortgaged(self):
        valid = lambda p: abs(p) == 7
        return sum([1 for p in self.properties() if valid(p)])

    def totalLiquidCash(self):
        return self.agentLiquidCash() + self.opponentLiquidCash()

    def totalLiquidAssets(self):
        return self.agentLiquidAsset() + self.opponentLiquidAsset()

    def totalWealth(self):
        return self.agentNetWealth() + self.opponentNetWealth()

    ## INFO ABOUT PHASE INFORMATIO

    def getPhaseInfo(self):
        if self.state[4] == 3:  # Buying Property
            return board[self.state[5][0]]['price']
        if self.state[4] == 4:  # Auction
            return board[self.state[5][0]]['price']
        if self.state[4] == 6:  # Jail
            return self.state[5]
    
    ## FUNCTION TO CALL ALL INFORMATION IN ONE SHOT AS AN ARRAY
    def extract_features(self):
        tw = (1.0*self.totalWealth())
        output =  [self.agentNetWealth()/tw, self.opponentNetWealth()/tw]
        output += [self.agentLiquidAsset(), self.opponentLiquidAsset()]
        output += [len(self.agentProperties()), len(self.opponentProperties())]
        output += [self.agentMonopolies(), self.opponentMonopolies()]
        output += [self.totalWealth(), self.propertiesOwned()]
        output += [self.agentPctOwnership(), self.opponentPctOwnership()]
        return output
    
    def extract_headers(self):
        header =  ['agent_netwealth_1', 'agent_netwealth_2']
        header += ['agent_liqassets_1', 'agent_liqassets_2']
        header += ['agent_propcount_1', 'agent_propcount_2']
        header += ['agent_monopoly_1',  'agent_monopoly_2']
        header += ['total_wealth', 'total_propoerty_count']
        header += ['agent_propratio_1', 'agent_prop_ratio_2']
        return header

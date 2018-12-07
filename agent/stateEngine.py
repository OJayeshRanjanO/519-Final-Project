from agent.lookup import board
import copy


def same_sign(x, y):
    return (x < 0 and y < 0) or (x > 0 and y > 0)


class State(object):
    def __init__(self, iden, state):
        self.state = [list(k) if type(k)==tuple else k for k in state[:-1]]
        self.iden = iden
        self.monopolies = {
            0: [1, 3], 1: [6, 8, 9], 2: [11, 13, 14], 3: [16, 18, 19], 4: [21, 23, 24], 5: [26, 27, 29],
            6: [31, 32, 34], 7: [37, 39], 8: [5, 15, 25, 35], 9: [12, 28]
        }
        self.mod_state = [list(k) if type(k)==tuple else k for k in state[:-1]]


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

    def playerSign(self, id):
        return (-1) ** (id)

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

    def properties(self, use_mod=False):
        if(use_mod):
            return self.mod_state[1]
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
        return self.agentLiquidCash() + self.calculateLiquidAsset(self.agentSign())

    def opponentLiquidAsset(self):
        return self.opponentLiquidCash() + self.calculateLiquidAsset(self.opponentSign())

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

    def agentMortgagedProperties(self):
        valid = lambda p: abs(self.properties()[p]) == 7
        return [i for i in self.agentProperties() if valid(i)]

    def agentUnbuiltProperties(self):
        valid = lambda p: abs(self.properties()[p]) == 1
        return [i for i in self.agentProperties() if valid(i)]

    def agentBuiltProperties(self):
        valid = lambda p: 1 < abs(self.properties()[p]) < 7
        return [i for i in self.agentProperties() if valid(i)]

    def agentBuildingCount(self):
        valid = lambda p: same_sign(self.agentSign(), p) and abs(p) < 7
        return sum([abs(p) - 1 for p in self.properties() if valid(p)])
    
    def opponentBuildingCount(self):
        valid = lambda p: same_sign(self.opponentSign(), p) and abs(p) < 7
        return sum([abs(p) - 1 for p in self.properties() if valid(p)])

    def opponentProperties(self):
        valid = lambda p: same_sign(self.opponentSign(), p)
        return [i for i, p in enumerate(self.properties()) if valid(p)]

    def opponentMortgagedProperties(self):
        valid = lambda p: abs(self.properties()[p]) == 7
        return [i for i in self.opponentProperties() if valid(i)]

    def opponentUnbuiltProperties(self):
        valid = lambda p: abs(self.properties()[p]) == 1
        return [i for i in self.opponentProperties() if valid(i)]

    def opponentBuiltProperties(self):
        valid = lambda p: 1 < abs(self.properties()[p]) < 7
        return [i for i in self.opponentProperties() if valid(i)]

    def agentPctOwnership(self):
        return len(self.agentProperties()) / max((1.0*(len(self.agentProperties()) + len(self.opponentProperties()))), 1)

    def opponentPctOwnership(self):
        return len(self.opponentProperties()) / max((1.0*(len(self.agentProperties()) + len(self.opponentProperties()))), 1)        
    
    def agentPctBuildingOwnership(self):
        return self.agentBuildingCount() / max(1, (1.0*(self.agentBuildingCount() + self.opponentBuildingCount())))
    
    def opponentPctBuildingOwnership(self):
        return self.opponentBuildingCount() / max(1, (1.0*(self.agentBuildingCount() + self.opponentBuildingCount())))


    
    def calculateMonopolies(self, properties, offset=0):
        monopolies = {}
        for p in properties:
            group = board[p]["monopoly"]
            if (not group in monopolies):
                monopolies[group] = [[], board[p]["monopoly_size"]]
            monopolies[group][0].append(p)
        return [monopolies[k][0] for k in monopolies if (len(monopolies[k][0]) + offset) >= monopolies[k][1]]

    def agentMonopolies(self, offset=0):
        return self.calculateMonopolies(self.agentProperties(), offset=offset)

    def opponentMonopolies(self, offset=0):
        return self.calculateMonopolies(self.opponentProperties(), offset=offset)

    def agentMonopolyCount(self):
        return len(self.calculateMonopolies(self.agentProperties()))

    def opponentMonopolyCount(self):
        return len(self.calculateMonopolies(self.opponentProperties()))

    def agentToCompleteMonopoly(self, need=0):
        oMonopolies = self.opponentMonopolies(offset=10)
        aMonopolies = self.agentMonopolies(offset=10)
        c_monopolies = []
        for o_m in oMonopolies:
            for a_m in aMonopolies:
                if(board[o_m[0]]['monopoly'] == board[a_m[0]]['monopoly']):
                    c_monopolies.append((a_m, o_m))

        needed = []
        for a, o in c_monopolies:    
            m_size = board[a[0]]['monopoly_size']
            if((len(a)+len(o)) == m_size and len(o)==need):         
                needed.append(o)

        return needed

    def opponentToCompleteMonopoly(self, need=0):
        oMonopolies = self.opponentMonopolies(offset=10)
        aMonopolies = self.agentMonopolies(offset=10)
        c_monopolies = []
        for o_m in oMonopolies:
            for a_m in aMonopolies:
                if(board[o_m[0]]['monopoly'] == board[a_m[0]]['monopoly']):
                    c_monopolies.append((a_m, o_m))

        needed = []
        for a, o in c_monopolies:    
            m_size = board[a[0]]['monopoly_size']
            if((len(a)+len(o)) == m_size and len(a)==need):         
                needed.append(a)

        return needed
                

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

    def getBuyPropertyIndex(self):
        if(self.state[4] == 3):
            return self.state[5][0]
        return -1

    def getPhaseInfo(self):
        if self.state[4] == 1:#TRADE
            return self.state[5][1:]
        if self.state[4] == 3:  # Buying Property
            return board[self.state[5][0]]['price']
        if self.state[4] == 4:  # Auction
            return board[self.state[5][0]]['price']
        if self.state[4] == 6:  # Jail
            return self.state[5]

    ## FUNCTION TO CALL ALL INFORMATION IN ONE SHOT AS AN ARRAY
    def extract_features(self):
        totalWealth = 1.0 * self.totalWealth()
        totalLiqAss = 1.0 * self.totalLiquidAssets()        
        
        output =  [self.agentNetWealth()/totalWealth, self.opponentNetWealth()/totalWealth]
        output += [self.agentLiquidAsset()/totalLiqAss, self.opponentLiquidAsset()/totalLiqAss]
        output += [len(self.agentProperties()), len(self.opponentProperties())]
        output += [self.agentMonopolyCount(), self.opponentMonopolyCount()]
        output += [self.totalWealth(), self.propertiesOwned()]
        output += [self.agentPctOwnership(), self.opponentPctOwnership()]
        output += [self.agentPctBuildingOwnership(), self.opponentPctBuildingOwnership()]
        return output
    
    def extract_headers(self):
        header =  ['agent_netwealth_1', 'agent_netwealth_2']
        header += ['agent_liqassets_1', 'agent_liqassets_2']
        header += ['agent_propcount_1', 'agent_propcount_2']
        header += ['agent_monopoly_1',  'agent_monopoly_2']
        header += ['total_wealth', 'total_propoerty_count']
        header += ['agent_propratio_1', 'agent_propratio_2']
        header += ['agent_bldgratio_1', 'agent_bldgratio_2']
        return header

    ## FUNCTION POTENTIALLY BUYING PROPERTY
    def agentModifyCash(self, val):
        self.state[3][self.agentIndex()] += val

    def opponentModifyCash(self, val):
        self.state[3][self.opponentIndex()] += val

    def agentBuyProperty(self, ind, cost):
        self.state[1][ind] = self.agentSign()
        self.agentModifyCash(-cost)

    def opponentBuyProperty(self, ind, cost):
        self.state[1][ind] = self.opponentSign()
        self.opponentModifyCash(-cost)


    ## FUNCTION ALL POSSIBLE BUY/SELL HOUSES POSSIBLE IN DEPTH 1
    def seeBuyHouse(self):
        purchases = []
        for m in self.agentMonopolies():
            vals = [abs(self.properties(use_mod=True)[p]) for p in m]
            minp = min([1 if v==7 else v for v in vals])
            buys = [p for p,v in zip(m, vals) if v==minp and v!=7]
            if(board[m[0]]['class'] == 'Street'):
                purchases += buys
        return purchases

    def setBuyHouse(self, indices):
        if(type(indices) != list):
            indices = [indices]
        for ind in indices:
            v = (abs(self.properties(use_mod=True)[ind])+1) * self.agentSign()
            self.properties(use_mod=True)[ind] = v

    def seeSellHouse(self):
        sellouts = []
        for m in self.agentMonopolies():
            vals = [abs(self.properties(use_mod=True)[p]) for p in m]
            maxp = max([1 if v==7 else v for v in vals])
            sells = [p for p,v in zip(m, vals) if v==maxp and v != 1 and v!=7]
            sellouts += sells
        return sellouts

    def setSellHouse(self, indices):
        if(type(indices) != list):
            indices = [indices]
        for ind in indices:
            v = (abs(self.properties(use_mod=True)[ind])-1) * self.agentSign()
            self.properties(use_mod=True)[ind] = v

    def clone(self):
        s_mod = copy.deepcopy(self.state)
        s_mod.append([])
        return State(self.iden, s_mod)

    def updateProperty(self, p_id, prop, val, cost):
        val = abs(val) * self.playerSign(p_id)
        self.state[1][prop] = val
        self.state[3][p_id] += -cost
        
		# modList = [(p_id, [(b_id, s_id, [(prop, val, bought)], c, b_c, s_c),...]),...]
    def updateProperties(self, mods):
        for b_id, s_id, props, c, b_c, s_c in mods:
            for prop, val, bought in props:
                p_id = b_id if bought else s_id
                self.updateProperty(p_id, prop, val, 0)
            self.state[3][b_id] += -b_c
            self.state[3][s_id] += -s_c        

    def getRent(self, p_id, prop):
        val = self.properties()[prop]
        v = val
        p_sign = self.playerSign(p_id)
        if(not v or same_sign(self.playerSign(p_id), v)):
            return 0
        v = abs(val)   
        if(v == 7):
            return 0

        rent = 0
        if (v == 1):
            mon_props = []
            if(p_id != self.agentIndex()):
                mon_props = self.agentMonopolies()
            else:
                mon_props = self.opponentMonopolies()
            
            mon_props = [it for sl in mon_props for it in sl]

            e_type = board[prop]['class']
            if(e_type == 'Railroad'):
                cnt = sum([1 for p in [5, 15, 25, 35] if same_sign(val, self.properties()[p])])
                rent = 25 * (2**(cnt-1))
            elif(e_type == 'Utility'):
                rent = 20
                if(prop in mon_props):
                    rent *= 2
            else:
                rent = board[prop]['rent']
                if(prop in mon_props):
                    rent *= 2
        elif (v == 6):
            rent = board[prop]['rent_hotel']
        else:
            rent = board[prop]['rent_house_' + str(int(v)-1)]
    
        return rent                   

    def getTradeInfo(self):
        if(self.state[4] == 1):
            return self.state[5]
        else:
            return [0, [], 0, []]


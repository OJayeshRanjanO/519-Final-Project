n_players = 2 # Number of players

verbose = {'pay': False, #Player has a debt to pay handle_payments method
           'buy': False, #player is buying an unowned property
           'bstm':False,
           'auction':False,
           'cards':False, #when player falls on chance or community cards
           'state': True, #state information during each turn
           'dice': True, #dice value for each turn
           'board':False,
           'win_condition':False, #information of how winner was chosen
           'turn':True, #info about turn
           'jail':False, #info if player goes to jail
           'win':True #who finally won
           }

f = open("monopoly.log", "w")
f.write("----------------------------------------------------------\n")

def log(section,msg):
  if verbose[section]:
    f.write(str(msg)+'\n')
  

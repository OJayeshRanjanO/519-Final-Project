n_players = 2 # Number of players

verbose = {'pay': True, #Player has a debt to pay handle_payments method
           'buy': True, #player is buying an unowned property
           'bstm':True,
           'auction':True,
           'cards':True, #when player falls on chance or community cards
           'state': True, #state information during each turn
           'dice': True, #dice value for each turn
           'board':True,
           'win_condition':True, #information of how winner was chosen
           'turn':True, #info about turn
           'jail':True, #info if player goes to jail
           'win':True #who finally won
           }

f = open("monopoly.log", "w")
f.write("----------------------------------------------------------\n")

def log(section,msg):
  if verbose[section]:
    f.write(str(msg)+'\n')
  

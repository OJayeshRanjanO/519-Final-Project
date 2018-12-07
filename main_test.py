import itertools
import json
import os.path
import random

num_games = 1000
# os.remove('monopoly.log')
# if (not os.path.isfile('monopoly.log')):
#     from agent import flagship_agent, kid_agent, drunk_agent, probabilistic_agent, cheapskate_agent, asset_hoarder_agent
#     from adjudicator import Adjudicator
#
#     dic = {"Flagship":flagship_agent,
#            "Kid":kid_agent,
#             "Drunk":drunk_agent,
#            "Probabilistic":probabilistic_agent,
#            "AssetHoarder":asset_hoarder_agent,
#            "CheapSkate":cheapskate_agent
#            }
    #,"Drunk","Probabilistic","AssetHoarder","CheapSkate"
    # models = ["Flagship","Kid"]
    # models = ["Flagship","Drunk"]
    # models = ["Flagship","Probabilistic"]
    # models = ["Flagship","AssetHoarder"]
    # models = ["Flagship","CheapSkate"]
    #
    # models = ["Kid","Drunk"]
    # models = ["Kid","Probabilistic"]
    # models = ["Kid","AssetHoarder"]
    # models = ["Kid","CheapSkate"]
    #
    # models = ["Drunk","Probabilistic"]
    # models = ["Drunk","AssetHoarder"]
    # models = ["Drunk","CheapSkate"]
    #
    # models = ["Probabilistic","AssetHoarder"]
    # models = ["Probabilistic","CheapSkate"]

    # models = ["AssetHoarder","CheapSkate"]

    # for i in range(len(models)):
    #     for j in range(i+1,len(models)):
    #         # tmp = open("monopoly.log", "w")
    #         # tmp.close()
    #         adj = Adjudicator()
    #         a1, a2 = dic[models[i]].Agent, dic[models[j]].Agent
    #         for k in range(num_games):
    #             print(k)
    #             adj.runGame(a1(1), a2(2))
    #
    #         with open("monopoly.log", "r") as fp:
    #             lines = fp.readlines()
    #             game_status = []
    #             for l in range(len(lines)):
    #                 if "AgentOne won" in lines[l]:
    #                     print(l,lines[l])
    #                     game_status.append(0)
    #                 elif "AgentTwo won" in lines[l]:
    #                     print(l, lines[l])
    #                     game_status.append(1)
    #             v = sum(game_status)
    #             s = num_games - sum(game_status)
    #             print(game_status)
    #             print(models[i],s,models[j],v)
    #             print()
    #             print()
    #             text_file_to_write = "gamestatistics_data.txt"
    #             data_file = open(text_file_to_write, "a")
    #             data_file.write(str(game_status)+"\n")
    #             final = models[i] + " " +str(s) + " " + models[j] + " " + str(v)
    #             data_file.write(final+"\n")
    #         fp.close()

            # os.remove("monopoly.log")


f = open("gamestatistics_data.txt")
lst = f.readlines()
dic = {"Flagship":[0 for i in range(num_games)],
       "Kid":[0 for i in range(num_games)],
        "Drunk":[0 for i in range(num_games)],
       "Probabilistic":[0 for i in range(num_games)],
       "AssetHoarder":[0 for i in range(num_games)],
       "CheapSkate":[0 for i in range(num_games)]
       }
for i in range(0,len(lst),2):
    sp = lst[i+1].strip().split()
    p1 = sp[0]#0
    p1_score = sp[1]
    p2 = sp[2]#1
    p2_score = sp[3]
    game_results = list(lst[i].strip().replace(",","").replace("[","").replace("]","").split())

    list_p1 = dic[p1]
    list_p2 = dic[p2]
    # print(game_results)
    # print(len(game_results),len(list_p1),len(list_p2))
    for j in range(len(game_results)):
        print(j)
        if game_results[j] == '0':
            list_p1[j]+=1
        if game_results[i] == '1':
            list_p2[j]+=1

    # print(game_results)
new_dic = {}
for i in dic:
    lst = dic[i]
    new_list = [lst[0]]
    sum = 0
    for j in range(1,len(lst)):
        sum += lst[j] + lst[j - 1]
        new_list.append(sum)
    new_dic[i] = new_list

for i in new_dic.keys():
    print(i,new_dic[i][-1])







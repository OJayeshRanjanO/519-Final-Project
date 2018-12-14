#!/usr/bin/env python
# coding: utf-8

# In[17]:


import numpy as np
import pandas as pd
import stateEngine
from sklearn.linear_model import ElasticNetCV
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# In[18]:


corpus = pd.read_csv("content/output.csv")
corpus.head()


# In[19]:


corpus.shape


# In[20]:


features = []
game = 0
prev = None
count = 0
counter = 0
for r in corpus.values[:10]:
    x = r.tolist()
    v = [x[0], x[1:43], x[43:45], x[45:47], x[47:]]
    s = stateEngine.State(1, v)
    
    turnNo = s.currentTurnNumber()
    
    if(prev is None or turnNo < prev):
        game += 1
        
    features.append(np.append(np.array([game]), np.append(r, s.extract_features())))
    
    prev = turnNo
    
output = np.array(features)
headers = ['game'] + corpus.columns.values.tolist() + stateEngine.State(1, [[]]).extract_headers()
print(headers)
corpus = pd.DataFrame(output, columns=headers)
corpus = corpus[corpus.columns.drop(list(corpus.filter(regex='property')))]
corpus.shape


# In[ ]:


i = [1, 2 , 4]
pd.DataFrame(i).to_csv('hello_world.csv')


# In[ ]:


pd.set_option('display.max_columns', 1000)
corpus.head()


# In[ ]:


game_list = corpus['game'].nunique()
print(game_list)


# In[ ]:


#Group by the game
game_list = corpus.groupby('game')
games = [group for _, group in game_list if group.values.shape[0] > 50]
print(len(games))


# In[ ]:


regressor_vector_p1 = []
regressor_vector_p2 = []
test_set_x_1 = []
test_set_y_1 = []
test_set_x_2 = []
test_set_y_2 = []


# In[ ]:


counter = 0
for game in games:
    
    t1 = game['agent_netwealth_1'].values
    t2 = game['agent_netwealth_2'].values
    
    X1_train, X1_test, y1_train, y1_test = train_test_split(game.drop('agent_netwealth_1', axis=1).values, t1, test_size=0.15)
    X2_train, X2_test, y2_train, y2_test = train_test_split(game.drop('agent_netwealth_2', axis=1).values, t2, test_size=0.15)
    
    e_net1 = ElasticNetCV(cv=10, random_state=0, max_iter=1e5, n_jobs=-1)
    e_net1.fit(X1_train, y1_train)    
    
    e_net2 = ElasticNetCV(cv=10, random_state=0, max_iter=1e5, n_jobs=-1)
    e_net2.fit(X2_train, y2_train)
    
    test_set_x_2.append(X2_test)
    test_set_y_2.append(y2_test)
    test_set_x_1.append(X1_test)
    test_set_y_1.append(y1_test)
    
    regressor_vector_p1.append(e_net1.coef_)
    regressor_vector_p2.append(e_net2.coef_)


# In[ ]:


weight1 = np.mean(np.array(regressor_vector_p1), axis=0)
weight2 = np.mean(np.array(regressor_vector_p2), axis=0)
weight_1_log = pd.DataFrame(np.log(np.array(regressor_vector_p1))).sum()
weight_2_log = pd.DataFrame(np.log(np.array(regressor_vector_p2))).sum()


# In[ ]:


final_weight_1 = np.exp(weight_1_log) / (len(np.array(regressor_vector_p1)))
final_weight_2 = np.exp(weight_2_log) / (len(np.array(regressor_vector_p2)))


# In[ ]:





# In[ ]:


# np.concatenate(np.array(test_set_y_1))
y_hat_1 = np.dot(np.concatenate(np.array(test_set_x_1)), weight1.reshape(-1, 1)).flatten()
error_p1 = mean_squared_error(np.concatenate(np.array(test_set_y_1)), y_hat_1)


# In[ ]:


y_hat_2 = np.dot(np.concatenate(np.array(test_set_x_2)), weight1.reshape(-1, 1)).flatten()
error_p2 = mean_squared_error(np.concatenate(np.array(test_set_y_2)), y_hat_2)


# In[ ]:


pd.DataFrame([error_p1]).to_csv('mse_p1.csv')
pd.DataFrame([error_p2]).to_csv('mse_p2.csv')

pd.DataFrame(weight1).to_csv('weight_vector_p1_final_v2.csv')
pd.DataFrame(weight2).to_csv('weight_vector_p2_final_v2.csv')


pd.DataFrame(final_weight_1).to_csv('weight_vector_p1_final_log.csv')
pd.DataFrame(final_weight_2).to_csv('weight_vector_p2_final_log.csv')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





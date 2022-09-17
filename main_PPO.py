import sys
import time
import environment.env_nn as environment
import numpy as np
from matplotlib import pyplot as plt
import agent.agent_PPO as ag
import torch
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
num_episodes = 200
max_number_of_stepsp=100
epsilon=0.8
dicrease=0.01
a=0.2   #LearningRate
allrewards=np.zeros(1)
path="PPO_A.pt"
path1="PPO_C.pt"

agent=ag.agent_PPO(30,9)
env=environment.Env()
if os.path.exists(path):
    agent.Policy.actor = torch.load(path)
    agent.Policy.critic = torch.load(path1)

env.wait_for_status_update()

for i in range(num_episodes):
    e_return=0
    epsilon -= dicrease
    #policy evaluation

    env.getstate()
    count=0
    while 1:
        prevstate=env.state
        count+=1
        #if count==1:
        #print("状态输入",prevstate)
            #count==0
        chosenAction,logpro=agent.policyAction(prevstate)
        #print("选择动作",chosenAction)
        nextstate, reward, Terminal=env.step(chosenAction)
        #nextstate, reward, Terminal = env.step(0)
        agent.save_r_log(reward,logpro,chosenAction,prevstate)
        #env.step 执行动作 获取state 得到reward

        e_return+=reward
        if Terminal==True :
            #print("判断结束")
            break
    #if i%2==0:
        # policy improvement
    agent.Policy.train_net()

    if i % 2 == 0 and i!=0:
     #print('score:',e_return,'\n',i ,'episode\n value:')
     #agent.Policy.plot_cost()
     allrewards=np.append(allrewards,e_return)
     torch.save(agent.Policy.actor, path)
     torch.save(agent.Policy.critic, path1)

     x=np.asarray(range(len(allrewards)))
     fig=plt.plot(x,allrewards)
     plt.savefig("PPO.png")
     #plt.show()
sys.exit()

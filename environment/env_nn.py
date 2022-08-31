import logging
import random
import numpy as np


#logger = logging.getLogger(__name__)


class Env():
    def __init__(self):

        self.states = list(range(16))  # 状态空间 0-15
        self.terminate_states = np.zeros(len(self.states))  # 终止状态为np格式
        self.terminate_states[4] = 1
        self.actions = [-4, 4, -1, 1, 0]  #上下左右不动


        self.size = 4

        self.viewer = None
        self.state = 15


    def step(self,action):             #action 01234
        # 系统当前状态
        state = self.state
        as_n = self.state + self.actions[action]

        if  ((as_n not in self.states))or\
                (as_n ==6 or as_n== 8 or as_n== 9) or(action==2 and  self.state % self.size == 0) or (action == 3 and self.state % self.size == 3) or action==4:
            self.state = state
            return state, -2, False

        elif self.terminate_states[as_n]:
            self.state=as_n
            return as_n, 100, True

        else:
            self.state = as_n
            return as_n, -1,False


    def reset(self):
        #self.state = self.states[int(random.random() * len(self.states))]
        self.state=15
        return self.state

    def getstate(self):
        a=1

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
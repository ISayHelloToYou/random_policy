import numpy as np
from config import *
"""generate a random policy for benchmark"""

class RandomPolciy:
    def __init__(self):
        self.action_space = np.arange((NUM_CHANNELS + 1) * NUM_SIZE ** NUM_SIZE)
        self.channel_space = np.arange(NUM_CHANNELS + 1)
        self.size_space = np.arange(NUM_SIZE) + 1
        self.users_action = np.zeros([NUM_USERS], np.int32)
        self.users_observation = np.zeros([NUM_USERS], np.int32)

    def getAction(self):
        """return: a random action"""
        mode = []
        index_list = []
        check_index = []

        x = list(np.random.choice(self.channel_space, size=NUM_USERS))
        Y = np.random.choice(self.size_space, size=3)  # 每次来的包的个数是固定的，但是大小是可变的
        y = [[] for i in range(NUM_USERS)]
        for i in range(len(buffer)):
            if len(buffer[i]) == 0:
                y[i] = list(np.random.choice(Y, size=3))
            else:
                length = len(buffer[i])
                buffer_temp = buffer[i].pop()
                y[i] = list(np.append(buffer_temp, np.random.choice(Y, size=3-1)))

        for i in range(1, NUM_SIZE + 1):
            for j in range(1, NUM_SIZE + 1):
                for k in range(1, NUM_SIZE + 1):
                    check_index.append([i, j, k])

        for i in range(len(y)):
            index_list.append(check_index.index(y[i]))

        res = list(zip(x, index_list))
        index = np.array(res)
        # array([[0, 1],
        # [0, 2],
        # [2, 0]])
        for i in range(len(index)):
            mode.append(TABLE[index[i][0]][index[i][1]])
        action = np.array(mode)
        return action




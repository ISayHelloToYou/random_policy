from config import *
'''
N_CHANNEL channels with identical 2-state Markov Transition Matrix
observation by default is -1. And good: 1; bad: 0.
'''

class Environment:
    def __init__(self):
        self.action_space = np.arange((NUM_CHANNELS + 1) * NUM_SIZE ** NUM_SIZE)
        self.channel_space = np.arange(NUM_CHANNELS + 1)
        self.size_space = np.arange(NUM_SIZE) + 1
        self.users_action = np.zeros([NUM_USERS], np.int32)
        self.users_observation = np.zeros([NUM_USERS], np.int32)

    def step(self, action):  # 形参action是通过sample（）得到的，是模式的集合
        channel_alloc_frequency = np.zeros([NUM_CHANNELS + 1], np.int32)  # 0 for no chnnel access
        obs = []
        reward = np.zeros([NUM_USERS])
        j = 0

        check_index = []
        for m in range(1, NUM_SIZE + 1):
            for n in range(1, NUM_SIZE + 1):
                for k in range(1, NUM_SIZE + 1):
                    check_index.append([m, n, k])

        for each in action:
            x, y = np.where(TABLE == each)
            index = np.array(list(zip(x, y)))
            self.users_action[j] = each  # action
            channel_alloc_frequency[index[0][0]] += 1
            j += 1

        for i in range(1, len(channel_alloc_frequency)):
            if channel_alloc_frequency[i] > 1:
                channel_alloc_frequency[i] = 0

        for i in range(len(action)):
            x, y = np.where(TABLE == self.users_action[i])
            index = np.array(list(zip(x, y)))  # array([[×, ×]]

            self.users_observation[i] = channel_alloc_frequency[index[0][0]]
            if self.users_action[i] >= 0 and self.users_action[i] < NUM_SIZE ** NUM_SIZE:  # accessing no channel,table的第一行
                self.users_observation[i] = 0

            if self.users_observation[i] == 1:
                if sum(check_index[index[0][1]]) <= CHANNEL_CAPACITY:
                    reward[i] = 1
                    done_traffics[i].append(check_index[index[0][1]])
                    buffer[i].clear()
                else:
                    from_buffer = check_index[index[0][1]].pop(0)
                    a = np.random.choice(check_index[index[0][1]], size=1, replace=False)
                    reward[i] = 1 + np.power(np.e, (-1 * a))
                    done_traffics[i].append(list(np.append(from_buffer, a)))

                    check_index[index[0][1]].remove(a)
                    buffer[i].append(check_index[index[0][1]])
            elif self.users_observation[i] == 0:
                reward[i] = 0
                buffer[i].clear()
            obs.append((self.users_observation[i], reward[i]))

        obs.append(channel_alloc_frequency)
        return obs, reward





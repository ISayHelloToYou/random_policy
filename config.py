"""
Denote s = N_NODES, c = N_CHANNELS, w = AGENT_STATE_WINDOWS_SIZE.
complexity:
  #(observation): pow(2, s)
  #(state): pow(2, ws)
  #(action): pow(c + 1, s)
"""
import math
import numpy as np
import sys

NUM_CHANNELS = 2  # Total number of channels
NUM_USERS = 3
NUM_SIZE = 3
TABLE = np.arange((NUM_CHANNELS+1) * NUM_SIZE**NUM_SIZE ).reshape(((NUM_CHANNELS+1) , NUM_SIZE**NUM_SIZE))
CHANNEL_CAPACITY = 7
N_NODES = 1
N_SENSING = 1

buffer = [[] for i in range(NUM_USERS)]
done_traffics = [[] for i in range(NUM_USERS)]
buffer_temp = 0

# current_state = [[] for i in range(NUM_USERS)]
# next_state = [[] for i in range(NUM_USERS)]

temp_prob = [(np.random.random(), np.random.random()) for i in range(NUM_USERS)]
P_DISTINCT_MATRIX = [[(x, 1 - x), (y, 1 - y)] for x, y in temp_prob]

B = [1 for i in range(NUM_CHANNELS)]

# for writing to the file
PERIOD = 100  # for writing to the file
T_THRESHOLD = 600000  # 5000000# num of plays; 80000000
T_EVAL = 50000

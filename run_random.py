import time
from random_policy import RandomPolciy
from config import *
from env_random import Environment


def one_hot(num, len):
    assert num >= 0 and num < len, "error"
    vec = np.zeros([len], np.int32)
    vec[num] = 1
    return vec


def state_generator(action, obs):
    state_vector = []
    if action is None:
        print('None')
        sys.exit()
    for user_i in range(action.size):
        x, y = np.where(TABLE == action[user_i])
        index = np.array(list(zip(x, y)))

        input_vector_i = one_hot(index[0][0], NUM_CHANNELS + 1)
        size_choose = one_hot(index[0][1], NUM_SIZE ** NUM_SIZE)
        channel_alloc = obs[-1]
        input_vector_i = np.append(input_vector_i, np.append(size_choose, channel_alloc))
        input_vector_i = np.append(input_vector_i, obs[user_i][0])  # ACK
        state_vector.append(input_vector_i)
    return state_vector


# def _state_transit(state):
#     current_state = state
#     next_state = current_state
#     for i in range(NUM_USERS):
#
#         temp = np.random.random()
#         if current_state[i][-1] == 0:
#             if temp < P_DISTINCT_MATRIX[i][0][0]:
#                 next_state[i] = state[i]
#             else:
#                 action = RandomPolciy.getAction()
#                 obs = Environment.step(action)
#                 state_new = state_generator(action, obs)
#                 next_state[i] = state_new[i]
#         else:
#             if temp < P_DISTINCT_MATRIX[i][1][0]:
#                 next_state[i] = state[i]
#             else:
#                 action = RandomPolciy.getAction()
#                 obs = Environment.step(action)
#                 state_new = state_generator(action, obs)
#                 next_state[i] = state_new[i]
#     current_state = next_state


# step 1: init
env = Environment()
policy = RandomPolciy()

total_rewards = []
channel_utilization = [[] for i in range(NUM_USERS)]
avg_reward = []
avg_channel_utilization = []
avg_collision = []
avg_collision_last100 = []
# cumulative reward
cum_r = [0]
# cumulative collision
cum_collision = []

start_time = time.time()

for i in range(T_THRESHOLD):
    action = policy.getAction()
    obs, reward = env.step(action)
    state = state_generator(action, obs)

    current_state = state
    next_state = current_state
    for i in range(NUM_USERS):
        temp = np.random.random()
        if current_state[i][-1] == 0:
            if temp < P_DISTINCT_MATRIX[i][0][0]:
                next_state[i] = state[i]
            else:
                action = policy.getAction()
                obs = env.step(action)
                state_new = state_generator(action, obs)
                next_state[i] = state_new[i]
        else:
            if temp < P_DISTINCT_MATRIX[i][1][0]:
                next_state[i] = state[i]
            else:
                action = policy.getAction()
                obs = env.step(action)
                state_new = state_generator(action, obs)
                next_state[i] = state_new[i]

    state = next_state

    # calculating sum of rewards
    sum_r = np.sum(reward)
    total_rewards.append(sum_r)

    r_num = 0
    for r in obs[-1:-(NUM_CHANNELS+1)]:
        if r == 1:
            r_num += 1
    collision = NUM_CHANNELS - r_num
    cum_collision.append(collision)
    print('cum_collision---' + str(cum_collision))
#     for i in range(len(action)):
#         x, y = np.where(TABLE == action[i])
#         index = np.array(list(zip(x, y)))
#         size_all = check_index[index[0][1]]
#         if obs[i][0] == 1:
#             if sum(size_all) <= CHANNEL_CAPACITY:
#                 channel_utilization[i].append(sum(size_all) / CHANNEL_CAPACITY)
#             else:
#                 channel_utilization[i].append((-np.log(reward[i] - 1)) / CHANNEL_CAPACITY)
#         else:
#             channel_utilization[i].append(0)
#
#     duration = time.time() - start_time
#
#     if count % PERIOD == 0:
#         accum_reward = total / float(count)
#         duration = time.time() - start_time
#         f.write('Index %d: accu_reward is %f, action is: %s and time duration is %f' % (
#             count, accum_reward, str(action_env), duration))
#         f.write('\n')
#
# f.close()
#
# duration = time.time() - start_time
# count = i + 1
# accum_reward = total / float(count)
# duration = time.time() - start_time
# f_result.write('Random final accu_reward is %f and time duration is %f\n' % (accum_reward, duration))


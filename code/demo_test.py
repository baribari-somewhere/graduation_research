import sys

from stable_baselines3 import DQN


from env_catan import Env_Catan
from env_constant_catan import Env_Constant_Catan
from env_comb_catan import Env_Comb_Catan
from env_player4 import Env_Constant_Catan_player4
from env_enemy import Env_Enemy
from ecc import *
# from env_constant_test_doing import Env_Constant_Test_Doing
# from env_constant_test_doing2 import Env_Constant_Test_Doing2
# from env_constant_test3 import Env_Constant_Test3
from env_constant_test4_get_resource import Env_Constant_Test4_Get_Resource
# from env_constant_test4_get_resource_board import Env_Constant_Test4_Get_Resource_Board
# from env_constant_catan_teacher4_husei import Env_Constant_Catan_Teacher4_Husei
# from env_constant_catan_teacher6 import Env_Constant_Catan_Teacher6
# from env_constant_catan_teacher7 import Env_Constant_Catan_Teacher7
# from env_constant_catan_teacher8_reward2n import Env_Constant_Catan_Teacher8_Reward2n
# from env_constant_catan_teacher9_reward2n import Env_Constant_Catan_Teacher9_Reward2n
from env_constant_catan_teacher_output import Env_Constant_Catan_Teacher_Output
# from env_constant_test import Env_Constant_Test
# from env_constant_test_random_board import Env_Constant_Test_Random_Board
# from env_constant_test_random_board_doing import Env_Constant_Test_Random_Board_Doing
# # from env_constant_test_random_board_doing2 import Env_Constant_Test_Random_Board_Doing2
# from env_constant_catan_teacher import Env_Constant_Catan_Teacher
# # from env_constant_test2 import Env_Constant_Test
import time

import setting


#env = Env_Catan()
#env = Env_Constant_Catan()
#env = Env_Comb_Catan()
# env = Env_Constant_Catan_player4()
# env=Env_Enemy()
# env = Env_Constant_Test4_Get_Resource()
# env = Env_Constant_Test4_Get_Resource()
# env = Env_Constant_Catan_Teacher4_Husei()
# env = Env_Constant_Test_Random_Board_Doing()
# env = Env_Constant_Catan_Teacher6()
# env = Env_Constant_Catan_Teacher7()
# env = Env_Constant_Catan_Teacher8_Reward2n()
env = Env_Constant_Catan_Teacher_Output()
if len(sys.argv) > 1:

    args = sys.argv

    model = DQN.load(f"./code/save_weights_constant/rl_model_{args[1]}_steps")

else:

    # model = DQN.load(

    #     f"./save_weights_constant/rl_model_{setting.default_total_timesteps}_steps")
    # model = DQN.load(
    #     f"./save_weights_test4_get_resource_20230113_conti10000000-12000000/rl_model_25000000_steps")
    # model = DQN.load(
        # f"./save_weights_teacher8_20230124_conti141000000/rl_model_300000_steps")
    model = DQN.load(
        f"./save_weights_teacher8_20230117/rl_model_103000000_steps.zip")
        # ./tmp/test_dqn


# 10回試行する

for i in range(10000):

    obs = env.reset()

    for j in range(2000):

        # time.sleep(0.001)

        action, _states = model.predict(obs)

        obs, rewards, dones, info = env.step(action)

        # env.render()

        if dones:

            break

env.close()

import sys

from stable_baselines3 import DQN


from env_catan import Env_Catan
from env_constant_catan import Env_Constant_Catan
from env_comb_catan import Env_Comb_Catan
from env_player4 import Env_Constant_Catan_player4
from env_enemy import Env_Enemy
from env_constant_catan_teacher import Env_Constant_Catan_Teacher
from env_constant_catan_teacher2 import Env_Constant_Catan_Teacher2
from env_constant_catan_teacher3 import Env_Constant_Catan_Teacher3
from env_constant_catan_teacher5_noenemy import Env_Constant_Catan_Teacher5_Noenemy
from env_constant_test4_get_resource_board import Env_Constant_Test4_Get_Resource_Board
from env_comb_20230123 import Env_Comb_20230123
from env_comb_20230123_output2_view import Env_Comb_20230123_Output2_View
from ecc import *
import time

import setting


#env = Env_Catan()
#env = Env_Constant_Catan()
env = Env_Comb_20230123_Output2_View()
# env=Env_Enemy()
# env = Env_Constant_Catan_Teacher()
# env = Env_Constant_Catan_Teacher5_Noenemy()
# env = Env_Constant_Test4_Get_Resource_Board()
# env=Env_Enemy()
if len(sys.argv) > 1:

    args = sys.argv

    model = DQN.load(f"./code/save_weights_constant/rl_model_{args[1]}_steps")

else:

    # model = DQN.load(
    # model = DQN.load(
    #     f"./save_weights_teacher_conti36000000/rl_model_20000000_steps")
    # #     f"./save_weights_constant/rl_model_{setting.default_total_timesteps}_steps")
    model = DQN.load(
        f"./save_weights_comb_20230126_typeB_3/rl_model_12000000_steps")
    # model = DQN.load("./save_weights_teacher8_20230117/rl_model_100000000_steps",
    #              env, verbose=1, tensorboard_log="log", device="auto")


# 10回試行する

for i in range(10000):

    obs = env.reset()

    for j in range(2000):

        # time.sleep(0.001)

        action, _states = model.predict(obs)
        # env.render()
        obs, rewards, dones, info = env.step(action)

        env.render()

        if dones:

            break

env.close()

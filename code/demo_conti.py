import sys

from stable_baselines3 import DQN


from env_catan import Env_Catan
from env_constant_catan import Env_Constant_Catan
from env_comb_catan import Env_Comb_Catan
import time

import setting_conti


#env = Env_Catan()
#env = Env_Constant_Catan()
env = Env_Comb_Catan()

if len(sys.argv) > 1:

    args = sys.argv

    model = DQN.load(f"./save_weights_conti/rl_model_{args[1]}_steps")

else:

    model = DQN.load(

        f"./save_weights_conti/rl_model_{setting_conti.default_total_timesteps}_steps")


# 10回試行する

for i in range(100):

    obs = env.reset()

    for j in range(2000):

        # time.sleep(0.001)

        action, _states = model.predict(obs)

        obs, rewards, dones, info = env.step(action)

        #env.render()

        if dones:

            break

env.close()

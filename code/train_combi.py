from stable_baselines3 import DQN

from stable_baselines3.common.callbacks import CheckpointCallback

from stable_baselines3.common.evaluation import evaluate_policy


import time

from board import *
from constant_board import *
from gameView import *
from player import *
from heuristicAIPlayer import *
from env_catan import *
from env_constant_catan import *
from env_comb_catan2 import *
from env_player4 import *
import setting
import queue
import numpy as np
import sys
import pygame
import matplotlib.pyplot as plt
from os import environ
environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"
# DEVICE = "gpu_limited"  # ["cpu", "gpu_limited", "gpu_unlimited"]


# if (DEVICE == "cpu"):

#     environ["CUDA_VISIBLE_DEVICES"] = "-1"

# elif (DEVICE == "gpu_limited"):

#     environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

# elif (DEVICE == "gpu_unlimited"):

#     pass


env_num=2
if(env_num==1):
    env = Env_Constant_Catan()
    checkpoint_callback = CheckpointCallback(

    save_freq=setting.default_save_freq, save_path="./save_weights_constant/")
elif(env_num==2):
    env = Env_Comb_Catan()
    checkpoint_callback = CheckpointCallback(

    save_freq=setting.default_save_freq, save_path="./save_weights_combi/")
elif(env_num==3):
    env = Env_Constant_Catan_player4()
    checkpoint_callback = CheckpointCallback(

    save_freq=setting.default_save_freq, save_path="./save_weights_player4/")

#env = Env_Catan()
#env = Env_Constant_Catan()
#env = Env_Comb_Catan()
#env = Monitor(env, log_dir, allow_early_resets=True)

model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="log", learning_rate=0.000025, device="auto")


print("start learning")

time_start = time.perf_counter()


# checkpoint_callback = CheckpointCallback(

#     save_freq=setting.default_save_freq, save_path="./save_weights/")

model.learn(total_timesteps=setting.default_total_timesteps,

            callback=checkpoint_callback)

time_end = time.perf_counter()

print("finish learning")

print(time_end - time_start)

#eval_env = Env_Catan()
#eval_env = Env_Constant_Catan()
eval_env = Env_Comb_Catan()
#eval_env = Env_Constant_Catan_player4()
mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=10)
print('Mean reward: {} +/- {}'.format(mean_reward, std_reward))


del model


# ログを見るやつ　　tensorboard --logdir log

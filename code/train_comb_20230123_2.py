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
from env_comb_lose import *
from env_comb_catan2 import *
from env_comb_20230116 import *
from env_comb_20230123 import *
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


#env = Env_Catan()
env = Env_Comb_20230123()
#env = Env_Comb_Catan_conti()
#env = Monitor(env, log_dir, allow_early_resets=True)

# model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="log", device="auto")
model = DQN.load("./save_weights_teacher8_20230117/rl_model_100000000_steps",
                 env, verbose=1, tensorboard_log="log", device="auto")
# model = DQN.load("./save_weights_comb_20230123_typeA/rl_model_10000000_steps",
#                  env, verbose=1, tensorboard_log="log", device="auto")


print("start learning")

time_start = time.perf_counter()

checkpoint_callback = CheckpointCallback(

    save_freq=setting.default_save_freq, save_path="./save_weights_comb_20230126_typeB_2")

model.learn(total_timesteps=setting.default_total_timesteps,

            callback=checkpoint_callback)

# num = 500000

# for i in range(1000):
#     if(i != 0):
#         model = DQN.load(
#             f"./tmp/comb_0123_dqn_{num*(i)}", env, verbose=1, tensorboard_log="log", device="auto")
#     else:
#         model = DQN.load("./save_weights_comb_20230123_typeA/rl_model_10000000_steps",
#                          env, verbose=1, tensorboard_log="log", device="auto")
#     model.learn(num)
#     model.save(f"./tmp/comb_0123_dqn_{num*(i+1)}")
#     del model

time_end = time.perf_counter()

print("finish learning")

print(time_end - time_start)

# #eval_env = Env_Catan()
# eval_env = Env_Comb_Catan_Lose()
# #eval_env = Env_Comb_Catan_conti()
# mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=10)
# print('Mean reward: {} +/- {}'.format(mean_reward, std_reward))


del model


# ログを見るやつ　　tensorboard --logdir log

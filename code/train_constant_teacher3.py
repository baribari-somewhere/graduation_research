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
from env_constant_catan_teacher2 import *
from env_comb_catan import *
from env_general_comb import *
# from env_constant_improve import *
import setting
import queue
import numpy as np
import sys
import pygame
import matplotlib.pyplot as plt
from os import environ

DEVICE = "gpu_limited"  # ["cpu", "gpu_limited", "gpu_unlimited"]


if (DEVICE == "cpu"):

    environ["CUDA_VISIBLE_DEVICES"] = "-1"

elif (DEVICE == "gpu_limited"):

    environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

elif (DEVICE == "gpu_unlimited"):

    pass


#env = Env_Catan()
env = Env_Constant_Catan_Teacher2()
# env = Env_General_comb()
#env = Env_Comb_Catan()
# env = Env_Constant_improve_Catan()
#env = Monitor(env, log_dir, allow_early_resets=True)

# model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="log",
#             device="auto")

model = DQN.load("./save_weights_teacher_20230108/rl_model_125000000_steps",
                 env, verbose=1, tensorboard_log="log", device="auto")

# print("start learning")

time_start = time.perf_counter()

checkpoint_callback = CheckpointCallback(

    save_freq=setting.default_save_freq, save_path="save_weights_teacher_20230108_conti125000000")

model.learn(total_timesteps=setting.default_total_timesteps,

            callback=checkpoint_callback)
# model.learn(total_timesteps=1000000)

time_end = time.perf_counter()

# print("finish learning")

# print(time_end - time_start)

# #eval_env = Env_Catan()
# eval_env = Env_Constant_Test()
# #eval_env = Env_Comb_Catan()
# mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=10)
# # print('Mean reward: {} +/- {}'.format(mean_reward, std_reward))


del model


# ログを見るやつ　　tensorboard --logdir log

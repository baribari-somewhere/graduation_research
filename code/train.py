from stable_baselines3 import DQN

from stable_baselines3.common.callbacks import CheckpointCallback

import time

from board import *
from gameView import *
from player import *
from heuristicAIPlayer import *
from env_catan import *
import setting
import queue
import numpy as np
import sys
import pygame
import matplotlib.pyplot as plt

env = Env_Catan()

model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="log", device="auto")


print("start learning")

time_start = time.perf_counter()

checkpoint_callback = CheckpointCallback(

    save_freq=setting.default_save_freq, save_path="./save_weights_police/")

model.learn(total_timesteps=setting.default_total_timesteps,

            callback=checkpoint_callback)

time_end = time.perf_counter()

print("finish learning")

print(time_end - time_start)

del model


import gym
import numpy as np
from gym import spaces
from player import *
#from board import *
from constant_board import *
from gameView import *
from player import *
from heuristicAIPlayer import *
from myAI import *
import queue
import numpy as np
import sys
import pygame
import matplotlib.pyplot as plt
import time
from typing import Literal

from action import ACTION
import collections


class Env_Plane_Catan(gym.Env):
    ACTION_MAP = np.array(ACTION)

    def __init__(self):
        #print("Initializing Settlers of Catan with only AI Players...")
        self.board = constant_catanBoard()

        # Game State variables(ゲームステート変数)
        self.gameOver = False
        self.maxPoints = 10
        self.numPlayers = 4
        self.team_V = False
        self.turn_count = 0

        self.point = 0

        self.count = 0

        self.build_F = False
        self.road_F = False

        self.save_road_dic = self.get_road_origin()

        self.change = False
        self.dicerolled = False

        # self.result = [0, 0, 0, 0]
        self.game_count = 1

        # Dictionary to keep track of dice statistics（サイコロの統計情報を記録する辞書）
        self.diceStats = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0,
                          7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
        self.diceStats_list = []

        # Initialize blank player queue and initial set up of roads + settlements（プレイヤーキューを空白にし、道路と集落を初期設定する）
        self.playerQueue = queue.Queue(self.numPlayers)
        self.gameSetup = True  # Boolean to take care of setup phase（ブール値でセットアップ段階を管理）

        # Initialize boardview object（ボードビューオブジェクトの初期化）
        self.boardView = catanGameView(self.board, self)

        # self.resources = {'ORE': 0, 'BRICK': 4,
        #                   'WHEAT': 2, 'WOOD': 4, 'SHEEP': 2}

        # Functiont to go through initial set up（初期セットアップを行うための関数）
        self.build_initial_settlements()
        # self.playCatan()

        self.isAI = True
        self.setupResources = []

        # print(f"self.ACTION_MAP:{self.ACTION_MAP}")
        # アクション数定義
        ACTION_NUM = len(self.ACTION_MAP)
        self.action_space = gym.spaces.Discrete(ACTION_NUM)
        self.observation_space = spaces.flatten_space(
            self.OBSERVATION_SPACE())
        # print(self.board.vertex_index_to_pixel_dict)

    # def step(self, action_index: int, board):

    def step(self, action_index: int):

        action = self.ACTION_MAP[action_index]
        done = False
        #reward = 0
        #numTurns = 0
        self.point = 0

        self.build_position = self.board.get_potential_cities(
            self.playerQueue.queue[0])
        self.road_position = self.board.get_potential_roads(
            self.playerQueue.queue[0])

        # print(f"action_index:{action_index}")

        for currPlayer in self.playerQueue.queue:
            # if(self.dicerolled == False):
            #     self.turn_count += 1
            #     diceNum = self.rollDice()
            #     diceRolled = True
            #     self.update_playerResources(diceNum, currPlayer)
            #     self.diceStats[diceNum] += 1
            #     self.diceStats_list.append(diceNum)
            #     self.dicerolled = True

            self.turn_count += 1
            diceNum = self.rollDice()
            diceRolled = True
            self.update_playerResources(diceNum, currPlayer)
            self.diceStats[diceNum] += 1
            self.diceStats_list.append(diceNum)
            self.dicerolled = True

            # currPlayer.updateDevCards()
            # currPlayer.devCardPlayedThisTurn = False

            if(self.turn_count >= 1000):
                reward -= 50
                done = True

            if(currPlayer.name == 'player1' and self.change == False):
                #print("player1 playing...")
                # print(f"self.change = {self.change}")

                self.action_input(action, currPlayer)

                reward = self.point
                # print(reward)

            elif(self.change == True):
                # print(currPlayer.name)
                # currPlayer.move(self.board)
                self.dicerolled = False
                if(currPlayer.name == "player4"):
                    self.change = False

            self.check_longest_road(currPlayer)
            if currPlayer.victoryPoints >= self.maxPoints:
                if(currPlayer.name == "player1"):
                    reward += 500000
                Over_Flag = True
                p_v = currPlayer.name

                p_team = self.check_team(currPlayer)
                self.gameOver = True
                self.turnOver = True
                # print(self.board.printGraph())
                # print("====================================================")
                # print(f"WINNER {currPlayer.name}")
                # print("{} & {} WINS IN {} TURNS!".format(
                #     p_v, p_team, int(self.turn_count)))
                # print(self.diceStats)
                # print("Exiting game in 10 seconds...")

                # if(currPlayer == "player1"):
                #     self.result[0] = self.result[0] + 1
                # if(currPlayer == "player2"):
                #     self.result[1] = self.result[1] + 1
                # if(currPlayer == "player3"):
                #     self.result[2] = self.result[2] + 1
                # if(currPlayer == "player14"):
                #     self.result[3] = self.result[3] + 1

                # total = self.result[0]+self.result[1] + \
                #     self.result[2]+self.result[3]

                if(self.game_count == 1):
                    f = open('result.txt', 'w')
                    f.write(f"{currPlayer.name}\n")
                else:
                    f = open('result.txt', 'a')
                    f.write(f"{currPlayer.name}\n")
                self.game_count += 1

                # print(self.result)
                # f = open('result.txt', 'a')
                # f.write(currPlayer.name)
                # if(self.game_count == 100):
                #     f.write(f"total_result：{self.result}")
                #     f.write(f"rate：{float(self.result[0]/total)}")
                # pygame.time.delay(5000)

                done = True

            # 辞書順board_resources,city,have_develop,have_resources,road,
            # robber_resources,settlement

        observation = np.array([])

        # どのマスにどの資源が設定されているか
        resource_list = self.check_board_resources(
            self.board.resourcesList)

        # 発展カード
        dev_list = self.get_DV()

        # 盗賊がどこにいるか
        robber_position = self.board.get_robber()

        # なんの資源を持っているか
        my_resource = self.check_have_resources()

        settle_city = self.set_thing()
        road = self.get_road()

        # observation = np.append(observation, np.array([resource_list, new_city, dev_list,
        #                         my_resource, new_road, robber_position, new_settlement]))

        # observation = np.append(observation, np.array([my_resource, dev_list,
        #                          road, robber_position, set&city]))

        #observation = np.append(observation, np.array([resource_list]))
        observation = np.append(observation, np.array([my_resource]))
        observation = np.append(observation, np.array([dev_list]))
        observation = np.append(observation, np.array([road]))
        observation = np.append(observation, np.array([robber_position]))
        observation = np.append(observation, np.array([settle_city]))
        # print(f"reward:{reward}")
        # print(f"my_resource: {my_resource}")
        # print(f"dev_list: {dev_list}")
        # print(f"road: {road}")
        # print(f"robber_position: {robber_position}")
        # print(f"settle_city: {settle_city}")

        # observation→observation_spaceに対応する値をnp.arrayの型で返却する※observation_spaceは辞書順(アルファベット順)で並んでいるので注意
        # print(observation)
        return observation, reward, done, {}

    def reset(self):

        self.board = constant_catanBoard()

        # Game State variables(ゲームステート変数)
        self.gameOver = False
        self.maxPoints = 10
        self.numPlayers = 4
        self.team_V = False
        self.change = False
        self.turn_count = 0
        self.point = 0
        self.change = False
        self.dicerolled = False
        # Dictionary to keep track of dice statistics（サイコロの統計情報を記録する辞書）
        self.diceStats = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0,
                          7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
        self.diceStats_list = []

        # Only accept 3 and 4 player games（3人および4人用のゲームのみをサポート）
        # while(self.numPlayers not in [3, 4]):
        #     try:
        #         self.numPlayers = int(
        #             input("Enter Number of Players (3 or 4):"))
        #     except:
        #         print("Please input a valid number")

        # print("Initializing game with {} players...".format(self.numPlayers))
        # print("Note that Player 1 goes first, Player 2 second and so forth.")

        # Initialize blank player queue and initial set up of roads + settlements（プレイヤーキューを空白にし、道路と集落を初期設定する）
        self.playerQueue = queue.Queue(self.numPlayers)
        self.gameSetup = True  # Boolean to take care of setup phase（ブール値でセットアップ段階を管理）

        # Initialize boardview object（ボードビューオブジェクトの初期化）
        self.boardView = catanGameView(self.board, self)

        # self.resources = {'ORE': 0, 'BRICK': 4,
        #                   'WHEAT': 2, 'WOOD': 4, 'SHEEP': 2}

        # Functiont to go through initial set up（初期セットアップを行うための関数）
        self.build_initial_settlements()

        observation = np.array([])

        # どのマスにどの資源が設定されているか
        resource_list = self.check_board_resources(
            self.board.resourcesList)

       # 発展カード
        #dev_list = self.get_DV(currPlayer)

        # 盗賊がどこにいるか
        robber_position = self.board.get_robber()

        # なんの資源を持っているか
        my_resource = self.check_have_resources()

        settle_city = self.set_thing()
        road = self.get_road()

        observation = np.append(observation, np.array([my_resource]))
        observation = np.append(observation, np.array([np.zeros(8)]))
        observation = np.append(observation, np.array([road]))
        observation = np.append(observation, np.array([robber_position]))
        observation = np.append(observation, np.array([settle_city]))

        self.isAI = True
        self.setupResources = []

        return observation

    def render(self, mode: Literal["human", "rgb_array", "ansi"] = "human") -> None:
        """描画関数
        mode の引数によって以下の変化がある
        | 引数名 | 内容 | 返り値 |
        | ---- | ---- | ---- |
        | human | 人にとって認識しやすいように可視化, 環境をポップアップ画面に表示 | なし |
        | rgb_array | 返り値の生成処理 | shape=(x, y, 3)のndarray |
        | ansi | 返り値の生成処理 | ansi文字列(str)もしくはStringIO.StringIO |
        """
        # self.boardView = catanGameView(self.board, self)
        if mode == "human":
            #self.boardView = catanGameView(self.board, self)
            time.sleep(0.1)
            #plt.hist(self.diceStats_list, bins=11)
            # plt.show()
            # pygame.event.pump()
            self.boardView.displayGameScreen()

            pygame.display.update()

    def OBSERVATION_SPACE(self):
        # 各タイルの資源（資源,マスの値）
        OBS_SPACE = spaces.Dict({
            # 各タイルの資源（資源,マスの値）
            # 1:desert,2:ore.3:brick,4:wheat,5:wood,6:sheep
            # "board_resources": spaces.Box(
            #     low=np.array([1, 2]),
            #     high=np.array([5, 12]),
            #     dtype=np.uint8
            # ),

            "robber_resources": spaces.Box(
                low=np.array([0]),
                high=np.array([len(self.board.hexTileDict)]),
                dtype=np.uint8
            ),
            # 所持している発展カード（種類,枚数）
            # 0:knight,1:VP,2:MONOPOLY,3:ROADBUILDER,4:YEAROFPLENTY
            "have_develop": spaces.Box(
                low=np.array(np.zeros(8)),
                high=np.array(np.full(8, 20)),  # 最大枚数は後で調整
                dtype=np.uint8
            ),

            # # 所持している資源カード（種類,枚数）
            # 0:ore.1:brick,2:wheat,3:wood,4:sheep
            "have_resources": spaces.Box(
                low=np.array(np.zeros(20)),
                high=np.array(np.full(20, 20)),  # 最大枚数は後で調整
                dtype=np.uint8
            ),
            "set_city": spaces.Box(
                low=np.array(np.zeros(54)),
                high=np.array(np.full(54, 1)),   # 最大枚数は後で調整
                dtype=np.uint8
            ),

            "road": spaces.Box(
                low=np.array(np.zeros(72)),
                high=np.array(np.full(72, 1)),  # 最大枚数は後で調整
                dtype=np.uint8
            ),
            # "PieceID1": spaces.Box(low=0, high=6, dtype=np.uint8),

        })

        return OBS_SPACE

    def int_check_convert(self, obj):
        if isinstance(int(obj), int):
            return True

    def int_check(self, obj):
        if isinstance(obj, int):
            return True

    def tuple_check(self, obj):
        if isinstance(obj, tuple):
            return True

    def str_check(self, obj):
        if isinstance(obj, str):
            return True

    def action_input(self, action, Player):

        self.point = 0

        self.count += 1

        # print(f"action: {action}")

        # if(self.count > 100):
        #     exit()
        # # print(f"action:{action}")
        # print(action)
        if(action[0] == "4"):
            count1 = 0
            count2 = 0
            for r1, r1_amount in Player.resources.items():
                for r2, r2_amount in Player.resources.items():
                    if(count1 == action[1][0] and count2 == action[1][1]):
                        Player.trade_with_bank(r1, r2)
                        self.change = True
                        self.dicerolled = False
                        break

                    count2 += 1
                count1 += 1

        elif(action[0] == "3"):
            self.build_position = self.board.vertex_index_to_pixel_dict[int(
                action[1])]
            self.build_F = True
            if(action[2] == "S"):
                if(self.build_F == True):
                    if((Player.resources['BRICK'] > 0 and Player.resources['WOOD'] > 0 and Player.resources['SHEEP'] > 0 and Player.resources['WHEAT'] > 0)):
                        possibleSettlements = self.board.get_potential_settlements(
                            Player)
                        #print(f"possibleSettlements: {possibleSettlements}")
                        if(self.build_position in possibleSettlements.keys()):
                            Player.build_settlement(self.build_position,
                                                    self.board)
                            self.point += 10000
                            # print("settlement")
                        self.build_F = False
                self.change = True
                self.dicerolled = False
            #self.action_input(action[1:], Player)
            elif(action[2] == "C"):
                if(self.build_F == True):
                    if(Player.resources['WHEAT'] >= 2 and Player.resources['ORE'] >= 3):
                        possibleCities = self.board.get_potential_cities(
                            Player)
                        #print(f"possibleCities: {possibleCities}")
                        if(self.build_position in possibleCities.keys()):
                            Player.build_city(self.build_position, self.board)
                            self.point += 10000
                            # print("City")
                        self.build_F = False

        elif(action[0] == "2"):
            self.road_position = (
                self.board.vertex_index_to_pixel_dict[action[1][0]], self.board.vertex_index_to_pixel_dict[action[1][1]])
            self.road_F = True
            if(self.road_F == True):
                # print("roadあり")
                if(Player.resources['BRICK'] > 0 and Player.resources['WOOD'] > 0):

                    possibleRoads = self.board.get_potential_roads(Player)
                    #print(f"possibleRoads: {possibleRoads}")
                    if((self.road_position[0], self.road_position[1]) in possibleRoads.keys()):
                        Player.build_road(self.road_position[0],
                                          self.road_position[1], self.board)
                        self.point += 500
                        # print("road")
                        # else:
                        #     print("場所無し")
                        self.road_F = False

                    # else:
                    #     print("素材無し")
            #self.action_input(action[1:], Player)

        elif(action[0] == "1"):
            # self.sample(action)
            # print(action)
            # exit()
            if(action[1] == "d"):
                Player.draw_devCard(self.board)
                self.point += 10
                #self.point += 0.1
                a = 0
            elif(action[1] == "u"):
                Player.play_devCard(Player)
                self.point += 100
                a = 0

            elif(action[1] == "p"):
                self.change = True
                self.dicerolled = False
                #self.point = 10
                # print("ok")
                a = 0
            elif(action[1] == "t"):
                for r1, r1_amount in Player.resources.items():
                    # heuristic to trade if a player has more than 5 of a particular resource（プレイヤーが特定のリソースを5つ以上持っている場合のヒューリスティックトレード）
                    if(r1_amount >= 6):
                        for r2, r2_amount in Player.resources.items():
                            if(r2_amount < 1):
                                self.trade_with_bank(r1, r2)
                                break
        self.change = True
        self.dicerolled = False

    # def action_input(self, action, Player):

    #     self.point = 0

    #     self.count += 1

    #    #print(f"action: {action}")

    #     # if(self.count > 100):
    #     #     exit()
    #     # print(f"action:{action}")
    #     if(self.int_check(action[0])):
    #         self.build_position = self.board.vertex_index_to_pixel_dict[int(
    #             action[0])]
    #         self.build_F = True
    #         self.action_input(action[1:], Player)

    #     elif(self.tuple_check(action[0])):
    #         self.road_position = (
    #             self.board.vertex_index_to_pixel_dict[action[0][0]], self.board.vertex_index_to_pixel_dict[action[0][1]])
    #         self.road_F = True
    #         self.action_input(action[1:], Player)

    #     elif(len(action[0]) == 1):
    #         # self.sample(action)
    #         # print(action)
    #         # exit()
    #         if(action[0] == "d"):
    #             Player.draw_devCard(self.board)

    #             #self.point += 0.1
    #             a = 0
    #         elif(action[0] == "u"):
    #             Player.play_devCard(Player)
    #             a = 0
    #         elif(action[0] == "R"):
    #             if(self.road_F == True):
    #                 # print("roadあり")
    #                 if(Player.resources['BRICK'] > 0 and Player.resources['WOOD'] > 0):

    #                     possibleRoads = self.board.get_potential_roads(Player)
    #                     #print(f"possibleRoads: {possibleRoads}")
    #                     if((self.road_position[0], self.road_position[1]) in possibleRoads.keys()):
    #                         Player.build_road(self.road_position[0],
    #                                           self.road_position[1], self.board)
    #                         self.point += 10
    #                         # print("road")
    #                     # else:
    #                     #     print("場所無し")
    #                     self.road_F = False

    #                 # else:
    #                 #     print("素材無し")

    #         elif(action[0] == "S"):
    #             if(self.build_F == True):
    #                 if((Player.resources['BRICK'] > 0 and Player.resources['WOOD'] > 0 and Player.resources['SHEEP'] > 0 and Player.resources['WHEAT'] > 0)):
    #                     possibleSettlements = self.board.get_potential_settlements(
    #                         Player)
    #                     #print(f"possibleSettlements: {possibleSettlements}")
    #                     if(self.build_position in possibleSettlements.keys()):
    #                         Player.build_settlement(self.build_position,
    #                                                 self.board)
    #                         self.point += 25
    #                         # print("settlement")
    #                     self.build_F = False
    #             a = 0
    #         elif(action[0] == "C"):
    #             if(self.build_F == True):
    #                 if(Player.resources['WHEAT'] >= 2 and Player.resources['ORE'] >= 3):
    #                     possibleCities = self.board.get_potential_cities(
    #                         Player)
    #                     #print(f"possibleCities: {possibleCities}")
    #                     if(self.build_position in possibleCities.keys()):
    #                         Player.build_city(self.build_position, self.board)
    #                         self.point += 35
    #                         # print("City")
    #                     self.build_F = False
    #                     # print("City")
    #             a = 0
    #         elif(action[0] == "p"):
    #             self.change = True
    #             self.dicerolled = False
    #             #self.point = 10
    #             a = 0
    #         elif(action[0] == "t"):
    #             for r1, r1_amount in Player.resources.items():
    #                 # heuristic to trade if a player has more than 5 of a particular resource（プレイヤーが特定のリソースを5つ以上持っている場合のヒューリスティックトレード）
    #                 if(r1_amount >= 6):
    #                     for r2, r2_amount in Player.resources.items():
    #                         if(r2_amount < 1):
    #                             self.trade_with_bank(r1, r2)
    #                             break

    #     else:
    #         self.action_input(action[0][0], Player)
    #         self.action_input(action[0][1:], Player)

    def check_team(self, player):
        if(player.name == "player1"):
            return "player3"
        elif(player.name == "player2"):
            return "player4"
        elif(player.name == "player3"):
            return "player1"
        elif(player.name == "player4"):
            return "player2"

    def check_board_resources(self, resources):
        resource_list = np.array([])
        for i in resources:
            if(i.type == "DESERT"):
                resource_list = np.append(resource_list, [1, i.num])
            elif(i.type == "ORE"):
                resource_list = np.append(resource_list, [2, i.num])
            elif(i.type == "BRICK"):
                resource_list = np.append(resource_list, [3, i.num])
            elif(i.type == "WHEAT"):
                resource_list = np.append(resource_list, [4, i.num])
            elif(i.type == "WOOD"):
                resource_list = np.append(resource_list, [5, i.num])
            elif(i.type == "SHEEP"):
                resource_list = np.append(resource_list, [6, i.num])
        return resource_list

    # settlementとcityを1つのリストで表現
    # 0:何もなし 1:player1のsettlement 2:player1のcity...

    def set_thing(self):
        thing_list = np.array(np.zeros(54))
        count = 1
        for player_i in self.player_set:

            for key in player_i.buildGraph.keys():
                # print(key)
                if(key == "SETTLEMENTS"):
                    # print("aaa")
                    #[key for key, value in self.board.vertex_index_to_pixel_dict.items() if value == player_i.buildGraph[key]]
                    for j in player_i.buildGraph[key]:
                        # print(j)
                        index = [
                            key for key, value in self.board.vertex_index_to_pixel_dict.items() if value == j]
                        thing_list[index[0]] = count
                elif(key == "CITIES"):
                    for j in player_i.buildGraph[key]:
                        index = [
                            key for key, value in self.board.vertex_index_to_pixel_dict.items() if value == j]
                        thing_list[index[0]] = count+1
            count += 2
        # print(f"set_city:{thing_list}")
        return thing_list

    # def get_DV(self, currplayer):
    #     dev_list = np.array([])
    #     count = 1
    #     for i in currplayer.devCard.keys():
    #         dev_list = np.append(dev_list, [count, currplayer.devCard[i]])

    #     return dev_list

    # def get_DV(self, currplayer):
    #     dev_list = np.array([])
    #     count = 1
    #     for i in currplayer.devCards.keys():
    #         dev_list = np.append(dev_list, np.array([currplayer.devCards[i]]))

    #     return dev_list

    def get_DV(self):
        dev_list = np.array([])
        for player_i in self.player_set:
            for i in player_i.devCards.keys():
                dev_list = np.append(
                    dev_list, np.array([player_i.devCards[i]]))
        return dev_list

    def get_key(self, d, val_search):
        keys = [key for key, value in d.items() if value == val_search]
        if keys:
            return keys
        else:
            return None

    def sample(self, obj):

        if isinstance(obj, bool):
            print('bool型です')

        if isinstance(obj, int):
            print('int型です')

        if isinstance(obj, float):
            print('float型です')

        if isinstance(obj, complex):
            print('complex型です')

        if isinstance(obj, list):
            print('list型です')

        if isinstance(obj, tuple):
            print('tuple型です')

        if isinstance(obj, range):
            print('range型です')

        if isinstance(obj, str):
            print('str型です')

        if isinstance(obj, set):
            print('set型です')

        if isinstance(obj, frozenset):
            print('frozenset型です')

        if isinstance(obj, dict):
            print('dict型です')

    def get_road_origin(self):
        # road_list=np.array(np.zeros(72))
        # updateGraphEdgesがヒントになりそう
        save_dic = {}
        count = 0
        # print(
        #     f"self.board.vertex_index_to_pixel_dict{self.board.vertex_index_to_pixel_dict}")
        for i in range(54):
            for j in range(54):
                if(i < j):
                    # self.board.vertex_index_to_pixel_dict[]
                    if(self.board.vertexDistance(self.board.vertex_index_to_pixel_dict[i], self.board.vertex_index_to_pixel_dict[j]) == self.board.edgeLength):
                        #save_dic[i, j] = count
                        save_dic[count] = (i, j)
                        count += 1
        if(len(save_dic) != 72):
            print("道路の数がエラー")
        # print(save_dic)

        return save_dic

    # 0:道無し 1:playre1の道 2:player2の道...

    def get_road(self):

        road_list = np.array(np.zeros(72))
        count = 1
        for player_i in self.player_set:
            for key in player_i.buildGraph.keys():
                if(key == "ROADS"):
                    save_list = player_i.buildGraph[key]
                    # print(save_list)
                    # print(f"save_dic{save_dic}")
                    for i in save_list:
                        # print(i[0])
                        # print(i[1])
                        edge1 = self.get_key(
                            self.board.vertex_index_to_pixel_dict, i[0])
                        edge2 = self.get_key(
                            self.board.vertex_index_to_pixel_dict, i[1])
                        if(edge1 > edge2):
                            x = edge1
                            edge1 = edge2
                            edge2 = x

                        # print(edge1)
                        # print(edge2)
                        #self.sample(tuple([edge1, edge2]))
                        # for j in save_dic.keys():
                        #     if(i == j):
                        #         road_list[save_dic[j]] = count
                        # print(f"save_dic{save_dic}")
                        #print(tuple([edge1[0], edge2[0]]))
                        edge_index = self.get_key(
                            self.save_road_dic, tuple([edge1[0], edge2[0]]))
                        # print(f"edge_index:{edge_index}")
                        # print(f"road_list:{road_list}")
                        road_list[edge_index] = count
            count += 1
        # print(f"road:{road_list}")
        return road_list

    # player_setがプレイヤー1から4を格納したリスト

    def check_have_resources(self):
        resource_list = np.array([])
        count = 1
        for player_i in self.player_set:
            for i in player_i.resources.keys():
                resource_list = np.append(
                    resource_list, np.array([player_i.resources[i]]))
            count += 1
        # print(f"resource_list:{resource_list}")
        return resource_list

    def initial_setup(self, board):
        # Build random settlement（ランダムな集落を作る）
        possibleVertices = board.get_setup_settlements(self)

        # Simple heuristic for choosing initial spot（初期位置の選択に関するシンプルなヒューリスティック）
        diceRoll_expectation = {2: 1, 3: 2, 4: 3, 5: 4,
                                6: 5, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1, None: 0}
        vertexValues = []

        # Get the adjacent hexes for each hex（各ヘクスの隣接ヘクスを取得）
        for v in possibleVertices.keys():
            vertexNumValue = 0
            resourcesAtVertex = []
            # For each adjacent hex get its value and overall resource diversity for that vertex（隣接する各ヘックスについて、その値とその頂点の全体的なリソース多様性を取得します）
            for adjacentHex in board.boardGraph[v].adjacentHexList:
                resourceType = board.hexTileDict[adjacentHex].resource.type
                if(resourceType not in resourcesAtVertex):
                    resourcesAtVertex.append(resourceType)
                numValue = board.hexTileDict[adjacentHex].resource.num
                # Add to total value of this vertex（この頂点の合計値に加算する）
                vertexNumValue += diceRoll_expectation[numValue]

            # basic heuristic for resource diversity（資源多様性のための基本的なヒューリスティック）
            vertexNumValue += len(resourcesAtVertex)*2
            for r in resourcesAtVertex:
                if(r != 'DESERT' and r not in self.setupResources):
                    vertexNumValue += 2.5  # Every new resource gets a bonus（新しいリソースにはボーナスがつく）

            vertexValues.append(vertexNumValue)

        vertexToBuild_index = vertexValues.index(max(vertexValues))
        vertexToBuild = list(possibleVertices.keys())[vertexToBuild_index]

        # Add to setup resources（セットアップリソースに追加）
        for adjacentHex in board.boardGraph[vertexToBuild].adjacentHexList:
            resourceType = board.hexTileDict[adjacentHex].resource.type
            if(resourceType not in self.setupResources and resourceType != 'DESERT'):
                self.setupResources.append(resourceType)

        self.build_settlement(vertexToBuild, board)

        # Build random road（ランダムな道路を作る）
        possibleRoads = board.get_setup_roads(self)
        randomEdge = np.random.randint(0, len(possibleRoads.keys()))
        self.build_road(list(possibleRoads.keys())[randomEdge][0], list(
            possibleRoads.keys())[randomEdge][1], board)

    def build_initial_settlements(self):
        # Initialize new players with names and colors（名前と色で新しいプレイヤーを初期化する関数）
        playerColors = ['black', 'darkslateblue', 'magenta4', 'orange1']

        self.player_set = []

        newPlayer = myAI('player1', 'black')
        newPlayer.updateAI()
        self.playerQueue.put(newPlayer)
        self.player_set.append(newPlayer)

        for i in range(3):
            #playerNameInput = input("Enter AI Player {} name: ".format(i+1))
            newPlayer = heuristicAIPlayer(f"player{i+2}", playerColors[i+1])
            newPlayer.updateAI()
            self.playerQueue.put(newPlayer)
            self.player_set.append(newPlayer)

        playerList = list(self.playerQueue.queue)

        # Build Settlements and roads of each player forwards（各プレイヤーの集落や道路を順次構築していく）
        for player_i in playerList:
            player_i.initial_setup(self.board)
            # pygame.event.pump()
            # self.boardView.displayGameScreen()
            # pygame.time.delay(1000)

        # Build Settlements and roads of each player reverse（各プレイヤーの集落と道路を逆向きに作る）
        playerList.reverse()
        for player_i in playerList:
            player_i.initial_setup(self.board)
            # pygame.event.pump()
            # self.boardView.displayGameScreen()
            # pygame.time.delay(1000)

            # print("Player {} starts with {} resources".format(
            #     player_i.name, len(player_i.setupResources)))

            # Initial resource generation（初期資源生成）
            # check each adjacent hex to latest settlement（最新の集落に隣接するヘクスをチェック）
            for adjacentHex in self.board.boardGraph[player_i.buildGraph['SETTLEMENTS'][-1]].adjacentHexList:
                resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                if(resourceGenerated != 'DESERT'):
                    player_i.resources[resourceGenerated] += 1
                    # print("{} collects 1 {} from Settlement".format(
                    #     player_i.name, resourceGenerated))

        # pygame.time.delay(5000)
        self.gameSetup = False

    # Function to roll dice （サイコロを振る機能）
    def rollDice(self):
        dice_1 = np.random.randint(1, 7)
        dice_2 = np.random.randint(1, 7)
        diceRoll = dice_1 + dice_2
        #print("Dice Roll = ", diceRoll, "{", dice_1, dice_2, "}")

        return diceRoll

    # Function to update resources for all players（全プレイヤーの資源を更新する機能）
    def update_playerResources(self, diceRoll, currentPlayer):
        if(diceRoll != 7):  # Collect resources if not a 7（7でない場合は資源を回収する）
            # First get the hex or hexes corresponding to diceRoll（最初に diceRoll に対応するヘクスを取得する）
            hexResourcesRolled = self.board.getHexResourceRolled(diceRoll)
            #print('Resources rolled this turn:', hexResourcesRolled)

            # Check for each player（各プレイヤーについて）
            for player_i in list(self.playerQueue.queue):
                # Check each settlement the player has（各プレイヤーが持つ集落をチェック）
                for settlementCoord in player_i.buildGraph['SETTLEMENTS']:
                    # check each adjacent hex to a settlement
                    for adjacentHex in self.board.boardGraph[settlementCoord].adjacentHexList:
                        # This player gets a resource if hex is adjacent and no robber
                        if(adjacentHex in hexResourcesRolled and self.board.hexTileDict[adjacentHex].robber == False):
                            resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                            player_i.resources[resourceGenerated] += 1
                            # print("{} collects 1 {} from Settlement".format(
                            #     player_i.name, resourceGenerated))

                # Check each City the player has（各プレイヤーが持つ都市をチェック）
                for cityCoord in player_i.buildGraph['CITIES']:
                    # check each adjacent hex to a settlement
                    for adjacentHex in self.board.boardGraph[cityCoord].adjacentHexList:
                        # This player gets a resource if hex is adjacent and no robber
                        if(adjacentHex in hexResourcesRolled and self.board.hexTileDict[adjacentHex].robber == False):
                            resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                            player_i.resources[resourceGenerated] += 2
                            # print("{} collects 2 {} from City".format(
                            #     player_i.name, resourceGenerated))

                # print("Player:{}, Resources:{}, Points: {}".format(
                #     player_i.name, player_i.resources, player_i.victoryPoints))
                #print('Dev Cards:{}'.format(player_i.devCards))
                #print("RoadsLeft:{}, SettlementsLeft:{}, CitiesLeft:{}".format(player_i.roadsLeft, player_i.settlementsLeft, player_i.citiesLeft))
                # print('MaxRoadLength:{}, Longest Road:{}\n'.format(
                #     player_i.maxRoadLength, player_i.longestRoadFlag))

        else:
            #print("AI using heuristic robber...")
            currentPlayer.heuristic_move_robber(self.board)

    # function to check if a player has the longest road - after building latest road（最新の道路を建設した後、最も長い道路を所有しているかどうかをチェックする機能）
    def check_longest_road(self, player_i):
        if(player_i.maxRoadLength >= 5):  # Only eligible if road length is at least 5（道路の長さが5以上である場合のみ対象）
            longestRoad = True
            for p in list(self.playerQueue.queue):
                # Check if any other players have a longer road（他のプレイヤーがより長い道路を持っているかどうかチェック）
                if(p.maxRoadLength >= player_i.maxRoadLength and p != player_i):
                    longestRoad = False

            # if player_i takes longest road and didn't already have longest road（もしplayer_iが最も長い道路を建設し，かつ既に最も長い道路を持っていなかった場合）
            if(longestRoad and player_i.longestRoadFlag == False):
                # Set previous players flag to false and give player_i the longest road points（前のプレイヤーのフラグをfalseにし，player_iに最長路のポイントを与える．）
                prevPlayer = ''
                for p in list(self.playerQueue.queue):
                    if(p.longestRoadFlag):
                        p.longestRoadFlag = False
                        p.victoryPoints -= 2
                        prevPlayer = 'from Player ' + p.name

                player_i.longestRoadFlag = True
                player_i.victoryPoints += 2

                # print("Player {} takes Longest Road {}".format(
                #     player_i.name, prevPlayer))

    # function to check if a player has the largest army - after playing latest knight（あるプレイヤーが最大の軍隊を持っているかどうかをチェックする関数 - 最新の騎士をプレイした後）
    def check_largest_army(self, player_i):
        if(player_i.knightsPlayed >= 3):  # Only eligible if at least 3 knights are player（ナイトが3人以上いる場合のみ対象）
            largestArmy = True
            for p in list(self.playerQueue.queue):
                # Check if any other players have more knights played（他のプレイヤーがより多くのナイトをプレイしているかどうかを確認する。）
                if(p.knightsPlayed >= player_i.knightsPlayed and p != player_i):
                    largestArmy = False

            # if player_i takes largest army and didn't already have it（player_iが最大の軍を持ち、まだ持っていなかった場合。）
            if(largestArmy and player_i.largestArmyFlag == False):
                # Set previous players flag to false and give player_i the largest points（前のプレイヤーのフラグをfalseに設定し、player_iに最大のポイントを与える）
                prevPlayer = ''
                for p in list(self.playerQueue.queue):
                    if(p.largestArmyFlag):
                        p.largestArmyFlag = False
                        p.victoryPoints -= 2
                        prevPlayer = 'from Player ' + p.name

                player_i.largestArmyFlag = True
                player_i.victoryPoints += 2

                # print("Player {} takes Largest Army {}".format(
                #     player_i.name, prevPlayer))

    # def build_settlement(self, vCoord, board):
    #     'Update player buildGraph and boardgraph to add a settlement on vertex v'
    #     # Take input from Player on where to build settlement
    #     # Check if player has correct resources
    #     # Update player resources and boardGraph with transaction
    #     '''
    #     プレイヤーから決済場所についての入力を受ける
    #         #プレーヤーが正しい資源を持っているかどうか確認する
    #             #プレイヤーの資源とボードグラフをトランザクションで更新する。
    #     '''

    #     # Check if player has resources available
    #     if(self.resources['BRICK'] > 0 and self.resources['WOOD'] > 0 and self.resources['SHEEP'] > 0 and self.resources['WHEAT'] > 0):
    #         if(self.settlementsLeft > 0):  # Check if player has settlements left(プレイヤーにセトリングが残っているかどうかを確認する)
    #             self.buildGraph['SETTLEMENTS'].append(vCoord)
    #             self.settlementsLeft -= 1

    #             # Update player resources(プレイヤーリソースのアップデート)
    #             self.resources['BRICK'] -= 1
    #             self.resources['WOOD'] -= 1
    #             self.resources['SHEEP'] -= 1
    #             self.resources['WHEAT'] -= 1

    #             self.victoryPoints += 1
    #             # update the overall boardGraph(boardGraph全体を更新する)
    #             board.updateBoardGraph_settlement(vCoord, self)

    #             print('{} Built a Settlement'.format(self.name))

    #             # Add port to players port list if it is a new port(新しいポートの場合、プレイヤーポートリストにポートを追加する)
    #             if((board.boardGraph[vCoord].port != False) and (board.boardGraph[vCoord].port not in self.portList)):
    #                 self.portList.append(board.boardGraph[vCoord].port)
    #                 print("{} now has {} Port access".format(
    #                     self.name, board.boardGraph[vCoord].port))

    #         else:
    #             print("No settlements available to build")

    #     else:
    #         print(
    #             "Insufficient Resources to Build Settlement. Build Cost: 1 BRICK, 1 WOOD, 1 WHEAT, 1 SHEEP")


# 前のstep

# 街道建設を選択した際にランダムに建設してる
                # if(action == "road"):
                #     # a = a
                #     if(currPlayer.resources['BRICK'] > 0 and currPlayer.resources['WOOD'] > 0):
                #         possibleRoads = self.board.get_setup_roads(self)
                #         print(f"possibleRoads:{possibleRoads}")
                #         randomEdge = np.random.randint(
                #             0, len(possibleRoads.keys()))
                #         currPlayer.build_road(list(possibleRoads.keys())[randomEdge][0], list(
                #             possibleRoads.keys())[randomEdge][1], self.board)
                #         # new_road = np.append(new_road, list(possibleRoads.keys())[randomEdge][0], list(
                #         #     possibleRoads.keys())[randomEdge][1])
                #         reward += 1
                # elif(action == "settlement"):
                #     #a = a
                #     # vCoord = 0
                #     # self.build_settlement(vCoord, board)
                #     possibleVertices = self.board.get_potential_settlements(
                #         self)
                #     if(possibleVertices != {} and (currPlayer.resources['BRICK'] > 0 and currPlayer.resources['WOOD'] > 0 and self.resources['SHEEP'] > 0 and self.resources['WHEAT'] > 0)):
                #         randomVertex = np.random.randint(
                #             0, len(possibleVertices.keys()))
                #         currPlayer.build_settlement(list(possibleVertices.keys())[
                #             randomVertex], self.board)
                #         # new_settlement = np.append(
                #         #     new_settlement, randomVertex)
                #         reward += 3

                # elif(action == "city"):
                #     #a = a
                #     # vCoord = 0
                #     # self.build_city(vCoord, board)
                #     possibleVertices = self.board.get_potential_cities(
                #         self)
                #     if(possibleVertices != {} and (currPlayer.resources['WHEAT'] >= 2 and currPlayer.resources['ORE'] >= 3)):
                #         randomVertex = np.random.randint(
                #             0, len(possibleVertices.keys()))
                #         currPlayer.build_city(list(possibleVertices.keys())[
                #             randomVertex], self.board)
                #         # new_city = np.append(new_city, randomVertex)
                #         reward += 5

                # elif(action == "dev"):
                #     #a = a
                #     currPlayer.draw_devCard(self.board)

                # elif(action == "use_dv"):
                #     #a = a
                #     currPlayer.play_devCard(self)

                # elif(action == "trade"):
                #     #a = a
                #     for r1, r1_amount in currPlayer.resources.items():
                #         # heuristic to trade if a player has more than 5 of a particular resource（プレイヤーが特定のリソースを5つ以上持っている場合のヒューリスティックトレード）
                #         if(r1_amount >= 6):
                #             for r2, r2_amount in currPlayer.resources.items():
                #                 if(r2_amount < 1):
                #                     self.trade_with_bank(r1, r2)
                #                     break
                # elif(action == "pass"):
                #     #a = a
                #     self.change = True

    # def action_input(self, action, Player):
    #     build_F = False
    #     road_F = False
    #     if(len(action) == 1):
    #         if(self.str_check(action)):
    #             if(len(action[0]) != 1):
    #                 self.action_input(action[0][0])
    #                 self.action_input(action[0][1:])

    #             if(action == "d"):
    #                 Player.draw_devCard(self.board)
    #                 self.point += 0.1

    #                 a = 0
    #             elif(action == "u"):
    #                 Player.play_devCard(Player)
    #                 a = 0
    #             elif(action == "R"):
    #                 if(road_F == True):
    #                     if(Player.resources['BRICK'] > 0 and Player.resources['WOOD'] > 0):
    #                         possibleRoads = self.board.get_potential_roads(
    #                             self, Player)
    #                         if(possibleRoads[road_position[0], road_position[1]] == True):
    #                             Player.build_road[road_position[0],
    #                                               road_position[1], self.board]
    #                             self.point += 0.5

    #                         road_F = False

    #             elif(action == "S"):
    #                 if(build_F == True):
    #                     if((Player.resources['BRICK'] > 0 and Player.resources['WOOD'] > 0 and Player.resources['SHEEP'] > 0 and Player.resources['WHEAT'] > 0)):
    #                         possibleSettlements = self.board.get_potential_settlements(
    #                             self, Player)
    #                         if(possibleSettlements[build_position] == True):
    #                             Player.build_settlement[build_position,
    #                                                     self.board]
    #                             self.point += 2
    #                         build_F = False
    #                 a = 0
    #             elif(action == "C"):
    #                 if(build_F == True):
    #                     if(Player.resources['WHEAT'] >= 2 and Player.resources['ORE'] >= 3):
    #                         possibleCities = self.board.get_potential_cities(
    #                             self, Player)
    #                         if(possibleCities[build_position]):
    #                             Player.build_city[build_position, self.board]
    #                             self.point += 3
    #                         build_F = False
    #                 a = 0
    #             elif(action == "p"):
    #                 self.change = True
    #                 self.dicerolled = False
    #                 a = 0
    #             elif(action == "t"):
    #                 for r1, r1_amount in Player.resources.items():
    #                     # heuristic to trade if a player has more than 5 of a particular resource（プレイヤーが特定のリソースを5つ以上持っている場合のヒューリスティックトレード）
    #                     if(r1_amount >= 6):
    #                         for r2, r2_amount in Player.resources.items():
    #                             if(r2_amount < 1):
    #                                 self.trade_with_bank(r1, r2)
    #                                 break
    #             elif(self.int_check(action)):
    #                 build_position = self.board.vertex_index_to_pixel_dict[int(
    #                     action)]
    #                 build_F = True
    #         # elif(self.tuple_check(action)):
    #         #     road_position = (
    #         #         self.board.vertex_index_to_pixel_dict[action[0]], self.board.vertex_index_to_pixel_dict[action[1]])
    #         #     road_F = True
    #         #     tuple_F = True
    #     else:
    #         if(self.tuple_check(action[0])):
    #             road_position = (
    #                 self.board.vertex_index_to_pixel_dict[action[0][0]], self.board.vertex_index_to_pixel_dict[action[0][1]])
    #             road_F = True
    #             #self.action_input(action[0], Player)
    #             self.action_input(action[1:], Player)
    #         else:
    #             self.action_input(action[0], Player)
    #             self.action_input(action[1:], Player)

    # def action_input(self, action, Player):

    #     self.point = 0

    #     self.count += 1

    #    #print(f"action: {action}")

    #     # if(self.count > 100):
    #     #     exit()
    #     # print(f"action:{action}")
    #     if(self.int_check(action[0])):
    #         self.build_position = self.board.vertex_index_to_pixel_dict[int(
    #             action[0])]
    #         self.build_F = True
    #         self.action_input(action[1:], Player)

    #     elif(self.tuple_check(action[0])):
    #         self.road_position = (
    #             self.board.vertex_index_to_pixel_dict[action[0][0]], self.board.vertex_index_to_pixel_dict[action[0][1]])
    #         self.road_F = True
    #         self.action_input(action[1:], Player)

    #     elif(len(action[0]) == 1):
    #         # self.sample(action)
    #         # print(action)
    #         # exit()
    #         if(action[0] == "d"):
    #             Player.draw_devCard(self.board)

    #             #self.point += 0.1
    #             a = 0
    #         elif(action[0] == "u"):
    #             Player.play_devCard(Player)
    #             a = 0
    #         elif(action[0] == "R"):
    #             if(self.road_F == True):
    #                 # print("roadあり")
    #                 if(Player.resources['BRICK'] > 0 and Player.resources['WOOD'] > 0):

    #                     possibleRoads = self.board.get_potential_roads(Player)
    #                     #print(f"possibleRoads: {possibleRoads}")
    #                     if((self.road_position[0], self.road_position[1]) in possibleRoads.keys()):
    #                         Player.build_road(self.road_position[0],
    #                                           self.road_position[1], self.board)
    #                         self.point += 10
    #                         # print("road")
    #                     # else:
    #                     #     print("場所無し")
    #                     self.road_F = False

    #                 # else:
    #                 #     print("素材無し")

    #         elif(action[0] == "S"):
    #             if(self.build_F == True):
    #                 if((Player.resources['BRICK'] > 0 and Player.resources['WOOD'] > 0 and Player.resources['SHEEP'] > 0 and Player.resources['WHEAT'] > 0)):
    #                     possibleSettlements = self.board.get_potential_settlements(
    #                         Player)
    #                     #print(f"possibleSettlements: {possibleSettlements}")
    #                     if(self.build_position in possibleSettlements.keys()):
    #                         Player.build_settlement(self.build_position,
    #                                                 self.board)
    #                         self.point += 25
    #                         # print("settlement")
    #                     self.build_F = False
    #             a = 0
    #         elif(action[0] == "C"):
    #             if(self.build_F == True):
    #                 if(Player.resources['WHEAT'] >= 2 and Player.resources['ORE'] >= 3):
    #                     possibleCities = self.board.get_potential_cities(
    #                         Player)
    #                     #print(f"possibleCities: {possibleCities}")
    #                     if(self.build_position in possibleCities.keys()):
    #                         Player.build_city(self.build_position, self.board)
    #                         self.point += 35
    #                         # print("City")
    #                     self.build_F = False
    #                     # print("City")
    #             a = 0
    #         elif(action[0] == "p"):
    #             self.change = True
    #             self.dicerolled = False
    #             #self.point = 10
    #             a = 0
    #         elif(action[0] == "t"):
    #             for r1, r1_amount in Player.resources.items():
    #                 # heuristic to trade if a player has more than 5 of a particular resource（プレイヤーが特定のリソースを5つ以上持っている場合のヒューリスティックトレード）
    #                 if(r1_amount >= 6):
    #                     for r2, r2_amount in Player.resources.items():
    #                         if(r2_amount < 1):
    #                             self.trade_with_bank(r1, r2)
    #                             break

    #     else:
    #         self.action_input(action[0][0], Player)
    #         self.action_input(action[0][1:], Player)

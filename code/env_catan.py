
import gym
import numpy as np
from gym import spaces
from board import *
from player import *
from board import *
from gameView import *
from player import *
from heuristicAIPlayer import *
from myAI import *
import queue
import numpy as np
import sys
import pygame
import matplotlib.pyplot as plt


class Env_Catan(gym.Env):
    def __init__(self, board):
        print("Initializing Settlers of Catan with only AI Players...")
        self.board = catanBoard()

        # Game State variables(ゲームステート変数)
        self.gameOver = False
        self.maxPoints = 10
        self.numPlayers = 4
        self.team_V = False

        # self.myAI=myAI("player1")
        # self.

        self.change = False

        # Dictionary to keep track of dice statistics（サイコロの統計情報を記録する辞書）
        self.diceStats = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0,
                          7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
        self.diceStats_list = []

        # Initialize blank player queue and initial set up of roads + settlements（プレイヤーキューを空白にし、道路と集落を初期設定する）
        self.playerQueue = queue.Queue(self.numPlayers)
        self.gameSetup = True  # Boolean to take care of setup phase（ブール値でセットアップ段階を管理）

        # Initialize boardview object（ボードビューオブジェクトの初期化）
        self.boardView = catanGameView(self.board, self)

        # Functiont to go through initial set up（初期セットアップを行うための関数）
        self.build_initial_settlements()
        # self.playCatan()

        # Plot diceStats histogram（diceStatsヒストグラムのプロット）
        plt.hist(self.diceStats_list, bins=11)
        plt.show()

        self.ACTION_MAP = np.array(
            ["road", "settlement", "city", "dev", "trade", "pass"])

        self.isAI = True
        self.setupResources = []  # List to keep track of setup resources（セットアップリソースを記録するためのリスト）
        # Initialize resources with just correct number needed for set up（セットアップに必要な数だけリソースを初期化する）
        # Dictionary that keeps track of resource amounts（リソース量を把握する辞書）
        self.resources = {'ORE': 0, 'BRICK': 4,
                          'WHEAT': 2, 'WOOD': 4, 'SHEEP': 2}
        #print("Added new AI Player:", self.name)

        # # Build random settlement（ランダムな集落を作る）
        # possibleVertices = board.get_setup_settlements(self)

        # # Simple heuristic for choosing initial spot（初期位置の選択に関するシンプルなヒューリスティック）
        # diceRoll_expectation = {2: 1, 3: 2, 4: 3, 5: 4,
        #                         6: 5, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1, None: 0}
        # vertexValues = []

        # # Get the adjacent hexes for each hex（各ヘクスの隣接ヘクスを取得）
        # for v in possibleVertices.keys():
        #     vertexNumValue = 0
        #     resourcesAtVertex = []
        #     # For each adjacent hex get its value and overall resource diversity for that vertex（隣接する各ヘックスについて、その値とその頂点の全体的なリソース多様性を取得します）
        #     for adjacentHex in board.boardGraph[v].adjacentHexList:
        #         resourceType = board.hexTileDict[adjacentHex].resource.type
        #         if(resourceType not in resourcesAtVertex):
        #             resourcesAtVertex.append(resourceType)
        #         numValue = board.hexTileDict[adjacentHex].resource.num
        #         # Add to total value of this vertex（この頂点の合計値に加算する）
        #         vertexNumValue += diceRoll_expectation[numValue]

        #     # basic heuristic for resource diversity（資源多様性のための基本的なヒューリスティック）
        #     vertexNumValue += len(resourcesAtVertex)*2
        #     for r in resourcesAtVertex:
        #         if(r != 'DESERT' and r not in self.setupResources):
        #             vertexNumValue += 2.5  # Every new resource gets a bonus（新しいリソースにはボーナスがつく）

        #     vertexValues.append(vertexNumValue)

        # vertexToBuild_index = vertexValues.index(max(vertexValues))
        # vertexToBuild = list(possibleVertices.keys())[vertexToBuild_index]

        # # Add to setup resources（セットアップリソースに追加）
        # for adjacentHex in board.boardGraph[vertexToBuild].adjacentHexList:
        #     resourceType = board.hexTileDict[adjacentHex].resource.type
        #     if(resourceType not in self.setupResources and resourceType != 'DESERT'):
        #         self.setupResources.append(resourceType)

        # self.build_settlement(vertexToBuild, board)

        # # Build random road（ランダムな道路を作る）
        # possibleRoads = board.get_setup_roads(self)
        # randomEdge = np.random.randint(0, len(possibleRoads.keys()))
        # self.build_road(list(possibleRoads.keys())[randomEdge][0], list(
        #     possibleRoads.keys())[randomEdge][1], board)

        # アクション数定義
        ACTION_NUM = len(self.ACTION_MAP)
        self.action_space = gym.spaces.Discrete(ACTION_NUM)
        self.observation_space = gym.spaces.Discrete(53)

    def step(self, action_index: int, board):
        action = self.ACTION_MAP[action_index]
        done = False

        for currPlayer in self.playerQueue.queue:
            diceNum = self.rollDice()
            diceRolled = True
            self.update_playerResources(diceNum, currPlayer)
            self.diceStats[diceNum] += 1
            self.diceStats_list.append(diceNum)

            currPlayer.updateDevCards()
            currPlayer.devCardPlayedThisTurn = False

            if(currPlayer == 'player1'):
                while(self.change == False):
                    if(action == "road"):
                        # a = a
                        if(self.resources['BRICK'] > 0 and self.resources['WOOD'] > 0):
                            possibleRoads = board.get_setup_roads(self)
                            randomEdge = np.random.randint(
                                0, len(possibleRoads.keys()))
                            self.build_road(list(possibleRoads.keys())[randomEdge][0], list(
                                possibleRoads.keys())[randomEdge][1], board)
                    elif(action == "settlement"):
                        #a = a
                        # vCoord = 0
                        # self.build_settlement(vCoord, board)
                        possibleVertices = board.get_potential_settlements(
                            self)
                        if(possibleVertices != {} and (self.resources['BRICK'] > 0 and self.resources['WOOD'] > 0 and self.resources['SHEEP'] > 0 and self.resources['WHEAT'] > 0)):
                            randomVertex = np.random.randint(
                                0, len(possibleVertices.keys()))
                            self.build_settlement(list(possibleVertices.keys())[
                                randomVertex], board)

                    elif(action == "city"):
                        #a = a
                        # vCoord = 0
                        # self.build_city(vCoord, board)
                        possibleVertices = board.get_potential_cities(self)
                        if(possibleVertices != {} and (self.resources['WHEAT'] >= 2 and self.resources['ORE'] >= 3)):
                            randomVertex = np.random.randint(
                                0, len(possibleVertices.keys()))
                            self.build_city(list(possibleVertices.keys())[
                                            randomVertex], board)

                    elif(action == "dev"):
                        #a = a
                        self.draw_devCard(board)
                    elif(action == "trade"):
                        #a = a
                        for r1, r1_amount in self.resources.items():
                            # heuristic to trade if a player has more than 5 of a particular resource（プレイヤーが特定のリソースを5つ以上持っている場合のヒューリスティックトレード）
                            if(r1_amount >= 6):
                                for r2, r2_amount in self.resources.items():
                                    if(r2_amount < 1):
                                        self.trade_with_bank(r1, r2)
                                        break
                    elif(action == "pass"):
                        #a = a
                        self.change = True
                self.change = False
            else:
                currPlayer.move(self.board)
            self.check_longest_road(currPlayer)
            if currPlayer.victoryPoints >= self.maxPoints:
                Over_Flag = True
                p_v = currPlayer.name
                done = True

        return observation, reward, done, {}

    def reset(self):

        # Game State variables(ゲームステート変数)
        self.gameOver = False
        self.maxPoints = 10
        self.numPlayers = 0
        self.team_V = False
        self.change = False

        # Dictionary to keep track of dice statistics（サイコロの統計情報を記録する辞書）
        self.diceStats = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0,
                          7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
        self.diceStats_list = []

        # Only accept 3 and 4 player games（3人および4人用のゲームのみをサポート）
        while(self.numPlayers not in [3, 4]):
            try:
                self.numPlayers = int(
                    input("Enter Number of Players (3 or 4):"))
            except:
                print("Please input a valid number")

        print("Initializing game with {} players...".format(self.numPlayers))
        print("Note that Player 1 goes first, Player 2 second and so forth.")

        # Initialize blank player queue and initial set up of roads + settlements（プレイヤーキューを空白にし、道路と集落を初期設定する）
        self.playerQueue = queue.Queue(self.numPlayers)
        self.gameSetup = True  # Boolean to take care of setup phase（ブール値でセットアップ段階を管理）

        # Initialize boardview object（ボードビューオブジェクトの初期化）
        self.boardView = catanGameView(self.board, self)

        # Functiont to go through initial set up（初期セットアップを行うための関数）
        self.build_initial_settlements()
        # self.playCatan()

        # Plot diceStats histogram（diceStatsヒストグラムのプロット）
        plt.hist(self.diceStats_list, bins=11)
        plt.show()

        self.ACTION_MAP = np.array(
            ["road", "settlement", "city", "dev", "trade", "pass"])

        self.isAI = True
        self.setupResources = []  # List to keep track of setup resources（セットアップリソースを記録するためのリスト）
        # Initialize resources with just correct number needed for set up（セットアップに必要な数だけリソースを初期化する）
        # Dictionary that keeps track of resource amounts（リソース量を把握する辞書）
        self.resources = {'ORE': 0, 'BRICK': 4,
                          'WHEAT': 2, 'WOOD': 4, 'SHEEP': 2}
        print("Added new AI Player:", self.name)

        return None

    def OBSERVATION_SPACE(self):
        # 各タイルの資源（資源,マスの値）
        OBS_SPACE = spaces.Dict({
            # 各タイルの資源（資源,マスの値）
            "board_resources": spaces.Box(
                low=np.array(1, 2),
                high=np.array(5, 12),
                dtype=np.uint8
            ),
            "robber_resources": spaces.Box(
                low=2,
                high=12,
                dtype=np.uint8
            ),
            # 所持している発展カード（種類,枚数）
            "board_resources": spaces.Box(
                low=np.array(1, 0),
                high=np.array(2, 20),  # 最大枚数は後で調整
                dtype=np.uint8
            ),
            # 所持している資源カード（種類,枚数）
            "board_resources": spaces.Box(
                low=np.array(1, 0),
                high=np.array(5, 20),  # 最大枚数は後で調整
                dtype=np.uint8
            ),
            # 開拓地のある場所
            "settlement_resources": spaces.Box(
                low=1,
                high=54,  # 最大枚数は後で調整
                dtype=np.uint8
            ),
            # 都市のある場所
            "settlement_resources": spaces.Box(
                low=1,
                high=54,  # 最大枚数は後で調整
                dtype=np.uint8
            ),
            # 道のある場所（頂点1,頂点2）
            "settlement_resources": spaces.Box(
                low=np.array(1, 1),
                high=np.array(54, 54),  # 最大枚数は後で調整
                dtype=np.uint8
            ),
            # "PieceID1": spaces.Box(low=0, high=6, dtype=np.uint8),

        })

        return flatten_space(OBS_SPACE)

    def build_initial_settlements(self):
        # Initialize new players with names and colors（名前と色で新しいプレイヤーを初期化する関数）
        playerColors = ['black', 'darkslateblue', 'magenta4', 'orange1']

        newPlayer = myAI('player1', 'black')
        newPlayer.updateAI()
        self.playerQueue.put(newPlayer)

        for i in range(3):
            #playerNameInput = input("Enter AI Player {} name: ".format(i+1))
            newPlayer = heuristicAIPlayer(f"player{i+2}", playerColors[i+1])
            newPlayer.updateAI()
            self.playerQueue.put(newPlayer)

        playerList = list(self.playerQueue.queue)

        # Build Settlements and roads of each player forwards（各プレイヤーの集落や道路を順次構築していく）
        for player_i in playerList:
            player_i.initial_setup(self.board)
            pygame.event.pump()
            self.boardView.displayGameScreen()
            pygame.time.delay(1000)

        # Build Settlements and roads of each player reverse（各プレイヤーの集落と道路を逆向きに作る）
        playerList.reverse()
        for player_i in playerList:
            player_i.initial_setup(self.board)
            pygame.event.pump()
            self.boardView.displayGameScreen()
            pygame.time.delay(1000)

            print("Player {} starts with {} resources".format(
                player_i.name, len(player_i.setupResources)))

            # Initial resource generation（初期資源生成）
            # check each adjacent hex to latest settlement（最新の集落に隣接するヘクスをチェック）
            for adjacentHex in self.board.boardGraph[player_i.buildGraph['SETTLEMENTS'][-1]].adjacentHexList:
                resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                if(resourceGenerated != 'DESERT'):
                    player_i.resources[resourceGenerated] += 1
                    print("{} collects 1 {} from Settlement".format(
                        player_i.name, resourceGenerated))

        pygame.time.delay(5000)
        self.gameSetup = False

    # Function to roll dice （サイコロを振る機能）
    def rollDice(self):
        dice_1 = np.random.randint(1, 7)
        dice_2 = np.random.randint(1, 7)
        diceRoll = dice_1 + dice_2
        print("Dice Roll = ", diceRoll, "{", dice_1, dice_2, "}")

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
                            print("{} collects 1 {} from Settlement".format(
                                player_i.name, resourceGenerated))

                # Check each City the player has（各プレイヤーが持つ都市をチェック）
                for cityCoord in player_i.buildGraph['CITIES']:
                    # check each adjacent hex to a settlement
                    for adjacentHex in self.board.boardGraph[cityCoord].adjacentHexList:
                        # This player gets a resource if hex is adjacent and no robber
                        if(adjacentHex in hexResourcesRolled and self.board.hexTileDict[adjacentHex].robber == False):
                            resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                            player_i.resources[resourceGenerated] += 2
                            print("{} collects 2 {} from City".format(
                                player_i.name, resourceGenerated))

                print("Player:{}, Resources:{}, Points: {}".format(
                    player_i.name, player_i.resources, player_i.victoryPoints))
                #print('Dev Cards:{}'.format(player_i.devCards))
                #print("RoadsLeft:{}, SettlementsLeft:{}, CitiesLeft:{}".format(player_i.roadsLeft, player_i.settlementsLeft, player_i.citiesLeft))
                print('MaxRoadLength:{}, Longest Road:{}\n'.format(
                    player_i.maxRoadLength, player_i.longestRoadFlag))

        else:
            print("AI using heuristic robber...")
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

                print("Player {} takes Longest Road {}".format(
                    player_i.name, prevPlayer))

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

                print("Player {} takes Largest Army {}".format(
                    player_i.name, prevPlayer))

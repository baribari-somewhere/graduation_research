# Settlers of Catan
# Gameplay class with pygame with AI players

from board import *
from gameView import *
from player import *
from heuristicAIPlayer import *
import queue
import numpy as np
import sys
import pygame
import matplotlib.pyplot as plt

# Class to implement an only AI（唯一のAIを実装するクラス）


class catanAIGame():
    # Create new gameboard
    def __init__(self):
        print("Initializing Settlers of Catan with only AI Players...")
        self.board = catanBoard()

        # Game State variables(ゲームステート変数)
        self.gameOver = False
        self.maxPoints = 10
        self.numPlayers = 0
        self.team_V = False

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
        self.playCatan()

        # Plot diceStats histogram（diceStatsヒストグラムのプロット）
        plt.hist(self.diceStats_list, bins=11)
        plt.show()

        return None

    # Function to initialize players + build initial settlements for players（プレイヤーの初期化＋プレイヤーのための初期集落を構築する関数）
    def build_initial_settlements(self):
        # Initialize new players with names and colors（名前と色で新しいプレイヤーを初期化する関数）
        playerColors = ['black', 'darkslateblue', 'magenta4', 'orange1']
        for i in range(self.numPlayers):
            playerNameInput = input("Enter AI Player {} name: ".format(i+1))
            newPlayer = heuristicAIPlayer(playerNameInput, playerColors[i])
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

    # Function that runs the main game loop with all players and pieces（すべてのプレーヤーと駒でメインゲームループを実行する関数）

    def playCatan(self):
        # self.board.displayBoard() #Display updated board（更新された碁盤を表示する）
        numTurns = 0
        Over_Flag = False
        while (self.gameOver == False):
            # Loop for each player's turn -> iterate through the player queue（各プレイヤーの手番をループする -> プレイヤーキューを繰り返し処理する）
            for currPlayer in self.playerQueue.queue:
                if(not Over_Flag):
                    numTurns += 1
                    print(
                        "---------------------------------------------------------------------------")
                    print("Current Player:", currPlayer.name)

                    turnOver = False  # boolean to keep track of turn（手番を記録するためのブーリアン）
                    diceRolled = False  # Boolean for dice roll status（サイコロの出目の状態を表すブール値）

                    # Update Player's dev card stack with dev cards drawn in previous turn and reset devCardPlayedThisTurn（ プレイヤーの開発カードスタックを前のターンに引いた開発カードで更新し、devCardPlayedThisTurnをリセットする）
                    currPlayer.updateDevCards()
                    currPlayer.devCardPlayedThisTurn = False

                    while(turnOver == False):

                        # TO-DO: Add logic for AI Player to move（AIプレイヤーの移動ロジックの追加）
                        # TO-DO: Add option of AI Player playing a dev card prior to dice roll（ダイスロールの前にAIプレイヤーが開発カードをプレイするオプションの追加）

                        # Roll Dice and update player resources and dice stats（ダイスを振ってプレイヤーのリソースとダイスのステータスを更新）
                        pygame.event.pump()
                        diceNum = self.rollDice()
                        diceRolled = True
                        self.update_playerResources(diceNum, currPlayer)
                        self.diceStats[diceNum] += 1
                        self.diceStats_list.append(diceNum)

                        # AI Player makes all its moves（AIプレイヤーは全ての移動を行う）
                        currPlayer.move(self.board)
                        # Check if AI player gets longest road and update Victory points（AIプレイヤーが最長路を獲得したかどうかを確認し、勝利点を更新する）
                        self.check_longest_road(currPlayer)
                        print("Player:{}, Resources:{}, Points: {}".format(
                            currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))

                        # Update back to original gamescreen（元のゲーム画面へのアップデート）
                        self.boardView.displayGameScreen()
                        pygame.time.delay(300)
                        turnOver = True

                    # Check if game is over（ゲームオーバーの確認）
                    wait_count = 0
                    #Over_Flag = False
                    if currPlayer.victoryPoints >= self.maxPoints:
                        Over_Flag = True
                        p_v = currPlayer.name
                        # self.gameOver = True
                        # self.turnOver = True
                        # print("====================================================")
                        # print("PLAYER {} WINS IN {} TURNS!".format(
                        #     currPlayer.name, int(numTurns/4)))
                        # print(self.diceStats)
                        # print("Exiting game in 10 seconds...")
                        # pygame.time.delay(10000)
                        # break
                if(Over_Flag):
                    wait_count += 1
                if(wait_count == 3):
                    p_team = currPlayer.name
                    self.gameOver = True
                    self.turnOver = True
                    print("====================================================")
                    print("PLAYER {} & PLAYER {} WINS IN {} TURNS!".format(
                        p_v, p_team, int(numTurns/4)))
                    print(self.diceStats)
                    print("Exiting game in 10 seconds...")
                    pygame.time.delay(10000)
                    break

                if(self.gameOver):
                    startTime = pygame.time.get_ticks()
                    runTime = 0
                    while(runTime < 5000):  # 5 second delay prior to quitting（終了前に5秒間の遅延）
                        runTime = pygame.time.get_ticks() - startTime

                    break

    # def playCatan(self):
    #     # self.board.displayBoard() #Display updated board（更新された碁盤を表示する）
    #     numTurns = 0
    #     Over_Flag = False
    #     while (self.gameOver == False):
    #         # Loop for each player's turn -> iterate through the player queue（各プレイヤーの手番をループする -> プレイヤーキューを繰り返し処理する）
    #         for currPlayer in self.playerQueue.queue:
    #             if(not Over_Flag):
    #             numTurns += 1
    #             print(
    #                 "---------------------------------------------------------------------------")
    #             print("Current Player:", currPlayer.name)

    #             turnOver = False  # boolean to keep track of turn（手番を記録するためのブーリアン）
    #             diceRolled = False  # Boolean for dice roll status（サイコロの出目の状態を表すブール値）

    #             # Update Player's dev card stack with dev cards drawn in previous turn and reset devCardPlayedThisTurn（ プレイヤーの開発カードスタックを前のターンに引いた開発カードで更新し、devCardPlayedThisTurnをリセットする）
    #             currPlayer.updateDevCards()
    #             currPlayer.devCardPlayedThisTurn = False

    #             while(turnOver == False):

    #                 # TO-DO: Add logic for AI Player to move（AIプレイヤーの移動ロジックの追加）
    #                 # TO-DO: Add option of AI Player playing a dev card prior to dice roll（ダイスロールの前にAIプレイヤーが開発カードをプレイするオプションの追加）

    #                 # Roll Dice and update player resources and dice stats（ダイスを振ってプレイヤーのリソースとダイスのステータスを更新）
    #                 pygame.event.pump()
    #                 diceNum = self.rollDice()
    #                 diceRolled = True
    #                 self.update_playerResources(diceNum, currPlayer)
    #                 self.diceStats[diceNum] += 1
    #                 self.diceStats_list.append(diceNum)

    #                 # AI Player makes all its moves（AIプレイヤーは全ての移動を行う）
    #                 currPlayer.move(self.board)
    #                 # Check if AI player gets longest road and update Victory points（AIプレイヤーが最長路を獲得したかどうかを確認し、勝利点を更新する）
    #                 self.check_longest_road(currPlayer)
    #                 print("Player:{}, Resources:{}, Points: {}".format(
    #                     currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))

    #                 # Update back to original gamescreen（元のゲーム画面へのアップデート）
    #                 self.boardView.displayGameScreen()
    #                 pygame.time.delay(300)
    #                 turnOver = True

    #                 # Check if game is over（ゲームオーバーの確認）
    #                 wait_count = 0
    #                 #Over_Flag = False
    #                 if currPlayer.victoryPoints >= self.maxPoints:
    #                     self.gameOver = True
    #                     self.turnOver = True
    #                     print("====================================================")
    #                     print("PLAYER {} WINS IN {} TURNS!".format(
    #                         currPlayer.name, int(numTurns/4)))
    #                     print(self.diceStats)
    #                     print("Exiting game in 10 seconds...")
    #                     pygame.time.delay(10000)
    #                     break

    #             if(self.gameOver):
    #                 startTime = pygame.time.get_ticks()
    #                 runTime = 0
    #                 while(runTime < 5000):  # 5 second delay prior to quitting（終了前に5秒間の遅延）
    #                     runTime = pygame.time.get_ticks() - startTime

    #                 break

    # def team_win():

        # Initialize new game and run（）（新しいゲームの初期化および実行）
newGame_AI = catanAIGame()

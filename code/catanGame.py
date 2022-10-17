# Settlers of Catan
# Gameplay class with pygame

from board import *
from gameView import *
from player import *
from heuristicAIPlayer import *
import queue
import numpy as np
import sys
import pygame

# Catan gameplay class definition（カタンゲームプレイクラス定義）


class catanGame():
    # Create new gameboard（新しいゲームボードを作成する）
    def __init__(self):
        print("Initializing Settlers of Catan Board...")
        self.board = catanBoard()

        # Game State variables（ゲームステート変数）
        self.gameOver = False
        self.maxPoints = 8
        self.numPlayers = 0

        # Only accept 3 and 4 player games（3人用と4人用のゲームのみ受け付けます）
        while(self.numPlayers not in [3, 4]):
            try:
                self.numPlayers = int(
                    input("Enter Number of Players (3 or 4):"))
            except:
                print("Please input a valid number")

        print("Initializing game with {} players...".format(self.numPlayers))
        print("Note that Player 1 goes first, Player 2 second and so forth.")

        # Initialize blank player queue and initial set up of roads + settlements（空白のプレイヤーキューの初期化と道路＋集落の初期設定）
        self.playerQueue = queue.Queue(self.numPlayers)
        self.gameSetup = True  # Boolean to take care of setup phase（ブール値でセットアップ段階を処理）

        # Initialize boardview object（boardviewオブジェクトの初期化）
        self.boardView = catanGameView(self.board, self)

        # Run functions to view board and vertex graph（ボードと頂点グラフを表示するための関数を実行する）
        # self.board.printGraph()

        # Functiont to go through initial set up（初期セットアップを行うための関数）
        self.build_initial_settlements()

        # Display initial board
        self.boardView.displayGameScreen()

    # Function to initialize players + build initial settlements for players（プレイヤーの初期化＋プレイヤーの初期集落を構築する関数）
    def build_initial_settlements(self):
        # Initialize new players with names and colors（新しいプレイヤーに名前と色を付けて初期化する機能）
        playerColors = ['black', 'darkslateblue', 'magenta4', 'orange1']
        for i in range(self.numPlayers - 1):
            playerNameInput = input("Enter Player {} name: ".format(i+1))
            newPlayer = player(playerNameInput, playerColors[i])
            self.playerQueue.put(newPlayer)

        # Add the AI Player last（AIプレーヤーを最後に追加する）
        test_AI_player = heuristicAIPlayer(
            'Random-Greedy-AI', playerColors[i+1])
        test_AI_player.updateAI()
        self.playerQueue.put(test_AI_player)

        playerList = list(self.playerQueue.queue)

        # display the initial gameScreen（初期状態のゲーム画面を表示する）
        self.boardView.displayGameScreen()
        print("Displaying Initial GAMESCREEN!")

        # Build Settlements and roads of each player forwards（各プレイヤーの入植地や道路を建設する）
        for player_i in playerList:
            if(player_i.isAI):
                player_i.initial_setup(self.board)

            else:
                self.build(player_i, 'SETTLE')
                self.boardView.displayGameScreen()

                self.build(player_i, 'ROAD')
                self.boardView.displayGameScreen()

        # Build Settlements and roads of each player reverse（各プレイヤーの集落や道路を逆向きに建設する）
        playerList.reverse()
        for player_i in playerList:
            if(player_i.isAI):
                player_i.initial_setup(self.board)
                self.boardView.displayGameScreen()

            else:
                self.build(player_i, 'SETTLE')
                self.boardView.displayGameScreen()

                self.build(player_i, 'ROAD')
                self.boardView.displayGameScreen()

            # Initial resource generation（初期リソース生成）
            # check each adjacent hex to latest settlement（最新の決済に隣接する各ヘックスをチェックする）
            for adjacentHex in self.board.boardGraph[player_i.buildGraph['SETTLEMENTS'][-1]].adjacentHexList:
                resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                if(resourceGenerated != 'DESERT'):
                    player_i.resources[resourceGenerated] += 1
                    print("{} collects 1 {} from Settlement".format(
                        player_i.name, resourceGenerated))

        self.gameSetup = False

        return

    # Generic function to handle all building in the game - interface with gameView（ゲーム内のすべての建物を処理する汎用関数 - gameViewとのインタフェース）
    def build(self, player, build_flag):
        if(build_flag == 'ROAD'):  # Show screen with potential roads（候補となる道路を表示する画面）
            if(self.gameSetup):
                potentialRoadDict = self.board.get_setup_roads(player)
            else:
                potentialRoadDict = self.board.get_potential_roads(player)

            roadToBuild = self.boardView.buildRoad_display(
                player, potentialRoadDict)
            if(roadToBuild != None):
                player.build_road(roadToBuild[0], roadToBuild[1], self.board)

        if(build_flag == 'SETTLE'):  # Show screen with potential settlements（決済候補の画面を表示する）
            if(self.gameSetup):
                potentialVertexDict = self.board.get_setup_settlements(player)
            else:
                potentialVertexDict = self.board.get_potential_settlements(
                    player)

            vertexSettlement = self.boardView.buildSettlement_display(
                player, potentialVertexDict)
            if(vertexSettlement != None):
                player.build_settlement(vertexSettlement, self.board)

        if(build_flag == 'CITY'):
            potentialCityVertexDict = self.board.get_potential_cities(player)
            vertexCity = self.boardView.buildSettlement_display(
                player, potentialCityVertexDict)
            if(vertexCity != None):
                player.build_city(vertexCity, self.board)

    # Wrapper Function to handle robber functionality（Robber機能を扱うWrapper機能）
    def robber(self, player):
        potentialRobberDict = self.board.get_robber_spots()
        print("Move Robber!")

        hex_i, playerRobbed = self.boardView.moveRobber_display(
            player, potentialRobberDict)
        player.move_robber(hex_i, self.board, playerRobbed)

    # Function to roll dice （サイコロを振る機能）
    def rollDice(self):
        dice_1 = np.random.randint(1, 7)
        dice_2 = np.random.randint(1, 7)
        diceRoll = dice_1 + dice_2
        print("Dice Roll = ", diceRoll, "{", dice_1, dice_2, "}")

        self.boardView.displayDiceRoll(diceRoll)

        return diceRoll

    # Function to update resources for all players（全プレイヤーのリソースを更新する機能）
    def update_playerResources(self, diceRoll, currentPlayer):
        if(diceRoll != 7):  # Collect resources if not a 7（7でない場合は、リソースを収集する）
            # First get the hex or hexes corresponding to diceRoll（まず、diceRoll に対応するヘクスを取得します）
            hexResourcesRolled = self.board.getHexResourceRolled(diceRoll)
            #print('Resources rolled this turn:', hexResourcesRolled)

            # Check for each player（各プレイヤーのチェック）
            for player_i in list(self.playerQueue.queue):
                # Check each settlement the player has（プレイヤーが持っている各決済を確認する）
                for settlementCoord in player_i.buildGraph['SETTLEMENTS']:
                    # check each adjacent hex to a settlement
                    for adjacentHex in self.board.boardGraph[settlementCoord].adjacentHexList:
                        # This player gets a resource if hex is adjacent and no robber
                        if(adjacentHex in hexResourcesRolled and self.board.hexTileDict[adjacentHex].robber == False):
                            resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                            player_i.resources[resourceGenerated] += 1
                            print("{} collects 1 {} from Settlement".format(
                                player_i.name, resourceGenerated))

                # Check each City the player has
                for cityCoord in player_i.buildGraph['CITIES']:
                    # check each adjacent hex to a settlement（隣接する各ヘックスをチェックし、決済する）
                    for adjacentHex in self.board.boardGraph[cityCoord].adjacentHexList:
                        # This player gets a resource if hex is adjacent and no robber（このプレイヤーは、ヘクスが隣接し、強盗がいなければ資源を得る）
                        if(adjacentHex in hexResourcesRolled and self.board.hexTileDict[adjacentHex].robber == False):
                            resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                            player_i.resources[resourceGenerated] += 2
                            print("{} collects 2 {} from City".format(
                                player_i.name, resourceGenerated))

                print("Player:{}, Resources:{}, Points: {}".format(
                    player_i.name, player_i.resources, player_i.victoryPoints))
                #print('Dev Cards:{}'.format(player_i.devCards))
                #print("RoadsLeft:{}, SettlementsLeft:{}, CitiesLeft:{}".format(player_i.roadsLeft, player_i.settlementsLeft, player_i.citiesLeft))
                print('MaxRoadLength:{}, LongestRoad:{}\n'.format(
                    player_i.maxRoadLength, player_i.longestRoadFlag))

        # Logic for a 7 roll（7の出目のロジック）
        else:
            # Implement discarding cards（カードの廃棄を実装）
            # Check for each player（各プレイヤーのチェック）
            for player_i in list(self.playerQueue.queue):
                if(currentPlayer.isAI):
                    print("AI discarding resources...")
                    # TO-DO
                else:
                    # Player must discard resources（プレイヤーは資源を捨てなければならない）
                    player_i.discardResources()

            # Logic for robber（強盗のためのロジック）
            if(currentPlayer.isAI):
                print("AI using heuristic robber...")
                currentPlayer.heuristic_move_robber(self.board)
            else:
                self.robber(currentPlayer)
                # Update back to original gamescreen（アップデートで元のゲーム画面に戻す）
                self.boardView.displayGameScreen()

    # function to check if a player has the longest road - after building latest road（最新の道路を建設した後に、プレイヤーが最も長い道路を持っているかどうかをチェックする機能）
    def check_longest_road(self, player_i):
        if(player_i.maxRoadLength >= 5):  # Only eligible if road length is at least 5（道路の長さが5m以上の場合のみ対象）
            longestRoad = True
            for p in list(self.playerQueue.queue):
                # Check if any other players have a longer road（他のプレーヤーが長いロードを持っているかどうかを確認する）
                if(p.maxRoadLength >= player_i.maxRoadLength and p != player_i):
                    longestRoad = False

            # if player_i takes longest road and didn't already have longest road（player_i が最短距離の道路を利用し，かつ最短距離の道路を持っていなかった場合）
            if(longestRoad and player_i.longestRoadFlag == False):
                # Set previous players flag to false and give player_i the longest road points（前選手フラグをfalseに設定し、player_iに最長ロードポイントを与える）
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

    # function to check if a player has the largest army - after playing latest knight（最新の騎士をプレイした後、最大の軍隊を持っているかどうかをチェックする関数です）
    def check_largest_army(self, player_i):
        if(player_i.knightsPlayed >= 3):  # Only eligible if at least 3 knights are player（ナイトが3人以上いる場合のみ対象）
            largestArmy = True
            for p in list(self.playerQueue.queue):
                # Check if any other players have more knights played（他のプレイヤーがより多くのナイトをプレイしているかどうかを確認する）
                if(p.knightsPlayed >= player_i.knightsPlayed and p != player_i):
                    largestArmy = False

            # if player_i takes largest army and didn't already have it（player_iが最大の軍を持ち、まだ持っていなかった場合）
            if(largestArmy and player_i.largestArmyFlag == False):
                # Set previous players flag to false and give player_i the largest points（前選手フラグをfalseに設定し、player_iに最大ポイントを与える）
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
        # self.board.displayBoard() #Display updated board（アップデートされたボードを表示）

        while (self.gameOver == False):

            # Loop for each player's turn -> iterate through the player queue（各プレイヤーのターンのループ → プレイヤーキューを繰り返し処理する）
            for currPlayer in self.playerQueue.queue:

                print(
                    "---------------------------------------------------------------------------")
                print("Current Player:", currPlayer.name)

                turnOver = False  # boolean to keep track of turn（ターンを追跡するためのブール型）
                diceRolled = False  # Boolean for dice roll status（サイコロの出目の状態を表すブール値）

                # Update Player's dev card stack with dev cards drawn in previous turn and reset devCardPlayedThisTurn（プレイヤーの開発カードを前のターンに引いた開発カードで更新し、devCardPlayedThisTurnをリセットします）
                currPlayer.updateDevCards()
                currPlayer.devCardPlayedThisTurn = False

                while(turnOver == False):

                    # TO-DO: Add logic for AI Player to move（AI Playerが移動するロジックを追加）
                    # TO-DO: Add option of AI Player playing a dev card prior to dice roll（ダイスロールの前に、AIプレーヤーが開発カードをプレイするオプションを追加）
                    if(currPlayer.isAI):
                        # Roll Dice
                        diceNum = self.rollDice()
                        diceRolled = True
                        self.update_playerResources(diceNum, currPlayer)

                        # AI Player makes all its moves（AIプレーヤーが全ての動作を行う）
                        currPlayer.move(self.board)
                        # Check if AI player gets longest road/largest army and update Victory points（AIプレイヤーが最長の道路と最大の軍隊を獲得したかどうかを確認し、勝利点を更新する）
                        self.check_longest_road(currPlayer)
                        self.check_largest_army(currPlayer)
                        print("Player:{}, Resources:{}, Points: {}".format(
                            currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))

                        # Update back to original gamescreen（アップデートで元のゲーム画面に戻す）
                        self.boardView.displayGameScreen()
                        turnOver = True

                    else:  # Game loop for human players（人間用ゲームループ）
                        for e in pygame.event.get():  # Get player actions/in-game events（プレイヤーのアクションやゲーム内のイベントを取得）
                            # print(e)
                            if e.type == pygame.QUIT:
                                sys.exit(0)

                            # Check mouse click in rollDice（rollDiceでマウスクリックを確認する）
                            if(e.type == pygame.MOUSEBUTTONDOWN):
                                # Check if player rolled the dice（サイコロを振ったかどうか確認する）
                                if(self.boardView.rollDice_button.collidepoint(e.pos)):
                                    if(diceRolled == False):  # Only roll dice once（サイコロを1回だけ振る）
                                        diceNum = self.rollDice()
                                        diceRolled = True

                                        self.boardView.displayDiceRoll(diceNum)
                                        # Code to update player resources with diceNum（diceNumでプレイヤーリソースを更新するコード）
                                        self.update_playerResources(
                                            diceNum, currPlayer)

                                # Check if player wants to build road（プレイヤーが道路を作りたいかをチェックする）
                                if(self.boardView.buildRoad_button.collidepoint(e.pos)):
                                    # Code to check if road is legal and build（道路が合法かどうかをチェックし、建設するためのコード）
                                    # Can only build after rolling dice（サイコロを振った後でないと作れない）
                                    if(diceRolled == True):
                                        self.build(currPlayer, 'ROAD')
                                        # Update back to original gamescreen（アップデートで元のゲーム画面に戻す）
                                        self.boardView.displayGameScreen()

                                        # Check if player gets longest road and update Victory points（プレイヤーが最長路を獲得したかどうかを確認し、ビクトリーポイントを更新する）
                                        self.check_longest_road(currPlayer)
                                        # Show updated points and resources （更新されたポイントやリソースを表示する）
                                        print("Player:{}, Resources:{}, Points: {}".format(
                                            currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))

                                # Check if player wants to build settlement（プレイヤーが集落を作りたいかを確認する）
                                if(self.boardView.buildSettlement_button.collidepoint(e.pos)):
                                    # Can only build settlement after rolling dice（サイコロを振ってからでないと集落を作れない）
                                    if(diceRolled == True):
                                        self.build(currPlayer, 'SETTLE')
                                        # Update back to original gamescreen（アップデートで元のゲーム画面に戻す）
                                        self.boardView.displayGameScreen()
                                        # Show updated points and resources  （更新されたポイントやリソースを表示する ）
                                        print("Player:{}, Resources:{}, Points: {}".format(
                                            currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))

                                # Check if player wants to build city（プレイヤーが都市を建設したいかどうかをチェックする）
                                if(self.boardView.buildCity_button.collidepoint(e.pos)):
                                    # Can only build city after rolling dice（サイコロを振ってからでないと街を作れない）
                                    if(diceRolled == True):
                                        self.build(currPlayer, 'CITY')
                                        # Update back to original gamescreen（アップデートで元のゲーム画面に戻す）
                                        self.boardView.displayGameScreen()
                                        # Show updated points and resources（更新されたポイントやリソースを表示する）
                                        print("Player:{}, Resources:{}, Points: {}".format(
                                            currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))

                                # Check if player wants to draw a development card（プレイヤーが開発カードを引きたいかどうか確認する）
                                if(self.boardView.devCard_button.collidepoint(e.pos)):
                                    # Can only draw devCard after rolling dice（サイコロを振ってからデブカードを引くことができる）
                                    if(diceRolled == True):
                                        currPlayer.draw_devCard(self.board)
                                        # Show updated points and resources（更新されたポイントやリソースを表示する）
                                        print("Player:{}, Resources:{}, Points: {}".format(
                                            currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))
                                        print('Available Dev Cards:',
                                              currPlayer.devCards)

                                # Check if player wants to play a development card - can play devCard whenever after rolling dice（開発カードを出したいかどうか確認する - サイコロを振ったらいつでも開発カードを出すことができる）
                                if(self.boardView.playDevCard_button.collidepoint(e.pos)):
                                    currPlayer.play_devCard(self)
                                    # Update back to original gamescreen（アップデートで元のゲーム画面に戻す）
                                    self.boardView.displayGameScreen()

                                    # Check for Largest Army and longest road（最大陸軍と最長道路をチェック）
                                    self.check_largest_army(currPlayer)
                                    self.check_longest_road(currPlayer)
                                    # Show updated points and resources（更新されたポイントやリソースを表示する）
                                    print("Player:{}, Resources:{}, Points: {}".format(
                                        currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))
                                    print('Available Dev Cards:',
                                          currPlayer.devCards)

                                # Check if player wants to trade with the bank（プレイヤーが銀行との取引を希望しているかどうかをチェックする）
                                if(self.boardView.tradeBank_button.collidepoint(e.pos)):
                                    currPlayer.initiate_trade(self, 'BANK')
                                    # Show updated points and resources（更新されたポイントやリソースを表示する）
                                    print("Player:{}, Resources:{}, Points: {}".format(
                                        currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))

                                # Check if player wants to trade with another player（プレイヤーが他のプレイヤーとのトレードを希望しているかどうかをチェックする）
                                if(self.boardView.tradePlayers_button.collidepoint(e.pos)):
                                    currPlayer.initiate_trade(self, 'PLAYER')
                                    # Show updated points and resources（更新されたポイントやリソースを表示する）
                                    print("Player:{}, Resources:{}, Points: {}".format(
                                        currPlayer.name, currPlayer.resources, currPlayer.victoryPoints))

                                # Check if player wants to end turn（ターンの終了を希望するかどうかを確認する）
                                if(self.boardView.endTurn_button.collidepoint(e.pos)):
                                    # Can only end turn after rolling dice（サイコロを振ってからでないとターンを終了できない）
                                    if(diceRolled == True):
                                        print("Ending Turn!")
                                        turnOver = True  # Update flag to nextplayer turn（次プレーヤーのターンにフラグを更新する）

                    # Update the display（ディスプレイを更新する）
                    #self.displayGameScreen(None, None)
                    pygame.display.update()

                    # Check if game is over（ゲームオーバーを確認する）
                    if currPlayer.victoryPoints >= self.maxPoints:
                        self.gameOver = True
                        self.turnOver = True
                        print("====================================================")
                        print("PLAYER {} WINS!".format(currPlayer.name))
                        print("Exiting game in 10 seconds...")
                        break

                if(self.gameOver):
                    startTime = pygame.time.get_ticks()
                    runTime = 0
                    while(runTime < 10000):  # 10 second delay prior to quitting（終了前に10秒間の遅延）
                        runTime = pygame.time.get_ticks() - startTime

                    break


# Initialize new game and run（新しいゲームの初期化および実行）
newGame = catanGame()
newGame.playCatan()

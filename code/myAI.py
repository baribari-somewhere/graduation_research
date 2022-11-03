# Settlers of Catan
# Heuristic AI class implementation（ヒューリスティックAIクラスの実装）

from board import *
from player import *
import numpy as np

# Class definition for an AI player（AIプレーヤーのクラス定義）


class myAI(player):

    # Update AI player flag and resources（AIプレイヤーフラグとリソースの更新）
    def updateAI(self):
        self.isAI = True
        self.road_F = False
        self.settlement_F = False
        self.city_F = False
        self.setupResources = []  # List to keep track of setup resources（セットアップリソースを記録するためのリスト）
        # Initialize resources with just correct number needed for set up（セットアップに必要な数だけリソースを初期化する）
        # Dictionary that keeps track of resource amounts（リソース量を把握する辞書）
        self.resources = {'ORE': 0, 'BRICK': 4,
                          'WHEAT': 2, 'WOOD': 4, 'SHEEP': 2}

        # 勝手につけたしたself.dev
        # self.devCards = {'KNIGHT': 0, 'VP': 0, 'MONOPOLY': 0,
        #                  'ROADBUILDER': 0, 'YEAROFPLENTY': 0}
        #print("Added new AI Player:", self.name)

    # Function to build an initial settlement - just choose random spot for now（初期集落を作る機能 - とりあえずランダムな場所を選んでください）
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

    def move(self, board):
        #print("AI Player {} playing...".format(self.name))
        # Trade resources if there are excessive amounts of a particular resource（特定のリソースが過剰にある場合、リソースをトレードする）
        self.trade()
        # Build a settlements, city and few roads（集落、都市、道路を作る）
        possibleVertices = board.get_potential_settlements(self)
        if(possibleVertices != {} and (self.resources['BRICK'] > 0 and self.resources['WOOD'] > 0 and self.resources['SHEEP'] > 0 and self.resources['WHEAT'] > 0)):
            randomVertex = np.random.randint(0, len(possibleVertices.keys()))
            self.build_settlement(list(possibleVertices.keys())[
                                  randomVertex], board)

        # Build a City（都市を創る）
        possibleVertices = board.get_potential_cities(self)
        if(possibleVertices != {} and (self.resources['WHEAT'] >= 2 and self.resources['ORE'] >= 3)):
            randomVertex = np.random.randint(0, len(possibleVertices.keys()))
            self.build_city(list(possibleVertices.keys())[randomVertex], board)

        # Build a couple roads（道路を2本作る）
        # for i in range(2):
        #     if(self.resources['BRICK'] > 0 and self.resources['WOOD'] > 0):
        #         possibleRoads = board.get_potential_roads(self)
        #         randomEdge = np.random.randint(0, len(possibleRoads.keys()))
        #         self.build_road(list(possibleRoads.keys())[randomEdge][0], list(
        #             possibleRoads.keys())[randomEdge][1], board)

        possibleRoads = board.get_potential_roads(self)
        if(possibleRoads != {} and self.resources['BRICK'] > 0 and self.resources['WOOD'] > 0):
            #possibleRoads = board.get_potential_roads(self)
            randomEdge = np.random.randint(0, len(possibleRoads.keys()))
            self.build_road(list(possibleRoads.keys())[randomEdge][0], list(
                possibleRoads.keys())[randomEdge][1], board)

        # Draw a Dev Card with 1/3 probability（1/3の確率でデブカードを引く）
        devCardNum = np.random.randint(0, 3)
        if(devCardNum == 0):
            self.draw_devCard(board)

        return

    # Wrapper function to control all trading（すべての取引を制御するラッパー機能）
    def trade(self):
        for r1, r1_amount in self.resources.items():
            if(r1_amount >= 6):  # heuristic to trade if a player has more than 5 of a particular resource（プレイヤーが特定のリソースを5つ以上持っている場合のヒューリスティックトレード）
                for r2, r2_amount in self.resources.items():
                    if(r2_amount < 1):
                        self.trade_with_bank(r1, r2)
                        break

    # Choose which player to rob（どのプレイヤーから奪うかを選ぶ）

    def choose_player_to_rob(self, board):
        '''Heuristic function to choose the player with maximum points.
        Choose hex with maximum other players, Avoid blocking own resource
        args: game board object
        returns: hex index and player to rob
        '''
        # Get list of robber spots（強盗スポットリスト入手）
        robberHexDict = board.get_robber_spots()

        # Choose a hexTile with maximum adversary settlements（敵の入植地が最大のヘクスタイルを選択する）
        maxHexScore = 0  # Keep only the best hex to rob（最高の呪文だけを奪っておく）
        for hex_ind, hexTile in robberHexDict.items():
            # Extract all 6 vertices of this hexTile（hexTile の 6 個の頂点をすべて抽出する）
            vertexList = polygon_corners(board.flat, hexTile.hex)

            hexScore = 0  # Heuristic score for hexTile（hexTileのヒューリスティックスコア）
            playerToRob_VP = 0
            playerToRob = None
            for vertex in vertexList:
                playerAtVertex = board.boardGraph[vertex].state['Player']
                if playerAtVertex == self:
                    hexScore -= self.victoryPoints
                elif playerAtVertex != None:  # There is an adversary on this vertex（この頂点には敵対者が存在する）
                    hexScore += playerAtVertex.visibleVictoryPoints
                    # Find strongest other player at this hex, provided player has resources（このヘクスにいる最強の他プレイヤーを探す(リソースがある場合)）
                    if playerAtVertex.visibleVictoryPoints >= playerToRob_VP and sum(playerAtVertex.resources.values()) > 0:
                        playerToRob_VP = playerAtVertex.visibleVictoryPoints
                        playerToRob = playerAtVertex
                else:
                    pass

            if hexScore >= maxHexScore and playerToRob != None:
                hexToRob_index = hex_ind
                playerToRob_hex = playerToRob
                maxHexScore = hexScore

        return hexToRob_index, playerToRob_hex

    def heuristic_move_robber(self, board):
        '''Function to control heuristic AI robber
        Calls the choose_player_to_rob and move_robber functions
        args: board object
        '''
        # Get the best hex and player to rob（最高のヘクスとプレイヤーを手に入れて強奪する）
        hex_i, playerRobbed = self.choose_player_to_rob(board)

        # Move the robber（強盗を移動させる）
        self.move_robber(hex_i, board, playerRobbed)

        return

    # def heuristic_play_dev_card(self, board):
    #     '''Heuristic strategies to choose and play a dev card
    #     args: board object
    #     '''
    #     #Check if player can play a devCard this turn
    #     if self.devCardPlayedThisTurn != True:
    #         #Get a list of all the unique dev cards this player can play
    #         devCardsAvailable = []
    #         for cardName, cardAmount in self.devCards.items():
    #             if(cardName != 'VP' and cardAmount >= 1): #Exclude Victory points
    #                 devCardsAvailable.append((cardName, cardAmount))

    #         if(len(devCardsAvailable) >=1):
        # If a hexTile is currently blocked, try and play a Knight

        # If expansion needed, try road-builder

        # If resources needed, try monopoly or year of plenty

    def resources_needed_for_settlement(self):
        '''Function to return the resources needed for a settlement
        args: player object - use self.resources
        returns: list of resources needed for a settlement

        集落に必要な資源を返す関数
        args: プレイヤーオブジェクト - self.resourcesを使用
        戻り値: 集落に必要な資源リスト
        '''
        resourcesNeededDict = {}
        for resourceName in self.resources.keys():
            if resourceName != 'ORE' and self.resources[resourceName] == 0:
                resourcesNeededDict[resourceName] = 1

        return resourcesNeededDict

    def resources_needed_for_city(self):
        '''Function to return the resources needed for a city
        args: player object - use self.resources
        returns: list of resources needed for a city

        都市に必要な資源を返す関数
        args: プレイヤーオブジェクト - self.resourcesを使用。
        returns: 都市に必要な資源のリスト
        '''
        resourcesNeededDict = {}
        if self.resources['ORE'] < 3:
            resourcesNeededDict['ORE'] = 3 - self.resources['ORE']

        if self.resources['WHEAT'] < 2:
            resourcesNeededDict['ORE'] = 2 - self.resources['WHEAT']

        return resourcesNeededDict

    def heuristic_discard(self):
        '''Function for the AI to choose a set of cards to discard upon rolling a 7

        7が出たときにAIが捨て札を選ぶ機能
        '''
        return

    # Function to propose a trade -> give r1 and get r2
    # Propose a trade as a dictionary with {r1:amt_1, r2: amt_2} specifying the trade
    # def propose_trade_with_players(self):

    # Function to accept/reject trade - return True if accept
    # def accept_trade(self, r1_dict, r2_dict):

    # Function to find best action - based on gamestate

    # 取引を提案する関数 → r1 を与え r2 を得る
    # トレードの提案は、トレードを指定する {r1:amt_1, r2:amt_2} という辞書として行う。
    # def propose_trade_with_players(self):

    # トレードを受け入れるか拒否するかの関数 - acceptの場合はTrueを返す。
    # def accept_trade(self, r1_dict, r2_dict):

    # 最適な行動を見つける関数 - gamestateに基づく

    def get_action(self):
        return

    # Function to execute the player's action（プレイヤーのアクションを実行する関数）
    def execute_action(self):
        return

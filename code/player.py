# Settlers of Catan
# Player class implementation(プレイヤークラスの実装)

from board import *
import numpy as np

# Class definition for a player(プレーヤーのクラス定義)


class player():
    'Class Definition for Game Player'

    # Initialize a game player, we use A, B and C to identify(ゲームプレイヤーの初期化、A,B,Cで識別します)
    def __init__(self, playerName, playerColor):
        self.name = playerName
        self.color = playerColor
        self.victoryPoints = 0
        self.isAI = False

        self.trade_fin = False

        self.settlementsLeft = 5
        self.roadsLeft = 15
        self.citiesLeft = 4
        # Dictionary that keeps track of resource amounts(リソース量を記録する辞書)
        self.resources = {'ORE': 5, 'BRICK': 6,
                          'WHEAT': 3, 'WOOD': 6, 'SHEEP': 3}

        self.knightsPlayed = 0
        self.largestArmyFlag = False

        self.maxRoadLength = 0
        self.longestRoadFlag = False

        # Undirected Graph to keep track of which vertices and edges player has colonised
        # Every time a player's build graph is updated the gameBoardGraph must also be updated
        '''#プレイヤーがどの頂点と辺を植民地化したかを記録するための 無向性グラフ
        #プレイヤーの構築グラフが更新されるたびに、gameBoardGraphも更新されなければならない。'''

        # Each of the 3 lists store vertex information - Roads are stores with tuples of vertex pairs(3つのリストにはそれぞれ頂点の情報が格納される - Roadsは頂点のペアのタプルを持つストア)
        self.buildGraph = {'ROADS': [], 'SETTLEMENTS': [], 'CITIES': []}
        self.portList = []  # List of ports acquired

        # Dev cards in possession(所持しているデビットカード)
        # List to keep the new dev cards draw - update the main list every turn(新開発カードのドローを維持するためのリスト - メインリストを毎ターン更新する)
        self.newDevCards = []
        self.devCards = {'KNIGHT': 0, 'VP': 0, 'MONOPOLY': 0,
                         'ROADBUILDER': 0, 'YEAROFPLENTY': 0}
        self.devCardPlayedThisTurn = False

        self.visibleVictoryPoints = self.victoryPoints - self.devCards['VP']

    # function to build a road from vertex v1 to vertex v2(頂点 v1 から頂点 v2 までの道路を作る機能)
    def build_road(self, v1, v2, board):
        'Update buildGraph to add a road on edge v1 - v2'

        # Check if player has resources available(プレイヤーにリソースがあるかどうか確認する)
        if(self.resources['BRICK'] > 0 and self.resources['WOOD'] > 0):
            if(self.roadsLeft > 0):  # Check if player has roads left(プレイヤーにロードが残っているか確認する)
                # 道を作る際にv1の方の数字を必ず小さくする
                if(v1 > v2):
                    x = v1
                    v1 = v2
                    v2 = x

                self.buildGraph['ROADS'].append((v1, v2))
                self.roadsLeft -= 1

                # Update player resources(プレイヤーリソースのアップデート)
                self.resources['BRICK'] -= 1
                self.resources['WOOD'] -= 1

                # update the overall boardGraph(boardGraph全体を更新する)
                board.updateBoardGraph_road(v1, v2, self)

                # Calculate current max road length and update(現在の最大道路長を計算し、更新します)
                maxRoads = self.get_road_length(board)
                self.maxRoadLength = maxRoads

                # print('{} Built a Road. MaxRoadLength: {}'.format(
                #     self.name, self.maxRoadLength))

            else:
                a = 1
                #print("No roads available to build")

        else:
            a = 1
            #print("Insufficient Resources to Build Road - Need 1 BRICK, 1 WOOD")

    # function to build a settlement on vertex with coordinates vCoord(座標vCoordを持つ頂点に集落を作る関数です)
    def build_settlement(self, vCoord, board):
        'Update player buildGraph and boardgraph to add a settlement on vertex v'
        # Take input from Player on where to build settlement
        # Check if player has correct resources
        # Update player resources and boardGraph with transaction
        '''
        プレイヤーから決済場所についての入力を受ける
            #プレーヤーが正しい資源を持っているかどうか確認する
                #プレイヤーの資源とボードグラフをトランザクションで更新する。
        '''

        # Check if player has resources available
        if(self.resources['BRICK'] > 0 and self.resources['WOOD'] > 0 and self.resources['SHEEP'] > 0 and self.resources['WHEAT'] > 0):
            if(self.settlementsLeft > 0):  # Check if player has settlements left(プレイヤーにセトリングが残っているかどうかを確認する)
                self.buildGraph['SETTLEMENTS'].append(vCoord)
                self.settlementsLeft -= 1

                # Update player resources(プレイヤーリソースのアップデート)
                self.resources['BRICK'] -= 1
                self.resources['WOOD'] -= 1
                self.resources['SHEEP'] -= 1
                self.resources['WHEAT'] -= 1

                self.victoryPoints += 1
                # update the overall boardGraph(boardGraph全体を更新する)
                board.updateBoardGraph_settlement(vCoord, self)

                #print('{} ()Built a Settlement'.format(self.name))

                # Add port to players port list if it is a new port(新しいポートの場合、プレイヤーポートリストにポートを追加する)
                if((board.boardGraph[vCoord].port != False) and (board.boardGraph[vCoord].port not in self.portList)):
                    self.portList.append(board.boardGraph[vCoord].port)
                    # print("{} now has {} Port access".format(
                    #     self.name, board.boardGraph[vCoord].port))

            else:
                a = 1
                # print("No settlements available to build")

        else:
            a = 1
            # print(
            #     "Insufficient Resources to Build Settlement. Build Cost: 1 BRICK, 1 WOOD, 1 WHEAT, 1 SHEEP")

    # function to build a city on vertex v(頂点vに都市を建設する機能)
    def build_city(self, vCoord, board):
        'Upgrade existing settlement to city in buildGraph'
        # Check if player has resources available(プレイヤーにリソースがあるかどうか確認する)
        if(self.resources['WHEAT'] >= 2 and self.resources['ORE'] >= 3):
            if(self.citiesLeft > 0):
                self.buildGraph['CITIES'].append(vCoord)
                # Increase number of settlements and decrease number of cities(集落の数を増やし、都市の数を減らす)
                self.settlementsLeft += 1
                self.citiesLeft -= 1

                # Update player resources(プレイヤーリソースのアップデート)
                self.resources['ORE'] -= 3
                self.resources['WHEAT'] -= 2
                self.victoryPoints += 1

                # update the overall boardGraph(boardGraph全体を更新する)
                board.updateBoardGraph_city(vCoord, self)
                #print('{} Built a City'.format(self.name))

            else:
                a = 1
                #print("No cities available to build")

        else:
            a = 1
            #print("Insufficient Resources to Build City. Build Cost: 3 ORE, 2 WHEAT")

    # function to move robber to a specific hex and steal from a player(強盗を特定のヘクスに移動させ、プレイヤーから盗む機能 強盗を特定のヘクスに移動させ、プレイヤーから盗む機能)
    def move_robber(self, hexIndex, board, player_robbed):
        'Update boardGraph with Robber and steal resource'
        board.updateBoardGraph_robber(hexIndex)

        # Steal a random resource from other players(他のプレイヤーからランダムに資源を盗む)
        self.steal_resource(player_robbed)

        return

    # Function to steal a random resource from player_2(プレイヤー_2からランダムな資源を盗む機能)
    def steal_resource(self, player_2):
        if(player_2 == None):
            #print("No Player on this hex to Rob")
            return

        # Get all resources player 2 has in a list and use random list index to steal(プレイヤー2が持っているすべての資源をリストで取得し、ランダムなリストのインデックスを使用して盗み出す)
        p2_resources = []
        for resourceName, resourceAmount in player_2.resources.items():
            p2_resources += [resourceName]*resourceAmount

        resourceIndexToSteal = np.random.randint(0, len(p2_resources))

        # Get a random permutation and steal a card(ランダムな順列を取得し、カードを盗む)
        p2_resources = np.random.permutation(p2_resources)
        resourceStolen = p2_resources[resourceIndexToSteal]

        # Update resources of both players(両プレイヤーのリソースを更新)
        player_2.resources[resourceStolen] -= 1
        self.resources[resourceStolen] += 1
        # print("Stole 1 {} from Player {}".format(
        #     resourceStolen, player_2.name))

        return

    # Function to calculate road length for longest road calculation
    # Use both player buildgraph and board graph to compute recursively
    '''
    #最長道路計算のための道路長を計算する関数
    #プレイヤーのビルドグラフとボードのグラフの両方を用いて再帰的に計算を行う'''

    def get_road_length(self, board):
        # List to store road lengths from each starting edge(各起点エッジからの道路の長さを格納するリスト)
        roadLengths = []
        # check for every starting edge(すべての始点エッジをチェックします)
        for road in self.buildGraph['ROADS']:
            # List to keep track of all lengths of roads resulting from this root road(このルートロードから生じるすべての長さの道路を記録するためのリスト)
            self.road_i_lengths = []
            roadCount = 0
            roadArr = []
            vertexList = []
            #print("Start road:", road)
            self.check_path_length(
                road, roadArr, roadCount, vertexList, board.boardGraph)

            road_inverted = (road[1], road[0])
            roadCount = 0
            roadArr = []
            vertexList = []
            self.check_path_length(
                road_inverted, roadArr, roadCount, vertexList, board.boardGraph)

            # Update roadLength with max starting from this road(この道路を起点とした最大値で roadLength を更新する)
            roadLengths.append(max(self.road_i_lengths))
            # print(self.road_i_lengths)

        #print("Road Lengths:", roadLengths, max(roadLengths))
        return max(roadLengths)

    # Function to checl the path length from a current edge to all possible other vertices not yet visited by t(現在の辺から，t がまだ訪れていない他のすべての可能な頂点までの経路長を チェックするための関数)
    def check_path_length(self, edge, edgeList, roadLength, vertexList, boardGraph):
        # Append current edge to list and increment road count(現在のエッジをリストに追加し、道路数を増加させる)
        edgeList.append(edge)  # Append the road(道路を追加する)
        roadLength += 1
        vertexList.append(edge[0])  # Append the first vertex(最初の頂点を追加する)

        # Get new neighboring forward edges from this edge - not visited by the search yet(このエッジから新しい隣接する前方エッジを取得する - まだ検索で訪れていないエッジを取得する)
        road_neighbors_list = self.get_neighboring_roads(
            edge, boardGraph, edgeList, vertexList)

        # print(neighboringRoads)
        # if no neighboring roads exist append the roadLength upto this edge(隣接する道路が存在しない場合，このエッジまでの道路の長さを追加する)
        if(road_neighbors_list == []):
            #print("No new neighbors found")
            self.road_i_lengths.append(roadLength)
            return

        else:
            # check paths from left and right neighbors separately(左隣と右隣のパスを別々にチェック)
            for neighbor_road in road_neighbors_list:
                #print("checking neighboring edge:", neighbor_road)
                self.check_path_length(
                    neighbor_road, edgeList, roadLength, vertexList, boardGraph)

    # Helper function to get neighboring edges from this road that haven't already been explored
    # We want forward neighbors only
    '''#この道路から、まだ探索されていない隣接辺を取得するためのヘルパー関数
    #前方近傍のみを取得したい'''

    def get_neighboring_roads(self, road_i, boardGraph, visitedRoads, visitedVertices):
        #print("Getting neighboring roads for current road:", road_i)
        newNeighbors = []
        # Use v1 and v2 to get the vertices to expand from(v1 と v2 を使って展開する頂点を取得する)
        v1 = road_i[0]
        v2 = road_i[1]
        for edge in self.buildGraph['ROADS']:
            if(edge[1] in visitedVertices):
                # flip the edge if the orientation is reversed(エッジの向きが反転している場合は、エッジを反転させる)
                edge = (edge[1], edge[0])

            if(edge not in visitedRoads):  # If it is a new distinct edge(新しい明確なエッジである場合)
                # Add condition for vertex to be not colonised by anyone else(頂点が他の誰からも植民地化されていないことの条件の追加)
                if(boardGraph[v2].state['Player'] in [self, None]):
                    # If v2 has neighbors, defined starting or finishing at v2(v2が隣接している場合、v2で開始または終了するように定義される)
                    if(edge[0] == v2 and edge[0] not in visitedVertices):
                        #print("Appending NEW neighbor:", edge)
                        newNeighbors.append(edge)

                    if(edge[0] == v1 and edge[0] not in visitedVertices):
                        newNeighbors.append(edge)

                    # If v1 has neighbors, defined starting or finishing at v2(v1 が隣接する場合、v2 で開始または終了するように定義される)
                    if(edge[1] == v2 and edge[1] not in visitedVertices):
                        newNeighbors.append((edge[1], edge[0]))

                    if(edge[1] == v1 and edge[1] not in visitedVertices):
                        newNeighbors.append((edge[1], edge[0]))

        return newNeighbors

    # function to end turn(ターンエンド機能)
    def end_turn():
        'Pass turn to next player and update game state'

    # function to draw a Development Card(開発カードを描画する機能)
    def draw_devCard(self, board):
        'Draw a random dev card from stack and update self.devcards'
        # Check if player has resources available
        if(self.resources['WHEAT'] >= 1 and self.resources['ORE'] >= 1 and self.resources['SHEEP'] >= 1):
            # Get alldev cards available(利用可能なalldevカードを取得する)
            devCardsToDraw = []
            for cardName, cardAmount in board.devCardStack.items():
                devCardsToDraw += [cardName]*cardAmount

            # IF there are no devCards left(デビットカードが残っていない場合)
            if(devCardsToDraw == []):
                #print("No Dev Cards Left!")
                a = 1
                return

            devCardIndex = np.random.randint(0, len(devCardsToDraw))

            # Get a random permutation and draw a card(ランダムな順列を取得し、カードを引く)
            devCardsToDraw = np.random.permutation(devCardsToDraw)
            cardDrawn = devCardsToDraw[devCardIndex]

            # Update player resources(プレイヤーリソースのアップデート)
            self.resources['ORE'] -= 1
            self.resources['WHEAT'] -= 1
            self.resources['SHEEP'] -= 1

            # If card is a victory point apply immediately, else add to new card list(カードが勝利ポイントであれば即座に適用し、そうでなければ新しいカードリストに追加する)
            if(cardDrawn == 'VP'):
                self.victoryPoints += 1
                board.devCardStack[cardDrawn] -= 1
                self.devCards[cardDrawn] += 1
                self.visibleVictoryPoints = self.victoryPoints - \
                    self.devCards['VP']

            # Update player dev card and the stack(プレイヤーデバイスカードとスタックをアップデート)
            else:
                self.newDevCards.append(cardDrawn)
                board.devCardStack[cardDrawn] -= 1

            # print("{} drew a {} from Development Card Stack".format(
            #     self.name, cardDrawn))

        else:
            a = 1
            #print("Insufficient Resources for Dev Card. Cost: 1 ORE, 1 WHEAT, 1 SHEEP")

    # Function to update dev card stack with dev cards drawn from prior turn(前のターンで引いた開発カードを開発カードスタックに反映させる機能)
    def updateDevCards(self):
        for newCard in self.newDevCards:
            self.devCards[newCard] += 1

        # Reset the new card list to blank(新しいカードリストを白紙に戻す)
        self.newDevCards = []

    # function to play a development card(開発カードをプレイする機能)
    def play_devCard(self, game):
        'Update game state'
        # Check if player can play a devCard this turn(このターンにデブカードをプレイできるかどうかチェックする)
        if(self.devCardPlayedThisTurn):
            #print('Already played 1 Dev Card this turn!')
            return

        # Get a list of all the unique dev cards this player can play(このプレイヤーがプレイできるすべてのユニークな開発カードのリストを取得する)
        devCardsAvailable = []
        for cardName, cardAmount in self.devCards.items():
            if(cardName != 'VP' and cardAmount >= 1):  # Exclude Victory points(ビクトリーポイントを除く)
                devCardsAvailable.append((cardName, cardAmount))

        if(devCardsAvailable == []):
            a = 1
            #print("No Development Cards available to play")
            return

        # Use Keyboard control to play the Dev Card(キーボード操作でデヴューカードを再生する)
        devCard_dict = {}
        for indx, card in enumerate(devCardsAvailable):
            devCard_dict[indx] = card[0]

        #print("Development Cards Available to Play", devCard_dict)

        devCardNumber = -1
        while (devCardNumber not in devCard_dict.keys()):
            devCardNumber = int(input("Enter Dev card number to play:"))

        # Play the devCard and update player's dev cards(devCardを再生し、プレイヤーのdevカードを更新する)
        devCardPlayed = devCard_dict[devCardNumber]
        self.devCardPlayedThisTurn = True

        #print("Playing Dev Card:", devCardPlayed)
        self.devCards[devCardPlayed] -= 1

        # Logic for each Dev Card(各デバイスカード用ロジック)
        if(devCardPlayed == 'KNIGHT'):
            game.robber(self)
            self.knightsPlayed += 1

        if(devCardPlayed == 'ROADBUILDER'):
            game.build(self, 'ROAD')
            game.boardView.displayGameScreen()
            game.build(self, 'ROAD')
            game.boardView.displayGameScreen()

        # Resource List for Year of Plenty and Monopoly(イヤー・オブ・プレンティとモノポリーのリソース・リスト)
        resource_list = ['BRICK', 'WOOD', 'WHEAT', 'SHEEP', 'ORE']

        if(devCardPlayed == 'YEAROFPLENTY'):
            #print("Resources available:", resource_list)

            r1, r2 = "", ""
            while ((r1 not in self.resources.keys()) or (r2 not in self.resources.keys())):
                r1 = input("Enter resource 1 name: ").upper()
                r2 = input("Enter resource 2 name: ").upper()

            self.resources[r1] += 1
            self.resources[r2] += 1

        if(devCardPlayed == 'MONOPOLY'):
            print("Resources to Monopolize:", resource_list)

            resourceToMonopolize = ""
            while (resourceToMonopolize not in self.resources.keys()):
                resourceToMonopolize = input(
                    "Enter resource name to monopolise: ").upper()

            # Loop over each player to Monopolize all resources(各プレイヤーをループさせ、すべてのリソースを独占する)
            for player in list(game.playerQueue.queue):
                if(player != self):
                    numLost = player.resources[resourceToMonopolize]
                    player.resources[resourceToMonopolize] = 0
                    self.resources[resourceToMonopolize] += numLost

        return

    # Function to basic trade 4:1 with bank, or use ports to trade(銀行と4対1の基本取引、またはポートを使っての取引に対応する機能)
    def trade_with_bank(self, r1, r2):
        '''Function to implement trading with bank
        r1: resource player wants to trade away
        r2: resource player wants to receive
        Automatically give player the best available trade ratio
        '''
        # Get r1 port string(r1 ポートの文字列を取得する)
        r1_port = "2:1 " + r1
        # Can use 2:1 port with r1(r1との2:1ポート使用可能)
        if(r1_port in self.portList and self.resources[r1] >= 2):
            self.resources[r1] -= 2
            self.resources[r2] += 1
            #print("Traded 2 {} for 1 {} using {} Port".format(r1, r2, r1))
            return

        # Check for 3:1 Port(3:1ポートにチェック)
        elif('3:1 PORT' in self.portList and self.resources[r1] >= 3):
            self.resources[r1] -= 3
            self.resources[r2] += 1
            #print("Traded 3 {} for 1 {} using 3:1 Port".format(r1, r2))
            return

        # Check 4:1 port(4:1ポートを確認)
        elif(self.resources[r1] >= 4):
            self.resources[r1] -= 4
            self.resources[r2] += 1
            #print("Traded 4 {} for 1 {}".format(r1, r2))
            return

        else:
            #print("Insufficient resource {} to trade with Bank".format(r1))
            self.trade_fin = True
            return

    # Function to initate a trade - with bank or other players(銀行や他のプレイヤーとの取引を開始する機能)
    def initiate_trade(self, game, trade_type):
        '''Wrapper function to initiate a trade with bank or other players
        trade_type: flag to determine the trade
        '''
        # List to show the resource names and trade menu options(リソース名とトレードメニューオプションを表示するためのリスト)
        resource_list = ['BRICK', 'WOOD', 'WHEAT', 'SHEEP', 'ORE']

        if trade_type == 'BANK':
            # display resource names(表示リソース名)
            print("\nBank Trading Menu - Resource Names:", resource_list)

            # Player to select resource to trade(プレイヤーは取引する資源を選択する)
            resourceToTrade = ""
            while (resourceToTrade not in self.resources.keys()):
                resourceToTrade = input(
                    "Enter resource name to trade with bank:").upper()

            # Player to select resource to receive - disallow receiving same resource as traded(プレイヤーは受け取る資源を選択する - トレードされた資源と同じものを受け取ることはできない)
            resourceToReceive = ""
            while (resourceToReceive not in self.resources.keys()) or (resourceToReceive == resourceToTrade):
                resourceToReceive = input(
                    "Enter resource name to receive from bank:").upper()

            # Try and trade with Bank(銀行と取引してみる)
            # Note: Ports and Error handling handled in trade with bank function(銀行機能とのトレードで処理されるポートおよびエラー処理)
            self.trade_with_bank(resourceToTrade, resourceToReceive)

            return

        elif trade_type == 'PLAYER':
            # Select player to trade with - generate list of other players(トレードする相手を選ぶ - 相手のリストを生成する)
            playerNames = [p.name for p in list(game.playerQueue.queue)]

            # print("\nInter-Player Trading Menu - Player Names:", playerNames)
            # print("Resource List:", resource_list)

            # Disallow trading with self(自己との取引禁止)
            playerToTrade_name = ''
            while (playerToTrade_name not in playerNames) or (playerToTrade_name == self.name):
                playerToTrade_name = input(
                    "Enter name of another player to trade with:")

            # Over write and store the target player object(ターゲット・プレイヤー・オブジェクトの書き込みと保存を行う)
            playerToTrade = None
            for player in list(game.playerQueue.queue):
                if player.name == playerToTrade_name:
                    playerToTrade = player

            # Select resource to trade - must have at least one of that resource to trade(トレードする資源を選択する - トレードするためには、その資源を少なくとも1つ持っている必要があります)
            resourceToTrade = ""
            while (resourceToTrade not in self.resources.keys()):
                resourceToTrade = input("Enter resource name to trade with player {}:".format(
                    playerToTrade_name)).upper()
                # Reset if invalid resource is chosen(無効なリソースが選択された場合、リセットされる)
                if resourceToTrade in self.resources.keys() and self.resources[resourceToTrade] == 0:
                    resourceToTrade = ""
                    #print("Players can only trade resources they already have")

            # Specify quantity to trade(取引数量を指定する)
            resource_traded_amount = 0
            while (resource_traded_amount > self.resources[resourceToTrade]) or (resource_traded_amount < 1):
                resource_traded_amount = int(input("Enter quantity of {} to trade with player {}:".format(
                    resourceToTrade, playerToTrade_name)))

            # Player to select resource to receive - disallow receiving same resource as traded(プレイヤーは受け取る資源を選択する - トレードされた資源と同じものを受け取ることはできない)
            resourceToReceive = ""
            while (resourceToReceive not in self.resources.keys()) or (resourceToReceive == resourceToTrade):
                resourceToReceive = input(
                    "Enter resource name to receive from player {}:".format(playerToTrade_name)).upper()
                # Reset if invalid resource is chosen(無効なリソースが選択された場合、リセットされる)
                if resourceToReceive in self.resources.keys() and playerToTrade.resources[resourceToReceive] == 0:
                    resourceToReceive = -""
                    # print("Player {} doesn't have any {} to trade".format(
                    #     playerToTrade_name, resourceToReceive))

            # Specify quantity to receive(受取数量を指定する)
            resource_received_amount = 0
            while (resource_received_amount > playerToTrade.resources[resourceToReceive]) or (resource_received_amount < 1):
                resource_received_amount = int(input("Enter quantity of {} to receive from player {}:".format(
                    resourceToReceive, playerToTrade_name)))

            # Execute trade - player gives resource traded and gains resource received(トレードの実行 - プレイヤーはトレードされた資源を渡し、受け取った資源を得る)
            self.resources[resourceToReceive] += resource_received_amount
            self.resources[resourceToTrade] -= resource_traded_amount

            # Other player gains resource traded and gives resource received(他プレイヤーは取引された資源を獲得し、受け取った資源を与える)
            playerToTrade.resources[resourceToReceive] -= resource_received_amount
            playerToTrade.resources[resourceToTrade] += resource_traded_amount

            # print("Player {} successfully traded {} {} for {} {} with player {}".format(self.name, resource_traded_amount, resourceToTrade,
            #                                                                             resource_received_amount, resourceToReceive, playerToTrade_name))

            return

        else:
            a = 1
            #print("Illegal trade_type flag")
            return

    # Function to discard cards(カード廃棄機能)
    def discardResources(self):
        '''Function to enable a player to select cards to discard when a 7 is rolled
        '''
        maxCards = 7  # Default is 7, but can be changed for testing(デフォルトは7ですが、テスト用に変更可能です)

        # Calculate resources to discard(廃棄する資源を計算する)
        totalResourceCount = 0
        for resource, amount in self.resources.items():
            totalResourceCount += amount

        # Logic to calculate number of cards to discard and allow player to select(捨てるカードの枚数を計算し、プレイヤーが選択できるようにするロジック)
        if totalResourceCount > maxCards:
            numCardsToDiscard = int(totalResourceCount/2)
            print("\nPlayer {} has {} cards and MUST choose {} cards to discard...".format(
                self.name, totalResourceCount, numCardsToDiscard))

            # Loop to allow player to discard cards(カードを捨てられるようにするループ)
            for i in range(numCardsToDiscard):
                print("Player {} current resources to choose from:", self.resources)

                resourceToDiscard = ''
                while (resourceToDiscard not in self.resources.keys()) or (self.resources[resourceToDiscard] == 0):
                    resourceToDiscard = input(
                        "Enter resource to discard: ").upper()

                # Discard that resource(そのリソースを破棄する)
                self.resources[resourceToDiscard] -= 1
                print("Player {} discarded a {}, and needs to discard {} more cards".format(
                    self.name, resourceToDiscard, (numCardsToDiscard-1-i)))

        else:
            print("\nPlayer {} has {} cards and does not need to discard any cards!".format(
                self.name, totalResourceCount))
            return

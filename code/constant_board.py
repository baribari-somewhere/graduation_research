# Settlers of Catan
# Game board class implementation
# カタンの開拓者たち
# ゲームボード・クラスの実装

from operator import index
from string import *
#import numpy as np
from hexTile import *
from hexLib import *
from player import *
#import networkx as nx
#import matplotlib.pyplot as plt
import pygame

pygame.init()

# Class to implement Catan board logic（カタンボードロジックを実装するクラス）
# Use a graph representation for the board（ボード用のグラフ表示を使用する）


class constant_catanBoard(hexTile, Vertex):
    'Class Definition for Catan Board Logic'
    # Object Creation - creates a random board configuration with hexTiles（オブジェクトの作成 - hexTilesでランダムなボード構成を作成します。）

    def __init__(self):
        # Dict to store all hextiles, with hexIndex as key（hexIndex をキーとして、すべてのヘキスタイルを格納するディクショナリ）
        self.hexTileDict = {}
        # Dict to store the Vertices coordinates with vertex indices as keys（頂点のインデックスをキーとする頂点座標を格納するディクショナリ）
        self.vertex_index_to_pixel_dict = {}
        self.boardGraph = {}  # Dict to store the vertex objects with the pixelCoordinates as keys（pixelCoordinates をキーとする頂点オブジェクトを格納するディクショナリ）

        self.edgeLength = 80  # Specify for hex size（六角サイズに指定する）
        self.size = self.width, self.height = 1000, 800
        self.flat = Layout(layout_flat, Point(self.edgeLength, self.edgeLength), Point(
            self.width/2, self.height/2))  # specify Layout

        self.total_hexIndex_i = 0

        ##INITIALIZE BOARD##
        #print("Initializing Catan Game Board...")
        # Assign resources numbers randomly（リソース番号をランダムに割り当てる）
        self.resourcesList = self.getRandomResourceList()
        #print(f"self.resourcesList: {self.resourcesList}")

        # Get a random permutation of indices 0-18 to use with the resource list（リソースリストで使用するインデックス0〜18のランダムな並べ替えを取得します）
        randomIndices = np.random.permutation(
            [i for i in range(len(self.resourcesList))])
        # print(f"randomIndices: {randomIndices}")

        reinitializeCount = 0
        # Initialize a valid resource list that does not allow adjacent 6's and 8's（隣接する6と8を許可しない有効なリソースリストの初期化）
        while(self.checkHexNeighbors(randomIndices) == False):
            reinitializeCount += 1
            randomIndices = np.random.permutation(
                [i for i in range(len(self.resourcesList))])
        #print(f"randomIndices: {randomIndices}")
        # randomIndices = [1, 4, 10, 6, 3, 15, 14, 11,
        #                  13, 2, 18, 7, 16, 8, 17, 9, 12, 0, 5]
        randomIndices = [5, 1, 11, 6, 17, 18, 13,
                         3, 10, 8, 14, 2, 15, 0, 9, 12, 7, 16, 4]

        #print("Re-initialized random board {} times".format(reinitializeCount))

        hexIndex_i = 0  # initialize hexIndex at 0（hexIndex を 0 で初期化する）
        # Neighbors are specified in adjacency matrix - hard coded（隣接行列で指定 - ハードコーディングされています）

        # Generate the hexes and the graphs with the Index, Centers and Resources defined（インデックス、センター、リソースを定義してヘクスとグラフを生成する）
        for rand_i in randomIndices:
            # Get the coordinates of the new hex, indexed by hexIndex_i（hexIndex_iでインデックスされた新しいhexの座標を取得する）
            hexCoords = self.getHexCoords(hexIndex_i)

            # Create the new hexTile with index and append + increment index（新しいhexTileをindexで作成し、append + increment indexする）
            newHexTile = hexTile(
                hexIndex_i, self.resourcesList[rand_i], hexCoords)
            if(newHexTile.resource.type == 'DESERT'):  # Initialize robber on Desert（砂漠で強盗を初期化する）
                newHexTile.robber = True

            self.hexTileDict[hexIndex_i] = newHexTile
            hexIndex_i += 1
            # print(newHexTile.resource.type)
        #print(f"self.hexTileDict: {self.hexTileDict.values()}")
        self.total_hexindex_i = hexIndex_i

        # Create the vertex graph（頂点グラフの作成）
        self.vertexIndexCount = 0  # initialize vertex index count to 0（頂点インデックス数を0に初期化する）
        self.generateVertexGraph()

        self.updatePorts()  # Add the ports to the graph（グラフにポートを追加する）

        # Initialize DevCardStack（DevCardStackの初期化）
        # self.devCardStack = {'KNIGHT': 15, 'VP': 5,
        #                      'MONOPOLY': 2, 'ROADBUILDER': 2, 'YEAROFPLENTY': 2}
        self.devCardStack = {'KNIGHT': 15, 'VP': 5, }

        #print(f"randomIndices: {randomIndices}")
        # self.displayBoardInfo()

        return None

    def getHexCoords(self, hexInd):
        # Dictionary to store Axial Coordinates (q, r) by hexIndex（軸座標(q,r)を hexIndex で格納するための辞書）
        coordDict = {0: Axial_Point(0, 0), 1: Axial_Point(0, -1), 2: Axial_Point(1, -1), 3: Axial_Point(1, 0), 4: Axial_Point(0, 1), 5: Axial_Point(-1, 1), 6: Axial_Point(-1, 0), 7: Axial_Point(0, -2), 8: Axial_Point(1, -2), 9: Axial_Point(2, -2), 10: Axial_Point(2, -1),
                     11: Axial_Point(2, 0), 12: Axial_Point(1, 1), 13: Axial_Point(0, 2), 14: Axial_Point(-1, 2), 15: Axial_Point(-2, 2), 16: Axial_Point(-2, 1), 17: Axial_Point(-2, 0), 18: Axial_Point(-1, -1)}
        return coordDict[hexInd]

    # Function to generate a random permutation of resources（リソースのランダムな並べ替えを生成する関数）
    def getRandomResourceList(self):
        # Define Resources as a dict（リソースをdictで定義する）
        Resource_Dict = {'DESERT': 1, 'ORE': 3,
                         'BRICK': 3, 'WHEAT': 4, 'WOOD': 4, 'SHEEP': 4}
        # Get a random permutation of the numbers（数値のランダムな並べ替えを取得する）
        # NumberList = np.random.permutation(
        #     [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12])
        NumberList = [3, 6, 8, 12, 6, 11, 8,
                      4, 4, 3, 10, 5, 2, 5, 11, 9, 10, 9]
        numIndex = 0

        resourceList = []
        for r in Resource_Dict.keys():
            numberofResource = Resource_Dict[r]
            if(r != 'DESERT'):
                for n in range(numberofResource):
                    resourceList.append(Resource(r, NumberList[numIndex]))
                    numIndex += 1
            else:
                resourceList.append(Resource(r, None))
        #print(f"resourceList: {resourceList}")
        return resourceList

    # Function to check neighboring hexTiles（隣接するhexTilesをチェックする機能）
    # Takes a list of rnadom indices as an input, and the resource list（ランダムなインデックスのリストを入力として受け取り、リソースリスト）
    def checkHexNeighbors(self, randomIndices):
        # store a list of neighbors as per the axial coordinate -> numeric indexing system（軸座標→数値インデックス方式で近傍のリストを格納する。）
        hexNeighborIndexList = {0: [1, 2, 3, 4, 5, 6], 1: [0, 2, 6, 7, 8, 18], 2: [0, 1, 3, 8, 9, 10],
                                3: [0, 2, 4, 10, 11, 12], 4: [0, 3, 5, 12, 13, 14], 5: [0, 4, 6, 14, 15, 16],
                                6: [0, 1, 5, 16, 17, 18], 7: [1, 8, 18], 8: [1, 2, 7, 9],
                                9: [2, 8, 10], 10: [2, 3, 9, 11], 11: [3, 10, 12],
                                12: [3, 4, 11, 13], 13: [4, 12, 14], 14: [4, 5, 13, 15],
                                15: [5, 14, 16], 16: [5, 6, 15, 17], 17: [6, 16, 18], 18: [1, 6, 7, 17]}

        # Check each position, random index pair for its resource roll value（各ポジション、ランダムインデックスペアのリソースロール値を確認する）
        for pos, random_Index in enumerate(randomIndices):
            rollValueOnHex = self.resourcesList[random_Index].num

            # Check each neighbor in the position and check if number is legal（ポジションの各隣接をチェックし、番号が正当であるかどうかを確認します）
            for neighbor_index in hexNeighborIndexList[pos]:
                rollValueOnNeighbor = self.resourcesList[randomIndices[neighbor_index]].num
                if rollValueOnHex in [6, 8] and rollValueOnNeighbor in [6, 8]:
                    return False

        # Return true if it legal for all hexes（すべてのヘクスで有効な場合はtrueを返す）
        return True

    # Function to generate the entire board graph（基板全体のグラフを生成する機能）

    def generateVertexGraph(self):
        for hexTile in self.hexTileDict.values():
            hexTileCorners = polygon_corners(
                self.flat, hexTile.hex)  # Get vertices of each hex（各ヘックスの頂点を取得する）
            # Create vertex graph with this list of corners（このコーナーのリストで頂点グラフを作成する）
            self.updateVertexGraph(hexTileCorners, hexTile.index)

        # Once all hexTiles have been added  get edges（すべてのhexTileが追加されたら、エッジを取得します）
        self.updateGraphEdges()

    # Function to update a graph of the board with each vertex as a node（各頂点をノードとする碁盤のグラフを更新する関数）

    def updateVertexGraph(self, vertexCoordList, hexIndx):
        for v in vertexCoordList:
            # Check if vertex already exists - update adjacentHexList if it does（頂点が既に存在するかどうかをチェックする - 存在する場合は adjacentHexList を更新する）
            if v in self.vertex_index_to_pixel_dict.values():
                for existingVertex in self.boardGraph.keys():
                    if(existingVertex == v):
                        self.boardGraph[v].adjacentHexList.append(hexIndx)

            else:  # Create new vertex if it doesn't exist（頂点が存在しない場合、新しい頂点を作成します）
                #print('Adding Vertex:', v)
                newVertex = Vertex(v, hexIndx, self.vertexIndexCount)
                # Create the index-pixel key value pair
                self.vertex_index_to_pixel_dict[self.vertexIndexCount] = v
                self.boardGraph[v] = newVertex
                self.vertexIndexCount += 1  # Increment index for future（将来のインクリメントインデックス）

    # Function to add adges to graph given all vertices（全頂点が与えられたグラフに頂点を追加する関数）

    def updateGraphEdges(self):
        for v1 in self.boardGraph.keys():
            for v2 in self.boardGraph.keys():
                if(self.vertexDistance(v1, v2) == self.edgeLength):
                    self.boardGraph[v1].edgeList.append(v2)

    @staticmethod
    def vertexDistance(v1, v2):
        dist = ((v1.x - v2.x)**2 + (v1.y - v2.y)**2)**0.5
        return round(dist)

    # View the board graph info（ボードグラフ情報を見る）
    def printGraph(self):
        print(len(self.boardGraph))
        for node in self.boardGraph.keys():
            print("Pixel:{}, Index:{}, NeighborVertexCount:{}, AdjacentHexes:{}".format(
                node, self.boardGraph[node].vertexIndex, len(self.boardGraph[node].edgeList), self.boardGraph[node].adjacentHexList))

    # Update Board vertices with Port info（ポート情報でボードの頂点を更新）
    def updatePorts(self):
        # list of vertex indices of all port pairs（すべてのポートペアの頂点インデックスのリスト）
        port_pair_list = [[43, 44], [33, 34], [45, 49], [27, 53], [
            24, 29], [30, 31], [36, 39], [41, 42], [51, 52]]

        # Get a random permutation of indices of ports（ポートのインデックスのランダムな並べ替えを取得します）
        # randomPortIndices = np.random.permutation(
        #     [i for i in range(len(port_pair_list))])
        randomPortIndices = [8, 5, 6, 7, 1, 0, 4, 3, 2]
        randomPortIndex_counter = 0

        # Initialize port dictionary with counts（ポート辞書をカウント数で初期化する）
        # Also use this dictionary to map vertex indices to specific ports as per the game board（また、この辞書を使用して、ゲームボードに従って、頂点のインデックスを特定のポートにマッピングします）
        port_dict = {'2:1 BRICK': 1, '2:1 SHEEP': 1, '2:1 WOOD': 1,
                     '2:1 WHEAT': 1, '2:1 ORE': 1, '3:1 PORT': 4}

        # Assign random port vertex pairs for each port type（ポートタイプごとにランダムなポート頂点ペアを割り当てる）
        for portType, portVertexPair_count in port_dict.items():
            portVertices = []
            for i in range(portVertexPair_count):  # Number of ports to assign（割り当てるポート数）
                # Add randomized port（ランダムポートの追加）
                portVertices += port_pair_list[randomPortIndices[randomPortIndex_counter]]
                randomPortIndex_counter += 1

            port_dict[portType] = portVertices

        # Iterate thru each port and update vertex info（各ポートを繰り返し、頂点情報を更新する）
        for portType, portVertexIndex_list in port_dict.items():
            for v_index in portVertexIndex_list:  # Each vertex（各頂点）
                # Get the pixel coordinates to update the boardgraph（boardgraphを更新するためのピクセル座標を取得する）
                vertexPixel = self.vertex_index_to_pixel_dict[v_index]
                # Update the port type（ポートタイプの更新）
                self.boardGraph[vertexPixel].port = portType

    # Function to Display Catan Board Info（カタンボード情報表示機能）

    def displayBoardInfo(self):
        for tile in self.hexTileDict.values():
            tile.displayHexInfo()
        return None

    # Function to get the list of potential roads a player can build.（プレイヤーが建設できる道路候補のリストを取得する機能）
    # Return these roads as a dictionary where key=vertex coordinates and values is the rect（これらの道路を，key=頂点座標，values=矩形の辞書として返します）
    def get_potential_roads(self, player):
        colonisableRoads = {}
        # Check potential roads from each road the player already has（プレイヤーが既に持っている各道路から、候補となる道路をチェックする）
        for existingRoad in player.buildGraph['ROADS']:
            for vertex_i in existingRoad:  # Iterate over both vertices of this road（この道路の両頂点に対して反復処理を行う）
                # Check neighbors from this vertex（この頂点からの近傍をチェックする）
                for indx, v_i in enumerate(self.boardGraph[vertex_i].edgeList):
                    # Edge currently does not have a road and vertex isn't colonised by another player（Edgeには現在道路がなく、頂点は他のプレイヤーによって植民地化されていません）
                    if((self.boardGraph[vertex_i].edgeState[indx][1] == False) and (self.boardGraph[vertex_i].state['Player'] in [None, player])):
                        # If the edge isn't already there in both its regular + opposite orientation（エッジが正規の向きと逆の向きの両方で既に存在しない場合）
                        if((v_i, vertex_i) not in colonisableRoads.keys() and (vertex_i, v_i) not in colonisableRoads.keys()):
                            # Use boolean to keep track of potential roads（潜在的な道路を追跡するためにブーリアンを使用します）
                            colonisableRoads[(vertex_i, v_i)] = True
                            #print(vertex_i, v_i)

        return colonisableRoads

    # Function to get available settlements for colonisation for a particular player（特定のプレイヤーが植民地化可能な集落を取得する機能）
    # Return these settlements as a dict of vertices with their Rects（これらの決済を、頂点とそのRectsのディクショナリとして返す）

    def get_potential_settlements(self, player):
        colonisableVertices = {}
        # Check starting from each road the player already has（プレイヤーが既に持っている各道路からチェックする）
        for existingRoad in player.buildGraph['ROADS']:
            for vertex_i in existingRoad:  # Iterate over both vertices of this road（この道路の両頂点に対して反復処理を行う）
                # Check if vertex isn't already in the potential settlements - to remove double checks（頂点が潜在的な解決策にまだ含まれていないかどうかを確認する - 二重チェックをなくすため）
                if(vertex_i not in colonisableVertices.keys()):
                    # Check if this vertex is already colonised（この頂点がすでに植民地化されているかどうかをチェックする）
                    if(self.boardGraph[vertex_i].isColonised):
                        break

                    canColonise = True
                    # Check each of the neighbors from this vertex（この頂点からの各隣接点をチェックする）
                    for v_neighbor in self.boardGraph[vertex_i].edgeList:
                        if(self.boardGraph[v_neighbor].isColonised):
                            canColonise = False
                            break

                # If all checks are good add this vertex and its rect as the value（すべてのチェックに問題がなければ、この頂点とその矩形を値として追加します）
                if(canColonise):
                    #colonisableVertices[vertex_i] = self.draw_possible_settlement(vertex_i, player.color)
                    colonisableVertices[vertex_i] = True

        return colonisableVertices

    # Function to get available cities for colonisation for a particular player（ すべてのチェックに問題がなければ、この頂点とその矩形を値として追加します）
    # Return these cities as a dict of vertex-vertexRect key value pairs（これらの都市を頂点-頂点RECTのキーと値の組のディクショナリとして返す）

    def get_potential_cities(self, player):
        colonisableVertices = {}
        # Check starting from each settlement the player already has（プレイヤーが既に持っている各決済を起点にチェック）
        for existingSettlement in player.buildGraph['SETTLEMENTS']:
            #colonisableVertices[existingSettlement] = self.draw_possible_city(existingSettlement, player.color)
            colonisableVertices[existingSettlement] = True

        return colonisableVertices

    # Special function to get potential first settlements during setup phase（セットアップ時に最初の決済候補を取得する特別な機能）
    def get_setup_settlements(self, player):
        colonisableVertices = {}
        # Check every vertex and every neighbor of that vertex, amd if both are open then we can build a settlement there（すべての頂点とその隣を調べ、両方が開いていれば、そこに集落を作ることができます。）
        for vertexCoord in self.boardGraph.keys():
            canColonise = True
            potentialVertex = self.boardGraph[vertexCoord]
            # First check if vertex is colonised（まず、頂点が植民地化されているかどうかを確認します）
            if(potentialVertex.isColonised):
                canColonise = False

            # Check each neighbor（各隣を確認する）
            for v_neighbor in potentialVertex.edgeList:
                # Check if any of first neighbors are colonised（最初の隣人が植民地化されているかどうかを確認する）
                if(self.boardGraph[v_neighbor].isColonised):
                    canColonise = False
                    break

            if(canColonise):  # If the vertex is colonisable add it to the dict with its Rect（頂点が植民地化可能であれば，そのRectとともにdictに追加する）
                #colonisableVertices[vertexCoord] = self.draw_possible_settlement(vertexCoord, player.color)
                colonisableVertices[vertexCoord] = True

        return colonisableVertices

    # Special function to get potential first roads during setup phase（セットアップ時に最初の道路候補を取得する特別機能）

    def get_setup_roads(self, player):
        colonisableRoads = {}
        # Can only build roads next to the latest existing player settlement（最新のプレイヤー居住地の隣にのみ道路を建設可能）
        latestSettlementCoords = player.buildGraph['SETTLEMENTS'][-1]
        for v_neighbor in self.boardGraph[latestSettlementCoords].edgeList:
            possibleRoad = (latestSettlementCoords, v_neighbor)
            #colonisableRoads[possibleRoad] = self.draw_possible_road(possibleRoad, player.color)
            colonisableRoads[possibleRoad] = True

        return colonisableRoads

    # Function to update boardGraph with Road by player（BoardGraphをRoad by playerで更新する関数）

    def updateBoardGraph_road(self, v_coord1, v_coord2, player):
        # Update edge from first vertex v1（最初の頂点 v1 からのエッジを更新する）
        for indx, v in enumerate(self.boardGraph[v_coord1].edgeList):
            if(v == v_coord2):
                self.boardGraph[v_coord1].edgeState[indx][0] = player
                self.boardGraph[v_coord1].edgeState[indx][1] = True

        # Update edge from second vertex v2（2番目の頂点からの辺を更新する v2）
        for indx, v in enumerate(self.boardGraph[v_coord2].edgeList):
            if(v == v_coord1):
                self.boardGraph[v_coord2].edgeState[indx][0] = player
                self.boardGraph[v_coord2].edgeState[indx][1] = True

        # self.draw_road([v_coord1, v_coord2], player.color) #Draw the settlement

    # Function to update boardGraph with settlement on vertex v（頂点vの決済でboardGraphを更新する関数）

    def updateBoardGraph_settlement(self, v_coord, player):
        self.boardGraph[v_coord].state['Player'] = player
        self.boardGraph[v_coord].state['Settlement'] = True
        self.boardGraph[v_coord].isColonised = True

        # self.draw_settlement(v_coord, player.color) #Draw the settlement

    # Function to update boardGraph with settlement on vertex v（頂点vの決済でboardGraphを更新する関数）
    def updateBoardGraph_city(self, v_coord, player):
        self.boardGraph[v_coord].state['Player'] = player
        self.boardGraph[v_coord].state['Settlement'] = False
        self.boardGraph[v_coord].state['City'] = True

        # Remove settlement from player's buildGraph（プレイヤーのbuildGraphから集落を削除する）
        player.buildGraph['SETTLEMENTS'].remove(v_coord)

    # Function to update boardGraph with Robber on hexTile（hexTile上のRobberでboardGraphを更新する関数です）
    def updateBoardGraph_robber(self, hexIndex):
        # Set all flags to false
        for hex_tile in self.hexTileDict.values():
            hex_tile.robber = False

        self.hexTileDict[hexIndex].robber = True

    # Function to get possible robber hexTiles（強盗の可能性のあるhexTilesを取得する機能）
    # Return robber hex spots with their hexIndex - rect representations as key-value pairs（robber hex spot と hexIndex - rect 表現を key-value ペアとして返します）
    def get_robber_spots(self):
        robberHexDict = {}
        for indx, hex_tile in self.hexTileDict.items():
            if(hex_tile.robber == False):
                #robberHexDict[indx] = self.draw_possible_robber(hex_tile.pixelCenter)
                robberHexDict[indx] = hex_tile

        return robberHexDict

    def get_robber(self):
        for indx, hex_tile in self.hexTileDict.items():
            if(hex_tile.robber == True):
                return indx

    # Get a Dict of players to rob based on the hexIndex of the robber, with the circle Rect as the value（RobberのhexIndexを元に、サークルRectを値として、強盗するプレイヤーのDictを取得する）
    def get_players_to_rob(self, hexIndex):
        # Extract all 6 vertices of this hexTile（hexTile の 6 個の頂点をすべて抽出する）
        hexTile = self.hexTileDict[hexIndex]
        vertexList = polygon_corners(self.flat, hexTile.hex)

        playersToRobDict = {}

        for vertex in vertexList:
            # There is a settlement on this vertex（この頂点には決済がある）
            if(self.boardGraph[vertex].state['Player'] != None):
                playerToRob = self.boardGraph[vertex].state['Player']
                # only add a player once with his/her first settlement/city（最初の居住地/都市で一度だけプレイヤーを追加する）
                if(playerToRob not in playersToRobDict.keys()):
                    #playersToRobDict[playerToRob] = self.draw_possible_players_to_rob(vertex)
                    playersToRobDict[playerToRob] = vertex

        return playersToRobDict

    # Function to get a hexTile with a particular number（特定の番号を持つhexTileを取得する関数）

    def getHexResourceRolled(self, diceRollNum):
        # Empty list to store the hex index rolled (min 1, max 2)（16進インデックスロールを格納する空のリスト (最小値1，最大値2)）
        hexesRolled = []
        for hexTile in self.hexTileDict.values():
            if hexTile.resource.num == diceRollNum:
                hexesRolled.append(hexTile.index)

        return hexesRolled

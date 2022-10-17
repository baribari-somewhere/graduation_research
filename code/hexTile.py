# Settlers of Catan
# Vertex and Hextile class implementation(VertexとHextileクラスの実装)

import collections
from hexLib import *

# Class to implement Catan board Hexagonal Tile(カタン盤六角牌を実装するクラス)
Resource = collections.namedtuple("Resource", ["type", "num"])


class hexTile():
    'Class Definition for Catan Board Hexagonal Tile'

    # Object Creation - specify the resource, num, center and neighbor list(オブジェクトの作成 - リソース、num、センター、ネイバーリストを指定します)
    # Center is a point in axial coordinates q, r and neighborList is a list of hexTiles(Center は軸座標 q, r の点で、neighborList は hexTiles のリストです)
    # hexIndex is a number from 0-18 specifying the Hex's position(hexIndex は Hex の位置を指定する 0-18 の数値)
    def __init__(self, hexIndex, hexResource, axialCoords, neighborList=None):
        self.hex = Axial_Hex(axialCoords)  # Hex representation of this tile
        self.resource = hexResource
        self.coord = axialCoords
        # Pixel coordinates of hex as Point(x, y)(六角形のピクセル座標をPoint(x, y)とする)
        self.pixelCenter = None
        self.index = hexIndex
        self.neighborList = neighborList
        self.robber = False

    # Function to update hex neighbors(hex neighborsの更新機能)
    def updateNeighbors(self):
        return None

    # Function to Display Hex Info(16進数情報を表示する機能)
    def displayHexInfo(self):
        print('Index:{}; Hex:{}; Axial Coord:{}'.format(
            self.index, self.resource, self.coord))
        return None

    # Function to display Hex Neighbors(Hex Neighborsを表示する機能)
    def displayHexNeighbors(self):
        print('Neighbors:')
        for neighbor in self.neighborList:
            neighbor.displayHexInfo()

        return None


# Class definition of a Vertex(Vertexのクラス定義)
class Vertex():

    def __init__(self, pixelCoord, adjHexIndex, vIndex):
        # Index to store vertex info(隣接するVerticesを格納するリスト)
        self.vertexIndex = vIndex
        self.pixelCoordinates = pixelCoord
        # List to store adjacent Vertices(隣接するVerticesを格納するリスト)
        self.edgeList = []
        # List to store indices of 3 adjacent hexes(隣接する3つのヘックスのインデックスを格納するリスト)
        self.adjacentHexList = [adjHexIndex]
        # Nested list to determine if a road is built on edge, and player building road(道路が端に作られているかどうかを判断するための入れ子リスト、および道路を作っているプレイヤー)
        self.edgeState = [[None, False], [None, False], [None, False]]

        self.state = {'Player': None, 'Settlement': False,
                      'City': False}  # Vertex state (バーテックス状態)
        # Add the corresponding port (BRICK, SHEEP, WHEAT, WOOD, ORE, 3:1) later(対応するポート（BRICK、SHEEP、WHEAT、WOOD、ORE、3:1）を後から追加してください)
        self.port = False
        self.isColonised = False

        self.edgeLength = 80  # Specify for hex size(六角サイズに指定する)

    # Function to get a Vertex by its pixel coordinates(ピクセル座標でVertexを取得する関数です)
    def getVertex_fromPixel(self, coords):
        if(self.pixelCoordinates == coords):
            return self

    # Function to return if a vertex v1 is adjacent to another v2(頂点v1が他の頂点v2に隣接しているかどうかを返す関数)
    def isAdjacent(self, v1, v2):
        dist = ((v1.pixelCoordinates.x - v2.pixelCoordinates.x)**2 +
                (v1.pixelCoordinates.y - v2.pixelCoordinates.y)**2)**0.5
        if(round(dist) == self.edgeLength):
            return True

        return False


# Test Code
# testHex = hexTile(0, Resource('Ore', 8), Point(2,3), [hexTile(2, Resource('Wheat', 11), Point(5,6)), hexTile(3, Resource('Brick', 11), Point(7,4))])
# testHex.displayHexInfo()
# testHex.displayHexNeighbors()

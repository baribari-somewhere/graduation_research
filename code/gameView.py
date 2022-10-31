# Settlers of Catan（カタンの開拓者たち）
# Game view class implementation with pygame（pygameによるゲームビュークラスの実装）

import pygame
from hexTile import *
from hexLib import *
import sys

pygame.init()

# Class to handle catan board display（カタンボードディスプレイを扱うクラス）


class catanGameView():
    'Class definition for Catan board display'

    def __init__(self, catanBoardObject, catanGameObject):
        self.board = catanBoardObject
        self.game = catanGameObject

        # #Use pygame to display the board（pygame を使って盤面を表示する）
        self.screen = pygame.display.set_mode(self.board.size)
        pygame.display.set_caption('Settlers of Catan')
        self.font_resource = pygame.font.SysFont('cambria', 15)
        self.font_ports = pygame.font.SysFont('cambria', 10)

        self.font_button = pygame.font.SysFont('cambria', 12)
        self.font_diceRoll = pygame.font.SysFont('cambria', 25)  # dice font
        self.font_Robber = pygame.font.SysFont('arialblack', 50)  # robber font

        return None

    # Function to display the initial board（初期基板を表示する機能）
    def displayInitialBoard(self):
        # Dictionary to store RGB Color values（RGBカラー値を格納する辞書）
        colorDict_RGB = {"BRICK": (255, 51, 51), "ORE": (128, 128, 128), "WHEAT": (
            255, 255, 51), "WOOD": (0, 153, 0), "SHEEP": (51, 255, 51), "DESERT": (255, 255, 204)}
        pygame.draw.rect(self.screen, pygame.Color(
            'royalblue2'), (0, 0, self.board.width, self.board.height))  # blue background（青背景）

        # Render each hexTile（各HexTileをレンダリングする）
        for hexTile in self.board.hexTileDict.values():
            hexTileCorners = polygon_corners(self.board.flat, hexTile.hex)

            hexTileColor_rgb = colorDict_RGB[hexTile.resource.type]
            pygame.draw.polygon(self.screen, pygame.Color(
                hexTileColor_rgb[0], hexTileColor_rgb[1], hexTileColor_rgb[2]), hexTileCorners, self.board.width == 0)
            #print(hexTile.index, hexTileCorners)

            # Get pixel center coordinates of hex（16進数の画素中心座標を取得する）
            hexTile.pixelCenter = hex_to_pixel(self.board.flat, hexTile.hex)
            if(hexTile.resource.type != 'DESERT'):  # skip desert text/number（砂漠のテキスト/番号をスキップする）
                resourceText = self.font_resource.render(str(
                    hexTile.resource.type) + " (" + str(hexTile.resource.num) + ")", False, (0, 0, 0))
                # add text to hex（テキストをHexに追加する）
                self.screen.blit(
                    resourceText, (hexTile.pixelCenter.x - 25, hexTile.pixelCenter.y))

        # Display the Ports - update images/formatting later（ポートの表示 - 後で画像/フォーマットを更新する）
        for vCoord, vertexInfo in self.board.boardGraph.items():
            if(vertexInfo.port != False):
                portText = self.font_ports.render(
                    vertexInfo.port, False, (0, 0, 0))
                #print("Displaying {} port with coordinates x ={} and y={}".format(vertexInfo.port, vCoord.x, vCoord.y))

                if(vCoord.x < 430 and vCoord.y > 130):
                    self.screen.blit(portText, (vCoord.x-50, vCoord.y))
                elif(vCoord.x > 430 and vCoord.y < 130):
                    self.screen.blit(portText, (vCoord.x, vCoord.y-15))
                elif(vCoord.x < 430 and vCoord.y < 130):
                    self.screen.blit(portText, (vCoord.x-50, vCoord.y-15))
                else:
                    self.screen.blit(portText, (vCoord.x, vCoord.y))

        pygame.display.update()

        return None

    # Function to draw a road on the board（ボードに道路を描く機能）
    def draw_road(self, edgeToDraw, roadColor):
        pygame.draw.line(self.screen, pygame.Color(roadColor),
                         edgeToDraw[0], edgeToDraw[1], 10)

    # Function to draw a potential road on the board - thin（基板上に道路候補を描く機能 - 薄型）
    def draw_possible_road(self, edgeToDraw, roadColor):
        roadRect = pygame.draw.line(self.screen, pygame.Color(
            roadColor), edgeToDraw[0], edgeToDraw[1], 5)
        return roadRect

    # Function to draw a settlement on the board at vertexToDraw（vertexToDrawで碁盤上に集落を描画する関数です）
    def draw_settlement(self, vertexToDraw, color):
        newSettlement = pygame.Rect(
            vertexToDraw.x-10, vertexToDraw.y-10, 25, 25)
        pygame.draw.rect(self.screen, pygame.Color(color), newSettlement)

    # Function to draw a potential settlement on the board - thin（ボード上に決済候補を描く機能 - 薄型）
    def draw_possible_settlement(self, vertexToDraw, color):
        possibleSettlement = pygame.draw.circle(self.screen, pygame.Color(
            color), (int(vertexToDraw.x), int(vertexToDraw.y)), 20, 3)
        return possibleSettlement

    # Function to draw a settlement on the board at vertexToDraw（vertexToDrawで碁盤上に集落を描画する関数です）
    def draw_city(self, vertexToDraw, color):
        pygame.draw.circle(self.screen, pygame.Color(
            color), (int(vertexToDraw.x), int(vertexToDraw.y)), 24)

    # Function to draw a potential settlement on the board - thin（ボード上に決済候補を描く機能 - 薄型）
    def draw_possible_city(self, vertexToDraw, color):
        possibleCity = pygame.draw.circle(self.screen, pygame.Color(
            color), (int(vertexToDraw.x), int(vertexToDraw.y)), 25, 5)
        return possibleCity

    # Function to draw the possible spots for a robber（強盗が入りそうな場所を描く機能）
    def draw_possible_robber(self, vertexToDraw):
        possibleRobber = pygame.draw.circle(self.screen, pygame.Color(
            'black'), (int(vertexToDraw.x), int(vertexToDraw.y)), 50, 5)
        return possibleRobber

    # Function to draw possible players to rob（強盗の可能性がある選手を引き寄せる機能）
    def draw_possible_players_to_rob(self, vertexCoord):
        possiblePlayer = pygame.draw.circle(self.screen, pygame.Color(
            'black'), (int(vertexCoord.x), int(vertexCoord.y)), 35, 5)
        return possiblePlayer

    # Function to render basic gameplay buttons（ゲームプレイの基本的なボタンをレンダリングする機能）
    def displayGameButtons(self):
        # Basic GamePlay Buttons（GamePlayの基本ボタン）
        diceRollText = self.font_button.render("ROLL DICE", False, (0, 0, 0))
        buildRoadText = self.font_button.render("ROAD", False, (0, 0, 0))
        buildSettleText = self.font_button.render("SETTLE", False, (0, 0, 0))
        buildCityText = self.font_button.render("CITY", False, (0, 0, 0))
        endTurnText = self.font_button.render("END TURN", False, (0, 0, 0))
        devCardText = self.font_button.render("DEV CARD", False, (0, 0, 0))
        playDevCardText = self.font_button.render(
            "PLAY DEV CARD", False, (0, 0, 0))
        tradeBankText = self.font_button.render(
            "TRADE W/ BANK", False, (0, 0, 0))
        tradePlayersText = self.font_button.render(
            "TRADE W/ PLAYER", False, (0, 0, 0))

        self.rollDice_button = pygame.Rect(20, 10, 80, 40)
        self.buildRoad_button = pygame.Rect(20, 70, 80, 40)
        self.buildSettlement_button = pygame.Rect(20, 120, 80, 40)
        self.buildCity_button = pygame.Rect(20, 170, 80, 40)

        self.devCard_button = pygame.Rect(20, 300, 100, 40)
        self.playDevCard_button = pygame.Rect(20, 350, 100, 40)

        self.tradeBank_button = pygame.Rect(20, 470, 120, 40)
        self.tradePlayers_button = pygame.Rect(20, 520, 120, 40)

        self.endTurn_button = pygame.Rect(20, 700, 80, 40)

        pygame.draw.rect(self.screen, pygame.Color(
            'darkgreen'), self.rollDice_button)
        pygame.draw.rect(self.screen, pygame.Color(
            'gray33'), self.buildRoad_button)
        pygame.draw.rect(self.screen, pygame.Color(
            'gray33'), self.buildSettlement_button)
        pygame.draw.rect(self.screen, pygame.Color(
            'gray33'), self.buildCity_button)
        pygame.draw.rect(self.screen, pygame.Color(
            'gold'), self.devCard_button)
        pygame.draw.rect(self.screen, pygame.Color(
            'gold'), self.playDevCard_button)
        pygame.draw.rect(self.screen, pygame.Color(
            'magenta'), self.tradeBank_button)
        pygame.draw.rect(self.screen, pygame.Color(
            'magenta'), self.tradePlayers_button)

        pygame.draw.rect(self.screen, pygame.Color(
            'burlywood'), self.endTurn_button)

        self.screen.blit(diceRollText, (30, 20))
        self.screen.blit(buildRoadText, (30, 80))
        self.screen.blit(buildSettleText, (30, 130))
        self.screen.blit(buildCityText, (30, 180))
        self.screen.blit(devCardText, (30, 310))
        self.screen.blit(playDevCardText, (30, 360))
        self.screen.blit(tradeBankText, (30, 480))
        self.screen.blit(tradePlayersText, (30, 530))

        self.screen.blit(endTurnText, (30, 710))

    # Function to display robber（強盗を表示する機能）

    def displayRobber(self):
        # Robber text（ロバーテキスト）
        robberText = self.font_Robber.render("R", False, (0, 0, 0))
        # Get the coordinates for the robber（強盗の座標を取得する）
        for hexTile in self.board.hexTileDict.values():
            if(hexTile.robber):
                robberCoords = hexTile.pixelCenter

        self.screen.blit(robberText, (int(robberCoords.x) -
                         20, int(robberCoords.y)-35))

    # Function to display the gameState board - use to display intermediate build screens（gameStateボードを表示する機能 - 中間ビルド画面を表示するために使用します）
    # gameScreenState specifies which type of screen is to be shown（gameScreenStateは、どのタイプの画面を表示するかを指定する）

    def displayGameScreen(self):
        # First display all initial hexes and regular buttons（最初にすべての初期ヘクスとレギュラーボタンを表示する）
        self.displayInitialBoard()
        self.displayGameButtons()
        self.displayRobber()

        # Loop through and display all existing buildings from players build graphs（プレイヤーのビルドグラフからすべての既存ビルをループして表示する）
        # Build Settlements and roads of each player（各プレイヤーの集落や道路を建設する）
        for player_i in list(self.game.playerQueue.queue):
            for existingRoad in player_i.buildGraph['ROADS']:
                self.draw_road(existingRoad, player_i.color)

            for settlementCoord in player_i.buildGraph['SETTLEMENTS']:
                self.draw_settlement(settlementCoord, player_i.color)

            for cityCoord in player_i.buildGraph['CITIES']:
                self.draw_city(cityCoord, player_i.color)

        # pygame.display.update()
        return
        # TO-DO Add screens for trades（TO-DO トレードのための画面を追加する）

    # Function to display dice roll（サイコロの出目を表示する機能）
    def displayDiceRoll(self, diceNums):
        # Reset blue background and show dice roll（ブルーバックのリセットとサイコロの出目表示）
        pygame.draw.rect(self.screen, pygame.Color('royalblue2'),
                         (100, 20, 50, 50))  # blue background（青背景）
        diceNum = self.font_diceRoll.render(str(diceNums), False, (0, 0, 0))
        self.screen.blit(diceNum, (110, 20))

        return None

    def buildRoad_display(self, currentPlayer, roadsPossibleDict):
        '''Function to control build-road action with display
        args: player, who is building road; roadsPossibleDict - possible roads
        returns: road edge of road to be built
        '''
        # Get all spots the player can build a road and display thin lines（プレイヤーが道路を作り、細い線を表示できるスポットをすべて取得する）
        # Get Rect representation of roads and draw possible roads（道路のRect表現を取得し、可能な道路を描画する）
        for roadEdge in roadsPossibleDict.keys():
            if roadsPossibleDict[roadEdge]:
                roadsPossibleDict[roadEdge] = self.draw_possible_road(
                    roadEdge, currentPlayer.color)
                #print("displaying road")

        pygame.display.update()

        # Get player actions until a mouse is clicked（マウスがクリックされるまでのプレイヤーのアクションを取得する）
        mouseClicked = False
        while(mouseClicked == False):
            # during gameSetup phase only exit if road is built（GameSetup期間中、道路が建設された場合のみ終了する）
            if(self.game.gameSetup):
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        sys.exit(0)
                    if(e.type == pygame.MOUSEBUTTONDOWN):
                        for road, roadRect in roadsPossibleDict.items():
                            if(roadRect.collidepoint(e.pos)):
                                #currentPlayer.build_road(road[0], road[1], self.board)
                                mouseClicked = True
                                return road

            else:
                for e in pygame.event.get():
                    # Exit this loop on mouseclick（マウスクリックでこのループを終了する）
                    if(e.type == pygame.MOUSEBUTTONDOWN):
                        for road, roadRect in roadsPossibleDict.items():
                            if(roadRect.collidepoint(e.pos)):
                                #currentPlayer.build_road(road[0], road[1], self.board)
                                return road

                        mouseClicked = True
                        return None

    def buildSettlement_display(self, currentPlayer, verticesPossibleDict):
        '''Function to control build-settlement action with display
        args: player, who is building settlement; verticesPossibleDict - dictionary of possible settlement vertices
        returns: vertex of settlement to be built
        '''
        # Get all spots the player can build a settlement and display thin circles（プレイヤーが集落を作り、薄い円を表示できるスポットをすべて取得する）
        # Add in the Rect representations of possible settlements（和解の可能性を示すRect表現を追加する）
        for v in verticesPossibleDict.keys():
            if verticesPossibleDict[v]:
                verticesPossibleDict[v] = self.draw_possible_settlement(
                    v, currentPlayer.color)

        pygame.display.update()

        # Get player actions until a mouse is clicked（マウスがクリックされるまでのプレイヤーのアクションを取得する）
        mouseClicked = False

        while(mouseClicked == False):
            if(self.game.gameSetup):  # during gameSetup phase only exit if settlement is built（ゲームセットアップ期間中、集落が建設された場合のみ終了する）
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        sys.exit(0)
                    if(e.type == pygame.MOUSEBUTTONDOWN):
                        for vertex, vertexRect in verticesPossibleDict.items():
                            if(vertexRect.collidepoint(e.pos)):
                                #currentPlayer.build_settlement(vertex, self.board)
                                mouseClicked = True
                                return vertex
            else:
                for e in pygame.event.get():
                    # Exit this loop on mouseclick（マウスクリックでこのループを終了する）
                    if(e.type == pygame.MOUSEBUTTONDOWN):
                        for vertex, vertexRect in verticesPossibleDict.items():
                            if(vertexRect.collidepoint(e.pos)):
                                #currentPlayer.build_settlement(vertex, self.board)
                                return vertex

                        mouseClicked = True
                        return None

    def buildCity_display(self, currentPlayer, verticesPossibleDict):
        '''Function to control build-city action with display
        args: player, who is building city; verticesPossibleDict - dictionary of possible city vertices
        returns: city vertex of city to be built
        '''
        # Get all spots the player can build a city and display circles（プレイヤーが街を作り、円を表示できるスポットをすべて取得する）
        # Get Rect representation of roads and draw possible roads（道路のRect表現を取得し、可能な道路を描画する）
        for c in verticesPossibleDict.keys():
            if verticesPossibleDict[c]:
                verticesPossibleDict[c] = self.draw_possible_city(
                    c, currentPlayer.color)

        pygame.display.update()

        mouseClicked = False  # Get player actions until a mouse is clicked - whether a city is built or not（マウスがクリックされるまでのプレイヤーの行動を取得 - 都市が建設されているかどうかに関わらず）

        while(mouseClicked == False):
            for e in pygame.event.get():
                # Exit this loop on mouseclick（マウスクリックでこのループを終了する）
                if(e.type == pygame.MOUSEBUTTONDOWN):
                    for vertex, vertexRect in verticesPossibleDict.items():
                        if(vertexRect.collidepoint(e.pos)):
                            #currentPlayer.build_city(vertex, self.board)
                            return vertex

                    mouseClicked = True
                    return None

    # Function to control the move-robber action with display（ムーブ・ロバーアクションをディスプレイで制御する機能）
    def moveRobber_display(self, currentPlayer, possibleRobberDict):
        # Get all spots the player can move robber to and show circles（プレイヤーが強盗を移動させることができるすべてのスポットを取得し、円を表示する）
        # Add in the Rect representations of possible robber spots（強盗が入りそうな場所をRectで表現する）
        for R in possibleRobberDict.keys():
            possibleRobberDict[R] = self.draw_possible_robber(
                possibleRobberDict[R].pixelCenter)

        pygame.display.update()

        mouseClicked = False  # Get player actions until a mouse is clicked - whether a road is built or not（マウスがクリックされるまでのプレイヤーの行動を取得する - 道路が建設されているかどうかに関わらず）

        while(mouseClicked == False):
            for e in pygame.event.get():
                # Exit this loop on mouseclick（マウスクリックでこのループを終了する）
                if(e.type == pygame.MOUSEBUTTONDOWN):
                    for hexIndex, robberCircleRect in possibleRobberDict.items():
                        if(robberCircleRect.collidepoint(e.pos)):
                            # Add code to choose which player to rob depending on hex clicked on（クリックされたヘクスに応じて、どのプレイヤーを奪うかを選択するコードを追加）
                            possiblePlayerDict = self.board.get_players_to_rob(
                                hexIndex)

                            playerToRob = self.choosePlayerToRob_display(
                                possiblePlayerDict)

                            # Move robber to that hex and rob（そのヘクスに強盗を移動させ、強盗をする）
                            # currentPlayer.move_robber(hexIndex, self.board, playerToRob) #Player moved robber to this hex（プレイヤーが強盗をこのヘクスに移動させた）
                            # Only exit out once a correct robber spot is chosen（正しい強盗スポットが選ばれたときのみ、外に出ることができます）
                            mouseClicked = True
                            return hexIndex, playerToRob

    # Function to control the choice of player to rob with display（ディスプレイでロブするプレーヤーの選択を制御する機能）
    # Returns the choice of player to rob（強盗するプレイヤーの選択肢を返す）
    def choosePlayerToRob_display(self, possiblePlayerDict):
        # Get all other players the player can move robber to and show circles（他のプレイヤーのうち、強盗を移動させることができるプレイヤーをすべて取得し、円を表示します）
        for player, vertex in possiblePlayerDict.items():
            possiblePlayerDict[player] = self.draw_possible_players_to_rob(
                vertex)

        pygame.display.update()

        # If dictionary is empty return None（辞書が空の場合は None を返す）
        if(possiblePlayerDict == {}):
            return None

        mouseClicked = False  # Get player actions until a mouse is clicked - whether a road is built or not（マウスがクリックされるまでのプレイヤーの行動を取得する - 道路が建設されているかどうかに関わらず）
        while(mouseClicked == False):
            for e in pygame.event.get():
                # Exit this loop on mouseclick（マウスクリックでこのループを終了する）
                if(e.type == pygame.MOUSEBUTTONDOWN):
                    for playerToRob, playerCircleRect in possiblePlayerDict.items():
                        if(playerCircleRect.collidepoint(e.pos)):
                            return playerToRob

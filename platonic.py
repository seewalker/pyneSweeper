#
import random
import time
import pygame

class State:
    ONGOING = 0
    GAMEOVER = 1
    VICTORY = 2
class Session:
    def __init__(self):
        self.gameOver = False
        self.CLOCKEVENT = pygame.USEREVENT + 1
        self.sweptSet = set()
        self.adjacency = set()
class gameParams:
    def __init__(self):
        self.EXPERT = 0
        self.DIFFICULT = 1
        self.REGULAR = 2
        self.EASY = 3

        self.EXPERT_HEIGHT = 16
        self.EXPERT_WIDTH = 31
        self.EXPERT_BOMBCOUNT = 120
        self.DIFFICULT_HEIGHT = 16
        self.DIFFICULT_WIDTH = 31
        self.DIFFICULT_BOMBCOUNT = 99
        self.REGULAR_HEIGHT = 14
        self.REGULAR_WIDTH = 22
        self.REGULAR_BOMBCOUNT = 60
        self.EASY_HEIGHT = 12
        self.EASY_WIDTH = 12
        self.EASY_BOMBCOUNT = 24 
class boardParams:
    def __init__(self, gridWidth, gridHeight):
        self.hasBorders = True
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.cellSize = 28
        self.bgColor = (220,255,220,255)
        self.virginCellColor = (238,213,183)
        self.hoverCellColor = (240, 210, 167)
        self.clickedCellColor = (255,239,219)
        self.depressedCellColor = (255,255,255)
        self.gameOverClickedColor = (255,160,160)
        self.gameOverVirginColor = (255,100,100)
        self.victoryClickedColor = (160,160,255)
        self.victoryVirginColor = (100,100,255)
        self.replayButtonColor = (0,0,0)
        #The next four are sizes of the frame pieces.
        self.frameTopSize = 2 * self.cellSize 
        self.frameBottomSize = self.cellSize
        self.frameLeftSize = self.cellSize 
        self.frameRightSize = self.cellSize
        self.boardWidth = self.frameLeftSize + self.cellSize * gridWidth + self.frameRightSize
        self.boardHeight = self.frameTopSize + self.cellSize * gridHeight + self.frameBottomSize
        #The next four are the absolute locations of the frame pieces.
        self.frameTop = self.frameTopSize
        self.frameBottom = self.boardHeight - self.frameBottomSize
        self.frameLeft = self.frameLeftSize
        self.frameRight = self.boardWidth - self.frameRightSize
        self.replayButtonWidth = 2 * self.frameTopSize
        self.replayMessageSize = 14;
        self.replayMessageColor = (255,255,0);
        self.gridGameOverColor = (255,0,0)
        self.gridLineWidth = 2 #what is this in actual coordinates? I could
        #use that value for the BUTTONDOWN rendering
        self.clockPeriod = 1000 # units : milliseconds
        self.clockSize = 48
        self.clockFont = 'freemono'
        self.clockColor = (255,140,80)
        self.countSize = 18
        self.bombSize = 48
        self.bombColor = (0,0,0)
        self.gridRect = (self.frameLeft, self.frameTop, self.frameRight, self.frameBottom)
        self.zeroColor = (102,205,170)
        self.oneColor = (0,0,240)
        self.twoColor = (221,160,221)
        self.threeColor = (240,0,0)
        self.fourColor = (0,0,0)
        self.fiveColor = (218,112,214)
        self.sixColor = (186,85,211)
        self.sevenColor = (253,50,204)
        self.eightColor = (148,0,211)
class essence:
    def __init__(self, mode, player, logfile="scores.log"):
        self.mode = mode
        self.t_naught = time.time()
        self.isTouched = False
        self.isVictorious = False
        self.bombs = set()
        self.numSweeps = 0
        self.player, self.logfile = player, logfile
        GameParams = gameParams()
        if self.mode == GameParams.EXPERT:
            self.height = GameParams.EXPERT_HEIGHT
            self.width = GameParams.EXPERT_WIDTH 
            self.numBombs = GameParams.EXPERT_BOMBCOUNT
        elif  self.mode ==  GameParams.DIFFICULT:
            self.height = GameParams.DIFFICULT_HEIGHT
            self.width = GameParams.DIFFICULT_WIDTH
            self.numBombs = GameParams.DIFFICULT_BOMBCOUNT
        elif self.mode == GameParams.REGULAR:
            self.height = GameParams.REGULAR_HEIGHT
            self.width = GameParams.REGULAR_WIDTH
            self.numBombs = GameParams.REGULAR_BOMBCOUNT
        elif self.mode == GameParams.EASY: 
            self.height = GameParams.EASY_HEIGHT
            self.width = GameParams.EASY_WIDTH
            self.numBombs = GameParams.EASY_BOMBCOUNT
            
    def placeBombs(self, freebee):
        for i in range(self.numBombs):
            placementOverlap = True
            while (placementOverlap):
                bombCoord = (random.randrange(self.width), random.randrange(self.height))
                if bombCoord not in self.bombs and bombCoord != freebee:
                    self.bombs.add(bombCoord)
                    placementOverlap = False

    def isSwept(self):
        if self.numSweeps == self.width * self.height - self.numBombs:
            return True
        else:
            return False

    def sweep(self,coord):
        self.numSweeps += 1
        if not self.isTouched:
            self.placeBombs(coord)
            self.isTouched = True
        if coord in self.bombs: 
            return State.GAMEOVER
        else:
            if self.isSwept():
               return State.VICTORY
            else:
               return State.ONGOING

    def adjacentCells(self, coord):
        x,y = coord
        for i in [(x+1,y),(x+1,y+1),(x,y+1),(x-1,y+1),(x-1,y),(x-1,y-1),(x,y-1),(x+1,y-1)]:
            yield i  

    def numAdjacent(self, coord):
        res = 0
        for i in self.adjacentCells(coord):
            if i in self.bombs:
                res += 1
        return res
   
    def hasAdjacent(self, coord):
        #This can break out of the loop, so it is the time-efficient alternative
        #to using 'numAdjacent(..) == 0'        
        for i in self.adjacentCells(coord):
            if i in self.bombs:
                return True
        return False
   
    def populateAdjacency(self, coord, adjacency, sweptSet):
        for i in self.adjacentCells(coord):
            if 0 <= i[0] < self.width and 0 <= i[1] < self.height:
                if i not in adjacency | sweptSet | self.bombs:
                    if not self.hasAdjacent(i): 
                       adjacency.add(i)
                       self.populateAdjacency(i, adjacency, sweptSet)
                       for j in self.adjacentCells(i): 
                           if 0 <= j[0] < self.width and 0 <= j[1] < self.height: 
                               if j not in adjacency | sweptSet | self.bombs:
                                   adjacency.add(j)
        return adjacency
   
    def saveResults(self, tFinal):
        fh = open(self.logfile, 'a')
        fh.write(self.player + " " + repr(self.mode) + " " + repr(self.numSweeps) + " " +
                repr(int(tFinal - self.t_naught)) + "\n")
        fh.close()

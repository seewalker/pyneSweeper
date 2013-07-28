#!/usr/bin/python
import sys
import pygame
import time
from pygame.locals import *
import platonic

def mapToList(x,y):
    return ((x / setting.cellSize) - (setting.frameLeft / setting.cellSize), (y / setting.cellSize) - (setting.frameTop / setting.cellSize))
def mapToCell(x,y):
    return (x - x % setting.cellSize, y - y % setting.cellSize)
def colorMap(numAdjacent):
    if (numAdjacent == 0):
        return setting.zeroColor
    elif (numAdjacent == 1):
        return setting.oneColor
    elif (numAdjacent == 2):
        return setting.twoColor
    elif (numAdjacent == 3):
        return setting.threeColor
    elif (numAdjacent == 4):
        return setting.fourColor
    elif (numAdjacent == 5):
        return setting.fiveColor
    elif (numAdjacent == 6):
        return setting.sixColor
    elif (numAdjacent == 7):
        return setting.sevenColor
    elif (numAdjacent == 8):
        return setting.eightColor
    else:
        return "numAdjacent out of range"
def clickWithinBounds(x,y):
    if setting.frameLeft <= x <= setting.frameRight and setting.frameTop <= y <= setting.frameBottom:
        return True
    else:
        return False
def clickWithinReplayButton(x,y):
    return 0 < x < setting.replayButtonWidth and 0 < y < frameTopSize
def drawClock():
    reading = int(time.time()) - int(soul.t_naught) #unit: seconds
    if not pygame.font.get_init():
        print("Font module is not initialized")
        sys.exit()
    else:
        fontObj = pygame.font.SysFont(setting.clockFont, setting.clockSize)
        clockObj = fontObj.render(repr(reading), True, setting.clockColor)
        clockRect = (setting.boardWidth - clockObj.get_width(), 0, setting.boardWidth, clockObj.get_height())      
        SURFACE.fill(setting.bgColor, clockRect) 
        SURFACE.blit(clockObj, clockRect)
def drawCells(state):
    SURFACE.fill(setting.bgColor, setting.gridRect)
    if setting.hasBorders or state == State.GAMEOVER:
        offset = setting.gridLineWidth
    else:
        offset = 0
    for i in range(setting.gridWidth):
        for j in range(setting.gridHeight):
            digitObj, bombObj = None, None
            cornerX = setting.frameLeft + i * setting.cellSize + offset
            cornerY = setting.frameTop + j * setting.cellSize + offset
            myCell = Rect(cornerX,cornerY, setting.cellSize - offset ,setting.cellSize - offset) 
            if state == State.ONGOING:
                if (i,j) in Session.sweptSet:
                    cellColor = setting.clickedCellColor
                    fontObj = pygame.font.SysFont('helvetica', setting.countSize) 
                    adjacency = soul.numAdjacent((i,j))
                    digitObj = fontObj.render(repr(adjacency), True, colorMap(adjacency))
                else:
                    cellColor = setting.virginCellColor
            elif state == State.GAMEOVER:
                if (i,j) in Session.sweptSet:
                   cellColor = setting.gameOverClickedColor
                else:
                   cellColor = setting.gameOverVirginColor
                if (i,j) in soul.bombs:
                   fontObj = pygame.font.SysFont('helvetica', setting.bombSize)
                   bombObj = fontObj.render("*", True, setting.bombColor)
            elif state == State.VICTORY:
                if (i,j) in Session.sweptSet:
                    cellColor = setting.victoryClickedColor
                else:
                    cellColor = setting.victoryVirginColor
                if (i,j) in soul.bombs:
                    fontObj = pygame.font.SysFont('helvetica', setting.bombSize)
                    bombObj = fontObj.render("*", True, setting.bombColor)
            SURFACE.fill(cellColor, myCell) #this is unconditional.
            if digitObj:
               digitPos = digitObj.get_rect() 
               digitPos.centerx = myCell.centerx
               digitPos.centery = myCell.centery
               SURFACE.blit(digitObj, digitPos)
            if bombObj:
               bombPos = bombObj.get_rect()
               bombPos.centerx = myCell.centerx
               bombPos.centery = myCell.centery + 0.4 * setting.cellSize 
               SURFACE.blit(bombObj, bombPos)

#Execution of program starts here.
GameParams = platonic.gameParams()
State = platonic.State() 
Session = platonic.Session()
try:
    if len(sys.argv ) < 2:
        raise IOError
    else:
        playerName = sys.argv[1]
    if sys.argv[2].lower() == "expert" or sys.argv[2] == GameParams.EXPERT:
        theMode = GameParams.EXPERT
    elif sys.argv[2].lower() == "difficult" or sys.argv[2] == GameParams.DIFFICULT:
        theMode = GameParams.DIFFICULT
    elif sys.argv[2].lower() == "regular" or sys.argv[2] == GameParams.REGULAR:
        theMode = GameParams.REGULAR
    elif sys.argv[2].lower() == "easy" or sys.argv[2] == GameParams.EASY:
        theMode = GameParams.EASY
    else:
        raise IOError
except IOError:
    print("Enter your name as the first argument")
    print("Enter one of four difficulties as the 2nd argument: expert, difficult,regular, or easy")
    sys.exit()
soul = platonic.essence(theMode, playerName)
setting = platonic.boardParams(soul.width, soul.height)
pygame.init()
pygame.mixer.quit() #necessary because sound underruns keep occuring
SURFACE = pygame.display.set_mode((setting.boardWidth, setting.boardHeight))
pygame.display.set_caption('')
pygame.time.set_timer(Session.CLOCKEVENT, setting.clockPeriod)
SURFACE.fill(setting.bgColor)
drawCells(State.ONGOING)
while not Session.gameOver:
    for event in pygame.event.get():
        if event.type == Session.CLOCKEVENT and not Session.gameOver:
            drawClock()
        if event.type == pygame.MOUSEBUTTONUP and clickWithinBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            listCoord = mapToList(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            if listCoord not in Session.sweptSet: 
                state = soul.sweep(listCoord)
                #The set of swept cells is maintained so that the recursive-zero
                #-sweeping does not sweep any one cell twice. That would lead
                #to a premature victory.
                Session.sweptSet.add(listCoord)
            if not soul.hasAdjacent(listCoord):
                Session.adjacency = soul.populateAdjacency(listCoord, set(), Session.sweptSet)
                for i in (Session.adjacency - Session.sweptSet): 
                    state = soul.sweep(i)
                    Session.sweptSet.add(i)
            drawCells(state)
            if state != State.ONGOING:
                soul.saveResults(time.time())
                drawCells(state)
                pygame.display.flip() 
                Session.gameOver = True
        if event.type == pygame.MOUSEMOTION:
            if True in pygame.mouse.get_pressed():
                drawCells(State.ONGOING)
                mouseX, mouseY = pygame.mouse.get_pos()
                cellX, cellY = mapToCell(mouseX,mouseY)
                myCell = Rect(cellX,cellY,setting.cellSize,setting.cellSize)
                SURFACE.fill(setting.hoverCellColor, myCell)
        if event.type == pygame.MOUSEBUTTONDOWN and clickWithinBounds(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            mouseX, mouseY = pygame.mouse.get_pos()
            cellX, cellY = mapToCell(mouseX,mouseY)
            myCell = Rect(cellX,cellY,setting.cellSize,setting.cellSize)
            SURFACE.fill(setting.hoverCellColor, myCell)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip() 
while Session.gameOver:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                sys.exit()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

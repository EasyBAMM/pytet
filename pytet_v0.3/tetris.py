from matrix import *
from random import *
from enum import Enum
#import LED_display as LMD


class TetrisState(Enum):
    Running = 0
    NewBlock = 1
    Finished = 2
# end of class TetrisState():


class Tetris():
    nBlockTypes = 0
    nBlockDegrees = 0
    setOfBlockObjects = 0
    iScreenDw = 0   # larget enough to cover the largest block

    @classmethod
    def init(cls, setOfBlockArrays):
        Tetris.nBlockTypes = len(setOfBlockArrays)
        Tetris.nBlockDegrees = len(setOfBlockArrays[0])
        Tetris.setOfBlockObjects = [
            [0] * Tetris.nBlockDegrees for _ in range(Tetris.nBlockTypes)]
        arrayBlk_maxSize = 0
        for i in range(Tetris.nBlockTypes):
            if arrayBlk_maxSize <= len(setOfBlockArrays[i][0]):
                arrayBlk_maxSize = len(setOfBlockArrays[i][0])
        # larget enough to cover the largest block
        Tetris.iScreenDw = arrayBlk_maxSize

        for i in range(Tetris.nBlockTypes):
            for j in range(Tetris.nBlockDegrees):
                Tetris.setOfBlockObjects[i][j] = Matrix(setOfBlockArrays[i][j])
        return

    def createArrayScreen(self):
        self.arrayScreenDx = Tetris.iScreenDw * 2 + self.iScreenDx
        self.arrayScreenDy = self.iScreenDy + Tetris.iScreenDw
        self.arrayScreen = [
            [0] * self.arrayScreenDx for _ in range(self.arrayScreenDy)]
        for y in range(self.iScreenDy):
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][x] = 1
            for x in range(self.iScreenDx):
                self.arrayScreen[y][Tetris.iScreenDw + x] = 0
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][Tetris.iScreenDw + self.iScreenDx + x] = 1

        for y in range(Tetris.iScreenDw):
            for x in range(self.arrayScreenDx):
                self.arrayScreen[self.iScreenDy + y][x] = 1

        return self.arrayScreen

    def __init__(self, iScreenDy, iScreenDx):
        self.iScreenDy = iScreenDy
        self.iScreenDx = iScreenDx
        self.idxBlockDegree = 0
        arrayScreen = self.createArrayScreen()
        self.iScreen = Matrix(arrayScreen)
        self.oScreen = Matrix(self.iScreen)
        self.justStarted = True
        return

    def printScreen(self):
        array = self.oScreen.get_array()

        for y in range(self.oScreen.get_dy()-Tetris.iScreenDw):
            for x in range(Tetris.iScreenDw, self.oScreen.get_dx()-Tetris.iScreenDw):
                if array[y][x] == 0:
                    print("□", end='')
                    #LMD.set_pixel(y, 19-x, 0)
                elif array[y][x] == 1:
                    print("■", end='')
                    #LMD.set_pixel(y, 19-x, 4)
                else:
                    print("XX", end='')
                    # continue
            print()

    def deleteFullLines(self):  # To be implemented!!
        checkRange = self.currBlk.get_dy()

        if self.top + self.currBlk.get_dy() >= self.iScreenDy:
            checkRange = self.iScreenDy - self.top

        # get blankLine
        arrayScreen = self.createArrayScreen()
        new_fullScreen = Matrix(arrayScreen)
        blankLine = new_fullScreen.clip(0, 0, 1, new_fullScreen.get_dx())

        # check line start from bottom
        remove = 0
        for i in reversed(range(checkRange)):
            checkLayer = self.top + i + remove
            line = self.oScreen.clip(
                checkLayer, 0, checkLayer + 1, self.oScreen.get_dx())
            if line.sum() == self.oScreen.get_dx():  # line.sum is equal to width
                temp = self.oScreen.clip(
                    0, 0, checkLayer, self.oScreen.get_dx())
                self.oScreen.paste(temp, 1, 0)
                self.oScreen.paste(blankLine, 0, 0)
                remove += 1

        return self.oScreen

    def accept(self, key):  # To be implemented!!
        if self.justStarted == True:  # key is num
            self.state = TetrisState.NewBlock

            self.top = 0
            self.left = Tetris.iScreenDw + self.iScreenDx//2 - 2
            self.idxBlockType = int(key)  # 블록 타입 번호 갱신
            self.idxBlockDegree = 0
            self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
            self.tempBlk = self.iScreen.clip(
                self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
            self.tempBlk = self.tempBlk + self.currBlk
            print()

            if self.tempBlk.anyGreaterThan(1):
                self.state = TetrisState.Finished
                self.oScreen = Matrix(self.iScreen)
                return self.state

            self.oScreen = Matrix(self.iScreen)
            self.oScreen.paste(self.tempBlk, self.top, self.left)

            self.justStarted = False

            return self.state
        else:  # key is 'a', 'd', 's', 'w'
            self.state = TetrisState.Running

            if key == 'a':  # move left
                self.left -= 1
            elif key == 'd':  # move right
                self.left += 1
            elif key == 's':  # move down
                self.top += 1
            elif key == 'w':  # rotate the block clockwise
                self.idxBlockDegree = (
                    self.idxBlockDegree + 1) % Tetris.nBlockDegrees
            elif key == ' ':  # drop the block
                while self.tempBlk.anyGreaterThan(1) is False:
                    self.top += 1
                    self.tempBlk = self.iScreen.clip(
                        self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
                    self.tempBlk = self.tempBlk + self.currBlk
            else:
                print('Wrong key!!!')

            self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
            self.tempBlk = self.iScreen.clip(
                self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
            self.tempBlk = self.tempBlk + self.currBlk
            print()

            if self.tempBlk.anyGreaterThan(1):
                if key == 'a':  # undo: move right
                    self.left += 1
                elif key == 'd':  # undo: move left
                    self.left -= 1
                elif key == 's':  # undo: move up
                    self.top -= 1
                    self.state = TetrisState.NewBlock
                elif key == 'w':  # undo: rotate the block counter-clockwise
                    self.idxBlockDegree = (
                        self.idxBlockDegree - 1) % Tetris.nBlockDegrees
                elif key == ' ':  # undo: move up
                    self.top -= 1
                    self.state = TetrisState.NewBlock

            self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
            self.tempBlk = self.iScreen.clip(
                self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
            self.tempBlk = self.tempBlk + self.currBlk
            print()

            self.oScreen = Matrix(self.iScreen)
            self.oScreen.paste(self.tempBlk, self.top, self.left)

            if self.state == TetrisState.NewBlock:
                self.oScreen = self.deleteFullLines()
                self.iScreen = Matrix(self.oScreen)
                self.top = 0
                self.left = Tetris.iScreenDw + self.iScreenDx//2 - 2
                self.idxBlockDegree = 0
                self.justStarted = True

            if self.tempBlk.anyGreaterThan(1):
                self.state = TetrisState.Finished
                self.oScreen = Matrix(self.iScreen)

            return self.state

# end of class Tetris():

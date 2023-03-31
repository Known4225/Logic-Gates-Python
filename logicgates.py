import turtle as t
from turtletools import turtleTools
import math as m
'''
Windows:
Shift key - turtools.keyPressed(16) (this is 7 on linux)
Space key - turtools.keyPressed(32) (this is o on linux)
Up arrow - turtools.keyPressed(38) (this is a on linux (problem))
Left arrow - turtools.keyPressed(37) (this is ctrl on linux)
Right arrow - turtools.keyPressed(39) (this is s on linux (problem))
Down arrow - turtools.keyPressed(40) (this is d on linux)

Linux:
Shift key - turtools.keyPressed(50) (this is ___ on windows)
Space key - turtools.keyPressed(65) (this is ___ on windows)
Up arrow - turtools.keyPressed(111) (this is ___ on windows)
Left arrow - turtools.keyPressed(113) (this is ___ on windows)
Right arrow - turtools.keyPressed(114) (this is ___ on windows)
Down arrow - turtools.keyPressed(116) (this is ___ on windows)
'''
global globalsize, turtools, themeColors
globalsize = 1.5
t.setup(960, 720)
t.colormode(255)
t.title("Logic Gates")
tps = 'inf' #set this to a different number to change the ticks per second, this changes things like how fast the scroll and rotate features work
turtools = turtleTools(t.getcanvas(), -240, -180, 240, 180, True)
themeColors = ['null', 0, 0, 0, 195, 195, 195, 255, 0, 0, 255, 146, 146, 230, 230, 230, 95, 95, 95, 255, 234, 0, 255, 248, 181, 255, 255, 255,
100, 100, 100, 195, 195, 195, 74, 198, 174, 155 ,199, 190, 50, 50, 50, 200, 200, 200, 136, 203, 213, 145, 207, 214, 30, 30, 30]
class master:
    def __init__(self):
        # light theme = 0, dark theme = 27
        self.theme = 0
        t.Screen().bgcolor(themeColors[25 + self.theme], themeColors[26 + self.theme], themeColors[27 + self.theme])
        self.sp = t.Turtle()
        self.sp.hideturtle()
        self.sp.penup()
        self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
        self.sp.shape('circle')
        self.scrollSpeed = 1 #this also changes the scroll speed
        self.rotateSpeed = 1 #this also changes the rotate speed
        self.rotateCooldown = 1
        self.mx = 0
        self.my = 0
        self.scaling = 2
        self.sidebar = 1
        self.GraphPrez = 12
        self.holding = 0
        self.holdingAng = 90
        self.indicators = 1
        self.mouseType = 0
        self.mouseMode = 0
        self.wxOffE = 0
        self.wyOffE = 0
        # self.tempAng = 0
        # self.tempAng2 = 0
        # self.tempAng3 = 0
        self.CSX = 0
        self.CSY = 0
        self.sxmax = 0
        self.sxmin = 0
        self.symax = 0
        self.symin = 0
        self.selecting = 0
        self.Cscl = 1
        self.hlgcomp = 0
        self.hglmove = 0
        self.tempX = 0
        self.tempY = 0
        self.offX = 0
        self.offY = 0
        self.FocalX = 0
        self.FocalY = 0
        self.FocalCSX = 0
        self.FocalCSY = 0
        self.selectX = 0
        self.selectY = 0
        self.wireHold = 0
        self.wiringStart = 0
        self.wiringEnd = 0
        self.components = ['null']
        self.compSlots = ['null', 'POWER', 1, 'NOT', 1, 'AND', 2, 'OR', 2, 'XOR', 2, 'NOR', 2, 'NAND', 2, 'BUFFER', 1]
        self.deleteQueue = ['null']
        self.inpComp = ['null']
        self.io = ['null']
        self.keys = ['null']
        self.bufferFrames = 1
        self.positions = ['null']
        self.selected = ['null']
        self.selectOb = ['null']
        self.wiring = ['null']
        self.wireTemp = ['null']
        self.sinRot = 0
        self.cosRot = 0
    def tick(self):
        t.setworldcoordinates(-240, -180, 240, 180)
        hp = turtools.height / 360
        wd = turtools.width / 480
        if hp > wd:
            self.scaling = wd
        else:
            self.scaling = hp
        self.mx, self.my = turtools.getMouseCoords()
        self.mw = turtools.mouseWheel()
        self.linuxMouse = 0
        if self.keys.count("up"):
            self.linuxMouse += 1
        if self.keys.count("down"):
            self.linuxMouse -= 1
        self.sp.clear()
        self.renderComp()
        self.renderWire(globalsize)
        self.renderSidebar(self.sidebar)
        self.hlgcompset()
        self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
        if self.holding == "POWER":
            self.POWER(self.mx, self.my, globalsize, self.holdingAng, 0, 0)
        if self.holding == "AND":
            self.AND(self.mx, self.my, globalsize, self.holdingAng)
        if self.holding == "OR":
            self.OR(self.mx, self.my, globalsize, self.holdingAng)
        if self.holding == "NOT":
            self.NOT(self.mx, self.my, globalsize, self.holdingAng)
        if self.holding == "XOR":
            self.XOR(self.mx, self.my, globalsize, self.holdingAng)
        if self.holding == "NOR":
            self.NOR(self.mx, self.my, globalsize, self.holdingAng)
        if self.holding == "NAND":
            self.NAND(self.mx, self.my, globalsize, self.holdingAng)
        if self.holding == "BUFFER":
            self.BUFFER(self.mx, self.my, globalsize, self.holdingAng)
        if ((turtools.keyPressed(39) or turtools.keyPressed(114)) and not turtools.keyPressed('s')):
            if not self.holding == 0 and not self.holding == 1:
                self.holdingAng += 0.5 * self.rotateSpeed
            else:
                if self.selecting > 1:
                    if self.keys.count("space") > 0:
                        self.rotateSelected(-0.5 * self.rotateSpeed)
                    else:
                        i = 1
                        for j in range(len(self.selected) - 1):
                            self.positions[self.selected[i] * 3] += 0.5 * self.rotateSpeed
                            if self.positions[self.selected[i] * 3] > 360:
                                self.positions[self.selected[i] * 3] -=360
                            i += 1
                else:
                    if not self.hlgcomp == 0:
                        self.positions[self.hlgcomp * 3] += 0.5 * self.rotateSpeed
                        if self.positions[self.hlgcomp * 3] > 360:
                            self.positions[self.hlgcomp * 3] -= 360
        if (turtools.keyPressed(37) or turtools.keyPressed(113)):
            if not self.holding == 0 and not self.holding == 1:
                self.holdingAng -= 0.5 * self.rotateSpeed
            else:
                if self.selecting > 1:
                    # space key
                    if self.keys.count("space") > 0:
                        self.rotateSelected(0.5 * self.rotateSpeed)
                    else:
                        i = 1
                        for j in range(len(self.selected) - 1):
                            self.positions[self.selected[i] * 3] -=  0.5 * self.rotateSpeed
                            if self.positions[self.selected[i] * 3] < 0:
                                self.positions[self.selected[i] * 3] += 360
                            i += 1
                else:
                    if not self.hlgcomp == 0:
                        self.positions[self.hlgcomp * 3] -= 0.5 * self.rotateSpeed
                        if self.positions[self.hlgcomp * 3] < 0:
                            self.positions[self.hlgcomp * 3] += 360
        self.mouseTick()
    def mouseTick(self):
        if turtools.mouseDown():
            if not self.keys.count("mouse") > 0:
                self.keys.append("mouse")
                self.keys.append(0) #buffer frames (0 on mouse since this problem does not exist on mouse events)
                if self.mx > self.boundXmin and self.mx < self.boundXmax and self.my > self.boundYmin and self.my < self.boundYmax:
                    self.mouseType = 0
                    if not self.selecting == 2 and not self.selected.count(self.hlgcomp) > 0 and not ((self.keys.count("space") > 0 or self.wireHold == 1) and not self.hlgcomp == 0):
                        self.wireHold = 0
                        self.selecting = 0
                        self.selectOb = ['null']
                        self.selected = ['null']
                    if self.keys.count('s') > 0 or (turtools.keyPressed(16) or turtools.keyPressed(50)):
                        if self.holding == 0 or self.holding == 1:
                            self.selecting = 1
                            self.selectOb = ['null']
                            self.selectX = self.mx
                            self.selectY = self.my
                        else:
                            self.components.append(self.holding)
                            self.positions.append(self.mx * self.Cscl + self.CSX)
                            self.positions.append(self.my * self.Cscl + self.CSY)
                            self.positions.append(self.holdingAng)
                            for i in range(3):
                                self.io.append(0)
                            self.inpComp.append(self.compSlots[self.compSlots.index(self.holding) + 1])
                            for i in range(2):
                                self.io.append(0)
                            self.holding = 1
                            # updateUNDO
                    else:
                        if self.holding == 0 or self.holding == 1:
                            if not self.hlgcomp == 0:
                                if self.keys.count("space") > 0 or self.wireHold == 1:
                                    self.wiringStart = self.hlgcomp
                                else:
                                    self.hglmove = self.hlgcomp
                                    self.tempX = self.positions[self.hglmove * 3 - 2]
                                    self.tempY = self.positions[self.hglmove * 3 - 1]
                                    self.offX = self.positions[self.hglmove * 3 - 2] - (self.mx * self.Cscl + self.CSX)
                                    self.offY = self.positions[self.hglmove * 3 - 1] - (self.my * self.Cscl + self.CSY)
                                if self.selectOb.count(self.hlgcomp) > 0:
                                    if self.selecting == 2:
                                        self.selecting = 3
                                        i = 1
                                        self.selected = ['null']
                                        for j in range(len(self.selectOb) - 1):
                                            self.selected.append(self.selectOb[i])
                                            i += 1
                                else:
                                    if not self.selecting == 3 and not (self.keys.count("space") > 0 or self.wireHold == 1 and not self.hlgcomp == 0):
                                        self.wireHold = 0
                                        self.selecting = 0
                                        self.selectOb = ['null']
                                        self.selected = ['null']
                            if self.holding == 1:
                                self.holding = 0
                        else:
                            self.components.append(self.holding)
                            self.positions.append(self.mx * self.Cscl + self.CSX)
                            self.positions.append(self.my * self.Cscl + self.CSY)
                            self.positions.append(self.holdingAng)
                            for i in range(3):
                                self.io.append(0)
                            self.inpComp.append(self.compSlots[self.compSlots.index(self.holding) + 1])
                            for i in range(2):
                                self.inpComp.append(0)
                            self.holding = 1
                            # updateUNDO
                        self.FocalX = self.mx
                        self.FocalY = self.my
                        self.FocalCSX = self.CSX
                        self.FocalCSY = self.CSY
                        if not self.selecting == 3 and not (self.keys.count("space") > 0 or self.wireHold == 1 and not self.hlgcomp == 0):
                            self.wireHold = 0
                            self.selecting = 0
                            self.selectOb = ['null']
                            self.selected = ['null']
                else:
                    self.mouseType = 1
                    self.FocalX = self.mx
                    self.FocalY = self.my
                    self.FocalCSX = self.CSX
                    self.FocalCSY = self.CSY
                    self.selecting = 0
                    self.sxmax = 0
                    self.symax = 0
                    self.sxmin = 0
                    self.symin = 0
                    self.selectOb = ['null']
                    self.selected = ['null']
                    if self.mx > 168:
                        if self.wireHold == 1:
                            self.wireHold = 0
                        else:
                            self.wireHold = 1
                    else:
                        if self.holding == self.compSlots[round((self.mx + 245) / 48) * 2 - 1]:
                            self.holding = 0
                        else:
                            self.holding = self.compSlots[round((self.mx + 245) / 48) * 2 - 1]
            if self.mouseType == 1 and self.mx > self.boundXmin and self.mx < self.boundXmax and self.my > self.boundYmin and self.my < self.boundYmax:
                self.mouseType = 2
            if (self.keys.count('s') > 0 or (turtools.keyPressed(16) or turtools.keyPressed(50))) and self.selecting == 1:
                self.selectX2 = self.mx
                self.selectY2 = self.my
                self.selectionBox(self.selectX, self.selectY, self.selectX2, self.selectY2)
                if abs(self.selectX - self.mx) > 4 or abs(self.selectY - self.my) > 4:
                    self.selected = ['null']
                    self.selectOb = ['null']
                else:
                    if self.selected.count(self.hlgcomp) > 0:
                        self.sxmax = 0
                        self.symax = 0
                        self.sxmin = 0
                        self.symin = 0
                        if not self.deleteQueue.count(self.hlgcomp) > 0:
                            self.deleteQueue.append(self.hlgcomp)
            else:
                if self.selecting == 1:
                    self.FocalX = self.mx
                    self.FocalY = self.my
                    self.FocalCSX = self.CSX
                    self.FocalCSY = self.CSY
                    self.selecting = 0
                    self.sxmax = 0
                    self.symax = 0
                    self.sxmin = 0
                    self.symin = 0
                if (self.keys.count("space") > 0 or self.wireHold == 1) and not self.wiringStart == 0:
                    if self.selected.count(self.wiringStart) > 0 or self.selected.count(self.hlgcomp) > 0:
                        self.sp.pencolor(themeColors[4 + self.theme], themeColors[5 + self.theme], themeColors[6 + self.theme])
                    else:
                        self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
                    self.sp.pensize(globalsize * 2 * self.scaling)
                    if self.selected.count(self.wiringStart) > 0 and self.selecting > 2:
                        i = 1
                        for j in range(len(self.selected) - 1):
                            self.sp.goto((self.positions[self.selected[i] * 3 - 2] - self.CSX) / self.Cscl, (self.positions[self.selected[i] * 3 - 1] - self.CSY) / self.Cscl)
                            self.sp.pendown()
                            if (not self.hlgcomp == 0 and not self.hlgcomp == self.wiringStart) and (self.inpComp[self.wiringEnd * 3 - 1] == 0 or (self.inpComp[self.wiringEnd * 3] == 0 and not self.inpComp[self.wiringEnd * 3 - 1] == self.wiringStart and self.inpComp[self.wiringEnd * 3 - 2] > 1)):
                                self.sp.goto((self.positions[self.hlgcomp * 3 - 2] - self.CSX) / self.Cscl, (self.positions[self.hlgcomp * 3 - 1] - self.CSY) / self.Cscl)
                            else:
                                self.sp.goto(self.mx, self.my)
                            self.sp.penup() 
                            i += 1
                    else:
                        if self.selected.count(self.hlgcomp) > 0 and self.selecting > 1:
                            i = 1
                            for j in range(len(self.selected) - 1):
                                self.sp.goto((self.positions[self.wiringStart * 3 - 2] - self.CSX) / self.Cscl, (self.positions[self.wiringStart * 3 - 1] - self.CSY) / self.Cscl)
                                self.sp.pendown()
                                self.sp.goto((self.positions[self.selected[i] * 3 - 2] - self.CSX) / self.Cscl, (self.positions[self.selected[i] * 3 - 1] - self.CSY) / self.Cscl)
                                self.sp.penup()
                                i += 1
                        else:
                            self.sp.goto((self.positions[self.wiringStart * 3 - 2] - self.CSX) / self.Cscl, (self.positions[self.wiringStart * 3 - 1] - self.CSY) / self.Cscl)
                            self.sp.pendown()
                            if (not self.hlgcomp == 0 and not self.hlgcomp == self.wiringStart) and (self.inpComp[self.wiringEnd * 3 - 1] == 0 or (self.inpComp[self.wiringEnd * 3] == 0 and not self.inpComp[self.wiringEnd * 3 - 1] == self.wiringStart and self.inpComp[self.wiringEnd * 3 - 2] > 1)):
                                self.sp.goto((self.positions[self.hlgcomp * 3 - 2] - self.CSX) / self.Cscl, (self.positions[self.hlgcomp * 3 - 1] - self.CSY) / self.Cscl)
                            else:
                                self.sp.goto(self.mx, self.my)
                            self.sp.penup()
                if self.hglmove == 0:
                    if self.keys.count("space") > 0 or self.wireHold == 1:
                        self.FocalX = self.mx
                        self.FocalY = self.my
                        self.FocalCSX = self.CSX
                        self.FocalCSY = self.CSY
                        self.wiringEnd = self.hlgcomp
                    else:
                        if self.holding == 0:
                            self.CSX = (self.FocalX - self.mx) * self.Cscl + self.FocalCSX
                            self.CSY = (self.FocalY - self.my) * self.Cscl + self.FocalCSY
                else:
                    if self.selecting == 3:
                        anchorX = self.positions[self.hglmove * 3 - 2]
                        anchorY = self.positions[self.hglmove * 3 - 1]
                        i = 1
                        for j in range(len(self.selected) - 1):
                            self.positions[self.selected[i] * 3 - 2] += self.mx * self.Cscl + self.CSX + self.offX - anchorX
                            self.positions[self.selected[i] * 3 - 1] += self.my * self.Cscl + self.CSY + self.offY - anchorY
                            i += 1
                    else:
                        self.positions[self.hglmove * 3 - 2] = self.mx * self.Cscl + self.CSX + self.offX
                        self.positions[self.hglmove * 3 - 1] = self.my * self.Cscl + self.CSY + self.offY
        else:
            if not (self.mx > self.boundXmin and self.mx < self.boundXmax and self.my > self.boundYmin and self.my < self.boundYmax) and self.hglmove > 0:
                if self.selecting > 1 and len(self.selected) > 1 and (self.holding == 0 or self.holding == 1):
                    for j in range(len(self.selected) - 1):
                        self.deleteComp(self.selected[1])
                    self.selecting = 0
                    self.selectOb = ['null']
                else:
                    self.deleteComp(self.hglmove)
            if self.mouseType == 2 and not self.holding == 0 and not self.holding == 1:
                self.mouseType = 0
                if self.mx > self.boundXmin and self.mx < self.boundXmax and self.my > self.boundYmin and self.my < self.boundYmax:
                    self.components.append(self.holding)
                    self.positions.append(self.mx * self.Cscl + self.CSX)
                    self.positions.append(self.my * self.Cscl + self.CSY)
                    self.positions.append(self.holdingAng)
                    for i in range(3):
                        self.io.append(0)
                    self.inpComp.append(self.compSlots[self.compSlots.index(self.holding) + 1])
                    for i in range(2):
                        self.inpComp.append(0)
                    self.holding = 1
                    # updateUNDO
                else:
                    self.holding = 0
            for j in range(len(self.deleteQueue) - 1):
                if self.selected.count(self.deleteQueue) > 0 and self.selectOb.count(self.deleteQueue) > 0:
                    self.selected.remove(self.deleteQueue[1])
                    self.selectOb.remove(self.deleteQueue[1])
                    self.deleteQueue.pop(1)
            if self.selecting == 1:
                self.selecting = 2
                i = 1
                self.selected = ['null']
                for j in range(len(self.selectOb) - 1):
                    self.selected.append(self.selectOb[i])
                    i += 1
                if not self.selectX == self.mx or not self.selectY == self.my:
                    self.selectOb = ['null']
                if self.selectX > self.selectX2:
                    self.selectX2 = self.selectX
                    self.selectX = self.mx
                if self.selectY > self.selectY2:
                    self.selectY2 = self.selectY
                    self.selectY = self.my
            else:
                if (self.keys.count("space") > 0 or self.wireHold == 1) and not self.wiringStart == 0 and not self.wiringEnd == 0 and not self.wiringStart == self.wiringEnd:
                    wireSQueue = ['null']
                    wireEQueue = ['null']
                    if self.selected.count(self.wiringStart) > 0 and self.selecting > 1:
                        wireSQueue.append(self.wiringStart)
                        wireEQueue.append(self.wiringEnd)
                        i = 1
                        for j in range(len(self.selected) - 1):
                            if not self.wiringStart == self.selected[i] and not self.wiringEnd == self.selected[i]:
                                wireSQueue.append(self.selected[i])
                            i += 1
                    else:
                        if self.selected.count(self.hlgcomp) > 0 and self.selecting > 1:
                            wireSQueue.append(self.wiringStart)
                            i += 1
                            for j in range(len(self.selected) - 1):
                                wireEQueue.append(self.selected[i])
                                i += 1
                        else:
                            wireSQueue.append(self.wiringStart)
                            wireEQueue.append(self.wiringEnd)
                            self.selected = ['null']
                            self.selectOb = ['null']
                            self.selecting = 0
                            self.sxmax = 0
                            self.symax = 0
                            self.sxmin = 0
                            self.symin = 0
                    k = 1
                    for l in range(len(wireEQueue) - 1):
                        j = 1
                        for m1 in range(len(wireSQueue) - 1):
                            if self.inpComp[wireEQueue[k] * 3] == wireSQueue[j] or self.inpComp[wireEQueue[k] * 3 - 1] == wireSQueue[j]:
                                i = 1
                                for n in range(int(round((len(self.wiring) - 1) / 3))):
                                    if self.wiring[i] == wireSQueue[j] and self.wiring[i + 1] == wireEQueue[k]:
                                        self.wiring.pop(i)
                                        self.wiring.pop(i)
                                        self.wiring.pop(i)
                                    else:
                                        i += 3
                                if self.inpComp[wireEQueue[k] * 3 - 1] == wireSQueue[j]:
                                    if self.inpComp[wireEQueue[k] * 3] == 0:
                                        self.inpComp[wireEQueue[k] * 3 - 1] = 0
                                        self.io[wireEQueue[k] * 3 - 2] = 0
                                    else:
                                        self.inpComp[wireEQueue[k] * 3 - 1] = self.inpComp[wireEQueue[k] * 3]
                                        self.inpComp[wireEQueue[k] * 3] = 0
                                else:
                                    self.inpComp[wireEQueue[k] * 3] = 0
                                self.io[wireEQueue[k] * 3 - 1] = 0
                            else:
                                if self.inpComp[wireEQueue[k] * 3 - 1] == 0:
                                    self.inpComp[wireEQueue[k] * 3 - 1] = wireSQueue[j]
                                    self.wiring.append(wireSQueue[j])
                                    self.wiring.append(wireEQueue[k])
                                    self.wiring.append(0)
                                else:
                                    if self.inpComp[wireEQueue[k] * 3] == 0 and not self.inpComp[wireEQueue[k] * 3 - 1] == wireSQueue[j] and self.inpComp[wireEQueue[k] * 3 - 2] > 1:
                                        self.inpComp[wireEQueue[k] * 3] = wireSQueue[j]
                                        self.wiring.append(wireSQueue[j])
                                        self.wiring.append(wireEQueue[k])
                                        self.wiring.append(0)
                            j += 1
                        k += 1
                if len(self.positions) > self.hglmove * 3 and self.components[self.hglmove] == "POWER" and self.positions[self.hglmove * 3 - 2] == self.tempX and self.positions[self.hglmove * 3 - 1] == self.tempY:
                    if self.io[self.hglmove * 3] == 0:
                        self.io[self.hglmove * 3] = 1
                    else:
                        self.io[self.hglmove * 3] = 0
                self.hglmove = 0
                self.wiringStart = 0
                self.wiringEnd = 0
                if self.keys.count("mouse") > 0:
                    # updateUNDO
                    self.removeKey("mouse")
        self.hotkeyTick()
    def hotkeyTick(self):
        if (turtools.keyPressed(32) or turtools.keyPressed(65)):
            self.refillKey("space")
        else:
            if self.keys.count("space") > 0:
                self.removeKey("space")
        if turtools.keyPressed('s'):
            self.refillKey('s')
        else:
            if self.keys.count('s') > 0:
                self.removeKey('s')
        if (turtools.keyPressed(38) or turtools.keyPressed(111)):
            self.refillKey("up")
        else:
            if self.keys.count("up") > 0:
                self.removeKey("up")
        if (turtools.keyPressed(40) or turtools.keyPressed(116)):
            self.refillKey("down")
        else:
            if self.keys.count("down") > 0:
                self.removeKey("down")
        if turtools.keyPressed('p') or turtools.keyPressed('e') or turtools.keyPressed('1'):
            if self.keys.count('p') < 1:
                if self.holding == "POWER":
                    self.holding = 0
                else:
                    self.holding = "POWER"
            self.refillKey('p')
        else:
            if self.keys.count('p') > 0:
                self.removeKey('p')
        if turtools.keyPressed('x'):
            if self.keys.count('d') < 1:
                if self.selecting > 1 and len(self.selected) > 1 and (self.holding == 0 or self.holding == 1):
                    for i in range(len(self.selected) - 1):
                        self.deleteComp(self.selected[1])
                        self.selected.pop(1)
                    self.selecting = 0
                    self.selectOb = ['null']
                else:
                    if not self.hlgcomp == 0:
                        self.deleteComp(self.hlgcomp)
            self.refillKey('d')
        else:
            if self.keys.count('d') > 0:
                self.removeKey('d')
        if turtools.keyPressed('a') or turtools.keyPressed('3'):
            if self.keys.count('a') < 1:
                if self.holding == "AND":
                    self.holding = 0
                else:
                    self.holding = "AND"
            self.refillKey('a')
        else:
            if self.keys.count('a') > 0:
                self.removeKey('a')
        if turtools.keyPressed('o') or turtools.keyPressed('q') or turtools.keyPressed('4'):
            if self.keys.count('o') < 1:
                if self.holding == "OR":
                    self.holding = 0
                else:
                    self.holding = "OR"
            self.refillKey('o')
        else:
            if self.keys.count('o') > 0:
                self.removeKey('o')
        if turtools.keyPressed('n') or turtools.keyPressed('w') or turtools.keyPressed('2'):
            if self.keys.count('n') < 1:
                if self.holding == "NOT":
                    self.holding = 0
                else:
                    self.holding = "NOT"
            self.refillKey('n')
        else:
            if self.keys.count('n') > 0:
                self.removeKey('n')
        # old code for toggling power blocks with the t key
        # if turtools.keyPressed('t')
        #     if self.keys.count('t') < 1:
        #         if self.components[self.hlgcomp] == "POWER":
        #             if self.io[self.hlgcomp * 3] == 0:
        #                 self.io[self.hlgcomp * 3] = 1
        #             else:
        #                 self.io[self.hlgcomp * 3] = 0
        #     self.refillKey('t')
        # else:
        #     if self.keys.count('t') > 0:
        #         self.removeKey('t')
        if turtools.keyPressed('t'):
            if self.keys.count('t') < 1:
                if self.theme == 0:
                    self.theme = 27
                else:
                    self.theme = 0
                t.Screen().bgcolor(themeColors[25 + self.theme], themeColors[26 + self.theme], themeColors[27 + self.theme])
            self.refillKey('t')
        else:
            if self.keys.count('t') > 0:
                self.removeKey('t')
        if turtools.keyPressed('5'):
            if self.keys.count('5') < 1:
                if self.holding == "XOR":
                    self.holding = 0
                else:
                    self.holding = "XOR"
            self.refillKey('5')
        else:
            if self.keys.count('5') > 0:
                self.removeKey('5')
        if turtools.keyPressed('6'):
            if self.keys.count('6') < 1:
                if self.holding == "NOR":
                    self.holding = 0
                else:
                    self.holding = "NOR"
            self.refillKey('6')
        else:
            if self.keys.count('6') > 0:
                self.removeKey('6')
        if turtools.keyPressed('7'):
            if self.keys.count('7') < 1:
                if self.holding == "NAND":
                    self.holding = 0
                else:
                    self.holding = "NAND"
            self.refillKey('7')
        else:
            if self.keys.count('7') > 0:
                self.removeKey('7')
        if turtools.keyPressed('8'):
            if self.keys.count('8') < 1:
                if self.holding == "BUFFER":
                    self.holding = 0
                else:
                    self.holding = "BUFFER"
            self.refillKey('8')
        else:
            if self.keys.count('8') > 0:
                self.removeKey('8')
        if turtools.keyPressed('9'):
            if self.keys.count('9') < 1:
                if self.wireHold == 1:
                    self.wireHold = 0
                else:
                    self.wireHold = 1
                    self.holding = 0
            self.refillKey('9')
        else:
            if self.keys.count('9') > 0:
                self.removeKey('9')
        if not self.holding == 0 and not self.holding == 1:
            self.wireHold = 0
        if turtools.keyPressed('c'):
            if self.keys.count('c') < 1:
                if self.selecting > 1 and len(self.selected) > 1 and (self.holding == 0 or self.holding == 1):
                    self.copySelected()
            self.refillKey('c')
        else:
            if self.keys.count('c') > 0:
                self.removeKey('c')
        if turtools.keyPressed('h'):
            if self.keys.count('h') < 1:
                self.sidebar += 1
                if self.sidebar > 2:
                    self.sidebar = 0
            self.refillKey('h')
        else:
            if self.keys.count('h') > 0:
                self.removeKey('h')
        self.scrollTick()
    def scrollTick(self):
        global globalsize
        # since the mouseWheel() command resets the value to 0, a variable must be used to store the value to make use of it later (since you can't just run the command again since it will be set to 0)
        # print(self.mw)
        if self.mw > 0 or self.linuxMouse > 0:
            if self.keys.count("space") > 0:
                if self.rotateCooldown == 1:
                    if self.selecting > 1:
                        self.rotateSelected(90)
                    else:
                        if not self.holding == 0 and not self.holding == 1:
                            self.holdingAng -= 90
                        else:
                            if not self.hlgcomp == 0:
                                self.positions[self.hlgcomp * 3] -= 90
                                if self.positions[self.hlgcomp * 3] < 0:
                                    self.positions[self.hlgcomp * 3] += 360
                    self.rotateCooldown = 0
            else:
                if self.Cscl > 0.15:
                    self.CSX += self.mx * 0.1 * self.scrollSpeed
                    self.CSY += self.my * 0.1 * self.scrollSpeed
                    self.Cscl -= 0.1 * self.scrollSpeed
                    globalsize = 1.5 / self.Cscl
        if self.mw < 0 or self.linuxMouse < 0:
            if self.keys.count("space") > 0:
                if self.rotateCooldown == 1:
                    if self.selecting > 1:
                        self.rotateSelected(-90)
                    else:
                        if not self.holding == 0 and not self.holding == 1:
                            self.holdingAng += 90
                        else:
                            if not self.hlgcomp == 0:
                                self.positions[self.hlgcomp * 3] += 90
                                if self.positions[self.hlgcomp * 3] > 360:
                                    self.positions[self.hlgcomp * 3] -= 360
                    self.rotateCooldown = 0
            else:
                self.CSX -= self.mx * 0.1 * self.scrollSpeed
                self.CSY -= self.my * 0.1 * self.scrollSpeed
                self.Cscl += 0.1 * self.scrollSpeed
                globalsize = 1.5 / self.Cscl
        if self.mw == 0 and self.linuxMouse == 0:
            self.rotateCooldown = 1
        # if len(turtools.keys) == 0 and not turtools.mouseDown():
        #     self.keys = ['null']
    def refillKey(self, key):
        i = 1
        for j in range(int(round((len(self.keys) - 1) / 2))):
            if self.keys[i] == key:
                self.keys[i + 1] = self.bufferFrames
                return
            i += 2
        self.keys.append(key)
        self.keys.append(self.bufferFrames)
        return
    def removeKey(self, key):
        i = 1
        for j in range(int(round((len(self.keys) - 1) / 2))):
            if self.keys[i] == key:
                if self.keys[i + 1] <= 0:
                    self.keys.pop(i)
                    self.keys.pop(i)
                else:
                    self.keys[i + 1] -= 1
                return
            i += 2
        return
    def copySelected(self):
        self.sxmax = 0
        self.sxmin = 0
        self.symax = 0
        self.symin = 0
        self.selecting = 3
        i = 1
        j = 0
        k = 0
        l = len(self.components) - self.selected[1]
        m1 = len(self.selected) - 1
        for n in range(m1):
            j += self.positions[self.selected[i] * 3 - 2]
            k += self.positions[self.selected[i] * 3 - 1]
            i += 1
        j /= m1
        k /= m1
        i = 1
        for n in range(m1):
            self.components.append(self.components[self.selected[i]])
            self.positions.append(self.positions[self.selected[i] * 3 - 2] + self.mx * self.Cscl + self.CSX - j)
            self.positions.append(self.positions[self.selected[i] * 3 - 1] + self.my * self.Cscl + self.CSY - k)
            self.positions.append(self.positions[self.selected[i] * 3])
            for o in range(3):
                self.io.append(0)
            self.inpComp.append(self.inpComp[self.selected[i] * 3 - 2])
            if self.selected.count(self.inpComp[self.selected[i] * 3 - 1]) > 0:
                self.inpComp.append(l + self.inpComp[self.selected[i] * 3 - 1])
            else:
                self.inpComp.append(0)
            if self.selected.count(self.inpComp[self.selected[i] * 3]) > 0:
                self.inpComp.append(l + self.inpComp[self.selected[i] * 3])
            else:
                self.inpComp.append(0)
            i += 1
        i = 1
        n = len(self.components) - len(self.selected)
        self.wireTemp = ['null']
        for o in range(m1):
            self.wireTemp.append(n + i)
            i += 1
        i = 1
        for o in range(int(round((len(self.wiring) - 1) / 3))):
            if self.selected.count(self.wiring[i]) and self.selected.count(self.wiring[i + 1]):
                self.wiring.append(self.wireTemp[self.selected.index(self.wiring[i])])
                self.wiring.append(self.wireTemp[self.selected.index(self.wiring[i + 1])])
                self.wiring.append(0)
            i += 3
        i = len(self.components) - len(self.selected) + 1
        self.selected = ['null']
        for o in range(m1):
            self.selected.append(i)
            i += 1
    def selectionBox(self, x1, y1, x2, y2):
        self.sp.pencolor(themeColors[4 + self.theme], themeColors[5 + self.theme], themeColors[6 + self.theme])
        self.sp.pensize(globalsize * 2 * self.scaling)
        self.sp.goto(x1, y1)
        self.sp.pendown()
        self.sp.goto(x1, y2)
        self.sp.goto(x2, y2)
        self.sp.goto(x2, y1)
        self.sp.goto(x1, y1)
        self.sp.penup()
        if x1 > x2:
            self.sxmax = x1
            self.sxmin = x2
        else:
            self.sxmax = x2
            self.sxmin = x1
        if y1 > y2:
            self.symax = y1
            self.symin = y2
        else:
            self.symax = y2
            self.symin = y1
    def deleteComp(self, index):
        i = 1
        for j in range(len(self.selected) - 1):
            if self.selected[i] > index:
                self.selected[i] -= 1
            i += 1
        i = 1
        for j in range(int(round((len(self.wiring) - 1) / 3))):
            if self.wiring[i] == index or self.wiring[i + 1] == index:
                self.wiring.pop(i)
                self.wiring.pop(i)
                self.wiring.pop(i)
            else:
                if self.wiring[i] > index:
                    self.wiring[i] -= 1
                if self.wiring[i + 1] > index:
                    self.wiring[i + 1] -= 1
                i += 3
        i = 2
        for j in range(int(round((len(self.inpComp) - 1) / 3))):
            if self.inpComp[i] == index or self.inpComp[i + 1] == index:
                if self.inpComp[i] == index:
                    if not self.inpComp[i + 1] == 0:
                        if self.inpComp[i + 1] > index:
                            self.inpComp[i] = self.inpComp[i + 1] - 1
                        else:
                            self.inpComp[i] = self.inpComp[i + 1]
                        self.inpComp[i + 1] = 0
                        self.io[i] = 0
                    else:
                        self.inpComp[i] = 0
                        self.inpComp[i + 1] = 0
                else:
                    if self.inpComp[i] > index:
                        self.inpComp[i] -= 1
                    self.inpComp[i + 1] = 0
                    self.io[i] = 0
            else:
                if self.inpComp[i] > index:
                        self.inpComp[i] -= 1
                if self.inpComp[i + 1] > index:
                        self.inpComp[i + 1] -= 1
            i += 3
        self.components.pop(index)
        for i in range(3):
            self.positions.pop(index * 3 - 2)
        for i in range(3):
            self.io.pop(index * 3 - 2)
        for i in range(3):
            self.inpComp.pop(index * 3 - 2)
    def hlgcompset(self):
        self.hlgcomp = 0
        i = 1
        for j in range(len(self.components) - 1):
            if (self.mx * self.Cscl + self.CSX + 18) > self.positions[i * 3 - 2] and (self.mx * self.Cscl + self.CSX - 18) < self.positions[i * 3 - 2] and (self.my * self.Cscl + self.CSY + 18) > self.positions[i * 3 - 1] and (self.my * self.Cscl + self.CSY - 18) < self.positions[i * 3 - 1]:
                self.hlgcomp = i
            i += 1
    def rotateSelected(self, degrees):
        i = 1
        j = 0
        k = 0
        for l in range(len(self.selected) - 1):
            j += self.positions[self.selected[i] * 3 - 2]
            k += self.positions[self.selected[i] * 3 - 1]
            i += 1
        j /= (len(self.selected) - 1)
        k /= (len(self.selected) - 1)
        i = 1
        for l in range(len(self.selected) - 1):
            n = j + (self.positions[self.selected[i] * 3 - 2] - j) * (m.cos(m.radians(degrees))) - (self.positions[self.selected[i] * 3 - 1] - k) * (m.sin(m.radians(degrees)))
            self.positions[self.selected[i] * 3 - 1] = k + (self.positions[self.selected[i] * 3 - 2] - j) * (m.sin(m.radians(degrees))) + (self.positions[self.selected[i] * 3 - 1] - k) * (m.cos(m.radians(degrees)))
            self.positions[self.selected[i] * 3 - 2] = n
            self.positions[self.selected[i] * 3] -= degrees
            if self.positions[self.selected[i] * 3] < 0:
                self.positions[self.selected[i] * 3] += 360
            if self.positions[self.selected[i] * 3] > 360:
                self.positions[self.selected[i] * 3] -= 360
            i += 1
    def wireIO(self, index1, index2):
        if self.components[self.wiring[index1]] == "BUFFER":
            self.io[self.wiring[index1] * 3] = self.io[self.wiring[index1] * 3 - 1]
            self.io[self.wiring[index1] * 3 - 1] = self.io[self.wiring[index1] * 3 - 2]
        if self.components[self.wiring[index1]] == "NOT":
            self.io[self.wiring[index1] * 3] = abs(self.io[self.wiring[index1] * 3 - 2] - 1)
        if self.components[self.wiring[index1]] == "AND":
            self.io[self.wiring[index1] * 3] = self.io[self.wiring[index1] * 3 - 2] * self.io[self.wiring[index1] * 3 - 1]
        if self.components[self.wiring[index1]] == "OR":
            self.io[self.wiring[index1] * 3] = m.ceil((self.io[self.wiring[index1] * 3 - 2] + self.io[self.wiring[index1] * 3 - 1]) / 2)
        if self.components[self.wiring[index1]] == "XOR":
            self.io[self.wiring[index1] * 3] = abs(self.io[self.wiring[index1] * 3 - 2] - self.io[self.wiring[index1] * 3 - 1])
        if self.components[self.wiring[index1]] == "NOR":
            self.io[self.wiring[index1] * 3] = abs(m.ceil((self.io[self.wiring[index1] * 3 - 2] - self.io[self.wiring[index1] * 3 - 1]) / 2) - 1)
        if self.components[self.wiring[index1]] == "NAND":
            self.io[self.wiring[index1] * 3] = abs(self.io[self.wiring[index1] * 3 - 2] * self.io[self.wiring[index1] * 3 - 1] - 1)
        self.wiring[index1 + 2] = self.io[self.wiring[index1] * 3]
        if self.inpComp[self.wiring[index2] * 3 - 1] == self.wiring[index1]:
            self.io[self.wiring[index1 + 1] * 3 - 2] = self.io[self.wiring[index1] * 3]
        else:
            self.io[self.wiring[index1 + 1] * 3 - 1] = self.io[self.wiring[index1] * 3]
        if self.compSlots[self.compSlots.index(self.components[self.wiring[index2]]) + 1] == 2:
            if self.inpComp[self.wiring[index2] * 3] == 0:
                self.wxOffE = 0
                self.wyOffE = 0
            else:
                tempAng = self.inpComp[self.wiring[index2] * 3 - 1] * 3
                tempAng2 = self.inpComp[self.wiring[index2] * 3] * 3
                tempAng3 = self.wiring[index2] * 3
                self.compareAng(index1, index2, self.inpComp[self.wiring[index2] * 3 - 1], self.inpComp[self.wiring[index2] * 3 - 2], self.positions[tempAng - 2] + m.sin(m.radians(self.positions[tempAng])) * 22.5 / self.Cscl, self.positions[tempAng - 1] + m.cos(m.radians(self.positions[tempAng])) * 22.5 / self.Cscl, self.positions[tempAng2 - 2] + m.sin(m.radians(self.positions[tempAng2])) * 22.5 / self.Cscl, self.positions[tempAng2 - 1] + m.cos(m.radians(self.positions[tempAng2])) * 22.5 / self.Cscl, self.positions[tempAng3 - 2] + m.sin(m.radians(self.positions[tempAng3])) * 22.5 / self.Cscl, self.positions[tempAng3 - 1] + m.cos(m.radians(self.positions[tempAng3])) * 22.5 / self.Cscl, self.positions[tempAng3])
        else:
            self.wxOffE = 0
            self.wyOffE = 0
    def compareAng(self, index1, index2, comp1, comp2, x1, y1, x2, y2, x3, y3, rot):
        sinRot = m.sin(m.radians(rot))
        cosRot = m.cos(m.radians(rot))
        morphX1 = ((x3 - x1) * cosRot) - ((y3 - y1) * sinRot)
        morphY1 = ((x3 - x1) * sinRot) - ((y3 - y1) * cosRot)
        morphX2 = ((x3 - x2) * cosRot) - ((y3 - y2) * sinRot)
        morphY2 = ((x3 - x2) * sinRot) - ((y3 - y2) * cosRot)
        if m.asin(morphX2 / m.sqrt(morphY2 ** 2 + morphX2 ** 2)) > m.asin(morphX1 / m.sqrt(morphY1 ** 2 + morphX1 ** 2)):
            if comp1 == self.wiring[index1]:
                self.wxOffE = (cosRot * -5) / self.Cscl
                self.wyOffE = (sinRot * 5) / self.Cscl
            else:
                self.wxOffE = (cosRot * 5) / self.Cscl
                self.wyOffE = (sinRot * -5) / self.Cscl
        else:
            if comp1 == self.wiring[index1]:
                self.wxOffE = (cosRot * 5) / self.Cscl
                self.wyOffE = (sinRot * -5) / self.Cscl
            else:
                self.wxOffE = (cosRot * -5) / self.Cscl
                self.wyOffE = (sinRot * 5) / self.Cscl
    def renderComp(self):
        i = 1
        self.selectOb = ['null']
        for j in range(len(self.components) - 1):
            renderX = (self.positions[i * 3 - 2] - self.CSX) / self.Cscl
            renderY = (self.positions[i * 3 - 1] - self.CSY) / self.Cscl
            if renderX + 15 * globalsize > -240 and renderX + -15 * globalsize < 240 and renderY + 15 * globalsize > -180 and renderY + -15 * globalsize < 180:
                if self.selected.count(i) > 0 or (renderX + 12 * globalsize > self.sxmin and renderX + -12 * globalsize < self.sxmax and renderY + 12 * globalsize > self.symin and renderY + -12 * globalsize < self.symax and self.selecting == 1):
                    self.selectOb.append(i)
                    self.sp.pencolor(themeColors[4 + self.theme], themeColors[5 + self.theme], themeColors[6 + self.theme])
                else:
                    self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
                if self.components[i] == "POWER":
                    if self.io[i * 3] == 1:
                        if self.selectOb.count(i) > 0:
                            self.POWER(renderX, renderY, globalsize, self.positions[i * 3], 1, 1)
                        else:
                            self.POWER(renderX, renderY, globalsize, self.positions[i * 3], 1, 0)
                    else:
                        if self.io[i * 3 - 2] == 1:
                            if self.selectOb.count(i) > 0:
                                self.POWER(renderX, renderY, globalsize, self.positions[i * 3], 2, 1)
                            else:
                                self.POWER(renderX, renderY, globalsize, self.positions[i * 3], 2, 0)
                        else:
                            if self.selectOb.count(i) > 0:
                                self.POWER(renderX, renderY, globalsize, self.positions[i * 3], 0, 1)
                            else:
                                self.POWER(renderX, renderY, globalsize, self.positions[i * 3], 0, 0)
                if self.components[i] == "AND":
                    self.AND(renderX, renderY, globalsize, self.positions[i * 3])
                if self.components[i] == "OR":
                    self.OR(renderX, renderY, globalsize, self.positions[i * 3])
                if self.components[i] == "NOT":
                    self.NOT(renderX, renderY, globalsize, self.positions[i * 3])
                if self.components[i] == "XOR":
                    self.XOR(renderX, renderY, globalsize, self.positions[i * 3])
                if self.components[i] == "NOR":
                    self.NOR(renderX, renderY, globalsize, self.positions[i * 3])
                if self.components[i] == "NAND":
                    self.NAND(renderX, renderY, globalsize, self.positions[i * 3])
                if self.components[i] == "BUFFER":
                    self.BUFFER(renderX, renderY, globalsize, self.positions[i * 3])
            i += 1
    def renderWire(self, size):
        self.sp.pensize(size * 2 * self.scaling)
        i = 1
        for j in range(int((len(self.wiring) - 1) / 3)):
            self.wireIO(i, i + 1)
            wireTXS = (self.positions[self.wiring[i] * 3 - 2] - self.CSX) / self.Cscl
            wireTYS = (self.positions[self.wiring[i] * 3 - 1] - self.CSY) / self.Cscl
            self.sp.goto(wireTXS, wireTYS)
            if self.wiring[i + 2] == 1:
                if self.selectOb.count(self.wiring[i]) > 0 or self.selectOb.count(self.wiring[i + 1]) > 0 or self.selected.count(self.wiring[i]) > 0 or self.selected.count(self.wiring[i + 1]) > 0:
                    self.sp.pencolor(themeColors[10 + self.theme], themeColors[11 + self.theme], themeColors[12 + self.theme])
                else:
                    self.sp.pencolor(themeColors[7 + self.theme], themeColors[8 + self.theme], themeColors[9 + self.theme])
            else:
                if self.selectOb.count(self.wiring[i]) > 0 or self.selectOb.count(self.wiring[i + 1]) > 0 or self.selected.count(self.wiring[i]) > 0 or self.selected.count(self.wiring[i + 1]) > 0:
                    self.sp.pencolor(themeColors[4 + self.theme], themeColors[5 + self.theme], themeColors[6 + self.theme])
                else:
                    self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
            self.sp.pendown()
            self.sp.goto(wireTXS + m.sin(m.radians(self.positions[self.wiring[i] * 3])) * 22.5 / self.Cscl, wireTYS + m.cos(m.radians(self.positions[self.wiring[i] * 3])) * 22.5 / self.Cscl)
            wireTXE = (self.positions[self.wiring[i + 1] * 3 - 2] - self.CSX) / self.Cscl
            wireTYE = (self.positions[self.wiring[i + 1] * 3 - 1] - self.CSY) / self.Cscl
            self.sp.goto(wireTXE - (m.sin(m.radians(self.positions[self.wiring[i + 1] * 3])) * 22.5 / self.Cscl + self.wxOffE), wireTYE - (m.cos(m.radians(self.positions[self.wiring[i + 1] * 3])) * 22.5 / self.Cscl + self.wyOffE))
            self.sp.goto(wireTXE, wireTYE)
            self.sp.penup()
            self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
            i += 3
    def renderSidebar(self, side):
        self.sp.pencolor(themeColors[13 + self.theme], themeColors[14 + self.theme], themeColors[15 + self.theme])
        self.sp.pensize(60 * self.scaling)
        self.boundXmin = -241
        self.boundXmax = 241
        self.boundYmin = -181
        self.boundYmax = 181
        if side == 1 or side == 2:
            i = 155 - (side % 2) * 305
            if i > 0:
                self.boundYmax = 120 - (side % 2) * 240
            else:
                self.boundYmin = 120 - (side % 2) * 240
            self.sp.goto(-280, i)
            self.sp.pendown()
            self.sp.goto(280, i)
            self.sp.penup()
            j = -200
            if self.holding == "POWER" and self.indicators == 1:
                self.sp.pencolor(themeColors[16 + self.theme], themeColors[17 + self.theme], themeColors[18 + self.theme])
            else:
                self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
            self.POWER(j, i, 1.5, 90, 0, 1)
            j += 50
            if self.holding == "NOT" and self.indicators == 1:
                self.sp.pencolor(themeColors[16 + self.theme], themeColors[17 + self.theme], themeColors[18 + self.theme])
            else:
                self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
            self.NOT(j, i, 1.5, 90)
            j += 50
            if self.holding == "AND" and self.indicators == 1:
                self.sp.pencolor(themeColors[16 + self.theme], themeColors[17 + self.theme], themeColors[18 + self.theme])
            else:
                self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
            self.AND(j, i, 1.5, 90)
            j += 50
            if self.holding == "OR" and self.indicators == 1:
                self.sp.pencolor(themeColors[16 + self.theme], themeColors[17 + self.theme], themeColors[18 + self.theme])
            else:
                self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
            self.OR(j, i, 1.5, 90)
            j += 50
            if self.holding == "XOR" and self.indicators == 1:
                self.sp.pencolor(themeColors[16 + self.theme], themeColors[17 + self.theme], themeColors[18 + self.theme])
            else:
                self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
            self.XOR(j, i, 1.5, 90)
            j += 50
            if self.holding == "NOR" and self.indicators == 1:
                self.sp.pencolor(themeColors[16 + self.theme], themeColors[17 + self.theme], themeColors[18 + self.theme])
            else:
                self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
            self.NOR(j, i, 1.5, 90)
            j += 50
            if self.holding == "NAND" and self.indicators == 1:
                self.sp.pencolor(themeColors[16 + self.theme], themeColors[17 + self.theme], themeColors[18 + self.theme])
            else:
                self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
            self.NAND(j, i, 1.5, 90)
            j += 50
            if self.holding == "BUFFER" and self.indicators == 1:
                self.sp.pencolor(themeColors[16 + self.theme], themeColors[17 + self.theme], themeColors[18 + self.theme])
            else:
                self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
            self.BUFFER(j, i, 1.5, 90)
            j += 45
            if (self.keys.count("space") > 0 or self.wireHold) and self.indicators == 1:
                self.sp.pencolor(themeColors[16 + self.theme], themeColors[17 + self.theme], themeColors[18 + self.theme])
            else:
                self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
            self.wireSymbol(j, i, 1.5, 90)
        self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
    def POWER(self, x, y, size, rot, state, select):
        rot = m.radians(rot)
        self.sp.goto(x, y)
        self.sp.pensize(size * 25 * self.scaling)
        self.sp.pendown()
        self.sp.forward(0)
        self.sp.penup()
        if state == 2:
            self.sp.pensize(size * 20 * self.scaling)
            if select == 1:
                self.sp.pencolor(themeColors[22 + self.theme], themeColors[23 + self.theme], themeColors[24 + self.theme])
            else:
                self.sp.pencolor(themeColors[19 + self.theme], themeColors[20 + self.theme], themeColors[21 + self.theme])
            self.sp.pendown()
            self.sp.forward(0)
            self.sp.penup()
            self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
        if state == 1:
            self.sp.pensize(size * 20 * self.scaling)
            if select == 1:
                self.sp.pencolor(themeColors[10 + self.theme], themeColors[11 + self.theme], themeColors[12 + self.theme])
            else:
                self.sp.pencolor(themeColors[7 + self.theme], themeColors[8 + self.theme], themeColors[9 + self.theme])
            self.sp.pendown()
            self.sp.forward(0)
            self.sp.penup()
            self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
    def NOT(self, x, y, size, rot):
        rot = m.radians(rot)
        sinRot = m.sin(rot)
        cosRot = m.cos(rot)
        self.sp.pensize(size * 2 * self.scaling)
        self.sp.goto(x + (-11 * size * sinRot) - (11 * size * cosRot), y + (-11 * size * cosRot) + (11 * size * sinRot))
        self.sp.pendown()
        self.sp.goto(x + (7 * size * sinRot), y + (7 * size * cosRot))
        self.sp.goto(x + (-11 * size * sinRot) - (-11 * size * cosRot), y + (-11 * size * cosRot) + (-11 * size * sinRot))
        self.sp.goto(x + (-11 * size * sinRot) - (11 * size * cosRot), y + (-11 * size * cosRot) + (11 * size * sinRot))
        self.sp.penup()
        self.sp.goto(x + (10 * size * sinRot), y + (10 * size * cosRot))
        self.sp.pensize(size * 7 * self.scaling)
        self.sp.pendown()
        self.sp.forward(0)
        self.sp.penup()
        self.sp.pensize(size * 3 * self.scaling)
        self.sp.pencolor(themeColors[25 + self.theme], themeColors[26 + self.theme], themeColors[27 + self.theme])
        self.sp.pendown()
        self.sp.forward(0)
        self.sp.penup()
        self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
    def AND(self, x, y, size, rot):
        rot = m.radians(rot)
        sinRot = m.sin(rot)
        cosRot = m.cos(rot)
        self.sp.pensize(size * 2 * self.scaling)
        self.sp.goto(x + (-12 * size * sinRot) - (-9 * size * cosRot), y + (-12 * size * cosRot) + (-9 * size * sinRot))
        self.sp.pendown()
        self.sp.goto(x + (4 * size * sinRot) - (-9 * size * cosRot), y + (4 * size * cosRot) + (-9 * size * sinRot))
        i = 180
        for j in range(self.GraphPrez + 1):
            k = m.radians(i)
            self.sp.goto(x + ((4 * size + m.sin(k) * 8 * size) * sinRot) - (m.cos(k) * 9 * size * cosRot), y + ((4 * size + m.sin(k) * 8 * size) * cosRot) + (m.cos(k) * 9 * size * sinRot))
            i -= (180 / self.GraphPrez)
        self.sp.goto(x + (-12 * size * sinRot) - (9 * size * cosRot), y + (-12 * size * cosRot) + (9 * size * sinRot))
        self.sp.goto(x + (-12 * size * sinRot) - (-9 * size * cosRot), y + (-12 * size * cosRot) + (-9 * size * sinRot))
        self.sp.penup()
    def OR(self, x, y, size, rot):
        rot = m.radians(rot)
        sinRot = m.sin(rot)
        cosRot = m.cos(rot)
        self.sp.pensize(size * 2 * self.scaling)
        self.sp.goto(x + (-11 * size * sinRot) - (9 * size * cosRot), y + (-11 * size * cosRot) + (9 * size * sinRot))
        self.sp.pendown()
        i = 180
        for j in range(self.GraphPrez + 1):
            k = m.radians(i)
            self.sp.goto(x + ((-11 * size + m.sin(k) * 5 * size) * sinRot) - (m.cos(k) * -9 * size * cosRot), y + ((-11 * size + m.sin(k) * 5 * size) * cosRot) + (m.cos(k) * -9 * size * sinRot))
            i -= (180 / self.GraphPrez)
        i += (180 / self.GraphPrez)
        for j in range(int(round((self.GraphPrez + 1)/1.5))):
            k = m.radians(i)
            self.sp.goto(x + ((-11 * size + m.sin(k) * 25 * size) * sinRot) - ((9 * size - m.cos(k) * 18 * size) * cosRot), y + ((-11 * size + m.sin(k) * 25 * size) * cosRot) + ((9 * size - m.cos(k) * 18 * size) * sinRot))
            i += (90 / self.GraphPrez)
        self.sp.goto(x + (10.3 * size * sinRot), y + (10.3 * size * cosRot))
        self.sp.penup()
        self.sp.goto(x + (-11 * size * sinRot) - (9 * size * cosRot), y + (-11 * size * cosRot) + (9 * size * sinRot))
        self.sp.pendown()
        i = 0
        for j in range(int(round((self.GraphPrez + 1)/1.5))):
            k = m.radians(i)
            self.sp.goto(x + ((-11 * size + m.sin(k) * 25 * size) * sinRot) - ((-9 * size + m.cos(k) * 18 * size) * cosRot), y + ((-11 * size + m.sin(k) * 25 * size) * cosRot) + ((-9 * size + m.cos(k) * 18 * size) * sinRot))
            i += (90 / self.GraphPrez)
        self.sp.goto(x + (10.3 * size * sinRot), y + (10.3 * size * cosRot))
        self.sp.penup()
    def XOR(self, x, y, size, rot):
        rot = m.radians(rot)
        sinRot = m.sin(rot)
        cosRot = m.cos(rot)
        self.sp.pensize(size * 2 * self.scaling)
        i = 180
        i -= 180 / self.GraphPrez
        k = m.radians(i)
        self.sp.goto(x + ((-15 * size + m.sin(k) * 5 * size) * sinRot) - (m.cos(k) * -9 * size * cosRot), y + ((-15 * size + m.sin(k) * 5 * size) * cosRot) + (m.cos(k) * -9 * size * sinRot))
        self.sp.pendown()
        for j in range(self.GraphPrez - 1):
            k = m.radians(i)
            self.sp.goto(x + ((-15 * size + m.sin(k) * 5 * size) * sinRot) - (m.cos(k) * -9 * size * cosRot), y + ((-15 * size + m.sin(k) * 5 * size) * cosRot) + (m.cos(k) * -9 * size * sinRot))
            i -= 180 / self.GraphPrez
        self.sp.penup()
        i = 180
        i -= 180 / self.GraphPrez
        k = m.radians(i)
        self.sp.goto(x + ((-11 * size + m.sin(k) * 5 * size) * sinRot) - (m.cos(k) * -9 * size * cosRot), y + ((-11 * size + m.sin(k) * 5 * size) * cosRot) + (m.cos(k) * -9 * size * sinRot))
        self.sp.pendown()
        for j in range(self.GraphPrez - 1):
            k = m.radians(i)
            self.sp.goto(x + ((-11 * size + m.sin(k) * 5 * size) * sinRot) - (m.cos(k) * -9 * size * cosRot), y + ((-11 * size + m.sin(k) * 5 * size) * cosRot) + (m.cos(k) * -9 * size * sinRot))
            i -= (180 / self.GraphPrez)
        i += (180 / self.GraphPrez)
        for j in range(int(round((self.GraphPrez - 2)/1.5))):
            k = m.radians(i)
            self.sp.goto(x + ((-11 * size + m.sin(k) * 25 * size) * sinRot) - ((9 * size - m.cos(k) * 18 * size) * cosRot), y + ((-11 * size + m.sin(k) * 25 * size) * cosRot) + ((9 * size - m.cos(k) * 18 * size) * sinRot))
            i += (90 / self.GraphPrez)
        self.sp.goto(x + (10.3 * size * sinRot), y + (10.3 * size * cosRot))
        self.sp.penup()
        i = 180
        i -= 180 / self.GraphPrez
        k = m.radians(i)
        self.sp.goto(x + ((-11 * size + m.sin(k) * 5 * size) * sinRot) - (m.cos(k) * -9 * size * cosRot), y + ((-11 * size + m.sin(k) * 5 * size) * cosRot) + (m.cos(k) * -9 * size * sinRot))
        self.sp.pendown()
        i = 0
        i += 180 / self.GraphPrez
        for j in range(int(round((self.GraphPrez - 2)/1.5))):
            k = m.radians(i)
            self.sp.goto(x + ((-11 * size + m.sin(k) * 25 * size) * sinRot) - ((-9 * size + m.cos(k) * 18 * size) * cosRot), y + ((-11 * size + m.sin(k) * 25 * size) * cosRot) + ((-9 * size + m.cos(k) * 18 * size) * sinRot))
            i += (90 / self.GraphPrez)
        self.sp.goto(x + (10.3 * size * sinRot), y + (10.3 * size * cosRot))
        self.sp.penup()
    def NOR(self, x, y, size, rot):
        rot = m.radians(rot)
        sinRot = m.sin(rot)
        cosRot = m.cos(rot)
        self.sp.pensize(size * 2 * self.scaling)
        self.sp.goto(x + (-13 * size * sinRot) - (9 * size * cosRot), y + (-13 * size * cosRot) + (9 * size * sinRot))
        self.sp.pendown()
        i = 180
        for j in range(self.GraphPrez + 1):
            k = m.radians(i)
            self.sp.goto(x + ((-13 * size + m.sin(k) * 5 * size) * sinRot) - (m.cos(k) * -9 * size * cosRot), y + ((-13 * size + m.sin(k) * 5 * size) * cosRot) + (m.cos(k) * -9 * size * sinRot))
            i -= (180 / self.GraphPrez)
        i += (180 / self.GraphPrez)
        for j in range(int(round((self.GraphPrez + 1)/1.5))):
            k = m.radians(i)
            self.sp.goto(x + ((-13 * size + m.sin(k) * 25 * size) * sinRot) - ((9 * size - m.cos(k) * 18 * size) * cosRot), y + ((-13 * size + m.sin(k) * 25 * size) * cosRot) + ((9 * size - m.cos(k) * 18 * size) * sinRot))
            i += (90 / self.GraphPrez)
        self.sp.goto(x + (8.3 * size * sinRot), y + (8.3 * size * cosRot))
        self.sp.penup()
        self.sp.goto(x + (-13 * size * sinRot) - (9 * size * cosRot), y + (-13 * size * cosRot) + (9 * size * sinRot))
        self.sp.pendown()
        i = 0
        for j in range(int(round((self.GraphPrez + 1)/1.5))):
            k = m.radians(i)
            self.sp.goto(x + ((-13 * size + m.sin(k) * 25 * size) * sinRot) - ((-9 * size + m.cos(k) * 18 * size) * cosRot), y + ((-13 * size + m.sin(k) * 25 * size) * cosRot) + ((-9 * size + m.cos(k) * 18 * size) * sinRot))
            i += (90 / self.GraphPrez)
        self.sp.goto(x + (8.3 * size * sinRot), y + (8.3 * size * cosRot))
        self.sp.penup()
        self.sp.goto(x + (11.5 * size * sinRot), y + (11.5 * size * cosRot))
        self.sp.pensize(size * 7 * self.scaling)
        self.sp.pendown()
        self.sp.forward(0)
        self.sp.penup()
        self.sp.pensize(size * 3 * self.scaling)
        self.sp.pencolor(themeColors[25 + self.theme], themeColors[26 + self.theme], themeColors[27 + self.theme])
        self.sp.pendown()
        self.sp.forward(0)
        self.sp.penup()
        self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
    def NAND(self, x, y, size, rot):
        rot = m.radians(rot)
        sinRot = m.sin(rot)
        cosRot = m.cos(rot)
        self.sp.pensize(size * 2 * self.scaling)
        self.sp.goto(x + (-12 * size * sinRot) - (-9 * size * cosRot), y + (-12 * size * cosRot) + (-9 * size * sinRot))
        self.sp.pendown()
        self.sp.goto(x + (4 * size * sinRot) - (-9 * size * cosRot), y + (4 * size * cosRot) + (-9 * size * sinRot))
        i = 180
        for j in range(self.GraphPrez + 1):
            k = m.radians(i)
            self.sp.goto(x + ((4 * size + m.sin(k) * 8 * size) * sinRot) - (m.cos(k) * 9 * size * cosRot), y + ((4 * size + m.sin(k) * 8 * size) * cosRot) + (m.cos(k) * 9 * size * sinRot))
            i -= (180 / self.GraphPrez)
        self.sp.goto(x + (-12 * size * sinRot) - (9 * size * cosRot), y + (-12 * size * cosRot) + (9 * size * sinRot))
        self.sp.goto(x + (-12 * size * sinRot) - (-9 * size * cosRot), y + (-12 * size * cosRot) + (-9 * size * sinRot))
        self.sp.penup()
        self.sp.goto(x + (15 * size * sinRot), y + (15 * size * cosRot))
        self.sp.pensize(size * 7 * self.scaling)
        self.sp.pendown()
        self.sp.forward(0)
        self.sp.penup()
        self.sp.pensize(size * 3 * self.scaling)
        self.sp.pencolor(themeColors[25 + self.theme], themeColors[26 + self.theme], themeColors[27 + self.theme])
        self.sp.pendown()
        self.sp.forward(0)
        self.sp.penup()
        self.sp.pencolor(themeColors[1 + self.theme], themeColors[2 + self.theme], themeColors[3 + self.theme])
    def BUFFER(self, x, y, size, rot):
        rot = m.radians(rot)
        sinRot = m.sin(rot)
        cosRot = m.cos(rot)
        self.sp.pensize(size * 2 * self.scaling)
        self.sp.goto(x + (-8 * size * sinRot) - (11 * size * cosRot), y + (-8 * size * cosRot) + (11 * size * sinRot))
        self.sp.pendown()
        self.sp.goto(x + (10 * size * sinRot), y + (10 * size * cosRot))
        self.sp.goto(x + (-8 * size * sinRot) - (-11 * size * cosRot), y + (-8 * size * cosRot) + (-11 * size * sinRot))
        self.sp.goto(x + (-8 * size * sinRot) - (11 * size * cosRot), y + (-8 * size * cosRot) + (11 * size * sinRot))
        self.sp.penup()
    def wireSymbol(self, x, y, size, rot):
        rot = m.radians(rot)
        sinRot = m.sin(rot)
        cosRot = m.cos(rot)
        self.sp.pensize(size * 2 * self.scaling)
        self.sp.goto(x + -12 * size, y + -9 * size)
        self.sp.pendown()
        self.sp.goto(x + -6 * size, y + -9 * size)
        self.sp.goto(x + 6 * size, y + 9 * size)
        self.sp.goto(x + 12 * size, y + 9 * size)
        self.sp.penup()
main = master()
if tps == 'inf' or tps == 'infinity':
    while True:
        main.tick()
else:
    while True:
        t.ontimer(main.tick(), int(1000/tps))

# Fader v.0.2.1 # "Now with time and space!"
# Time travel roguelike tech demo
# Written by Eric Fedrowisch. All rights reserved.

import libtcodpy as libtcod
from components import *

# Container class for timeframes
class Continuum():
    def __init__(self, zone = None):
        self.timeframes = []
        self.timeframes.append(Timeframe(self, 0)) #Create inital timeframe
        self.timeframes[0].zone = zone
        self.focalTimeframeIndex = 0 # Initially focus is on leading edge of present
        self.targetTimeframeIndex = self.focalTimeframeIndex
        self.time_jaunt_length = 25 # How many turns max can you go back to from LEP
        self.messageQueue = []

    def placeObject(self, obj, position, timeframe):
        frame = self.timeframes[timeframe]
        tile = frame.zone.index[position]
        tile.add(obj)

    def removeObject(self, obj, position, timeframe):
        frame = self.timeframes[timeframe]
        tile = frame.zone.index[position]
        tile.remove(obj)

    def moveObject(self, obj, startPos, timeFrom, endPos, timeGo,):
        self.placeObject(obj, startPos, timeGo)
        self.removeObject(obj, endPos, timeFrom)

    def nextTurn(self):
        self.messageQueue = []
        self.timeframes[self.focalTimeframeIndex].play()
        if self.targetTimeframeIndex != self.focalTimeframeIndex:
            self.focalTimeframeIndex = self.targetTimeframeIndex
            self.targetTimeframeIndex = self.focalTimeframeIndex
            return

        if self.focalTimeframeIndex == 0: # If focalTimeframeIndex is at LEP...
            # Time moves forward from leading edge of present
            if len(self.timeframes) >= self.time_jaunt_length: # If too many timeframes...
                self.timeframes.pop(-1) # Remove furthest in past timeframe AND
            PreviousFrame = self.timeframes[0]
            NextFrame = Timeframe(self, (PreviousFrame.turn+1), PreviousFrame)
            self.timeframes.insert(0, NextFrame) # Add one more timeframe
        else: # If focalTimeframeIndex is NOT at LEP...
            self.focalTimeframeIndex -= 1
        self.targetTimeframeIndex = self.focalTimeframeIndex

    def indexInBounds(self, turn):
        return turn >= 0 and turn < len(self.timeframes)

    def changetargetTimeframeIndex(self, amount):
        target = self.targetTimeframeIndex + amount
        if self.indexInBounds(target):
            self.targetTimeframeIndex = target

    def timeline(self):
        timeBar = []
        for i in range(0, len(self.timeframes)):
            timeBar.append('o')
        if len(self.timeframes) < 25:
            for i in range(len(timeBar),25):
                timeBar.append('.')
        timeBar[self.focalTimeframeIndex] = '@'
        if self.targetTimeframeIndex != self.focalTimeframeIndex:
            timeBar[self.targetTimeframeIndex] = 'X'
        timeBar = timeBar[::-1] # Reverse timeBar
        timeBar.insert(0,'Time Gauge: (|')
        timeBar.append('|)')
        timeBar = "".join(timeBar)
        return timeBar

    def state(self, verbose = False):
        state = ''
        if not verbose:
            state = state + "| " + str(self.focalTimeframeIndex) \
            + " turns from LEP. " +  " | Current turn is " \
            + str(self.timeframes[self.focalTimeframeIndex].turn)
        else:
            state = state + "| " + str(self.focalTimeframeIndex) \
            + " turns from LEP. " + " | Current turn is " \
            + str(self.timeframes[self.focalTimeframeIndex].turn)\
            + " | Time advancing? " +  str(self.focalTimeframeIndex == 0) + " | "
        return state

    def turnContents(self):
        turns = []
        for t in self.timeframes:
            turns.insert(0,t.turn)
        return str(turns)

    @property
    def zone(self):
        return self.timeframes[self.focalTimeframeIndex].zone
    @property
    def timeframe(self):
        return self.timeframes[self.focalTimeframeIndex]

# zone and event container
class Timeframe():
    def __init__(self, Continuum, turn, PreviousFrame = None):
        self.continuum = Continuum
        self.turn = turn
        self.zone = None
        if PreviousFrame:
            self.zone = PreviousFrame.zone
        self.eventQueue = []
    def play(self):
        # Play/Replay turn, noting any changes, checking for collisons/paradoxes
        for event in self.eventQueue:
            event.resolve()

class Zone():
    def __init__(self, xSize = 20, ySize = 20):
        self.zoneMap = []
        self.index = dict() # Zone dict for lookup by (x,y) tuple
        self.xSize, self.ySize = xSize, ySize
        for y in range(0, ySize):
            for x in range(0, xSize):
                self.zoneMap.append(Tile(x, y))
        for t in self.zoneMap:
            self.index[(t.position.x,t.position.y)] = t

class Event():
    def __init__(self, timeframe, string = None):
        self.timeframe = timeframe
        self.string = string
    def resolve(self):
        if self.string:
            self.timeframe.continuum.messageQueue.append(self.string) # Ugly


class Player():
    def __init__(self, position, continuum, timeClone = False):
        self.continuum = continuum
        self.position = Position(position[0], position[1]) # TODO: Cleanup here
        self.visual = Visual(char = "@", color = libtcod.red)
        self.timeClone = timeClone
    @property
    def x(self):
        return self.position.x
    @property
    def y(self):
        return self.position.y

    def move(self, dx = 0, dy = 0): # Given int x,y in range (-1,1)
        x, y = self.x + dx, self.y + dy
        tile, msg = None, ''
        zone = self.continuum.zone
        if (x,y) in zone.index:  # If square exists:
            tile = zone.index[(x,y)]
        else:
            msg = "Player tried to move to non-existent square:" + str((x,y)) \
            + ".How ambitious is that!?"
        if tile:
            if self.continuum.focalTimeframeIndex != self.continuum.targetTimeframeIndex: # Lateral & Time move event
                msg = "Player tried to move through time to " + str((x,y)) + '.'
            else: # Lateral move event
                if dx == 0 and dy == 0:
                    msg = "Player stood still."
                else:
                    msg = "Player moved to " + str((x,y)) + '.'
            self.continuum.moveObject(self, (x,y), self.continuum.targetTimeframeIndex, (self.x, self.y), self.continuum.focalTimeframeIndex)
            self.x, self.y = x, y
        self.continuum.timeframe.eventQueue.append(Event(self.continuum.timeframe, msg))
            # If square not blocked:


        # Leave time clone


class Tile():
    def __init__(self, x, y, char = '.', color = libtcod.lightest_grey, back = libtcod.BKGND_NONE):
        self.position = Position(x, y)
        self.contents = []
        self.explored = False
        self.back = libtcod.BKGND_NONE
        self.visual = Visual(char, color)

    def add(self, item):
        self.contents.append(item)

    def remove(self,item):
        self.contents.remove(item)

    def getItem(self, item):
        for x in self.contents:
            if x is item:
                return x
                break
        return None

    def getItemType(self, type):
        for x in self.contents:
            if isinstance(x, type):
                return x
                break
        return None

    def containsPlayer(self):
        playerInside = False
        for x in self.contents:
            if isinstance(x, Player):
                playerInside = True
                break
        return playerInside

    @property
    def x(self):
        return self.position.x
    @property
    def y(self):
        return self.position.y
    @property
    def char(self):
        char = self.visual.char
        if self.containsPlayer():
            char = self.getItemType(Player).visual.char
        return char
    @property
    def color(self):
        color = self.visual.color
        if self.containsPlayer():
            color = self.getItemType(Player).visual.color
        return color

# Exercise
if __name__ == '__main__':
    c = Continuum()
    c.state(verbose = True)
    print "#####After advancing 30 turns...######"
    for i in range(0,30):
        c.nextTurn()
    print c.state(verbose = True)
    z = Zone()
    p = Player(0,0)
    t = z.index[(0,0)]
    t.add(p)
    print t.contents, t.containsPlayer
    print t.getItemType(Player)
    t.remove(p)
    print t.contents, t.containsPlayer()
    print t.getItem(p)

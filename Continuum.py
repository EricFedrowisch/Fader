# Fader v.0.2 # "Now with time and space!"
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
        self.focalTimeframe = 0 # Initially focus is on leading edge of present
        self.time_jaunt_length = 25 # How many turns max can you go back to from LEP
        self.targetTimeframe = self.focalTimeframe
        self.messageQueue = []

    def placeObject(self, obj, position, timeframe):
        frame = self.timeframes[timeframe]
        tile = frame.zone.index[position]
        tile.add(obj)

    def nextTurn(self):
        self.messageQueue = []
        self.timeframes[self.focalTimeframe].play()
        if self.targetTimeframe != self.focalTimeframe:
            self.focalTimeframe = self.targetTimeframe
            self.targetTimeframe = self.focalTimeframe
            return

        if self.focalTimeframe == 0: # If focalTimeframe is at LEP...
            # Time moves forward from leading edge of present
            if len(self.timeframes) >= self.time_jaunt_length: # If too many timeframes...
                self.timeframes.pop(-1) # Remove furthest in past timeframe AND
            PreviousFrame = self.timeframes[0]
            NextFrame = Timeframe(self, (PreviousFrame.turn+1), PreviousFrame)
            self.timeframes.insert(0, NextFrame) # Add one more timeframe
        else: # If focalTimeframe is NOT at LEP...
            self.focalTimeframe -= 1
        self.targetTimeframe = self.focalTimeframe

    def indexInBounds(self, turn):
        return turn >= 0 and turn < len(self.timeframes)

    def changeTargetTimeframe(self, amount):
        target = self.targetTimeframe + amount
        if self.indexInBounds(target):
            self.targetTimeframe = target

    def timeline(self):
        timeBar = []
        for i in range(0, len(self.timeframes)):
            timeBar.append('o')
        if len(self.timeframes) < 25:
            for i in range(len(timeBar),25):
                timeBar.append('.')
        timeBar[self.focalTimeframe] = '@'
        if self.targetTimeframe != self.focalTimeframe:
            timeBar[self.targetTimeframe] = 'X'
        timeBar = timeBar[::-1] # Reverse timeBar
        timeBar.insert(0,'Time Gauge: (|')
        timeBar.append('|)')
        timeBar = "".join(timeBar)
        return timeBar

    def state(self, verbose = False):
        state = ''
        if not verbose:
            state = state + "| " + str(self.focalTimeframe) \
            + " turns from LEP. " +  " | Current turn is " \
            + str(self.timeframes[self.focalTimeframe].turn)
        else:
            state = state + "| " + str(self.focalTimeframe) \
            + " turns from LEP. " + " | Current turn is " \
            + str(self.timeframes[self.focalTimeframe].turn)\
            + " | Time advancing? " +  str(self.focalTimeframe == 0) + " | "
        return state

    def turnContents(self):
        turns = []
        for t in self.timeframes:
            turns.insert(0,t.turn)
        return str(turns)

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
    def resolve(self,timeframe):
        if self.string:
            self.timeframe.continuum.messageQueue.append(self.string) # Ugly


class Player():
    def __init__(self, position, timeClone = False):
        self.position = Position(position[0], position[1]) # TODO: Cleanup here
        self.visual = Visual(char = "@", color = libtcod.red)
        self.timeClone = timeClone
    @property
    def x(self):
        return self.position.x
    @property
    def y(self):
        return self.position.y
    def move(self,x,y):
        pass


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

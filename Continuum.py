# Fader v.0.1
# Time travel roguelike tech demo
# Written by Eric Fedrowisch. All rights reserved.
# Jan.13, 2018: Basic class outlines begun and high level logic stubbed out.
#               Got time to run forward in a straight line.
# Jan. 14, 2018: Got one backward hop then resuming forward flow to work.
# Jan. 14, 2018: Got multiple backwards hops to work. Forward too.

import libtcodpy as libtcod

# Container class for timeframes
class Continuum():
    def __init__(self, zone = None):
        self.timeframes = []
        self.timeframes.append(Timeframe(self, 0)) #Create inital timeframe
        self.timeframes[0].zone = zone
        self.advance_time = True
        self.focalTimeframe = 0 # Initially focus is on leading edge of present
        self.time_jaunt_length = 25 # How many turns max can you go back to from LEP
        self.targetTimeframe = self.focalTimeframe

    #TODO: Fix Next Turn Logic
    def nextTurn(self):
        self.timeframes[self.focalTimeframe].play()

        if self.targetTimeframe != self.focalTimeframe:
            # Travel Forwards
            if self.targetTimeframe < self.focalTimeframe:
                t = abs(self.targetTimeframe - self.focalTimeframe)
                self.travelForward(t)
            # Travel Backwards
            elif self.targetTimeframe > self.focalTimeframe:
                t = (self.targetTimeframe - self.focalTimeframe)
                self.travelBack(t)
            #self.targetTimeframe = self.focalTimeframe

        if self.advance_time: # If focalTimeframe is at LEP...
            # Time moves forward from leading edge of present
            if len(self.timeframes) >= self.time_jaunt_length: # If too many timeframes...
                self.timeframes.pop(-1) # Remove furthest in past timeframe AND
                PreviousFrame = self.timeframes[0]
                NextFrame = Timeframe(self, (PreviousFrame.turn+1), PreviousFrame)
                self.timeframes.insert(0, NextFrame) # Add one more timeframe
            elif len(self.timeframes) >= 1: # If too few timeframes...
                PreviousFrame = self.timeframes[0]
                NextFrame = Timeframe(self, (PreviousFrame.turn+1), PreviousFrame)
                self.timeframes.insert(0, NextFrame) # Add one more timeframe
            self.focalTimeframe = 0
        else: # If focalTimeframe is NOT at LEP...
            # Replay past turn, noting any changes, checking for collisons/paradoxes
            if self.focalTimeframe == 0:
                self.advance_time = True
                #self.nextTurn() #Will this cause subtle bugs? I put it here to prevent dupe LEP turns, but not sure fixing one problem won't make others
            self.focalTimeframe -= 1

    def timeline(self):
        tLen = len(self.timeframes)
        timeBar = []
        print
        for i in range(0,tLen):
            timeBar.append('o')
        if tLen < 25:
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

    def changeTargetTimeframe(self, amount):
            target = self.targetTimeframe + amount
            if self.indexInBounds(target):
                self.targetTimeframe = target

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
            + " | Time advancing? " +  str(self.advance_time) + " | "
        return state

    def turnContents(self):
        turns = []
        for t in self.timeframes:
            turns.append(t.turn)
        return str(turns)

    def indexInBounds(self, turns):
        n = turns + self.focalTimeframe
        return n >= 0 and n < len(self.timeframes)

    def travelBack(self, turns):
        print "### Trying to travel back " + str(turns) + " turns. ###"
        if self.indexInBounds(turns):
            self.advance_time = False
            self.focalTimeframe += turns
        else:
            print "### Travel back failed. Out of bounds. ###"

    def travelForward(self, turns):
        print "### Trying to travel forward " + str(turns) + " turns. ###"
        if self.indexInBounds(turns * -1):
            self.focalTimeframe -= turns
            if self.focalTimeframe > 0:
                self.advance_time = False
            elif self.focalTimeframe == 0:
                self.advance_time = True
        else:
            print "### Travel forward failed. Out of bounds. ###"

# zone and event container
class Timeframe():
    def __init__(self, Continuum, turn, PreviousFrame = None):
        self.turn = turn
        self.zone = None
        if PreviousFrame:
            self.zone = PreviousFrame.zone
    def play(self):
        # Play/Replay turn, noting any changes, checking for collisons/paradoxes
        print("Playing turn " + str(self.turn))

class Zone():
    def __init__(self, xSize = 20, ySize = 20):
        self.zoneMap = []
        for y in range(0, ySize):
            for x in range(0, xSize):
                self.zoneMap.append(Tile(x, y))

class Object():
    def __init__(self, x, y, char = '.', color = libtcod.lightest_grey):
        self.x, self.y = x, y
        self.char = char
        self.color = color

class Tile(Object):
    def __init__(self, x, y, char = '.', color = libtcod.lightest_grey):
        Object.__init__(self, x, y, char, color)
        self.contents = []
        self.explored = False


# Exercise
if __name__ == '__main__':
    c = Continuum()
    c.state(verbose = True)
    print "#####After advancing 30 turns...######"
    for i in range(0,30):
        c.nextTurn()
    c.state(verbose = True)
    c.travelBack(15)
    for i in range(0,10):
        c.state()
        c.nextTurn()
    c.state(verbose = True)
    c.travelForward(15)
    c.state(verbose = True)
    c.travelBack(25)
    c.state(verbose = True)
    c.travelForward(3)
    c.state(verbose = True)
    for i in range(0,10):
        c.state()
        c.nextTurn()
    c.state(verbose = True)

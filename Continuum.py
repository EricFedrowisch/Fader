# Fader v.0.1
# Time travel roguelike tech demo
# Written by Eric Fedrowisch. All rights reserved.

import libtcodpy as libtcod

# Container class for timeframes
class Continuum():
    def __init__(self, zone = None):
        self.timeframes = []
        self.timeframes.append(Timeframe(self, 0)) #Create inital timeframe
        self.timeframes[0].zone = zone
        self.focalTimeframe = 0 # Initially focus is on leading edge of present
        self.time_jaunt_length = 25 # How many turns max can you go back to from LEP
        self.targetTimeframe = self.focalTimeframe

    #TODO: Fix Next Turn Logic
    def nextTurn(self):
        self.timeframes[self.focalTimeframe].play()
        if self.targetTimeframe != self.focalTimeframe:
            t = self.targetTimeframe - self.focalTimeframe
            if self.targetTimeframe < self.focalTimeframe:
                self.travel(-t) # Travel Forwards
            elif self.targetTimeframe > self.focalTimeframe:
                self.travel(t) # Travel Backwards

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
        #n = turns + self.focalTimeframe
        #print "Inbounds Check: n = ", n, n >= 0 and n < len(self.timeframes), "Turns = ", turns
        return turn >= 0 and turn < len(self.timeframes)

    def changeTargetTimeframe(self, amount):
        target = self.targetTimeframe + amount
        if self.indexInBounds(target):
            self.targetTimeframe = target
        print "Change target:", target

    def travel(self, turns):
        #print "### Trying to travel " + str(turns) + " turns. ###"
        if self.indexInBounds(turns):
            self.focalTimeframe += turns

    def timeline(self):
        tLen = len(self.timeframes)
        timeBar = []
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
        #turns = turns.reverse()
        return str(turns)

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

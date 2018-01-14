# Fader v.0.1
# Time travel roguelike tech demo
# Written by Eric Fedrowisch. All rights reserved.
# Jan.13, 2018: Basic class outlines begun and high level logic stubbed out.
#               Got time to run forward in a straight line.
# Jan. 14, 2018: Got one backward hop then resuming forward flow to work.
# Jan. 14, 2018: Got multiple backwards hops to work.
# Container class for timeframes
class Continuum():
    def __init__(self):
        self.timeframes = []
        self.advance_time = True
        self.focalTimeframe = 0 # Initially focus is on leading edge of present
        self.time_jaunt_length = 25 # How many turns max can you go back to from LEP
        self.leadingTurn = 0

    def state(self):
        print str(self.focalTimeframe) + " turns from LEP.", "Current turn is " \
        + str(self.timeframes[self.focalTimeframe].turn)

    def turnContents(self):
        turns = []
        for t in self.timeframes:
            turns.append(t.turn)
        return turns

    def nextTurn(self):
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
            else:
                self.timeframes.insert(0,Timeframe(self)) # Add first timeframe
            self.timeframes[self.focalTimeframe].play()
            self.leadingTurn +=1
            self.focalTimeframe = 0
        else: # If focalTimeframe is NOT at LEP...
            # Replay past turn, noting any changes, checking for collisons/paradoxes

            self.timeframes[self.focalTimeframe].play()
            if self.focalTimeframe > 0:
                self.focalTimeframe -= 1
            else:
                self.advance_time = True
                self.nextTurn() #Will this cause subtle bugs? I put it here to prevent dupe LEP turns, but not sure fixing one problem won't make others


# Map and event container
class Timeframe():
    def __init__(self, Continuum, turn, PreviousFrame = None):
        self.turn = turn
        self.map = None
        if PreviousFrame:
            self.map = PreviousFrame.map
    def play(self):
        # Play/Replay turn, noting any changes, checking for collisons/paradoxes
        pass

class Map():
    def __init__(self):
        pass

if __name__ == '__main__':
    c = Continuum()
    t1 = Timeframe(c, 0)
    c.timeframes.append(t1)
    print "Initial turns in Continuum:", c.turnContents()
    c.state()
    print "#####After advancing 30 turns...######"
    for i in range(0,30):
        c.nextTurn()
    print c.turnContents()
    print("###### Go back 5 turns #######")
    c.focalTimeframe += 5
    c.advance_time = False
    for i in range(0,3):
        c.state()
        c.nextTurn()
    print "Continuum so far:", c.turnContents()
    print "Time advancing?", c.advance_time
    print("###### Go forward 3 turns #######")
    c.focalTimeframe -= 3
    for i in range(0,5):
        c.state()
        c.nextTurn()
    print "Continuum so far:", c.turnContents()
    print "Time advancing?", c.advance_time
    for i in range(0,10):
        c.state()
        c.nextTurn()
    print "Continuum so far:", c.turnContents()
    print "Time advancing?", c.advance_time

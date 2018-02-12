import libtcodpy as libtcod
from continuum import *

#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
TITLE = 'Fader v.0.2.1' # "Now with time and space!"

class game():
    def __init__(self):
        self.debug = False
        self.exit = False
        #Initialize Continuum
        zone = Zone()
        self.continuum = Continuum(zone)
        pos = (10,10)
        self.player = Player(pos, continuum = self.continuum)
        self.continuum.placeObject(self.player, pos, self.continuum.focalTimeframeIndex)
        # Initialize Console
        self.font = libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        self.con  = libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, False)
        # Do main loop
        self.textQueue = []
        self.main()

    @property
    def timeframe(self):
        return self.continuum.timeframe#s[self.continuum.focalTimeframeIndex]
    @property
    def focalTimeframeIndex(self):
        return self.continuum.focalTimeframeIndex
    @property
    def targetTurn(self):
        return self.continuum.timeframes[self.continuum.targetTimeframeIndex].turn
    @property
    def zone(self):
        return self.timeframe.zone

    def main(self):
        while not libtcod.console_is_window_closed() and self.exit != True:
            self.draw()
            if (self.handle_keys()): #If player took turn
                self.continuum.nextTurn()
        print "Thanks for playing!"

    def draw(self):
        libtcod.console_clear(self.con) #Clear console
        self.drawUI()
        self.drawMap()
        libtcod.console_flush()

    def drawUI(self):
        turn = "Timeframe Turn: " + str(self.timeframe.turn) + ' ' \
        + "Focal Timeframe: " + str(self.continuum.focalTimeframeIndex) + ' ' \
        + "Target Timeframe: " + str(self.targetTurn)
        self.textQueue = []
        self.textQueue.extend([self.continuum.timeline(), turn])
        if self.debug:
            self.textQueue.extend([self.continuum.state(verbose = True), self.continuum.turnContents()])
        y = (SCREEN_HEIGHT/2) + (self.zone.ySize/2)
        self.textQueue.extend(self.continuum.messageQueue)
        for text in self.textQueue:
            x = SCREEN_WIDTH/2 - len(text)/2
            y = self.con_print(x, y + 1, text)

    def drawMap(self):
        xAdj = (SCREEN_WIDTH/2) - (self.zone.xSize/2)
        yAdj = (SCREEN_HEIGHT/2) - (self.zone.ySize/2)
        for tile in self.zone.tileList:
            libtcod.console_set_default_foreground(self.con, tile.color)
            libtcod.console_put_char(self.con, (tile.x + xAdj), (tile.y + yAdj), tile.char, tile.back)

    def con_print(self, x = 0, y=(SCREEN_HEIGHT-1), string = '', Color = None):
        if Color:
            libtcod.console_set_default_foreground(self.con, Color)
        else:
            libtcod.console_set_default_foreground(self.con, libtcod.lightest_grey)
        for char in string:
            x+= 1
            libtcod.console_put_char(self.con, x, y, char, libtcod.BKGND_NONE)
            if x >= (SCREEN_WIDTH - 1): #Really simplistic word wrap
                x,y = 0, y+1
        return y # Return last line drawn to

    def handle_keys(self):
        turnTaken = False

        key = libtcod.console_wait_for_keypress(True)

        # Alt+Enter: toggle fullscreen
        if key.vk == libtcod.KEY_ENTER and (key.lalt or key.ralt):
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        # Exit game
        elif key.vk == libtcod.KEY_ESCAPE:
            self.exit = True  #exit game
        # Pass Turn
        elif key.vk == libtcod.KEY_SPACE:
            turnTaken = True
            self.player.move(dx = 0, dy = 0)
        elif key.vk == libtcod.KEY_CHAR:
            # Timeframe targeting
            if key.c == ord('q') or key.c == ord('Q'):
                self.continuum.changetargetTimeframeIndex(1)
            elif key.c == ord('e') or key.c == ord('E'):
                self.continuum.changetargetTimeframeIndex(-1)
            # MOVEMENT
            elif key.c == ord('w') or key.c == ord('W') or \
            libtcod.console_is_key_pressed(libtcod.KEY_UP):
                turnTaken = True
                self.player.move(dx = 0, dy = -1) #player y -= 1
            elif key.c == ord('s') or key.c == ord('S') or \
            libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
                turnTaken = True
                self.player.move(dx = 0, dy = 1) #player y += 1
            elif key.c == ord('a') or key.c == ord('A') or \
            libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
                turnTaken = True
                self.player.move(dx = -1, dy = 0) #player x -= 1
            elif key.c == ord('d') or  key.c == ord('D') or \
            libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
                turnTaken = True
                self.player.move(dx = 1, dy = 0) #player x += 1
            # Debug keys
            elif key.c == ord('i') or key.c == ord('I'):
                self.debug = not self.debug
            elif key.c == ord('p') or key.c == ord('P'):
                turnTaken = True
                self.player.move(dx = -100, dy = -100)
        return turnTaken

    def drawHelp(self):
        pass

    def exit(self):
        pass

if __name__ == '__main__':
    GAME = game()

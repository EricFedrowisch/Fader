import libtcodpy as libtcod
import continuum as continuum

#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
TITLE = 'Fader v.0.1'

class game():
    def __init__(self):
        self.exit = False
        #Initialize Continuum
        zone = continuum.Zone()
        self.continuum = continuum.Continuum(zone)
        # Initialize Console
        self.font = libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        self.con  = libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, False)
        # Do main loop
        self.main()

    @property
    def timeframe(self):
        return self.continuum.timeframes[self.continuum.focalTimeframe]
    @property
    def focalTimeframe(self):
        return self.continuum.focalTimeframe
    @property
    def focalTurn(self):
        return self.continuum.timeframes[self.focalTimeframe].turn
    @property
    def targetTurn(self):
        return self.continuum.timeframes[self.continuum.targetTimeframe].turn
    @property
    def zone(self):
        return self.timeframe.zone.zoneMap

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
        turn = "Timeframe Turn: " + str(self.timeframe.turn) + ' '
        turn += "Focal Timeframe: " + str(self.focalTurn) + ' '
        turn += "Target Timeframe: " + str(self.targetTurn)
        self.con_print(string = turn)
        self.con_print(y=(SCREEN_HEIGHT-2), string = self.continuum.timeline())
        self.con_print(y=(SCREEN_HEIGHT-3), string = self.continuum.state(verbose = True))
        self.con_print(y=(SCREEN_HEIGHT-4), string = self.continuum.turnContents())


    def drawMap(self):
        for tile in self.zone:
            libtcod.console_set_default_foreground(self.con, tile.color)
            libtcod.console_put_char(self.con, tile.x, tile.y, tile.char, libtcod.BKGND_NONE)

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

    def handle_keys(self):
        turnTaken = False

        key = libtcod.console_wait_for_keypress(True)

        #Alt+Enter: toggle fullscreen
        if key.vk == libtcod.KEY_ENTER and (key.lalt or key.ralt):
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        elif key.vk == libtcod.KEY_ESCAPE:
            self.exit = True  #exit game

        elif key.vk == libtcod.KEY_SPACE: #Wait turn
            turnTaken = True
        elif key.vk == libtcod.KEY_CHAR:
            if key.c == ord('q') or key.c == ord('Q'):
                self.continuum.changeTargetTimeframe(1)
            elif key.c == ord('e') or key.c == ord('E'):
                self.continuum.changeTargetTimeframe(-1)
            elif key.c == ord('i') or key.c == ord('I'):
                self.continuum.state(verbose = True)
            '''
            elif key.c == ord('w'):
                playery -= 1
            elif key.c == ord('s'):
                playery += 1
            elif key.c == ord('a'):
                playerx -= 1
            elif key.c == ord('d'):
                playerx += 1
            '''
        return turnTaken
        '''# Arrow movement keys
        if libtcod.console_is_key_pressed(libtcod.KEY_UP):
            playery -= 1

        elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            playery += 1

        elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            playerx -= 1

        elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            playerx += 1
        '''

    def drawHelp(self):
        pass

    def exit(self):
        pass

if __name__ == '__main__':
    GAME = game()

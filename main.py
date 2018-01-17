import libtcodpy as libtcod
import continuum as continuum

#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
TITLE = 'Fader v.0.1'

class game():
    def __init__(self):
        self.exit = False
        # Initialize Console
        self.font = libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        self.con  = libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, False)
        #Initialize Continuum
        zone = continuum.Zone()
        self.continuum = continuum.Continuum(zone)
        # Do main loop
        self.main()

    @property
    def timeframe(self):
        return self.continuum.timeframes[self.continuum.focalTimeframe]

    @property
    def zone(self):
        return self.timeframe.zone.zoneMap

    def main(self):
        while not libtcod.console_is_window_closed() and self.exit != True:
            self.draw()
            #handle keys and exit game if needed
            self.handle_keys()
        print "Thanks for playing!"

    def draw(self):
        for tile in self.zone:
            libtcod.console_set_default_foreground(self.con, tile.color)
            libtcod.console_put_char(self.con, tile.x, tile.y, tile.char, libtcod.BKGND_NONE)


        #libtcod.console_set_default_foreground(0, libtcod.white)
        #libtcod.console_put_char(0, playerx, playery, '@', libtcod.BKGND_NONE)

        libtcod.console_flush()

        #libtcod.console_put_char(0, playerx, playery, ' ', libtcod.BKGND_NONE)

    def handle_keys(self):
        key = libtcod.console_wait_for_keypress(True)

        #Alt+Enter: toggle fullscreen
        if key.vk == libtcod.KEY_ENTER and (key.lalt or key.ralt):
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        elif key.vk == libtcod.KEY_ESCAPE:
            self.exit = True  #exit game

        #movement keys
        if libtcod.console_is_key_pressed(libtcod.KEY_UP):
            playery -= 1

        elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            playery += 1

        elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            playerx -= 1

        elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            playerx += 1

    def exit(self):
        pass

if __name__ == '__main__':
    GAME = game()

# Fader v.0.2 # "Now with time and space!"
# Time travel roguelike tech demo
# Written by Eric Fedrowisch. All rights reserved.

import libtcodpy as libtcod

class Position():
    def __init__(self, x, y):
        self.x, self.y = x, y

class Visual():
    def __init__(self, char, color):
        if color:
            self.char = char
        else:
            self.char = "."
        if color:
            self.color = color
        else:
            self.color = libtcod.lightest_grey

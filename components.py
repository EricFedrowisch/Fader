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

class Move():
    def __init__(self, object, initial_pos, end_pos):
        self.object = object
        self.initial_pos = Position(x = initial_pos[0], y = initial_pos[1])
        self.end_pos = Position(x = end_pos[0], y = end_pos[1])

class Pickup():
    def __init__(self, actor, item):
        self.actor = actor
        self.item = item

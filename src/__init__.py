# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Adventure import Adventure
from Creature import Creature
from Game import Game
import Inventory.CATEGORY
from Inventory import Item
from Settings import Settings

import pyglet


if __name__ == '__main__':
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(
        pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA
    )

    window = pyglet.window.Window(
        width=Settings.WIDTH, height=Settings.HEIGHT
    )

    game = Game(window)
    game.add_creature(Creature('First'))
    game.add_creature(Creature('Second'))
    game.add_creature(Creature('Third'))

    game.add_adventure(Adventure('First'))
    game.add_adventure(Adventure('Second'))
    game.add_adventure(Adventure('Third'))

    item = Item()
    item.name = 'Bird drumstick'
    item.add_food_component()
    item.quantity = 5
    game.inventory.add_item(item)

    item = Item()
    item.name = 'Weapon'
    item._categories.add(Inventory.CATEGORY.WEAPON)
    item.quantity = 2
    game.inventory.add_item(item)

    item = Item()
    item.name = 'Armor'
    item._categories.add(Inventory.CATEGORY.ARMOR)
    item.quantity = 1
    game.inventory.add_item(item)

    @window.event
    def on_draw():
        game.draw()

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        game.ui.mouse_motion(x, y)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            game.ui.click(x, y)

    pyglet.app.run()

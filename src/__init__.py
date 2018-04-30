# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Creature import Creature
from Settings import Settings

from ObjectManager import ObjectManager
from Game import Game
from ui import Ui

import pyglet


if __name__ == '__main__':
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(
        pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA
    )

    window = pyglet.window.Window(
        width=Settings.WIDTH, height=Settings.HEIGHT
    )

    object_manager = ObjectManager()
    object_manager.add_object('game', Game(window))
    object_manager.add_object('ui', Ui())

    ObjectManager.game.add_creature(Creature('RadicalTeapot'))

    # Add a sword and chestplate
    ObjectManager.game.inventory.add_items({
        'items.armor.chestplate': 1,
        'items.weapon.sword': 1,
        'items.utility.backpack': 1
    })

    @window.event
    def on_draw():
        ObjectManager.game.draw()

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        ObjectManager.ui.mouse_motion(x, y)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            ObjectManager.ui.click(x, y)

    @window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        ObjectManager.ui.scroll(x, y, scroll_y)

    pyglet.app.run()

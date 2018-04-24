# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Creature import Creature
from Settings import Settings

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

    ui = Ui()
    game = Game(window, ui)

    game.add_creature(Creature('RadicalTeapot'))

    # Add a sword and chestplate
    game.inventory.add_items({
        'items.armor.chestplate': 1,
        'items.weapon.sword': 1
    })

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

    @window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        game.ui.scroll(x, y, scroll_y)

    pyglet.app.run()

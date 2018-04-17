# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Creature import Creature
from Game import Game
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
    game.add_creature(Creature('RadicalTeapot'))

    game.inventory.add_items([(100, 1), (200, 1)])

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

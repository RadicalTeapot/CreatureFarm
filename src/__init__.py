# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Creature import Creature
from UI import AttributeLabel
from UI import Button
from UI import UI

from functools import partial
import pyglet
import random


def build_ui(creature):
    ui = UI()
    button = Button(125, 50, 150, 50, 'Feed')
    button.register_handler(partial(creature.eat, 10))
    ui.add_button(button)

    button = Button(325, 50, 150, 50, 'Sleep')
    button.register_handler(partial(creature.sleep, 10))
    ui.add_button(button)

    button = Button(525, 50, 150, 50, 'Adventure')
    button.register_handler(lambda: print('Adventure'))
    ui.add_button(button)

    label = AttributeLabel(600, 550, pre='HP:')
    ui.add_label(label)
    label = AttributeLabel(600, 525, pre='Strength:')
    ui.add_label(label)
    label = AttributeLabel(600, 500, pre='Agility:')
    ui.add_label(label)
    label = AttributeLabel(600, 475, pre='Stamina:')
    ui.add_label(label)
    label = AttributeLabel(600, 450, pre='Speed:')
    ui.add_label(label)
    label = AttributeLabel(600, 425, pre='Hunger:')
    ui.add_label(label)
    label = AttributeLabel(600, 400, pre='Sleep:')
    ui.add_label(label)

    return ui


if __name__ == '__main__':
    creature = Creature()
    ui = build_ui(creature)

    window = pyglet.window.Window(width=800, height=600)

    @window.event
    def on_draw():
        window.clear()

        # Draw ui bg
        pyglet.graphics.draw_indexed(
            4, pyglet.gl.GL_TRIANGLES,
            [0, 1, 2, 2, 1, 3],
            ('v2i', (
                550, 600,
                800, 600,
                550, 0,
                800, 0
            )),
            ('c3B', (
                40, 40, 40,
                40, 40, 40,
                40, 40, 40,
                40, 40, 40
            ))
        )
        pyglet.graphics.draw_indexed(
            4, pyglet.gl.GL_TRIANGLES,
            [0, 1, 2, 2, 1, 3],
            ('v2i', (
                0, 150,
                800, 150,
                0, 0,
                800, 0
            )),
            ('c3B', (
                30, 30, 30,
                30, 30, 30,
                30, 30, 30,
                30, 30, 30
            ))
        )

        ui.draw()

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            ui.click(x, y)

    pyglet.app.run()

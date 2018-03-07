# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Creature import Creature
from UI import AttributeLabel
from UI import Button
from UI import Panel
from UI import UI

from functools import partial
import pyglet


def build_ui(creature):
    ui = UI()
    # Right panel
    panel = Panel(550, 150, 250, 450)
    panel.set_layout(1)

    label = AttributeLabel(pre='HP:')
    panel.add_label(label)
    label = AttributeLabel(pre='Strength:')
    panel.add_label(label)
    label = AttributeLabel(pre='Agility:')
    panel.add_label(label)
    label = AttributeLabel(pre='Stamina:')
    panel.add_label(label)
    label = AttributeLabel(pre='Speed:')
    panel.add_label(label)
    label = AttributeLabel(pre='Hunger:')
    panel.add_label(label)
    label = AttributeLabel(pre='Sleep:')
    panel.add_label(label)

    ui.add_panel(panel)
    panel.show()

    # Bottom panel
    panel = Panel(0, 0, 800, 150)
    panel.set_layout(0)

    button = Button('(c) Creatures')
    # button.register_handler(partial(creature.eat, 10))
    panel.add_button(button)

    button = Button('(i) Inventory')
    # button.register_handler(lambda: print('Adventure'))
    panel.add_button(button)

    button = Button('(o) Cook')
    # button.register_handler(lambda: print('Adventure'))
    panel.add_button(button)

    button = Button('(b) Build')
    # button.register_handler(lambda: print('Adventure'))
    panel.add_button(button)

    button = Button('(f) Feed')
    # button.register_handler(partial(creature.sleep, 10))
    panel.add_button(button)

    button = Button('(e) Equip')
    # button.register_handler(partial(creature.sleep, 10))
    panel.add_button(button)

    button = Button('(m) Mutate')
    # button.register_handler(lambda: print('Adventure'))
    panel.add_button(button)

    button = Button('(a) Adventure')
    # button.register_handler(partial(creature.sleep, 10))
    panel.add_button(button)

    ui.add_panel(panel)
    panel.show()

    return ui


if __name__ == '__main__':
    creature = Creature()
    ui = build_ui(creature)

    window = pyglet.window.Window(width=800, height=600)

    @window.event
    def on_draw():
        window.clear()
        ui.draw()

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        ui.mouse_motion(x, y)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            ui.click(x, y)

    pyglet.app.run()

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

    label = AttributeLabel(15, panel.rect.height - 20, pre='HP:')
    panel.add_label(label)
    label = AttributeLabel(15, panel.rect.height - 45, pre='Strength:')
    panel.add_label(label)
    label = AttributeLabel(15, panel.rect.height - 70, pre='Agility:')
    panel.add_label(label)
    label = AttributeLabel(15, panel.rect.height - 95, pre='Stamina:')
    panel.add_label(label)
    label = AttributeLabel(15, panel.rect.height - 120, pre='Speed:')
    panel.add_label(label)
    label = AttributeLabel(15, panel.rect.height - 145, pre='Hunger:')
    panel.add_label(label)
    label = AttributeLabel(15, panel.rect.height - 170, pre='Sleep:')
    panel.add_label(label)

    ui.add_panel(panel)
    panel.show()

    # Bottom panel
    panel = Panel(0, 0, 800, 150)

    button = Button(20, panel.rect.height - 70, 150, 50, 'Creatures')
    # button.register_handler(partial(creature.eat, 10))
    panel.add_button(button)

    button = Button(180, panel.rect.height - 70, 150, 50, 'Inventory')
    # button.register_handler(lambda: print('Adventure'))
    panel.add_button(button)

    button = Button(340, panel.rect.height - 70, 150, 50, 'Cook')
    # button.register_handler(lambda: print('Adventure'))
    panel.add_button(button)

    button = Button(500, panel.rect.height - 70, 150, 50, 'Build')
    # button.register_handler(lambda: print('Adventure'))
    panel.add_button(button)

    button = Button(20, panel.rect.height - 130, 150, 50, 'Feed')
    # button.register_handler(partial(creature.sleep, 10))
    panel.add_button(button)

    button = Button(180, panel.rect.height - 130, 150, 50, 'Equip')
    # button.register_handler(partial(creature.sleep, 10))
    panel.add_button(button)

    button = Button(340, panel.rect.height - 130, 150, 50, 'Mutate')
    # button.register_handler(lambda: print('Adventure'))
    panel.add_button(button)

    button = Button(500, panel.rect.height - 130, 150, 50, 'Adventure')
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
    def on_mouse_release(x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            ui.click(x, y)

    pyglet.app.run()

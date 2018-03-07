# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Creature import Creature
from Game import Game
from UI import AttributeLabel
from UI import Button
from UI import Panel
from UI import UI

from functools import partial
import pyglet

WIDTH, HEIGHT = 800, 600


def build_ui(game):
    ui = UI()
    # Creatures panel
    creatures_panel = Panel(
        WIDTH // 2 - 200, HEIGHT // 2 - 250, 400, 500, True, 10
    )
    ui.add_panel(creatures_panel)

    # Right panel
    panel = Panel(WIDTH - 250, HEIGHT - 450, 250, 450)

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
    panel = Panel(0, 0, WIDTH, 150)

    button = Button(20, panel.rect.height - 70, '(c) Creatures')
    button.register_handler(partial(game.show_creatures, creatures_panel))
    panel.add_button(button)

    button = Button(180, panel.rect.height - 70, '(i) Inventory')
    # button.register_handler(lambda: print('Adventure'))
    panel.add_button(button)

    button = Button(340, panel.rect.height - 70, '(o) Cook')
    # button.register_handler(lambda: print('Adventure'))
    panel.add_button(button)

    button = Button(500, panel.rect.height - 70, '(b) Build')
    # button.register_handler(lambda: print('Adventure'))
    panel.add_button(button)

    button = Button(20, panel.rect.height - 130, '(f) Feed')
    # button.register_handler(partial(creature.sleep, 10))
    panel.add_button(button)

    button = Button(180, panel.rect.height - 130, '(e) Equip')
    # button.register_handler(partial(creature.sleep, 10))
    panel.add_button(button)

    button = Button(340, panel.rect.height - 130, '(m) Mutate')
    # button.register_handler(lambda: print('Adventure'))
    panel.add_button(button)

    button = Button(500, panel.rect.height - 130, '(a) Adventure')
    # button.register_handler(partial(creature.sleep, 10))
    panel.add_button(button)

    ui.add_panel(panel)
    panel.show()

    return ui


if __name__ == '__main__':
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(
        pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA
    )
    window = pyglet.window.Window(width=WIDTH, height=HEIGHT)

    game = Game()
    game.add_creature(Creature())
    game.add_creature(Creature())
    game.add_creature(Creature())
    ui = build_ui(game)

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

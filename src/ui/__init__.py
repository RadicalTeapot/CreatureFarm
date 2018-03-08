# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.Panel import Panel
from ui.Elements import AttributeLabel
from ui.Elements import Button

from Settings import Settings


class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, x, y):
        return (
            x >= self.x and y >= self.y and
            x <= self.x + self.width and
            y <= self.y + self.height
        )


class Ui(object):
    def __init__(self, game):
        self.game = game
        self.creature_panel = None
        self.right_panel = None
        self.bottom_panel = None
        self.build()

        self.panels = sorted([
            self.creature_panel,
            self.right_panel,
            self.bottom_panel
        ], key=lambda panel: panel.depth)

    def build(self):
        self.creature_panel = Panel(
            Settings.WIDTH // 2 - 200, Settings.HEIGHT // 2 - 250,
            400, 500, True, 10
        )
        self.creature_panel.add_tab(True, 'Creatures', 1)

        self.right_panel = Panel(
            Settings.WIDTH - 250, Settings.HEIGHT - 450, 250, 450
        )
        tab = self.right_panel.add_tab(True)

        self.right_panel.add_label(tab, AttributeLabel(self.game, 'name'))
        self.right_panel.add_label(
            tab, AttributeLabel(self.game, 'hp', pre='HP:')
        )
        self.right_panel.add_label(
            tab, AttributeLabel(self.game, 'strength', pre='Strength:')
        )
        self.right_panel.add_label(
            tab, AttributeLabel(self.game, 'agility', pre='Agility:')
        )
        self.right_panel.add_label(
            tab, AttributeLabel(self.game, 'stamina', pre='Stamina:')
        )
        self.right_panel.add_label(
            tab, AttributeLabel(self.game, 'speed', pre='Speed:')
        )
        self.right_panel.add_label(
            tab, AttributeLabel(self.game, 'hunger', pre='Hunger:')
        )
        self.right_panel.add_label(
            tab, AttributeLabel(self.game, 'tired', pre='Sleep:')
        )

        self.right_panel.show()

        self.bottom_panel = Panel(0, 0, Settings.WIDTH, 150)
        tab = self.bottom_panel.add_tab(True)

        button = Button('(c) Creatures')
        button.register_handler(self.game.show_creatures)
        self.bottom_panel.add_button(tab, button)

        button = Button('(i) Inventory')
        # button.register_handler(lambda: print('Adventure'))
        self.bottom_panel.add_button(tab, button)

        button = Button('(o) Cook')
        # button.register_handler(lambda: print('Adventure'))
        self.bottom_panel.add_button(tab, button)

        button = Button('(b) Build')
        # button.register_handler(lambda: print('Adventure'))
        self.bottom_panel.add_button(tab, button)

        button = Button('(f) Feed')
        # button.register_handler(partial(creature.sleep, 10))
        self.bottom_panel.add_button(tab, button)

        button = Button('(e) Equip')
        # button.register_handler(partial(creature.sleep, 10))
        self.bottom_panel.add_button(tab, button)

        button = Button('(m) Mutate')
        # button.register_handler(lambda: print('Adventure'))
        self.bottom_panel.add_button(tab, button)

        button = Button('(a) Adventure')
        button.register_handler(self.game.start_adventure)
        self.bottom_panel.add_button(tab, button)

        self.bottom_panel.show()

    def mouse_motion(self, x, y):
        for panel in self.panels:
            if panel.mouse_motion(x, y):
                break

    def click(self, x, y):
        for panel in self.panels:
            if panel.is_dialog and panel.click(x, y):
                return True

        for panel in self.panels:
            if not panel.is_dialog and panel.click(x, y):
                return True
        return False

    def draw(self):
        for panel in self.panels:
            panel.draw()

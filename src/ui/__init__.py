# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.Elements import Button
from ui.Elements import DescriptionLabel

from ui.Panel import Dialog
from ui.Panel import Panel

from Constants import ITEM_CATEGORY
from Constants import UI_BUTTON
from Constants import UI_STATE

from Settings import Settings

from functools import partial

import pyglet


class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (0, 0, 0)

        self.vertex_list = pyglet.graphics.vertex_list_indexed(
            4,
            [0, 1, 2, 2, 1, 3],
            ('v2i', self._build_vertices()),
            ('c3B', self._build_color())
        )

    def _build_vertices(self):
        return [
            self.x, self.y,
            self.x + self.width, self.y,
            self.x, self.y + self.height,
            self.x + self.width, self.y + self.height
        ]

    def _build_color(self):
        return [
            *self.color, *self.color, *self.color, *self.color
        ]

    def update_position(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.vertex_list.vertices = self._build_vertices()

    def update_color(self, color):
        self.color = color
        self.vertex_list.colors = self._build_color()

    def contains(self, x, y):
        return (
            x >= self.x and y >= self.y and
            x <= self.x + self.width and
            y <= self.y + self.height
        )

    def draw(self):
        self.vertex_list.draw(pyglet.gl.GL_TRIANGLES)


class UiState(object):
    def __init__(self, ui):
        self.ui = ui

    def enter(self):
        self.ui.left_panel.clear()
        self.ui.central_panel.clear()
        self.ui.right_panel.clear()

    @classmethod
    def refresh(cls, ui):
        return cls.enter()


class CreatureState(UiState):
    def __init__(self, ui):
        super().__init__(ui)
        self.selected_creature = None

    def enter(self):
        super().enter()

        if self.selected_creature is None and self.ui.game.creatures:
            self.selected_creature = self.ui.game.creatures[0]

        # Left panel
        tab = self.ui.left_panel.add_tab(True, 'Creatures', 1)
        buttons = []
        for creature in self.ui.game.creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(
                partial(self.select_creature, creature)
            )
            buttons.append(button)
            button.pressed = (creature == self.selected_creature)
        self.ui.left_panel.add_buttons(tab, buttons)

        # Central panel
        self.ui.central_panel.add_tab(True, 'Stats', 1)

        # Right panel
        self.ui.right_panel.add_tab(True, 'Description', 1)

        self.select_creature(self.selected_creature)

    def select_creature(self, creature):
        self.selected_creature = creature
        self.display_creature_stats()
        self.display_creature_description()

    def display_creature_stats(self):
        tab = self.ui.central_panel.get_tabs()[0]
        tab.clear()

        if self.selected_creature is None:
            return

        label = DescriptionLabel((
            'HP: {}/{}\n\n'
            'Melee: Lvl. {} ({} %)\n\n'
            'Marksmanship: Lvl. {} ({} %)\n\n'
            'Cooking: Lvl. {} ({} %)\n\n'
            'Building: Lvl. {} ({} %)\n\n'
        ).format(
            self.selected_creature.hp,
            self.selected_creature.max_hp,
            int(self.selected_creature.melee),
            int((
                self.selected_creature.melee -
                int(self.selected_creature.melee)
            ) * 100),
            int(self.selected_creature.marksmanship),
            int((
                self.selected_creature.marksmanship -
                int(self.selected_creature.marksmanship)
            ) * 100),
            int(self.selected_creature.cooking),
            int((
                self.selected_creature.cooking -
                int(self.selected_creature.cooking)
            ) * 100),
            int(self.selected_creature.building),
            int((
                self.selected_creature.building -
                int(self.selected_creature.building)
            ) * 100)
        ), tab.rect.width)
        tab.add_label(label)

    def display_creature_description(self):
        tab = self.ui.right_panel.get_tabs()[0]
        tab.clear()

        if self.selected_creature is None:
            return

        label = DescriptionLabel(
            self.selected_creature.get_description(), tab.rect.width
        )
        self.ui.right_panel.add_label(tab, label)


class NewAdventureState(UiState):
    def __init__(self, ui):
        super().__init__(ui)
        self.selected_creature = None
        self.selected_adventure = None

    def enter(self):
        super().enter()
        self.selected_creature = None
        self.selected_adventure = None

        self.ui.central_panel.add_tab(True, 'Adventures', 1)
        self.ui.right_panel.add_tab(True, 'Description', 1)

        # Left panel
        tab = self.ui.left_panel.add_tab(True, 'Creatures', 1)
        buttons = []
        for creature in self.ui.game.creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(
                partial(self.select_creature, creature)
            )
            buttons.append(button)
            button.pressed = (creature == self.selected_creature)
        self.ui.left_panel.add_buttons(tab, buttons)

    def select_creature(self, creature):
        self.selected_creature = creature

        tab = self.ui.central_panel.get_tabs()[0]
        tab.clear()
        buttons = []
        for adventure in self.ui.game.adventures:
            count = len([
                creature
                for creature in self.ui.game.creatures
                if creature.activity == adventure
            ])
            button = Button('{} ({})'.format(adventure.title, count))
            button.register_handler(
                partial(self.select_adventure, adventure)
            )
            buttons.append(button)
            button.pressed = (adventure == self.selected_adventure)
        self.ui.central_panel.add_buttons(tab, buttons)

    def select_adventure(self, adventure):
        self.selected_adventure = adventure

        tab = self.ui.right_panel.get_tabs()[0]
        tab.clear()
        label = DescriptionLabel(
            self.selected_adventure.get_description(), tab.rect.width
        )
        self.ui.right_panel.add_label(tab, label)
        if self.selected_adventure.is_available(self.selected_creature):
            button = Button('Start', False)
            button.register_handler(self.ui.game.start_adventure)
            self.ui.right_panel.add_button(tab, button)


class CurrentAdventureState(UiState):
    def __init__(self, ui):
        super().__init__(ui)
        self.selected_adventure = None
        self.selected_creature = None

    def enter(self):
        super().enter()
        # Left panel
        tab = self.ui.left_panel.add_tab(True, 'Adventures', 1)
        buttons = []
        for adventure in self.ui.game.adventures:
            count = len([
                creature
                for creature in self.ui.game.creatures
                if creature.activity == adventure
            ])
            if count == 0:
                continue
            button = Button('{} ({})'.format(adventure.title, count))
            button.register_handler(
                partial(self.select_adventure, adventure)
            )
            buttons.append(button)
            button.pressed = (adventure == self.selected_adventure)
        self.ui.left_panel.add_buttons(tab, buttons)

        # Central panel
        self.ui.central_panel.add_tab(True, 'Creatures', 1)

        # Right panel
        self.ui.right_panel.add_tab(True, 'Description', 1)

        if self.selected_adventure:
            self.select_adventure(self.selected_adventure)

    def select_adventure(self, adventure):
        self.selected_adventure = adventure

        creatures = [
            creature
            for creature in self.ui.game.creatures
            if creature.activity == adventure
        ]

        if (
            creatures and
            (
                self.selected_creature is None or
                self.selected_creature not in [
                    creature.id for creature in creatures
                ]
            )
        ):
            self.selected_creature = creatures[0].id

        tab = self.ui.central_panel.get_tabs()[0]
        tab.clear()
        buttons = []
        for creature in creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(
                partial(self.select_creature, creature.id)
            )
            buttons.append(button)
            button.pressed = (creature.id == self.selected_creature)
        self.ui.central_panel.add_buttons(tab, buttons)

        self.select_creature(self.selected_creature)

    def select_creature(self, creature_id):
        self.selected_creature = creature_id

        tab = self.ui.right_panel.get_tabs()[0]
        tab.clear()

        creature = [
            creature
            for creature in self.ui.game.creatures
            if creature.id == self.selected_creature
        ]
        if creature:
            creature = creature[0]
            label = DescriptionLabel((
                '{} turns left'.format(creature.timer)
            ), tab.rect.width)
            self.ui.right_panel.add_label(tab, label)


class InventoryState(UiState):
    def __init__(self, ui):
        super().__init__(ui)
        self.selected_category = None
        self.selected_item = None

    def enter(self):
        super().enter()

        tab = self.ui.left_panel.add_tab(True, 'Categories', 1)
        self.ui.central_panel.add_tab(True, 'Items', 1)
        self.ui.right_panel.add_tab(True, 'Description', 1)

        if self.selected_category is None:
            self.selected_category = ITEM_CATEGORY[0]

        for category in ITEM_CATEGORY:
            button = Button(category)
            button.register_handler(partial(self.select_category, category))
            self.ui.left_panel.add_button(tab, button)
            button.pressed = (self.selected_category == category)

        self.select_category(self.selected_category)

    def select_category(self, category):
        self.selected_category = category

        items = self.ui.game.inventory.get_items(self.selected_category)
        items = sorted(items, key=lambda item: item.name)

        if (
            items and (
                self.selected_item is None or
                self.selected_item not in [item.name for item in items]
            )
        ):
            self.selected_item = items[0].name
        elif not items:
            self.selected_item = None

        tab = self.ui.central_panel.get_tabs()[0]
        tab.clear()
        buttons = []
        for item in items:
            button = Button(item.name)
            button.register_handler(partial(self.select_item, item.name))
            button.pressed = (item.name == self.selected_item)
            buttons.append(button)
        self.ui.central_panel.add_buttons(tab, buttons)

        self.select_item(self.selected_item)

    def select_item(self, item):
        if self.selected_item is None:
            return

        self.selected_item = item

        item = [
            item
            for item in self.ui.game.inventory.get_items()
            if item.has_category(self.selected_category) and
            item.name == self.selected_item
        ]
        if not item:
            raise RuntimeError('Cannot find item')

        tab = self.ui.right_panel.get_tabs()[0]
        tab.clear()
        label = DescriptionLabel(item[0].get_description(), tab.rect.width)
        self.ui.right_panel.add_label(tab, label)


class CookState(UiState):
    def __init__(self, ui):
        super().__init__(ui)
        self.selected_creature = None
        self.selected_recipe = None

    def enter(self):
        super().enter()

        self.ui.central_panel.add_tab(True, 'Recipes', 1)
        self.ui.right_panel.add_tab(True, 'Description', 1)

        if self.selected_creature is None and self.ui.game.creatures:
            self.selected_creature = self.ui.game.creatures[0]

        tab = self.ui.left_panel.add_tab(True, 'Creatures', 1)
        buttons = []
        for creature in self.ui.game.creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(partial(self.select_creature, creature))
            buttons.append(button)
            button.pressed = (creature == self.selected_creature)
        self.ui.left_panel.add_buttons(tab, buttons)

        self.select_creature(self.selected_creature)

    def select_creature(self, creature):
        self.selected_creature = creature

        recipes = self.ui.game.inventory.get_recipes()
        if self.selected_recipe is None and recipes:
            self.selected_recipe = recipes[0]

        tab = self.ui.central_panel.get_tabs()[0]
        tab.clear()
        buttons = []
        # TODO: Display available recipes first then rest greyed out
        # recipe may not be available due to muissing ingredients or low
        # creature cooking skills
        for recipe in self.ui.game.inventory.get_recipes():
            name = recipe.name
            button = Button(name)
            button.register_handler(partial(self.select_recipe, recipe))
            buttons.append(button)
            button.pressed = (recipe == self.selected_recipe)
        self.ui.central_panel.add_buttons(tab, buttons)

        self.select_recipe(self.selected_recipe)

    def select_recipe(self, recipe):
        self.selected_recipe = recipe

        tab = self.ui.right_panel.get_tabs()[0]
        tab.clear()
        label = DescriptionLabel(recipe.get_description(), tab.rect.width)
        self.ui.right_panel.add_label(tab, label)
        if recipe.is_available(self.selected_creature):
            button = Button('Cook', False)
            button.register_handler(self.ui.game.start_cooking)
            self.ui.right_panel.add_button(tab, button)


class FeedState(UiState):
    def __init__(self, ui):
        super().__init__(ui)
        self.selected_creature = None
        self.selected_item = None

    def enter(self):
        super().enter()

        self.ui.central_panel.add_tab(True, 'Food', 1)
        self.ui.right_panel.add_tab(True, 'Description', 1)

        if self.selected_creature is None and self.ui.game.creatures:
            self.selected_creature = self.ui.game.creatures[0]

        tab = self.ui.left_panel.add_tab(True, 'Creatures', 1)
        buttons = []
        for creature in self.ui.game.creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(partial(self.select_creature, creature))
            buttons.append(button)
            button.pressed = (creature == self.selected_creature)
        self.ui.left_panel.add_buttons(tab, buttons)

        self.select_creature(self.selected_creature)

    def select_creature(self, creature):
        self.selected_creature = creature

        food = self.ui.game.inventory.get_items(ITEM_CATEGORY.FOOD)
        if self.selected_item is None and food:
            self.selected_item = food[0]

        tab = self.ui.central_panel.get_tabs()[0]
        tab.clear()
        buttons = []
        for item in food:
            name = item.name
            button = Button(name)
            button.register_handler(partial(self.select_item, item))
            buttons.append(button)
            button.pressed = (item == self.selected_item)
        self.ui.central_panel.add_buttons(tab, buttons)

        self.select_item(self.selected_item)

    def select_item(self, item):
        self.selected_item = item

        tab = self.ui.right_panel.get_tabs()[0]
        tab.clear()
        label = DescriptionLabel(item.get_description(), tab.rect.width)
        self.ui.right_panel.add_label(tab, label)

        button = Button('Eat', False)
        button.register_handler(self.ui.game.feed_creature)
        self.ui.right_panel.add_button(tab, button)


class Ui(object):
    def __init__(self, game):
        self.game = game

        UI_STATE.CREATURE = CreatureState(self)
        UI_STATE.NEW_ADVENTURE = NewAdventureState(self)
        UI_STATE.CURRENT_ADVENTURE = CurrentAdventureState(self)
        UI_STATE.INVENTORY = InventoryState(self)
        UI_STATE.COOK = CookState(self)
        UI_STATE.FEED = FeedState(self)

        self._state = UI_STATE.CREATURE

        self.dialogs = []
        self.panels = []

        self.callbacks = dict([
            (button, None) for button in UI_BUTTON
        ])

        self.register_callback(
            UI_BUTTON.CREATURE,
            partial(self.set_state, UI_STATE.CREATURE)
        )
        self.register_callback(
            UI_BUTTON.START_ADVENTURE,
            partial(self.set_state, UI_STATE.NEW_ADVENTURE)
        )
        self.register_callback(
            UI_BUTTON.CURRENT_ADVENTURE,
            partial(self.set_state, UI_STATE.CURRENT_ADVENTURE)
        )
        self.register_callback(
            UI_BUTTON.INVENTORY,
            partial(self.set_state, UI_STATE.INVENTORY)
        )
        self.register_callback(
            UI_BUTTON.COOK,
            partial(self.set_state, UI_STATE.COOK)
        )
        self.register_callback(
            UI_BUTTON.FEED,
            partial(self.set_state, UI_STATE.FEED)
        )

        self.build()

    def register_callback(self, button_type, method):
        if button_type not in UI_BUTTON:
            raise KeyError('Wrong button type')
        self.callbacks[button_type] = method

    def callback(self, button_type):
        if callable(self.callbacks[button_type]):
            self.callbacks[button_type]()

    def build(self):
        self.left_panel = Panel(0, Settings.HEIGHT - 450, 150, 445)
        self.central_panel = Panel(150, Settings.HEIGHT - 450, 250, 445)
        self.right_panel = Panel(
            400, Settings.HEIGHT - 450, Settings.WIDTH - 400, 445
        )
        self.bottom_panel = Panel(0, 0, Settings.WIDTH, 150)

        self.panels = [
            self.left_panel,
            self.central_panel,
            self.right_panel,
            self.bottom_panel
        ]

        self.refresh()
        self.build_bottom_ui()

    def refresh(self):
        self._state.enter()

    def build_bottom_ui(self):
        tab = self.bottom_panel.add_tab(True)

        creature_button = Button('(c) Creatures')
        self.bottom_panel.add_button(tab, creature_button)

        inventory_button = Button('(i) Inventory')
        self.bottom_panel.add_button(tab, inventory_button)

        cook_button = Button('(o) Cook')
        self.bottom_panel.add_button(tab, cook_button)

        build_button = Button('(b) Build')
        self.bottom_panel.add_button(tab, build_button)

        feed_button = Button('(f) Feed')
        self.bottom_panel.add_button(tab, feed_button)

        equip_button = Button('(e) Equip')
        self.bottom_panel.add_button(tab, equip_button)

        mutate_button = Button('(m) Mutate')
        self.bottom_panel.add_button(tab, mutate_button)

        start_adventure_button = Button('(s) Start Adventure')
        self.bottom_panel.add_button(tab, start_adventure_button)

        current_adventures_button = Button('(u) Current Adventures')
        self.bottom_panel.add_button(tab, current_adventures_button)

        finish_turn_button = Button('(t) Finish Turn', False)
        self.bottom_panel.add_button(tab, finish_turn_button)

        # Callbacks
        creature_button.register_handler(
            partial(self.callback, UI_BUTTON.CREATURE)
        )
        start_adventure_button.register_handler(
            partial(self.callback, UI_BUTTON.START_ADVENTURE)
        )
        current_adventures_button.register_handler(
            partial(self.callback, UI_BUTTON.CURRENT_ADVENTURE)
        )
        finish_turn_button.register_handler(
            partial(self.callback, UI_BUTTON.FINISH_TURN)
        )
        inventory_button.register_handler(
            partial(self.callback, UI_BUTTON.INVENTORY)
        )
        cook_button.register_handler(
            partial(self.callback, UI_BUTTON.COOK)
        )
        feed_button.register_handler(
            partial(self.callback, UI_BUTTON.FEED)
        )

    def display_dialog(self, text):
        self.dialogs.append(Dialog(text, self.close_dialog))

    def close_dialog(self):
        self.dialogs.pop()

    def set_state(self, state):
        self._state = state
        self.refresh()

    def mouse_motion(self, x, y):
        if self.dialogs:
            return self.dialogs[-1].mouse_motion(x, y)

        for panel in self.panels:
            panel.mouse_motion(x, y)

    def click(self, x, y):
        if self.dialogs:
            return self.dialogs[-1].click(x, y)

        for panel in self.panels:
            if panel.click(x, y):
                return True
        return False

    def draw(self):
        for panel in self.panels:
            panel.draw()

        if self.dialogs:
            self.dialogs[-1].draw()

# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.Elements import Button
from ui.Elements import DescriptionLabel

from ui.Panel import Dialog
from ui.Panel import Panel

from ui.Buffer import Buffer

from Constants import ACTIVITY_TYPE
from Constants import ITEM_CATEGORY
from Constants import UI_BUTTON
from Constants import UI_STATE

from ObjectManager import ObjectManager
from Settings import Settings

from functools import partial

import pyglet
import os


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
            ('c3B', self._build_color()),
            ('t2f', self._build_texture())
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

    def _build_texture(self):
        return [
            0, 0,
            1, 0,
            0, 1,
            1, 1
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
    def enter(self):
        ObjectManager.ui.left_panel.clear()
        ObjectManager.ui.central_panel.clear()
        ObjectManager.ui.right_panel.clear()

    @classmethod
    def refresh(cls):
        return cls.enter()


class CreatureState(UiState):
    def __init__(self):
        super().__init__()
        self.selected_creature = None

    def enter(self):
        super().enter()

        if self.selected_creature is None and ObjectManager.game.creatures:
            self.selected_creature = ObjectManager.game.creatures[0]

        # Left panel
        tab = ObjectManager.ui.left_panel.add_tab(True, 'Creatures', 1)
        buttons = []
        for creature in ObjectManager.game.creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(
                partial(self.select_creature, creature)
            )
            buttons.append(button)
            button.pressed = (creature == self.selected_creature)
        ObjectManager.ui.left_panel.add_buttons(tab, buttons)

        # Central panel
        ObjectManager.ui.central_panel.add_tab(True, 'Stats', 1)

        # Right panel
        ObjectManager.ui.right_panel.add_tab(True, 'Description', 1)

        self.select_creature(self.selected_creature)

    def select_creature(self, creature):
        self.selected_creature = creature
        self.display_creature_stats()
        self.display_creature_description()

    def display_creature_stats(self):
        tab = ObjectManager.ui.central_panel.get_tabs()[0]
        tab.clear()

        if self.selected_creature is None:
            return

        label = DescriptionLabel((
            'HP: {}/{}\n\n'
            '\n'
            'Strength: {}\n\n'
            'Melee: Lvl. {} ({} %)\n\n'
            'Marksmanship: Lvl. {} ({} %)\n\n'
            '\n'
            'Evasion: Lvl. {} ({} %)\n\n'
            'Armor: {}\n\n'
            '\n'
            'Cooking: Lvl. {} ({} %)\n\n'
            'Building: Lvl. {} ({} %)\n\n'
            '\n'
            'Inventory space: {} ({} total)\n\n'
        ).format(
            self.selected_creature.hp,
            self.selected_creature.max_hp,
            self.selected_creature.strength,
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
            int(self.selected_creature.evasion),
            int((
                self.selected_creature.evasion -
                int(self.selected_creature.evasion)
            ) * 100),
            self.selected_creature.armor,
            int(self.selected_creature.cooking),
            int((
                self.selected_creature.cooking -
                int(self.selected_creature.cooking)
            ) * 100),
            int(self.selected_creature.building),
            int((
                self.selected_creature.building -
                int(self.selected_creature.building)
            ) * 100),
            int(self.selected_creature.get_inventory_size_left()),
            int(self.selected_creature.inventory_size)
        ), tab.rect.width)
        tab.add_label(label)

    def display_creature_description(self):
        tab = ObjectManager.ui.right_panel.get_tabs()[0]
        tab.clear()

        if self.selected_creature is None:
            return

        label = DescriptionLabel(
            self.selected_creature.get_description(), tab.rect.width
        )
        ObjectManager.ui.right_panel.add_label(tab, label)


class NewAdventureState(UiState):
    def __init__(self):
        super().__init__()
        self.selected_creature = None
        self.selected_adventure = None

    def enter(self):
        super().enter()
        self.selected_creature = None
        self.selected_adventure = None

        ObjectManager.ui.central_panel.add_tab(True, 'Adventures', 1)
        ObjectManager.ui.right_panel.add_tab(True, 'Description', 1)

        # Left panel
        tab = ObjectManager.ui.left_panel.add_tab(True, 'Creatures', 1)
        buttons = []
        for creature in ObjectManager.game.creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(
                partial(self.select_creature, creature)
            )
            buttons.append(button)
            button.pressed = (creature == self.selected_creature)
        ObjectManager.ui.left_panel.add_buttons(tab, buttons)

    def select_creature(self, creature):
        self.selected_creature = creature

        tab = ObjectManager.ui.central_panel.get_tabs()[0]
        tab.clear()
        buttons = []
        for adventure_template in ObjectManager.game.adventure_templates:
            count = len([
                creature
                for creature in ObjectManager.game.creatures
                if creature.busy and
                creature.activity.activity_type == ACTIVITY_TYPE.ADVENTURE and
                creature.activity.template == adventure_template
            ])
            button = Button('{} ({})'.format(adventure_template.title, count))
            button.register_handler(
                partial(self.select_adventure, adventure_template)
            )
            buttons.append(button)
            button.pressed = (adventure_template == self.selected_adventure)
        ObjectManager.ui.central_panel.add_buttons(tab, buttons)

    def select_adventure(self, adventure_template):
        self.selected_adventure = adventure_template

        tab = ObjectManager.ui.right_panel.get_tabs()[0]
        tab.clear()
        label = DescriptionLabel(
            self.selected_adventure.get_description(), tab.rect.width
        )
        ObjectManager.ui.right_panel.add_label(tab, label)
        if self.selected_adventure.is_available(self.selected_creature):
            button = Button('Start', False)
            button.register_handler(ObjectManager.game.start_adventure)
            ObjectManager.ui.right_panel.add_button(tab, button)


class CurrentAdventureState(UiState):
    def __init__(self):
        super().__init__()
        self.selected_adventure = None
        self.selected_creature = None

    def enter(self):
        super().enter()
        # Left panel
        tab = ObjectManager.ui.left_panel.add_tab(True, 'Adventures', 1)
        buttons = []
        for adventure_template in ObjectManager.game.adventure_templates:
            count = len([
                creature
                for creature in ObjectManager.game.creatures
                if creature.busy and
                creature.activity.activity_type == ACTIVITY_TYPE.ADVENTURE and
                creature.activity.template == adventure_template
            ])
            if count == 0:
                continue
            button = Button('{} ({})'.format(adventure_template.title, count))
            button.register_handler(
                partial(self.select_adventure, adventure_template)
            )
            buttons.append(button)
            button.pressed = (adventure_template == self.selected_adventure)
        ObjectManager.ui.left_panel.add_buttons(tab, buttons)

        # Central panel
        ObjectManager.ui.central_panel.add_tab(True, 'Creatures', 1)

        # Right panel
        ObjectManager.ui.right_panel.add_tab(True, 'Description', 1)

        if self.selected_adventure:
            self.select_adventure(self.selected_adventure)

    def select_adventure(self, adventure_template):
        self.selected_adventure = adventure_template

        creatures = [
            creature
            for creature in ObjectManager.game.creatures
            if creature.activity.activity_type == ACTIVITY_TYPE.ADVENTURE and
            creature.activity.template == adventure_template
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

        tab = ObjectManager.ui.central_panel.get_tabs()[0]
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
        ObjectManager.ui.central_panel.add_buttons(tab, buttons)

        self.select_creature(self.selected_creature)

    def select_creature(self, creature_id):
        self.selected_creature = creature_id

        tab = ObjectManager.ui.right_panel.get_tabs()[0]
        tab.clear()

        creature = [
            creature
            for creature in ObjectManager.game.creatures
            if creature.id == self.selected_creature
        ]
        if not creature:
            return

        creature = creature[0]
        # TODO: Display how many turns passed (and maybe other info) as
        # description label

        # Only recal if creature current activity is adventure (not in a fight
        # or other sub-activity)
        if (
            creature.activity and
            creature.activity.activity == self.selected_adventure
        ):
            button = Button('Recall', False)
            button.register_handler(creature.free)
            ObjectManager.ui.right_panel.add_button(tab, button)
        else:
            label = DescriptionLabel('Cannot recall', tab.rect.width)
            ObjectManager.ui.right_panel.add_label(tab, label)


class InventoryState(UiState):
    def __init__(self):
        super().__init__()
        self.selected_category = None
        self.selected_item = None

    def enter(self):
        super().enter()

        tab = ObjectManager.ui.left_panel.add_tab(True, 'Categories', 1)
        ObjectManager.ui.central_panel.add_tab(True, 'Items', 1)
        ObjectManager.ui.right_panel.add_tab(True, 'Description', 1)

        if self.selected_category is None:
            self.selected_category = ITEM_CATEGORY.FOOD

        for category in ITEM_CATEGORY:
            button = Button(category.value)
            button.register_handler(partial(self.select_category, category))
            ObjectManager.ui.left_panel.add_button(tab, button)
            button.pressed = (self.selected_category == category)

        self.select_category(self.selected_category)

    def select_category(self, category):
        self.selected_category = category

        items = ObjectManager.game.inventory.get_items(self.selected_category)
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

        tab = ObjectManager.ui.central_panel.get_tabs()[0]
        tab.clear()
        buttons = []
        for item in items:
            button = Button(item.name)
            button.register_handler(partial(self.select_item, item.name))
            button.pressed = (item.name == self.selected_item)
            buttons.append(button)
        ObjectManager.ui.central_panel.add_buttons(tab, buttons)

        self.select_item(self.selected_item)

    def select_item(self, item):
        if self.selected_item is None:
            return

        self.selected_item = item

        item = [
            item
            for item in ObjectManager.game.inventory.get_items(
                self.selected_category
            )
            if item.name == self.selected_item
        ]
        if not item:
            raise RuntimeError('Cannot find item')

        tab = ObjectManager.ui.right_panel.get_tabs()[0]
        tab.clear()
        label = DescriptionLabel(item[0].get_description(), tab.rect.width)
        ObjectManager.ui.right_panel.add_label(tab, label)


class CookState(UiState):
    def __init__(self):
        super().__init__()
        self.selected_creature = None
        self.selected_recipe = None

    def enter(self):
        super().enter()

        ObjectManager.ui.central_panel.add_tab(True, 'Recipes', 1)
        ObjectManager.ui.right_panel.add_tab(True, 'Description', 1)

        if self.selected_creature is None and ObjectManager.game.creatures:
            self.selected_creature = ObjectManager.game.creatures[0]

        tab = ObjectManager.ui.left_panel.add_tab(True, 'Creatures', 1)
        buttons = []
        for creature in ObjectManager.game.creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(partial(self.select_creature, creature))
            buttons.append(button)
            button.pressed = (creature == self.selected_creature)
        ObjectManager.ui.left_panel.add_buttons(tab, buttons)

        self.select_creature(self.selected_creature)

    def select_creature(self, creature):
        self.selected_creature = creature

        recipes = ObjectManager.game.inventory.get_recipes()
        if self.selected_recipe is None and recipes:
            self.selected_recipe = recipes[0]

        tab = ObjectManager.ui.central_panel.get_tabs()[0]
        tab.clear()
        buttons = []
        # TODO: Display available recipes first then rest greyed out
        # recipe may not be available due to muissing ingredients or low
        # creature cooking skills
        for recipe in ObjectManager.game.inventory.get_recipes():
            name = recipe.name
            button = Button(name)
            button.register_handler(partial(self.select_recipe, recipe))
            buttons.append(button)
            button.pressed = (recipe == self.selected_recipe)
        ObjectManager.ui.central_panel.add_buttons(tab, buttons)

        self.select_recipe(self.selected_recipe)

    def select_recipe(self, recipe):
        self.selected_recipe = recipe

        tab = ObjectManager.ui.right_panel.get_tabs()[0]
        tab.clear()
        label = DescriptionLabel(recipe.get_description(), tab.rect.width)
        ObjectManager.ui.right_panel.add_label(tab, label)
        if recipe.is_available(self.selected_creature):
            button = Button('Cook', False)
            button.register_handler(ObjectManager.game.start_cooking)
            ObjectManager.ui.right_panel.add_button(tab, button)


class FeedState(UiState):
    def __init__(self):
        super().__init__()
        self.selected_creature = None
        self.selected_item = None

    def enter(self):
        super().enter()

        ObjectManager.ui.central_panel.add_tab(True, 'Food', 1)
        ObjectManager.ui.right_panel.add_tab(True, 'Description', 1)

        if self.selected_creature is None and ObjectManager.game.creatures:
            self.selected_creature = ObjectManager.game.creatures[0]

        tab = ObjectManager.ui.left_panel.add_tab(True, 'Creatures', 1)
        buttons = []
        for creature in ObjectManager.game.creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(partial(self.select_creature, creature))
            buttons.append(button)
            button.pressed = (creature == self.selected_creature)
        ObjectManager.ui.left_panel.add_buttons(tab, buttons)

        self.select_creature(self.selected_creature)

    def select_creature(self, creature):
        self.selected_creature = creature

        food = ObjectManager.game.inventory.get_items(ITEM_CATEGORY.FOOD)
        if self.selected_item is None and food:
            self.selected_item = food[0]

        tab = ObjectManager.ui.central_panel.get_tabs()[0]
        tab.clear()
        buttons = []
        for item in food:
            name = item.name
            button = Button(name)
            button.register_handler(partial(self.select_item, item))
            buttons.append(button)
            button.pressed = (item == self.selected_item)
        ObjectManager.ui.central_panel.add_buttons(tab, buttons)

        if self.selected_item is not None:
            self.select_item(self.selected_item)

    def select_item(self, item):
        self.selected_item = item

        tab = ObjectManager.ui.right_panel.get_tabs()[0]
        tab.clear()
        label = DescriptionLabel(item.get_description(), tab.rect.width)
        ObjectManager.ui.right_panel.add_label(tab, label)

        button = Button('Eat', False)
        button.register_handler(ObjectManager.game.start_feeding)
        ObjectManager.ui.right_panel.add_button(tab, button)


class EquipState(UiState):
    def __init__(self):
        super().__init__()
        self.selected_creature = None
        self.selected_item = None

    def enter(self):
        super().enter()

        ObjectManager.ui.central_panel.add_tab(True, "Items", 1)
        ObjectManager.ui.right_panel.add_tab(True, "Compare", 1)

        if self.selected_creature is None and ObjectManager.game.creatures:
            self.selected_creature = ObjectManager.game.creatures[0]

        tab = ObjectManager.ui.left_panel.add_tab(True, 'Creatures', 1)
        buttons = []
        for creature in ObjectManager.game.creatures:
            name = creature.name
            button = Button(name)
            button.register_handler(partial(self.select_creature, creature))
            buttons.append(button)
            button.pressed = (creature == self.selected_creature)
        ObjectManager.ui.left_panel.add_buttons(tab, buttons)

        if self.selected_creature is not None:
            self.select_creature(self.selected_creature)

    def select_creature(self, creature):
        self.selected_creature = creature

        tab = ObjectManager.ui.central_panel.get_tabs()[0]
        tab.clear()

        # TODO: Put weapons and armors in different tabs

        # TODO: Instead of filtering out equiped item, show them greyed out
        # and ask the user if they want to unequip it for the original creature
        # to equip it to the selected one
        weapons = [
            item
            for item in ObjectManager.game.inventory.get_items(
                ITEM_CATEGORY.WEAPON
            )
            if not item.equiped
        ]
        if self.selected_item is None and weapons:
            self.selected_item = weapons[0]

        buttons = []
        for item in weapons:
            name = item.name
            button = Button(name)
            button.register_handler(partial(self.select_item, item))
            buttons.append(button)
            button.pressed = (item == self.selected_item)

        armors = [
            item
            for item in ObjectManager.game.inventory.get_items(
                ITEM_CATEGORY.ARMOR
            )
            if not item.equiped
        ]
        for item in armors:
            name = item.name
            button = Button(name)
            button.register_handler(partial(self.select_item, item))
            buttons.append(button)
            button.pressed = (item == self.selected_item)

        ObjectManager.ui.central_panel.add_buttons(tab, buttons)

        if self.selected_item is not None:
            self.select_item(self.selected_item)

    def select_item(self, item):
        self.selected_item = item

        tab = ObjectManager.ui.right_panel.get_tabs()[0]
        tab.clear()

        body_part = self.selected_item.body_part

        equiped = self.selected_creature.equipment[body_part]
        description = 'Equiped :\n\n'
        if equiped:
            description += equiped.get_description()
        else:
            description += 'Nothing'
        description += '\n\nSelected :\n\n{}'.format(
            self.selected_item.get_description()
        )
        label = DescriptionLabel(description, tab.rect.width)
        ObjectManager.ui.right_panel.add_label(tab, label)

        button = Button('Equip', False)
        button.register_handler(ObjectManager.game.equip_item)
        ObjectManager.ui.right_panel.add_button(tab, button)


class LoadState(UiState):
    def __init__(self):
        super().__init__()

    def enter(self):
        super().enter()

        tab = ObjectManager.ui.left_panel.add_tab(True, 'Files', 1)
        buttons = []
        for save_file in os.listdir(os.path.abspath(Settings.SAVE_FOLDER)):
            button = Button(save_file, False)
            button.register_handler(partial(self.select_file, save_file))
            buttons.append(button)
        ObjectManager.ui.left_panel.add_buttons(tab, buttons)

    def select_file(self, save_file):
        ObjectManager.game.load(os.path.normpath(os.path.join(
            os.path.abspath(Settings.SAVE_FOLDER), save_file
        )))


class Ui(object):
    def __init__(self):
        self.dialogs = []
        self.panels = []

        self.create_states()
        self.create_callbacks()
        self.buffer = Buffer()

    def create_callbacks(self):
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
        self.register_callback(
            UI_BUTTON.EQUIP,
            partial(self.set_state, UI_STATE.EQUIP)
        )
        self.register_callback(
            UI_BUTTON.LOAD,
            partial(self.set_state, UI_STATE.LOAD)
        )

        self.register_callback(
            UI_BUTTON.FINISH_TURN, ObjectManager.game.update
        )
        self.register_callback(
            UI_BUTTON.SAVE, ObjectManager.game.save
        )

    def create_states(self):
        UI_STATE.CREATURE = CreatureState()
        UI_STATE.NEW_ADVENTURE = NewAdventureState()
        UI_STATE.CURRENT_ADVENTURE = CurrentAdventureState()
        UI_STATE.INVENTORY = InventoryState()
        UI_STATE.COOK = CookState()
        UI_STATE.FEED = FeedState()
        UI_STATE.EQUIP = EquipState()
        UI_STATE.LOAD = LoadState()

        self._state = UI_STATE.CREATURE

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
        tab = self.bottom_panel.add_tab(True, content_wrap=True)

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

        load_button = Button('(l) Load', False)
        self.bottom_panel.add_button(tab, load_button)

        save_button = Button('(v) Save', False)
        self.bottom_panel.add_button(tab, save_button)

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
        equip_button.register_handler(
            partial(self.callback, UI_BUTTON.EQUIP)
        )
        load_button.register_handler(
            partial(self.callback, UI_BUTTON.LOAD)
        )
        save_button.register_handler(
            partial(self.callback, UI_BUTTON.SAVE)
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

    def scroll(self, x, y, scroll):
        if self.dialogs:
            return self.dialogs[-1].scroll(x, y, scroll)

        for panel in self.panels:
            if panel.scroll(x, y, scroll):
                return True
        return False

    def draw(self):
        for panel in self.panels:
            panel.draw()

        if self.dialogs:
            # TODO: Draw a semi-transparent black rect over the image if
            # some dialogs have to be shown

            # TODO: Loop on sorted dialogs by depth and draw all of them
            self.dialogs[-1].draw()

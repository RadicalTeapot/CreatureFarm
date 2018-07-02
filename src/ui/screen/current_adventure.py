# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.screen import UiState
from ui.widget.widgets import ListEntry

from ObjectManager import ObjectManager
from functools import partial


class CurrentAdventureModel:
    def __init__(self):
        self.running_adventures = {}
        self.selected_adventure = ''
        self.selected_creature = ''
        self.log = None


class CurrentAdventure(UiState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._model = CurrentAdventureModel()

        # ################################################################### #
        #                            Ui bindings                              #
        # ################################################################### #
        self.adventure_spinner.bind(
            text=lambda spinner, value: self.adventure_selected(value)
        )
        self.creature_spinner.bind(
            text=lambda spinner, value: self.creature_selected(value)
        )
        self.recall.bind(on_press=self.end_adventure)

    def __enter__(self):
        self.adventure_selected()
        self.creature_selected()
        self.load_log()
        return self

    def adventure_selected(self, name=''):
        self._model.selected_adventure = name
        adventures = ObjectManager.game.running_adventures.get(
            self._model.selected_adventure, []
        )
        self._model.running_adventures = {
            adventure.group_name: adventure
            for adventure in adventures
        }
        self.update_ui()

    def creature_selected(self, name=''):
        self._model.selected_creature = name
        self.load_log()
        self.load_creatures()
        self.update_ui()

    def load_creatures(self):
        # TODO unbind on_tool_tip from buttons before clearing the list
        self.creature_list.clear()
        adventure = self._model.running_adventures.get(
            self._model.selected_creature,
            None
        )
        if adventure is None:
            return
        for creature in adventure.creatures:
            entry = ListEntry.simple(creature.template_name)
            entry.set_tool_tip(creature.template_name)
            entry.bind(on_tool_tip=partial(
                self.update_tool_tip, creature
            ))
            self.creature_list.append(entry)

    def update_tool_tip(self, creature, entry):
        alive = '[color=#55FF55]Alive[/color]'
        if creature.is_dead():
            alive = '[color=#FF2222]Dead[/color]'
        entry.set_tool_tip(
            f'Name: {creature.template_name} ({alive})\n'
            f'HP: {creature.stats["hp"]:.1f}/{creature.stats["max_hp"]:.1f}\n'
            f'Biomass: {creature.stats["held_biomass"]:.1f}/'
            f'{creature.stats["max_biomass"]:.1f}'
        )
        pass

    def load_log(self):
        adventure = self._model.running_adventures.get(
            self._model.selected_creature,
            None
        )
        if self._model.log:
            self._model.log.deregister_callback('current_adventure')
            self._model.log = None
        if adventure:
            self._model.log = adventure.log
            self._model.log.register_callback(
                'current_adventure', self.update_log
            )
        self.update_log()

    def end_adventure(self, button):
        adventure = self._model.running_adventures.get(
            self._model.selected_creature,
            None
        )
        if adventure is None:
            return
        ObjectManager.game.end_adventure(adventure)

        self.creature_selected()
        self.load_log()

    def update_ui(self):
        self.adventure_spinner.values = (
            ObjectManager.game.running_adventures.keys()
        )
        self.adventure_spinner.text = self._model.selected_adventure
        self.creature_spinner.values = self._model.running_adventures.keys()
        self.creature_spinner.text = self._model.selected_creature
        self.update_log()

    def update_log(self, entry=None):
        if self._model.log is not None:
            self.description = '\n'.join([
                str(entry) for entry in self._model.log.get_log()
            ])
        else:
            self.description = ''

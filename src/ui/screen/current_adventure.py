# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.screen import UiState

from ObjectManager import ObjectManager


class CurrentAdventureModel:
    def __init__(self):
        self.adventures = {}
        self.creatures = {}
        self.selected_adventure = ''
        self.selected_creature = ''
        self.log = ''


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

    def __enter__(self):
        self.update_adventures()
        self.adventure_selected()
        self.creature_selected()
        return self

    def update_adventures(self):
        data = ObjectManager.game.get_running_adventures().items()
        self._model.adventures = {
            key: value
            for key, value in data
        }

    def adventure_selected(self, name=''):
        self._model.selected_adventure = name
        adventures = self._model.adventures.get(
            self._model.selected_adventure, []
        )
        self._model.creatures = {
            adventure.creatures_name: adventure
            for adventure in adventures
        }
        self.update_ui()

    def creature_selected(self, name=''):
        self._model.selected_creature = name
        self.load_log()
        self.update_ui()

    def load_log(self):
        adventure = self._model.creatures.get(
            self._model.selected_creature,
            None
        )
        if adventure:
            self._model.log = f'{self._model.selected_creature} {adventure.log}'

    def update_ui(self):
        self.adventure_spinner.values = self._model.adventures.keys()
        self.adventure_spinner.text = self._model.selected_adventure
        self.creature_spinner.values = self._model.creatures.keys()
        self.creature_spinner.text = self._model.selected_creature

        self.description = self._model.log

# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.screen import UiState

from ObjectManager import ObjectManager


class CurrentAdventureModel:
    def __init__(self):
        self.creatures = {}
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

    def __enter__(self):
        self.adventure_selected()
        self.creature_selected()
        return self

    def adventure_selected(self, name=''):
        self._model.selected_adventure = name
        adventures = ObjectManager.game.running_adventures.get(
            self._model.selected_adventure, []
        )
        self._model.creatures = {
            adventure.group_name: adventure
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
            if self._model.log:
                self._model.log.deregister_callback('current_adventure')
            self._model.log = adventure.log
            self._model.log.register_callback(
                'current_adventure', self.update_log
            )

    def update_ui(self):
        self.adventure_spinner.values = (
            ObjectManager.game.running_adventures.keys()
        )
        self.adventure_spinner.text = self._model.selected_adventure
        self.creature_spinner.values = self._model.creatures.keys()
        self.creature_spinner.text = self._model.selected_creature
        self.update_log()

    def update_log(self, entry=None):
        if self._model.log is not None:
            self.description = '\n'.join([
                str(entry) for entry in self._model.log.get_log()
            ])
        else:
            self.description = ''

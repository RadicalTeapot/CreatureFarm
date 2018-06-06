# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.screen import UiState


class CurrentAdventureModel:
    def __init__(self):
        self.all_creatures = {}
        self.selected_creature = ''


class CurrentAdventure(UiState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._model = CurrentAdventureModel()

        # ################################################################### #
        #                            Ui bindings                              #
        # ################################################################### #
        self.creature_spinner.bind(
            text=lambda spinner, value: self.creature_selected(value)
        )

    def __enter__(self):
        self.update_creatures()
        self.creature_selected()
        return self

    def update_creatures(self):
        # TODO Get template and group list from game and populate model dict
        # with it instead of using dummy data
        self._model.all_creatures = {
            'A': None,
            'B': None,
            'C': None,
        }

    def creature_selected(self, name=''):
        self._model.selected_creature = name
        self.update_ui()

    def update_ui(self):
        self.creature_spinner.values = self._model.all_creatures.keys()
        self.creature_spinner.text = self._model.selected_creature

        # TODO load and display log here
        self.description.text = (
            f'{self._model.selected_creature} placeholder log'
        )

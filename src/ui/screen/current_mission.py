# -*- coding: utf-8 -*-
"""DOCSTRING."""

from kivy.properties import ObjectProperty

from ui.screen import UiState


class CurrentMission(UiState):
    spinner = ObjectProperty()
    description = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        values = ['a', 'b', 'c']
        self.spinner.values = values
        self.spinner.text = values[0]

        self.spinner.bind(text=self.select_mission)
        self.select_mission(self.spinner, values[0])

    def select_mission(self, spinner, value):
        print(f'Mission {value} selected')
        self.description.text = '\n'.join([f'Mission {value}'] * 5)

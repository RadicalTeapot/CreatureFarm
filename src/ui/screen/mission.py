# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.screen import UiState
from ui.widget.widgets import ListEntry

from kivy.properties import ObjectProperty

from functools import partial


class Mission(UiState):
    left_panel = ObjectProperty()
    mission_label = ObjectProperty()
    creature_spinner = ObjectProperty()
    start_button = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.selected_mission = None
        self.selected_creature = None

        for mission in ['Scout', 'Forage', 'Attack']:
            entry = ListEntry.simple({'name': mission})
            entry.button.bind(on_press=partial(self.mission_selected, entry))
            self.left_panel.layout.add_widget(entry)

        self.creature_spinner.bind(text=self.select_creature)
        self.start_button.bind(on_press=self.start_mission)

    def mission_selected(self, entry, button):
        print(f"selected mission {entry.data['name']}")
        self.mission_label.text = entry.data['name']
        self.selected_mission = entry

        creatures = ['a', 'b', 'c']
        self.creature_spinner.values = creatures
        self.creature_spinner.text = ''
        self.creature_spinner.text = creatures[0]

    def select_creature(self, spinner, value):
        if not value:
            return
        print(f'selected creature {value}')
        self.selected_creature = value

    def start_mission(self, button):
        print(
            f'{self.selected_creature} started mission '
            f'{self.selected_mission.data["name"]}'
        )

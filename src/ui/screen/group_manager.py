# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.screen import UiState
from ui.widget.widgets import ListEntry
from ui.widget.dialog import Dialog

from kivy.properties import ObjectProperty
from functools import partial


class GroupManager(UiState):
    left_panel = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # TODO: Switch to a a proper model when implementing
        self.entries = ['Group A', 'Group B']
        self.build_entries()

    def build_entries(self):
        self.left_panel.layout.clear_widgets()
        list_entry = ListEntry.simple({'name': 'New Group'})
        list_entry.button.bind(on_press=self.new_group)
        self.left_panel.layout.add_widget(list_entry)
        for entry in self.entries:
            list_entry = ListEntry.deletable({'name': entry})
            list_entry.button.bind(
                on_press=partial(self.load_group, list_entry.data)
            )
            list_entry.delete_button.bind(
                on_press=partial(self.delete_group, list_entry.data)
            )
            self.left_panel.layout.add_widget(list_entry)

    def new_group(self, button):
        dialog = Dialog.get_text('Enter new group name')
        dialog.bind(on_dismiss=self.create_new_group)

    def create_new_group(self, dialog):
        if not dialog.valid:
            return
        self.entries.append(dialog.text)
        self.build_entries()

    def load_group(self, data, button):
        self.group_name = data['name']

    def delete_group(self, data, button):
        self.entries.remove(data['name'])
        self.build_entries()

# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.screen import UiState
from ui.widget.widgets import ListEntry
from ui.widget.dialog import Dialog

from kivy.properties import ObjectProperty

from collections import OrderedDict
from functools import partial

from types import SimpleNamespace


class GroupManagerModel:
    def __init__(self):
        self.groups = OrderedDict()
        self.all_templates = {}

        self.name = ''
        self.selected = {'selected': None, 'contents': []}
        self.available = {'selected': None, 'contents': []}


class GroupManager(UiState):
    left_panel = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._model = GroupManagerModel()

        # ################################################################### #
        #                            Ui bindings                              #
        # ################################################################### #
        self.add_button.bind(
            on_press=partial(
                self.move_template,
                source=self._model.available,
                destination=self._model.selected
            )
        )
        self.remove_button.bind(
            on_press=partial(
                self.move_template,
                source=self._model.selected,
                destination=self._model.available
            )
        )
        self.group_text_input.bind(focus=self.update_group_name)
        self.available_list.bind(on_item_pressed=self.select_template)
        self.selected_list.bind(on_item_pressed=self.select_template)
        self.save_button.bind(on_press=self.save_group)
        self.clear_button.bind(on_press=lambda button: self.load_group())

    def __enter__(self):
        self.update_templates()
        self.populate_group_list()
        self.load_group()
        return self

    def update_templates(self):
        # TODO Get template list from game and populate model dict with it
        # instead of using dummy data
        self._model.all_templates = {
            'First': SimpleNamespace(cost=10),
            'Second': SimpleNamespace(cost=20),
            'Third': SimpleNamespace(cost=30)
        }

    def update_group_name(self, text_input, focus):
        self._model.name = self.group_text_input.text

    def populate_group_list(self):
        self.group_list.clear()

        entry = ListEntry.simple('New Group')
        entry.bind(on_press=self.new_group)
        self.group_list.append(entry)

        for name in self._model.groups.keys():
            entry = ListEntry.deletable(name)
            entry.bind(on_press=lambda entry: self.load_group(entry.name))
            entry.bind(on_delete=lambda entry: self.delete_group(entry.name))
            self.group_list.append(entry)

    def new_group(self, button):
        dialog = Dialog.get_text('Enter new group name')
        dialog.bind(on_dismiss=self.create_new_group)

    def create_new_group(self, dialog):
        if not dialog.valid:
            return

        self._model.groups[dialog.text] = []
        self.populate_group_list()
        self.load_group(dialog.text)

    def load_group(self, name=''):
        self._model.name = name
        self._model.selected['selected'] = None
        # Shallow copy of the list of templates
        self._model.selected['contents'] = list(
            self._model.groups.get(name, [])
        )

        self._model.available['selected'] = None
        self._model.available['contents'] = [
            name
            for name in self._model.all_templates.keys()
            if name not in self._model.selected['contents']
        ]
        self.update_ui()

    def delete_group(self, name):
        del self._model.groups[name]
        self.populate_group_list()

    def update_ui(self):
        # Update the group name text input in the ui
        self.group_name = self._model.name

        lists = zip(
            [self._model.selected, self._model.available],
            [self.selected_list, self.available_list]
        )
        # Rebuild ui lists from model contents
        for data, ui_list in lists:
            ui_list.clear()
            for template in data['contents']:
                entry = ListEntry.togglable(template)
                if data['selected'] == template:
                    entry.state = 'down'
                ui_list.append(entry)

    def select_template(self, entry_list, selected_entry):
        name = selected_entry.name if selected_entry.state == 'down' else None

        if entry_list == self.selected_list:
            self._model.selected['selected'] = name
        else:
            self._model.available['selected'] = name

        self.update_ui()

    def move_template(self, button, source, destination):
        if source['selected'] is None:
            return

        source['contents'].remove(source['selected'])
        destination['contents'].append(source['selected'])
        source['selected'] = None
        self.update_ui()
        self.update_cost()

    def update_cost(self):
        self.biomass = str(sum(
            self._model.all_templates[name].cost
            for name in self._model.selected['contents']
        ))

    def save_group(self, button):
        # Uncomment and further implement to have a renaming/update system
        # if self._model.name:
        #     del self._model.groups[self._model.name]

        # TODO Warn the user when name already exists
        self._model.name = self.group_text_input.text
        # Shallow copy the list of mutations
        self._model.groups[self._model.name] = list(
            self._model.selected['contents']
        )
        self.populate_group_list()

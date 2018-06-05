# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.screen import UiState
from ui.widget.widgets import ListEntry
from ui.widget.dialog import Dialog

from functools import partial

from ObjectManager import ObjectManager


class TemplateEditor(UiState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_button.bind(
            on_press=partial(
                self.move_mutation,
                source=self.available_list,
                destination=self.selected_list
            )
        )
        self.remove_button.bind(
            on_press=partial(
                self.move_mutation,
                source=self.selected_list,
                destination=self.available_list
            )
        )

        # TODO: Switch to a a proper model when implementing
        self.entries = ['First', 'Second']
        self.build_entries()

        self.available_list.bind(on_item_pressed=self.select_mutation)
        self.selected_list.bind(on_item_pressed=self.select_mutation)

        # TODO do a proper refresh when needed (on open or periodically)
        # instead of putting it in __init__
        self.update_available()

    def build_entries(self):
        self.template_list.clear()
        list_entry = ListEntry.entry(
            ListEntry.entry_type.SIMPLE, {'name': 'New Template'}
        )
        list_entry.button.bind(on_press=self.new_template)
        self.template_list.append(list_entry)
        for entry in self.entries:
            list_entry = ListEntry.entry(
                ListEntry.entry_type.DELETABLE, {'name': entry}
            )
            list_entry.button.bind(
                on_press=partial(self.load_template, list_entry.data)
            )
            list_entry.delete_button.bind(
                on_press=partial(self.delete_template, list_entry.data)
            )
            self.template_list.append(list_entry)

    def new_template(self, button):
        dialog = Dialog.get_text('Enter new template name')
        dialog.bind(on_dismiss=self.create_new_template)

    def create_new_template(self, dialog):
        if not dialog.valid:
            return
        self.entries.append(dialog.text)
        self.build_entries()

    def load_template(self, data, button):
        self.template_name = data['name']

    def delete_template(self, data, button):
        self.entries.remove(data['name'])
        self.build_entries()

    def update_available(self):
        mutations = ObjectManager.game.available_mutations()
        self.available_list.clear()
        for mutation in mutations:
            entry = ListEntry.entry(
                ListEntry.entry_type.TOGGLABLE, {'name': mutation.name}
            )
            self.available_list.append(entry)

    def select_mutation(self, entry_list, selected_entry):
        state = 'normal'
        if selected_entry.state == 'normal':
            state = 'down'

        for entry in entry_list:
            entry.state = 'normal'

        selected_entry.state = state

    def move_mutation(self, button, source, destination):
        if source.selected_entry is None:
            return
        destination.append(
            ListEntry.entry(
                ListEntry.entry_type.TOGGLABLE, source.selected_entry.data
            )
        )
        source.remove(source.selected_entry)
        source.selected_entry = None

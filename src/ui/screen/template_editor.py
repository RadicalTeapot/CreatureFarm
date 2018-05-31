# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.screen import UiState
from ui.widget.widgets import ListEntry
from ui.widget.dialog import Dialog

from kivy.properties import ObjectProperty

from functools import partial


class TemplateEditor(UiState):
    left_panel = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # TODO: Switch to a a proper model when implementing
        self.entries = ['First', 'Second']
        self.build_entries()

    def build_entries(self):
        self.left_panel.layout.clear_widgets()
        list_entry = ListEntry.simple({'name': 'New Template'})
        list_entry.button.bind(on_press=self.new_template)
        self.left_panel.layout.add_widget(list_entry)
        for entry in self.entries:
            list_entry = ListEntry.deletable({'name': entry})
            list_entry.button.bind(
                on_press=partial(self.load_template, list_entry.data)
            )
            list_entry.delete_button.bind(
                on_press=partial(self.delete_template, list_entry.data)
            )
            self.left_panel.layout.add_widget(list_entry)

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

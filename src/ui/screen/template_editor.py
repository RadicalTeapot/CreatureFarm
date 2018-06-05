# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.screen import UiState
from ui.widget.widgets import ListEntry
from ui.widget.dialog import Dialog

from functools import partial
from collections import OrderedDict

from ObjectManager import ObjectManager


class TemplateEditorModel:
    def __init__(self):
        self.templates = OrderedDict()
        self.all_mutations = {}
        self.name = ''
        self.available = []
        self.selected = []


class TemplateEditor(UiState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._model = TemplateEditorModel()
        # TODO do a proper refresh when needed (on open or periodically)
        # instead of putting it in __init__
        self._model.all_mutations = dict(
            [
                (mutation.name, mutation)
                for mutation in ObjectManager.game.available_mutations()
            ]
        )

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
        self.available_list.bind(on_item_pressed=self.select_mutation)
        self.selected_list.bind(on_item_pressed=self.select_mutation)
        self.save_button.bind(on_press=self.save_template)
        self.clear_button.bind(on_press=lambda button: self.load_template())

        self.populate_template_list()
        self.load_template()

    def populate_template_list(self):
        self.template_list.clear()

        list_entry = ListEntry.simple('New Template')
        list_entry.bind(on_press=self.new_template)
        self.template_list.append(list_entry)

        for name, mutations in self._model.templates.items():
            list_entry = ListEntry.deletable(name)
            list_entry.bind(
                on_press=lambda entry: self.load_template(entry.name)
            )
            list_entry.bind(
                on_delete=lambda entry: self.delete_template(entry.name)
            )
            self.template_list.append(list_entry)

    def new_template(self, button):
        dialog = Dialog.get_text('Enter new template name')
        dialog.bind(on_dismiss=self.create_new_template)

    def create_new_template(self, dialog):
        if not dialog.valid:
            return

        self._model.templates[dialog.text] = []
        self.populate_template_list()
        self.load_template(dialog.text)

    def load_template(self, name=''):
        self._model.name = name
        # Shallow copy the list of mutations
        self._model.selected = list(self._model.templates.get(name, []))
        self._model.available = [
            name
            for name in self._model.all_mutations
            if name not in self._model.selected
        ]
        self.update_mutation_lists()

    def delete_template(self, name):
        del self._model.templates[name]
        self.populate_template_list()

    def update_mutation_lists(self):
        self.template_name = self._model.name

        self.available_list.clear()
        for mutation in self._model.available:
            self.available_list.append(ListEntry.togglable(mutation))

        self.selected_list.clear()
        for mutation in self._model.selected:
            self.selected_list.append(ListEntry.togglable(mutation))

    def select_mutation(self, entry_list, selected_entry):
        state = selected_entry.state

        for entry in entry_list:
            entry.state = 'normal'

        selected_entry.state = state

    def move_mutation(self, button, source, destination):
        if source.selected_entry is None:
            return
        destination.append(
            ListEntry.togglable(source.selected_entry.name)
        )
        source.remove(source.selected_entry)
        source.selected_entry = None

        self.update_mutation_cost()

    def update_mutation_cost(self):
        # TODO: Do fancier computation in Game instead
        self.biomass = str(sum(
            [
                self._model.all_mutations[entry.name].biomass_cost
                for entry in self.selected_list
            ]
        ))

    def save_template(self, button):
        # Uncomment and further implement to have a renaming/update system
        # if self._model.name:
        #     del self._model.templates[self._model.name]

        # TODO: Warn the user when name already exists
        self._model.name = self.template_text_input.text
        self._model.templates[self._model.name] = [
            mutation.name
            for mutation in self.selected_list
        ]
        self.populate_template_list()

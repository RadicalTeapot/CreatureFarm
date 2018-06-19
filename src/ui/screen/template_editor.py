# -*- coding: utf-8 -*-
"""DOCSTRING."""

from ui.screen import UiState
from ui.widget.widgets import ListEntry
from ui.widget.dialog import Dialog

from functools import partial

from ObjectManager import ObjectManager
from DataStructures import Template


class TemplateEditorModel:
    def __init__(self):
        self.name = ''
        # The selected field stores the currently selected entry
        self.available = {'selected': None, 'contents': []}
        self.selected = {'selected': None, 'contents': []}


class TemplateEditor(UiState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._model = TemplateEditorModel()

        # ################################################################### #
        #                            Ui bindings                              #
        # ################################################################### #
        self.add_button.bind(
            on_press=partial(
                self.move_mutation,
                source=self._model.available,
                destination=self._model.selected
            )
        )
        self.remove_button.bind(
            on_press=partial(
                self.move_mutation,
                source=self._model.selected,
                destination=self._model.available
            )
        )
        self.template_text_input.bind(focus=self.update_template_name)
        self.available_list.bind(on_item_pressed=self.select_mutation)
        self.selected_list.bind(on_item_pressed=self.select_mutation)
        self.save_button.bind(on_press=self.save_template)
        self.clear_button.bind(on_press=lambda button: self.load_template())

    def __enter__(self):
        self.populate_template_list()
        self.load_template()
        return self

    def update_template_name(self, text_input, focus):
        self._model.name = self.template_text_input.text

    def populate_template_list(self):
        self.template_list.clear()

        entry = ListEntry.simple('New Template')
        entry.bind(on_press=self.new_template)
        self.template_list.append(entry)

        for name in ObjectManager.game.creature_templates:
            entry = ListEntry.deletable(name)
            entry.bind(on_press=lambda entry: self.load_template(entry.name))
            entry.bind(on_delete=lambda entry: self.delete_template(entry.name))
            self.template_list.append(entry)

    def new_template(self, button):
        dialog = Dialog.get_text('Enter new template name')
        dialog.bind(on_dismiss=self.create_new_template)

    def create_new_template(self, dialog):
        if not dialog.valid:
            return

        ObjectManager.game.creature_templates[dialog.text] = Template()
        self.populate_template_list()
        self.load_template(dialog.text)

    def load_template(self, name=''):
        self._model.name = name

        self._model.selected['selected'] = None
        # Shallow copy the list of mutations
        templates = ObjectManager.game.creature_templates
        self._model.selected['contents'] = list(
            templates.get(name, Template()).mutations
        )

        self._model.available['selected'] = None
        self._model.available['contents'] = [
            mutation.name
            for mutation in ObjectManager.game.get_mutations()
            if mutation.name not in self._model.selected['contents']
        ]

        self.update_cost()
        self.update_ui()

    def delete_template(self, name):
        del ObjectManager.game.creature_templates[name]
        self.populate_template_list()

    def update_ui(self):
        # Update the template name text input in the ui
        self.template_name = self._model.name

        lists = zip(
            [self._model.selected, self._model.available],
            [self.selected_list, self.available_list]
        )
        # Rebuild ui lists from model contents
        for data, ui_list in lists:
            ui_list.clear()
            for mutation in data['contents']:
                entry = ListEntry.togglable(mutation)
                if data['selected'] == mutation:
                    entry.state = 'down'
                ui_list.append(entry)

    def select_mutation(self, entry_list, selected_entry):
        name = selected_entry.name if selected_entry.state == 'down' else None

        if entry_list == self.selected_list:
            self._model.selected['selected'] = name
        else:
            self._model.available['selected'] = name

        self.update_ui()

    def move_mutation(self, button, source, destination):
        if source['selected'] is None:
            return

        source['contents'].remove(source['selected'])
        destination['contents'].append(source['selected'])
        source['selected'] = None
        self.update_ui()
        self.update_cost()

    def get_biomass_cost(self, mutation_names):
        mutations = {
            mutation.name: mutation
            for mutation in ObjectManager.game.get_mutations()
        }
        return sum([
            mutations[name].biomass_cost
            for name in mutation_names
        ])

    def update_cost(self):
        # TODO: Do fancier computation (have threshold where the cost of
        # everything is multiplied)
        self.biomass = str(
            self.get_biomass_cost(self._model.selected['contents'])
        )

    def save_template(self, button):
        # Uncomment and further implement to have a renaming/update system
        # if self._model.name:
        #     del ObjectManager.game.creature_templates[self._model.name]

        # TODO Warn the user when name already exists
        self._model.name = self.template_text_input.text

        templates = ObjectManager.game.creature_templates
        templates[self._model.name] = Template(
            # Shallow copy the list of mutations
            mutations=list(self._model.selected['contents']),
            cost=self.get_biomass_cost(self._model.selected['contents'])
        )

        self.populate_template_list()

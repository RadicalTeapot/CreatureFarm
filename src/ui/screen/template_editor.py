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
        self.size = 1.
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
        self.size_slider.bind(value=self.update_template_size)

    def __enter__(self):
        self.populate_template_list()
        self.load_template()
        return self

    def update_template_name(self, text_input, focus):
        self._model.name = self.template_text_input.text

    def update_template_size(self, slider, value):
        self._model.size = value
        self.update_cost()

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
        template = ObjectManager.game.creature_templates.get(name, Template())
        self._model.size = template.size

        self._model.selected['selected'] = None
        # Shallow copy the list of mutations
        self._model.selected['contents'] = list(template.mutations)

        self._model.available['selected'] = None
        self._model.available['contents'] = [
            mutation_id
            for mutation_id in sorted(ObjectManager.game.mutations.keys())
            if mutation_id not in self._model.selected['contents']
        ]

        self.update_cost()
        self.update_ui()

    def delete_template(self, name):
        del ObjectManager.game.creature_templates[name]
        self.populate_template_list()

    def update_ui(self):
        # Update the template name text input in the ui
        self.template_name = self._model.name
        # Update the template size text input in the ui
        self.template_size = self._model.size

        # Sort list based on mutation names
        self._model.selected['contents'] = sorted(
            self._model.selected['contents'],
            key=lambda id_: ObjectManager.game.mutations[id_].name
        )

        # Reorder list base on validity and mutation name
        valid, invalid = [], []
        for mutation_id in self._model.available['contents']:
            (
                valid
                if ObjectManager.game.mutations[mutation_id].is_valid(
                    self._model.selected['contents']
                )
                else invalid
            ).append(mutation_id)
        self._model.available['contents'] = sorted(
            valid, key=lambda id_: ObjectManager.game.mutations[id_].name
        )
        self._model.available['contents'].extend(sorted(
            invalid, key=lambda id_: ObjectManager.game.mutations[id_].name
        ))

        lists = (
            (self._model.selected, self.selected_list),
            (self._model.available, self.available_list),
        )

        # Rebuild ui lists from model contents
        for data, ui_list in lists:
            ui_list.clear()
            for mutation_id in data['contents']:
                mutation = ObjectManager.game.mutations[mutation_id]
                entry = ListEntry.togglable(mutation.name, data=mutation_id)
                entry.set_tool_tip(
                    mutation.get_description(self._model.selected['contents'])
                )
                if data['selected'] == mutation_id:
                    entry.state = 'down'
                if (
                    data == self._model.available and
                    not mutation.is_valid(self._model.selected['contents'])
                ):
                    entry.state = 'normal'
                    entry.deactivate()
                ui_list.append(entry)

    def select_mutation(self, entry_list, selected_entry):
        id_ = selected_entry.data if selected_entry.state == 'down' else None

        if entry_list == self.selected_list:
            self._model.selected['selected'] = id_
        else:
            self._model.available['selected'] = id_

        self.update_ui()

    def move_mutation(self, button, source, destination):
        if source['selected'] is None:
            return

        source['contents'].remove(source['selected'])
        destination['contents'].append(source['selected'])
        source['selected'] = None
        self.update_ui()
        self.update_cost()

    def update_cost(self):
        self.biomass = ObjectManager.game.get_biomass_cost(
            self._model.selected['contents'],
            self._model.size
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
            size=self._model.size,
            cost=ObjectManager.game.get_biomass_cost(
                self._model.selected['contents'],
                self._model.size
            )
        )

        self.populate_template_list()

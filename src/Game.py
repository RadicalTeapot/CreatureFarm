# -*- coding: utf-8 -*-
"""DOCSTRING."""

from activity.Adventure import AdventureTemplate
from Enemy import EnemyTemplate
from Mutation import MutationTemplate

from ObjectManager import ObjectManager
from Settings import Settings
from DataStructures import GameModel
from DataStructures import Knowledge

import json
import os

from kivy.core.window import Window


class Game(object):
    def __init__(self):
        self._model = GameModel()

        self._parse_adventures()
        self._parse_enemies()
        self._parse_mutations()
        self._parse_knowledge()

        self.keyboard = Window.request_keyboard(
            None,
            None,
            'text'
        )
        self.keyboard.bind(on_key_down=self.key_press)

    def key_press(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'escape':
            ObjectManager.ui.open_escape_menu()

        return True

    def _parse_adventures(self):
        with open("data/json/adventures.json", 'r') as json_data:
            items = json.loads(json_data.read()).items()

        for id_, data in items:
            self._model.adventure_templates[id_] = (
                AdventureTemplate.from_data(id_, data)
            )

    def _parse_enemies(self):
        with open("data/json/enemies.json", 'r') as json_data:
            items = json.loads(json_data.read()).items()

        for id_, data in items:
            self._model.enemy_templates[id_] = (
                EnemyTemplate.from_data(id_, data)
            )

    def _parse_mutations(self):
        with open("data/json/mutations.json", 'r') as json_data:
            items = json.loads(json_data.read()).items()

        for id_, data in items:
            self._model.mutation_templates[id_] = (
                MutationTemplate.from_data(id_, data)
            )

    def _parse_knowledge(self):
        with open("data/json/knowledge.json", 'r') as json_data:
            items = json.loads(json_data.read()).items()

        for id_, data in items:
            self._model.knowledge[id_] = Knowledge(data, 0.)

    def update(self):
        for creature in self.creatures:
            creature.update()
        self.date += 1
        ObjectManager.ui.refresh()

    def has_knowledge(self, knowledge_id):
        if knowledge_id not in self.knowledge:
            raise KeyError('Knowledge {} not found'.format(knowledge_id))
        return (
            self.knowledge[knowledge_id].current_level >=
            self.knowledge[knowledge_id].base_cost
        )

    def get_mutations(self):
        # TODO Check for knowledge and return only available mutation
        return self._model.mutation_templates.values()

    def get_adventures(self):
        # TODO Return only available adventures
        return self._model.adventure_templates.values()

    @property
    def running_adventures(self):
        return self._model.running_adventures

    @property
    def creature_templates(self):
        return self._model.creature_templates

    @property
    def creature_groups(self):
        return self._model.creature_groups

    @property
    def biomass(self):
        return self._model.biomass

    @biomass.setter
    def biomass(self, value):
        self._model.biomass = value
        ObjectManager.ui.update_biomass()

    def add_running_adventure(self, name, new_adventure):
        # Adventure instances are indexed by their name
        running = self._model.running_adventures.get(name, [])
        running.append(new_adventure)
        self._model.running_adventures[name] = running

        ObjectManager.ui.update_adventure_count()

    def load(self, path=None):
        if path is None:
            path = os.path.normpath(os.path.join(
                os.path.abspath(Settings.SAVE_FOLDER),
                'save'
            ))
        with open(path, 'r') as save_file:
            self._model.deserialize(json.loads(save_file.read()))
        ObjectManager.ui.reload()

    def save(self):
        data = self._model.serialize()
        path = os.path.normpath(os.path.join(
            os.path.abspath(Settings.SAVE_FOLDER),
            'save'
        ))
        with open(path, 'w') as save_file:
            save_file.write(json.dumps(data))

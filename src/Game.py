# -*- coding: utf-8 -*-
"""DOCSTRING."""

from Adventure import AdventureTemplate
from Enemy import EnemyTemplate
from Mutation import MutationTemplate

from Creature import Creature

from ObjectManager import ObjectManager
from Settings import Settings
from Adventure import Adventure
from DataStructures import GameModel
from DataStructures import Knowledge

import json
import os
import random

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
            items = json.loads(json_data.read())

        for data in items:
            adventure = AdventureTemplate.from_data(data)
            if adventure in self._model.adventure_templates:
                raise RuntimeError(
                    'Duplicate adventure {} not allowed'.format(
                        adventure.name
                    )
                )
            self._model.adventure_templates[adventure.name] = adventure

    def _parse_enemies(self):
        with open("data/json/enemies.json", 'r') as json_data:
            items = json.loads(json_data.read()).items()

        for id_, data in items:
            self._model.enemy_templates[id_] = (
                EnemyTemplate.from_data(id_, data)
            )

    def _parse_mutations(self):
        with open("data/json/mutations.json", 'r') as json_data:
            items = json.loads(json_data.read())

        for data in items:
            mutation = MutationTemplate.from_data(data)
            if mutation in self._model.mutation_templates:
                raise RuntimeError(
                    'Duplicate mutation {} not allowed'.format(
                        mutation.name
                    )
                )
            self._model.mutation_templates[mutation.name] = mutation

    def _parse_knowledge(self):
        with open("data/json/knowledge.json", 'r') as json_data:
            items = json.loads(json_data.read()).items()

        for id_, data in items:
            self._model.knowledge[id_] = Knowledge(data, 0.)

    def has_knowledge(self, knowledge_id):
        if knowledge_id not in self.knowledge:
            raise KeyError('Knowledge {} not found'.format(knowledge_id))
        return (
            self.knowledge[knowledge_id].current_level >=
            self.knowledge[knowledge_id].base_cost
        )

    def get_mutations(self):
        # TODO Check for knowledge and return only available mutation
        return self._model.mutation_templates

    def get_adventures(self):
        # TODO Return only available adventures
        return self._model.adventure_templates

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

    @property
    def enemies(self):
        return self._model.enemy_templates

    @biomass.setter
    def biomass(self, value):
        self._model.biomass = value
        ObjectManager.ui.update_biomass()

    def get_biomass_cost(self, mutation_names):
        return sum(
            self._model.mutation_templates[mutation].biomass_cost
            for mutation in mutation_names
        )

    def add_running_adventure(self, adventure_name, template_names, group_name):
        cost = sum([
            self.creature_templates[template_name].cost
            for template_name in template_names
        ])
        self.biomass -= cost

        # Adventure instances are indexed by their name
        running = self._model.running_adventures.get(adventure_name, [])
        new_adventure = Adventure(
            creatures=[
                Creature(
                    template_name,
                    self.creature_templates[template_name].mutations
                )
                for template_name in template_names
            ],
            creature_name=group_name,
            template_name=adventure_name
        )
        running.append(new_adventure)
        new_adventure.start()
        self._model.running_adventures[adventure_name] = running

        ObjectManager.ui.update_adventure_count()

    def end_adventure(self, adventure):
        # Each dead creature held biomass and its cost are returned
        # to the adventure pool
        returned_biomass = sum(
            creature.stat['held_biomass'] + creature.cost
            for creature in adventure.creatures
            if creature.is_dead()
        )
        self._model.adventure_templates[adventure.template_name].biomass_pool += \
            returned_biomass

        # Each alive creature held biomass and its cost are returned
        # to the game pool
        extracted_biomass = sum(
            creature.stat['held_biomass'] + creature.cost
            for creature in adventure.creatures
            if not creature.is_dead()
        )
        self.biomass += extracted_biomass

        self._model.running_adventures[adventure.template_name].remove(
            adventure
        )

        # TODO Knowledge

    def update(self):
        for adventures in self._model.running_adventures.values():
            for adventure in adventures:
                adventure.update()
        # TODO Refill each adventure template biomass (using regen speed)

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

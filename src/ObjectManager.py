# -*- coding: utf-8 -*-
"""DOCSTRING."""


class ObjectManagerType(type):
    def __getattr__(cls, key):
        if ObjectManager._instance is None:
            raise RuntimeError('Object manager not instanced !')
        if key not in ObjectManager._instance.objects:
            raise AttributeError('Cannot find {} object'.format(key))
        return ObjectManager._instance.objects[key]


class ObjectManager(object, metaclass=ObjectManagerType):
    _instance = None

    def __init__(self):
        if ObjectManager._instance is not None:
            raise RuntimeError('Object manager already initialized !')
        self.objects = {}
        ObjectManager._instance = self

    def add_object(self, object_name, object_instance):
        if ObjectManager._instance is None:
            raise RuntimeError('Object manager not instanced !')
        ObjectManager._instance.objects[object_name] = object_instance

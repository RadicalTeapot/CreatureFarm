# -*- coding: utf-8 -*-
"""DOCSTRING."""

from kivy.factory import Factory


class ListEntry:
    @staticmethod
    def simple(data):
        instance = Factory.SimpleListEntry()
        instance.data = data
        return instance

    @staticmethod
    def deletable(data):
        instance = Factory.DeletableListEntry()
        instance.data = data
        return instance

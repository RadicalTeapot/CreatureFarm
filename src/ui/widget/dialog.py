# -*- coding: utf-8 -*-
"""DOCSTRING."""

from kivy.factory import Factory


class Dialog:
    @staticmethod
    def get_text(message):
        instance = Factory.TextDialog()
        instance.title = message

        instance.open()
        return instance

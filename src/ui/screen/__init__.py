# -*- coding: utf-8 -*-
"""DOCSTRING."""

from kivy.properties import BooleanProperty
from kivy.uix.widget import Widget


class UiState(Widget):
    hide_top_bar = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

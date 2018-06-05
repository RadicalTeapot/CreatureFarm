# -*- coding: utf-8 -*-
"""DOCSTRING."""

from kivy.factory import Factory

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

from enum import Enum
from functools import partial


class ListWidget(Widget):
    layout = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entries = []

    def __len__(self):
        return len(self._entries)

    def __getitem__(self, index):
        return self._entries[index]

    def __setitem__(self, index, value):
        del self[index]
        self.insert(index, value)

    def __delitem__(self, index):
        entry = self._entries.pop(index)
        self.layout.clear_widgets([entry])

    def __contains__(self, value):
        return value in self._entries

    def __iter__(self):
        return iter(self._entries)

    def append(self, value):
        self._entries.append(value)
        self.layout.add_widget(value)

    def insert(self, index, value):
        self._entries.insert(index, value)
        self.layout.add_widget(value, index)

    def clear(self):
        self._entries = []
        self.layout.clear_widgets()

    def remove(self, value):
        if value not in self:
            return
        index = 0
        for i, v in enumerate(self):
            if v == value:
                index = i
        del self[index]


class TogglableListWidget(ListWidget):
    # _togglable_entry = Factory.TogglableListEntry().__class__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_item_pressed')
        self.selected_entry = None

    def append(self, value):
        # if not isinstance(value, self._togglable_entry):
        #     raise TypeError('Wrong entry type')
        super().append(value)
        value.button.bind(on_press=partial(self.item_pressed, value))

    def item_pressed(self, entry, button):
        self.dispatch('on_item_pressed', entry)

    def on_item_pressed(self, instance):
        if instance.state == 'normal':
            self.selected_entry = None
        else:
            self.selected_entry = instance


class ListEntryType(Enum):
    SIMPLE = 0
    DELETABLE = 1
    TOGGLABLE = 2


class ListEntry:
    entry_type = ListEntryType

    @staticmethod
    def entry(entry_type, data):
        instance = None
        if entry_type == ListEntry.entry_type.SIMPLE:
            instance = Factory.SimpleListEntry()
        elif entry_type == ListEntry.entry_type.DELETABLE:
            instance = Factory.DeletableListEntry()
        elif entry_type == ListEntry.entry_type.TOGGLABLE:
            instance = Factory.TogglableListEntry()
        instance.data = data
        return instance

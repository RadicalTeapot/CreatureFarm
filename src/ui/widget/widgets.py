# -*- coding: utf-8 -*-
"""DOCSTRING."""

from kivy.factory import Factory
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class ListWidget(Widget):
    layout = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._entries = []
        self.selected_entry = None

        self.register_event_type('on_item_pressed')

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

        if isinstance(value, TogglableListEntry):
            value.bind(on_press=self.item_pressed)

    def insert(self, index, value):
        self._entries.insert(index, value)
        self.layout.add_widget(value, index)

    def clear(self):
        self._entries = []
        self.layout.clear_widgets()

    def take(self, value):
        self.selected_entry = None
        return self._entries.pop(self._entries.index(value))

    def item_pressed(self, entry):
        self.dispatch('on_item_pressed', entry)

    def on_item_pressed(self, instance):
        if isinstance(instance, TogglableListEntry):
            if instance.state == 'normal':
                self.selected_entry = None
            else:
                self.selected_entry = instance


class ListEntry(Widget):
    entry_type = {
        'SIMPLE': 0,
        'DELETABLE': 1,
        'TOGGLABLE': 2,
    }

    button = ObjectProperty()

    def __init__(self, data=None):
        super().__init__()

        self.data = data
        self.tool_tip = None

        Window.bind(mouse_pos=self.on_mouse_pos)
        self.clock_event = None

        self.register_event_type('on_press')
        self.register_event_type('on_tool_tip')
        self.button.bind(on_press=self.button_pressed)

    def set_tool_tip(self, message):
        if self.tool_tip is None:
            self.tool_tip = Factory.ToolTip()
        self.tool_tip.text = message

    def _open_tool_tip(self, *args):
        self.dispatch('on_tool_tip')
        Window.add_widget(self.tool_tip)

    def on_tool_tip(self):
        pass

    def _close_tool_tip(self):
        Window.remove_widget(self.tool_tip)

    def remove_tool_tip(self):
        self.tool_tip = None

    def on_mouse_pos(self, *args):
        if self.tool_tip is None:
            return

        pos = args[1]
        self.tool_tip.pos = pos

        inside = self.collide_point(*self.to_widget(*pos))
        if inside and self.clock_event is None:
                self.clock_event = Clock.schedule_once(self._open_tool_tip, 1)
        elif not inside and self.clock_event is not None:
            Clock.unschedule(self.clock_event)
            self._close_tool_tip()
            self.clock_event = None

    def button_pressed(self, button):
        self.dispatch('on_press')

    def on_press(self):
        pass

    @classmethod
    def entry(cls, entry_type, name, data):
        instance = None
        if entry_type == cls.entry_type['SIMPLE']:
            instance = SimpleListEntry(data)
        elif entry_type == cls.entry_type['DELETABLE']:
            instance = DeletableListEntry(data)
        elif entry_type == cls.entry_type['TOGGLABLE']:
            instance = TogglableListEntry(data)
        instance.name = name
        return instance

    @classmethod
    def simple(cls, name, data=None):
        return cls.entry(cls.entry_type['SIMPLE'], name, data)

    @classmethod
    def deletable(cls, name, data=None):
        return cls.entry(cls.entry_type['DELETABLE'], name, data)

    @classmethod
    def togglable(cls, name, data=None):
        return cls.entry(cls.entry_type['TOGGLABLE'], name, data)


class SimpleListEntry(ListEntry):
    pass


class DeletableListEntry(ListEntry):
    delete_button = ObjectProperty()

    def __init__(self, data=None):
        super().__init__(data)
        self.register_event_type('on_delete')
        self.delete_button.bind(on_press=self.delete_button_pressed)

    def delete_button_pressed(self, button):
        self.dispatch('on_delete')

    def on_delete(self):
        pass


class TogglableListEntry(ListEntry):
    _states = ['normal', 'down']

    def __init__(self, data=None):
        super().__init__(data)

    @property
    def state(self):
        return self.button.state

    @state.setter
    def state(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected str, got {} instead'.format(
                type(value).__name__
            ))
        if value not in TogglableListEntry._states:
            raise ValueError(
                f'Wrong state, only {TogglableListEntry._states!r} '
                f'are valid.'
            )
        self.button.state = value

    def _set_active(self, state):
        self.button.disabled = state

    def activate(self):
        self._set_active(False)

    def deactivate(self):
        self._set_active(True)

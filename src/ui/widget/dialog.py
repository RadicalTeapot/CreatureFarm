# -*- coding: utf-8 -*-
"""DOCSTRING."""

from kivy.factory import Factory
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty

from ObjectManager import ObjectManager


class Dialog:
    @staticmethod
    def get_text(message):
        instance = Factory.TextDialog()
        instance.title = message

        instance.open()
        return instance


class EscapeMenu(ModalView):
    save_button = ObjectProperty()
    load_button = ObjectProperty()
    exit_to_menu = ObjectProperty()
    exit_to_desktop = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pressed_button = None

        self.save_button.bind(on_press=self.button_pressed)
        self.load_button.bind(on_press=self.button_pressed)
        self.exit_to_menu.bind(on_press=self.button_pressed)
        self.exit_to_desktop.bind(on_press=self.button_pressed)

    def open(self, *args):
        super().open(*args)
        ObjectManager.game.keyboard.bind(on_key_down=self.key_pressed)
        self.pressed_button = None

    def button_pressed(self, button):
        self.pressed_button = button
        self.dismiss()

    def key_pressed(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'escape':
            self.dismiss()

        return True

    def dismiss(self, *args, **kwargs):
        ObjectManager.game.keyboard.unbind(on_key_down=self.key_pressed)
        super().dismiss(*args, **kwargs)

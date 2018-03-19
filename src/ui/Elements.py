# -*- coding: utf-8 -*-
"""DOCSTRING."""

import pyglet
import ui


class Button(object):
    margin = 5
    hover_color = (100, 150, 200)
    pressed_color = (50, 75, 100)
    regular_color = (0, 0, 0)

    def __init__(self, text, is_tristate=True):
        self.rect = ui.Rect(0, 0, 0, 0)
        # self.color = self.regular_color
        self.pressed = False
        self.hovered = False

        self.text = pyglet.text.Label(
            text,
            x=self.rect.x + self.margin,
            y=self.rect.y + self.margin,
            anchor_x='left', anchor_y='bottom'
        )
        self.handler = None
        self.is_tristate = is_tristate

        self.rect.update_position(
            self.rect.x, self.rect.y,
            self.text.content_width + 2 * self.margin,
            self.text.content_height + 2 * self.margin
        )

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value
        self.rect.update_position(
            self.rect.x, self.rect.y, self.rect.width, self.rect.height
        )
        self.text.x = self.rect.x + self.margin

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value
        self.rect.update_position(
            self.rect.x, self.rect.y, self.rect.width, self.rect.height
        )
        self.text.y = self.rect.y + self.margin

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.rect.update_position(
            self.rect.x, self.rect.y, self.rect.width, self.rect.height
        )

        self.text.x = self.rect.x + self.margin
        self.text.y = self.rect.y + self.margin

    def register_handler(self, function):
        self.handler = function

    def hover(self, x, y):
        self.hovered = self.rect.contains(x, y)

    def click(self, x, y):
        pressed = self.rect.contains(x, y)
        if pressed and self.handler is not None:
            self.handler()
        return pressed

    def draw(self):
        if self.hovered:
            self.rect.update_color(self.hover_color)
        elif self.is_tristate and self.pressed:
            self.rect.update_color(self.pressed_color)
        else:
            self.rect.update_color(self.regular_color)

        self.rect.draw()
        self.text.draw()


class AttributeLabel(object):
    def __init__(self, obj=None, attribute=None, pre='', post=''):
        self.rect = ui.Rect(0, 0, 0, 0)

        self.pre = pre
        self.post = post
        self.obj = obj
        self.attribute = attribute
        self.label = pyglet.text.Label(
            '{} - {}'.format(
                self.pre,
                self.post
            ),
            x=self.rect.x, y=self.rect.y,
            anchor_x='left', anchor_y='bottom'
        )

        self.rect.width = self.label.content_width
        self.rect.height = self.label.content_height

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.rect.update_position(
            self.rect.x, self.rect.y, self.rect.width, self.rect.height
        )

        self.label.x = self.rect.x
        self.label.y = self.rect.y

    def set_attribute(self, obj, attribute):
        self.obj = obj
        self.attribute = attribute

    def click(self, x, y):
        return self.rect.contains(x, y)

    def draw(self):
        if self.obj and self.attribute:
            self.label.text = '{} {} {}'.format(
                self.pre,
                getattr(self.obj, self.attribute),
                self.post
            )
        else:
            self.label.text = '{} - {}'.format(
                self.pre,
                self.post
            )
        self.label.draw()


class DescriptionLabel(object):
    def __init__(self, text, width):
        self.document = pyglet.text.decode_text(text)
        self.document.set_style(0, len(text), dict(color=(255, 255, 255, 255)))

        self.text = pyglet.text.layout.TextLayout(
            self.document, multiline=True, wrap_lines=True, width=width
        )

        self.rect = ui.Rect(
            0, 0, width, self.text.content_height
        )

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.rect.update_position(
            self.rect.x, self.rect.y, self.rect.width, self.rect.height
        )

        self.text.x = self.rect.x
        self.text.y = self.rect.y

    def draw(self):
        self.text.draw()

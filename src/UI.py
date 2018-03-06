# -*- coding: utf-8 -*-
"""DOCSTRING."""

import pyglet


class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def click(self, x, y):
        return (
            x >= self.x and y <= self.y and
            x <= self.x + self.width and
            y <= self.y + self.height
        )


class Button(object):
    def __init__(self, x, y, width, height, text, parent=None):
        self.parent = parent

        self.rect = Rect(x, y, width, height)

        if self.parent:
            self.rect.x += self.parent.x
            self.rect.y += self.parent.y

        self.text = pyglet.text.Label(
            text,
            x=self.rect.x + self.rect.width // 2,
            y=self.rect.y + self.rect.height // 2,
            anchor_x='center', anchor_y='center'
        )
        self.handler = None

    def register_handler(self, function):
        self.handler = function

    def click(self, x, y):
        if self.rect.click(x, y):
            if self.handler is not None:
                self.handler()
            return True

    def draw(self):
        pyglet.graphics.draw_indexed(
            4, pyglet.gl.GL_TRIANGLES,
            [0, 1, 2, 2, 1, 3],
            ('v2i', (
                self.x, self.y,
                self.x + self.width, self.y,
                self.x, self.y + self.height,
                self.x + self.width, self.y + self.height
            )),
            ('c3B', (
                128, 196, 255,
                128, 196, 255,
                128, 196, 255,
                128, 196, 255,
            ))
        )
        self.text.draw()


class AttributeLabel(object):
    def __init__(
        self, x, y, obj=None, attribute=None, pre='', post='', parent=None
    ):
        self.parent = parent

        self.rect = Rect(x, y, 0, 0)

        if self.parent:
            self.rect.x += self.parent.x
            self.rect.y += self.parent.y

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
            anchor_x='left', anchor_y='center'
        )

    def set_attribute(self, obj, attribute):
        self.obj = obj
        self.attribute = attribute

    def click(self, x, y):
        return self.rect.click(x, y)

    def draw(self):
        if self.obj and self.attribute:
            self.label.text = '{} {} {}'.format(
                self.pre,
                int(getattr(self.obj, self.attribute)),
                self.post
            )
        else:
            self.label.text = '{} - {}'.format(
                self.pre,
                self.post
            )
        self.label.draw()


class Panel(object):
    def __init__(self, x, y, width, height, is_main=False, parent=None):
        self.parent = parent

        self.rect = Rect(x, y, width, height)

        if self.parent:
            self.rect.x += self.parent.x
            self.rect.y += self.parent.y

        self.displayed = False
        self.is_main = is_main

        self.buttons = []
        self.labels = []

    def add_button(self, button):
        self.buttons.append(button)

    def add_label(self, label):
        self.labels.append(label)

    def show(self):
        self.displayed = True

    def hide(self):
        self.displayed = False

    def draw(self):
        if not self.displayed:
            return
        if self.is_main:
            pyglet.graphics.draw_indexed(
                4, pyglet.gl.GL_TRIANGLES,
                [0, 1, 2, 2, 1, 3],
                ('v2i', (
                    0, 0,
                    800, 0,
                    0, 600,
                    800, 600
                )),
                ('c4B', (
                    0, 0, 0, 75,
                    0, 0, 0, 75,
                    0, 0, 0, 75,
                    0, 0, 0, 75
                ))
            )

        for i in range(0, 3):
            margin = i * 5
            color = (1 - (i % 2)) * 255

            pyglet.graphics.draw_indexed(
                4, pyglet.gl.GL_TRIANGLES,
                [0, 1, 2, 2, 1, 3],
                ('v2i', (
                    self.rect.x + margin, self.rect.y + margin,
                    self.rect.x + self.rect.width - margin, self.rect.y + margin,
                    self.rect.x + margin, self.rect.y + self.rect.height - margin,
                    self.rect.x + self.rect.width - margin, self.rect.y + self.rect.height - margin
                )),
                ('c3B', (
                    color, color, color,
                    color, color, color,
                    color, color, color,
                    color, color, color
                ))
            )

        self.draw_contents()

    def draw_contents(self):
        for button in self.buttons:
            button.draw()
        for label in self.labels:
            label.draw()

    def click(self, x, y):
        if not self.displayed:
            return False

        if self.rect.click(x, y):
            for button in self.buttons:
                if button.click(x, y):
                    return True
            return True


class UI(object):
    def __init__(self):
        self.panels = []

    def add_panel(self, panel):
        self.panels.append(panel)

    def click(self, x, y):
        for panel in self.panels:
            if panel.click(x, y):
                break

    def draw(self):
        for panel in self.panels:
            panel.draw()

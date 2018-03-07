# -*- coding: utf-8 -*-
"""DOCSTRING."""

import pyglet


class Rect(object):
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self.width = width
        self.height = height

        self.offset_x = 0
        self.offset_y = 0

    @property
    def x(self):
        return self._x + self.offset_x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y + self.offset_y

    @y.setter
    def y(self, value):
        self._y = value

    def set_offset(self, x, y):
        self.offset_x = x
        self.offset_y = y

    def contains(self, x, y):
        return (
            x >= self.x and y >= self.y and
            x <= self.x + self.width and
            y <= self.y + self.height
        )


class Button(object):
    margin = 5
    hover_color = (100, 150, 200)
    regular_color = (0, 0, 0)

    def __init__(self, x, y, text):
        self._parent = None
        self.rect = Rect(x, y, 0, 0)

        self.text = pyglet.text.Label(
            text,
            x=self.rect.x + self.margin,
            y=self.rect.y + self.margin,
            anchor_x='left', anchor_y='bottom'
        )

        self.rect.width = self.text.content_width + 2 * self.margin
        self.rect.height = self.text.content_height + 2 * self.margin

        self.color = self.regular_color

        self.handler = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
        if parent is not None:
            self.rect.set_offset(parent.rect.x, parent.rect.y)
        else:
            self.rect.set_offset(0, 0)

    def register_handler(self, function):
        self.handler = function

    def hover(self, x, y):
        if self.rect.contains(x, y):
            self.color = self.hover_color
        else:
            self.color = self.regular_color

    def click(self, x, y):
        if self.rect.contains(x, y):
            if self.handler is not None:
                self.handler()
            return True

    def draw(self):
        pyglet.graphics.draw_indexed(
            4, pyglet.gl.GL_TRIANGLES,
            [0, 1, 2, 2, 1, 3],
            ('v2i', (
                self.rect.x, self.rect.y,
                self.rect.x + self.rect.width, self.rect.y,
                self.rect.x, self.rect.y + self.rect.height,
                self.rect.x + self.rect.width, self.rect.y + self.rect.height
            )),
            ('c3B', (
                *self.color,
                *self.color,
                *self.color,
                *self.color
            ))
        )
        self.text.draw()


class AttributeLabel(object):
    def __init__(self, x, y, obj=None, attribute=None, pre='', post=''):
        self._parent = None
        self.rect = Rect(x, y, 0, 0)

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

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
        if parent is not None:
            self.rect.set_offset(parent.rect.x, parent.rect.y)
        else:
            self.rect.set_offset(0, 0)

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
    def __init__(self, x, y, width, height, is_main=False):
        self.rect = Rect(x, y, width, height)

        self.displayed = False
        self.is_main = is_main

        self.buttons = []
        self.labels = []

    def add_button(self, button):
        button.parent = self
        self.buttons.append(button)

    def add_label(self, label):
        label.parent = self
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
            margin = i * 3
            color = (i % 2) * 128

            pyglet.graphics.draw_indexed(
                4, pyglet.gl.GL_TRIANGLES,
                [0, 1, 2, 2, 1, 3],
                ('v2i', (
                    self.rect.x + margin, self.rect.y + margin,
                    self.rect.x + self.rect.width - margin,
                    self.rect.y + margin,
                    self.rect.x + margin,
                    self.rect.y + self.rect.height - margin,
                    self.rect.x + self.rect.width - margin,
                    self.rect.y + self.rect.height - margin
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

    def mouse_motion(self, x, y):
        if not self.displayed:
            return

        for button in self.buttons:
            button.hover(x, y)

    def click(self, x, y):
        if not self.displayed:
            return False

        if self.rect.contains(x, y):
            for button in self.buttons:
                if button.click(x, y):
                    return True
            return True


class UI(object):
    def __init__(self):
        self.panels = []

    def add_panel(self, panel):
        self.panels.append(panel)

    def mouse_motion(self, x, y):
        for panel in self.panels:
            if panel.mouse_motion(x, y):
                break

    def click(self, x, y):
        for panel in self.panels:
            if panel.click(x, y):
                break

    def draw(self):
        for panel in self.panels:
            panel.draw()

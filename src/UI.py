# -*- coding: utf-8 -*-
"""DOCSTRING."""

import pyglet


class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, x, y):
        return (
            x >= self.x and y >= self.y and
            x <= self.x + self.width and
            y <= self.y + self.height
        )


class Layout(object):
    def __init__(self, parent, direction, spacing):
        self.rect = parent.rect
        self.direction = direction
        self.spacing = spacing
        self.content = []

    def clear(self):
        del self.content[:]

    def add_content(self, content):
        if isinstance(content, list):
            self.content.extend(content)
        else:
            self.content.append(content)
        self.reorganize()

    def reorganize(self):
        axis = 'width' if self.direction == 0 else 'height'
        other_axis = 'width' if self.direction == 1 else 'height'
        size = getattr(self.rect, axis)

        pos = self.spacing
        other_pos = self.spacing
        # Track the largest item of the column
        max_size = 0

        for content in self.content:
            content_size = getattr(content.rect, axis)
            # If content doesn't fit, go to next column
            if pos + content_size + self.spacing > size:
                pos = self.spacing
                other_pos += max_size + self.spacing
                max_size = 0
            else:
                max_size = max(max_size, getattr(content.rect, other_axis))

            content.set_pos(
                self.rect.x + (pos if self.direction == 0 else other_pos),
                # Flip y to simulate drawing content from top to bottom
                (
                    (self.rect.y + self.rect.height) -
                    (other_pos if self.direction == 0 else pos) -
                    content.rect.height
                )
            )
            pos += content_size + self.spacing


class Button(object):
    margin = 5
    hover_color = (100, 150, 200)
    regular_color = (0, 0, 0)

    def __init__(self, text):
        self.rect = Rect(0, 0, 0, 0)
        self.color = self.regular_color

        self.text = pyglet.text.Label(
            text,
            x=self.rect.x + self.margin,
            y=self.rect.y + self.margin,
            anchor_x='left', anchor_y='bottom'
        )
        self.handler = None

        self.rect.width = self.text.content_width + 2 * self.margin
        self.rect.height = self.text.content_height + 2 * self.margin

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

        self.text.x = self.rect.x + self.margin
        self.text.y = self.rect.y + self.margin

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
                *self.color, *self.color, *self.color, *self.color
            ))
        )
        self.text.draw()


class AttributeLabel(object):
    def __init__(self, obj=None, attribute=None, pre='', post=''):
        self.rect = Rect(0, 0, 0, 0)

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


class Panel(object):
    border_margin = 3

    def __init__(self, x, y, width, height, is_main=False, depth=-1):
        self.rect = Rect(x, y, width, height)

        self.displayed = False
        self.is_main = is_main
        self.layout = None
        self.depth = depth

        self.buttons = []
        self.labels = []

    def set_layout(self, direction=0, spacing=10):
        self.layout = Layout(self, direction, spacing)

        # Take panel border into account
        self.layout.rect.x += 2 * self.border_margin
        self.layout.rect.y += 2 * self.border_margin
        self.layout.rect.width -= 4 * self.border_margin
        self.layout.rect.height -= 4 * self.border_margin

    def add_button(self, button):
        if self.layout:
            self.layout.add_content(button)
        self.buttons.append(button)

    def add_buttons(self, buttons):
        if self.layout:
            self.layout.add_content(buttons)
        self.buttons.extend(buttons)

    def add_label(self, label):
        if self.layout:
            self.layout.add_content(label)
        self.labels.append(label)

    def clear(self):
        del self.buttons[:]
        del self.labels[:]
        if self.layout:
            self.layout.clear()

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
            margin = i * self.border_margin
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
            return False

        if not self.is_main and not self.rect.contains(x, y):
            return False

        for button in self.buttons:
            button.hover(x, y)

        return True

    def click(self, x, y):
        if not self.displayed:
            return False

        if self.rect.contains(x, y):
            for button in self.buttons:
                if button.click(x, y):
                    return True
            return True
        elif self.is_main:
            self.hide()
            return True
        return False


class UI(object):
    def __init__(self):
        self.panels = []

    def add_panel(self, panel):
        self.panels.append(panel)
        self.panels = sorted(self.panels, key=lambda panel: panel.depth)

    def mouse_motion(self, x, y):
        for panel in self.panels:
            if panel.mouse_motion(x, y):
                break

    def click(self, x, y):
        for panel in self.panels:
            if panel.is_main and panel.click(x, y):
                return True

        for panel in self.panels:
            if not panel.is_main and panel.click(x, y):
                return True
        return False

    def draw(self):
        for panel in self.panels:
            panel.draw()

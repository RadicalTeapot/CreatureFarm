# -*- coding: utf-8 -*-
"""DOCSTRING."""

import pyglet
import ui


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


class Tab(object):
    def __init__(self, title='', active=False, visible=True):
        self.title = title
        self.title_button = ui.Button(self.title)

        self.layout = None
        self.rect = ui.Rect(0, 0, 0, 0)

        self.buttons = []
        self.labels = []

        self.active = active
        self.visible = visible

    def set_layout(self, direction=0, spacing=10):
        self.layout = Layout(self, direction, spacing)

    def set_active(self, active):
        # TODO: Grey out title when tab not active
        self.active = active

    def set_visible(self, visible):
        self.visible = visible

    def add_button(self, button):
        self.layout.add_content(button)
        self.buttons.append(button)

    def add_buttons(self, buttons):
        self.layout.add_content(buttons)
        self.buttons.extend(buttons)

    def add_label(self, label):
        self.layout.add_content(label)
        self.labels.append(label)

    def draw(self):
        if not self.visible:
            return

        if len(self.title):
            self.title_button.draw()

        if not self.active:
            return

        for button in self.buttons:
            button.draw()
        for label in self.labels:
            label.draw()

    def mouse_motion(self, x, y):
        if not self.active or not self.visible:
            return

        for button in self.buttons:
            button.hover(x, y)

    def click(self, x, y):
        if not self.active or not self.visible:
            return

        pressed = [button.click(x, y) for button in self.buttons]
        if any(pressed):
            for button, state in zip(self.buttons, pressed):
                button.pressed = state


class Panel(object):
    border_margin = 3
    tab_spacing = 20

    def __init__(self, x, y, width, height, is_dialog=False, depth=-1):
        self.rect = ui.Rect(x, y, width, height)

        self.is_dialog = is_dialog
        self.displayed = not is_dialog
        self.depth = depth

        self.tab_groups = {}
        self.current_group = None

    def add_tab(self, group, active, title='', direction=0, spacing=10):
        tab = Tab(title)
        tab_group = self.tab_groups.get(group, [])

        tab_group.append(tab)
        self.tab_groups[group] = tab_group

        # Take panel border into account
        tab.rect.x = self.rect.x + 2 * self.border_margin
        tab.rect.y = self.rect.y + 2 * self.border_margin
        tab.rect.width = self.rect.width - 4 * self.border_margin
        tab.rect.height = self.rect.height - 4 * self.border_margin

        # Set tab button position
        x = self.rect.x + self.tab_spacing
        tab.title_button.y = (
            self.rect.height + self.rect.y -
            tab.title_button.rect.height + ui.Button.margin * 2
        )
        for tab in tab_group:
            if len(tab.title):
                tab.title_button.x = x
                x += tab.title_button.rect.width + self.tab_spacing

        tab.set_layout(direction, spacing)
        tab.set_active(active)
        if active:
            [tab.set_active(False) for tab in tab_group]
        tab.set_active(True)

        return tab

    def set_active_tab(self, title, group=None):
        tabs = self.get_tabs(group)

        for tab in tabs:
            tab.set_active(tab.title == title)

    def get_tabs(self, group=None):
        if group is None:
            group = self.current_group

        tabs = []
        if group is not None and group in self.tab_groups:
            tabs = self.tab_groups[group]
        else:
            [tabs.extend(value) for value in self.tab_groups.values()]

        return tabs

    def set_current_group(self, group):
        if group is None:
            self.current_group = None
            return

        if group not in self.tab_groups:
            raise KeyError('{} not in tab_groups'.format(group))
        self.current_group = group

    def add_button(self, tab, button):
        tab.add_button(button)

    def add_buttons(self, tab, buttons):
        tab.add_buttons(buttons)

    def add_label(self, tab, label):
        tab.add_label(label)

    def clear(self, tab):
        del tab.buttons[:]
        del tab.labels[:]
        tab.layout.clear()

    def show(self):
        self.displayed = True

    def hide(self):
        self.displayed = False

    def draw(self):
        if not self.displayed:
            return
        if self.is_dialog:
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

    def mouse_motion(self, x, y):
        if not self.displayed:
            return

        if self.current_group is None:
            return

        if not self.is_dialog and not self.rect.contains(x, y):
            for tab in self.tab_groups[self.current_group]:
                for button in tab.buttons:
                    button.hovered = False
                tab.title_button.hovered = False
            return

        for tab in self.tab_groups[self.current_group]:
            if len(tab.title):
                tab.title_button.hover(x, y)
            tab.mouse_motion(x, y)

    def click(self, x, y):
        if not self.displayed:
            return False

        if self.current_group is None:
            return False

        if self.rect.contains(x, y):
            for tab in self.tab_groups[self.current_group]:
                if len(tab.title):
                    if tab.title_button.click(x, y):
                        return True
                tab.click(x, y)
            return True
        return False

    def draw_contents(self):
        if self.current_group is None:
            return

        for tab in self.tab_groups[self.current_group]:
            tab.draw()

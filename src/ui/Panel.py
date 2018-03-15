# -*- coding: utf-8 -*-
"""DOCSTRING."""

import pyglet
import ui
from ui.Elements import Button
from Settings import Settings


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

    def __init__(self, x, y, width, height):
        self.rect = ui.Rect(x, y, width, height)
        self.border_rect = ui.Rect(
            x + self.border_margin, y + self.border_margin,
            width - 2 * self.border_margin, height - 2 * self.border_margin
        )
        self.border_rect.update_color((200, 200, 200))
        self.inner_rect = ui.Rect(
            x + 2 * self.border_margin, y + 2 * self.border_margin,
            width - 4 * self.border_margin, height - 4 * self.border_margin
        )

        self.tab_groups = {}
        self.current_group = None

    def add_tab(self, group, active, title='', direction=0, spacing=10):
        tab = Tab(title)
        tab_group = self.tab_groups.get(group, [])

        tab_group.append(tab)
        self.tab_groups[group] = tab_group

        # Take panel border into account
        tab.rect = self.inner_rect

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

    def draw(self):
        self.rect.draw()
        self.border_rect.draw()
        self.inner_rect.draw()
        self.draw_contents()

    def mouse_motion(self, x, y):
        if self.current_group is None:
            return

        if not self.rect.contains(x, y):
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


class Dialog(object):
    border_margin = 3
    content_margin = 10

    def __init__(self, text, callback=None):
        self.displayed = True
        self.callback = callback

        document = pyglet.text.decode_text(text)
        document.set_style(0, len(text), dict(color=(255, 255, 255, 255)))
        self.text = pyglet.text.layout.TextLayout(
            document, multiline=True, wrap_lines=False
        )

        self.button = Button('Ok')

        width = self.text.content_width + self.content_margin * 2
        height = (
            self.text.content_height +
            self.button.rect.height + self.content_margin * 4
        )
        x = Settings.WIDTH // 2 - width // 2
        y = Settings.HEIGHT // 2 - height // 2

        self.rect = ui.Rect(
            x - self.border_margin * 2, y - self.border_margin * 2,
            width + self.border_margin * 4, height + self.border_margin * 4
        )
        self.border_rect = ui.Rect(
            x - self.border_margin, y - self.border_margin,
            width + self.border_margin * 2, height + self.border_margin * 2
        )
        self.border_rect.update_color((200, 200, 200))
        self.inner_rect = ui.Rect(x, y, width, height)

        self.text.x = x + self.content_margin
        self.text.y = y + self.button.rect.height + self.content_margin * 3

        self.button.set_pos(
            x + width - self.button.rect.width - self.content_margin,
            y + self.content_margin
        )
        self.button.register_handler(self.accepted)

    def mouse_motion(self, x, y):
        self.button.hover(x, y)

    def click(self, x, y):
        # Steal the mouse click focus from other panel by not checking rect
        # containning click
        if self.displayed:
            self.button.click(x, y)
            return True
        return False

    def accepted(self):
        self.displayed = False
        if callable(self.callback):
            self.callback()

    def draw(self):
        if self.displayed:
            self.rect.draw()
            self.border_rect.draw()
            self.inner_rect.draw()
            self.text.draw()
            self.button.draw()

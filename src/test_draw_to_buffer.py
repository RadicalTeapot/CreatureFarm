# -*- coding: utf-8 -*-
"""DOCSTRING."""

import pyglet
import pyglet.gl as gl


BUF_WIDTH = 50
BUF_HEIGHT = 50


def set_viewport(width, height):
    gl.glViewport(0, 0, width, height)

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0, width, 0, height, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)


def clear(*color):
    gl.glClearColor(*color, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)


def draw_to_buffer():
    set_viewport(BUF_WIDTH, BUF_HEIGHT)
    clear(1, 0, 0)

    pyglet.graphics.draw_indexed(
        4,
        gl.GL_TRIANGLES,
        [0, 1, 2, 2, 1, 3],
        ('v2i', (
            25, 0,
            50, 25,
            0, 25,
            25, 50
        )),
        ('c3B', (
            0, 255, 0,
            255, 255, 0,
            0, 255, 255,
            0, 0, 255
        ))
    )


if __name__ == '__main__':
    texture = pyglet.image.Texture.create(BUF_WIDTH, BUF_HEIGHT, rectangle=True)
    gl.glTexParameteri(texture.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(texture.target, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

    window = pyglet.window.Window(width=800, height=600)

    @window.event
    def on_draw():
        draw_to_buffer()
        buffer = pyglet.image.get_buffer_manager().get_color_buffer()
        texture.blit_into(buffer, 0, 0, 0)

        set_viewport(window.width, window.height)

        clear(0, 0, 0)
        texture.blit(100, 100, width=400, height=400)

    pyglet.app.run()

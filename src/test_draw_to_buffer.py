# -*- coding: utf-8 -*-
"""DOCSTRING."""

import pyglet
import pyglet.gl as gl
import ctypes


BUF_WIDTH = 50
BUF_HEIGHT = 50


def build_buffer():
    buffer = gl.GLuint(0)
    gl.glGenFramebuffers(1, ctypes.byref(buffer))
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, buffer)

    texture = gl.GLuint(0)
    gl.glGenTextures(1, ctypes.byref(texture))
    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexImage2D(
        gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, BUF_WIDTH, BUF_HEIGHT,
        0, gl.GL_RGBA, gl.GL_FLOAT, None
    )
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST
    )
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST
    )

    gl.glFramebufferTexture2D(
        gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D,
        texture, 0
    )

    if (
        gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) !=
        gl.GL_FRAMEBUFFER_COMPLETE
    ):
        raise RuntimeError('Framebuffer incomplete !')

    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
    gl.glDisable(gl.GL_TEXTURE_2D)

    return buffer, texture


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
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, buffer)
    set_viewport(BUF_WIDTH, BUF_HEIGHT)
    clear(1, 0, 0)

    pyglet.graphics.draw_indexed(
        4, gl.GL_TRIANGLES,
        [0, 1, 2, 2, 1, 3],
        ('v2i', (
            0, 25,
            25, 50,
            25, 0,
            50, 25
        )),
        ('c3f', (
            0, 1, 0,
            1, 1, 0,
            1, 0, 1,
            0, 0, 1
        ))
    )

    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)


def draw_texture(texture):
    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)

    gl.glTranslatef(50, 50, 0)
    gl.glScalef(7, 7, 1)

    pyglet.graphics.draw_indexed(
        4,
        gl.GL_TRIANGLES,
        [0, 1, 2, 2, 1, 3],
        ('v2i', (
            0, 0,
            BUF_WIDTH, 0,
            0, BUF_HEIGHT,
            BUF_WIDTH, BUF_HEIGHT
        )),
        ('t2f', (
            0, 0,
            1, 0,
            0, 1,
            1, 1
        ))
    )

    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
    gl.glDisable(gl.GL_TEXTURE_2D)


if __name__ == '__main__':
    window = pyglet.window.Window(width=800, height=600)

    buffer, texture = build_buffer()

    @window.event
    def on_draw():
        draw_to_buffer(buffer)

        set_viewport(window.width, window.height)

        clear(0, 0, 0)
        draw_texture(texture)

    pyglet.app.run()

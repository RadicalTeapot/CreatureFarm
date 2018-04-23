# -*- coding: utf-8 -*-
"""DOCSTRING."""

import pyglet.gl as gl
import ctypes


class Buffer(object):
    def __init__(self):
        self.id = gl.GLuint(0)
        gl.glGenFramebuffers(1, ctypes.byref(self.id))

    def __enter__(self):
        self.bind()
        return self

    def bind(self):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.id)

    def __exit__(self, exec_type, exec_value, traceback):
        self.unbind()

    def unbind(self):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    def bind_texture(self, texture):
        with texture:
            gl.glFramebufferTexture2D(
                gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D,
                texture.id, 0
            )

            if (
                gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) !=
                gl.GL_FRAMEBUFFER_COMPLETE
            ):
                raise RuntimeError('Framebuffer incomplete !')


class Texture:
    def __init__(self, width, height):
        self.id = gl.GLuint(0)
        gl.glGenTextures(1, ctypes.byref(self.id))

        self.bind()
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height,
            0, gl.GL_RGBA, gl.GL_FLOAT, None
        )
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST
        )
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST
        )
        self.unbind()

    def bind(self):
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.id)

    def unbind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        gl.glDisable(gl.GL_TEXTURE_2D)

    def __enter__(self):
        self.bind()
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.unbind()

# -*- coding: utf-8 -*-
"""DOCSTRING."""

class GameSingleton(object):
    _instance = None

    @staticmethod
    def getInstance(window=None):
        if GameSingleton._instance is None:
            GameSingleton._instance = Game(window)
        return GameSingleton._instance

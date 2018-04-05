# -*- coding: utf-8 -*-
"""DOCSTRING."""

from collections import namedtuple

ACTIVITY_TYPE = namedtuple('activity_type', [
    'ADVENTURE', 'COOK'
])(
    'on an adventure', 'cooking'
)

ENTRY_TYPE = namedtuple('type', [
    'INFO',
    'IMPORTANT',
    'CRITICAL'
])

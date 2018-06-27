# -*- coding: utf-8 -*-
"""DOCSTRING."""

import logging
import os
from collections import OrderedDict


class LogEntry(object):
    def __init__(self, date, message, activity_type, entry_type):
        self.date = date
        self.message = message
        self.entry_type = entry_type
        self.activity_type = activity_type

    def __str__(self):
        return (
            f'{self.date} - {self.activity_type} - '
            f'{self.entry_type} - {self.message}'
        )


class Logger(object):
    def __init__(self, name):
        self.name = name
        self.entries = []

        # Create a logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        path = os.path.abspath('logs')
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, 'log.log')

        file_handler = logging.FileHandler(path, 'w')
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter('%(name)s - %(message)s')

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.callbacks = OrderedDict()

    def register_callback(self, name, func):
        if name in self.callbacks:
            raise KeyError(f'Callback {name} already exists.')
        if not callable(func):
            raise TypeError(f'Callback {name} not callable')
        self.callbacks[name] = func

    def deregister_callback(self, name):
        if name not in self.callbacks:
            raise KeyError(f'Callback {name} not registered')
        del self.callbacks[name]

    def add_entry(
        self, date, message, activity_type, entry_type
    ):
        entry = LogEntry(date, message, activity_type, entry_type)
        self.entries.append(entry)

        self.logger.info(f'{date} - {activity_type} - {entry_type} - {message}')

        for callback in self.callbacks.values():
            callback(entry)

    def get_log(self, date_range=None, activity_type=None, entry_type=None):
        log = [entry for entry in self.entries]
        if date_range is not None:
            log = [
                entry
                for entry in log
                if entry.date >= date_range[0] and entry.date <= date_range[1]
            ]
        if activity_type is not None:
            log = [
                entry
                for entry in log
                if entry.activity_type == activity_type
            ]
        if entry_type is not None:
            log = [
                entry
                for entry in log
                if entry.entry_type == entry_type
            ]

        return log

    def serialize(self):
        data = {}
        data['name'] = self.name
        data['entries'] = [
            {
                'date': entry.date,
                'message': entry.message,
                'entry_type': entry.entry_type,
                'activity_type': entry.activity_type
            }
            for entry in self.entries
        ]

        return data

    @classmethod
    def deserialize(cls, data):
        instance = cls(data['name'])
        for entry in data['entries']:
            instance.add_entry(
                entry['date'],
                entry['message'],
                entry['activity_type'],
                entry['entry_type']
            )
        return instance

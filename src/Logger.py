# -*- coding: utf-8 -*-
"""DOCSTRING."""

import logging


class LogEntry(object):
    def __init__(self, date, message, activity_type, entry_type):
        self.date = date
        self.message = message
        self.entry_type = entry_type
        self.activity_type = activity_type


class Logger(object):
    def __init__(self, name):
        self.entries = []

        # Create a logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler('logs/log.log', 'w')
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter('%(name)s - %(message)s')

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def add_entry(
        self, date, message, activity_type, entry_type
    ):
        self.entries.append(LogEntry(date, message, activity_type, entry_type))

        self.logger.info('{date} - {activity} - {level} - {message}'.format(
            date=date,
            activity=activity_type.name,
            level=entry_type.name,
            message=message
        ))

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

# -*- coding: utf-8 -*-
"""DOCSTRING."""


class LogEntry(object):
    def __init__(self, date, message, activity_type, entry_type):
        self.date = date
        self.message = message
        self.entry_type = entry_type
        self.activity_type = activity_type


class Logger(object):
    def __init__(self):
        self.entries = []

    def add_entry(
        self, date, message, activity_type, entry_type
    ):
        self.entries.append(LogEntry(date, message, activity_type, entry_type))

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

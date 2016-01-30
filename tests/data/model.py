#!/usr/bin/env python
# coding=utf-8

from unittest.mock import MagicMock


class ExampleModelPrivate(object):

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.to_json = MagicMock()
        self.to_dict = MagicMock()


class ExampleModel(ExampleModelPrivate):
    '''
    Example model for test
    '''
    model_entity = ExampleModelPrivate("Test", 99)
    objects = MagicMock(return_value=[model_entity])
    objects.get = MagicMock(return_value=model_entity)
    save = MagicMock()
    to_json = MagicMock()
    to_dict = MagicMock()

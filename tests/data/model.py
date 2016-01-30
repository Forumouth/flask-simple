#!/usr/bin/env python
# coding=utf-8


import json
from unittest.mock import MagicMock


class ExampleModelPrivate(object):

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.to_dict = MagicMock(return_value={
            "name": self.name,
            "age": self.age
        })
        self.to_json = MagicMock(
            return_value=json.dumps(self.to_dict.return_value)
        )
        self.get = MagicMock(return_value=self)

    def reset_mocks(self):
        self.get.reset_mock()
        self.to_dict.reset_mock()


class ExampleModel(ExampleModelPrivate):
    '''
    Example model for test
    '''
    model_entity = ExampleModelPrivate("Test", 99)
    objects = MagicMock(return_value=model_entity)

    @classmethod
    def reset_mocks(cls):
        cls.objects.get.reset_mock()
        cls.objects.reset_mock()
        cls.model_entity.reset_mocks()

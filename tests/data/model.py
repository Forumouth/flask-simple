#!/usr/bin/env python
# coding=utf-8


import json
from unittest.mock import MagicMock


class ExampleModelPrivate(object):
    initialized = MagicMock(return_value=None)
    save = MagicMock()

    def __init__(self, **kwargs):
        statecall = kwargs.pop("statecall", True)
        get_effect = kwargs.pop("get_effect", None)
        self.kwargs = kwargs
        self.to_dict = MagicMock(return_value=self.kwargs)
        self.to_json = MagicMock(
            return_value=json.dumps(self.to_dict.return_value)
        )
        self.get = MagicMock(return_value=self, side_effect=get_effect)
        if statecall:
            self.initialized(**self.kwargs)

    def reset_mocks(self):
        self.fields = {}
        self.initialized.reset_mock()
        self.get.reset_mock()
        self.to_dict.reset_mock()
        self.save.reset_mock()


class ExampleModel(ExampleModelPrivate):
    '''
    Example model for test
    '''
    model_entity = ExampleModelPrivate(name="Test", age=99, statecall=False)
    objects = MagicMock(return_value=model_entity)

    @classmethod
    def reset_mocks(cls):
        cls.objects.reset_mock()
        cls.model_entity.reset_mocks()

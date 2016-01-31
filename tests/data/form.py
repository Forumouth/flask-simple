#!/usr/bin/env python
# coding=utf-8

from unittest.mock import MagicMock


def generate_example_form(valid=True, errors=None):
    '''
    Generates example form for testing.
    :param valid: True if the form is valid, set otherwise
    '''

    class ExampleForm(object):
        '''
        Example form for test
        '''
        validate = MagicMock(return_value=valid)
        initialized = MagicMock(return_value=None)
        populate_obj = MagicMock(return_value=None)

        def __init__(self, *args, **kwargs):
            '''
            For args and kwargs, do nothing.
            '''
            self.errors = None
            self.initialized(*args, **kwargs)

        @classmethod
        def reset_mocks(cls):
            cls.validate.reset_mock()

    return ExampleForm

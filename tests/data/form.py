#!/usr/bin/env python
# coding=utf-8

from unittest.mock import MagicMock


def generate_example_form(valid=True):
    '''
    Generates example form for testing.
    :param valid: True if the form is valid, set otherwise
    '''

    class ExampleForm(object):
        '''
        Example form for test
        '''

        def __init__(self, *args, **kwargs):
            '''
            For args and kwargs, do nothing.
            '''

            self.validate = MagicMock(return_value=valid)

    return ExampleForm

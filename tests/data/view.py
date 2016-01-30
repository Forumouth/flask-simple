#!/usr/bin/env python
# coding=utf-8

from src import FlaskEasyView

from .model import ExampleModel
from .form import generate_example_form
from .testapp import testapp


class SimpleView(FlaskEasyView):
    '''
    Simple Example View for test
    '''
    route_prefix = "/simple"
    trailing_slash = False
    model = ExampleModel
    form = generate_example_form()


SimpleView.register(testapp)

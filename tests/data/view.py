#!/usr/bin/env python
# coding=utf-8

from flask.ext.simple import FlaskEasyView

from .model import ExampleModel
from .form import generate_example_form
from .testapp import app


class SimpleView(FlaskEasyView):
    '''
    Simple Example View for test
    '''
    trailing_slash = False
    model = ExampleModel
    form = generate_example_form()
    list_name = "simple"


class SimpleTemplateView(SimpleView):
    '''
    Simple Example View with render_template
    '''
    route_base = "/templated"
    template = "test.jinja"
    list_name = "simple_templated"


class WithoutFormView(FlaskEasyView):
    '''
    Simple Example View without form
    '''
    route_base = "/noform"
    trailing_slash = False
    model = ExampleModel
    list_name = "simple_no_form"


SimpleView.register(app)
SimpleTemplateView.register(app)
WithoutFormView.register(app)

#!/usr/bin/env python
# coding=utf-8

from .model import ExampleModel
from .form import generate_example_form
from .view import SimpleView, SimpleTemplateView, WithoutFormView
from .testapp import app

__all__ = [
    "ExampleModel",
    "generate_example_form",
    "SimpleView",
    "SimpleTemplateView",
    "WithoutFormView",
    "app"
]

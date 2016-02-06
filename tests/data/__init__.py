#!/usr/bin/env python
# coding=utf-8

from .model import ExampleModel
from .form import generate_example_form
from .view import (
    SimpleView, SimpleTemplateView, WithoutFormView,
    SimpleValidationFailureView
)
from .testapp import app

sample_oid = "56b5baab63cbbfb5dece4cbd"

__all__ = [
    "ExampleModel",
    "generate_example_form",
    "SimpleView",
    "SimpleTemplateView",
    "WithoutFormView",
    "SimpleValidationFailureView",
    "sample_oid",
    "app"
]

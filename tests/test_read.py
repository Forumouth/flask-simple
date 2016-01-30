#!/usr/bin/env python
# coding=utf-8

import json
from unittest import TestCase

from .data import app


class SimpleReadTest(TestCase):
    '''
    EasyView simply read tests without template.
    In this case, returns the returned value of model.to_json().
    '''

    def setUp(self):
        from .data import SimpleView
        app.testing = True
        self.client = app.test_client()
        self.view = SimpleView
        self.model = self.view.model

    def tearDown(self):
        self.model.reset_mocks()

    def test_index(self):
        '''
        Fetch the data as usual...
        '''
        with self.client as client:
            resp = client.get("/simple")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.mimetype, "application/json")
            self.assertDictEqual(json.loads(resp.data.decode("utf-8")), {
                self.view.list_name: (
                    self.model.model_entity.to_dict.return_value
                )
            })
        assert self.view.model.objects.called
        assert self.view.model.model_entity.to_json.called

    def test_get(self):
        '''
        Fetch the data by pk
        '''
        with self.client as client:
            resp = client.get("/simple/test")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.mimetype, "application/json")
            self.assertDictEqual(
                json.loads(resp.data.decode("utf-8")),
                self.model.model_entity.to_dict.return_value
            )
        self.view.model.objects.assert_called_once_with(pk="test")
        assert self.view.model.objects.return_value.get.called
        assert self.view.model.model_entity.to_json.called


class SimpleReadTestWithTemplate(TestCase):
    '''
    EasyView Simple read case with template
    In this case, render_template should be called with the template and
    model.
    '''

    def setUp(self):
        from .data import SimpleTemplateView
        from src.mocks import render_template
        app.testing = True
        self.client = app.test_client()
        self.view = SimpleTemplateView
        self.model = self.view.model
        self.render_template = render_template

    def tearDown(self):
        self.model.reset_mocks()
        self.render_template.reset_mock()

    def test_index(self):
        '''
        Render the template with model
        '''
        with self.client as client:
            resp = client.get("/templated")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.mimetype, "text/html")
            self.assertEqual(
                resp.data.decode("utf-8"),
                self.render_template.return_value
            )
        self.render_template.assert_called_once_with(
            self.view.template, model=self.model
        )

    def test_get(self):
        '''
        Render the template with model by pk-filtered
        '''
        with self.client as client:
            resp = client.get("/templated/test")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.mimetype, "text/html")
            self.assertEqual(
                resp.data.decode("utf-8"),
                self.render_template.return_value
            )
        self.render_template.assert_called_once_with(
            self.view.template, model=self.model
        )

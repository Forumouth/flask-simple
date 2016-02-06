#!/usr/bin/env python
# coding=utf-8

import json
from unittest import TestCase

from .data import app


class SimpleCreateValidTest(TestCase):
    '''
    Create test, and form validation is valid.
    '''
    def setUp(self):
        from .data import SimpleView
        app.testing = True
        self.client = app.test_client()
        self.view = SimpleView
        self.model = self.view.model
        self.form = self.view.form

    def tearDown(self):
        self.model.reset_mocks()
        self.form.reset_mocks()

    def test_post(self):
        data = {"test": "this is a test"}
        with self.client as cli:
            resp = cli.post(
                "/simple",
                data=json.dumps(data),
                headers={"Content-Type": "application/json"},
                follow_redirects=True
            )
            self.assertEqual(resp.status_code, 200)
            self.assertFalse(resp.data)
        self.form.initialized.assert_called_with(data=data)
        assert self.form.validate.called
        assert self.form.populate_obj.called
        self.assertIs(
            # I don't think this is good, if there is someone who
            # can code better, please create PR.
            type(self.form.populate_obj.call_args[0][0]), self.model
        )
        assert self.model.save.called


class CreationValidTestWithoutForm(TestCase):
    '''
    Creation test, but without form validator.
    '''
    def setUp(self):
        from .data import WithoutFormView
        app.testing = True
        self.client = app.test_client()
        self.view = WithoutFormView
        self.model = self.view.model

    def tearDown(self):
        self.model.reset_mocks()

    def test_post(self):
        data = {"name": "Test man", "age": 9}
        with self.client as cli:
            resp = cli.post(
                "/noform",
                data=json.dumps(data),
                headers={
                    "Content-Type": "application/json"
                },
                follow_redirects=True
            )
            self.assertEqual(resp.status_code, 200)
            self.assertFalse(resp.data)
        self.model.initialized.assert_called_once_with(**data)
        assert self.model.save.called


class SimpleCreateInvalidTest(TestCase):
    '''
    Create test, and form validation is NOT valid.
    '''
    def setUp(self):
        from .data import SimpleValidationFailureView
        app.testing = True
        self.client = app.test_client()
        self.view = SimpleValidationFailureView
        self.model = self.view.model
        self.form = self.view.form

    def tearDown(self):
        self.model.reset_mocks()
        self.form.reset_mocks()

    def test_post(self):
        data = {"test": "this is a test"}
        with self.client as cli:
            resp = cli.post(
                self.view.route_base,
                data=json.dumps(data),
                headers={
                    "Content-Type": "application/json"
                },
                follow_redirects=True
            )
            self.assertEqual(resp.status_code, 417)
            self.assertEqual(resp.mimetype, "application/json")
            self.assertDictEqual(
                json.loads(resp.data.decode("utf-8")), self.view.expected_err
            )
        self.form.initialized.assert_called_with(data=data)
        assert self.form.validate.called
        self.model.save.assert_not_called()

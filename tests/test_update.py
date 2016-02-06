#!/usr/bin/env python2
# coding=utf-8

import json
from unittest import TestCase

from .data import app, sample_oid


class SimpleTestCaseBase(TestCase):
    def setUp(self):
        from .data import SimpleView
        self.view = SimpleView
        self.model = self.view.model
        self.data = self.model.model_entity.kwargs
        self.form = self.view.form
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        self.model.reset_mocks()
        self.form.reset_mocks()

    def model_must_be_updated(self):
        self.model.objects.assert_called_once_with(pk=sample_oid)
        assert self.model.model_entity.get.called
        self.form.initialized.assert_called_once_with(self.data)
        assert self.form.validate.called
        self.form.populate_obj.assert_called_once_with(
            self.model.model_entity
        )
        assert self.model.model_entity.save.called


class TestSimpleValidUpdate(SimpleTestCaseBase):
    '''
    Test simple valid update
    '''

    def test_simple_put(self):
        '''
        Sending PUT request, then response correctly
        '''
        with self.client as client:
            resp = client.put(
                ("/simple/{}").format(sample_oid),
                data=json.dumps(self.data),
                headers={"Content-Type": "application/json"},
                follow_redirects=True
            )
            self.assertEqual(resp.status_code, 200)
            self.assertFalse(resp.data)
        self.model_must_be_updated()

    def test_simple_patch(self):
        '''
        Sending patch request, then response correctly
        '''
        with self.client as client:
            resp = client.patch(
                ("/simple/{}").format(sample_oid),
                data=json.dumps(self.data),
                headers={"Content-Type": "application/json"},
                follow_redirects=True
            )
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.mimetype, "application/json")
            self.assertDictEqual(
                json.loads(resp.data.decode("utf-8")), self.data
            )
        self.model_must_be_updated()

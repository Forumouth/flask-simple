#!/usr/bin/env python
# coding=utf-8

import json
from flask import current_app, jsonify
from flask.ext.classy import FlaskView


class FlaskEasyView(FlaskView):
    '''
    Flask Easy View class
    '''

    def __render_template__(self, *args, **kwargs):
        if current_app.testing:
            from .mocks import render_template
        else:
            from flask import render_template
        return render_template(*args, **kwargs)

    def __json_or_render__(self, model, query_mode=False):
        template = getattr(self, "template", None)
        if template:
            return self.__render_template__(template, model=self.model)
        else:
            if query_mode:
                return jsonify({self.list_name: json.loads(model.to_json())})
            else:
                return jsonify(json.loads(model.to_json()))

    def index(self):
        entity = self.model.objects()
        return self.__json_or_render__(entity, True)

    def get(self, pk):
        entity = self.model.objects(pk=pk).get()
        return self.__json_or_render__(entity)

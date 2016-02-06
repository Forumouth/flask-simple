#!/usr/bin/env python
# coding=utf-8

import json
from flask import current_app, jsonify, request, make_response
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

    def post(self):
        model = None
        if hasattr(self, "form"):
            form = self.form(data=request.get_json())
            if not form.validate():
                return make_response(jsonify(form.errors), 417)
            model = self.model()
            form.populate_obj(model)
        else:
            model = self.model(**request.get_json())
        model.save()
        return "", 200

    def __update(self, _id):
        form = self.form(request.get_json())
        form.validate()

        model = self.model.objects(pk=_id).get()
        form.populate_obj(model)
        model.save()
        return model

    def put(self, _id):
        self.__update(_id)
        return "", 200

    def patch(self, _id):
        updated_model = self.__update(_id)
        return jsonify(json.loads(updated_model.to_json()))

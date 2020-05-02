#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    question = StringField('Search', validators=[DataRequired()])
    button = SubmitField('Search')

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formadata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
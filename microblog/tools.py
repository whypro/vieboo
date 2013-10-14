# -*- coding: utf-8 -*-
from flask import current_app
from flask.ext.themes import render_theme_template


def get_default_theme():
    return current_app.config['DEFAULT_THEME']


def render_template(template, **context):
    return render_theme_template(get_default_theme(), template, **context)
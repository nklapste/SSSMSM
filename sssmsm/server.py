# -*- coding: utf-8 -*-

"""Flask server definition"""

from logging import getLogger

from flask import Flask, render_template

__log__ = getLogger(__name__)

APP = Flask(__name__)

DEFAULT_REDIS_HOST = 'redis'
DEFAULT_REDIS_PORT = 6379


@APP.route('/', methods=["GET"])
def index():
    return render_template('index.html')

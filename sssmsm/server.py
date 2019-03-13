# -*- coding: utf-8 -*-

"""Flask server definition"""

import datetime
from enum import Enum
from logging import getLogger

from flask import Flask, render_template, request
from flask_restplus import Api, Resource, fields

__log__ = getLogger(__name__)

APP = Flask(__name__)

######################
# frontend definition
######################


@APP.route('/', methods=["GET"])
def index():
    return render_template('index.html')


#################
# API definition
#################

# TODO: enable for prod
# # TODO: make so that it can be enabled/disabled
# # monkey patch courtesy of
# # https://github.com/noirbizarre/flask-restplus/issues/54
# # so that /swagger.json is served over https
# from flask import url_for
#
#
# @property
# def specs_url(self):
#     """Monkey patch for HTTPS"""
#     return url_for(self.endpoint('specs'), _external=True, _scheme='https')
# Api.specs_url = specs_url

__api_version__ = (0, 0, 0)


API = Api(
    APP,
    version="{}.{}.{}".format(*__api_version__),
    title='SSSMSM API',
    doc='/api/doc',
    description='API for the '
                'Super Simple Scalable MicroService Manager (SSSMSM)!',
    contact_email="nklapste@ualberta.ca",
)


instance_status_request_model = API.model(
    'instance_status_request',
    {
        'name': fields.String(description='Name noting type of the instance'),
    }
)


class InstanceStatus(Enum):
    created = 'created'
    destroyed = 'destroyed'


instance_status_update_model = API.model(
    'instance_status_update',
    {
        'name': fields.String(description='Name noting type of the instance'),
        'status': fields.String(description='Updated status of the instance',
                                enum=InstanceStatus._member_names_),  # pylint: disable=no-member
        'date_updated': fields.DateTime(dt_format='iso8601'),
    }
)


@API.route('/api/create')
class CreateInstance(Resource):
    @API.expect(instance_status_request_model)
    @API.marshal_with(instance_status_update_model, code=201,
                      description='Instance created')
    def post(self):
        json_data = request.json
        return {
            "name": json_data["name"],
            "status": "created",
            "date_updated": datetime.datetime.utcnow().isoformat()
        }, 201


@API.route('/api/destroy')
class DestroyInstance(Resource):
    @API.expect(instance_status_request_model)
    @API.marshal_with(instance_status_update_model, code=202,
                      description='Instance destroyed')
    def post(self):
        json_data = request.json
        return {
            "name": json_data["name"],
            "status": "destroyed",
            "date_updated": datetime.datetime.utcnow().isoformat()
        }, 202
        # NOTE: using http 202 accepted as we likely have to
        # process removal slowly

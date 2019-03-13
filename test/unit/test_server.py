# -*- coding: utf-8 -*-

"""pytests for :mod:`sssmsm.server`"""

import json

import pytest
from flask import Response

import sssmsm.server


@pytest.fixture
def client():
    sssmsm.server.APP.config['TESTING'] = True
    client = sssmsm.server.APP.test_client()
    yield client


def test_get_index(client):
    resp: Response = client.get('/')
    assert resp
    assert resp.status == "200 OK"
    assert resp.mimetype == "text/html"
    assert b"Hello World!" in resp.data


def test_get_api_docs(client):
    resp: Response = client.get('/api/doc')
    assert resp
    assert resp.status == "200 OK"
    assert resp.mimetype == "text/html"
    assert b"SSSMSM API" in resp.data


def test_post_create(client):
    resp: Response = client.post(
        "/api/create",
        data=json.dumps({"name": "ssswms"}),
        content_type='application/json'
    )
    assert resp
    assert resp.status == "201 CREATED"
    assert resp.mimetype == "application/json"
    assert resp.json


def test_post_destroy(client):
    resp: Response = client.post(
        "/api/destroy",
        data=json.dumps({"name": "ssswms"}),
        content_type='application/json'
    )
    assert resp
    assert resp.status == "202 ACCEPTED"
    assert resp.mimetype == "application/json"
    assert resp.json

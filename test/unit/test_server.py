# -*- coding: utf-8 -*-

"""pytests for :mod:`ghast.server`"""

import pytest

import ghast.server

ghast.server.APP.register_blueprint(
    ghast.server.API_BLUEPRINT,
    url_prefix="/test"
)


@pytest.fixture(scope="session")
def client():
    ghast.server.APP.config['TESTING'] = True
    client = ghast.server.APP.test_client()
    yield client


def test_get_index(client):
    resp = client.post('/test/')
    assert resp
    assert resp.status == "200 OK"
    assert resp.mimetype == "application/json"
    assert b"{}" in resp.data


def test_get_api_docs(client):
    resp = client.get('/test/doc')
    assert resp
    assert resp.status == "200 OK"
    assert resp.mimetype == "text/html"
    assert b"Graylog HTTP Alert Script Triggerer (ghast) API" in resp.data

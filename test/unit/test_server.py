# -*- coding: utf-8 -*-

"""pytests for :mod:`sssmsm.server`"""

import pytest

import sssmsm.server


@pytest.fixture(scope="session")
def client():
    sssmsm.server.APP.config['TESTING'] = True
    sssmsm.server.APP.register_blueprint(
        sssmsm.server.API_BLUEPRINT,
        url_prefix="/test"
    )
    client = sssmsm.server.APP.test_client()
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
    assert b"SSSMSM API" in resp.data

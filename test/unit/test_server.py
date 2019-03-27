# -*- coding: utf-8 -*-

"""pytests for :mod:`ghast.server`"""

import pytest
import subprocess

import ghast.server

from unittest.mock import patch

ghast.server.APP.register_blueprint(
    ghast.server.API_BLUEPRINT,
    url_prefix="/test"
)


@pytest.fixture(scope="session")
def client():
    ghast.server.APP.config['TESTING'] = True
    client = ghast.server.APP.test_client()
    yield client


@pytest.fixture()
def client_with_script():
    ghast.server.APP.config['TESTING'] = True
    ghast.server.ALERT_SCRIPT_PATH = "foobar"
    client = ghast.server.APP.test_client()
    yield client
    ghast.server.ALERT_SCRIPT_PATH = None


def test_invalid_get_method(client):
    resp = client.get('/test/')
    assert resp
    assert resp.status == "405 METHOD NOT ALLOWED"
    assert resp.mimetype == "application/json"
    assert resp.json


def test_receive_graylog_http_alert_callback_no_script(client):
    resp = client.post('/test/')
    assert resp
    assert resp.status == "200 OK"
    assert resp.mimetype == "application/json"
    assert b'{"script": null, "script_return_code": null}' in resp.data
    assert resp.json


def test_receive_graylog_http_alert_callback_script(client_with_script):
    with patch.object(subprocess, "call", return_value=0) as \
            mock_subprocess_call:
        resp = client_with_script.post('/test/')
        assert resp
        assert resp.status == "200 OK"
        assert resp.mimetype == "application/json"
        assert b'{"script": "foobar", "script_return_code": 0}' in resp.data
        assert resp.json
        mock_subprocess_call.assert_called_once_with("foobar")


def test_get_api_docs(client):
    resp = client.get('/test/doc')
    assert resp
    assert resp.status == "200 OK"
    assert resp.mimetype == "text/html"
    assert b"Graylog HTTP Alert Script Triggerer (ghast) API" in resp.data

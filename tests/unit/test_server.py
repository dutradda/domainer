from domainer.domain import Domain

from connexion.apps.aiohttp_app import AioHttpApp
from connexion.apps.flask_app import FlaskApp

import logging
import mock
import pytest


@pytest.fixture
def aiohttp_app_cls_mock(monkeypatch):
    mock_ = mock.MagicMock(wraps=AioHttpApp)
    mock_.return_value.run = mock.MagicMock()
    monkeypatch.setattr('domainer.server.AioHttpApp', mock_)
    return mock_


@pytest.fixture
def domain_server_cls(aiohttp_app_cls_mock):
    from domainer.server import DomainServer
    return DomainServer


@pytest.fixture
def domain_mock():
    domain = Domain('Domainer Test', '0.0.1', mock.MagicMock(),
                    description='Testing Domainer Framework')
    mock_ = mock.MagicMock(wraps=domain)
    return mock_


@pytest.fixture
def flask_app_cls_mock():
    mock_ = mock.MagicMock(wraps=FlaskApp)
    mock_.return_value.run = mock.MagicMock()
    return mock_


def test_run(domain_server_cls, aiohttp_app_cls_mock, domain_mock):
    server = domain_server_cls(domain_mock)
    server.run()
    logger = logging.getLogger('connexion.aiohttp_app')

    assert aiohttp_app_cls_mock.return_value.run.call_args_list == [mock.call()]


def test_run_with_flask_app(domain_server_cls, flask_app_cls_mock, domain_mock):
    server = domain_server_cls(domain_mock, app_cls=flask_app_cls_mock)
    server.run()
    logger = logging.getLogger('connexion.flask_app')

    assert flask_app_cls_mock.return_value.run.call_args_list == [mock.call()]

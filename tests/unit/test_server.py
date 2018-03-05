import logging

import mock
import pytest
from domainer.constants import APP_CLS
from domainer.domain import Domain


@pytest.fixture
def default_app_cls_mock(monkeypatch):
    mock_ = mock.MagicMock(wraps=APP_CLS)
    mock_.return_value.run = mock.MagicMock()
    monkeypatch.setattr('domainer.server.APP_CLS', mock_)
    return mock_


@pytest.fixture
def domain_server_cls(default_app_cls_mock):
    from domainer.server import DomainServer
    return DomainServer


@pytest.fixture
def domain_mock():
    domain = Domain(mock.MagicMock())
    mock_ = mock.MagicMock(wraps=domain)
    return mock_


@pytest.fixture
def flask_app_cls_mock():
    mock_ = mock.MagicMock(wraps=FlaskApp)
    mock_.return_value.run = mock.MagicMock()
    return mock_


def test_run(domain_server_cls, default_app_cls_mock, domain_mock):
    server = domain_server_cls(domain_mock)
    server.run()
    logger = logging.getLogger('connexion.aiohttp_app')

    assert default_app_cls_mock.return_value.run.call_args_list == [mock.call()]

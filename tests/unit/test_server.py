import six

import mock
import pytest
from domainer.domain import Domain
from domainer.exceptions import DomainerError

if six.PY34:
    @pytest.fixture
    def aiohttp_app_factory_mock(monkeypatch):
        mock_ = mock.MagicMock()
        monkeypatch.setattr('domainer.server.AioHttpAppFactory', mock_)
        return mock_
else:
    @pytest.fixture
    def aiohttp_app_factory_mock():
        return mock.MagicMock()


@pytest.fixture
def flask_app_factory_mock(monkeypatch):
    mock_ = mock.MagicMock()
    monkeypatch.setattr('domainer.server.FlaskAppFactory', mock_)
    return mock_


@pytest.fixture
def domain_server_cls(aiohttp_app_factory_mock, flask_app_factory_mock):
    from domainer.server import DomainServer
    return DomainServer


@pytest.fixture
def domain_mock():
    subdomain = mock.MagicMock()
    subdomain.name = 'test'
    domain = Domain(subdomain)
    mock_ = mock.MagicMock(wraps=domain)
    return mock_


def test_init_with_app_factory_flask_cls(domain_server_cls, aiohttp_app_factory_mock,
                                         flask_app_factory_mock, domain_mock):
    assert domain_server_cls('', domain_mock, app_factory=flask_app_factory_mock)


def test_init_with_app_factory_flask(domain_server_cls, aiohttp_app_factory_mock,
                                     flask_app_factory_mock, domain_mock):
    assert domain_server_cls('', domain_mock, app_factory='flask')


if six.PY34:
    def test_init_with_app_factory_aiohttp(domain_server_cls, aiohttp_app_factory_mock,
                                           flask_app_factory_mock, domain_mock):
        assert domain_server_cls('', domain_mock, app_factory='aiohttp')

    def test_run(domain_server_cls, aiohttp_app_factory_mock, domain_mock):
        server = domain_server_cls('', domain_mock)
        server.run()

        assert aiohttp_app_factory_mock.make.return_value.run.call_args_list == [mock.call()]

else:
    def test_init_error_with_app_factory_aiohttp(domain_server_cls, flask_app_factory_mock,
                                                 domain_mock):
        with pytest.raises(DomainerError):
            domain_server_cls('', domain_mock, app_factory='aiohttp')

    def test_run(domain_server_cls, flask_app_factory_mock, domain_mock):
        server = domain_server_cls('', domain_mock)
        server.run()

        assert flask_app_factory_mock.make.return_value.run.call_args_list == [mock.call()]

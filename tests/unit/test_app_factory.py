import six

import mock
import pytest


@pytest.fixture
def validate_spec_mock(monkeypatch):
    mock_ = mock.MagicMock()
    mock_.return_value.spec_derefered = {}
    monkeypatch.setattr('domainer.app_factory.validate_spec', mock_)
    return mock_


def test_if_validate_spec_was_called(validate_spec_mock):
    from domainer.app_factory import FlaskAppFactory
    spec = {}
    flask_app = FlaskAppFactory.make('test')
    flask_app.add_api(spec)
    assert validate_spec_mock.call_args_list == [mock.call(spec)]


if six.PY34:
    def test_if_validate_spec_was_called_with_aiohttp(validate_spec_mock):
        from domainer.app_factory import AioHttpAppFactory
        spec = {}
        aiohttp_app = AioHttpAppFactory.make('test')
        aiohttp_app.add_api(spec)
        assert validate_spec_mock.call_args_list == [mock.call(spec)]


def test_resolve_operation_id_empty(validate_spec_mock):
    from domainer.app_factory import FlaskAppFactory
    spec = {}
    operation = mock.MagicMock()
    operation.operation = {}
    flask_app = FlaskAppFactory.make('test')
    api = flask_app.add_api(spec)
    assert api.resolver.resolve_operation_id(operation) == ''


def test_resolve_operation_id(validate_spec_mock):
    from domainer.app_factory import FlaskAppFactory
    spec = {}
    operation = mock.MagicMock()
    operation.operation = {
        'x-swagger-domain-module': 'test_domain',
        'operationId': 'testing'
    }
    flask_app = FlaskAppFactory.make('test')
    api = flask_app.add_api(spec)
    assert api.resolver.resolve_operation_id(operation) == \
        'test_domain.testing'

import six
from connexion.apps.flask_app import FlaskApp

import mock
import pytest

if six.PY34:
    from connexion.apps.aiohttp_app import AioHttpApp

    @pytest.fixture
    def aiohttp_app_mock(monkeypatch):
        mock_ = mock.MagicMock(wraps=AioHttpApp)
        return mock_
else:
    @pytest.fixture
    def aiohttp_app_mock():
        return mock.MagicMock()


@pytest.fixture
def flask_app_mock(monkeypatch):
    mock_ = mock.MagicMock(wraps=FlaskApp)
    return mock_


@pytest.fixture
def minimal_swagger_spec():
    return {
      "swagger": "2.0",
      "info": {
        "version": "1.0.0",
        "title": "Swagger Petstore"
      },
      "paths": {
        "/pets": {
          "get": {
            "operationId": "mock.Mock.__init__",
            "description": "Returns all pets",
            "responses": {
              "200": {
                "description": "A list of pets."
              }
            }
          }
        }
      }
    }


def test_flask_app_add_api(minimal_swagger_spec):
    from domainer.app_factory import FlaskAppFactory
    flask_app = FlaskAppFactory.make('test')
    assert flask_app.add_api(minimal_swagger_spec)


if six.PY34:
    def test_aiohttp_app_add_api(minimal_swagger_spec):
        from domainer.app_factory import AioHttpAppFactory
        aiohttp_app = AioHttpAppFactory.make('test')
        assert aiohttp_app.add_api(minimal_swagger_spec)

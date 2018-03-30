import six

from domainer.app_factory import FlaskAppFactory
from domainer.exceptions import DomainerError

if six.PY34:  # pragma: 2.7 no cover
    from domainer.app_factory import AioHttpAppFactory


class DomainServer(object):

    _app_cls = None

    def __init__(self, spec, domain, app_kwargs={},
                 api_kwargs={}, app_factory=None):
        if app_factory is None:
            if six.PY34:  # pragma: 2.7 no cover
                app_factory = AioHttpAppFactory
            else:  # pragma: 3 no cover
                app_factory = FlaskAppFactory

        elif app_factory == 'flask':
            app_factory = FlaskAppFactory
        elif app_factory == 'aiohttp':  # pragma: 2.7 no cover
            if not six.PY34:  # pragma: 3 no cover
                raise DomainerError("'aiohttp' app_factory just can be used "
                                    "with python >= 3.4")

            app_factory = AioHttpAppFactory

        self.domain = domain
        self._set_app(app_factory, **app_kwargs)
        self._api = self._app.add_api(spec, **api_kwargs)

    def _set_app(self, app_factory, **kwargs):
        import_name = self.domain.__module__
        self._app = app_factory.make(import_name, **kwargs)

    def run(self, **kwargs):
        self._app.run(**kwargs)

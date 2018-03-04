import six

from domainer.constants import APP_CLS


class DomainServer(object):

    _app_cls = None

    def __init__(self, spec, domain, app_kwargs={}, api_kwargs={}):
        self.domain = domain
        self._set_app(**app_kwargs)
        self._api = self._app.add_api(spec, **api_kwargs)

    def _set_app(self, **kwargs):
        if six.PY34:  # pragma: 2.7 no cover
            kwargs['only_one_api'] = True

        import_name = self.domain.__module__
        self._app = APP_CLS(import_name, **kwargs)

    def run(self, **kwargs):
        if self.domain:
            self.domain.configure_environment()

        self._app.run(**kwargs)

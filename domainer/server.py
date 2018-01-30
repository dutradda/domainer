from connexion.apps.aiohttp_app import AioHttpApp


class DomainServer(object):

    def __init__(self, domain, app_cls=None, app_kwargs={}, api_kwargs={}):
        if app_cls is None:
            app_cls = AioHttpApp
            app_kwargs['only_one_api'] = True

        spec = domain.get_swagger_spec()

        self._import_name = domain.__module__
        self._app = app_cls(self._import_name, **app_kwargs)
        self._api = self._app.add_api(spec, **api_kwargs)

    def run(self, **kwargs):
        self._app.run(**kwargs)

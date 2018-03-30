import six
from connexion.apps.flask_app import FlaskApp
from openapi21 import validate_spec


class AppFactoryMeta(type):

    def _make(cls, app_base_cls, *args, **kwargs):
        def __init__(self, *args_, **kwargs_):
            app_base_cls.__init__(self, *args_, **kwargs_)
            api_cls_name = cls.build_cls_name(self.api_cls)
            methods = {'_validate_spec': _validate_spec}
            self.api_cls = type(api_cls_name, (self.api_cls,), methods)

        cls_name = cls.build_cls_name(app_base_cls)
        methods = {'__init__': __init__}
        app_cls = type(cls_name, (app_base_cls,), methods)
        app_cls._validate_spec = _validate_spec
        return app_cls(*args, **kwargs)

    def build_cls_name(cls, other_cls):
        return 'Domainer{}'.format(other_cls.__name__)


def _validate_spec(self, spec):
    validate_spec(spec)


if six.PY34:  # pragma: 2.7 no cover
    from connexion.apps.aiohttp_app import AioHttpApp

    @six.add_metaclass(AppFactoryMeta)
    class AioHttpAppFactory(object):

        @classmethod
        def make(cls, *args, **kwargs):
            if len(args) < 2:
                args = (args[0], kwargs.pop('only_one_api', True))
            return cls._make(AioHttpApp, *args, **kwargs)


@six.add_metaclass(AppFactoryMeta)
class FlaskAppFactory(object):

    @classmethod
    def make(cls, *args, **kwargs):
        return cls._make(FlaskApp, *args, **kwargs)

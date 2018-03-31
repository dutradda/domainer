import six
from connexion.apps.flask_app import FlaskApp
from connexion.resolver import Resolver
from openapi21 import validate_spec


class _DomainerResolver(Resolver):

    def resolve_operation_id(self, operation):
        spec = operation.operation
        x_domain_module = spec.get('x-swagger-domain-module', '')
        x_subdomain_module = spec.get('x-swagger-subdomain-module', '')
        x_router_controller = spec.get('x-swagger-router-controller', '')
        modules = [module for module in (x_domain_module, x_subdomain_module,
                                         x_router_controller) if module]

        if modules:
            spec['x-swagger-router-controller'] = '.'.join(modules)

        return Resolver.resolve_operation_id(self, operation)


class AppFactoryMeta(type):

    def _make(cls, app_base_cls, *args, **kwargs):
        cls_name = cls.build_cls_name(app_base_cls)
        methods = {
            '__init__': _build_app_init(cls, app_base_cls),
            'add_api': _build_app_add_api(app_base_cls)
        }
        app_cls = type(cls_name, (app_base_cls,), methods)
        return app_cls(*args, **kwargs)

    def build_cls_name(cls, other_cls):
        return 'Domainer{}'.format(other_cls.__name__)


def _build_app_init(cls, app_base_cls):
    def _app_init(self, *args_, **kwargs_):
        app_base_cls.__init__(self, *args_, **kwargs_)
        api_cls_name = cls.build_cls_name(self.api_cls)
        methods = {
            '__init__': _api_init,
            '_validate_spec': _api_validate_spec
        }
        self.api_cls = type(api_cls_name, (self.api_cls,), methods)
    return _app_init


def _api_init(self, specification, base_path=None, arguments=None,
              validate_responses=False, strict_validation=False,
              resolver=_DomainerResolver(), auth_all_paths=False, debug=False,
              resolver_error_handler=None, validator_map=None,
              pythonic_params=False, options=None, **old_style_options):
    super(type(self), self).__init__(
        specification, base_path=base_path, arguments=arguments,
        validate_responses=validate_responses,
        strict_validation=strict_validation, resolver=resolver,
        auth_all_paths=auth_all_paths, debug=debug,
        resolver_error_handler=resolver_error_handler,
        validator_map=validator_map, pythonic_params=pythonic_params,
        options=options, **old_style_options
    )


def _api_validate_spec(self, spec):
    self.spec_resolver = validate_spec(spec)
    self.specification = self.spec_resolver.spec_derefered


def _build_app_add_api(app_base_cls):
    def _app_add_api(self, specification, base_path=None, arguments=None,
                     auth_all_paths=None, validate_responses=False,
                     strict_validation=False, resolver=_DomainerResolver(),
                     resolver_error=None, pythonic_params=False,
                     options=None, **old_style_options):
        return app_base_cls.add_api(
            self, specification, base_path=base_path, arguments=arguments,
            auth_all_paths=auth_all_paths,
            validate_responses=validate_responses,
            strict_validation=strict_validation, resolver=resolver,
            resolver_error=resolver_error, pythonic_params=pythonic_params,
            options=options, **old_style_options
        )
    return _app_add_api


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

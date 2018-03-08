import re

from six import add_metaclass

from domainer.exceptions import DomainerError


class _MetaLayersBase(type):

    def new_cls(cls, name):
        name = camelCase_to_snake_case(name + '_{}'.format(cls.__pattern__))
        return type(cls)(name, (cls,), {})

    def get_name(cls):
        name = camelCase_to_snake_case(cls.__name__)
        return name

    def _raise_invalid_cls(cls, invalid_cls):
        if cls is invalid_cls:
            raise DomainerError("The class '{}' "
                                "cannot be instantiated! "
                                "Inherit this class instead.".format(
                                    invalid_cls.get_name()
                                ))


def camelCase_to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


@add_metaclass(_MetaLayersBase)
class _LayersBase(object):
    pass

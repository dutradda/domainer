from domainer.layers._base import _LayersBase


class BaseActiveRecord(_LayersBase):

    __pattern__ = 'active_record'

    def __new__(cls, *args, **kwargs):
        cls._raise_invalid_cls(BaseActiveRecord)
        return object.__new__(cls)

    def __init__(self, daos):
        self.daos = daos

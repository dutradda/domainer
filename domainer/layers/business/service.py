from domainer.layers._base import _LayersBase


class BaseService(_LayersBase):

    __pattern__ = 'service'

    def __new__(cls, *args, **kwargs):
        cls._raise_invalid_cls(BaseService)
        return object.__new__(cls)

    def __init__(self, daos, active_records, repositories):
        self.daos = daos
        self.active_records = active_records
        self.repositories = repositories

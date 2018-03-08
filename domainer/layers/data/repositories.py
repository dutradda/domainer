from domainer.layers._base import _LayersBase


class BaseRepository(_LayersBase):

    __pattern__ = 'repository'

    def __new__(cls, *args, **kwargs):
        cls._raise_invalid_cls(BaseRepository)
        return object.__new__(cls)

    def __init__(self, daos, active_records):
        self.daos = daos
        self.active_records = active_records

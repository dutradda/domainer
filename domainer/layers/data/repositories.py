from domainer.exceptions import DomainerError
from domainer._domainer_base import (_SetActiveRecordsMixin,
                                     _SetDaosMixin,
                                     _SetRepositoriesMixin)


class BaseRepository(_SetActiveRecordsMixin,
                     _SetDaosMixin):

    def __new__(cls, *args, **kwargs):
        cls._raise_invalid_cls(BaseRepository)
        return object.__new__(cls)

    def __init__(self, daos=None, active_records=None):
        self._set_daos(daos)
        self._set_active_records(active_records)

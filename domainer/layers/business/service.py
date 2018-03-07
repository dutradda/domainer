from domainer.exceptions import DomainerError
from domainer._domainer_base import (_SetActiveRecordsMixin,
                                     _SetDaosMixin,
                                     _SetRepositoriesMixin)


class BaseService(_SetActiveRecordsMixin,
                  _SetDaosMixin,
                  _SetRepositoriesMixin):

    def __new__(cls, *args, **kwargs):
        cls._raise_invalid_cls(BaseService)
        return object.__new__(cls)

    def __init__(self, active_records=None, repositories=None, daos=None):
        self._set_daos(daos)
        self._set_active_records(active_records)
        self._set_repositories(repositories)

from domainer.exceptions import DomainerError


class BaseService(object):

    name = None

    def __new__(cls, *args, **kwargs):
        if cls is BaseService:
            raise DomainerError("The class 'BaseService' "
                                "cannot be instantiated! "
                                "Inherit this class instead.")
        return object.__new__(cls)

    def __init__(self, daos, active_records, repositories):
        self._daos = daos
        self._active_records = active_records
        self._repositories = repositories

    def get_name(self):
        if self.name is None:
            return type(self).__name__
        else:
            return self.name


class GenericService(BaseService):

    def __init__(self, name, daos, active_records, repositories):
        self.name = name
        BaseService.__init__(self, daos, active_records, repositories)

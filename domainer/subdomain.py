from six import iteritems

from domainer.layers.application.controller import GenericController
from domainer.layers.business.service import GenerericService
from domainer.layers.data.repositories import GenerericRepository
from domainer.exceptions import DomainerError


class Subdomain(object):

    def __init__(self, name, services=set(), active_records=set(),
                 repositories=set(), controller=None, daos=None):
        if (not services and not active_records and 
                not repositories and controller is None):
            raise DomainerError("At least one of these arguments must be "
                                "setted: 'services', 'active_records', "
                                "'repositories' or 'controller'.")
        if daos is None:
            daos = {}
        self._daos = daos
        self._all_subdomains = {}
        self._active_records = {}
        self._repositories = {}
        self.services = self.s = {}
        self._set_active_records(active_records)
        self._set_repositories(repositories)
        self._set_services(services)
        self._set_controller(controller)

    def _set_active_records(self, active_records):
        for active_record in active_records:
            active_record_name = active_record.get_name()
            active_record_instance = active_record(self._daos)
            self._active_records[active_record_name] = active_record_instance

    def _set_repositories(self, repositories):
        for repository in repositories:
            repository_name = repository.get_name()
            repository_instance = repository(self._daos, self._active_records)
            self._repositories[repository_name] = repository_instance

    def _set_services(self, services):
        for service in services:
            service_name = service.get_name()
            service_instance = service(self._daos, self._active_records,
                                       self._repositories)
            self.s[service_name] = service_instance

    def _set_controller(self, controller_cls):
        if controller_cls is None:
            controller = self._discover_controller()
        else:
            controller = self._build_controller(controller_cls)

        self.controller = self.c = controller

    def _build_controller(self, controller_cls):
        return controller_cls(self.services, self._all_subdomains)

    def _discover_controller(self):
        if not self.services:
            if self._repositories:
                self._set_services([GenerericService])

            elif self._active_records:
                self._set_repositories([GenerericRepository])
                self._set_services([GenerericService])

        return self._build_controller(GenericController)

    def update_daos(self, new_daos):
        for k, v in iteritems(new_daos):
            if k not in self._daos:
                self._daos[k] = v

    def set_subdomains(self, subdomains):
        self._all_subdomains.update(subdomains)

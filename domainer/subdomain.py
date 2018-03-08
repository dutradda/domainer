from six import iteritems

from domainer.exceptions import DomainerError
from domainer.layers.application.controller import GenericController
from domainer.layers.business.service import BaseService
from domainer.layers.data.repositories import BaseRepository


class Subdomain(object):

    def __init__(self, name, services=set(), active_records=set(),
                 repositories=set(), controller=None, daos={}):
        if (not services and not active_records and
                not repositories and controller is None):
            raise DomainerError("At least one of these arguments must be "
                                "setted: 'services', 'active_records', "
                                "'repositories' or 'controller'.")

        self._all_subdomains = {}
        self.name = name
        self._set_daos(daos)
        self._set_active_records(active_records)
        self._set_repositories(repositories)
        self._set_services(services)
        self._set_controller(controller)

    def _set_daos(self, daos):
        self._daos = {}
        self._daos.update(daos)

    def _set_active_records(self, active_records):
        self._active_records = {}

        for active_record in active_records:
            active_record_name = active_record.get_name()
            active_record_instance = active_record(self._daos)
            self._active_records[active_record_name] = active_record_instance

    def _set_repositories(self, repositories):
        self._repositories = {}
        for repository in repositories:
            self._set_repository(repository)

    def _set_repository(self, repository):
        repository_name = repository.get_name()
        repository_instance = repository(self._daos, self._active_records)
        self._repositories[repository_name] = repository_instance

    def _set_services(self, services):
        self.services = self.s = {}

        for service in services:
            self._set_service(service)

        else:
            if self._repositories:
                service_cls = BaseService.new_cls(self.name)
                self._set_service(service_cls)

            elif self._active_records:
                repository_cls = BaseRepository.new_cls(self.name)
                service_cls = BaseService.new_cls(self.name)
                self._set_repository(repository_cls)
                self._set_service(service_cls)

    def _set_service(self, service):
        service_name = service.get_name()
        service_instance = service(self._daos, self._active_records,
                                   self._repositories)
        self.services[service_name] = service_instance

    def _set_controller(self, controller_cls):
        if controller_cls is None:
            controller = self._build_controller(GenericController)
        else:
            controller = self._build_controller(controller_cls)

        self.controller = self.c = controller

    def _build_controller(self, controller_cls):
        return controller_cls(self.services, self._all_subdomains)

    def update_daos(self, new_daos):
        for k, v in iteritems(new_daos):
            if k not in self._daos:
                self._daos[k] = v

    def set_subdomains(self, subdomains):
        self._all_subdomains.update(subdomains)

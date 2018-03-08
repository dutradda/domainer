import mock
import pytest
from domainer.exceptions import DomainerError
from domainer.layers.application.controller import GenericController
from domainer.layers.business.service import BaseService
from domainer.layers.data.active_records.base import BaseActiveRecord
from domainer.layers.data.repositories import BaseRepository
from domainer.subdomain import Subdomain


def test_init_with_controller():
    MyController = type('MyController', (GenericController,), {})
    subdomain = Subdomain('core', controller=MyController)
    assert isinstance(subdomain.controller, MyController)


def test_init_creating_controllers_only_with_services():
    MyService = type('MyService', (BaseService,), {})
    subdomain = Subdomain('core', services=[MyService])
    assert len(subdomain.controller.services) == 1
    assert isinstance(subdomain.controller.services['my_service'], MyService)


def test_init_creating_controllers_only_with_active_records():
    MyActiveRecord = type('MyActiveRecord', (BaseActiveRecord,), {})
    subdomain = Subdomain('core', active_records=[MyActiveRecord])
    controller = subdomain.controller
    assert isinstance(controller.services['core_service']
                      .active_records['my_active_record'],
                      MyActiveRecord)


def test_init_creating_controllers_only_with_repositories():
    MyRepository = type('MyRepository', (BaseRepository,), {})
    subdomain = Subdomain('core', repositories=[MyRepository])
    controller = subdomain.controller
    assert isinstance(controller.services['core_service']
                      .repositories['my_repository'],
                      MyRepository)


def test_init_error_insuficient_arguments():
    with pytest.raises(DomainerError) as exc_info:
        Subdomain('core')

    assert exc_info.value.args == (
        "At least one of these arguments must be "
        "setted: 'services', 'active_records', "
        "'repositories' or 'controller'.",
    )

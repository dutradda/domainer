import mock
import pytest

from domainer.exceptions import DomainerError
from domainer.subdomain import Subdomain
from domainer.layers.business.service import BaseService


def test_create_controllers_only_with_services():
    class MyService(BaseService):
        pass

    subdomain = Subdomain('core', services=[MyService])
    assert len(subdomain.controller.services) == 1
    assert isinstance(subdomain.controller.services['MyService'],
                      MyService)


def test_error_insuficient_arguments():
    with pytest.raises(DomainerError) as exc_info:
        Subdomain('core')

    assert exc_info.value.args == (
        "At least one of these arguments must be "
        "setted: 'services', 'active_records', "
        "'repositories' or 'controller'.",
    )


def test_create_controllers_only_with_active_records():
    active_record = mock.MagicMock(name='core_active_record')
    subdomain = Subdomain('core', active_records=[active_record])
    controller = subdomain.controller
    print(controller.services)
    assert controller.services['core_active_record_service'] \
           .active_records['core_active_record'] == active_record


def test_error_not_found_suitable_controllers():
    with pytest.raises(Exception) as exc_info:
        Subdomain('core')

    assert exc_info.value.args == ('Domainer c',)

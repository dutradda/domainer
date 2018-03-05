import mock
import pytest

from domainer.exceptions import DomainerError
from domainer.subdomain import Subdomain


def test_create_controllers_only_with_services():
    service = mock.MagicMock(name='core_service')
    subdomain = Subdomain('core', services=[service])
    controller = list(subdomain.controllers)[0]
    assert controller.services == {'core_service': service}


def test_error_insuficient_arguments():
    with pytest.raises(DomainerError) as exc_info:
        Subdomain('core')

    assert exc_info.value.args == (
        "At least one of these arguments must be "
        "setted: 'services', 'active_records' or "
        "'controllers'.",
    )


def test_create_controllers_only_with_active_records():
    active_record = mock.MagicMock(name='core_active_record')
    subdomain = Subdomain('core', active_records=[active_record])
    controller = list(subdomain.controllers)[0]
    assert controller.services['core_active_record_service'] \
           .active_records['core_active_record'] == active_record


def test_error_not_found_suitable_controllers():
    with pytest.raises(Exception) as exc_info:
        Subdomain('core')

    assert exc_info.value.args == ('Domainer c',)

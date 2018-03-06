import mock
import pytest

from domainer.domain import Domain


@pytest.fixture
def core_subdomain():
    core_subdomain = mock.MagicMock()
    core_subdomain.name = 'core_subdomain'
    return core_subdomain


def test_subdomains_as_attributes(core_subdomain):
    domain = Domain(core_subdomain)
    assert domain.core_subdomain == core_subdomain


def test_set_daos(core_subdomain):
    daos = {'test': mock.MagicMock()}
    domain = Domain(core_subdomain, daos=daos)
    assert core_subdomain.update_daos.call_args_list == [mock.call(daos)]

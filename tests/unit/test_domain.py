import mock
import pytest
from domainer.domain import Domain
from domainer.subdomain import Subdomain


@pytest.fixture
def core_subdomain():
    return Subdomain('core', controller=mock.MagicMock())


def test_subdomains_as_attributes(core_subdomain):
    domain = Domain(core_subdomain)
    assert domain.core == core_subdomain


def test_subdomains_set_daos(core_subdomain):
    daos = {'test': mock.MagicMock()}
    domain = Domain(core_subdomain, daos=daos)
    assert domain.core._daos == daos

import mock

from domainer.domain import Domain


def test_subdomains_as_attributes():
    core_domain = mock.MagicMock(name='core_domain')
    domain = Domain(core_domain)
    assert domain.core_domain == core_domain


def test_set_daos():
    core_domain = mock.MagicMock(name='core_domain')
    daos = {'test': mock.MagicMock()}
    domain = Domain(core_domain, daos=daos)
    assert core_domain.set_daos.calls_args_list == [mock.call(daos)]

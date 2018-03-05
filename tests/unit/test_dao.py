import mock

from domainer.layers.data.daos.factory import DAOsFactory
from domainer.layers.data.daos.relational import RelationalDao
from domainer.layers.data.daos.key_value.redis import RedisDao
from domainer.layers.data.daos.document.elasticsearch import ElasticSearchDao


def test_factory_make_relational():
    relational_dao = DAOsFactory.make_relational('')
    assert isinstance(relational_dao, RelationalDao)


def test_factory_make_key_value():
    relational_dao = DAOsFactory.make_key_value('')
    assert isinstance(relational_dao, RedisDao)


def test_factory_make_document():
    relational_dao = DAOsFactory.make_document('')
    assert isinstance(relational_dao, ElasticSearchDao)

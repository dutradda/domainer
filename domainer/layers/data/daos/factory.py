from domainer.layers.data.daos.document.elasticsearch import ElasticSearchDao
from domainer.layers.data.daos.key_value.redis import RedisDao
from domainer.layers.data.daos.relational import RelationalDao


class DAOsFactory(object):

    @classmethod
    def make_relational(cls, url):
        return RelationalDao()

    @classmethod
    def make_key_value(cls, url):
        return RedisDao()

    @classmethod
    def make_document(cls, url):
        return ElasticSearchDao()

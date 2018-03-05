import sqlalchemy as sa

from domainer import Domain, Subdomain, RelationalActiveRecord, DAOsFactory


class ProductsActiveRecord(RelationalActiveRecord):
    __tablename__ = 'products'
    __enable_replication__ = True

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    sku = sa.Column(sa.String(8), nullable=False, unique=True)
    name = sa.Column(sa.String(255), nullable=False, unique=True)
    value = sa.Column(sa.Float(), nullable=False)

products_subdomain = Subdomain(active_records=[ProductsActiveRecord])
relational_dao = DAOsFactory.make_relational('sqlite:///')
key_value_dao = DAOsFactory.make_key_value('sqlite:///')
document_dao = DAOsFactory.make_document('localhost:9200')
daos_map = {
    'relational': relational_dao,
    'key_value': key_value_dao,
    'document': document_dao
}
store = Domain(products_subdomain, daos=daos_map)

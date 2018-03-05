import sqlalchemy as sa

from domainer import Domain, Subdomain, RelationalActiveRecord, DAOsFactory


class ProductsActiveRecord(RelationalActiveRecord):
    __tablename__ = 'products'

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    sku = sa.Column(sa.String(8), nullable=False, unique=True)
    name = sa.Column(sa.String(255), nullable=False, unique=True)
    value = sa.Column(sa.Float(), nullable=False)

products_subdomain = Subdomain(active_records=[ProductsActiveRecord])
key_value_dao = DAOsFactory.make_key_value('localhost:6379')
store = Domain(products_subdomain, daos={'main': key_value_dao})

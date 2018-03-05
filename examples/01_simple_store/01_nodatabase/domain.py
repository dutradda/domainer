from domainer import Domain, Subdomain, Service


class ProductsService(Service):

    products = []

    def get(self):
        return type(self).products

    def insert(self, product):
        type(self).products.append(product)
        return {'message': 'success'}


products_subdomain = Subdomain('products', services=[ProductsService])
store = Domain(products_subdomain)



class GenericController(object):

    def __init__(self, services, subdomains):
        self.services = services
        self.subdomains = self.sd = {
            subdomain.name: subdomain for subdomain in subdomains
        }

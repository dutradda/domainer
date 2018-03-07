

class GenericController(object):
    
    def __init__(self, services=None, subdomains=None):
        if services is None:
            services = {}

        if subdomains is None:
            subdomains = {}

        self.services = services
        self.subdomains = self.sd = {
            subdomain.name: subdomain for subdomain in subdomains
        }

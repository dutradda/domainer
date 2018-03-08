from six import itervalues


class Domain(object):

    def __init__(self, core_subdomain, support_subdomains=set(),
                 generic_subdomains=set(), daos=None):
        self._core_subdomain = core_subdomain
        self._support_subdomains = support_subdomains
        self._generic_subdomains = generic_subdomains
        self.all_subdomains = {}
        self._set_all_subdomains()
        if daos is not None:
            self.set_daos(daos)
        self._set_attributes()

    def _set_all_subdomains(self):
        all_subdomains = set([self._core_subdomain])
        all_subdomains.update(self._support_subdomains,
                              self._generic_subdomains)

        for subdomain in all_subdomains:
            self.all_subdomains[subdomain.name] = subdomain

        for subdomain in all_subdomains:
            subdomain.set_subdomains(self.all_subdomains)

    def set_daos(self, daos):
        for subdomain in itervalues(self.all_subdomains):
            subdomain.update_daos(daos)

    def _set_attributes(self):
        for subdomain in itervalues(self.all_subdomains):
            setattr(self, subdomain.name, subdomain)



class Domain(object):

    def __init__(self, core_subdomain, support_subdomains=set(),
                 generic_subdomains=set()):
        self._core_subdomain = core_subdomain
        self._support_subdomains = support_subdomains
        self._generic_subdomains = generic_subdomains

    def configure_environment(self):
        pass

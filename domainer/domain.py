

class Domain(object):

    def __init__(self, core_subdomain, support_subdomains=set(), generic_subdomains=set(),
                 description=None, title=None, version='1.0.0', common_spec_definitions=None,
                 spec_template=None):
        self._core_subdomain = core_subdomain
        self._support_subdomains = support_subdomains
        self._generic_subdomains = generic_subdomains
        self._title = title
        self._version = version
        self._description = description
        self._common_definitions = common_definitions

    def get_swagger_spec(self):
        pass


def normalize_all_of_refs(object_, deref):
    new_object = {}
    for key, value in iteritems(object_):
        value = deref(value)
        if key == 'allOf':
            for all_of_i in value:
                for key_i, value_i in iteritems(deref(all_of_i)):
                    new_object[key_i] = deref(value_i)
        else:
            new_object[key] = value

    return new_object

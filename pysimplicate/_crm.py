def organisation(self):
    result = self.call('/crm/organization')
    return result


def person(self, filter={}):
    url = '/crm/person'
    for field in ('first_name', 'last_name'):
        if field in filter.keys():
            url = self.add_url_param(url, field, filter[field])
    result = self.call(url)
    return result

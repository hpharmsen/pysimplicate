def organisation(self):
    result = self.call('/crm/organization')
    return result


def persons(self, first_name: str = '', last_name: str = ''):
    url = '/crm/person'
    if first_name:
        url = self.add_url_param(url, 'first_name', first_name)
    if last_name:
        self.add_url_param(url, 'last_name', last_name)
    result = self.call(url)
    return result

import sys


def employee(self, filter={}):
    url = '/hrm/employee'

    fields = ('first_name', 'last_name', 'employment_status')
    self.check_filter( 'employee', fields, filter )
    for field in fields:
        if field in filter.keys():
            # value = '1' if field=='active' else filter[field]
            url = self.add_url_param(url, field, filter[field])

    result = self.call(url)
    return result

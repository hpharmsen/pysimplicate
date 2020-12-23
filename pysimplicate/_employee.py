def employee(self, filter):
    url = '/hrm/employee'

    for field in ('first_name', 'last_name', 'employment_status'):
        if field in filter.keys():
            #value = '1' if field=='active' else filter[field]
            url = self.add_url_param(url, field, filter[field])

    result = self.call(url)
    return result

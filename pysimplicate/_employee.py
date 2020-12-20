def employees(self, first_name: str = '', last_name: str = '', active: bool = True):
    url = '/hrm/employee'  # ?name[gt]=&[status.label]=active
    if active:
        url = self.add_url_param(url, 'employment_status', 'active')
    if first_name:
        url = self.add_url_param(url, 'q[first_name]', first_name)
    if last_name:
        self.add_url_param(url, 'q[last_name]', last_name)
    result = self.call(url)
    return result

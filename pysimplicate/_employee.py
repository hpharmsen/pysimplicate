def employee(self, filter={}):
    url = '/hrm/employee'
    fields = ('name', 'first_name', 'last_name', 'employment_status')
    return self.composed_call( url, fields, filter)


def organisation(self):
    result = self.call('/crm/organization')
    return result


def person(self, filter={}):
    url = '/crm/person'
    fields = ('first_name','last_name')
    return self.composed_call( url, fields, filter)

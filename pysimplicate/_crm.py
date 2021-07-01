def organisation(self):
    result = self.call('/crm/organization')
    return result


def person(self, filter={}):
    url = '/crm/person'
    fields = ('first_name', 'family_name', 'full_name', 'work_email')
    return self.composed_call(url, fields, filter)

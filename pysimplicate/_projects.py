def project(self, filter={}):
    url = '/projects/project?sort=-updated_at'
    # fields = {'from_date':'modified',
    #           'until_date':'created',
    #           'status':'project_status.id',
    #           'active':'active'}

    for field in ('from_date', 'until_date', 'status', 'active', 'project_number'):
        if field in filter.keys():
            value = filter[field]
            if field == 'from_date':
                url = self.add_url_param(url, 'modified', value, 'ge')
            elif field == 'until_date':
                url = self.add_url_param(url, 'created', value, 'le')
            elif field == 'status':
                status_options = self.projectstatus_dict().keys()
                assert value in status_options, f"Status can only be one of {status_options}"
                url = self.add_url_param(url, 'project_status.id', self.projectstatus_dict()[value])
            elif field == 'active' and value:
                url = self.add_url_param(url, 'project_status.id', self.projectstatus_dict()['tab_pactive'])
            else:
                url = self.add_url_param(url, field, value)
    result = self.call(url)
    return result


def projectstatus(self):
    url = '/projects/projectstatus'
    result = self.call(url)
    return result


def projectstatus_dict(self):
    # Retrieves the list of project statusses and caches it
    if not hasattr(self, '_projectstatus_dict'):
        self._projectstatus_dict = {status['label']: status['id'] for status in self.projectstatus()}
    return self._projectstatus_dict


def project_by_name(self, name, filter={}):
    name = name.lower()
    return [
        p
        for p in self.project(filter)
        if p['name'].lower().count(name) or p['organization']['name'].lower().count(name)
    ]


# Diensten
def service(self, filter={}):
    url = '/projects/service'
    fields = ('project_id', 'status', 'track_hours')
    return self.composed_call(url, fields, filter)


# Kostensoorten
def purchasetypes(self):
    url = '/projects/purchasetype'
    result = self.call(url)
    return result

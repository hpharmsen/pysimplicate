def project(self, filter):
    url = '/projects/project?sort=-updated_at'

    for field in ('from_date', 'until_date', 'status'):
        if field in filter.keys():
            value = filter[field]
            if field=='from_date':
                url = self.add_url_param(url, 'modified', value, 'ge')
            if field=='until_date':
                url = self.add_url_param(url, 'created', value, 'le')
            if field=='status':
                assert value in projectstatus_dict().keys(), "Status can only be one of {projectstatus_dict.keys()}"
                url = self.add_url_param(url, 'project_status.id', projectstatus_dict()[value])
    result = self.call(url)
    return result


def projectstatus(self):
    url = '/projects/projectstatus'
    result = self.call(url)
    return result


def projectstatus_dict(self):
    # Retrieves the list of project statusses and caches it
    if not hasattr(self, '_projectstatus_dict'):
        self._project_statusdict = {status['label']: status['id'] for status in self.project_status()}
    return self._projectstatus_dict

# Diensten
def service(self):
    url = '/projects/service'
    result = self.call(url)
    return result

# Kostensoorten
def purchasetypes(self):
    url = '/projects/purchasetype'
    result = self.call(url)
    return result

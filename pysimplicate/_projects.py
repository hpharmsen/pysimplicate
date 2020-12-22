def projects(self, from_date: str = '', until_date: str = '', status: str = ''):
    url = '/projects/project?sort=-updated_at'
    if from_date:
        url = self.add_url_param(url, 'modified', from_date, 'ge')
    if until_date:
        url = self.add_url_param(url, 'created', until_date, 'le')
    if status:
        status_dict = self.project_status()
        assert status in status_dict.keys, "Status can only be one of {status_dict.keys}"
        url = self.add_url_param(url, '&q[project_status.id]', status_dict[status] )
    result = self.call(url)
    return result


def projectstatus(self):
    url = '/projects/projectstatus'
    result = self.call(url)
    return result

def project_status_options(self):
    # Retrieves the list of project statusses and caches it
    if not hasattr(self,'_project_status_dict'):
        self._project_status_dict = {status['label']:status['id'] for status in self.project_status()}
    return self._project_status_dict


def service(self):
    url = '/projects/service'
    result = self.call(url)
    return result


# Kostensoorten
def purchasetypes(self):
    url = '/projects/purchasetype'
    result = self.call(url)
    return result

def projects(self, from_date: str = '', until_date: str = '', status: str = ''):
    url = '/projects/project?sort=-updated_at'
    if from_date:
        url += '&q[modified][ge]=' + from_date
    if until_date:
        url += '&q[created][le]=' + until_date
    if (
        status
    ):  # !! Dit werkt niet helaas. URL is '/projects/project?sort=-updated_at&q[modified][ge]=2019-01-01&q[created][le]=2019-07-01&q[project_status.label]=tab_pactive'
        assert status in ('active', 'closed'), "Status can only be 'active' or 'closed'"
        url += '&q[project_status.label]=tab_p' + status
    result = self.call(url)
    return result


def service(self):
    url = '/projects/service'
    result = self.call(url)
    return result


# Kostensoorten
def purchasetypes(self):
    url = '/projects/purchasetype'
    result = self.call(url)
    return result

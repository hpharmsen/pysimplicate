def hours_types(self):
    url = '/hours/hourstype'
    result = self.call(url)
    return {d['id']: {'type': d['type'], 'tariff': d['tariff'], 'label': d['label']} for d in result}


def hours_data(
    self,
    project: str = None,
    service: str = None,
    label: str = None,
    revenue_group_id: str = None,
    hourstype: str = None,
    employee: str = None,
    from_date: str = '',
    until_date: str = '',
):
    url = '/hours/hours?sort=start_date'
    if project:
        url = self.add_url_param(url, 'project.project_number', project)
    if service:
        url = self.add_url_param(url, 'projectservice.name', service)
    if label:
        url = self.add_url_param(url, 'type.label', label)
    if revenue_group_id:
        url = self.add_url_param(url, 'projectservice.revenue_group_id', revenue_group_id)
    if hourstype:
        url = self.add_url_param(url, 'type.label', hourstype)
    if employee:
        url = self.add_url_param(url, 'employee.name', employee)
    if from_date:
        url = self.add_url_param(url, 'start_date', from_date, 'ge')
    if until_date:
        url = self.add_url_param(url, 'start_date', until_date, 'le')
    result = self.call(url)
    return result


def hours_data_simplified(
    self,
    project: str = None,
    service: str = None,
    label: str = None,
    revenue_group_id: str = None,
    hourstype: str = None,
    employee: str = None,
    from_date: str = '',
    until_date: str = '',
):
    data = self.hours_data(project, service, label, revenue_group_id, hourstype, employee, from_date, until_date)
    result = [
        {
            'employee': d['employee']['name'],
            'project_name': d['project']['name'],
            'project_number': d['project']['project_number'],
            'service': d['projectservice']['name'],
            'type': d['type']['type'],
            'label': d['type']['label'],
            'billable': d['billable'],
            'tariff': d['tariff'],
            'hours': d['hours'],
            'start_date': d['start_date'],
            'status': d['status'],
            'corrections': d['corrections'],
        }
        for d in data
    ]
    return result


def hours_count(
    self,
    project: str = None,
    service: str = None,
    label: str = None,
    revenue_group_id: str = None,
    hourstype: str = None,
    employee: str = None,
    from_date: str = '',
    until_date: str = '',
):
    hours = self.hours_data(project, service, label, revenue_group_id, hourstype, employee, from_date, until_date)
    # todo: Correcties eraf trekken
    return sum([d['hours'] for d in hours])


def turnover(
    self,
    project: str = None,
    service: str = None,
    label: str = None,
    revenue_group_id: str = None,
    hourstype: str = None,
    employee: str = None,
    from_date: str = '',
    until_date: str = '',
):
    hours = self.hours_data(project, service, label, revenue_group_id, hourstype, employee, from_date, until_date)
    # todo:  Correcties eraf trekken
    if not hours:
        # print( 'Could not calculate hours', locals())
        return 0
    for h in hours:
        if h['corrections']['amount'] > 0:
            corrections = h['corrections']['amount']
            corrections += 0

    return sum([d['hours'] * d['tariff'] for d in hours])

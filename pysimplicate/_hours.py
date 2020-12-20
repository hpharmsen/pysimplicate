def hours_types(self):
    url = '/hours/hourstype'
    result = self.call(url)
    return {d['id']: {'type': d['type'], 'tariff': d['tariff'], 'label': d['label']} for d in result}


def hours_data(self, project: str = None, service: str = None, label: str = None, revenue_group_id: str = None,
               hourstype: str = None, employee: str = None,
               from_date: str = '', until_date: str = ''):
    url = '/hours/hours?sort=start_date'
    if project:
        url += '&q[project.project_number]=' + project
    if service:
        url += '&q[projectservice.name]=' + service
    if label:
        url += '&q[type.label]=' + label
    if revenue_group_id:
        url += '&q[projectservice.revenue_group_id]=' + revenue_group_id
    if hourstype:
        url += '&q[type.label]=' + hourstype
    if employee:
        url += '&q[employee.name]=' + employee
    if from_date:
        url += '&q[start_date][ge]=' + from_date
    if until_date:
        url += '&q[start_date][le]=' + until_date
    result = self.call(url)
    return result


def hours_data_simplified(self, project: str = None, service: str = None, label: str = None,
                          revenue_group_id: str = None,
                          hourstype: str = None, employee: str = None, from_date: str = '', until_date: str = ''):
    data = self.hours_data(project, service, label, revenue_group_id, hourstype, employee, from_date, until_date)
    result = [{'employee': d['employee']['name'],
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
               'corrections': d['corrections']
               } for d in data]
    return result


def hours_count(self, project: str = None, service: str = None, label: str = None, revenue_group_id: str = None,
                hourstype: str = None, employee: str = None, from_date: str = '', until_date: str = ''):
    hours = self.hours_data(project, service, label, revenue_group_id, hourstype, employee, from_date, until_date)
    # todo: Correcties eraf trekken
    return sum([d['hours'] for d in hours])


def turnover(self, project: str = None, service: str = None, label: str = None, revenue_group_id: str = None,
             hourstype: str = None, employee: str = None, from_date: str = '', until_date: str = ''):
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

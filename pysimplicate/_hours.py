def hourstype(self):
    url = '/hours/hourstype'
    result = self.call(url)
    return result


def hourstype_simple(self):
    result = self.hourstype()
    return {d['id']: {'type': d['type'], 'tariff': d['tariff'], 'label': d['label']} for d in result}


def hours(self, filter={}):
    url = '/hours/hours?sort=start_date'

    fields = {
        'employee_id': 'employee.id',
        'employee_name': 'employee.name',
        'project': 'project.project_number',
        'service': 'projectservice.name',
        'hourstype': 'type.label',
        'start_date': 'start_date',
        'end_date': 'start_date',
        'revenuegroup_id': 'projectservice.revenue_group_id',
    }

    return self.composed_call(url, fields, filter)


def hours_since(self, since, filter={}):
    filter['updated_at'] = since
    return hours(self, filter)


def hours_simple(self, filter={}):
    data = self.hours(filter)
    result = [
        {
            'employee': d['employee']['name'],
            'project_id': d['project']['id'],
            'project_name': d['project']['name'],
            'project_number': d['project'].get('project_number', ''),
            'service': d['projectservice']['name'],
            'type': d['type']['type'],
            'label': d['type']['label'],
            'billable': d['billable'],
            'tariff': d['tariff'],
            'service_tariff': d['type']['tariff'],
            'hours': d['hours'],
            'start_date': d['start_date'],
            'status': d.get('status', ''),
            'corrections': d['corrections'],
            'note': d.get('note', ''),
        }
        for d in data
    ]
    return result


def hours_count(self, filter={}):
    hours = self.hours(filter)
    return sum([d['hours'] + d['corrections']['amount'] for d in hours])


def turnover(self, filter={}):
    hours = self.hours(filter)
    if not hours:
        # print( 'Could not calculate hours', locals())
        return 0
    for h in hours:
        h['hours'] += h['corrections']['amount']

    return sum([d['hours'] * d['tariff'] for d in hours])


def book_hours(self, fields):
    url = '/hours/hours'
    return self.post(url, fields)


def hours_approval(self, fields):
    url = '/hours/approval'
    return self.post(url, fields)


def delete_hours(self, id):
    url = f'/hours/hours/{id}'
    return self.delete(url)

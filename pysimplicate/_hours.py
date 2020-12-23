def hourstype(self):
    url = '/hours/hourstype'
    result = self.call(url)
    return result

def hourstype_simple(self):
    result = self.hourstype()
    return {d['id']: {'type': d['type'], 'tariff': d['tariff'], 'label': d['label']} for d in result}


def hours(self, filter):
    url = '/hours/hours?sort=start_date'

    fields = { 'employee_name':'employee.name',
               'project':'project.project_number',
               'service':'projectservice.name',
               'hourstype':'type.label',
               'start_date': 'start_date',
               'end_date':'end_date',
               'revenuegroup_id':'projectservice.revenue_group_id'}
    for field, extended_field in fields.items():
        if field in filter.keys():
            value = filter[field]
            operator = ''
            if field == 'start_date':
                operator = 'ge'
            elif field == 'end_date':
                operator = 'le'
            url = self.add_url_param(url, extended_field, value, operator)

    result = self.call(url)
    return result


def hours_simple(self, filter):
    data = self.hours(filter)
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


def hours_count(self, filter):
    hours = self.hours(filter)
    # todo: Correcties eraf trekken
    return sum([d['hours'] for d in hours])


def turnover(self, filter):
    hours = self.hours(filter)
    # todo:  Correcties eraf trekken
    if not hours:
        # print( 'Could not calculate hours', locals())
        return 0
    for h in hours:
        if h['corrections']['amount'] > 0:
            corrections = h['corrections']['amount']
            corrections += 0

    return sum([d['hours'] * d['tariff'] for d in hours])

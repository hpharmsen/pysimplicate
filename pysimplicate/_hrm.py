from beautiful_date import *


# Fetches all contracts
def contract(self):
    url = '/hrm/contract'
    result = self.call(url)
    return result


# Fetches all leave types
# Returns list of {id, employee, start_date, end_date, year, description}
def leave(self, filter={}):
    url = '/hrm/leave'
    fields = {
        'employee_name': 'employee.name',
        'year': 'year',
        'leavetype_label': 'leavetype.label',
        'affects_balance': 'leavetype.affects_balance',
        'start_date': 'start_date',
        'end_date': 'end_date',
    }
    for field, extended_field in fields.items():
        if field in filter.keys():
            value = filter[field]
            operator = ''
            if field == 'affects_balance':
                value = str(int(value))
            elif field == 'start_date':
                operator = 'ge'
            elif field == 'end_date':
                operator = 'le'
            url = self.add_url_param(url, extended_field, value, operator)

    result = self.call(url)
    return result


def leave_simple(self, filter={}):
    # Returns list of {employee_name, start_date, days, description}
    leaves = leave(self, filter)
    if not leaves:
        return False

    res = []
    for l in leaves:
        if not l.get('start_date'):
            continue
        start = _to_date(l['start_date'])
        days = l['hours'] / 8
        res += [
            {
                'id': l['id'],
                'name': l['employee']['name'],
                'start_day': start[:],
                'days': days,
                'description': l['description'],
            }
        ]
    return res


def _to_date(date: str):
    y, m, d = date.split()[0].split('-')
    return BeautifulDate(int(y), int(m), int(d))


# Fetches all leave types
# Returns list of {id, label, blocked, color, affects_balance}
def leavetype(self, show_blocked=False):
    url = '/hrm/leavetype'
    if not show_blocked:
        url = self.add_url_param(url, 'blocked', 'False')
    result = self.call(url)
    return result


# Fetches all leave balances for employees
# Returns list of {employee (id, name), balance (in hours), year, leave_type (id, label)}
def leavebalance(self, filter={}):
    url = '/hrm/leavebalance'
    fields = {
        'employee_name': 'employee.name',
        'year': 'year',
        'leavetype_label': 'leavetype.label',
        'affects_balance': 'leavetype.affects_balance',
    }
    for field, extended_field in fields.items():
        if field in filter.keys():
            value = filter[field]
            if field == 'affects_balance':
                value = str(int(value))
            url = self.add_url_param(url, extended_field, value)

    result = self.call(url)
    return result

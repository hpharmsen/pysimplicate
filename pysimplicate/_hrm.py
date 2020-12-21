from beautiful_date import *

# Fetches all leave types
# Returns list of {id, employee, start_date, end_date, year, description}
def leave(self, employee_name=None, year=None, from_date:str=None, until_date:str=None, leavetype_label=None, affects_balance=None):
    url = '/hrm/leave'
    if employee_name:
        url = self.add_url_param(url, 'q[employee.name]', employee_name)
    if year:
        url = self.add_url_param(url, 'q[year]', str(year))
    if leavetype_label:
        url = self.add_url_param(url, 'q[leavetype.label]', leavetype_label)
    if affects_balance != None:
        url = self.add_url_param(url, 'q[leavetype.affects_balance]', str(int(affects_balance)))
    if from_date:
        url += '&q[start_date][ge]=' + from_date
    if until_date:
        url += '&q[end_date][le]=' + until_date

    result = self.call(url)
    return result


def leave_simplified(self, employee_name=None, year=None, from_date:str=None, until_date:str=None, leavetype_label=None, affects_balance=None):
    # Returns list of {employee_name, start_date, days, description}
    leaves = leave(self, employee_name, year, from_date, until_date, leavetype_label, affects_balance)
    if not leaves:
        return False

    res = []
    for l in leaves:
        if not l.get('start_date'):
            continue
        start = _to_date(l['start_date'])
        end = _to_date(l['end_date'])
        days = (end - start).days
        res += [{'name': l['employee']['name'], 'start_day': start[:], 'days': days, 'description': l['description']}]
    return res


def _to_date(date: str):
    y, m, d = date.split()[0].split('-')
    return BeautifulDate(int(y), int(m), int(d))


# Fetches all leave types
# Returns list of {id, label, blocked, color, affects_balance}
def leavetypes(self, show_blocked=False):
    url = '/hrm/leavetype'
    if not show_blocked:
        url = self.add_url_param(url, 'q[blocked]', 'False')
    result = self.call(url)
    return result


# Fetches all leave balances for employees
# Returns list of {employee (id, name), balance (in hours), year, leave_type (id, label)}
def leavebalance(self, employee_name=None, year=None, leavetype_label=None, affects_balance=None):
    url = '/hrm/leavebalance'
    if employee_name:
        url = self.add_url_param(url, 'q[employee.name]', employee_name)
    if year:
        url = self.add_url_param(url, 'q[year]', str(year))
    if leavetype_label:
        url = self.add_url_param(url, 'q[leavetype.label]', leavetype_label)
    if affects_balance != None:
        url = self.add_url_param(url, 'q[leavetype.affects_balance]', str(int(affects_balance)))
    result = self.call(url)
    return result

import datetime

# Fetches all contracts
def contract(self, filter={}):
    url = '/hrm/contract'
    fields = {'employee_name': 'employee.name'}
    result = self.composed_call(url, fields, filter)
    return result


def employee(self, filter={}):
    url = '/hrm/employee'
    fields = {
        'full_name': 'person.full_name',
        'name': 'name',
        'status': 'status.label',
        'work_email': 'work_email',
        'function': 'function',
    }
    result = self.composed_call(url, fields, filter)
    return result


# Time tables
def timetable(self, filter={}):
    url = '/hrm/timetable'
    fields = {
        'employee_name': 'employee.name',
        'start_date': 'start_date',
        'end_date': 'start_date',
    }
    return self.composed_call(url, fields, filter)
    # self.check_filter('timetable', fields, filter)
    # for field, extended_field in fields.items():
    #     if field in filter.keys():
    #         value = filter[field]
    #         operator = ''
    #         if field == 'start_date':
    #             operator = 'ge'
    #         elif field == 'end_date':
    #             operator = 'le'
    #         url = self.add_url_param(url, extended_field, value, operator)
    #
    # result = self.call(url)
    # return result


def timetable_simple(self, employee_name):
    # in: employee name
    # out: [(8, 8), (8, 8), (8, 8), (8, 8), (8, 8), (0, 0), (0, 0)]
    table = self.timetable({'employee_name': employee_name})[-1]
    res = [(table['even_week'][f'day_{i}']['hours'], table['odd_week'][f'day_{i}']['hours']) for i in range(1, 8)]
    return res


def timetable_today(self, employee_name):
    day_of_week = datetime.datetime.today().weekday()  # weekday is 0 for Monday
    week_number = datetime.datetime.today().isocalendar()[1]
    index = week_number % 2
    table = self.timetable_simple(employee_name)
    res = table[day_of_week][index]
    return res


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
        'end_date': 'start_date',
    }
    return self.composed_call(url, fields, filter)


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
    return self.composed_call(url, fields, filter)


def absence(self, filter={}):
    url = '/hrm/absence'
    fields = {
        'employee_name': 'employee.name',
        'year': 'year',
        'start_date': 'start_date',
        'end_date': 'end_date',
    }
    return self.composed_call(url, fields, filter)

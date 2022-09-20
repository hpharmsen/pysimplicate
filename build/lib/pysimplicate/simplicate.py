import time
import requests
import datetime
import pandas as pd

DATE_FORMAT = '%Y-%m-%d'

# TODO: /projects/project naar composed_call


class Simplicate:
    def __init__(self, subdomain, api_key, api_secret):
        self.subdomain = subdomain
        self.api_key = api_key
        self.api_secret = api_secret
        self.error = ''  # To store error messages
        self.status_code = 0

    from ._crm import organisation, person
    from ._hours import (
        hourstype,
        hourstype_simple,
        hours,
        hours_since,
        hours_simple,
        hours_count,
        turnover,
        book_hours,
        hours_approval,
        delete_hours,
    )
    from ._hrm import (
        contract,
        employee,
        leave,
        leave_simple,
        leavetype,
        leavebalance,
        timetable,
        timetable_simple,
        timetable_today,
        absence,
    )
    from ._invoices import invoice, invoice_per_year, invoiced_per_service, invoice_lines_per_year
    from ._projects import project, project_by_name, projectstatus, projectstatus_dict, service, purchasetypes
    from ._sales import revenuegroup, revenuegroup_dict, sales, sales_flat
    from ._service import defaultservice

    def call(self, url_path: str):
        my_headers = {'Authentication-Key': self.api_key, 'Authentication-Secret': self.api_secret}
        url = f'https://{ self.subdomain}.simplicate.nl/api/v2{url_path}'
        delimiter = '&' if url.count('?') else '?'
        url += delimiter + 'metadata=count&offset='
        result = []
        offset = 0
        connection_reset_tries = 0
        while True:
            try:
                url2 = url + str(offset)
                while True:
                    response = requests.get(url2, headers=my_headers, timeout=15)
                    if response.status_code == 429:
                        time.sleep(10)  # Rate limit exceeded. Wait 10 secs and try again
                        continue
                    break
                self.status_code = response.status_code
                response.raise_for_status()
                # Code here will only run if the request is successful
                json = response.json()
                if type(json['data']) == list:
                    result += json['data']
                    offset += 100
                    if offset < json['metadata']['count']:
                        continue
                else:
                    result = json['data']
                self.error = ''
                return result
            except requests.exceptions.HTTPError as errh:
                print(errh)
                self.error = errh
            except requests.exceptions.ConnectionError as errc:
                connection_reset_tries += 1
                if connection_reset_tries <= 2:
                    continue  # Try again
                self.error = errc
                print(errc)
            except requests.exceptions.Timeout as errt:
                connection_reset_tries += 1
                if connection_reset_tries <= 2:
                    continue  # Try again
                self.error = errt
                print(errt)
            except requests.exceptions.RequestException as err:
                self.error = err
                print(err)
            # print(url2)
            # try:
            #    print(response.content)
            # except:
            #    pass  # There was no respons yet
            return False

    def post(self, url_path: str, post_fields: dict):
        headers = {
            'Authentication-Key': self.api_key,
            'Authentication-Secret': self.api_secret,
            'Content-type': 'application/json',
            'Accept': 'text/plain',
        }
        url = f'https://{ self.subdomain}.simplicate.nl/api/v2{url_path}'
        if not post_fields.get('update_at'):
            post_fields['update_at'] = datetime.datetime.now().strftime(DATE_FORMAT)
        response = requests.post(url, json=post_fields, headers=headers)
        return response

    def put(self, url_path: str, put_fields: dict):
        headers = {
            'Authentication-Key': self.api_key,
            'Authentication-Secret': self.api_secret,
            'Content-type': 'application/json',
            'Accept': 'text/plain',
        }
        url = f'https://{ self.subdomain}.simplicate.nl/api/v2{url_path}'
        response = requests.put(url, json=put_fields, headers=headers)
        return response

    def delete(self, url_path: str):
        headers = {
            'Authentication-Key': self.api_key,
            'Authentication-Secret': self.api_secret,
            'Content-type': 'application/json',
            'Accept': 'text/plain',
        }
        url = f'https://{ self.subdomain}.simplicate.nl/api/v2{url_path}'
        response = requests.delete(url, headers=headers)
        return response

    def composed_call(self, url, fields, filter):
        if type(fields) == tuple:
            fields = {field: field for field in fields}
        fields['updated_at'] = 'updated_at'  # Default field

        if 'day' in filter.keys():
            day = filter['day']
            if type(day) != str:
                day = day.strftime(DATE_FORMAT)
            filter['start_date'] = day
            filter['end_date'] = (datetime.datetime.strptime(day, DATE_FORMAT) + datetime.timedelta(days=1)).strftime(
                DATE_FORMAT
            )
            del filter['day']

        self.check_filter(url, fields, filter)

        for field, extended_field in fields.items():
            if field in filter.keys():
                value = filter[field]
                operator = ''
                if field in ('start_date', 'from_date', 'updated_at'):
                    operator = 'ge'
                elif field in ('end_date', 'until_date'):
                    operator = 'lt'
                elif field == 'affects_balance':
                    value = str(int(value))
                url = self.add_url_param(url, extended_field, value, operator)

        result = self.call(url)
        return result

    def direct_call(self, url):
        my_headers = {'Authentication-Key': self.api_key, 'Authentication-Secret': self.api_secret}
        response = requests.get(url, headers=my_headers, timeout=15)
        response.raise_for_status()
        # Code here will only run if the request is successful
        # json = response.json()
        # return json
        return response.text

    def add_url_param(self, url, key, value, operator=''):
        # Adds parameter to the simplicate API url in the form: &q[key]=value or &q[key][operator]=value
        delimiter = '&' if url.count('?') else '?'
        operator = f'[{operator}]' if operator else ''
        return url + delimiter + f'q[{key}]' + operator + '=' + requests.utils.quote(str(value))

    def check_filter(self, function_name, fields, filter):
        # Checks if the keys in the passed filter are all supported by the function
        unused_keys = [k for k in filter.keys() if k not in fields]
        assert (
            not unused_keys
        ), f'parameter(s) {unused_keys} not supported by function {function_name}. Supported fields are {tuple(fields.keys())}'

    def to_pandas(self, function_result):
        def flatten_json(y):
            out = {}

            def flatten(x, name=''):
                if type(x) is dict:
                    for a in x:
                        flatten(x[a], name + a + '_')
                elif type(x) is list:
                    i = 0
                    for a in x:
                        flatten(a, name + str(i) + '_')
                        i += 1
                else:
                    out[name[:-1]] = x

            flatten(y)
            return out

        res = pd.DataFrame([flatten_json(a) for a in function_result])
        return res
